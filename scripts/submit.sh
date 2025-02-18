#!/bin/bash
#SBATCH --job-name=robogen                 # Job name
#SBATCH --partition=h100-agent-10-train    # Partition name
#SBATCH --gres=gpu:1                       # Request 2 GPUs
#SBATCH --time=24:00:00                    # (Optional) Max run time (5 minutes)
#SBATCH --output=output.%j                 # Standard output log (%j will be replaced with Job ID)
#SBATCH --error=error.%j                   # Standard error log
#SBATCH --cpus-per-task=64

# Run the nvidia-smi command
echo "Running job on the allocated GPU(s):"
source ~/.bashrc
conda activate robogen

# TASKS=(
#     "Pack my t-shirt, jeans, and underwear in the suitcase. My t-shirt is on my bed, the jeans in the closet, and the underwear is in a set of drawers"
#     "Sort a red, blue, and green pen in that order from left to right"
#     "Clean the plates, forks, and knives using the dishwasher"
#     "Clean the garbage scattered all over the floor and my bed in room"
#     "Prepare the dining room table for 4 people. Place plates, forks, and knives at each spot for each person on the table."
#     "Make me a cup of coffee. The coffee beans, coffee cup, and the spoon are located in the cupboard."
# )
# CATEGORIES=("Suitcase" "Pen" "Dishwasher" "TrashCan" "Knife" "CoffeeMachine")


TASKS=(
    "I want a fruit that is commonly associated with keeping doctors away."
    "Pick an energy drink with a powerful boost of caffeine."
    "Tonight is the day I propose to my girlfriend. Please insert a suitable flower into the vase."
    "Sort the books on the shelf starting with the most recent publication year and ending with the oldest"
    "Sort the billiard balls into baskets in front of you? We need them organized for the upcoming tournament"
    "Sort out these books on the shelf so the library looks tidy?"
    "Prepare Pb(OH)₂ to conduct a chemistry experiment"
    "Sort out the drinks to help keep the bar area tidy and efficient for service?"
    "Play chess as black"
    "Play Texas Holdem"
)

CATEGORIES=("Table" "Table" "Table" "StorageFurniture" "StorageFurniture" "StorageFurniture" "Table" "Table" "Table" "Table")


LOG_DIR="logs"

mkdir -p "$LOG_DIR"  # Ensure log directory exists


for i in "${!TASKS[@]}"; do
    TASK="${TASKS[i]}"
    CATEGORY="${CATEGORIES[i]}"
    LOG_FILE="$LOG_DIR/${CATEGORY}.log"

    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting task: $TASK (Category: $CATEGORY)" | tee -a "$LOG_FILE"

    python generate.py --task "$TASK" --category "$CATEGORY" &>> "$LOG_FILE" &
done

echo "All tasks started. Check logs in $LOG_DIR"
wait  # Wait for all background processes to complete
echo "All tasks completed."

# TASK="Wash and dry my clothes"
# CATEGORY="WashingMachine"

# python generate.py --task "$TASK" --category "$CATEGORY"
