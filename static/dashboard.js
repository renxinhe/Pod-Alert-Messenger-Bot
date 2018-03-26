var printer_listings = new Vue({
    el: '#dashboard-table',
    data: {
        printers: [],
        loaded: false,
        load_time: '',
    },
    delimiters: ['[[',']]'],
    methods: {
        loadData: function () {
            console.log(get_current_datetime_str()  + ': Loading job_data...')
            $.get('/job_data', function (data) {
                this.printers = JSON.parse(data);
                this.printers.map( (printer) => {
                    printer.rounded_progress = Math.round(printer.progress).toString();
                    printer.width_progress = printer.rounded_progress.toString() + '%';
                    if (printer.progress_color == 'bg-danger') {
                        printer.progress = '';
                    } else {
                        printer.progress += '%';
                    }
                    return printer;
                });
                this.loaded = true;
                this.load_time = get_current_time_str();
            }.bind(this));
        }
    },
    mounted: function () {
        this.$nextTick(function () {
            this.loadData();
            setInterval(function () {
                this.loadData();
            }.bind(this), 30000); 
        });
    },
});