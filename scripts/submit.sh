#!/bin/bash
#SBATCH --job-name=robogen                 # Job name
#SBATCH --partition=h100-agent-10-train    # Partition name
#SBATCH --gres=gpu:2                       # Request 2 GPUs
#SBATCH --time=24:00:00                    # (Optional) Max run time (5 minutes)
#SBATCH --output=output.%j                 # Standard output log (%j will be replaced with Job ID)
#SBATCH --error=error.%j                   # Standard error log

# Run the nvidia-smi command
echo "Running job on the allocated GPU(s):"
source ~/.bashrc
conda activate robogen

nohup bash -c 'export CUDA_VISIBLE_DEVICES=1 && vllm serve "meta-llama/Llama-3.1-8B-Instruct"' > vllm_output.log 2>&1 &
sleep 60

python run.py
