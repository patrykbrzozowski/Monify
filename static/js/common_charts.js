// const line_chart = (res, canvas_id) => {
//     let canvas = $(`#${canvas_id}`)
//     const config = {
//         type: 'line',
//         data: {
//             labels: res.labels,
//             datasets: [
//                 {
//                     type: 'scatter',
//                     label: 'Balance Checks',
//                     data: res.data_balance_check,
//                     borderWidth: 2,
//                     backgroundColor: 'rgba(28, 200, 138, 0.1)',
//                     borderColor: 'rgba(28, 200, 138, 1)',
//                 },
//                 {
//                     type: 'scatter',
//                     label: 'Balance Today',
//                     data: res.data_today,
//                     borderWidth: 2,
//                     backgroundColor: 'rgba(246, 194, 62, 0.1)',
//                     borderColor: 'rgba(246, 194, 62, 1)',
//                 },
//                 {
//                     label: 'Balance Estimated',
//                     data: res.data_estimated,
//                     fill: true,
//                     borderWidth: 2,
//                     backgroundColor: "rgba(78, 115, 223, 0.1)",
//                     borderColor: "rgba(78, 115, 223, 1)",
//                     cubicInterpolationMode: 'monotone',
//                     tension: 0.4,
//                     pointRadius: 0,
//                 },
//             ]
//         },
//         options: {
//             maintainAspectRatio: false,
//             layout: {
//                 padding: {
//                     left: 10,
//                     right: 10,
//                     top: 10,
//                     bottom: 5
//                 }
//             },
//             responsive: true,
//             plugins: {
//                 legend: {
//                     position: 'top',
//                 },
//                 title: {
//                     display: false,
//                 },
//                 tooltip: {
//                     mode: 'index',
//                     intersect: false,
//                     position: 'nearest'
//                 }
//             },
//             elements: {
//                 point: {
//                     radius: 4,
//                 }
//             },
//             scales: {
//                 x: {
//                     grid: {
//                         display: false,
//                         drawBorder: false
//                     },
//                     ticks: {
//                         display: true,
//                         autoSkip: true
//                     }
//                 },
//                 y: {
//                     ticks: {
//                         maxTicksLimit: 5,
//                         padding: 10,
//                         // Include a dollar sign in the ticks
//                         callback: function (value, index, values) {
//                             return new Intl.NumberFormat('en-IE', {
//                                 style: 'currency', currency: 'PLN',
//                                 maximumSignificantDigits: 1
//                             }).format(value);
//                         }
//                     },
//                     gridLines: {
//                         color: "rgb(234, 236, 244)",
//                         zeroLineColor: "rgb(234, 236, 244)",
//                         drawBorder: false,
//                         borderDash: [2],
//                         zeroLineBorderDash: [2]
//                     }
//                 },
//             }
//         }
//     };
//     new Chart(canvas, config);
// }

const incomes_vs_outcomes_line_chart = (res, canvas_id, context_label) => {
    let canvas = $(`#${canvas_id}`)
    const config = {
        type: 'bar',
        data:{
            labels: res.month_labels,
            datasets:[
                {
                    label: "Przychody",
                    data: res.total_income_monthly_sum,
                    backgroundColor: "#4ade80",
                    borderWidth: 2,
                    borderRadius: Number.MAX_VALUE,
                    borderSkipped: false,
                },
                {
                    label: "Wydatki",
                    data: res.total_outcome_monthly_sum,
                    backgroundColor: "#f87171",
                    borderWidth: 2,
                    borderRadius: Number.MAX_VALUE,
                    borderSkipped: false,
                }
            ]
        },
        options: {
            barValueSpacing: 20,
            scales:
        {
            y: {
                display: false,
                grid: {
                    drawBorder: false, // <-- this removes y-axis line
                    lineWidth: 0.5,
                }
            },
            x: {
                grid: {
                    drawBorder: false, // <-- this removes y-axis line
                    lineWidth: 0.5,
                }
            }
        },
            plugins : {
          datalebels : {
            display: function(context) {
                return context.dataset.data[context.dataIndex] > 1;
          }
        },
        tooltip: {
            callbacks: {
              label: (context) => {
                return ` ${context.label} - ${context.raw} ${context_label}`
              }
            }
          }
        },
            aspectRatio: 1,
            maintainAspectRatio: false
        }

    };
    new Chart(canvas, config);
}

const line_chart_outcomes = (res, canvas_id, context_label) => {
    let canvas = $(`#${canvas_id}`)
    const config = {
        type: 'bar',
        data: {
            labels: res.labels,
            datasets: [
                {
                    data: res.data,
                    backgroundColor: [
                        'rgb(255, 99, 132)',
                        'rgb(255, 159, 64)',
                        'rgb(255, 205, 86)',
                        'rgb(75, 192, 192)',
                        'rgb(54, 162, 235)',
                        'rgb(153, 102, 255)',
                        'rgb(201, 203, 207)',
                        'rgb(255, 205, 86)',
                        // 'rgb(255, 150, 60)',
                        'rgb(179, 136, 235)',
                        'rgb(247, 174, 248)',
                        'rgb(128, 147, 241)',
                        'rgb(114, 221, 247)',
                        'rgb(253, 197, 245)',
                        'rgb(116, 198, 157)',
                        'rgb(247, 37, 133)',
                        'rgb(156, 102, 68)',
                        'rgb(221, 184, 146)',
                        'rgb(27, 38, 59)',
                        'rgb(90, 24, 154)',
                        // '#f60a0a',
                        // '#2019c0',
                        // '#a81b1b',
                        // '#000000',
                        // '#ffd200',
                        // '#468650',
                        // '#21248a',
                        // '#ff7a00',
                        // '#dfdfdf',
                        // '#b60000',
                        // '#2f8ebc',
                        // '#011d92',
                        // '#dfdfdf',
                        // '#e0be1d',
                        // '#0b66aa',
                        // '#295934',
                        // '#2933d9',
                        // '#00d614',
                        // '#c30000',
                        // '#354dcb',
                        // '#762424',
                        // '#ffc000',
                        // '#6dc0f6',
                        // '#dfdfdf',
                        // '#a07900',
                        // '#ff6000',
                        // '#ff0000',
                        // '#ffbcbc',
                        // '#064a00',
                        // '#201b82',
                        // '#3d2269',
                        // '#294bff',
                        // '#ff3333',
                        // '#f6a900',
                        // '#3c73d3',
                        // '#cf3535',
                        // '#ecc615',
                        // '#c82727',
                        // '#071260',
                    ],
                    borderWidth: 2,
                    borderRadius: Number.MAX_VALUE,
                    borderSkipped: false,
                }
            ]
        },
        options: {
            barValueSpacing: 20,
            scales:
        {
            y: {
                stacked: true,
            },
            x: {
                grid: {
                    drawBorder: false, // <-- this removes y-axis line
                    lineWidth: 0.5,
                }
            }
        },
            plugins : {
                legend: {
                    display: false,
                },
          datalebels : {
            display: function(context) {
                return context.dataset.data[context.dataIndex] > 1;
          }
        },
        tooltip: {
            callbacks: {
              label: (context) => {
                return ` ${context.label} - ${context.raw} ${context_label}`
              }
            }
          }
        },
        },
        responsive: true
    };


    new Chart(canvas, config);

}

const line_chart_progress_503020 = (res, canvas_id, user_currency) => {
    let canvas = $(`#${canvas_id}`)
    const config = {
        type: 'line',
        data: {
            // label: ['Styczen', 'xx', 'ss', 'sdax', 'sda', 'dd', 'ss', 'bb', 'cc', 'ww', 'wa', 'dasd'],
            datasets: [
                {
                    label: 'Niezbędne wydatki - 50% (zawartość)',
                    data: res.year_data.slice(0,12),
                    backgroundColor: [
                        // 'rgb(255, 99, 132)',
                        // 'rgb(255, 159, 64)',
                        // 'rgb(255, 205, 86)',
                        // 'rgb(75, 192, 192)',
                        // 'rgb(54, 162, 235)',
                        // 'rgb(153, 102, 255)',
                        // 'rgb(201, 203, 207)',
                        // 'rgb(255, 205, 86)',
                        // // 'rgb(255, 150, 60)',
                        // 'rgb(179, 136, 235)',
                        // 'rgb(247, 174, 248)',
                        // 'rgb(128, 147, 241)',
                        // 'rgb(114, 221, 247)',
                        // 'rgb(253, 197, 245)',
                        // 'rgb(116, 198, 157)',
                        // 'rgb(247, 37, 133)',
                        // 'rgb(156, 102, 68)',
                        'rgb(221, 184, 146)',
                        // 'rgb(27, 38, 59)',
                        // 'rgb(90, 24, 154)',
                    ],
                    parsing: {
                        yAxisKey: 'box50'
                    }
                },
                {
                    label: 'Niezbędne wydatki - 50% (cel)',
                    data: res.year_data.slice(0,12),
                    backgroundColor: [
                        'rgb(247, 174, 248)',
                    ],
                    parsing: {
                        yAxisKey: 'goal_box50'
                    }
                },
                {
                    label: 'Zbędne wydatki - 30% (zawartość)',
                    data: res.year_data.slice(0,12),
                    backgroundColor: [
                        'rgb(255, 205, 86)',
                    ],
                    parsing: {
                        yAxisKey: 'box30'
                    }
                },
                {
                    label: 'Zbędne wydatki - 30% (cel)',
                    data: res.year_data.slice(0,12),
                    backgroundColor: [
                        'rgb(75, 192, 192)',
                    ],
                    parsing: {
                        yAxisKey: 'goal_box30'
                    }
                },
                {
                    label: 'Oszczędności i inwestycje - 20% (zawartość)',
                    data: res.year_data.slice(0,12),
                    backgroundColor: [
                        'rgb(201, 203, 207)',
                    ],
                    parsing: {
                        yAxisKey: 'box20'
                    }
                },
                {
                    label: 'Oszczędności i inwestycje - 20% (cel)',
                    data: res.year_data.slice(0,12),
                    backgroundColor: [
                        'rgb(128, 147, 241)',
                    ],
                    parsing: {
                        yAxisKey: 'goal_box20'
                    }
                },
            ]
        },
        options: {
            // barValueSpacing: 20,
            parsing: {
                xAxisKey: 'month',
            },
            plugins : {
          
        tooltip: {
            callbacks: {
              label: (context) => {
                // console.log(context)
                return ` ${context.dataset.label} - ${context.formattedValue} ${user_currency}`
              }
            }
          }
        },
            scales:
        {
            // y: {
            //     stacked: true,
            // },
            // x: {
            //     max: 2,
            // }
        },
        },
        responsive: true
    };


    new Chart(canvas, config);

}

const line_chart_progress_6jars = (res, canvas_id, user_currency) => {
    let canvas = $(`#${canvas_id}`)
    const config = {
        type: 'line',
        data: {
            // label: ['Styczen', 'xx', 'ss', 'sdax', 'sda', 'dd', 'ss', 'bb', 'cc', 'ww', 'wa', 'dasd'],
            datasets: [
                {
                    label: 'Słoik 1 - Niezbędne wydatki (zawartość)',
                    data: res.year_data.slice(0,12),
                    backgroundColor: [
                        'rgb(221, 184, 146)',
                    ],
                    parsing: {
                        yAxisKey: 'jar1'
                    }
                },
                {
                    label: 'Słoik 1 - Niezbędne wydatki (cel)',
                    data: res.year_data.slice(0,12),
                    backgroundColor: [
                        'rgb(247, 174, 248)',
                    ],
                    parsing: {
                        yAxisKey: 'goal_jar_1'
                    }
                },
                {
                    label: 'Słoik 2 - Duże/niespodziewane wydatki (zawartość)',
                    data: res.year_data.slice(0,12),
                    backgroundColor: [
                        'rgb(255, 205, 86)',
                    ],
                    parsing: {
                        yAxisKey: 'jar2'
                    }
                },
                {
                    label: 'Słoik 2 - Duże/niespodziewane wydatki (cel)',
                    data: res.year_data.slice(0,12),
                    backgroundColor: [
                        'rgb(75, 192, 192)',
                    ],
                    parsing: {
                        yAxisKey: 'goal_jar_2345'
                    }
                },
                {
                    label: 'Słoik 3 - Przyjemności/rozrywka (zawartość)',
                    data: res.year_data.slice(0,12),
                    backgroundColor: [
                        'rgb(201, 203, 207)',
                    ],
                    parsing: {
                        yAxisKey: 'jar3'
                    }
                },
                {
                    label: 'Słoik 3 - Przyjemności/rozrywka (cel)',
                    data: res.year_data.slice(0,12),
                    backgroundColor: [
                        'rgb(128, 147, 241)',
                    ],
                    parsing: {
                        yAxisKey: 'goal_jar_2345'
                    }
                },
                {
                    label: 'Słoik 4 - Edukacja (zawartość)',
                    data: res.year_data.slice(0,12),
                    backgroundColor: [
                        'rgb(114, 221, 247)',
                    ],
                    parsing: {
                        yAxisKey: 'jar4'
                    }
                },
                {
                    label: 'Słoik 4 - Edukacja (cel)',
                    data: res.year_data.slice(0,12),
                    backgroundColor: [
                        'rgb(253, 197, 245)',
                    ],
                    parsing: {
                        yAxisKey: 'goal_jar_2345'
                    }
                },
                {
                    label: 'Słoik 5 - Oszczędności/inwestycje (zawartość)',
                    data: res.year_data.slice(0,12),
                    backgroundColor: [
                        'rgb(116, 198, 157)',
                    ],
                    parsing: {
                        yAxisKey: 'jar5'
                    }
                },
                {
                    label: 'Słoik 5 - Oszczędności/inwestycje (cel)',
                    data: res.year_data.slice(0,12),
                    backgroundColor: [
                        'rgb(247, 37, 133)',
                    ],
                    parsing: {
                        yAxisKey: 'goal_jar_2345'
                    }
                },
                {
                    label: 'Słoik 6 - Pomoc innym/dobroczynność (zawartość)',
                    data: res.year_data.slice(0,12),
                    backgroundColor: [
                        'rgb(156, 102, 68)',
                    ],
                    parsing: {
                        yAxisKey: 'jar6'
                    }
                },
                {
                    label: 'Słoik 6 - Pomoc innym/dobroczynność (cel)',
                    data: res.year_data.slice(0,12),
                    backgroundColor: [
                        'rgb(27, 38, 59)',
                    ],
                    parsing: {
                        yAxisKey: 'goal_jar_6'
                    }
                },
            ]
        },
        options: {
            // barValueSpacing: 20,
            parsing: {
                xAxisKey: 'month',
            },
            plugins : {
          
        tooltip: {
            callbacks: {
              label: (context) => {
                // console.log(context)
                return ` ${context.dataset.label} - ${context.formattedValue} ${user_currency}`
              }
            }
          }
        },
            scales:
        {
            // y: {
            //     stacked: true,
            // },
            // x: {
            //     max: 2,
            // }
        },
        },
        responsive: true
    };


    new Chart(canvas, config);

}

const doughnut_chart = (res, canvas_id) => {
    let canvas = $(`#${canvas_id}`)
    const config = {
        type: 'doughnut',
        data: {
            labels: res.labels,
            datasets: [
                {
                    data: res.data,
                    backgroundColor: [
                        'rgb(255, 99, 132)',
                        'rgb(255, 159, 64)',
                        'rgb(255, 205, 86)',
                        'rgb(75, 192, 192)',
                        'rgb(54, 162, 235)',
                        'rgb(153, 102, 255)',
                        'rgb(201, 203, 207)',
                        'rgb(255, 205, 86)',
                        // 'rgb(255, 150, 60)',
                        'rgb(179, 136, 235)',
                        'rgb(247, 174, 248)',
                        'rgb(128, 147, 241)',
                        'rgb(114, 221, 247)',
                        'rgb(253, 197, 245)',
                        'rgb(116, 198, 157)',
                        'rgb(247, 37, 133)',
                        'rgb(156, 102, 68)',
                        'rgb(221, 184, 146)',
                        'rgb(27, 38, 59)',
                        'rgb(90, 24, 154)',
                        // '#f60a0a',
                        // '#2019c0',
                        // '#a81b1b',
                        // '#000000',
                        // '#ffd200',
                        // '#468650',
                        // '#21248a',
                        // '#ff7a00',
                        // '#dfdfdf',
                        // '#b60000',
                        // '#2f8ebc',
                        // '#011d92',
                        // '#dfdfdf',
                        // '#e0be1d',
                        // '#0b66aa',
                        // '#295934',
                        // '#2933d9',
                        // '#00d614',
                        // '#c30000',
                        // '#354dcb',
                        // '#762424',
                        // '#ffc000',
                        // '#6dc0f6',
                        // '#dfdfdf',
                        // '#a07900',
                        // '#ff6000',
                        // '#ff0000',
                        // '#ffbcbc',
                        // '#064a00',
                        // '#201b82',
                        // '#3d2269',
                        // '#294bff',
                        // '#ff3333',
                        // '#f6a900',
                        // '#3c73d3',
                        // '#cf3535',
                        // '#ecc615',
                        // '#c82727',
                        // '#071260',
                    ],
                    hoverOffset: 4,
                }
            ]
        },
        options: {
            plugins: {
                legend: {
                    display: false,
                },
            },
            maintainAspectRatio: false,
            layout: {
                padding: {
                    left: 5,
                    right: 5,
                    top: 5,
                    bottom: 5
                }
            },
            
        },
        responsive: true
    };

    let myChart = null;

    if(myChart!= null) {
        myChart.destroy()
    }

    myChart = new Chart(canvas, config);
}

const doughnut_chart_outcomes = (res, canvas_id, context_label) => {
    let canvas = $(`#${canvas_id}`)
    const config = {
        type: 'doughnut',
        data: {
            labels: res.labels,
            datasets: [
                {
                    data: res.data,
                    backgroundColor: [
                        'rgb(255, 99, 132)',
                        'rgb(255, 159, 64)',
                        'rgb(255, 205, 86)',
                        'rgb(75, 192, 192)',
                        'rgb(54, 162, 235)',
                        'rgb(153, 102, 255)',
                        'rgb(201, 203, 207)',
                        'rgb(255, 205, 86)',
                        // 'rgb(255, 150, 60)',
                        'rgb(179, 136, 235)',
                        'rgb(247, 174, 248)',
                        'rgb(128, 147, 241)',
                        'rgb(114, 221, 247)',
                        'rgb(253, 197, 245)',
                        'rgb(116, 198, 157)',
                        'rgb(247, 37, 133)',
                        'rgb(156, 102, 68)',
                        'rgb(221, 184, 146)',
                        'rgb(27, 38, 59)',
                        'rgb(90, 24, 154)',
                        // '#f60a0a',
                        // '#2019c0',
                        // '#a81b1b',
                        // '#000000',
                        // '#ffd200',
                        // '#468650',
                        // '#21248a',
                        // '#ff7a00',
                        // '#dfdfdf',
                        // '#b60000',
                        // '#2f8ebc',
                        // '#011d92',
                        // '#dfdfdf',
                        // '#e0be1d',
                        // '#0b66aa',
                        // '#295934',
                        // '#2933d9',
                        // '#00d614',
                        // '#c30000',
                        // '#354dcb',
                        // '#762424',
                        // '#ffc000',
                        // '#6dc0f6',
                        // '#dfdfdf',
                        // '#a07900',
                        // '#ff6000',
                        // '#ff0000',
                        // '#ffbcbc',
                        // '#064a00',
                        // '#201b82',
                        // '#3d2269',
                        // '#294bff',
                        // '#ff3333',
                        // '#f6a900',
                        // '#3c73d3',
                        // '#cf3535',
                        // '#ecc615',
                        // '#c82727',
                        // '#071260',
                    ],
                    hoverOffset: 4,
                }
            ]
        },
        options: {
            plugins: {
                legend: {
                    display: false,
                },
                tooltip: {
                  callbacks: {
                    label: (context) => {
                      // console.log(context)
                      return ` ${context.label} - ${context.parsed} ${context_label}`
                    }
                  }
                },
            },
            layout: {
                padding: {
                    left: 5,
                    right: 5,
                    top: 5,
                    bottom: 5
                }
            },
            responsive: true,
            maintainAspectRatio: true
        },
        
    };


    if(myChart_outcomes!= null) {
        myChart_outcomes.destroy()
    }

      myChart_outcomes = new Chart(canvas, config);

}

const doughnut_chart_incomes = (res, canvas_id, context_label) => {
    let canvas = $(`#${canvas_id}`)
    const config = {
        type: 'doughnut',
        data: {
            labels: res.labels,
            datasets: [
                {
                    data: res.data,
                    backgroundColor: [
                        'rgb(255, 99, 132)',
                        'rgb(255, 159, 64)',
                        'rgb(255, 205, 86)',
                        'rgb(75, 192, 192)',
                        'rgb(54, 162, 235)',
                        'rgb(153, 102, 255)',
                        'rgb(201, 203, 207)',
                        'rgb(255, 205, 86)',
                        // 'rgb(255, 150, 60)',
                        'rgb(179, 136, 235)',
                        'rgb(247, 174, 248)',
                        'rgb(128, 147, 241)',
                        'rgb(114, 221, 247)',
                        'rgb(253, 197, 245)',
                        'rgb(116, 198, 157)',
                        'rgb(247, 37, 133)',
                        'rgb(156, 102, 68)',
                        'rgb(221, 184, 146)',
                        'rgb(27, 38, 59)',
                        'rgb(90, 24, 154)',
                        // '#f60a0a',
                        // '#2019c0',
                        // '#a81b1b',
                        // '#000000',
                        // '#ffd200',
                        // '#468650',
                        // '#21248a',
                        // '#ff7a00',
                        // '#dfdfdf',
                        // '#b60000',
                        // '#2f8ebc',
                        // '#011d92',
                        // '#dfdfdf',
                        // '#e0be1d',
                        // '#0b66aa',
                        // '#295934',
                        // '#2933d9',
                        // '#00d614',
                        // '#c30000',
                        // '#354dcb',
                        // '#762424',
                        // '#ffc000',
                        // '#6dc0f6',
                        // '#dfdfdf',
                        // '#a07900',
                        // '#ff6000',
                        // '#ff0000',
                        // '#ffbcbc',
                        // '#064a00',
                        // '#201b82',
                        // '#3d2269',
                        // '#294bff',
                        // '#ff3333',
                        // '#f6a900',
                        // '#3c73d3',
                        // '#cf3535',
                        // '#ecc615',
                        // '#c82727',
                        // '#071260',
                    ],
                    hoverOffset: 4,
                }
            ]
        },
        options: {
            plugins: {
                legend: {
                    display: false,
                },
                tooltip: {
                  callbacks: {
                    label: (context) => {
                      // console.log(context)
                      return ` ${context.label} - ${context.parsed} ${context_label}`
                    }
                  }
                }
            },
            layout: {
                padding: {
                    left: 5,
                    right: 5,
                    top: 5,
                    bottom: 5
                }
            },
            responsive: true,
            maintainAspectRatio: true
        },
    };


    if(myChart_incomes!= null) {
        myChart_incomes.destroy()
    }

      myChart_incomes = new Chart(canvas, config);

}

const bar_chart_incomes = (res, canvas_id, context_label) => {
    let canvas = $(`#${canvas_id}`)
    const config = {
        type: 'bar',
        data: {
            labels: res.labels,
            datasets: [
                {
                    data: res.data,
                    backgroundColor: "#4ade80",
                    borderWidth: 2,
                    borderRadius: Number.MAX_VALUE,
                    borderSkipped: false,
                    hoverOffset: 4,
                }
            ]
        },
        options: {
            barValueSpacing: 20,
            scales:
        {
            y: {
                display: false,
                grid: {
                    drawBorder: false, // <-- this removes y-axis line
                    lineWidth: 0.5,
                }
            },
            x: {
                grid: {
                    drawBorder: false, // <-- this removes y-axis line
                    lineWidth: 0.5,
                }
            }
        },
            plugins: {
                legend: {
                    display: false,
                },
                tooltip: {
                  callbacks: {
                    label: (context) => {
                      // console.log(context)
                      return ` ${context.label} - ${context.raw} ${context_label}`
                    }
                  }
                }
            },
            layout: {
                padding: {
                    left: 5,
                    right: 5,
                    top: 5,
                    bottom: 5
                }
            },
            aspectRatio: 1,
            maintainAspectRatio: false
        },
    };


    if(myChart_bar_incomes!= null) {
        myChart_bar_incomes.destroy()
    }

      myChart_bar_incomes = new Chart(canvas, config);

}

const bar_chart_outcomes = (res, canvas_id, context_label) => {
    let canvas = $(`#${canvas_id}`)
    const config = {
        type: 'bar',
        data: {
            labels: res.labels,
            datasets: [
                {
                    data: res.data,
                    backgroundColor: "#f87171",
                    borderWidth: 2,
                    borderRadius: Number.MAX_VALUE,
                    borderSkipped: false,
                    hoverOffset: 4,
                }
            ]
        },
        options: {
          barValueSpacing: 20,
            scales:
        {
            y: {
                display: false,
                grid: {
                    drawBorder: false, // <-- this removes y-axis line
                    lineWidth: 0.5,
                }
            },
            x: {
                grid: {
                    drawBorder: false, // <-- this removes y-axis line
                    lineWidth: 0.5,
                }
            }
        },
            plugins: {
                legend: {
                    display: false,
                },
                tooltip: {
                  callbacks: {
                    label: (context) => {
                      // console.log(context)
                      return ` ${context.label} - ${context.raw} ${context_label}`
                    }
                  }
                }
            },
            layout: {
                padding: {
                    left: 5,
                    right: 5,
                    top: 5,
                    bottom: 5
                }
            },
            aspectRatio: 1,
            maintainAspectRatio: false
        },
    };


    if(myChart_bar_outcomes!= null) {
      myChart_bar_outcomes.destroy()
    }

    myChart_bar_outcomes = new Chart(canvas, config);

}
