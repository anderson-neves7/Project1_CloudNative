import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Timestamp so the screenshot shows when the script was run
print("Analysis started at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Load the dataset
file_name = "All_Diets.csv"
if not os.path.exists(file_name):
    print("CSV file not found in the project folder.")
    exit()

df = pd.read_csv(file_name)

# Quick preview
print("\nFirst few rows:")
print(df.head())

print("\nColumns in the dataset:")
print(df.columns)

# Clean missing numeric values
numeric_cols = ["Protein(g)", "Carbs(g)", "Fat(g)"]
for col in numeric_cols:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].mean())

# Average macros by diet type
if "Diet_type" in df.columns:
    avg_macros = df.groupby("Diet_type")[numeric_cols].mean()
    print("\nAverage macronutrients by diet type:")
    print(avg_macros)
else:
    print("Diet_type column missing.")
    exit()

# Add ratio columns
df["Protein_to_Carbs_ratio"] = df["Protein(g)"] / df["Carbs(g)"]
df["Carbs_to_Fat_ratio"] = df["Carbs(g)"] / df["Fat(g)"]

print("\nSample of new ratio columns:")
print(df[["Diet_type", "Recipe_name", "Protein_to_Carbs_ratio", "Carbs_to_Fat_ratio"]].head())

# Top 5 protein-rich recipes per diet type
if "Recipe_name" in df.columns:
    top_protein = df.sort_values("Protein(g)", ascending=False).groupby("Diet_type").head(5)
    print("\nTop 5 protein-rich recipes per diet type:")
    print(top_protein[["Diet_type", "Recipe_name", "Protein(g)"]])
else:
    print("Recipe_name column missing.")

# Create folder for charts
if not os.path.exists("figures"):
    os.mkdir("figures")

# Chart 1: Average protein by diet type
plt.figure(figsize=(10, 6))
sns.barplot(data=avg_macros.reset_index(), x="Diet_type", y="Protein(g)")
plt.xticks(rotation=45)
plt.title("Average Protein by Diet Type")
plt.tight_layout()
plt.savefig("figures/avg_protein_by_diet.png")
plt.close()

# Chart 2: Heatmap of average macros
plt.figure(figsize=(8, 6))
sns.heatmap(avg_macros, annot=True, cmap="Blues", fmt=".1f")
plt.title("Average Macronutrients by Diet Type")
plt.tight_layout()
plt.savefig("figures/avg_macros_heatmap.png")
plt.close()

# Chart 3: Protein vs Carbs for top recipes
plt.figure(figsize=(10, 6))
sns.scatterplot(data=top_protein, x="Carbs(g)", y="Protein(g)", hue="Diet_type")
plt.title("Top Protein-Rich Recipes (Protein vs Carbs)")
plt.tight_layout()
plt.savefig("figures/top_protein_scatter.png")
plt.close()

print("\nAnalysis complete. Charts saved in the 'figures' folder.")
