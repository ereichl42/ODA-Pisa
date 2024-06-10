document.addEventListener("DOMContentLoaded", function () {
    // Fetch initial data
    fetch('/api/years_countries')
        .then(response => response.json())
        .then(data => {
            const countriesSelect = document.getElementById('countries');
            for (const [name, code] of Object.entries(data.countries)) {
                const option = document.createElement('option');
                option.value = code;
                option.text = name;
                countriesSelect.add(option);
            }

            const financeMetricSelect = document.getElementById('finance-metric');
            for (const metric of data.finance_metrics) {
                const option = document.createElement('option');
                option.value = metric;
                option.text = metric;
                financeMetricSelect.add(option);
            }
        });

    // Fetch PISA data once on page load
    fetch('/api/pisa_data')
        .then(response => response.json())
        .then(data => {
            window.pisaData = data;
        });

    // Handle applying finance metric
    document.getElementById('apply-metric').addEventListener('click', function () {
        const selectedMetric = document.getElementById('finance-metric').value;
        fetch(`/api/finance_data?metric=${selectedMetric}`)
            .then(response => response.json())
            .then(data => {
                window.financeData = data;
                updateGraph();
            });
    });

    // Handle range slider changes
    document.getElementById('start-year').addEventListener('input', function () {
        document.getElementById('start-year-value').innerText = this.value;
        updateGraph();
    });

    document.getElementById('end-year').addEventListener('input', function () {
        document.getElementById('end-year-value').innerText = this.value;
        updateGraph();
    });

    // Handle country selection changes
    document.getElementById('countries').addEventListener('change', updateGraph);

    function updateGraph() {
        const startYear = document.getElementById('start-year').value;
        const endYear = document.getElementById('end-year').value;
        const selectedCountries = Array.from(document.getElementById('countries').selectedOptions).map(option => option.value);

        // Here you would process the window.pisaData and window.financeData
        // and update the chart accordingly
    }
});
