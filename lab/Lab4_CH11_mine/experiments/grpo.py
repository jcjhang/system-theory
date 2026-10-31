"""GRPO with LoRA starting from the merged SFT model."""
import argparse
import json
import os

import torch
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import GRPOConfig, GRPOTrainer

p = argparse.ArgumentParser()
p.add_argument("--model", default="runs/sft/merged")
p.add_argument("--out", default="runs/grpo_acc")
p.add_argument("--reward", default="accuracy", choices=["accuracy", "length_penalty", "step"])
p.add_argument("--start", type=int, default=2000)
p.add_argument("--n", type=int, default=1000)
p.add_argument("--max_steps", type=int, default=-1)
p.add_argument("--lr", type=float, default=2e-5)
p.add_argument("--beta", type=float, default=0.05)
p.add_argument("--num_gen", type=int, default=8)
p.add_argument("--max_new", type=int, default=256)
p.add_argument("--save_steps", type=int, default=125)
args = p.parse_args()

os.makedirs(args.out, exist_ok=True)
os.environ["GROUP_LOG"] = f"{args.out}/groups.jsonl"
from common import REWARDS, rl_dataset, setup_generation, setup_tokenizer  # noqa: E402

tok = setup_tokenizer(AutoTokenizer.from_pretrained(args.model))
tok.padding_side = "left"
model = AutoModelForCausalLM.from_pretrained(args.model, dtype=torch.bfloat16)
setup_generation(model, tok)

lora = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.0, task_type="CAUSAL_LM",
                  target_modules=["q_proj", "k_proj", "v_proj", "o_proj"])

cfg = GRPOConfig(
    output_dir=args.out, num_train_epochs=1, max_steps=args.max_steps,
    per_device_train_batch_size=args.num_gen, gradient_accumulation_steps=4,  # 4 prompts / step
    num_generations=args.num_gen, max_completion_length=args.max_new, temperature=0.8,
    learning_rate=args.lr, warmup_steps=0.05, beta=args.beta, epsilon=0.2,
    loss_type="grpo", scale_rewards="group",
    bf16=True, logging_steps=5, save_strategy="steps", save_steps=args.save_steps,
    report_to="tensorboard", seed=42,
)
trainer = GRPOTrainer(model=model, reward_funcs=REWARDS[args.reward], args=cfg,
                      train_dataset=rl_dataset(args.start, args.start + args.n),
                      processing_class=tok, peft_config=lora)
trainer.train()

merged = trainer.model.merge_and_unload()
merged.save_pretrained(f"{args.out}/merged")
tok.save_pretrained(f"{args.out}/merged")
json.dump({"log_history": trainer.state.log_history,
           "peak_mem_gb": torch.cuda.max_memory_allocated() / 2**30, "args": vars(args)},
          open(f"{args.out}/summary.json", "w"), indent=1)
print("peak mem GB", torch.cuda.max_memory_allocated() / 2**30)
