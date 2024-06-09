import pandas as pd
import json


def load_pisa_data(data_dict):
    # Initialize the resulting JSON structure

    # I take a deep copy of the template structure.
    template_path = 'data/templates/pisa_dataset_template.json'
    with open(template_path, 'r') as f:
        pisa_results = json.load(f)

    # Remove the example data which was included in the template. The metadata is kept.
    pisa_results["countries"] = []

    # Iterate through each dataframe in the dictionary
    for result_type, df in data_dict.items():
        # Clean the data and transform it
        df = df.rename(columns={'Year/Study': 'Year',
                       'Jurisdiction': 'Country', 'Average': result_type})

        # Fill forward the 'Year' column where there are gaps
        df['Year'] = df['Year'].fillna(method='ffill')

        # Replace non-numeric values with None
        df[result_type] = pd.to_numeric(df[result_type], errors='coerce')

        # Iterate through the rows to build the nested structure
        for _, row in df.iterrows():
            year = int(row['Year'])
            country = row['Country']
            score = row[result_type] if pd.notnull(row[result_type]) else None

            # Find or create the country entry
            country_entry = next(
                (item for item in pisa_results["countries"] if item["country"] == country), None)
            if not country_entry:
                country_entry = {"country": country, "data": {}}
                pisa_results["countries"].append(country_entry)

            # Find or create the year entry
            if year not in country_entry["data"]:
                country_entry["data"][year] = {"combined": None}

            # Add the score to the corresponding type
            country_entry["data"][year][result_type] = score

            # Calculate the combined score if all three types are present
            if all(key in country_entry["data"][year] and country_entry["data"][year][key] is not None for key in ["math", "reading", "science"]):
                combined_score = (country_entry["data"][year]["math"] + country_entry["data"]
                                  [year]["reading"] + country_entry["data"][year]["science"]) / 3
                country_entry["data"][year]["combined"] = combined_score

    return pisa_results


# Example usage with the provided data dictionary
# This dictionary should contain the dataframes for 'math', 'science', and 'reading'
example_data_dict = {
    "math": pd.DataFrame({
        "Year/Study": [2012, None, None, 2015, None, None, 2018, None, None],
        "Jurisdiction": ["AT", "BG", "US", "AT", "BG", "US", "AT", "BG", "US"],
        "Average": [500, 450, 490, 505, 455, 495, 515, 460, 500],
        "Standard Error": [3.2, 2.5, 2.9, 3.1, 2.6, 2.8, 3.3, 2.7, 2.9]
    }),
    "reading": pd.DataFrame({
        "Year/Study": [2012, None, None, 2015, None, None, 2018, None, None],
        "Jurisdiction": ["AT", "BG", "US", "AT", "BG", "US", "AT", "BG", "US"],
        "Average": [495, 440, 480, 500, 445, 485, 505, 450, 490],
        "Standard Error": [3.3, 2.6, 3.0, 3.2, 2.7, 2.9, 3.4, 2.8, 3.0]
    }),
    "science": pd.DataFrame({
        "Year/Study": [2012, None, None, 2015, None, None, 2018, None, None],
        "Jurisdiction": ["AT", "BG", "US", "AT", "BG", "US", "AT", "BG", "US"],
        "Average": [505, 460, 500, 510, 465, 505, 520, 470, 510],
        "Standard Error": [3.4, 2.7, 3.1, 3.3, 2.8, 3.0, 3.5, 2.9, 3.1]
    })
}

pisa_results = load_pisa_data(example_data_dict)

# Save the results to a JSON file
output_file = 'pisa_results.json'
with open(output_file, 'w') as f:
    json.dump(pisa_results, f, indent=4)

print(f"PISA results saved to {output_file}")
