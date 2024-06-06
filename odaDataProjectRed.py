import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. URL der Datenquelle
url = 'https://stats.oecd.org/SDMX-JSON/data/CSPCUBE/PISA+PISA_T1G+PISA_T1H+PISA_T1E+PISA_T1F+PISA_T1K+PISA_T1L+PISA_T1I+PISA_T1J+PISA_T1C+PISA_T1D+PISA_T1A+PISA_T1B.AUT/all?startTime=2011&endTime=2024&dimensionAtObservation=allDimensions'

# 2. Daten herunterladen
response = requests.get(url)
data = response.json()

# 3. Daten in einen Pandas-Datensatz umwandeln
observations = data['dataSets'][0]['observations']
dimensions = data['structure']['dimensions']['observation']
dim_labels = [dim['id'] for dim in dimensions]
dim_values = {dim['id']: {i: value['name'] for i, value in enumerate(dim['values'])} for dim in dimensions}

# 4. Daten umstrukturieren
records = []
for key, value in observations.items():
    indices = key.split(':')
    record = {dim_labels[i]: dim_values[dim_labels[i]][int(index)] for i, index in enumerate(indices)}
    record['Value'] = value[0]
    records.append(record)

# 5. Pandas-Datensatz erstellen
df = pd.DataFrame(records)

# 6. Daten anzeigen (optional)
print(df.head())

# 7. Vorhandene Spaltennamen ausgeben
print("Vorhandene Spalten im DataFrame:", df.columns.tolist())

# 8. Daten in ein verständliches Format bringen
df['Value'] = pd.to_numeric(df['Value'])
df['Time Period'] = df['TIME_PERIOD']
df_pivot = df.pivot_table(index='Time Period', columns='SUB', values='Value')

# 9. Vorhandene Spalten im Pivot DataFrame ausgeben
print("Vorhandene Spalten im Pivot DataFrame:", df_pivot.columns.tolist())

# 10. Visualisierung der Scores mit Standardabweichungen
plots = [
    ('Mean scores on the reading scale in PISA 2012: men', 'Standard error on the reading scale in PISA 2012: men', 'Mean scores on the reading scale in PISA 2012: women', 'Standard error on the reading scale in PISA 2012: women', 'Reading scores'),
    ('Mean scores on the science scale in PISA 2012: men', 'Standard error on the science scale in PISA 2012: men', 'Mean scores on the science scale in PISA 2012: women', 'Standard error on the science scale in PISA 2012: women', 'Science scores'),
    ('Mean scores on the mathematics scale in PISA 2012: men', 'Standard error on the mathematics scale in PISA 2012: men', 'Mean scores on the mathematics scale in PISA 2012: women', 'Standard error on the mathematics scale in PISA 2012: women', 'Mathematics scores')
]

fig, axs = plt.subplots(len(plots), 1, figsize=(12, 18), sharex=True)

bar_width = 0.2  # Balkenbreite reduziert
index = np.arange(len(df_pivot.index))

for i, (score_men, std_err_men, score_women, std_err_women, title) in enumerate(plots):
    if score_men in df_pivot.columns and std_err_men in df_pivot.columns and score_women in df_pivot.columns and std_err_women in df_pivot.columns:
        axs[i].bar(index, df_pivot[score_men], bar_width, yerr=df_pivot[std_err_men], label='Men', capsize=5, color='blue')
        axs[i].bar(index + bar_width, df_pivot[score_women], bar_width, yerr=df_pivot[std_err_women], label='Women', capsize=5, color='red')
        axs[i].set_xlim(-0.5, len(df_pivot.index) - 0.5)
        axs[i].set_ylim(0, 800)
        axs[i].set_ylabel('Score')
        axs[i].set_title(f'{title} with Standard Error')
        axs[i].set_xticks(index + bar_width / 2)
        axs[i].set_xticklabels(df_pivot.index)
        axs[i].legend()
        axs[i].grid(True)


plt.xlabel('Year')
#plt.tight_layout()
plt.show()

#if __name__ == "__main__":
#    main()