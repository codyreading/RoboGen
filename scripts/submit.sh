#!/bin/bash
#SBATCH --job-name=robogen                 # Job name
#SBATCH --partition=h100-agent-10-train    # Partition name
#SBATCH --gres=gpu:1                       # Request 2 GPUs
#SBATCH --time=24:00:00                    # (Optional) Max run time (5 minutes)
#SBATCH --output=logs/output.%j                 # Standard output log (%j will be replaced with Job ID)
#SBATCH --error=logs/error.%j                   # Standard error log
#SBATCH --cpus-per-task=64

# Run the nvidia-smi command
echo "Running job on the allocated GPU(s):"
source ~/.bashrc
conda activate robogen


LOG_DIR="logs"

mkdir -p "$LOG_DIR"  # Ensure log directory exists

# Define the CSV file path
CSV_FILE="experiments.csv"
index=0

# Set IFS to handle CSV properly (handle quoted values correctly)
while IFS=, read -r category task || [[ -n "$category" ]]; do
    # Skip the header
    if [[ "$index" -eq 0 ]]; then
        ((index++))
        continue
    fi

    # Remove surrounding quotes from variables
    CATEGORY=$(echo "$category" | sed 's/^"//;s/"$//')
    TASK=$(echo "$task")
    LOG_FILE="$LOG_DIR/${index}_${CATEGORY}.log"
    CMD="python generate.py --task ${TASK} --category ${CATEGORY} &>> ${LOG_FILE} &"
    echo $CMD
    #eval $CMD

    # Increment index
    ((index++))

done < <(cat "$CSV_FILE")  # Ensure last line is processed


echo "All tasks started. Check logs in $LOG_DIR"
wait  # Wait for all background processes to complete
echo "All tasks completed."
