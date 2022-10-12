
$(document).ready(function () {

  $.get("/finances/get_incomes_vs_outcomes_chart", function (res) {
      incomes_vs_outcomes_line_chart(res, 'year_chart_canvas', res.context_label)
  });

  // $.get("/finances/get_progress_data", function (res) {
  //     line_chart_progress_503020(res, 'line_chart_progress_503020', res.user_currency)
  // });

  // $.get("/finances/get_progress_data", function (res) {
  //     line_chart_progress_6jars(res, 'line_chart_progress_6jars', res.user_currency)
  // });

  


  // $.get("/finances/get_income_or_outcome_by_type?get_what=income&summary_type=mon1", function (res) {
  //     doughnut_chart(res, 'income_by_type')
  // });

  // $.get("/finances/get_income_or_outcome_by_type?get_what=outcome&summary_type=mon3", function (res) {
  //     doughnut_chart(res, 'outcome_by_type')
  // });

  // $.get("/finances/get_year_chart?balance_type=savings", function (res) {
  //     line_chart(res, 'savings_year')
  // });

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
