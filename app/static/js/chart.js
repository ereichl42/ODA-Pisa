let myChart;

export function initializeChart() {
    const ctx = document.getElementById('data-graph').getContext('2d');
    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [], // Add your labels here
            datasets: [{
                label: 'PISA Data',
                data: [], // Add your PISA data here
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }, {
                label: 'Finance Data',
                data: [], // Add your finance data here
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

export function updateChartData(filteredPisaData, filteredFinanceData, startYear, endYear) {
    myChart.data.labels = getYearsInRange(startYear, endYear);
    myChart.data.datasets[0].data = filteredPisaData;
    myChart.data.datasets[1].data = filteredFinanceData;
    myChart.update();
}

function getYearsInRange(startYear, endYear) {
    const years = [];
    for (let year = startYear; year <= endYear; year++) {
        years.push(year);
    }
    return years;
}

document.addEventListener('DOMContentLoaded', initializeChart);
