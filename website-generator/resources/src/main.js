// Get scoreboard database
let charts = document.getElementById("charts");
let database = JSON.parse(charts.getAttribute("database"));

let palette = {
    passed: '#adff2f',
    failed: '#e93d27',
    font: '#c7d4d3'
}
Chart.defaults.global.defaultFontColor = palette.font;

// Generate circle charts
for (let framework in database) {
    let circle_chart = document.getElementById('circle_' + database[framework].name);
    let trend = database[framework].trend;
    let last_idx = trend.length - 1;
    let chart_data = {
        labels: ['Passed', 'Failed'],
        datasets: [{
            backgroundColor: [palette.passed, palette.failed],
            borderWidth: 0,
            data: [trend[last_idx].passed,
                trend[last_idx].failed
            ]
        }]
    }

    new Chart(circle_chart, {
        type: 'doughnut',
        data: chart_data,
        options: {
            legend: { position: 'bottom' },
            cutoutPercentage: 80,
            title: {
                display: true,
                text: database[framework].name
            }
        }
    });
}

// Generate bar chart
let bar_chart = document.getElementById('bar_chart');
let bar_chart_labels = [];
let bar_chart_datasets = [{
        data: [],
        backgroundColor: palette.passed,
        label: "Passed"
    },
    {
        data: [],
        backgroundColor: palette.failed,
        label: "Failed"
    }
]
for (let framework in database) {
    let trend = database[framework].trend;
    let last_idx = trend.length - 1;
    bar_chart_labels.push(database[framework].name)
    bar_chart_datasets[0].data.push(trend[last_idx].passed);
    bar_chart_datasets[1].data.push(trend[last_idx].failed);
}

new Chart(bar_chart, {
    type: 'bar',
    data: {
        labels: bar_chart_labels,
        datasets: bar_chart_datasets
    },
    options: {
        title: {
            fontSize: 40,
            display: true,
            text: ""
        },
        legend: {
            display: true,
            position: 'bottom'
        },
        scales: {
            xAxes: [{
                barPercentage: 0.4,
                categoryPercentage: 0.5
            }],
            yAxes: [{
                ticks: {
                    beginAtZero: true
                },
                scaleLabel: {
                    fontSize: 20,
                    display: true,
                    labelString: "unit tests"
                }
            }]
        }
    }
});