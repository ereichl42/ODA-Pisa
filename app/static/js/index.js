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
        .then(response => response.json())
        .then(pisaData => {
            window.pisaData = pisaData;
        })
        .catch(error => console.error('Error fetching data:', error));

    // Event listener for button
    document.getElementById('apply-metric').addEventListener('click', fetchFinanceData);
});

function fetchFinanceData() {
    const metric = document.getElementById('finance-metrics').value;
    fetch(`/api/finance_data?metric=${metric}`)
        .then(response => response.json())
        .then(data => {
            window.financeData = data;
            updateChart();
        })
        .catch(error => console.error('Error fetching finance data:', error));
}

function updateYearLabels() {
    const startYear = document.getElementById('start-year').value;
    const endYear = document.getElementById('end-year').value;
    document.getElementById('start-year-label').textContent = startYear;
    document.getElementById('end-year-label').textContent = endYear;
    updateChart();
}

function updateEducationLevelLabels() {
    const startLevel = document.getElementById('start-education-level').value;
    const endLevel = document.getElementById('end-education-level').value;
    document.getElementById('start-education-level-label').textContent = startLevel;
    document.getElementById('end-education-level-label').textContent = endLevel;
    updateChart();
}

function updateChart() {
    const startYear = parseInt(document.getElementById('start-year').value);
    const endYear = parseInt(document.getElementById('end-year').value);
    const selectedCountries = Array.from(document.getElementById('countries').selectedOptions).map(option => option.value);

    if (!window.pisaData || !window.financeData) {
        return;
    }

    const filteredPisaData = filterDataByYearsAndCountries(window.pisaData, startYear, endYear, selectedCountries);
    const filteredFinanceData = filterDataByYearsAndCountries(window.financeData, startYear, endYear, selectedCountries);

    updateChartData(filteredPisaData, filteredFinanceData, startYear, endYear);
}

function filterDataByYearsAndCountries(data, startYear, endYear, countries) {
    return data.filter(entry => {
        const year = parseInt(entry.Year);
        return year >= startYear && year <= endYear && countries.includes(entry.Country);
    });
}
