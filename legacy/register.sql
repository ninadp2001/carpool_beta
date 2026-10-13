-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 03, 2022 at 08:44 AM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.1.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `register`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin_login`
--

CREATE TABLE `admin_login` (
  `Admin_Name` varchar(50) NOT NULL,
  `Admin_Password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin_login`
--

INSERT INTO `admin_login` (`Admin_Name`, `Admin_Password`) VALUES
('admin', 'change-me');

-- --------------------------------------------------------

--
-- Table structure for table `car`
--

CREATE TABLE `car` (
  `brand` varchar(50) CHARACTER SET latin1 DEFAULT NULL,
  `seater` varchar(10) DEFAULT NULL,
  `rate` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `car`
--

INSERT INTO `car` (`brand`, `seater`, `rate`) VALUES
('MARUTI WAGONR', '4 Seater', '8 km'),
('TATA TIAGO', '4 Seater', '8 km'),
('MARUTI SWIFT DZIRE', '5 Seater', '10 rs/km'),
('HYUNDI VERNA', '5 Seater', '10 rs/km'),
('MARUTI ERTIGA', '7 Seater', '13 rs/km'),
('INNOVA CRYSTA', '7 Seater', '13 rs/km'),
('TATA WINGER', '13 Seater', '18 rs/km'),
('TEMPO TRAVELLER', '17 Seater', '22 rs/km');

-- --------------------------------------------------------

--
-- Table structure for table `rentalbooking`
--

CREATE TABLE `rentalbooking` (
  `username` varchar(50) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `cartype` varchar(50) CHARACTER SET latin1 DEFAULT NULL,
  `km` int(255) DEFAULT NULL,
  `amount` int(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `rentalbooking`
--


-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(30) NOT NULL,
  `fname` text NOT NULL,
  `lname` text NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `fname`, `lname`, `username`, `email`, `password`) VALUES
(1, 'Demo', 'User', 'Demo@001', 'demo@example.com', 'Demo@12345');

-- --------------------------------------------------------

--
-- Table structure for table `washbooking`
--

CREATE TABLE `washbooking` (
  `username` varchar(50) NOT NULL,
  `type` varchar(120) DEFAULT NULL,
  `center` varchar(11) DEFAULT NULL,
  `name` varchar(150) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `time` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `washbooking`
--


-- --------------------------------------------------------

--
-- Table structure for table `washcenters`
--

CREATE TABLE `washcenters` (
  `id` int(11) NOT NULL,
  `washingPointName` varchar(255) DEFAULT NULL,
  `washingPointAddress` varchar(255) DEFAULT NULL,
  `location` varchar(100) NOT NULL,
  `contactNumber` bigint(20) DEFAULT NULL,
  `creationDate` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `washcenters`
--

INSERT INTO `washcenters` (`id`, `washingPointName`, `washingPointAddress`, `location`, `contactNumber`, `creationDate`) VALUES
(1, 'Splash & Dash', '402 Blue Empress Appartments, \r\nBorsapada Raod, Kandivali West,\r\nOpposite Poisar Gymkhana,\r\nMumbai - 400067, ', 'Kandivali West', 7947411184, '2022-01-21 14:01:14'),
(2, 'PAAJIAUTO', 'Evershine Nagar,\r\nNew Link Road,Malad West,\r\nNear Movie Time Cinema,\r\nMumbai - 400064', 'Malad West', 7949315450, '2022-01-21 14:02:38'),
(3, 'Extreme Car Care\r\n', 'Shop No 01, Vanai Niwas,\r\nSector 02, Ghansoli, \r\nNear Ghansoli Station,\r\nNavi Mumbai - 400701', 'Ghansoli', 7947288767, '2022-01-21 14:03:16'),
(4, '360 Moto Care', 'Shop No B-15 and Shop No A-16,\r\nShah Arcade, Plot No 4 and 5,\r\nSector No 6, Kharghar,\r\nNear Global IT Park (Map),\r\nNavi Mumbai - 410210', 'Kharghar', 7947179719, '2022-01-21 14:03:51'),
(5, 'Auto Launder\r\n', 'Ground Floor No 1 Plot 105B,\r\nDulabi Kasam Chawl S L Matkar Rd,\r\nNear Parel S T Depot\r\nPrabhadevi, Mumbai - 400025', 'Prabhadevi', 7947197114, '2022-01-21 14:04:54'),
(6, 'Baba Auto Garage', 'LBS Road, Patan Wada Compaund,\r\nLBS Marg, Ghatkopar West,\r\nOpposite Brand Factory\r\nMumbai - 400084', 'Ghatkopar West', 7947186715, '2022-01-21 14:05:25'),
(7, 'Zebro Auto Care', 'Plot No 7, Laxmi Narayan Shopping Complex,\r\nSion Trombay Road, Adjacent to Yes Bank,\r\nChembur East, Mumbai - 400071,', 'Chembur East', 7947168789, '2022-01-21 14:06:12'),
(8, 'Vks Auto Shine\r\n', 'Next to Tata Moters,\r\nEastern Express Highway,\r\nNitin Company Thane West, \r\nThane - 400602', 'Thane West', 8045783832, '2022-01-21 14:06:41'),
(9, '3c Crystal Clear Car', 'Zojawala Petroleum,\r\nL B S Marg, Mulund West,\r\nOpposite Santoshi Mata Temple\r\nMumbai - 400080', 'Mulund West', 7947371337, '2022-01-21 14:07:13'),
(10, 'Star Auto Care Repair and Service', '4th Pasta Lane, Colaba, \r\nColaba Market Post Office,\r\nMumbai - 400005', 'Colaba', 9920069887, '2022-01-21 14:07:43');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `washcenters`
--
ALTER TABLE `washcenters`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `washcenters`
--
ALTER TABLE `washcenters`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
