var avgdropdown = "<select id = 'avg_options' style = 'margin-top: 5px;''>" +
"<option hidden disabled selected value>-- Select Option --</option>" +
    "<option value = '0'>Current Reading</option>" +
    "<option value = '1'>1 hr Average</option>" +
    "<option value = '2'>3 hr Average</option>" +
    "<option value = '3'>6 hr Average</option>" +
    "<option value = '4'>24 hr Average</option>" +
"<select>";
var zoomdropdown = "<select id = 'zoom_options' style = 'margin-top: 5px;'>" +
"<option hidden disabled selected value>-- Select Option --</option>" +
    "<option value = '1'>Center on Location</option>" +
    "<option value = '0'>Center on Gibsons</option>" +
"<select>";
var correctdropdown = "<select id = 'correction_factor'>" +
"<option hidden disabled selected value>-- Select Option --</option>" +
    "<option value = '0'>No Correction Factor</option>" +
    "<option value = '1'>AQ-SPEC</option>" +
    "<option value = '2'>LRAPA</option>" +
    "<option value = '3'>U of Utah</option>" +
    "<option value = '4'>UNBC</option>" +
"<select>";
var pm_image = "https://scairquality.ca/Map_Icons/slider_custom_white.png";
   

var menustring = "<p class = 'menu'><br><b>Correction Factor: </b>" + correctdropdown + "<br><b>Location Zoom: " + zoomdropdown + "<br><b>Historical Averages: " + avgdropdown + "<br>" + "<img class = 'pm' src='" + pm_image + "'>";

var hist_data;
var chart_view = '_daily';
unit = '-3';
supunit = unit.sup();


function openPopup()
{
    $('#settings').html(menustring);
    console.log(menustring);
}

function ajaxRetrieve()
{
$(document).ready(function() {
    // Variable to hold request
    var request;

    // Abort any pending request
    if (request) {
        request.abort();
    }

    request = $.ajax({
        url: "/cur_database_conn_json.php",
        type: "get",
        dataType: "json"
    });

    request.done(function (response, textStatus, jqXHR){
        var correction = Cookies.get('correction_factor');
        var averages = Cookies.get('average');
        setMarkers(response, correction, averages);
        //console.log(response);
        //console.log("Hooray, it worked!");
    });

    request.fail(function (jqXHR, textStatus, errorThrown){
        console.error(
            "The following error occurred: " +
            textStatus, errorThrown
        );
    });
});
}

function deleteMarkers()
{
for (let i = 0; i < markers.length; i++)
{
    markers[i].setMap(null);
}
markers = [];
}

var infowindow;
function setMarkers(values, correctiontype, average)
{
if (typeof infowindow == 'undefined'){
    infowindow_status = null;
}
else {
    infowindow_status = infowindow.getMap();
}

//console.log(infowindow_status);
if ((infowindow_status == null) || (typeof infowindow_status == 'undefined'))
{
    var message;
    infowindow = new google.maps.InfoWindow();
    //console.log("Updating Markers");

    deleteMarkers();

    master = values;

    var icon_10 = {
    url: "https://scairquality.ca/Map_Icons/Map_Icon_10.png",
    scaledSize: new google.maps.Size(30, 30),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(15,15)
    };

    var icon_20 = {
    url: "https://scairquality.ca/Map_Icons/Map_Icon_20.png",
    scaledSize: new google.maps.Size(30, 30),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(15,15)
    };

    var icon_30 = {
    url: "https://scairquality.ca/Map_Icons/Map_Icon_30.png",
    scaledSize: new google.maps.Size(30, 30),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(15,15)
    };

    var icon_40 = {
    url: "https://scairquality.ca/Map_Icons/Map_Icon_40.png",
    scaledSize: new google.maps.Size(30, 30),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(15,15)
    };

    var icon_50 = {
    url: "https://scairquality.ca/Map_Icons/Map_Icon_50.png",
    scaledSize: new google.maps.Size(30, 30),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(15,15)
    };

    var icon_60 = {
    url: "https://scairquality.ca/Map_Icons/Map_Icon_60.png",
    scaledSize: new google.maps.Size(30, 30),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(15,15)
    };

    var icon_70 = {
    url: "https://scairquality.ca/Map_Icons/Map_Icon_70.png",
    scaledSize: new google.maps.Size(30, 30),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(15,15)
    };

    var icon_80 = {
    url: "https://scairquality.ca/Map_Icons/Map_Icon_80.png",
    scaledSize: new google.maps.Size(30, 30),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(15,15)
    };

    var icon_90 = {
    url: "https://scairquality.ca/Map_Icons/Map_Icon_90.png",
    scaledSize: new google.maps.Size(30, 30),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(15,15)
    };

    var icon_100 = {
    url: "https://scairquality.ca/Map_Icons/Map_Icon_100.png",
    scaledSize: new google.maps.Size(30, 30),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(15,15)
    };

    var icon_100plus = {
    url: "https://scairquality.ca/Map_Icons/Map_Icon_100+.png",
    scaledSize: new google.maps.Size(30, 30),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(15,15)
    };

    var icon_NA = {
    url: "https://scairquality.ca/Map_Icons/Map_Icon_NA.png",
    scaledSize: new google.maps.Size(30, 30),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(15,15)
    };

    for (let i = 0; i < master.length; i++)
    {
        //Sets the Lat Lng and Air quality Value for each sensor
        var location = new google.maps.LatLng(master[i][4], master[i][5]);

        if (average == 0)
        {
            rounded[i] = String(Math.round(master[i][2] * 10) / 10);
        }
        else if (average == 1)
        {
            rounded[i] = String(Math.round(master[i][6] * 10) / 10);
        }
        else if (average == 2)
        {
            rounded[i] = String(Math.round(master[i][7] * 10) / 10);
        }
        else if (average == 3)
        {
            rounded[i] = String(Math.round(master[i][8] * 10) / 10);
        }
        else if (average == 4)
        {
            rounded[i] = String(Math.round(master[i][9] * 10) / 10);
        }
        else
        {
            rounded[i] = String(Math.round(master[i][2] * 10) / 10);
        }
        

        var icon_type;
        var font_colour = 'white';
        if ((rounded[i] > 100) && (rounded[i] < 1000))
        {
            rounded[i] = Math.round(rounded[i]);
            icon_type = icon_100plus;
            message = "<b style = 'color: red;'>Risk Level: Very High </b><br><b>At Risk Population:</b> Avoid strenuous activities outdoors. Children and the elderly should also avoid outdoor physical exertion.<br>" + 
            "<b>General Population:</b> Reduce or reschedule strenuous activities outdoors, especially if you experience symptoms such as coughing and throat irritiation.<br>";
        }
        else if ((rounded[i] < 100) && (rounded[i] >= 90))
        {
            rounded[i] = Math.round(rounded[i]);
            icon_type = icon_100;
            message = "<b style = 'color: red;'>Risk Level: High </b><br><b>At Risk Population:</b> Reduce or reschedule strenuous activities outdoors. Children and elderly should also take it easy.<br>" + 
            "<b>General Population:</b> Consider reducing or reschedulig strenuous activities outdoors if you are experiencing symptoms as coughing and throat irritation.<br>";
        }
        else if ((rounded[i] < 90) && (rounded[i] >= 80))
        {
            rounded[i] = Math.round(rounded[i]);
            icon_type = icon_90;
            message = "<b style = 'color: red;'>Risk Level: High </b><br><b>At Risk Population:</b> Reduce or reschedule strenuous activities outdoors. Children and elderly should also take it easy.<br>" + 
            "<b>General Population:</b> Consider reducing or reschedulig strenuous activities outdoors if you are experiencing symptoms as coughing and throat irritation.<br>";
        }
        else if ((rounded[i] < 80) && (rounded[i] >= 70))
        {
            rounded[i] = Math.round(rounded[i]);
            icon_type = icon_80;
            message = "<b style = 'color: red;'>Risk Level: High </b><br><b>At Risk Population:</b> Reduce or reschedule strenuous activities outdoors. Children and elderly should also take it easy.<br>" + 
            "<b>General Population:</b> Consider reducing or reschedulig strenuous activities outdoors if you are experiencing symptoms as coughing and throat irritation.<br>";
        }
        else if ((rounded[i] < 70) && (rounded[i] >= 60))
        {
            rounded[i] = Math.round(rounded[i]);
            icon_type = icon_70;
            message = "<b style = 'color: red;'>Risk Level: High </b><br><b>At Risk Population:</b> Reduce or reschedule strenuous activities outdoors. Children and elderly should also take it easy.<br>" + 
            "<b>General Population:</b> Consider reducing or reschedulig strenuous activities outdoors if you are experiencing symptoms as coughing and throat irritation.<br>";
        }
        else if ((rounded[i] < 60) && (rounded[i] >= 50))
        {
            icon_type = icon_60;
            font_colour = 'black';
            message = "<b style = 'color: orange;'>Risk Level: Moderate </b><br><b>At Risk Population:</b> Consider reducing or reschedulig strenuous activities outdoors if you are experiencing symptoms.<br>" + 
            "<b>General Population:</b> No need to modify your usual outdoor activities unless you experience symptoms such as coughing and throat irritation.<br>";
        }
        else if ((rounded[i] < 50) && (rounded[i] >= 40))
        {
            rounded[i] = Math.round(rounded[i]);
            icon_type = icon_50;
            font_colour = 'black';
            message = "<b style = 'color: orange;'>Risk Level: Moderate </b><br><b>At Risk Population:</b> Consider reducing or reschedulig strenuous activities outdoors if you are experiencing symptoms.<br>" + 
            "<b>General Population:</b> No need to modify your usual outdoor activities unless you experience symptoms such as coughing and throat irritation.<br>";
        }
        else if ((rounded[i] < 40) && (rounded[i] >= 30))
        {
            rounded[i] = Math.round(rounded[i]);
            icon_type = icon_40;
            font_colour = 'black';
            message = "<b style = 'color: orange;'>Risk Level: Moderate </b><br><b>At Risk Population:</b> Consider reducing or reschedulig strenuous activities outdoors if you are experiencing symptoms.<br>" + 
            "<b>General Population:</b> No need to modify your usual outdoor activities unless you experience symptoms such as coughing and throat irritation.<br>";
        }
        else if ((rounded[i] < 30) && (rounded[i] >= 20))
        {
            rounded[i] = Math.round(rounded[i]);
            icon_type = icon_30;
            message = "<b style = 'color: green;'>Risk Level: Low </b><br><b>At Risk Population:</b> Enjoy your usual outdoor activities.<br> <b>General Population:</b> Ideal air quality for outdoor activities.<br>";
        }
        else if ((rounded[i] < 20) && (rounded[i] >= 10))
        {
            rounded[i] = Math.round(rounded[i]);
            icon_type = icon_20;
            message = "<b style = 'color: green;'>Risk Level: Low </b><br><b>At Risk Population:</b> Enjoy your usual outdoor activities.<br> <b>General Population:</b> Ideal air quality for outdoor activities.<br>";
        }
        else if ((rounded[i] < 10) && (rounded[i] >= 0))
        {
            icon_type = icon_10;
            font_colour = 'black';
            message = "<b style = 'color: green;'>Risk Level: Low </b><br><b>At Risk Population:</b> Enjoy your usual outdoor activities.<br> <b>General Population:</b> Ideal air quality for outdoor activities.<br>";
        }
        else
        {
            icon_type = icon_NA
        }

        data_pass[i] = {
            "ID": master[i][0], 
            "Name": master[i][1], 
            "Value": rounded[i]
        };
        //console.log(data_pass[i]);

        

        contentstring[i] = "<div id = 'sensor" + master[i][0] + "'> <h3 style = 'margin: 10px; font-size: 1.3em; font-family: 'serif';'>"
        + data_pass[i]["Name"] + " (" + data_pass[i]["ID"] + ")</h3>" + message + "<br><b>Chart Data options: </b> &nbsp;" + "<select id = 'time_period'>" +
            "<option hidden value = '_daily'>Averaging Period</option>" + 
            "<option value = '_daily'>Daily</option>" +
            "<option value = '_hourly'>Hourly</option> " +
        "</select> &nbsp;" +
        "<select id = 'chart_correction'>" +
            "<option hidden disabled selected value>Correction Factor</option>" +
            "<option value = '0'>No Correction Factor</option>" +
            "<option value = '1'>AQ-SPEC</option>" +
            "<option value = '2'>LRAPA</option>" +
            "<option value = '3'>U of Utah</option>" +
            "<option value = '4'>UNBC</option>" +
        "</select>";
    
        //creates new markers
        var label_value = String(correctionFactor(rounded[i], correctiontype));
        var marker = new google.maps.Marker({
                position: location, 
                map: map,
                label: { text: label_value, fontSize: '12px', color: font_colour },
                icon: icon_type
        });
        markers.push(marker);
        
        //creates pop-ups
        google.maps.event.addListener(marker, 'click', (function (marker, i) {
        return function () {
                infowindow.open(map, marker);
                infowindow.setContent(contentstring[i] + "<div class = 'infowindow' id = 'container" + master[i][0] + "'></div></div>");
                
                var latlng = marker.getPosition();
                map_recenter(latlng, 0, -200);

                google.maps.event.addListener(infowindow, 'domready', function(){
                    ajaxhistoricalRetrieve(data_pass[i], chart_view);
                });
                waitForChange(data_pass[i]);
            }
        })(marker, i)); 
    }
}
else
{
    //console.log("Infowindow is open, skipping refresh.")
}
}

function setMapzoom()
{
var current_zoom = Cookies.get("location_zoom");
var gibsons = {lat: 49.401154, lng: -123.5075};

if (current_zoom == 1) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            initialLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
            map.setCenter(initialLocation);
            map.setZoom(10);
        });
    }
}
else
{
    map.setCenter(gibsons);
    map.setZoom(10);
}
}

function correctionFactor(value, type)
{
var corrected;

if (type == 0)
{
    corrected = value;
}
else if (type == 1)
{
    //AQ-SPEC: y = 0.624x + 2.728 (0-100 ug/m3)
    if (value < 100)
    {
        corrected = Math.round(((0.624 * value) + 2.728) * 10) / 10;
    }
    else
    {
        corrected = value;
        console.log("Value did not meet requirements for correction factor")
    }
}
else if (type == 2)
{
    //U of Utah: y = 0.778x + 2.65 (0-60 ug/m3)
    if (value < 60)
    {
        corrected = Math.round(((0.778 * value) + 2.65) * 10) / 10;
    }
    else
    {
        corrected = value;
        console.log("Value did not meet requirements for correction factor")
    }

}
else if (type == 3)
{
    //LRAPA y = 0.5x - 0.66 (0-60 ug/m3)
    if (value < 60)
    {
        corrected = Math.round(((0.5 * value) - 0.66) * 10) /10;
    }
    else
    {
        corrected = value;
        console.log("Value did not meet requirements for correction factor")
    }

}
else if (type == 4)
{
    //UNBC y = 0.68x + 1.91 (0-20 ug/m3)
    //UNBC y = 0.87x - 6.62 (>20 ug/m3)
    if (value < 20)
    {
        corrected = Math.round(((0.68 * value) + 1.91) * 10) / 10;
    }
    else if (value > 20)
    {
        corrected = Math.round(((0.87 * value) - 6.62) * 10) / 10;
    }
    else
    {
        corrected = value;
        console.log("Value did not meet requirements for correction factor")
    }
}
else
{
    corrected = value;
}

return corrected;
}
function ajaxhistoricalRetrieve(sensor, time_period, zoom, cfactor)
{
//console.log("Post: " + sensor["ID"]);
postarray = 'val=' + sensor["ID"] + time_period;
element = "container" + sensor["ID"];
//console.log(element);
$(document).ready(function(){
    var request;

    request = $.ajax({
        url: "/hist_database_conn.php",
        type: "post",
        dataType: "text",
        data: postarray
    });

    request.done(function (response){
        if (typeof cfactor !== 'undefined')
        {
            //console.log(cfactor);
            var corrected = [];
            var data = JSON.parse(response);
            //console.log(data);
            for (i in data[0])
            {
                //console.log("i = " + i);
                var list_part = [];
                for (x in data[0][i])
                {
                    //console.log(data[0][i][x]);
                    var point = [data[0][i][x][0], correctionFactor(data[0][i][x][1], cfactor)];
                    list_part.push(point);
                }
                corrected.push(list_part);
            }
            var final = [];
            final.push(corrected);
            //console.log(final);
            drawChart(sensor, element, final, zoom);
        }
        else
        {
            var json_data = JSON.parse(response);
            drawChart(sensor, element, json_data, zoom);
        }
    });

    request.fail(function(jqXHR, textStatus, errorThrown){
        console.error("The following error occurred: " +
        textStatus, errorThrown
        );
    });
});
}
function drawChart(sensor, element, data, zoom)
{
    //console.log('Placing chart at: ' + element);
    //data_array = JSON.parse(data);
    //console.log(data_array[0]);
    data_array = data;

     mychart = Highcharts.stockChart(element, {
        chart: {
            zoomType: 'x'
        },
        yAxis: {
            title: {
                    text: 'Air Qualiy (&#181g/m<sup>-3</sup>)',
                    type: 'linear',
                    tickInterval: 1,
                    useHTML: true
                },
            opposite: false,
            plotBands: [{
                from: 0,
                to: 10,
                color: '#21c6f5'
            },
            {
                from: 10,
                to: 20,
                color: "#189aca"
            },
            {
                from: 20,
                to: 30,
                color: "#0d6797"
            },
            {
                from: 30,
                to: 40,
                color: "#fffd37"
            },
            {
                from: 40,
                to: 50,
                color: "#ffcc2e"
            },
            {
                from: 50,
                to: 60,
                color: "#fe9a3f"
            },
            {
                from: 60,
                to: 70,
                color: "#fd6769"
            },
            {
                from: 70,
                to: 80,
                color: "#ff3b3b"
            },
            {
                from: 80,
                to: 90,
                color: "#ff0101"
            },
            {
                from: 90,
                to: 100,
                color: "#cb0713"
            },
            {
                from: 100,
                to: 5000,
                color: "#650205"
            }]
        },
        xAxis: {
                type: 'datetime'
        },
        plotOptions: {
                series: {
                    turboThreshold: 0
                }
            },
        series: [{
            name: 'A Channel',
            color: '#00FF00',
            data: data_array[0][0]
        },
        {
            name: 'B Channel',
            color: 'green',
            data: data_array[0][1]
        }],
        rangeSelector: {
            allButtonsEnabled: true,
            enabled: true
        },
        tooltip: {
            valueDecimals: 1,
            valueSuffix: ' &#181g m<sup>-3</sup>',
            useHTML: true
        }
        });

    if (typeof zoom !== 'undefined'){
        mychart.xAxis[0].setExtremes(zoom[0], zoom[1]);
    }
}
function map_recenter(latlng,offsetx,offsety) {
var point1 = map.getProjection().fromLatLngToPoint(
(latlng instanceof google.maps.LatLng) ? latlng : map.getCenter()
);
var point2 = new google.maps.Point(
( (typeof(offsetx) == 'number' ? offsetx : 0) / Math.pow(2, map.getZoom()) ) || 0,
( (typeof(offsety) == 'number' ? offsety : 0) / Math.pow(2, map.getZoom()) ) || 0
);  
map.setCenter(map.getProjection().fromPointToLatLng(new google.maps.Point(
point1.x - point2.x,
point1.y + point2.y
)));
}

function waitForChange(sensor){
$(document).ready(function() {
//Triggers when a change occurs in the specified element
div_id = "sensor" + sensor["ID"];
$("#" + div_id).on('change','#time_period', function() {
var min, max;
({min, max} = mychart.axes[0].getExtremes()); 
var zoom = [min, max];

var time = $("#time_period").val();
ajaxhistoricalRetrieve(sensor, time, zoom);
//console.log("Time period for sensor #" + sensor + " Has been changed to " + time);

});

$("#" + div_id).on('change','#chart_correction', function() {
var min, max;
({min, max} = mychart.axes[0].getExtremes()); 
var zoom = [min, max];

var time = $("#time_period").val();
var correction = $("#chart_correction").val();
ajaxhistoricalRetrieve(sensor, time, zoom, correction);
//console.log("Time period for sensor #" + sensor + " Has been changed to " + time);
});
});
}



