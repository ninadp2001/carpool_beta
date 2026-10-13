<?php include ("connection.php");   include ("conn2.php");

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
        <link rel="stylesheet" href="css/car.css">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Crete+Round&display=swap" rel="stylesheet">
    </head>
    <body>
        

<!-------- NAV BAR -------->
        <header><a href="home.php" class="logo"><img src="img/logo1.png" alt=""></a>
            <ul class="navbar">
                <li><a href="#home">HOME</a>
                <li><a href="#plan">WASHING PLAN</a>
                <li><a href="#center">WASHING CENTER</a>
                <li><a href="#about">ABOUT</a>
            </ul>
            <div class="header-btn">
                <a href="user.php" class="login"><?php if($_SESSION['UserID']){echo $_SESSION['UserID'];}?></a>
                <a href="logout.php" class="login">Logout</a>
            </div>
        </header>


 <!-------- HOME -------->

 <section class="home" id="home">

        <div class="banner"> 
            <div class="row">
                <div class="col-1">
                    <h2>MODERN EQUIPMENT</h2>
                    <h3>We love to shine cars <br> Book now to feel the experience.</h3>
                    <a href="booking.php"><button type="button" class="button">BOOK NOW</button></a>
                </div>

                <div class="col-2">
                    <img src="img/car.png" class="car">
                    <div class="color-box"> </div>
                </div>
            </div>

            <div class="bar" >
                <div class="row2">
                    <div class="col"><h1>Impressive Interior</h1> 
                        <p> Internal cleaning and dry system and sucton vaccuming using our speacial car cleaning accessories.</p>
                    </div>

                    <div class="col"><h1> Ready to Shine</h1>
                        <p> External cleaning with wet steam and also high pressure wash using our speacial car cleaning accessories.</p>
                    </div>
                
                    <div class="col"><h1>Disinfection</h1>
                        <p> Sanitizing is a procedure of proper cleaning and removing virus and germ it is also part of anti-bacterial treatment.</p>
                    </div>
                
                    <div class="col"><h1> Detailing Glow</h1>
                        <p> Rubbing is a process that result in the removal of stain and marks on the paint surface of the car and gives your car a smooth and clean look.</p>
                    </div>
                </div>
            </div>

        
        </div>  

</section>
        <!-------- WASHING PLAN -------->

<section class="plan" id="plan">

    <div class="banner">
        <div class="container">
                <div class="text-box">
                    <h1>WASHING PLAN</h1>
                    <h2>Choose Your Plan</h2>
                </div>
               
                <div class="row">

                        <div class="price-body">
                            <h2>Basic Cleaning</h2>
                            <h3>Rs. 550</h3>
                                <ul><div class="uli">
                                    <li><i class="far fa-check-circle"></i>      Seats Washing</li>
                                    <li><i class="far fa-check-circle"></i>      Vacuum Cleaning</li>
                                    <li><i class="far fa-check-circle"></i>      Exterior Cleaning</li>
                                    <li><i class="far fa-times-circle"></i>      Interior Wet Cleaning</li>
                                    <li><i class="far fa-times-circle"></i>      Window Wiping</li>
                                    <li><i class="far fa-times-circle"></i>      Disinfection</li>
                                    <li><i class="far fa-times-circle"></i>      Detailing Glow</li>
                                </div></ul>
                                <div class="book"><h4>
                                    <a  href="booking.php"  class="btn">Book Now</a></h4>
                                </div>
                        </div>

                        <div class="price-body">
                            <h2><span>Premium Cleaning</span></h2>
                            <h3>Rs. 750</h3>
                            <ul><div class="uli">
                                <li><i class="far fa-check-circle"></i>      Seats Washing</li>
                                <li><i class="far fa-check-circle"></i>      Vacuum Cleaning</li>
                                <li><i class="far fa-check-circle"></i>      Exterior Cleaning</li>
                                <li><i class="far fa-check-circle"></i>      Interior Wet Cleaning</li>
                                <li><i class="far fa-check-circle"></i>      Window Wiping</li>
                                <li><i class="far fa-times-circle"></i>      Disinfection</li>
                                <li><i class="far fa-times-circle"></i>      Detailing Glow</li>
                            </div></ul>
                            <div class="book"><h4>
                                    <a  href="booking.php"  class="btn">Book Now</a></h4>
                            </div>
                        </div>                    
                        
                        <div class="price-body">
                            <h2>Complex Cleaning</h2>
                            <h3>Rs. 1050</h3>
                            <ul><div class="uli">
                                <li><i class="far fa-check-circle"></i>      Seats Washing</li>
                                <li><i class="far fa-check-circle"></i>      Vacuum Cleaning</li>
                                <li><i class="far fa-check-circle"></i>      Exterior Cleaning</li>
                                <li><i class="far fa-check-circle"></i>      Interior Wet Cleaning</li>
                                <li><i class="far fa-check-circle"></i>      Window Wiping</li>
                                <li><i class="far fa-check-circle"></i>      Disinfection</li>
                                <li><i class="far fa-check-circle"></i>      Detailing Glow</li>
                            </div></ul>
                            <div class="book"><h4>
                                    <a  href="booking.php"  class="btn">Book Now</a></h4>
                            </div>
                        </div>
                    
                </div>

        </div>
    </div>

</section>


<!-------- WASHING CENTER-------->

<section class="center" id="center"> 

<div class="banner">
       <div class="text">
            <h2>Select the preferred location.</h2>
        </div>

            <div class="row">
                <?php
                    $sql = "SELECT * from washcenters";
                    $query = $conn -> prepare($sql);
                    $query->execute();
                    $results=$query->fetchAll(PDO::FETCH_OBJ);
                    foreach($results as $result)
                    {               
                ?>  
                    <div class="col">
                        <div class="text1">
                
                        <h2><?php echo htmlentities($result->washingPointName);?></h2>
                        <p><?php echo htmlentities($result->washingPointAddress);?><p>
                        <p><span>Call:</span><?php echo htmlentities($result->contactNumber);?></p>
                        </div>
                    
                    </div>
                <?php
                    }
                ?>
            </div>
</div>
</section>


<!-------- ABOUT -------->

<section class="about" id="about"> 
<div class="banner">





</section>




    </body>
</html>