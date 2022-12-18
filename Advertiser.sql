-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 18, 2022 at 12:32 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `advertiser`
--

-- --------------------------------------------------------

--
-- Table structure for table `advertise`
--

CREATE TABLE `advertiser_admins` (
  `Id` int(11) NOT NULL,
  `User_Id` bigint(11) NOT NULL,
  `User_Name` text NOT NULL,
  `User_First_Name` text NOT NULL,
  `User_Last_Name` text NOT NULL,
  `User_Full_Name` text NOT NULL,
  `Active` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `advertiser_admins` (`Id`,`User_Id`,`User_Name`,`User_First_Name`,`User_Last_Name`,`User_Full_Name`,`Active`) VALUES
(1, 2057086971,'Modern_Istanbul','Modern','Istanbul','Modern Istanbul',1);


CREATE TABLE `advertise` (
  `Id` int(11) NOT NULL,
  `Advertise_Id` bigint(11) NOT NULL,
  `Start_Time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Advertise_Count` int(11) NOT NULL DEFAULT 0,
  `Advertise_Period` int(11) NOT NULL DEFAULT 24,
  `User_Id` bigint(11) NOT NULL,
  `User_Name` text NOT NULL,
  `User_First_Name` text NOT NULL,
  `User_Last_Name` text NOT NULL,
  `User_Full_Name` text NOT NULL,
  `Active` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `advertise`
--

INSERT INTO `advertise` (`Id`, `Advertise_Id`, `Start_Time`, `Advertise_Count`, `User_Id`, `User_Name`, `Advertise_Period`,`User_First_Name`,`User_Last_Name`,`User_Full_Name`,`Active`) VALUES
(1, 653, '2022-12-17 23:01:41', 0, 2057086971, 'Modern_Istanbul', 1, 'Modern','Istanbul','Modern Istanbul',0);

-- --------------------------------------------------------

--
-- Table structure for table `advertise_group`
--

CREATE TABLE `advertise_group` (
  `Id` int(11) NOT NULL,
  `Advertise_Id` bigint(11) NOT NULL,
  `Group_Id` bigint(11) NOT NULL,
  `Group_Name` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `advertise_runs`
--

CREATE TABLE `advertise_runs` (
  `Id` int(11) NOT NULL,
  `Advertise_Id` bigint(11) NOT NULL,
  `Advertise_Remain` bigint(11) NOT NULL,
  `Advertise_NextRun` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Group_Id` bigint(11) NOT NULL,
  `Group_Name` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bot_groups`
--

CREATE TABLE `bot_groups` (
  `Id` int(11) NOT NULL,
  `Group_Id` bigint(11) NOT NULL,
  `Group_Name` text NOT NULL,
  `Advertise_Group` int(11) DEFAULT 0,
  `Active` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `bot_groups`
--

INSERT INTO `bot_groups` (`Id`, `Group_Id`, `Group_Name`, `Advertise_Group`, `Active`) VALUES
(1, -880377162, 'Advertise_Group', 1, 1),
(2, -2147483648, 'تبلیغات Modern Istanbul', 0, 1),
(3, -2147483648, 'چارشی | بی واسطه بخرید و بفروشید', 0, 1),
(4, -2147483648, 'ARSES HOLDİNG İSTANBUL', 0, 1),
(5, -2147483648, 'نیازمندیهای استانبول(همیاری)', 0, 1),
(6, -2147483648, 'تبلیغات گسترده کشوری', 0, 1),
(7, -2147483648, 'همراهان استانبول❤️', 0, 1);

--
-- Indexes for dumped tables
--

ALTER TABLE `advertiser_admins`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `advertise`
--
ALTER TABLE `advertise`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `advertise_group`
--
ALTER TABLE `advertise_group`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `advertise_runs`
--
ALTER TABLE `advertise_runs`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `bot_groups`
--
ALTER TABLE `bot_groups`
  ADD PRIMARY KEY (`Id`);

--
-- AUTO_INCREMENT for dumped tables
--
ALTER TABLE `advertiser_admins`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- AUTO_INCREMENT for table `advertise`
--
ALTER TABLE `advertise`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `advertise_group`
--
ALTER TABLE `advertise_group`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- AUTO_INCREMENT for table `advertise_runs`
--
ALTER TABLE `advertise_runs`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- AUTO_INCREMENT for table `bot_groups`
--
ALTER TABLE `bot_groups`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
