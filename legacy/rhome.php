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
        <title>Car Pool</title>
        <link rel="stylesheet" href="css/rhome.css">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Crete+Round&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://pro.fontawesome.com/releases/v5.10.0/css/all.css" integrity="sha384-AYmEC3Yw5cVb3ZcuHtOA93w35dYTsvhLPVnYs9eStHfGJvOvKxVfELGroGkvsg+p" crossorigin="anonymous"/>
    </head>
    <body>

        <header><a href="home.php" class="logo"><img src="img/logo1.png" alt=""></a>
            <ul class="navbar">
                <li><a href="#home">HOME</a>
                <li><a href="#ride">SERVICE</a>
                <li><a href="#services">CARS</a>
                <li><a href="#about">ABOUT</a>
            </ul>
            <div class="header-btn">
            <a href="user.php" class="login"><?php if($_SESSION['UserID']){echo $_SESSION['UserID'];}else{ header("location:login.php");}?></a>
                <a href="logout.php" class="login">Logout</a>
            </div>
        </header>
        <section class="home" id="home">
            <div class="text">
                <h1><span>Looking</span> to <br> rent a car</h1><br>
                <p><ul>
                    <li><i class="far fa-check-circle"></i>Unbeatable Rates</li>
                    <li><i class="far fa-check-circle"></i>Easy & Quick Online Car Booking</li>
                    <li><i class="far fa-check-circle"></i>Clean & Well Maintained Fleet</li>
                </ul></p><br>

                <a href="form.php"><input type="submit" value="RENT NOW" class="btn"></a>

        </div>
            
        </section>

    <!-------- RIDE -------->

    <section class="ride" id="ride">
       
            <div class="heading">
                <h1>How Its Work</h1>
                <hr class="h">
                <h2>Rent With 3 Easy Steps</h2>
            </div>

            <div class="container">
                <div class="box">
                    <i class="fas fa-map-marker-alt"></i>
                    <h2>Choose a Location</h2>
                    <p>It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose.</p>
                </div>

                <div class="box">
                    <i class="far fa-calendar-alt"></i></i>
                    <h2>Pick Up-date</h2>
                    <p>It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose.</p>
                </div>

                <div class="box">
                    <i class="fas fa-calendar-check"></i></i>
                    <h2>Book A Car</h2>
                    <p>It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose.</p>
                </div>
            </div>
        </div>
    </section>
<!-------- CARS -------->

            <section class="services" id="services">

                
                <div class="heading">
                    <h1>How Its Work</h1>
                    <hr class="h">
                    <h2> Explore Out Top Deals <br> From Top Rated Deals</h2>
                </div>

                <div class="services-container">
                    <div class="box">
                        <div class="box-img">
                            <img src="img/wagonr.jpg" alt="">
                        </div>
                        <p>4 Seater</p>
                        <h3>MARUTI WAGONR</h3>
                        <h2>Rs. 8 <span>per km</span></h2>
                        <a href="form.php" class="btn">RENT NOW</a>
                    </div>
                
                    <div class="box">
                        <div class="box-img">
                        <img src="img/tiago.jpeg" alt="">
                        </div>
                        <p>4 Seater</p>
                        <h3>TATA TIAGO</h3>
                        <h2>Rs. 8 <span>per km</span></h2>
                        <a href="form.php" class="btn">RENT NOW</a>
                    </div>

                    <div class="box">
                        <div class="box-img">
                        <img src="img/dzire.jpg" alt="">
                        </div>
                        <p>5 Seater</p>
                        <h3>MARUTI SWIFT DZIRE</h3>
                        <h2>Rs. 10 <span>per km</span></h2>
                        <a href="form.php" class="btn">RENT NOW</a>
                    </div>

                    <div class="box">
                        <div class="box-img">
                        <img src="img/verna.jpg" alt="">
                        </div>
                        <p>5 Seater</p>
                        <h3>HYUNDI VERNA</h3>
                        <h2>Rs. 10 <span>per km</span></h2>
                        <a href="form.php" class="btn">RENT NOW</a>
                    </div>

                    <div class="box">
                        <div class="box-img">
                        <img src="img/ertiga.jpg" alt="">
                        </div>
                        <p>7 Seater</p>
                        <h3>MARUTI ERTIGA</h3>
                        <h2>Rs. 13 <span>per km</span></h2>
                        <a href="form.php" class="btn">RENT NOW</a>
                    </div>

                    <div class="box">
                        <div class="box-img">
                        <img src="img/innova.jpg" alt="">
                        </div>
                        <p>7 Seater</p>
                        <h3>INNOVA CRYSTA</h3>
                        <h2>Rs. 13 <span>per km</span></h2>
                        <a href="form.php" class="btn">RENT NOW</a>
                    </div>

                    <div class="box">
                        <div class="box-img">
                        <img src="img/winger.jpg" alt="">
                        </div>
                        <p>13 Seater</p>
                        <h3>TATA WINGER</h3>
                        <h2>Rs. 18 <span>per km</span></h2>
                        <a href="form.php" class="btn">RENT NOW</a>
                    </div>

                    <div class="box">
                        <div class="box-img">
                        <img src="img/traveller.jpg" alt="">
                        </div>
                        <p>17 Seater</p>
                        <h3>TEMPO TRAVELLER</h3>
                        <h2>Rs. 22 <span>per km</span></h2>
                        <a href="form.php" class="btn">RENT NOW</a>
                    </div>
                
                </div>

            </section>
          
<!-------- ABOUT -------->




    </body>
</html>