<?php
require ('connection.php');

if (isset($_POST['submit']))
{
	// print_r($_POST); die;
	$fname       = $_POST['fname'];
	$lname       = $_POST['lname'];
	$username    = $_POST['username'];
	$email       = $_POST['email'];
	$password    = $_POST['password'];
	$conpassword = $_POST['conpassword'];

	$query = "INSERT INTO `users` (`fname`,`lname`,`username`,`email`, `password`) VALUES ('$fname','$lname','$username','$email', '$password')";
	$data = mysqli_query($conn,$query);
	
	if($data==1) 
		{
			header('location:login.php');
		}
		else
		{
			echo" <script> alert('FAILED'); </script>";
		}
}
			
?>