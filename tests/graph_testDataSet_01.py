import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import pandas as pd

# Sample datasets (you would load your actual datasets here)
datasets = {
    "educ_expenditure_level_source": pd.DataFrame({
        "Year": range(2012, 2021),
        "Data": [100, 110, 120, 130, 140, 150, 160, 170, 180]
    }),
    "educ_expenditure_gdp": pd.DataFrame({
        "Year": range(2012, 2021),
        "Data": [90, 95, 100, 105, 110, 115, 120, 125, 130]
    }),
    "educ_expenditure_public_gni": pd.DataFrame({
        "Year": range(2012, 2021),
        "Data": [80, 85, 90, 95, 100, 105, 110, 115, 120]
    }),
    "educ_expenditure_per_student": pd.DataFrame({
        "Year": range(2012, 2021),
        "Data": [70, 75, 80, 85, 90, 95, 100, 105, 110]
    }),
    "educ_financial_aid_percentage": pd.DataFrame({
        "Year": range(2012, 2021),
        "Data": [60, 65, 70, 75, 80, 85, 90, 95, 100]
    })
}

# Function to update the graph


def update_graph():
    selected_dataset = dataset_var.get()
    data = datasets[selected_dataset]
    plt.figure(figsize=(8, 6))
    plt.plot(data["Year"], data["Data"], marker='o')
    plt.title(f"{selected_dataset} Data")
    plt.xlabel("Year")
    plt.ylabel("Data")
    plt.grid(True)
    plt.show()


# Create tkinter window
window = tk.Tk()
window.title("Dataset Selector")

# Dropdown menu for selecting dataset
dataset_var = tk.StringVar(window)
dataset_var.set(list(datasets.keys())[0])  # Set default value
dataset_dropdown = ttk.Combobox(
    window, textvariable=dataset_var, values=list(datasets.keys()))
dataset_dropdown.pack(pady=10)

# Button to update graph
update_button = tk.Button(window, text="Update Graph", command=update_graph)
update_button.pack(pady=5)

# Display initial graph
update_graph()

# Start tkinter event loop
window.mainloop()
