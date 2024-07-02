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

    // Prepare PISA data for chart
    Object.keys(pisaData).forEach(country => {
        const countryData = pisaData[country];
        const years = Object.keys(countryData).map(year => parseInt(year));
        const pisaValues = years.map(year => countryData[year]);

        datasets.push({
            label: `${country} PISA`,
            data: years.map((year, index) => ({ x: year, y: pisaValues[index] })),
            borderColor: getRandomColor(),
            fill: false,
            yAxisID: 'pisa-axis' // Associate dataset with the PISA y-axis
        });
    });

    // Prepare Finance data for chart
    Object.keys(financeData).forEach(country => {
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
            borderColor: getRandomColor(),
            fill: false,
            yAxisID: 'finance-axis' // Associate dataset with the Finance y-axis
        });
    });

    // Update the finance-axis after calculating min and max
    //chart.options.scales.y[1].min = financeMin;
    //chart.options.scales.y[1].max = financeMax;

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