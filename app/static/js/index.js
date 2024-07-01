import { populateCountries, populateFinanceMetrics } from './countrySelectionBox.js';
import { createDoubleRangeSlider } from './doubleRangeSlider.js';
import { initializeChart, updateChartData } from './dataChart.js';

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
async function applySelectionAndUpdateGraph() {
    // Check if PISA data is missing
    if (!window.pisaData) {
        await fetchPisaData();
    }
    // Check if the finace data is missing corresponding to the selected metric
    const typeOfMetric = document.getElementById('finance-metrics').value;
    if (!window.financeData || !(typeOfMetric in window.financeData)) {
        await fetchFinanceData(typeOfMetric);
    }

    // Delay for 500 milliseconds before updating the chart
    await new Promise(resolve => setTimeout(resolve, 500));

    // Update the chart
    prepareAndUpdateChart();
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

function prepareAndUpdateChart() {
    // Guard clause required if the data was not fetched yet
    // This should never happen since the fetching is done before
    if (!window.pisaData || !window.financeData) {
        // DEBUG: Log the missing data
        console.error('Missing data:', window.pisaData, window.financeData);
        return;
    }

    const selectedCountries = Array.from(document.getElementById('countries').selectedOptions).map(option => option.value);
    // Guard clause if no countries are selected
    if (selectedCountries.length === 0) {
        // DEBUG: Log the missing countries
        console.error('No countries selected');
        return;
    }

    const selectedMetric = document.getElementById('finance-metrics').value;
    const startYear = parseInt(document.getElementById('start-year').value);
    const endYear = parseInt(document.getElementById('end-year').value);
    const startEducationLevel = parseInt(document.getElementById('start-education-level').value);
    const endEducationLevel = parseInt(document.getElementById('end-education-level').value);

    // Currently the education levels are not correctly in the slider but instead 1 to 5
    // Have to map it to get the correct values
    const mappedStartEducationLevel = educationLevelMap[startEducationLevel];
    const mappedEndEducationLevel = educationLevelMap[endEducationLevel];

    // DEBUG: Log the selected countries, metric, and years
    console.log('Selected countries:', selectedCountries);
    console.log('Selected metric:', selectedMetric);
    console.log('Selected years:', startYear, endYear);
    console.log('Selected education levels:', mappedStartEducationLevel, mappedEndEducationLevel);

    // Filter the data
    const filteredPisaData = filterPisaData(window.pisaData, selectedCountries, startYear, endYear);
    const filteredFinanceData = filterFinanceData(window.financeData[selectedMetric], selectedCountries, startEducationLevel, endEducationLevel, startYear, endYear);

    // Update the chart
    updateChartData(filteredPisaData, filteredFinanceData);
}

function filterPisaData(pisaData, countries, startYear, endYear) {
    const filteredData = {};

    countries.forEach(country => {
        if (pisaData.countries[country]) {
            filteredData[country] = {};
            for (let year = startYear; year <= endYear; year++) {
                if (pisaData.countries[country][year]) {
                    filteredData[country][year] = pisaData.countries[country][year];
                }
            }
        }
    });

    return filteredData;
}

function filterFinanceData(financeData, countries, startEducationLevel, endEducationLevel, startYear, endYear) {
    const filteredData = {};

    countries.forEach(country => {
        if (financeData.countries[country]) {
            filteredData[country] = {};
            for (let year = startYear; year <= endYear; year++) {
                const yearData = financeData.countries[country][year];
                if (yearData) {
                    filteredData[country][year] = {};
                    for (let level = startEducationLevel; level <= endEducationLevel; level++) {
                        const mappedLevel = educationLevelMap[level];
                        if (yearData[mappedLevel]) {
                            filteredData[country][year][level] = yearData[mappedLevel];
                        }
                    }
                }
            }
        }
    });

    return filteredData;
}

// Education levels must be mapped for correct handling, e.g. comparing with each other in filter
// Have to map it here to the correct values
// The education levels are ED01, ED02, ED1, ED2, ED3
// We can map them to 1, 2, 3, 4, 5
const educationLevelMap = {
    1: 'ED01',
    2: 'ED02',
    3: 'ED1',
    4: 'ED2',
    5: 'ED3'
};