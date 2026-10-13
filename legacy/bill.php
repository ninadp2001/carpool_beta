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
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Invoice</title>
    <script>
    function print(pdf) {
        // Create an IFrame.
        var iframe = document.createElement('iframe');  
        // Hide the IFrame.  
        iframe.style.visibility = "hidden"; 
        // Define the source.  
        iframe.src = pdf;        
        // Add the IFrame to the web page.
        document.body.appendChild(iframe);  
        iframe.contentWindow.focus();       
        iframe.contentWindow.print(); // Print.
    }
    </script>
    <style>
        body{
            background-color: #F6F6F6; 
            margin-top: 3%;
            padding: 0;
        }
        h1,h2,h3,h4,h5,h6{
            margin: 0;
            padding: 0;
        }
        p{
            margin: 0;
            padding: 0;
        }
        .container{
            width: 80%;
            margin-right: auto;
            margin-left: auto;
        }
        .brand-section{
           background-color: #0d1033;
           padding: 10px 40px;
        }
        .logo{
            width: 50%;
        }

        .row{
            display: flex;
            flex-wrap: wrap;
        }
        .col-6{
            width: 50%;
            flex: 0 0 auto;
        }
        .text-white{
            color: #fff;
        }
        .company-details{
            float: right;
            text-align: right;
            padding: 15px
        }
        .body-section{
            padding: 16px;
            text-align: center;
            border: 1px solid gray;
        }
        .heading{
            font-size: 20px;
            margin-bottom: 08px;
        }
        .sub-heading{
            color: #262626;
            margin-bottom: 05px;
        }
        table{
            background-color: #fff;
            width: 100%;
            border-collapse: collapse;
        }
        table thead tr{
            border: 1px solid #111;
            background-color: #f2f2f2;
        }
        table td {
            vertical-align: middle !important;
            text-align: center;
        }
        table th, table td {
            padding-top: 08px;
            padding-bottom: 08px;
        }
        .table-bordered{
            box-shadow: 0px 0px 5px 0.5px gray;
        }
        .table-bordered td, .table-bordered th {
            border: 1px solid #dee2e6;
        }
        .text-right{
            text-align: end;
        }
        .w-20{
            width: 20%;
        }
        .float-right{
            float: right;
        }
    </style>
</head>
<body>

    <div class="container">
        <div class="brand-section">
            <div class="row">
                <div class="col-6">
                    <img src="img/logo1.png"width="100" height="60">
                </div>
                <div class="col-6">
                    <div class="company-details">
                        <h1 class="text-white">CARPOOL</h1>
                    </div>
                </div>
            </div>
        </div>
        <?php
        $query =sprintf("SELECT * FROM users where username='%s'",$_SESSION['UserID']);
        $data = mysqli_query($conn, $query);
        $total = mysqli_num_rows($data);

        if($total != 0)
        {
            while($result= mysqli_fetch_assoc($data))
                {
        ?>
        <div class="body-section">
            <div class="row">
                <div class="col-6">
                    <h2 class="heading">Invoice No.: 001</h2>
                </div>
                <div class="col-6">
                    <p class="sub-heading">Name:&nbsp;&nbsp; <?php echo $result['fname'];?> </p>
                    <p class="sub-heading">Username:&nbsp;&nbsp; <?php echo $result['username'];?>  </p>
                    <p class="sub-heading">Email ID:&nbsp;&nbsp; <?php echo $result['email'];?>  </p>
                </div>
            </div>
        </div>
<?php
    }
    }
?>
        <div class="body-section">
            <h3 class="heading">Summary</h3>
            <br>
            <table class="table-bordered">
                <thead>
                    <tr>
                        <th>Customer Name</th>
                        <th class="w-25">Rate Per Kilometer</th>
                        <th class="w-25">Kilometers</th>
                        <th class="w-25">Amount</th>
                    </tr>
                </thead>

                <?php
                // $q ="SELECT * FROM rentalbooking ORDER BY id DESC ";
                $q =sprintf("SELECT * FROM rentalbooking where username='%s'",$_SESSION['UserID']);
                $d = mysqli_query($conn, $q);

                if(mysqli_num_rows($d) > 0)
                {
                    foreach($d as $r)
                    {
                ?>

                <tbody>
                    <tr>
                        <td><?php echo $r['name'];?></td>
                        <td><?php echo $r['rate'];?></td>
                        <td><?php echo $r['km'];?></td>
                        <td><?php echo $r['amount1'];?></td>
                    </tr>
                    <tr>
                        <td colspan="3" class="text-right">Tax Total&nbsp;&nbsp;</td>
                        <td>12% SGST<br> 12% CGST</td>
                    </tr>
                    <tr>
                        <td colspan="3" class="text-right">Grand Total&nbsp;&nbsp;</td>
                        <td><?php echo $r['billamount'];?></td>
                    
                    <?php
                        }
                    }
                    ?>
                    </tr>
                </tbody>
            </table>
            <br>
            <h3 class="heading">Payment Status: Paid</h3>
            <h3 class="heading">Payment Mode: Online </h3>
        </div>

        <div class="body-section">
            <p>&copy; Copyright 2021 - Carpool. All rights reserved. 
                
            </p>
        </div>      
    </div>      
<div align="center">
    <button onclick="print('http\://localhost:8081/main/bill.php')">Print PDF</button>
    <button><a href="rhome.php">HOME</button>
</div>
</body>
</html>