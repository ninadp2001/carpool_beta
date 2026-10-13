<?php include ("connection.php"); 

session_start();
    if(!isset($_SESSION['UserID']))
    {
        header('location:login.php');
    }

?>

<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Booking Form</title>
        <meta content="width=device-width, initial-scale=1.0" name="viewport">
        <link href="css/booking.css" rel="stylesheet">
        <link rel="stylesheet" href="https://pro.fontawesome.com/releases/v5.10.0/css/all.css" integrity="sha384-AYmEC3Yw5cVb3ZcuHtOA93w35dYTsvhLPVnYs9eStHfGJvOvKxVfELGroGkvsg+p" crossorigin="anonymous"/>
        
    </head>
    <body>
    <div class="banner">
        <div class="form">
            <div class="title">
                <h4><u>BOOKING DETAILS</u></h4>
            </div>

            <form action="" method="POST">
                <div class="content">
                    <label>Package Type :</label>
                    <select name="type" required class="content-control" >
                        <option value="Not Selected">SELECT PACKAGE</option>
                        <option value="BASIC CLEANING">BASIC CLEANING (Rs 550)</option>
                        <option value="PREMIUM CLEANING">PREMIUM CLEANING (Rs 750)</option>
                        <option value="COMPLEX CLEANING">COMPLEX CLEANING (Rs 1050)</option>
                    </select> 
                </div>

                <div class="content">
                    <label>Washing Center :</label>
                        <select name="center" required   class="content-control">
                        <option>Select Washing Point</option>

                        <?php
                        $query =sprintf("SELECT * FROM washcenters");
                        $data = mysqli_query($conn, $query);
                        $total = mysqli_num_rows($data);

                        if($total != 0)
                        {
                            while($result= mysqli_fetch_assoc($data)){
                        ?>
                        <option value="<?php echo $result['location'];?>">
                        <?php echo $result['washingPointName'];?>
                        (<?php echo $result['location'];?>)
                    
                        </option>
                        <?php }  }   ?>
                        </select>
                </div>  
                

                <div class="content">
                <label>Full Name :</label>
                <input type="text" name="name" required class="content-control"  placeholder="ENTER FULL NAME"><br>
                </div>
                
                <div class="content">
                    <label>Washing Date :</label>
                    <input type="date" name="date" required class="content-control" >
                </div>    
                        
                <div class="content">
                    <label>Washing Time :</label>
                    <select name="time" required class="content-control" >
                        <option value="Not Selected">SELECT TIME</option>
                        <option value="00:12:00">12 PM</option>
                        <option value="00:14:00">2 PM</option>
                        <option value="00:16:00">4 PM</option>
                        <option value="00:18:00">6 PM</option>
                        <option value="00:20:00">8 PM</option>
                    </select>
                </div>

                <div class="content" align="center">
                <input name="submit" type="submit" value="BOOK NOW" class="btn">
                </div>

                <div class="close">
                <a href="cwhome.php"><input value="CLOSE" class="btn"></a>
                </div>
            </form>


        </div>
    </body>
</html>


<?php
    if(isset($_POST['submit']))
    {
        $username= $_SESSION['UserID'];
        $ptype  =$_POST['type'];
        $wpoint =$_POST['center'];   
        $fname  =$_POST['name'];
        $date   =$_POST['date'];
        $time   =$_POST['time'];


        $q = "INSERT INTO `washbooking` (`username`,`type`,`center`,`name`,`date`, `time`) VALUES ('$username','$ptype','$wpoint','$fname','$date', '$time')";
        $d = mysqli_query($conn,$q);
        
            if($d)
            {
                
                echo '<script>alert("Booking Successful")</script>';
            }
            else
            {
                echo '<script>alert("FAILED")</script>';
            }
    }

 
?>
