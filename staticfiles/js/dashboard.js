$(document).ready(function () {

  $.get("/finances/get_incomes_vs_outcomes_chart", function (res) {
      incomes_vs_outcomes_line_chart(res, 'year_chart_canvas', res.context_label)
  });

})

const $greeting = $('#greeting');
const hour = new Date().getHours();

if (hour < 18) $greeting.text('Dzień dobry');
else $greeting.text('Dobry wieczór');

function alpineInstance() {
  return {
    summary_data: []
  };
}
