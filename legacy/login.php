<?php require("connection.php"); ?>


<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Login and Registration Page</title>
	<link rel="stylesheet" href="css/login.css">
	<link href="https://fonts.googleapis.com/css2?family=Crete+Round&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://pro.fontawesome.com/releases/v5.10.0/css/all.css" integrity="sha384-AYmEC3Yw5cVb3ZcuHtOA93w35dYTsvhLPVnYs9eStHfGJvOvKxVfELGroGkvsg+p" crossorigin="anonymous"/>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-	awesome.min.css">
</head>
<body>

<div class="container">
	<div class="form-container">
		<div class="button-box">
			<div id="btn"></div>
				<button type="button" class="toggle-btn" onclick="login()">LOGIN</button>
		</div>
		<div class="social-icons">
			<a href="https://www.facebook.com/"><img src="img/fb.png"></a>
			<a href="https://twitter.com/"><img src="img/tw.png"></a>
			<a href="https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn&flowEntry=ServiceLogin"><img src="img/gp.png"></a>
		</div>

		<form action="" method="POST" id="login" class="input-group" autocomplete="off">
			<div class="input-name">
				<i class="fa fa-envelope email" ></i>
				<input type="text" class="text-name" placeholder="Username" name="username1">
			</div>

			<div class="input-name">
				<i class="fa fa-lock email " ></i>
				<input type="password" class="text-name" placeholder="Password" name="lpass">
			</div>

			<button type="submit" class="login-btn" name="login"><b>LOGIN</b></button>

		</form>

		
		<h5 class="reg"> New Registration <a href="register.php" >Click Here</a></h5>


		<a href="home.php"><button type="button" class="home-btn"><i class="fa fa-step-backward lock"></i>BACK</button></a>
</body>
</html>

	<?php		

if(isset($_POST['login']))
{
    $q= "SELECT * FROM `users` WHERE `username`='$_POST[username1]' AND `password`='$_POST[lpass]' ";
    $result= mysqli_query($conn,$q);
    
	if(mysqli_num_rows($result)==1)
    {
        session_start();
        $_SESSION['UserID']=$_POST['username1'];
        header("location:home.php");
    }  
	else
	{
    echo" <script> alert('Invalid Credentials'); </script>";
	}

}
?>
