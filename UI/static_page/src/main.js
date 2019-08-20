/* chart.js chart examples */

Chart.defaults.global.defaultFontColor = '#8494a4';

// chart colors
let palette = {
    green: '#adff2f',
    yellow: '#f4a33c',
    red: '#e93d27',
    background: '#042c34'
}
let colors = [palette.red, palette.green, '#333333', '#c3e6cb', '#dc3545', '#6c757d'];


let onnx_summary = { "failed": 51, "passed": 507, "skipped": 0, "date": "08/01/2019 20:40:05" }
let ngraph_summary = { "failed": 105, "passed": 453, "skipped": 0, "date": "08/01/2019 20:03:03" }
let tensorflow_summary = { "date": "08/01/2019 20:03:03", "failed": 64, "passed": 494, "skipped": 0 }
let pytorch_summary = { "date": "08/06/2019 06:51:40", "failed": 151, "passed": 407, "skipped": 0 }


/* large line chart */

// Parse attribute test
let chLine = document.getElementById("chLine");
let values = chLine.getAttribute("values");
console.log(values)
console.log(typeof(values))
let values_array = JSON.parse(values)
console.log(typeof(values_array))
console.log(values_array)

let chartData = {
    labels: ["S", "M", "T", "W", "T", "F", "S"],
    datasets: [{
            data: [589, 445, 483, 503, 689, 692, 634],
            label: "ONNX-Runtime",
            backgroundColor: 'transparent',
            borderColor: palette.green,
            borderWidth: 4,
            pointBackgroundColor: palette.green
        },
        {
            data: [639, 465, 493, 478, 589, 632, 674],
            label: "nGraph",
            // backgroundColor: colors[3],
            borderColor: palette.yellow,
            borderWidth: 4,
            pointBackgroundColor: palette.yellow
        }
    ]
};
if (chLine) {
    new Chart(chLine, {
        type: 'line',
        data: chartData,
        options: {

            scales: {
                xAxes: [{
                    ticks: {
                        beginAtZero: false
                    }
                }]
            },
            legend: {
                display: true
            },
            responsive: true
        }
    });
}

/* large pie/donut chart */
let chPie = document.getElementById("chPie");
if (chPie) {
    new Chart(chPie, {
        type: 'pie',
        data: {
            labels: ['Desktop', 'Phone', 'Tablet', 'Unknown'],
            datasets: [{
                backgroundColor: [colors[1], colors[0], colors[2], colors[5]],
                borderWidth: 0,
                data: [50, 40, 15, 5]
            }]
        },
        plugins: [{
            beforeDraw: function(chart) {
                let width = chart.chart.width,
                    height = chart.chart.height,
                    ctx = chart.chart.ctx;
                ctx.restore();
                let fontSize = (height / 70).toFixed(2);
                ctx.font = fontSize + "em sans-serif";
                ctx.textBaseline = "middle";
                let text = chart.config.data.datasets[0].data[0] + "%",
                    textX = Math.round((width - ctx.measureText(text).width) / 2),
                    textY = height / 2;
                ctx.fillText(text, textX, textY);
                ctx.save();
            }
        }],
        options: { layout: { padding: 0 }, legend: { display: false }, cutoutPercentage: 80 }
    });
}

/* bar chart */
let chBar = document.getElementById("chBar");
if (chBar) {
    new Chart(chBar, {
        type: 'bar',
        data: {
            labels: ["ONNX-Runtime", "nGraph", "Tensorflow", "Pytorch"],
            datasets: [{
                    data: [onnx_summary.failed, ngraph_summary.failed, tensorflow_summary.failed, pytorch_summary.failed],
                    backgroundColor: colors[0]
                },
                {
                    data: [onnx_summary.passed, ngraph_summary.passed, tensorflow_summary.passed, pytorch_summary.passed],
                    backgroundColor: colors[1]
                }
            ]
        },
        options: {
            legend: {
                display: false
            },
            scales: {
                xAxes: [{
                    barPercentage: 0.4,
                    categoryPercentage: 0.5
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

/* 3 donut charts */
let donutOptions = {
    cutoutPercentage: 85,
    legend: { position: 'bottom', padding: 5, labels: { pointStyle: 'circle', usePointStyle: true } }
};

// ONNX-Runtime - donut1
let chDonutData1 = {
    labels: ['Failed', 'Passed'],
    datasets: [{
        backgroundColor: colors.slice(0, 3),
        borderWidth: 0,
        data: [onnx_summary.failed, onnx_summary.passed, onnx_summary.skipped]
    }]
};

let chDonut1 = document.getElementById("chDonut1");
if (chDonut1) {
    donutOptions.title = {
        display: true,
        text: 'ONNX-Runtime'
    }
    new Chart(chDonut1, {
        type: 'pie',
        data: chDonutData1,
        options: donutOptions
    });
}

//  nGraph - donut2
let chDonutData2 = {
    labels: ['Failed', 'Passed'],
    datasets: [{
        backgroundColor: colors.slice(0, 3),
        borderWidth: 0,
        data: [ngraph_summary.failed, ngraph_summary.passed, ngraph_summary.skipped]
    }]
};
let chDonut2 = document.getElementById("chDonut2");
if (chDonut2) {
    donutOptions.title = {
        display: true,
        text: 'nGraph'
    }
    new Chart(chDonut2, {
        type: 'pie',
        data: chDonutData2,
        options: donutOptions
    });
}

// Tensorflow - donut3
let chDonutData3 = {
    labels: ['Failed', 'Passed'],
    datasets: [{
        backgroundColor: colors.slice(0, 3),
        borderWidth: 0,
        data: [tensorflow_summary.failed, tensorflow_summary.passed, tensorflow_summary.skipped]
    }]
};
let chDonut3 = document.getElementById("chDonut3");
if (chDonut3) {
    donutOptions.title = {
        display: true,
        text: 'Tensorflow'
    }
    new Chart(chDonut3, {
        type: 'pie',
        data: chDonutData3,
        options: donutOptions
    });
}

// Pytorch - donut4
let chDonutData4 = {
    labels: ['Failed', 'Passed'],
    datasets: [{
        backgroundColor: colors.slice(0, 3),
        borderWidth: 0,
        data: [pytorch_summary.failed, pytorch_summary.passed, pytorch_summary.skipped]
    }]
};
let chDonut4 = document.getElementById("chDonut4");
if (chDonut4) {
    donutOptions.title = {
        display: true,
        text: 'Pytorch'
    }
    new Chart(chDonut4, {
        type: 'pie',
        data: chDonutData4,
        options: donutOptions
    });
}

/* 3 line charts */
let lineOptions = {
    legend: { display: false },
    tooltips: { interest: false, bodyFontSize: 11, titleFontSize: 11 },
    scales: {
        xAxes: [{
            ticks: {
                display: false
            },
            gridLines: {
                display: false,
                drawBorder: false
            }
        }],
        yAxes: [{ display: false }]
    },
    layout: {
        padding: {
            left: 6,
            right: 6,
            top: 4,
            bottom: 6
        }
    }
};

let chLine1 = document.getElementById("chLine1");
if (chLine1) {
    new Chart(chLine1, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            datasets: [{
                backgroundColor: '#ffffff',
                borderColor: '#ffffff',
                data: [10, 11, 4, 11, 4],
                fill: false
            }]
        },
        options: lineOptions
    });
}
let chLine2 = document.getElementById("chLine2");
if (chLine2) {
    new Chart(chLine2, {
        type: 'line',
        data: {
            labels: ['A', 'B', 'C', 'D', 'E'],
            datasets: [{
                backgroundColor: '#ffffff',
                borderColor: '#ffffff',
                data: [4, 5, 7, 13],
                fill: false
            }]
        },
        options: lineOptions
    });
}

let chLine3 = document.getElementById("chLine3");
if (chLine3) {
    new Chart(chLine3, {
        type: 'line',
        data: {
            labels: ['Pos', 'Neg', 'Nue', 'Other', 'Unknown'],
            datasets: [{
                backgroundColor: '#ffffff',
                borderColor: '#ffffff',
                data: [13, 15, 10, 9],
                fill: false
            }]
        },
        options: lineOptions
    });
}