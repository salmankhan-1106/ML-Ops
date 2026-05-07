# =========================================================
# FILE: generate_dataset.py
#
# PURPOSE:
# Generates a UNIQUE dataset for each student
# using values from config.json
#
# OUTPUT:
# dataset/train.csv
#
# =========================================================

import pandas as pd
import numpy as np
import json
import os

# =========================================================
# LOAD CONFIG
# =========================================================

with open("config.json") as f:
    config = json.load(f)

student_id = config["student_id"]
seed = config["seed"]
noise_level = config["noise_level"]

# =========================================================
# REPRODUCIBILITY
# =========================================================

np.random.seed(seed)

# =========================================================
# DATASET PARAMETERS
# =========================================================

ROWS = 500

# Generate features
f1 = np.random.rand(ROWS)
f2 = np.random.rand(ROWS)
f3 = np.random.rand(ROWS)
f4 = np.random.rand(ROWS)
f5 = np.random.rand(ROWS)

# =========================================================
# GENERATE NOISE
# =========================================================

noise = np.random.normal(
    loc=0,
    scale=noise_level,
    size=ROWS
)

# =========================================================
# GENERATE LABEL
#
# Different weights create meaningful patterns
# =========================================================

score = (
    (f1 * 0.30) +
    (f2 * 0.20) +
    (f3 * 0.40) +
    (f4 * 0.05) +
    (f5 * 0.05) +
    noise
)

label = (score > 0.5).astype(int)

# =========================================================
# CREATE DATAFRAME
# =========================================================

df = pd.DataFrame({
    "f1": f1,
    "f2": f2,
    "f3": f3,
    "f4": f4,
    "f5": f5,
    "label": label
})

# =========================================================
# CREATE DATASET DIRECTORY
# =========================================================

os.makedirs("dataset", exist_ok=True)

# =========================================================
# SAVE DATASET
# =========================================================

output_path = "dataset/train.csv"

df.to_csv(output_path, index=False)

# =========================================================
# OPTIONAL METADATA
# Useful for evaluation
# =========================================================

metadata = {
    "student_id": student_id,
    "seed": seed,
    "noise_level": noise_level,
    "rows": ROWS,
    "dataset_version": config["dataset_version"]

	}


with open("dataset/metadata.json", "w") as f:
    json.dump(metadata, f, indent=4)

# =========================================================
# SUCCESS MESSAGE
# =========================================================

print("=" * 50)
print("DATASET GENERATED SUCCESSFULLY")
print("=" * 50)

print(f"Student ID       : {student_id}")
print(f"Seed             : {seed}")
print(f"Noise Level      : {noise_level}")
print(f"Rows Generated   : {ROWS}")
print(f"Dataset Location : {output_path}")

print("=" * 50)
