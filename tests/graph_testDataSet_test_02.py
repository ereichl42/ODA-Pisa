import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import pandas as pd

# Sample datasets (you would load your actual datasets here)
datasets = {
    "educ_expenditure_level_source": pd.DataFrame({
        "Year": range(2012, 2021),
        "Country_A": [100, 110, 120, 130, 140, 150, 160, 170, 180],
        "Country_B": [90, 95, 100, 105, 110, 115, 120, 125, 130],
        "Country_C": [80, 85, 90, 95, 100, 105, 110, 115, 120]
    }),
    "educ_expenditure_gdp": pd.DataFrame({
        "Year": range(2012, 2021),
        "Country_A": [70, 75, 80, 85, 90, 95, 100, 105, 110],
        "Country_B": [60, 65, 70, 75, 80, 85, 90, 95, 100],
        "Country_C": [50, 55, 60, 65, 70, 75, 80, 85, 90]
    }),
}

# Function to update the graph


def update_graph():
    selected_dataset = dataset_var.get()
    selected_countries = country_var.get()
    data = datasets[selected_dataset]

    # Select data for the chosen countries
    if "All" in selected_countries:
        selected_data = data.drop(columns=["Year"])
    else:
        selected_data = data[["Year"] + selected_countries]

    # Plotting
    plt.figure(figsize=(8, 6))
    for country in selected_data.columns[1:]:
        plt.plot(selected_data["Year"],
                 selected_data[country], marker='o', label=country)
    plt.title(f"{selected_dataset} Data")
    plt.xlabel("Year")
    plt.ylabel("Data")
    plt.legend()
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

# Dropdown menu for selecting countries
countries = ["All"] + datasets[next(iter(datasets))].columns[1:].tolist()
country_var = tk.StringVar(window)
country_var.set("All")  # Set default value
country_dropdown = ttk.Combobox(
    window, textvariable=country_var, values=countries, state="readonly")
country_dropdown.pack(pady=5)

# Button to update graph
update_button = tk.Button(window, text="Update Graph", command=update_graph)
update_button.pack(pady=5)

# Display initial graph
update_graph()

# Start tkinter event loop
window.mainloop()
