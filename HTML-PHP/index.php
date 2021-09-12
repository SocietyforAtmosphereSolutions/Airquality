<!DOCTYPE html>
<html class='a'>
    <!--<meta name='viewport' content='width=device-width, initial-scale=1.00, maximum-scale=1.00, minimum-scale=1.00, user-scalable=no'>-->
    <head>
        <title>Home</title>
        <style>
            @import url('global.css');
            #map 
            {
                height: 100%;
                width: 100%;
                position: absolute;
            }
            #map_container
            {
                height: 100%;
                width: 100%;
            }
            #heading
            {
                position: absolute;
                margin: 0;
                text-align: center;
                left: 50%;
                transform: translate(-50%);
            }
            #settings
            {
                display: block;
                position: absolute;
                text-align: center;
                bottom: 0px;
                width: 200px;
            }
            #menu
            {
                position: fixed;
                height: 25px;
                width: 150px;
                font-size: 14px;
                bottom: 5px;
                left: 25px;
            }
            #logos
            {
                position: fixed;
                height: 25px;
                width: 150px;
                font-size: 14px;
                top: 5px;
                right: 60px;
            }
            #correction_factor
            {
                margin: 2px;
            }
           
        </style>
        <script src ="https://scairquality.ca/map_page_functions.js?2"></script>
        <script src ="https://scairquality.ca/chart_plugin.js"></script>
        <script src="https://code.highcharts.com/stock/highstock.js"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/js-cookie@rc/dist/js.cookie.min.js"></script>
    </head>
    <body style = 'overflow: hidden;'>
        <div id = 'map_container'>
            <div id = 'map'></div>
            <div id = 'heading'>
                <h1 class = 'a'>Sunshine Coast Air Quality</h1>
                <input type = 'button' class = 'option' value = 'Home' onclick = "window.location.href = '/index.php'">
                <input type = 'button' class = 'option' value = 'Current Values' onclick = "window.location.href = '/ajax_current.php'">
                <input type = 'button' class = 'option' value = 'Search Engine' onclick = "window.location.href = '/Individual_Search.php'">
            </div>
            <div id = 'settings'>
                <p class = 'menu'><br><b>Correction Factor: </b>
                <select id = 'correction_factor'>
                    <option hidden disabled selected value>-- Select Option --</option>
                    <option value = '0'>No Correction Factor</option>
                    <option value = '1'>AQ-SPEC</option>
                    <option value = '2'>LRAPA</option>
                    <option value = '3'>U of Utah</option>
                    <option value = '4'>UNBC</option>
                <select><br>
                <b>Location Zoom: <select id = 'zoom_options' style = 'margin-top: 5px;'>
                    <option hidden disabled selected value>-- Select Option --</option>
                    <option value = '1'>Center on Location</option>
                    <option value = '0'>Center on Gibsons</option>
                <select><br>
                <b>Historical Averages: <select id = 'avg_options' style = 'margin-top: 5px;''>
                    <option hidden disabled selected value>-- Select Option --</option>
                    <option value = '0'>Current Reading</option>
                    <option value = '1'>1 hr Average</option>
                    <option value = '2'>3 hr Average</option>
                    <option value = '3'>6 hr Average</option>
                    <option value = '4'>24 hr Average</option>
                <select><br>
                <img class = 'pm' src='https://scairquality.ca/Map_Icons/slider_custom_white.png'>
            </div>
            <div id = 'logos'>
                <p style = 'background-color: #4ABF22; border-radius: 5px; color: white; text-align: center; font-size: 16px; margin: 1px; position: fixed; display: block; height: 200px; width: 350px; right: 1px;'>
                A project of the Sunshine Coast Clean Air Society and Society for Atmosphere Solutions. <br> 
                Made Possible thanks to support from our partners: <br>
                <img style = 'position: fixed; height: 56px; width: 180px; right: 150px; top: 92px;' src = 'https://scairquality.ca/Map_Icons/SCCU.png'><br>
                <img style = 'position: fixed; height: 85px; width: 85px; right: 15px; top: 80px;' src = 'https://scairquality.ca/Map_Icons/SCRD.png'>
                <br><br><br><br><a href>www.atmospheresolutions.ca</a>
            </div>  
        </div>
        <div id = 'container' style = 'width:400px; height:200px;'></div>
        <script>
            var map;
            var is_open = false;
            var open_0 = false;
            var open_1 = false;
            var open_2 = false;
            var master;
            var markers = [];
            var gibsons = {lat: 49.401154, lng: -123.5075};
            var rounded = new Array();
            var data_pass = new Array();
            var contentstring = new Array();
            var current_zoom;

            function initMap()
            {
                map = new google.maps.Map(document.getElementById('map'), {
                    center: gibsons,
                    zoom: 10,
                    mapTypeId: 'terrain',
                    streetViewControl: false,
                    fullscreenControl: false,
                    options: {
                        gestureHandling: 'greedy'
                    }
                });

                //Cookies.set('correction_factor', 0);
                //Cookies.set('average', 0);
                setMapzoom();
                ajaxRetrieve();
                setInterval(ajaxRetrieve, 60*1000);
            }
            
            $(document).ready(function() {
 
            //Triggers when a change occurs in the specified element
            $("#settings").on('change','#correction_factor', function() {

                var correction_type = $("#correction_factor").val();
                Cookies.set('correction_factor', correction_type);
                ajaxRetrieve();
                });
            
            //Triggers when a change occurs in the specified element
            $("#settings").on('change','#avg_options', function() {

                var averages = $("#avg_options").val();
                Cookies.set('average', averages);
                ajaxRetrieve();
                });

            //Triggers when a change occurs in the specified element
            $("#settings").on('change','#zoom_options', function() {

                var correction_type = $("#zoom_options").val();
                Cookies.set('location_zoom', correction_type);
                setMapzoom();
                });
            });
        </script>
        <script async defer
            src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyA_nOosJgGoJYrYGQkXRgRbr7nKYzbgg34&callback=initMap'>
        </script>
    </body>
</html>
