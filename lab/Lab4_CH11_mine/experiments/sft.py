"""SFT with LoRA on GSM8K, then merge the adapter into a standalone model."""
import argparse
import json
import os

import torch
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTConfig, SFTTrainer

from common import BASE_MODEL, setup_generation, setup_tokenizer, sft_dataset

p = argparse.ArgumentParser()
p.add_argument("--out", default="runs/sft")
p.add_argument("--n", type=int, default=2000)
p.add_argument("--epochs", type=float, default=3)
p.add_argument("--bs", type=int, default=8)
p.add_argument("--lr", type=float, default=1e-4)
args = p.parse_args()

tok = setup_tokenizer(AutoTokenizer.from_pretrained(BASE_MODEL))
model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, dtype=torch.bfloat16)
setup_generation(model, tok)

lora = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, task_type="CAUSAL_LM",
                  target_modules=["q_proj", "k_proj", "v_proj", "o_proj"])

cfg = SFTConfig(
    output_dir=args.out, num_train_epochs=args.epochs, per_device_train_batch_size=args.bs,
    learning_rate=args.lr, warmup_steps=0.1, weight_decay=0.01, lr_scheduler_type="linear",
    bf16=True, logging_steps=10, save_strategy="no", report_to="tensorboard",
    max_length=768, seed=42,
)
trainer = SFTTrainer(model=model, args=cfg, train_dataset=sft_dataset(0, args.n),
                     processing_class=tok, peft_config=lora)
trainable, total = trainer.model.get_nb_trainable_parameters()
print(f"trainable params: {trainable} / {total} = {100 * trainable / total:.3f}%")
trainer.train()

merged = trainer.model.merge_and_unload()
merged.save_pretrained(f"{args.out}/merged")
tok.save_pretrained(f"{args.out}/merged")
json.dump({"log_history": trainer.state.log_history, "trainable_params": trainable,
           "total_params": total, "peak_mem_gb": torch.cuda.max_memory_allocated() / 2**30,
           "args": vars(args)}, open(f"{args.out}/summary.json", "w"), indent=1)
print("peak mem GB", torch.cuda.max_memory_allocated() / 2**30)
