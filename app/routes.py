# app/routes.py

import os
import json
from flask import Flask, jsonify, request, Blueprint, render_template

# Blueprint configuration
routes = Blueprint('routes', __name__)

# Load country list from JSON file
with open('data/reference/country_codes.json') as f:
    country_codes = json.load(f)

# Hard-coded years
FIRST_YEAR = 2000
LAST_YEAR = 2022

# Directory containing finance metric JSON files
FINANCE_DATA_DIR = 'data/financial_data'


@routes.route('/')
def index():
    return render_template('index.html')


@routes.route('/api/years_countries', methods=['GET'])
def get_years_countries():
    finance_metrics = [os.path.splitext(f)[0] for f in os.listdir(
        FINANCE_DATA_DIR) if f.endswith('.json')]
    years_countries_data = {
        "first_year": FIRST_YEAR,
        "last_year": LAST_YEAR,
        "countries": country_codes,
        "finance_metrics": finance_metrics
    }
    return jsonify(years_countries_data)


@routes.route('/api/pisa_data', methods=['GET'])
def get_pisa_data():
    # Load PISA data from JSON file
    with open('data/pisa_data/pisa_dataset.json') as f:
        pisa_data = json.load(f)
    return jsonify(pisa_data)


@routes.route('/api/finance_data', methods=['GET'])
def get_finance_data():
    metric = request.args.get('metric')
    metric_file = os.path.join(FINANCE_DATA_DIR, f"{metric}.json")
    if not os.path.exists(metric_file):
        return jsonify({"error": "Finance metric data not found"}), 404

    with open(metric_file) as f:
        finance_data = json.load(f)
    return jsonify(finance_data)
