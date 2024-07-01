document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [], // Add your labels here
            datasets: [{
                label: 'Sample Data',
                data: [], // Add your data here
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
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

    document.getElementById('update-graph').addEventListener('click', function () {
        const countries = Array.from(document.getElementById('countries').selectedOptions).map(option => option.value);
        const financeMetric = document.getElementById('finance-metric').value;
        const startYear = document.getElementById('start-year').value;
        const endYear = document.getElementById('end-year').value;
        const startEducationLevel = document.getElementById('start-education-level').value;
        const endEducationLevel = document.getElementById('end-education-level').value;

        console.log('Selected Countries:', countries);
        console.log('Selected Finance Metric:', financeMetric);
        console.log('Year Range:', startYear, endYear);
        console.log('Education Level Range:', startEducationLevel, endEducationLevel);

        // Update chart data here
        // Example: myChart.data.labels = [...];
        // Example: myChart.data.datasets[0].data = [...];
        // myChart.update();
    });
});
