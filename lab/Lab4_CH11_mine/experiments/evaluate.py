"""Greedy evaluation on the first N GSM8K test questions (same prompt for every model)."""
import argparse
import json
import re
import time

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

from common import (BASE_MODEL, EOS, IM_END, PAD, PROMPT_TMPL, count_steps, extract_answer, gt_number,
                    gt_steps, has_format, is_correct, load_gsm8k, setup_generation,
                    setup_tokenizer)

p = argparse.ArgumentParser()
p.add_argument("--model", required=True)
p.add_argument("--adapter", default=None, help="optional LoRA checkpoint dir on top of --model")
p.add_argument("--name", required=True)
p.add_argument("--n", type=int, default=200)
p.add_argument("--bs", type=int, default=50)
p.add_argument("--max_new", type=int, default=400)
p.add_argument("--out", default="results")
args = p.parse_args()

tok = setup_tokenizer(AutoTokenizer.from_pretrained(BASE_MODEL))
tok.padding_side = "left"
model = AutoModelForCausalLM.from_pretrained(args.model, dtype=torch.bfloat16).cuda()
if args.adapter:
    model = PeftModel.from_pretrained(model, args.adapter).merge_and_unload()
model.eval()
setup_generation(model, tok)

ds = load_gsm8k("test").select(range(args.n))
ARITH = re.compile(r"(-?\d+(?:\.\d+)?)\s*([+\-*/x×])\s*(-?\d+(?:\.\d+)?)\s*=\s*(-?\d+(?:\.\d+)?)")


def wrong_arith(text):
    for a, op, b, c in ARITH.findall(text.replace(",", "")):
        a, b, c = float(a), float(b), float(c)
        v = {"+": a + b, "-": a - b, "*": a * b, "x": a * b, "×": a * b,
             "/": a / b if b else None}[op]
        if v is not None and abs(v - c) > 1e-2 * max(1, abs(v)):
            return True
    return False


def error_type(text):
    if not has_format(text):
        return "format"
    if wrong_arith(text):
        return "calculation"
    return "reasoning/understanding"


details, t0 = [], time.time()
for i in range(0, args.n, args.bs):
    batch = ds.select(range(i, min(i + args.bs, args.n)))
    prompts = [PROMPT_TMPL.format(question=q) for q in batch["question"]]
    enc = tok(prompts, return_tensors="pt", padding=True).to("cuda")
    with torch.no_grad():
        out = model.generate(**enc, max_new_tokens=args.max_new, do_sample=False)
    for j, ex in enumerate(batch):
        ids = out[j, enc["input_ids"].shape[1]:]
        text = tok.decode(ids, skip_special_tokens=False)
        text = text.split(EOS)[0].split(IM_END)[0].replace(PAD, "")
        gt = gt_number(ex["answer"])
        ok = is_correct(text, gt)
        details.append({
            "question": ex["question"], "ground_truth": gt, "output": text,
            "pred": extract_answer(text), "correct": ok, "format": has_format(text),
            "n_tokens": len(tok(text)["input_ids"]), "n_steps": count_steps(text),
            "gt_steps": len(gt_steps(ex["answer"])),
            "error_type": None if ok else error_type(text),
        })
    print(f"{len(details)}/{args.n}", flush=True)


def acc(rows):
    return sum(r["correct"] for r in rows) / len(rows) if rows else None


buckets = {"1-2": [r for r in details if r["gt_steps"] <= 2],
           "3-4": [r for r in details if 3 <= r["gt_steps"] <= 4],
           "5+": [r for r in details if r["gt_steps"] >= 5]}
errs = [r["error_type"] for r in details if not r["correct"]]
summary = {
    "name": args.name, "n": args.n,
    "accuracy": acc(details),
    "format_correctness": sum(r["format"] for r in details) / args.n,
    "avg_tokens": sum(r["n_tokens"] for r in details) / args.n,
    "avg_steps": sum(r["n_steps"] for r in details) / args.n,
    "accuracy_by_steps": {k: {"acc": acc(v), "n": len(v)} for k, v in buckets.items()},
    "error_types": {t: errs.count(t) for t in sorted(set(errs))},
    "eval_seconds": time.time() - t0,
    "peak_mem_gb": torch.cuda.max_memory_allocated() / 2**30,
}
print(json.dumps(summary, indent=1))
json.dump({"summary": summary, "details": details},
          open(f"{args.out}/eval_{args.name}.json", "w"), indent=1)
