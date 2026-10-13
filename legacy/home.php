<?php

session_start();

?>

<html>
    <head>
        <title> Car Pool </title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="css/home.css">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Crete+Round&display=swap" rel="stylesheet">
       
    </head>
    <body>

    <!-------- NAV BAR -------->
    <header><a href="home.php" class="logo"><img src="img/logo1.png" alt=""></a>
            <ul class="navbar">
                <li><a href="cwhome.php">CAR WASH</a>
                <li><a href="rhome.php">CAR RENTAL</a>
                <li><a href="about.php">ABOUT</a>
            </ul>
            <div class="header-btn">
                <a href="login.php" class="login">Login / Sign Up</a>
            </div>
    </header>


<!-------- HOME -------->

        
        <div class="banner">
                <div class="content" >
                    <h2> CAR SERVICE FOR YOUR CAR</h2><br>
                    <h3> KEEPING YOUR CAR CLEAN IS A SYMBOL OF LOVING IT</h3>
                    <div>
                    <a href="cwhome.php"><button type="button">CAR WASH</button></a>
                    <a href="rhome.php"><button type="button">CAR RENTAL</button></a>
                    </div>

                </div>
        </div>

        </body>
</html>