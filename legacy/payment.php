<?php
include("connection.php");

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
        <title>Payment Gateway</title>
        <meta content="width=device-width, initial-scale=1.0" name="viewport">
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.2/css/all.css">
        <link rel="stylesheet" href="css/gateway.css">
    </head>
    <body>

            <div class="payment">

                <div class="payment-logo">
                    <img src="img/logo1.png" class="logo">
                </div>
    
    
                <h2>Payment Gateway</h2>
                
                <form action="bill.php" method="POST" autocomplete="off" onsubmit="return validation()">

                    <!-- <div class="content">
                        <label class="label">Amount:></label><br>
                    </div> -->

                    <div class="content">
                        <label class="label">Card Holder :</label>
                        <i class="fa fa-user lock" ></i>
                        <input type="text" class="input"  placeholder="Card Holder Name" name="name" id="name">
                        <br><strong id="error" class="error"> </strong>
                    </div>

                    <div class="content">
                        <label class="label">Card Number :</label>
                        <i class="fa fa-credit-card lock" ></i>
                        <input type="text" class="input"  placeholder="0000 0000 0000 0000"  name="cdno" id="cdno">
                        <br><strong id="error2" class="error"> </strong>
                    </div>

                    <div class="grp">

                        <div class="half">
                            <label class="label">Expiry Date :</label>
                            <i class="fa fa-calendar-alt lock" ></i>
                            <input type="text" class="input"  placeholder="00 / 00"  name="expd" id="expd">
                            <br><strong id="error3" class="error"> </strong>
                        </div>

                        <div class="half">
                            <label class="label">CVV :</label>
                            <i class="fa fa-lock lock" ></i>
                            <input type="text" class="input"  placeholder="000"  name="cvv" id="cvv">
                            <br><strong id="error4" class="error"> </strong>
                        </div>

                    </div>
                    

                    <input type="submit" class="btn" name="submit" value="PAY"></input>

                </form>
            </div>

            <script>
          
        function validation()
        {
            var a = document.getElementById('name').value;
            var b = document.getElementById('cdno').value;
            var c = document.getElementById('expd').value;
            var d = document.getElementById('cvv').value;
            
            /* Name Validation */
            if(a == ""){
                document.getElementById('error').innerHTML= "**Please Enter a Valid Name.";
                return false;
            }
            if(!isNaN(a)){
                document.getElementById('error').innerHTML= "**Name Must have only Aplhabet.";
                return false;
            }
            if(a.length<3){
                document.getElementById('error').innerHTML= "**Name Must be more than 3 charater.";
                return false;
            }
            else{
                document.getElementById('error').innerHTML= "";
            }
            
            /* Card Number Validation */
            if(b == ""){
                document.getElementById('error2').innerHTML= "**Please Enter a Valid Card Number.";
                return false;
            }
            if(isNaN(b)){
                document.getElementById('error2').innerHTML= "**Card Number have only Numbers.";
                return false;
            }
            if(b.length>16 || b.length<16) {
                document.getElementById('error2').innerHTML= "**Must Have 16 Digit.";
                return false;
            }
            else{
                document.getElementById('error2').innerHTML= "";
            }         
            
            /* Expiry Date Validation */
            if(c == ""){
                document.getElementById('error3').innerHTML= "**Please Enter Valid Data.";
                return false;
            }
            if(c.length>5){
                document.getElementById('error3').innerHTML= "**Please Enter Valid Data.";
                return false;
            }
            else{
                document.getElementById('error3').innerHTML= "";
            }                
            
            /* CVV Validation */
            if(d == ""){
                document.getElementById('error4').innerHTML= "**Please Enter Valid Data.";
                return false;
            }
            if(isNaN(d)){
                document.getElementById('error4').innerHTML= "**Only Numbers are allowed.";
                return false;
            }
            if(d.length>3){
                document.getElementById('error4').innerHTML= "**Please Enter Valid Data.";
                return false;
            }
            else{
                document.getElementById('error4').innerHTML= "";
            }

        }
    </script>

    </body>
</html>

