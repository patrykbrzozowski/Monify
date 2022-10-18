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
                return ` ${context.label} - ${context.formattedValue} ${context_label}`
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


const line_chart_progress_503020 = (res, canvas_id, user_currency) => {
    let canvas = $(`#${canvas_id}`)
    const config = {
        type: 'line',
        data: {
            datasets: [
                {
                    label: 'Niezbędne wydatki - 50% (zawartość)',
                    data: res.year_data.slice(0,12),
                    backgroundColor: [
                        'rgb(221, 184, 146)',
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
            parsing: {
                xAxisKey: 'month',
            },
            plugins : {
          
        tooltip: {
            callbacks: {
              label: (context) => {
                return ` ${context.dataset.label} - ${context.formattedValue} ${user_currency}`
              }
            }
          }
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
            parsing: {
                xAxisKey: 'month',
            },
            plugins : {
          
        tooltip: {
            callbacks: {
              label: (context) => {
                return ` ${context.dataset.label} - ${context.formattedValue} ${user_currency}`
              }
            }
          }
        },
        },
        responsive: true
    };

    new Chart(canvas, config);
}
