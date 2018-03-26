var PRINTER_SERIALS = ["10094", "10097", "10098", "10213", "10453", "10454", "10025", "10026", "10034", "10035", "10038", "10047"]

function get_all_printer_json() {
    $.get("/job_data", function(data) {
        console.log(data);
        return JSON.parse(data);
    });
}

function get_printer_json(serial) {
    $.get("/job_data/" + serial, function(data) {
        try {
            return JSON.parse(str(data));
        } catch(e) {
            return JSON.parse('{errno: "EJSONPARSE", message:"' + str(data) + '"}');
        }
    });
}

function get_current_datetime_str() {
    var currentdate = new Date();
    var options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZoneName: 'short'
    };
    return currentdate.toLocaleDateString('en-US', options);
}

function get_current_time_str() {
    var currentdate = new Date(); 
    var options = {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZoneName: 'short'
    };
    return currentdate.toLocaleDateString('en-US', options);
}

