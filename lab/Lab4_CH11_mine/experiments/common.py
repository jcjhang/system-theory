"""Shared helpers: GSM8K formatting, answer extraction, reward functions."""
import json
import os
import re

from datasets import load_dataset

BASE_MODEL = "Qwen/Qwen3-0.6B-Base"
IM_END = "<|im_end|>"
# Base model never learned to emit <|im_end|>, so completions end with <|endoftext|> instead.
EOS = "<|endoftext|>"
PAD = "<|fim_pad|>"

PROMPT_TMPL = (
    "<|im_start|>system\nSolve the math problem step by step. "
    "End with 'Final Answer: <number>'.<|im_end|>\n"
    "<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant\n"
)


# ---------- data ----------
def gt_number(answer: str) -> str:
    return answer.split("####")[-1].strip().replace(",", "")


def gt_steps(answer: str) -> list[str]:
    body = answer.split("####")[0]
    body = re.sub(r"<<[^>]*>>", "", body)  # drop calculator annotations
    return [ln.strip() for ln in body.strip().split("\n") if ln.strip()]


def to_completion(answer: str) -> str:
    steps = gt_steps(answer)
    lines = ["Let me solve this step by step."]
    lines += [f"Step {i}: {s}" for i, s in enumerate(steps, 1)]
    lines.append(f"Final Answer: {gt_number(answer)}")
    return "\n".join(lines)


def load_gsm8k(split: str):
    return load_dataset("openai/gsm8k", "main", split=split)


def sft_dataset(n_start: int, n_end: int):
    ds = load_gsm8k("train").select(range(n_start, n_end))
    return ds.map(
        lambda x: {"prompt": PROMPT_TMPL.format(question=x["question"]),
                   "completion": to_completion(x["answer"])},
        remove_columns=ds.column_names,
    )


def rl_dataset(n_start: int, n_end: int):
    ds = load_gsm8k("train").select(range(n_start, n_end))
    return ds.map(
        lambda x: {"prompt": PROMPT_TMPL.format(question=x["question"]),
                   "ground_truth": gt_number(x["answer"])},
        remove_columns=ds.column_names,
    )


# ---------- answer parsing ----------
NUM_RE = r"-?\d[\d,]*\.?\d*"


def extract_answer(text: str):
    text = text.split(EOS)[0].split(IM_END)[0]
    m = re.search(r"Final Answer:\s*\$?\s*(" + NUM_RE + ")", text)
    if m:
        s = m.group(1)
    else:
        nums = re.findall(NUM_RE, text)
        if not nums:
            return None
        s = nums[-1]
    s = s.replace(",", "").rstrip(".")
    try:
        return float(s)
    except ValueError:
        return None


def is_correct(text: str, gt: str) -> bool:
    pred = extract_answer(text)
    return pred is not None and abs(pred - float(gt)) < 1e-4


def count_steps(text: str) -> int:
    return len(re.findall(r"Step \d+:", text))


def has_format(text: str) -> bool:
    return "Final Answer:" in text


# ---------- rewards (TRL signature: completions, **dataset columns) ----------
LENGTH_TARGET = 200   # chars
LENGTH_ALPHA = 0.001
STEP_BONUS = 0.1

_GROUP_LOG = os.environ.get("GROUP_LOG")  # jsonl path; logs every rollout group


def _log(prompts, completions, gts, rewards, name):
    if not _GROUP_LOG:
        return
    with open(_GROUP_LOG, "a") as f:
        f.write(json.dumps({"reward": name, "prompts": prompts, "completions": completions,
                            "ground_truth": gts, "rewards": rewards}) + "\n")


def accuracy_reward(completions, ground_truth, prompts=None, **kw):
    r = [1.0 if is_correct(c, g) else 0.0 for c, g in zip(completions, ground_truth)]
    _log(prompts, completions, ground_truth, r, "accuracy")
    return r


def length_penalty_reward(completions, ground_truth, prompts=None, **kw):
    r = []
    for c, g in zip(completions, ground_truth):
        if is_correct(c, g):
            r.append(max(0.0, 1.0 - LENGTH_ALPHA * max(0, len(c) - LENGTH_TARGET)))
        else:
            r.append(0.0)
    _log(prompts, completions, ground_truth, r, "length_penalty")
    return r


def step_reward(completions, ground_truth, prompts=None, **kw):
    r = [(1.0 + STEP_BONUS * count_steps(c)) if is_correct(c, g) else 0.0
         for c, g in zip(completions, ground_truth)]
    _log(prompts, completions, ground_truth, r, "step")
    return r


REWARDS = {"accuracy": accuracy_reward, "length_penalty": length_penalty_reward, "step": step_reward}


def setup_tokenizer(tok):
    tok.eos_token = EOS
    tok.pad_token = PAD  # must differ from EOS, otherwise EOS can get masked out of the labels
    return tok


def setup_generation(model, tok):
    gc = model.generation_config
    gc.eos_token_id = [tok.convert_tokens_to_ids(EOS), tok.convert_tokens_to_ids(IM_END)]
    gc.pad_token_id = tok.pad_token_id
