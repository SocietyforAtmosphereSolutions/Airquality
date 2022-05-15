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

  $sort_region = $_POST['region'];
  $region = ("'" . $sort_region . "'");

  $sql = "SELECT ID, Label, PM2_5Value, Lat, Lon, lastModified FROM cur_avg_data WHERE Region = $region";
  $result = $conn->query($sql);

  if ($result->num_rows > 0)
   {
     echo
     "<div>
         <table border ='1'>
           <tr>
             <th>ID</th>
             <th>Location</th>
             <th>Air Quality Value</th>
            <th>Last Modified</th>
          </tr>";

    while($row = $result->fetch_assoc())
    {
        $id = $row["ID"];
        $label = $row["Label"];
        $value = $row["PM2_5Value"];
        $last = $row["lastModified"];

        echo "<tr>";
        echo "<td>$id</td>";
        echo "<td>$label</td>";
        echo "<td>$value</td>";
        echo "<td>$last</td>";
    }
    echo "</table></div>";
  }
  else
  {
    //echo "0 results";
  }
  $conn->close();
?>

