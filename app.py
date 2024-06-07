from flask import Flask, request, jsonify, render_template, send_file
import requests
import json
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

base_url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
dataset_code = "educ_uoe_fina01"

# Function to fetch available years and countries from the dataset
def fetch_years_and_countries():
    params = {
        "lang": "EN",
        "format": "JSON",
    }
    url = f"{base_url}{dataset_code}"
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        time_dimensions = data['dimension']['time']['category']['index']
        years = sorted([int(year) for year in time_dimensions.keys()])
        geo_dimension = data['dimension']['geo']['category']['index']
        countries = {name: code for code, name in data['dimension']['geo']['category']['label'].items()}
        return min(years), max(years), countries
    else:
        return None, None, {}

# Endpoint to serve the frontend
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to get years and countries
@app.route('/api/years_countries', methods=['GET'])
def get_years_countries():
    first_year, last_year, country_codes = fetch_years_and_countries()
    return jsonify({
        "first_year": first_year,
        "last_year": last_year,
        "countries": country_codes
    })

# Endpoint to fetch data based on user input
@app.route('/api/fetch_data', methods=['POST'])
def fetch_data():
    data = request.json
    time_period = data.get('time_period')
    countries = data.get('countries')

    params = {
        "lang": "EN",
        "format": "JSON"
    }

    if time_period:
        if "-" in time_period:
            start_year, end_year = time_period.split("-")
            params["sinceTimePeriod"] = start_year
            params["untilTimePeriod"] = end_year
        else:
            params["time"] = time_period
    else:
        params["sinceTimePeriod"] = "1900"

    if countries:
        params["geo"] = ",".join(countries)
    else:
        return jsonify({"error": "Please select at least one country."}), 400

    url = f"{base_url}{dataset_code}"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return jsonify({"error": f"Failed to retrieve data: {response.status_code}"}), 500

# Endpoint to generate and serve a plot
@app.route('/api/plot', methods=['POST'])
def plot_data():
    data = request.json
    time_period = data.get('time_period')
    countries = data.get('countries')

    # Here, you'd implement the logic to generate your plot based on `time_period` and `countries`.
    # For now, let's create a dummy plot.
    plt.figure()
    plt.plot([1, 2, 3], [4, 5, 6])
    plt.title("Sample Plot")
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
