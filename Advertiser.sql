-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 18, 2022 at 11:20 AM
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

INSERT INTO `advertise` (`Id`, `Advertise_Id`, `Start_Time`, `Advertise_Count`, `Advertise_Period`, `User_Id`, `User_Name`, `User_First_Name`, `User_Last_Name`, `User_Full_Name`, `Active`) VALUES
(1, 653, '2022-12-18 03:46:12', 0, 1, 2057086971, 'Modern_Istanbul', 'Modern', 'Istanbul', 'Modern Istanbul', 0);

-- --------------------------------------------------------

--
-- Table structure for table `advertiser_admins`
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

--
-- Dumping data for table `advertiser_admins`
--

INSERT INTO `advertiser_admins` (`Id`, `User_Id`, `User_Name`, `User_First_Name`, `User_Last_Name`, `User_Full_Name`, `Active`) VALUES
(1, 2057086971, 'Modern_Istanbul', 'Modern', 'Istanbul', 'Modern Istanbul', 1);

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
(2, -1001702818002, 'تبلیغات Modern Istanbul', 0, 1),
(3, -1001144942180, 'نیازمندیهای استانبول', 0, 0),
(4, -1001213552027, ' 🇹🇷دیوار شهر استانبول🇹🇷', 0, 0),
(5, -1001297266212, ' نیازمندی ترکیه و ایران (عمومی) 🇹🇷', 0, 0),
(6, -1001300758476, ' نیازمندی ترکیه و ایران (عمومی)🇹🇷', 0, 0),
(7, -1001289840286, ' نیازصنعت ابزار', 0, 0),
(8, -1001149708252, ' تبلیغات استان اصفهان پیربکران فلاورجان مبارکه بهاران ابریشم کلیشاد سودرجان قهدریجان', 0, 0),
(9, -1001516526756, ' تبلیغات گسترده کشوری', 0, 0),
(10, -1001436337105, ' همراهان استانبول❤️', 0, 1),
(11, -1001076381224, ' گروه ایرانیان کانادا / ترکیه / ایران 🇨🇦🇮🇷🇹🇷', 0, 0),
(12, -1001231494433, ' GLOBAL_GRUP ( تبلیغات آزاد )', 0, 0),
(13, -1001376490799, ' دیوار استانبول🇹🇷', 0, 0),
(14, -1001274923265, ' دیوار بیلیکدوزو ترکیه🔖istanbul🔖😊', 0, 0),
(15, -1001179282853, ' 🇹🇷تبلیغات ترکیه و حومه🇹🇷', 0, 0),
(16, -1001418843037, ' تبلیغات آزاد سورنا( استانبول)', 0, 0),
(17, -1001166264532, ' دیوار جمهوریت', 0, 0),
(18, -1001428682447, ' ARSES HOLDİNG İSTANBUL', 0, 0),
(19, -1001397695283, ' دیوار استانبول ترکیه ⁦⁦🇹🇷', 0, 0),
(20, -1001265799667, ' تبلیغات آزاد دنیزلی کالا', 0, 0),
(21, -1001304882403, ' Finding Jobs In Canada', 0, 0),
(22, -1001237069129, ' تور و اسکان کانادا 🇨🇦', 0, 0),
(23, -1001176658557, ' 🇨🇦 ایرانیان کبک و مونترال 🇨🇦', 0, 0),
(24, -1001127228802, ' رستوران ها و تفریحات مونترال', 0, 0),
(25, -1001409610941, ' ایرانیان🇮🇷 کانادا🇨🇦🌐', 0, 0),
(26, -1001317920282, ' 🇨🇦 Welcome to Canada 🇨🇦', 0, 0),
(27, -1001205559938, ' 👑 KING TRADE 👑', 0, 0),
(28, -1001288654911, ' گروه مشاورین املاک کوروش بزرگ در استانبول', 0, 0),
(29, -1001333338348, ' مسکن ارگ بریانک', 0, 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `advertise`
--
ALTER TABLE `advertise`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `advertiser_admins`
--
ALTER TABLE `advertiser_admins`
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

--
-- AUTO_INCREMENT for table `advertise`
--
ALTER TABLE `advertise`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `advertiser_admins`
--
ALTER TABLE `advertiser_admins`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `advertise_group`
--
ALTER TABLE `advertise_group`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `advertise_runs`
--
ALTER TABLE `advertise_runs`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `bot_groups`
--
ALTER TABLE `bot_groups`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
