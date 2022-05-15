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

  $idtable = 'sensor' . $_POST['val'];
  //echo($idtable);

  $sql = "SELECT AChannel, BChannel, lastModified FROM $idtable ORDER BY LastModified";
  $result = $conn->query($sql);

  if ($result->num_rows > 0)
   {
    $monitor_array = array();

    while($row = $result->fetch_assoc())
    {
      $AC = $row["AChannel"];
      $BC = $row["BChannel"];
      $last = $row["lastModified"];

      $date = date_create($last);
      $date_formatted = date_format($date, "U");

      $A_Channel = floatval($AC);
      $B_Channel = floatval($BC);
      $date_epoch = floatval($date_formatted) * 1000;
                    
      $monitor_array1[] = array($date_epoch, $A_Channel);
      $monitor_array2[] = array($date_epoch, $B_Channel);
    }

    $monitor_array[] = array($monitor_array1, $monitor_array2);

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

