document.addEventListener("DOMContentLoaded", function () {
    // Fetch initial data for countries and finance metrics
    fetch('/api/years_countries')
        .then(response => response.json())
        .then(data => {
            //console.log(data);  // Debug print
            populateCountries(data.countries);
            populateFinanceMetrics(data.finance_metrics);
        })
        .catch(error => console.error('Error fetching years and countries:', error));

    // Fetch PISA data
    fetch('/api/pisa_data')
        .then(response => response.json())
        .then(data => {
            window.pisaData = data;
        })
        .catch(error => console.error('Error fetching PISA data:', error));

    // Event listeners for sliders and button
    document.getElementById('apply-metric').addEventListener('click', fetchFinanceData);
    document.getElementById('start-year').addEventListener('input', updateYearLabels);
    document.getElementById('end-year').addEventListener('input', updateYearLabels);
});

function populateCountries(countries) {
    //console.log("Populating countries:", countries);  // Debug print
    const countriesSelect = document.getElementById('countries');
    countriesSelect.innerHTML = '';  // Clear existing options
    
    // Populate country dropdown using Object.entries directly
    Object.entries(countries.countries).forEach(([name, code]) => {
        const option = document.createElement('option');
        option.value = name; // Use the country name as the value
        option.textContent = name; // Display only the country name
        countriesSelect.appendChild(option);
    });
}

function populateFinanceMetrics(metrics) {
    const metricsSelect = document.getElementById('finance-metrics');
    metricsSelect.innerHTML = '';  // Clear existing options
    metrics.forEach(metric => {
        const option = document.createElement('option');
        option.value = metric;
        option.text = metric.replace(/_/g, ' ').toUpperCase();
        metricsSelect.add(option);
    });
}

function fetchFinanceData() {
    const metric = document.getElementById('finance-metrics').value;
    //console.log('Fetching finance data for metric:', metric);
    fetch(`/api/finance_data?metric=${metric}`)
        .then(response => response.json())
        .then(data => {
            window.financeData = data;
            updateGraph();
        })
        .catch(error => console.error('Error fetching finance data:', error));
}

function updateYearLabels() {
    document.getElementById('start-year-label').textContent = document.getElementById('start-year').value;
    document.getElementById('end-year-label').textContent = document.getElementById('end-year').value;
    updateGraph();
}

function updateGraph() {
    const startYear = parseInt(document.getElementById('start-year').value);
    const endYear = parseInt(document.getElementById('end-year').value);
    const selectedCountries = Array.from(document.getElementById('countries').selectedOptions).map(option => option.value);

    if (!window.pisaData || !window.financeData) {
        return;
    }

    const filteredPisaData = filterDataByYearsAndCountries(window.pisaData, startYear, endYear, selectedCountries);
    const filteredFinanceData = filterDataByYearsAndCountries(window.financeData, startYear, endYear, selectedCountries);

    // Code to update the graph using Chart.js or any other library
    // Example:
    const ctx = document.getElementById('data-graph').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: getYearsInRange(startYear, endYear),
            datasets: [
                {
                    label: 'PISA Data',
                    data: filteredPisaData,
                    borderColor: 'blue',
                    fill: false
                },
                {
                    label: 'Finance Data',
                    data: filteredFinanceData,
                    borderColor: 'green',
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom'
                }
            }
        }
    });
}

function filterDataByYearsAndCountries(data, startYear, endYear, countries) {
    // Filter data based on the selected years and countries
    // This function will depend on the structure of your data
    if (typeof data === 'object' && !Array.isArray(data)) {
        data = Object.entries(data).map(([key, value]) => value);
    }
    return data.filter(entry => {
        const year = parseInt(entry.Year);
        return year >= startYear && year <= endYear && countries.includes(entry.Country);
    });
}

function getYearsInRange(startYear, endYear) {
    const years = [];
    for (let year = startYear; year <= endYear; year++) {
        years.push(year);
    }
    return years;
}