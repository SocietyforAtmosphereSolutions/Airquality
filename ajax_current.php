<!DOCTYPE html>
<html class = 'a'>
  <head>
  <title>Current Values</title>
    <div>
      <h1 class = 'a'>Sunshine Coast Air Quality</h1>
      <input type = 'button' class = 'option' value = 'Home' onclick = "window.location.href = '/index.php'">
      <input type = 'button' class = 'option' value = 'Current Values' onclick = "window.location.href = '/ajax_current.php'">
      <input type = 'button' class = 'option' value = 'Search Engine' onclick = "window.location.href = '/Individual_Search.php'">
    </div>
    <style>
      @import url('CSS/current_vals.css');
      @import url('CSS/global.css');
    </style>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  </head>
  <body>
  <div id= 'region_selection'>
    <select id = 'region' name = 'region' class = 'option' style = 'margin-top: 30px;'>
      <option>Select Region:</option>
      <?php
          $monitor_list = file_get_contents('/home/legal-server/python_code/monitor_list.json');
          $region_array = json_decode($monitor_list, true);
          $array = $region_array["Regions"];
          $x = count($array);

          //echo("<select id = 'region' name = 'region'>");
          for ($i = 0; $i < $x; $i++)
          {
            $region_val = $array[$i]["Name"];
            echo("<option value = '$region_val'>$region_val</option>");
          }
          // echo('</select>');
      ?>
    </select>
  </div><br>
  <div id = 'table'></div>
  </body>
  <script>
    $(document).ready(function() {
    // Variable to hold request
    var request;

    //Triggers when a change occurs in the specified element
    $("#region_selection").on('change','#region', function() {

      // Abort any pending request
      if (request) {
          request.abort();
      }

      var $form = $(this);
      var $inputs = $form.find("select");
      var serializedData = $form.serialize();

	    console.log("Sending Data: " + serializedData);      

      // Disable the inputs for the duration of the Ajax request.
      $inputs.prop("disabled", true);

      request = $.ajax({
          url: "/cur_database_conn.php",
          type: "post",
          dataType: "text",
          data: serializedData
      });

    request.done(function (response, textStatus, jqXHR){
	        $('#table').html(response);
          console.log("Hooray, it worked!");
      });

      request.fail(function (jqXHR, textStatus, errorThrown){
          console.error("Data:" + serializedData +
              "The following error occurred: "+
              textStatus, errorThrown
          );
      });

      request.always(function () {
        // Reenable the inputs
        $inputs.prop("disabled", false);
      });
    });
  });
  </script>
</html>
