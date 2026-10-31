#!/bin/bash
# Run E1-E4 sequentially on one GPU. Each stage is skipped if its output already exists,
# so the script can be re-launched after a failure.
cd ~/ch11_agentic_rl
. .venv/bin/activate
export CUDA_VISIBLE_DEVICES=${GPU:-0} HF_HUB_DISABLE_PROGRESS_BARS=1 TOKENIZERS_PARALLELISM=false
mkdir -p logs results
./gpu_mem_logger.sh &

stage() {  # stage <name> <done-file> <cmd...>
  local name=$1 done=$2; shift 2
  if [ -e "$done" ]; then echo "[skip] $name"; return; fi
  echo "[$(date '+%F %T')] start $name"
  if "$@" > "logs/$name.log" 2>&1; then
    echo "[$(date '+%F %T')] done  $name"
  else
    echo "[$(date '+%F %T')] FAIL  $name (see logs/$name.log)"
  fi
}

SFT=runs/sft/merged

# ---- E1 / E2 ----
stage eval_base  results/eval_base.json  python evaluate.py --model Qwen/Qwen3-0.6B-Base --name base
stage sft        $SFT/config.json        python sft.py --out runs/sft --n 2000 --epochs 3 --bs 8 --lr 1e-4
stage eval_sft   results/eval_sft.json   python evaluate.py --model $SFT --name sft
stage grpo_acc   runs/grpo_acc/merged/config.json \
      python grpo.py --model $SFT --out runs/grpo_acc --reward accuracy --n 1000
stage eval_grpo_acc results/eval_grpo_acc.json python evaluate.py --model runs/grpo_acc/merged --name grpo_acc
stage eval_grpo_acc_125 results/eval_grpo_acc_125.json \
      python evaluate.py --model $SFT --adapter runs/grpo_acc/checkpoint-125 --name grpo_acc_125

# ---- E3: reward functions (125 steps each, compare with grpo_acc_125) ----
for R in length_penalty step; do
  stage grpo_$R runs/grpo_$R/merged/config.json \
        python grpo.py --model $SFT --out runs/grpo_$R --reward $R --n 500 --save_steps 1000
  stage eval_grpo_$R results/eval_grpo_$R.json python evaluate.py --model runs/grpo_$R/merged --name grpo_$R
done

# ---- E4: KL coefficient / learning rate (100 steps each) ----
stage grpo_beta0   runs/grpo_beta0/merged/config.json \
      python grpo.py --model $SFT --out runs/grpo_beta0 --beta 0.0 --n 400 --save_steps 1000
stage grpo_beta05  runs/grpo_beta05/merged/config.json \
      python grpo.py --model $SFT --out runs/grpo_beta05 --beta 0.5 --n 400 --save_steps 1000
stage grpo_lr2e-4  runs/grpo_lr2e-4/merged/config.json \
      python grpo.py --model $SFT --out runs/grpo_lr2e-4 --lr 2e-4 --n 400 --save_steps 1000
for X in beta0 beta05 lr2e-4; do
  stage eval_grpo_$X results/eval_grpo_$X.json python evaluate.py --model runs/grpo_$X/merged --name grpo_$X
done

echo "[$(date '+%F %T')] ALL DONE"
