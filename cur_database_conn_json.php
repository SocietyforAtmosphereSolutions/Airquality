<?php
  $servername = "localhost";
  $username = "airdata";
  $password = "AESl0uis!";
  $dbname = "airdata";

  // Create connection
  $conn = new mysqli($servername, $username, $password, $dbname);
  // Check connection
  if ($conn->connect_error)
  {
    die("Connection failed: " . $conn->connect_error);
  }

  $sql = "SELECT ID, Label, PM2_5Value, Lat, Lon, lastModified, v3, v4, v5, v6 FROM cur_avg_data";
  $result = $conn->query($sql);

  if ($result->num_rows > 0)
  {
    $monitor_array = array();

    while($row = $result->fetch_assoc())
    {
      $id = $row["ID"];
      $label = $row["Label"];
      $value = $row["PM2_5Value"];
      $last = $row["lastModified"];
      $lat = $row["Lat"];
      $lng = $row["Lon"]; 
      $v3 = $row["v3"];
      $v4 = $row["v4"];
      $v5 = $row["v5"];
      $v6 = $row["v6"];
                    
      $monitor_array[] = array($id, $label, $value, $last, $lat, $lng, $v3, $v4, $v5, $v6);
    }

    //converts PHP array into a format javascript can interpret
    $javascriptarray = json_encode($monitor_array);

    echo($javascriptarray);
  }
  else
  {
    echo "0 results";
  }
  $conn->close();
?>


