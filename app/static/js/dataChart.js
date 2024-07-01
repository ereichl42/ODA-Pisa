// app/static/js/dataChart.js

// chart.js is imported in the index.html file

let chart;

export function initializeChart() {
    const ctx = document.getElementById('data-graph').getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: []
        },
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom'
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

export function updateChartData(pisaData, financeData) {
    const datasets = [];

    // Prepare PISA data for chart
    Object.keys(pisaData).forEach(country => {
        const countryData = pisaData[country];
        const years = Object.keys(countryData).map(year => parseInt(year));
        const pisaValues = years.map(year => countryData[year].combined);

        datasets.push({
            label: `${country} PISA`,
            data: years.map((year, index) => ({ x: year, y: pisaValues[index] })),
            borderColor: getRandomColor(),
            fill: false
        });
    });

    // Prepare Finance data for chart
    Object.keys(financeData).forEach(country => {
        const countryData = financeData[country];
        const years = Object.keys(countryData).map(year => parseInt(year));
        const financeValues = years.map(year => {
            let total = 0;
            const levels = Object.keys(countryData[year]);
            levels.forEach(level => total += countryData[year][level]);
            return total;
        });

        datasets.push({
            label: `${country} Finance`,
            data: years.map((year, index) => ({ x: year, y: financeValues[index] })),
            borderColor: getRandomColor(),
            fill: false
        });
    });

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