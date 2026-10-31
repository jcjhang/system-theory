#!/bin/bash
# Extra E3 run: step reward without KL and with a high learning rate, to try to provoke reward hacking.
# Waits for run_all.sh to finish so the two never share the GPU.
cd ~/ch11_agentic_rl
while pgrep -u "$USER" -f "bash ./run_all.sh" > /dev/null; do sleep 60; done
. .venv/bin/activate
export CUDA_VISIBLE_DEVICES=${GPU:-0} HF_HUB_DISABLE_PROGRESS_BARS=1 TOKENIZERS_PARALLELISM=false
echo "[$(date '+%F %T')] start grpo_step_hack" >> logs/run_all.out
python grpo.py --model runs/sft/merged --out runs/grpo_step_hack --reward step --beta 0.0 --lr 1e-4 \
  --n 400 --save_steps 1000 > logs/grpo_step_hack.log 2>&1 &&
python evaluate.py --model runs/grpo_step_hack/merged --name grpo_step_hack > logs/eval_grpo_step_hack.log 2>&1
echo "[$(date '+%F %T')] EXTRA DONE (exit $?)" >> logs/run_all.out
