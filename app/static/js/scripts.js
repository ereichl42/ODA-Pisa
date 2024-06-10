document.addEventListener("DOMContentLoaded", function () {
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            const pisaData = data.pisa;
            const financeData = data.finance;

            // Extract years
            const years = Object.keys(pisaData).sort();

            // Set time period input value
            document.getElementById('time-period').value = `${years[0]}-${years[years.length - 1]}`;

            // Populate countries select
            const countriesSelect = document.getElementById('countries');
            const countryNames = data.country_names;
            for (const [name, code] of Object.entries(countryNames)) {
                const option = document.createElement('option');
                option.value = code;
                option.text = name;
                countriesSelect.add(option);
            }

            // Create initial chart
            const chart = createChart(years, []);

            // Add event listener for country selection changes
            document.getElementById('countries').addEventListener('change', function () {
                const selectedCountries = Array.from(countriesSelect.selectedOptions).map(option => option.value);
                const datasets = generateDatasets(selectedCountries, pisaData, financeData, years);
                updateChart(chart, years, datasets);
            });

            // Initial load
            const initialCountries = Array.from(countriesSelect.selectedOptions).map(option => option.value);
            const initialDatasets = generateDatasets(initialCountries, pisaData, financeData, years);
            updateChart(chart, years, initialDatasets);
        });
});

function toggleOECDCountries() {
    const oecdCountries = ["AT", "AU", "BE", "CA", "CL", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IS", "IE", "IL", "IT", "JP", "KR", "LV", "LT", "LU", "MX", "NL", "NZ", "NO", "PL", "PT", "SK", "SI", "ES", "SE", "CH", "TR", "GB", "US"];
    const countriesSelect = document.getElementById('countries');
    const oecdChecked = document.getElementById('oecd').checked;

    for (const option of countriesSelect.options) {
        if (oecdCountries.includes(option.value)) {
            option.selected = oecdChecked;
        }
    }
}

function fetchData() {
    const timePeriod = document.getElementById('time-period').value;
    const countriesSelect = document.getElementById('countries');
    const selectedCountries = Array.from(countriesSelect.selectedOptions).map(option => option.value);

    if (selectedCountries.length === 0) {
        alert("Please select at least one country.");
        return;
    }

    fetch('/api/fetch_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ time_period: timePeriod, countries: selectedCountries })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                document.getElementById('result').textContent = JSON.stringify(data, null, 4);
            }
        });
}

function generatePlot() {
    const timePeriod = document.getElementById('time-period').value;
    const countriesSelect = document.getElementById('countries');
    const selectedCountries = Array.from(countriesSelect.selectedOptions).map(option => option.value);

    if (selectedCountries.length === 0) {
        alert("Please select at least one country.");
        return;
    }

    fetch('/api/plot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ time_period: timePeriod, countries: selectedCountries })
    })
        .then(response => {
            if (response.ok) {
                return response.blob();
            } else {
                return response.json().then(data => { throw new Error(data.error); });
            }
        })
        .then(blob => {
            const url = URL.createObjectURL(blob);
            const img = document.getElementById('plot');
            img.src = url;
            img.style.display = 'block';
        })
        .catch(error => {
            alert(error.message);
        });
}

function generateDatasets(countries, pisaData, financeData, years) {
    const datasets = [];

    countries.forEach(countryCode => {
        if (pisaData[countryCode]) {
            const pisaResults = years.map(year => pisaData[countryCode][year] ? pisaData[countryCode][year].score : null);
            datasets.push({
                label: `PISA Results - ${countryCode}`,
                data: pisaResults,
                borderColor: getRandomColor(),
                fill: false
            });
        }
    });

    countries.forEach(countryCode => {
        if (financeData.education_levels[countryCode]) {
            for (const [level, levelData] of Object.entries(financeData.education_levels[countryCode].countries)) {
                const expenditureData = years.map(year => levelData[year] ? levelData[year] : null);
                datasets.push({
                    label: `Financial Expenditure - ${countryCode} - ${level}`,
                    data: expenditureData,
                    borderColor: getRandomColor(),
                    fill: false
                });
            }
        }
    });

    return datasets;
}

function createChart(labels, datasets) {
    const ctx = document.getElementById('chart').getContext('2d');
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Education Investments and PISA Results'
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'year'
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function updateChart(chart, labels, datasets) {
    chart.data.labels = labels;
    chart.data.datasets = datasets;
    chart.update();
}

function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}
