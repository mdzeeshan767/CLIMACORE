window.onload = function () {
    const ctx = document.getElementById('tempChart');

    const rows = document.querySelectorAll("table tr");
    const labels = [];
    const data = [];

    rows.forEach((row, index) => {
        if (index === 0) return;
        const cells = row.querySelectorAll("td");
        labels.push(cells[0].innerText);
        data.push(parseFloat(cells[1].innerText));
    });

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Temperature',
                data: data,
                borderWidth: 2
            }]
        }
    });
};
