#!/bin/bash
# Every 10 s, record the GPU memory (as nvidia-smi sees it) of this user's processes.
# Stops when run_all.sh exits.
cd ~/ch11_agentic_rl
echo "time,pid,cmd,used_mib" > logs/gpu_mem.csv
while pgrep -u "$USER" -f "bash ./run_all.sh" > /dev/null; do
  nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader,nounits |
  while IFS=", " read -r pid mem; do
    if [ "$(ps -o user= -p "$pid" 2>/dev/null)" = "$USER" ]; then
      echo "$(date +%T),$pid,$(ps -o args= -p "$pid" | cut -c1-100 | tr , ' '),$mem" >> logs/gpu_mem.csv
    fi
  done
  sleep 10
done
