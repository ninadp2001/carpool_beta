<?php require("connection.php"); ?>


<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Login and Registration Page</title>
	<link rel="stylesheet" href="css/register.css">
	<link href="https://fonts.googleapis.com/css2?family=Crete+Round&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://pro.fontawesome.com/releases/v5.10.0/css/all.css" integrity="sha384-AYmEC3Yw5cVb3ZcuHtOA93w35dYTsvhLPVnYs9eStHfGJvOvKxVfELGroGkvsg+p" crossorigin="anonymous"/>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-	awesome.min.css">
</head>
<body>

<div class="container">
	<div class="form-container">
		<div class="button-box">
			<div id="btn"></div>
				<button type="button" class="toggle-btn" onclick="register()">REGISTER</button>
		</div>
		<div class="social-icons">
			<a href="https://www.facebook.com/"><img src="img/fb.png"></a>
			<a href="https://twitter.com/"><img src="img/tw.png"></a>
			<a href="https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn&flowEntry=ServiceLogin"><img src="img/gp.png"></a>
		</div>

		<form action="registersubmit.php" method="POST" id="register" class="reggroup" autocomplete="off" onsubmit="return validation()">
			
			<div class="grp">
				<div class="regname">
					<i class="fa fa-user lock" ></i>
					<input type="text" placeholder="First Name" class="text-name" name="fname" id="fname" value="">
					<br><strong id="error" class="error"> </strong>
				</div>

				<div class="regname">
					<i class="fa fa-user lock" ></i>
					<input type="text" placeholder="Last Name" class="text-name" name="lname" id="lname" value="">
					<br><strong id="error2" class="error"> </strong>
				</div>
			</div>

			<div class="regname">
				<i class="fa fa-user email"></i>
				<input type="text" placeholder="Username" class="text-name" name="username" id="username" value="">
				<br><strong id="error3" class="error"> </strong>
			</div>

			<div class="regname">
				<i class="fa fa-envelope email" ></i>
				<input type="text" placeholder="Email ID" class="text-name" name="email" id="email" value="">
				<br><strong id="error4" class="error"> </strong>
			</div>

			<div class="regname">
				<i class="fa fa-lock email " ></i>
				<input type="password" placeholder="Password" class="text-name" name="password" id="password" value="">
				<br><strong id="error5" class="error"> </strong>
			</div>

			<div class="regname">
				<i class="fa fa-lock email" ></i>
				<input type="password" placeholder="Confirm Password" class="text-name" name="conpassword" id="conpassword" value="">
				<br><strong id="error6" class="error"> </strong>
			</div>

			<button type="submit" class="login-btn" name="submit"><b>REGISTER</b></button>

		</form>

		<a href="home.php"><button type="button" class="home-btn"><i class="fa fa-step-backward lock"></i>BACK</button></a>
	
	</div>
</div>

<script>

function validation()
    {
	    var a = document.getElementById('fname').value;
		var b = document.getElementById('lname').value;
		var c = document.getElementById('username').value;
		var d = document.getElementById('email').value;
		var e = document.getElementById('password').value;
        var f = document.getElementById('conpassword').value;
		
        /* First Name Validation */
        if(a == ""){
			document.getElementById('error').innerHTML= "**Please Enter a Valid Name.";
            return false;
		}
        if(a.length<3){
            document.getElementById('error').innerHTML= "**Name Must be more than 3 charater.";
            return false;
        }
		if(!isNaN(a)){
            document.getElementById('error').innerHTML= "**Name Must have only Alphabets.";
            return false;
        }
		else{
			document.getElementById('error').innerHTML= "";
		}
        
		/* Last Name Validation */
        if(b == ""){
			document.getElementById('error2').innerHTML= "**Please Enter a Valid Name.";
            return false;
		}
        if(b.length<3){
            document.getElementById('error2').innerHTML= "**Name Must be more than 3 charater.";
            return false;
        }
		if(!isNaN(b)){
            document.getElementById('error2').innerHTML= "**Name Must have only Alphabets.";
            return false;
        }
		else{
			document.getElementById('error2').innerHTML= "";
		}

		/* Userame Validation */
		if(c == ""){
			document.getElementById('error3').innerHTML= "**Please Enter a Valid Username.";
            return false;
		}
		if(c.length<8){
            document.getElementById('error3').innerHTML= "**Username Should be in Admin@001 form.";
            return false;
        }
		if(c.search(/[a-z]/)==-1){
			document.getElementById('error3').innerHTML= "**Username Should be in Admin@001 form.";
			return false;
		}
		if(c.search(/[A-Z]/)==-1){
			document.getElementById('error3').innerHTML= "**Username Should be in Admin@001 form.";
			return false;
		}
		if(c.search(/[!\@\#\$\%\^\&\*\(\)\_\-\=\+\,\<\.\/\>\?]/)==-1){
			document.getElementById('error3').innerHTML= "**Username Should be in Admin@001 form.";
			return false;
		}
		else{
			document.getElementById('error3').innerHTML= "";
		}

		/* Email Validation */

        if(d == ""){
			document.getElementById('error4').innerHTML= "**Please Enter a Valid Email ID.";
            return false;
		}                
		if(d.indexOf('@')<=0){
            document.getElementById("error4").innerHTML= "**Enter a Valid Email ID.";
            return false;
        }
        if(d.charAt(d.length-4)!='.' && d.charAt(d.length-3)!='.'){
            document.getElementById('error4').innerHTML= "**Enter a Valid Email ID.";
            return false;
        }
        else{
			document.getElementById('error4').innerHTML= "";
		}
		
        /* Password Validation */
        if(e == ""){
			document.getElementById('error5').innerHTML= "**Please Enter Password.";
            return false;
		}
        if(e.length<8){
            document.getElementById('error5').innerHTML= "**Password Must be greater than 8 character.";
            return false;
        }
		if(e.search(/[0-9]/)==-1){
			document.getElementById('error5').innerHTML= "**Password Must have atleast one integer.";
			return false;
		}
		if(e.search(/[a-z]/)==-1){
			document.getElementById('error5').innerHTML= "**Password Must have atleast one lower case chareacter.";
			return false;
		}
		if(e.search(/[A-Z]/)==-1){
			document.getElementById('error5').innerHTML= "**Password Must have atleast one upper case chareacter.";
			return false;
		}
		if(e.search(/[!\@\#\$\%\^\&\*\(\)\_\-\=\+\,\<\.\/\>\?]/)==-1){
			document.getElementById('error5').innerHTML= "**Password Must have a specail chareacter.";
			return false;
		}
		else{
			document.getElementById('error5').innerHTML= "";
		}
        if(e!=f){
            document.getElementById('error6').innerHTML= "**Password Donot Match.";
            return false;
        }
		
    }
</script>

</body>
</html>


