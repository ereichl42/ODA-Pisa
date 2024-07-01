import { populateCountries, populateFinanceMetrics } from './countrySelectionBox.js';
import { createDoubleRangeSlider } from './doubleRangeSlider.js';
import { initializeChart, updateChartData } from './chart.js';

document.addEventListener("DOMContentLoaded", function () {
    // Fetch initial data for countries, years, and finance metrics
    fetch('/api/years_countries')
        .then(response => response.json())
        .then(data => {
            populateCountries(data.countries);
            populateFinanceMetrics(data.finance_metrics);

            // TODO: Fetch available education levels
            // Temporary education levels: 1 to 5
            const minEducationLevel = 1;
            const maxEducationLevel = 5;

            // Initialize sliders with available years from the response
            createDoubleRangeSlider('year-range-slider', 'start-year', 'end-year', data.first_year, data.last_year);
            // Initialize sliders with available education levels from the response
            createDoubleRangeSlider('education-level-range-slider', 'start-education-level', 'end-education-level', minEducationLevel, maxEducationLevel);
        })
        .catch(error => console.error('Error fetching initial data:', error));

    // Initialize the chart
    initializeChart();

    // Event listener for button
    document.getElementById('apply-metric').addEventListener('click', applySelectionAndUpdateGraph);
});

// Function to apply all filters, fetch missing data if needed, and update the graph
function applySelectionAndUpdateGraph() {
    // Check if PISA data is missing
    if (!window.pisaData) {
        fetchPisaData();
    }
    // Check if the finace data is missing corresponding to the selected metric
    typeOfMetric = document.getElementById('finance-metrics').value;
    if (!window.financeData || !(typeOfMetric in window.financeData)) {
        fetchFinanceData(typeOfMetric);
    }
    // Update the chart
    updateChart();
}

// Function to fetch PISA data
function fetchPisaData() {
    fetch('/api/pisa_data')
        .then(response => response.json())
        .then(data => {
            window.pisaData = data;
        })
        .catch(error => console.error('Error fetching PISA data:', error));
}

// Function to fetch Finance data of a selected metric
function fetchFinanceData(typeOfMetric) {
    fetch(`/api/finance_data?metric=${typeOfMetric}`)
        .then(response => response.json())
        .then(data => {
            // The global variable is a dictionary with keys as metric names and values as the corresponding data
            // If global variable is not defined yet, initialize it as an empty dictionary and add the received data
            window.financeData = window.financeData || {};
            window.financeData[typeOfMetric] = data;
        })
        .catch(error => console.error('Error fetching finance data:', error));
}

function updateChart() {
    // Guard clause required if the data was not fetched yet
    // This should never happen since the fetching is done before
    if (!window.pisaData || !window.financeData) {
        return;
    }

    const selectedCountries = Array.from(document.getElementById('countries').selectedOptions).map(option => option.value);
    // Guard clause if no countries are selected
    if (selectedCountries.length === 0) {
        return;
    }

    const selectedMetric = document.getElementById('finance-metrics').value;
    const startYear = parseInt(document.getElementById('start-year').value);
    const endYear = parseInt(document.getElementById('end-year').value);

    // DEBUG: Log the selected countries, metric, and years
    console.log('Selected countries:', selectedCountries);
    console.log('Selected metric:', selectedMetric);
    console.log('Selected years:', startYear, endYear);

    // TODO: Update the chart with the selected data
    //
}