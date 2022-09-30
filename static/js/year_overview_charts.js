$(document).ready(function () {

    $.get("/finances/get_year_chart_custom", function (res) {
        line_chart_new(res, 'year_chart_canvas', res.context_label)
    });

    $.get("/finances/get_progress_data", function (res) {
        line_chart_progress_503020(res, 'line_chart_progress_503020', res.user_currency)
    });

    $.get("/finances/get_progress_data", function (res) {
        line_chart_progress_6jars(res, 'line_chart_progress_6jars', res.user_currency)
    });

    


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