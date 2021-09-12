<!DOCTYPE html>
<html class = 'a'>
  <head>
    <title>Search Engine</title>
    <div>
      <h1 class = 'a'>Sunshine Coast Air Quality</h1>
      <input type = 'button' class = 'option' value = 'Home' onclick = "window.location.href = '/index.php'">
      <input type = 'button' class = 'option' value = 'Current Values' onclick = "window.location.href = '/ajax_current.php'">
      <input type = 'button' class = 'option' value = 'Search Engine' onclick = "window.location.href = '/Individual_Search.php'">
    </div>
    <style>
      @import url('global.css');
    </style>
  </head>
  <body>
    </div>
    <form action = 'conn-table-individual.php' name = 'select1' method = 'post'/><br><br>
      <p>Enter ID of Sensor:</p>
      <input type = 'text' name = 'id_box' value = '1086'/>

      <p>Time Frame</P>
      <select name = 'time_drop' id = 'time_drop'>
        <option value = 'hour'>Hourly Data</option>
        <option value = 'day'>Daily Data</option>
      </select>

      <p>Select one option:</p>
      <select id = 'ascdesc' name = 'ascdesc'>
        <option value = 'DESC'>Descending Order</option>
        <option value = 'ASC'>Ascending Order</option>
      </select>

      <p>How many rows would you like to view?</p>
      <input type = 'text' name = 'limit'/><br><br>

      <input class = 'button' type = 'submit' value = 'Next Page'/>
    </form>
  </body>
</html>
