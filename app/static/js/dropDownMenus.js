
export function populateFinanceMetrics(metrics) {
    const metricSelectionContainer = document.getElementById('finance-metric-selection-box');

    const selectHTML = document.createElement('select');
    selectHTML.setAttribute('id', 'finance-metrics');
    selectHTML.setAttribute('name', 'finance-metrics');

    metrics.forEach(metric => {
        const option = document.createElement('option');
        option.setAttribute('value', metric); // Setting the value attribute to the metric name
        option.textContent = metric.replace(/_/g, ' ').toUpperCase(); // Setting text content to metric name in uppercase
        selectHTML.appendChild(option);
    });

    metricSelectionContainer.innerHTML = ''; // Clear previous content
    metricSelectionContainer.appendChild(selectHTML);
}


export function populatePisaMetrics(metrics) {
    const metricSelectionContainer = document.getElementById('pisa-metric-selection-box');

    const selectHTML = document.createElement('select');
    selectHTML.setAttribute('id', 'pisa-metrics');
    selectHTML.setAttribute('name', 'pisa-metrics');

    metrics.forEach(metric => {
        const option = document.createElement('option');
        option.setAttribute('value', metric); // Setting the value attribute to the metric name
        option.textContent = metric.replace(/_/g, ' ').toUpperCase(); // Setting text content to metric name in uppercase
        selectHTML.appendChild(option);
    });

    metricSelectionContainer.innerHTML = ''; // Clear previous content
    metricSelectionContainer.appendChild(selectHTML);
}
