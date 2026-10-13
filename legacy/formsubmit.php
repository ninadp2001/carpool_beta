<?php

include ("connection.php"); 
session_start();
    if(!isset($_SESSION['UserID']))
    {
        header('location:login.php');
    }

    if(isset($_POST['submit']))
    {
        $username   =$_SESSION['UserID'];
        $name       =$_POST['name'];
        $date       =$_POST['date'];   
        $cartype    =$_POST['rate'];
        $rate       =$_POST['car'];
        $km         =$_POST['km'];
        $amount     =$_POST['amount1'];
        $billamount  =$_POST['amount2'];


        $q="INSERT INTO `rentalbooking` (`username`,`name`,`date`,`rate`,`km`,`amount1`,`billamount`) VALUES ('$username','$name','$date','$rate','$km', '$amount','$billamount')";
        $d = mysqli_query($conn,$q);

        
        if(isset($d) && $d==1) 
        {
            header('location:payment.php');
            session_start();
            $_SESSION['bill']=$billamount;
            
        }
        else 
        {
            echo "<script>alert('Try Again Later.');</script>";

        }

    }

?>
