from flask import Blueprint, render_template, jsonify, request
import pandas as pd
import os
import json

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/data', methods=['GET'])
def get_data():
    # Example data loading
    pisa_path = os.path.join('data', 'pisa_data', 'pisa_dataset.json')
    with open(pisa_path, 'r') as f:
        pisa_data = json.load(f)

    finance_path = os.path.join(
        'data', 'financial_data', 'educ_expenditure_gdp.json')
    with open(finance_path, 'r') as f:
        finance_data = json.load(f)

    return jsonify({'pisa': pisa_data, 'finance': finance_data})

# Additional routes and data processing functions
