<!DOCTYPE html>
<html class = 'a'>
  <head>
  <title>Current Values</title>
   <div>
    <h1 class = 'a'>Sunshine Coast Air Quality</h1>
    <input class = 'option' value = 'Home' onclick = "window.location.href = '/index.php'">
    <input class = 'option2' value = 'Current Values' onclick = "window.location.href = '/Current_values.php'">
    <input class = 'option3' value = 'Search Engine' onclick = "window.location.href = '/search.php'">
  </div>
    <style>
      @import url('current_vals.css');
    </style>
  </head>
  <body>
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

      #$sql = "SELECT * FROM (SELECT *, max(lastModified) AS max_date FROM monitor_data GROUP BY ID HAVING Region = $region) AS aggregated_table INNER JOIN monitor_data AS table2 ON aggregated_table.max_date=table2.lastModified WHERE table2.Region = $region GROUP BY table2.lastModified ORDER BY table2.ID";                                                        
      $sql = "SELECT ID, Label, PM2_5Value, Lat, Lon, lastModified FROM current_data WHERE Region = $region";
      $result = $conn->query($sql);

      if ($result->num_rows > 0)
      {
        echo
        "<table border ='1'>
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
      }
      else
      {
        echo "0 results";
      }
      $conn->close();
    ?>
    <form action = 'current_values_region.php' name = 'select' method = 'post'/>
        <p>Select Region:</p>
        <?php
            $monitor_list = file_get_contents('/home/legal-server/python_code/monitor_list.json');
            $region_array = json_decode($monitor_list, true);
            $array = $region_array["Regions"];

            $x = count($array);

            echo("<select name = 'region'>");
            for ($i = 0; $i < $x; $i++)
            {
              $region_val = $array[$i]["Name"];
              echo("<option value = '$region_val'>$region_val</option>");
            }
            echo('</select>');
        ?>
        <input class = 'button' type = 'submit' value = 'Change Region'/><br><br>
    </form>
  </body>
</html>
