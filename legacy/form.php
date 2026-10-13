<?php 
include ("connection.php"); 
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
        <title>Rental Form</title>
        <meta content="width=device-width, initial-scale=1.0" name="viewport">
        <link href="css/form.css" rel="stylesheet">
        <link rel="stylesheet" href="https://pro.fontawesome.com/releases/v5.10.0/css/all.css" integrity="sha384-AYmEC3Yw5cVb3ZcuHtOA93w35dYTsvhLPVnYs9eStHfGJvOvKxVfELGroGkvsg+p" crossorigin="anonymous"/>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
        
        <script>
            $(document).ready(function(){
                $('select').on('change', function (e) {
                    var km=$("#my_sel").val()
                    console.log(km)
                    $("#ip_4").text(km)

                });

                $("#ip_5").keyup(function(){
                    var km=$("#my_sel").val()
                    km=(km.split(" "))[0]
                    
                    let x=$("#ip_5").val()
                    let final=parseInt(km)*parseInt(x)
                    // console.log(final)
                    let gst=(parseInt(final)*(24/100)).toFixed(2)
                    // console.log(gst)
                    let final2=parseInt(final)+parseInt(gst)
                    console.log(final2)

                    if (isNaN(final) && isNaN(final2)) {
                        $("#ip_6").text("")
                        $("#ip_7").text("")
                    }
                    else {
                        $("#ip_6").text(final)
                        $("#ip_6_hiden").val(final)
                        $("#ip_7").text(final2)
                        $("#ip_7_hiden").val(final2)
                    
                      
                    }
                    
                });
            });
        </script>

    </head>
    <body>
    <div class="banner">

        <div class="form">
            <div class="title">
                <h4><u>BOOKING DETAILS</u></h4>
            </div>

            <form action="formsubmit.php" method="POST" autocomplete="off">
                <div class="content">
                    <label>Full Name :</label>
                    <input type="text" name="name" required class="content-control"  placeholder="ENTER FULL NAME"><br>
                    </div>

                    <div class="content">
                    <label>Booking Date :</label>
                    <input type="date" name="date" required class="content-control" >
                    </div>

                    <div class="content">
                    <label>Select Car :</label>
                        <select id="my_sel" name="car" required class="content-control">
                        <option name="0" value="0">Car type</option>
                    
                        <?php
                        $query =sprintf("SELECT * FROM car");
                        $data = mysqli_query($conn, $query);
                        $total = mysqli_num_rows($data);

                        if($total != 0)
                        {
                            while($result= mysqli_fetch_assoc($data)){
                        ?>
                       <option value="<?php echo $result['rate'];?>">
                            <?php echo $result['brand'];?>
                            (<?php echo $result['seater'];?>)
                            
                    
                        </option>
                        <?php }  }   ?>
                        </select>
                </div>  

                <div class="content">
                    <label>Rate per km :</label>
                    <label id="ip_4" name="rate" class="content-control" ></label><br>

                </div>  
                        
                <div class="content">
                    <label>Enter Kilometer :</label>
                    <input id="ip_5" type="number" name="km" required class="content-control"  placeholder="KM to be driven"><br>
                    </div>

                <div class="content">
                    <label>Amount (in rupees):</label>  
                    <label id="ip_6"  class="content-control">
                    </label><br>
                </div>
                
                <div class="content" style='display:none'>
                    <label>Amount (in rupees):</label>  
                    <input id="ip_6_hiden" type="hidden" name="amount1" required class="content-control"  placeholder="KM to be driven"><br>
                    </label><br>
                </div>

                <div class="content">
                    <label>Total Amount (including taxes):</label>  
                    <label id="ip_7"  class="content-control">
                    </label><br>
                </div>
                
                <div class="content" style='display:none'>
                    <label>Total Amount :</label>  
                    <input id="ip_7_hiden" type="hidden" name="amount2" required class="content-control"  placeholder="KM to be driven"><br>
                    </label><br>
                </div>
                

                <div class="content" align="center">
                    <input type="submit" value="SUBMIT"  name="submit" class="btn">
                </div>

       
                <div class="close">
                <a href="rhome.php"><input value="CLOSE" class="btn"></a>
                </div>

                </form>
        </div>
    </body>
</html>

