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

  $sql = "SELECT ID, Label, PM2_5Value, Lat, Lon, lastModified FROM averaged_readings";
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
                    
      $monitor_array[] = array($id, $label, $value, $last, $lat, $lng);
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


