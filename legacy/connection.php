<?php

$admin= mysqli_connect("localhost","root","","register");
if(mysqli_connect_error())
{
    echo"Cannot Connect";
}

$servername= "localhost";
$username= "root";
$password= "";
$dbname= "register";

$conn = mysqli_connect($servername,$username,$password,$dbname);

if($conn){
      //  echo "Connection OK";
}
else{
    echo "Failed" .mysqli_connect_error();
}

?>
