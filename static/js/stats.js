$(document).ready(function () {
  let myChart_outcomes = null;
  let myChart_incomes = null;
  let myChart_bar_incomes = null;
  let myChart_bar_outcomes = null;

  const doughnut_chart_outcomes = (res, canvas_id, context_label) => {
    let canvas = $(`#${canvas_id}`);
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
              'rgb(165,42,42)',
              'rgb(255,127,80)',
              'rgb(255,215,0)',
              'rgb(218,165,32)',
              'rgb(128,128,0)',
              'rgb(240,230,140)',
              'rgb(154,205,50)',
              'rgb(127,255,0)',
              'rgb(152,251,152)',
              'rgb(143,188,143)',
              'rgb(46,139,87)',
              'rgb(32,178,170)',
              'rgb(0,139,139)',
              'rgb(0,255,255)',
              'rgb(127,255,212)',
              'rgb(176,224,230)',
              'rgb(70,130,180)',
              'rgb(0,0,128)',
              'rgb(0,0,255)',
              'rgb(138,43,226)',
              'rgb(72,61,139)',
              'rgb(123,104,238)',
              'rgb(139,0,139)',
              'rgb(153,50,204)',
              'rgb(128,0,128)',
              'rgb(221,160,221)',
              'rgb(255,0,255)',
              'rgb(219,112,147)',
              'rgb(255,105,180)',
              'rgb(255,192,203)',
              'rgb(139,69,19)',
              'rgb(205,133,63)',
              'rgb(210,180,140)',
              'rgb(188,143,143)',
              'rgb(176,196,222)',
              'rgb(169,169,169)',
              'rgb(105,105,105)',
              'rgb(128,0,0)'
            ],
            hoverOffset: 4
          }
        ]
      },
      options: {
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                return ` ${context.label} - ${context.formattedValue} ${context_label}`;
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
      }
    };

    if (myChart_outcomes != null) {
      myChart_outcomes.destroy();
    }
    myChart_outcomes = new Chart(canvas, config);
  };

  const doughnut_chart_incomes = (res, canvas_id, context_label) => {
    let canvas = $(`#${canvas_id}`);
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
              'rgb(90, 24, 154)'
            ],
            hoverOffset: 4
          }
        ]
      },
      options: {
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                return ` ${context.label} - ${context.formattedValue} ${context_label}`;
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
      }
    };

    if (myChart_incomes != null) {
      myChart_incomes.destroy();
    }
    myChart_incomes = new Chart(canvas, config);
  };

  const bar_chart_incomes = (res, canvas_id, context_label) => {
    let canvas = $(`#${canvas_id}`);
    const config = {
      type: 'bar',
      data: {
        labels: res.labels,
        datasets: [
          {
            data: res.data,
            backgroundColor: '#4ade80',
            borderWidth: 2,
            borderRadius: Number.MAX_VALUE,
            borderSkipped: false,
            hoverOffset: 4
          }
        ]
      },
      options: {
        barValueSpacing: 20,
        scales: {
          y: {
            display: false,
            grid: {
              drawBorder: false, // <-- this removes y-axis line
              lineWidth: 0.5
            }
          },
          x: {
            grid: {
              drawBorder: false, // <-- this removes y-axis line
              lineWidth: 0.5
            }
          }
        },
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                return ` ${context.label} - ${context.formattedValue} ${context_label}`;
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
      }
    };

    if (myChart_bar_incomes != null) {
      myChart_bar_incomes.destroy();
    }
    myChart_bar_incomes = new Chart(canvas, config);
  };

  const bar_chart_outcomes = (res, canvas_id, context_label) => {
    let canvas = $(`#${canvas_id}`);
    const config = {
      type: 'bar',
      data: {
        labels: res.labels,
        datasets: [
          {
            data: res.data,
            backgroundColor: '#f87171',
            borderWidth: 2,
            borderRadius: Number.MAX_VALUE,
            borderSkipped: false,
            hoverOffset: 4
          }
        ]
      },
      options: {
        barValueSpacing: 20,
        scales: {
          y: {
            display: false,
            grid: {
              drawBorder: false, // <-- this removes y-axis line
              lineWidth: 0.5
            }
          },
          x: {
            grid: {
              drawBorder: false, // <-- this removes y-axis line
              lineWidth: 0.5
            }
          }
        },
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                return ` ${context.label} - ${context.formattedValue} ${context_label}`;
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
      }
    };

    if (myChart_bar_outcomes != null) {
      myChart_bar_outcomes.destroy();
    }
    myChart_bar_outcomes = new Chart(canvas, config);
  };

  $.get(`/finances/get_income_or_outcome_by_type?get_what=outcome&summary_type=year1&view_type=amount`,
    function (res) {
      doughnut_chart_outcomes(res, 'outcome_by_type', res.context_label);
    }
  );

  $.get(`/finances/get_income_or_outcome_by_type?get_what=income&summary_type=year1&view_type=amount`,
    function (res) {
      doughnut_chart_incomes(res, 'income_by_type', res.context_label);
    }
  );

  $.get(`/finances/get_income_or_outcome_bar_chart?get_what=income&summary_type=year1`,
    function (res) {
      bar_chart_incomes(res, 'income_bar_chart', res.context_label);
    }
  );

  $.get(`/finances/get_income_or_outcome_bar_chart?get_what=outcome&summary_type=year1`,
    function (res) {
      bar_chart_outcomes(res, 'outcome_bar_chart', res.context_label);
    }
  );

  $('#chart-time-type-outcome').on('change', function () {
    let summary_type = $('#chart-time-type-outcome').val();
    let view_type = $('#chart-view-type-outcome').val();
    $.get(`/finances/get_income_or_outcome_by_type?get_what=outcome&summary_type=${summary_type}&view_type=${view_type}`,
      function (res) {
        doughnut_chart_outcomes(res, 'outcome_by_type', res.context_label);
      }
    );
  });

  $('#chart-view-type-outcome').on('change', function () {
    let summary_type = $('#chart-time-type-outcome').val();
    let view_type = $('#chart-view-type-outcome').val();
    $.get(`/finances/get_income_or_outcome_by_type?get_what=outcome&summary_type=${summary_type}&view_type=${view_type}`,
      function (res) {
        doughnut_chart_outcomes(res, 'outcome_by_type', res.context_label);
      }
    );
  });

  $('#chart-time-type-income').on('change', function () {
    let summary_type = $('#chart-time-type-income').val();
    let view_type = $('#chart-view-type-income').val();
    $.get(`/finances/get_income_or_outcome_by_type?get_what=income&summary_type=${summary_type}&view_type=${view_type}`,
      function (res) {
        doughnut_chart_incomes(res, 'income_by_type', res.context_label);
      }
    );
  });

  $('#chart-view-type-income').on('change', function () {
    let summary_type = $('#chart-time-type-income').val();
    let view_type = $('#chart-view-type-income').val();
    $.get(`/finances/get_income_or_outcome_by_type?get_what=income&summary_type=${summary_type}&view_type=${view_type}`,
      function (res) {
        doughnut_chart_incomes(res, 'income_by_type', res.context_label);
      }
    );
  });

  $('#bar-chart-time-type-outcome').on('change', function () {
    let summary_type = $('#bar-chart-time-type-outcome').val();
    $.get(`/finances/get_income_or_outcome_bar_chart?get_what=outcome&summary_type=${summary_type}`,
      function (res) {
        bar_chart_outcomes(res, 'outcome_bar_chart', res.context_label);
      }
    );
  });

  $('#bar-chart-time-type-income').on('change', function () {
    let summary_type = $('#bar-chart-time-type-income').val();
    $.get(`/finances/get_income_or_outcome_bar_chart?get_what=income&summary_type=${summary_type}`,
      function (res) {
        bar_chart_incomes(res, 'income_bar_chart', res.context_label);
      }
    );
  });
});

function alpineInstance() {
  return {
    stats_data: []
  };
}