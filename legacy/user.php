<?php include ("connection.php");

session_start();
    if(!isset($_SESSION['UserID']))
    {
        header('location:login.php');
    }
?>

<html>
    <head>
        <title> Car Pool </title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.10.0/css/all.min.css" rel="stylesheet">
        <link rel="stylesheet" href="css/user.css">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Crete+Round&display=swap" rel="stylesheet">
    </head>
    <body>
        

<!-------- NAV BAR -------->
        <header><a href="home.php" class="logo"><img src="img/logo1.png" alt=""></a>
            <ul class="navbar">
                <li><a href="#home">HOME</a>
                <li><a href="#wb">WASHING BOOKING</a>
                <li><a href="#rb">RENTAL BOOKING</a>
            </ul>

            <div class="header-btn">
            
            <a href="home.php" class="login">HOME</a>
            </div>

        </header>

<!-------- WASHING -------->

<section class="wb" id="wb">

<?php

$query =sprintf("SELECT * FROM washbooking where username='%s'",$_SESSION['UserID']);
$data = mysqli_query($conn, $query);
$total = mysqli_num_rows($data);

if($total != 0)
{
?>



<h2>CAR WASH BOOKING DETAILS </h2>

    <table class="table">
        <tr class="title">
        <th>Type of Wash</th>
        <th>Washing Center</th>
        <th>Name of Customer</th>
        <th>Date of Appointment</th>
        <th>Time of Appointment</th>
        </tr>
        <?php
            while($result= mysqli_fetch_assoc($data))
                {
                    echo " <tr>
                            <td>".$result['type']."</td>
                            <td>".$result['center']."</td>
                            <td>".$result['name']."</td>
                            <td>".$result['date']."</td>
                            <td>".$result['time']."</td>
                            </tr>";
                }

            }
            else
                {
                    echo "<h2> No Records Found </h2>";
                }
        ?>
    </table>
</section>


<!-------- RENTAL -------->

<section class="rb" id="rb">

<?php

$rent =sprintf("SELECT * FROM rentalbooking where username='%s'",$_SESSION['UserID']);
$data1 = mysqli_query($conn, $rent);
$total1 = mysqli_num_rows($data1);

if($total1 != 0)
{
?>



<h2>CAR RENTAL BOOKING DETAILS </h2>

    <table class="table">
        <tr class="title">
        <th>Name of Customer</th>
        <th>Rate Per Kilometers</th>
        <th>Kilometers</th>
        <th>Date of Travel</th>
        <th>Amount</th>
        </tr>
    <?php
        while($result= mysqli_fetch_assoc($data1))
            {
                echo " <tr>
                        <td>".$result['name']."</td>
                        <td>".$result['rate']."</td>
                        <td>".$result['km']."</td>
                        <td>".$result['date']."</td>
                        <td>".$result['billamount']."</td>
                        </tr>";
            }

        }
        else
            {
                "<h2> No Records Found </h2>";
            }
    ?>
</table>





</body>
</html>