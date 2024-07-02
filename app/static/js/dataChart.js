// app/static/js/dataChart.js

// chart.js is imported in the index.html file

let chart;

export function initializeChart() {
    const ctx = document.getElementById('data-graph').getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({ length: 23 }, (_, i) => 2000 + i), // Generate years from 2000 to 2022
            datasets:
                [
                    {
                        label: 'PISA',
                        data: [],
                        borderColor: 'rgba(255, 99, 132, 1)',
                        fill: false,
                        yAxisID: 'pisa-axis'
                    },
                    {
                        label: 'Finance',
                        data: [],
                        borderColor: 'rgba(54, 162, 235, 1)',
                        fill: false,
                        yAxisID: 'finance-axis'
                    }
                ]
        },
        options: {
            scales: {
                x: {
                    type: 'category',   // Fitting for years
                    position: 'bottom',
                    title: {
                        display: true,
                        text: 'Year'
                    }
                },
                y: [
                    {
                        id: 'pisa-axis',
                        type: 'linear',
                        position: 'left',
                        beginAtZero: false,
                        // Hard coded min and max for PISA scores (optional, not sure yet)
                        min: 300,
                        max: 700
                    },
                    {
                        id: 'finance-axis',
                        type: 'linear',
                        position: 'right',
                        beginAtZero: false
                        // Actual min and max are set dynamically based on data in updateChartData
                    }
                ]
            }
        }
    });
}


export function updateChartData(pisaData, financeData) {
    const datasets = [];

    // Create list of countries from data and generate colors for them
    const countries = Object.keys(pisaData).concat(Object.keys(financeData));
    const countryColors = generateCountryColors(countries);

    // Prepare PISA data for chart
    Object.keys(pisaData).forEach((country, index) => {
        const countryData = pisaData[country];
        const years = Object.keys(countryData).map(year => parseInt(year));
        const pisaValues = years.map(year => countryData[year]);

        datasets.push({
            label: `${country} PISA`,
            data: years.map((year, index) => ({ x: year, y: pisaValues[index] })),
            borderColor: countryColors[index].color,
            borderDash: [5, 5], // Dashed line
            fill: false,
            yAxisID: 'pisa-axis' // Associate dataset with the PISA y-axis
        });
    });

    // Prepare Finance data for chart
    Object.keys(financeData).forEach((country, index) => {
        const countryData = financeData[country];
        const years = Object.keys(countryData).map(year => parseInt(year));
        const financeValues = years.map(year => {
            let total = 0;
            const levels = Object.keys(countryData[year]);
            // All investments between the investigated education levels are summed up for each year
            levels.forEach(level => total += countryData[year][level]);
            return total;
        });

        datasets.push({
            label: `${country} Finance`,
            data: years.map((year, index) => ({ x: year, y: financeValues[index] })),
            borderColor: countryColors[index].color,
            pointStyle: 'circle', // Dotted line
            pointRadius: 3,
            fill: false,
            yAxisID: 'finance-axis' // Associate dataset with the Finance y-axis
        });
    });

    // Update datasets and refresh the chart
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

// Instead of random colors, the colors should be chosen in a range of colors and based on alphabetical order of the countries
function generateCountryColors(countryNames) {
    const colors = [];
    const sortedCountryNames = countryNames.sort();

    for (let i = 0; i < sortedCountryNames.length; i++) {
        const color = generateColor(i, sortedCountryNames.length);
        colors.push({ country: sortedCountryNames[i], color });
    }

    return colors;
}

function generateColor(index, totalCountries) {
    const hue = (index / totalCountries) * 360;
    const saturation = 70;
    const lightness = 50;

    return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
}