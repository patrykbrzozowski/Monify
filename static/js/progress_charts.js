$(document).ready(function () {
    $.get("/finances/get_progress_data", function (res) {
        line_chart_progress_503020(res, 'line_chart_progress_503020', res.user_currency)
    });

    $.get("/finances/get_progress_data", function (res) {
        line_chart_progress_6jars(res, 'line_chart_progress_6jars', res.user_currency)
    });
})

function alpineInstance() {
    return {
      progress_data: [],
      pageNumber: 0,
      size: 3,
      total: "",
      fetchProgressData() {
        fetch('/finances/get_progress_data')
                .then(response => response.json())
                .then(data => this.progress_data = data)
      },

      get filteredYearData() {
        const start = this.pageNumber * this.size,
          end = start + this.size;

          this.total = this.progress_data.year_data?.length || 0;
          return this.progress_data.year_data?.slice(start, end) || this.progress_data.year_data;
      },

      //Create array of all pages (for loop to display page numbers)
      pages() {
        return Array.from({
          length: Math.ceil(this.total / this.size),
        });
      },

      //Next Page
      nextPage() {
        this.pageNumber++;
      },

      //Previous Page
      prevPage() {
        this.pageNumber--;
      },

      //Total number of pages
      pageCount() {
        return Math.ceil(this.total / this.size);
      },

      //Return the start range of the paginated results
      startResults() {
        return this.pageNumber * this.size + 1;
      },

      //Return the end range of the paginated results
      endResults() {
        let resultsOnPage = (this.pageNumber + 1) * this.size;

        if (resultsOnPage <= this.total) {
          return resultsOnPage;
        }

        return this.total;
      },

      //Link to navigate to page
      viewPage(index) {
        this.pageNumber = index;
      },
    };
}
