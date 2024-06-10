from flask import Flask, request, jsonify, render_template, send_file
import requests
import json
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

base_url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
dataset_code = "educ_uoe_fina01"


def fetch_years_and_countries():
    # Function to fetch available years and countries from the dataset
    country_codes = []
    with open('country_codes.json') as f:
        country_codes = json.load(f)
        country_codes = country_codes['countries']
    first_year = 2000
    last_year = 2022


@app.route('/')
def index():
    # Endpoint to serve the frontend
    return render_template('index.html')


@app.route('/api/years_countries', methods=['GET'])
def get_years_countries():
    # Endpoint to get years and countries
    first_year, last_year, country_codes = fetch_years_and_countries()
    return jsonify({
        "first_year": first_year,
        "last_year": last_year,
        "countries": country_codes
    })


@app.route('/api/fetch_data', methods=['POST'])
def fetch_data():
    # Endpoint to fetch data based on user input
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


@app.route('/api/plot', methods=['POST'])
def plot_data():
    # Endpoint to generate and serve a plot
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
