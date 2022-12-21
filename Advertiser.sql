-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 21, 2022 at 07:59 AM
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
  `Advertise_Period` float NOT NULL DEFAULT 24,
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
(1, 954, '2022-12-20 11:08:28', 0, 2, 2057086971, 'Modern_Istanbul', 'Modern', 'Istanbul', 'Modern Istanbul', 1);

-- --------------------------------------------------------

--
-- Table structure for table `advertiser_users`
--

CREATE TABLE `advertiser_users` (
  `Id` int(11) NOT NULL,
  `User_Id` bigint(11) NOT NULL,
  `User_Name` text NOT NULL,
  `User_First_Name` text NOT NULL,
  `User_Last_Name` text NOT NULL,
  `User_Full_Name` text NOT NULL,
  `Admin` int(11) DEFAULT NULL,
  `Active` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `advertiser_users`
--

INSERT INTO `advertiser_users` (`Id`, `User_Id`, `User_Name`, `User_First_Name`, `User_Last_Name`, `User_Full_Name`, `Admin`, `Active`) VALUES
(1, 2057086971, 'Modern_Istanbul', 'Modern', 'Istanbul', 'Modern Istanbul', 1, 1);

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
  `Group_Name` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `advertise_runs`
--

INSERT INTO `advertise_runs` (`Id`, `Advertise_Id`, `Advertise_Remain`, `Advertise_NextRun`, `Group_Id`, `Group_Name`) VALUES
(6, 653, -1, '2022-12-19 21:11:11', -1001702818002, '0'),
(7, 653, -2, '2022-12-19 22:11:11', -1001702818002, '0'),
(8, 653, -3, '2022-12-19 22:11:11', -882770672, '0'),
(9, 653, -4, '2022-12-19 22:41:11', -1001702818002, '0'),
(10, 653, -5, '2022-12-19 22:41:11', -1001436337105, '0'),
(11, 653, -6, '2022-12-19 22:41:11', -882770672, '0'),
(12, 653, -7, '2022-12-19 23:41:11', -1001702818002, '0'),
(13, 653, -8, '2022-12-19 23:41:11', -1001436337105, '0'),
(14, 653, -9, '2022-12-19 23:41:11', -882770672, '0'),
(15, 653, -10, '2022-12-20 00:41:12', -1001702818002, '0'),
(16, 653, -11, '2022-12-20 00:41:12', -1001436337105, '0'),
(17, 653, -12, '2022-12-20 00:41:12', -882770672, '0'),
(18, 653, -13, '2022-12-20 01:41:12', -1001702818002, '0'),
(19, 653, -14, '2022-12-20 01:41:12', -1001436337105, '0'),
(20, 653, -15, '2022-12-20 01:41:12', -882770672, '0'),
(21, 653, -16, '2022-12-20 02:41:12', -1001702818002, '0'),
(22, 653, -17, '2022-12-20 02:41:12', -1001436337105, '0'),
(23, 653, -18, '2022-12-20 02:41:12', -882770672, '0'),
(24, 653, -19, '2022-12-20 03:41:12', -1001702818002, 'تبلیغات Modern Istanbul'),
(25, 653, -20, '2022-12-20 03:41:12', -1001436337105, ' همراهان استانبول❤️'),
(26, 653, -21, '2022-12-20 04:41:12', -1001702818002, 'تبلیغات Modern Istanbul'),
(27, 653, -22, '2022-12-20 04:41:12', -1001436337105, ' همراهان استانبول❤️'),
(28, 653, -23, '2022-12-20 05:41:12', -1001702818002, 'تبلیغات Modern Istanbul'),
(29, 653, -24, '2022-12-20 05:41:12', -1001436337105, ' همراهان استانبول❤️'),
(30, 653, -25, '2022-12-20 06:41:12', -1001702818002, 'تبلیغات Modern Istanbul'),
(31, 653, -26, '2022-12-20 06:41:12', -1001436337105, ' همراهان استانبول❤️'),
(32, 653, -27, '2022-12-20 08:41:12', -1001702818002, 'تبلیغات Modern Istanbul'),
(33, 653, -28, '2022-12-20 08:41:12', -1001436337105, ' همراهان استانبول❤️'),
(34, 653, -29, '2022-12-20 10:41:12', -1001702818002, 'تبلیغات Modern Istanbul'),
(35, 653, -30, '2022-12-20 10:41:12', -1001436337105, ' همراهان استانبول❤️'),
(36, 653, -31, '2022-12-20 18:54:06', -1001702818002, 'تبلیغات Modern Istanbul'),
(37, 653, -32, '2022-12-20 18:54:06', -1001436337105, ' همراهان استانبول❤️'),
(38, 954, -1, '2022-12-20 19:44:14', -1001702818002, 'تبلیغات Modern Istanbul'),
(39, 954, -2, '2022-12-20 19:44:14', -1001436337105, ' همراهان استانبول❤️'),
(40, 954, -3, '2022-12-20 21:44:14', -1001702818002, 'تبلیغات Modern Istanbul'),
(41, 954, -4, '2022-12-20 21:44:14', -1001436337105, ' همراهان استانبول❤️'),
(42, 954, -5, '2022-12-20 23:44:14', -1001702818002, 'تبلیغات Modern Istanbul'),
(43, 954, -6, '2022-12-20 23:44:14', -1001436337105, ' همراهان استانبول❤️'),
(44, 954, -7, '2022-12-21 01:44:14', -1001702818002, 'تبلیغات Modern Istanbul'),
(45, 954, -8, '2022-12-21 01:44:14', -1001436337105, ' همراهان استانبول❤️'),
(46, 954, -9, '2022-12-21 03:44:14', -1001702818002, 'تبلیغات Modern Istanbul'),
(47, 954, -10, '2022-12-21 03:44:14', -1001436337105, ' همراهان استانبول❤️'),
(48, 954, -11, '2022-12-21 05:44:14', -1001702818002, 'تبلیغات Modern Istanbul'),
(49, 954, -12, '2022-12-21 05:44:14', -1001436337105, ' همراهان استانبول❤️'),
(50, 954, -13, '2022-12-21 07:44:14', -1001702818002, 'تبلیغات Modern Istanbul'),
(51, 954, -14, '2022-12-21 07:44:14', -1001436337105, ' همراهان استانبول❤️'),
(52, 954, -15, '2022-12-21 09:44:14', -1001702818002, 'تبلیغات Modern Istanbul'),
(53, 954, -16, '2022-12-21 09:44:14', -1001436337105, ' همراهان استانبول❤️'),
(54, 954, -17, '2022-12-21 11:44:14', -1001702818002, 'تبلیغات Modern Istanbul'),
(55, 954, -18, '2022-12-21 11:44:14', -1001436337105, ' همراهان استانبول❤️'),
(56, 954, -19, '2022-12-21 13:44:14', -1001702818002, 'تبلیغات Modern Istanbul');

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
(3, -1001144942180, 'نیازمندیهای استانبول', 0, 1),
(4, -1001213552027, ' 🇹🇷دیوار شهر استانبول🇹🇷', 0, 1),
(5, -1001297266212, ' نیازمندی ترکیه و ایران (عمومی) 🇹🇷', 0, 1),
(6, -1001300758476, ' نیازمندی ترکیه و ایران (عمومی)🇹🇷', 0, 1),
(7, -1001289840286, ' نیازصنعت ابزار', 0, 1),
(8, -1001149708252, ' تبلیغات استان اصفهان پیربکران فلاورجان مبارکه بهاران ابریشم کلیشاد سودرجان قهدریجان', 0, 1),
(9, -1001516526756, ' تبلیغات گسترده کشوری', 0, 1),
(10, -1001436337105, ' همراهان استانبول❤️', 0, 1),
(11, -1001076381224, ' گروه ایرانیان کانادا / ترکیه / ایران 🇨🇦🇮🇷🇹🇷', 0, 1),
(12, -1001231494433, ' GLOBAL_GRUP ( تبلیغات آزاد )', 0, 1),
(13, -1001376490799, ' دیوار استانبول🇹🇷', 0, 1),
(14, -1001274923265, ' دیوار بیلیکدوزو ترکیه🔖istanbul🔖😊', 0, 1),
(15, -1001179282853, ' 🇹🇷تبلیغات ترکیه و حومه🇹🇷', 0, 1),
(16, -1001418843037, ' تبلیغات آزاد سورنا( استانبول)', 0, 1),
(17, -1001166264532, ' دیوار جمهوریت', 0, 1),
(18, -1001428682447, ' ARSES HOLDİNG İSTANBUL', 0, 1),
(19, -1001397695283, ' دیوار استانبول ترکیه ⁦⁦🇹🇷', 0, 1),
(20, -1001265799667, ' تبلیغات آزاد دنیزلی کالا', 0, 1),
(21, -1001304882403, ' Finding Jobs In Canada', 0, 1),
(22, -1001237069129, ' تور و اسکان کانادا 🇨🇦', 0, 1),
(23, -1001176658557, ' 🇨🇦 ایرانیان کبک و مونترال 🇨🇦', 0, 1),
(24, -1001127228802, ' رستوران ها و تفریحات مونترال', 0, 1),
(25, -1001409610941, ' ایرانیان🇮🇷 کانادا🇨🇦🌐', 0, 1),
(26, -1001317920282, ' 🇨🇦 Welcome to Canada 🇨🇦', 0, 1),
(27, -1001205559938, ' 👑 KING TRADE 👑', 0, 1),
(28, -1001288654911, ' گروه مشاورین املاک کوروش بزرگ در استانبول', 0, 1),
(29, -1001333338348, ' مسکن ارگ بریانک', 0, 1),
(30, -882770672, 'Adv_1', 0, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `advertise`
--
ALTER TABLE `advertise`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `advertiser_users`
--
ALTER TABLE `advertiser_users`
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
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `advertise_group`
--
ALTER TABLE `advertise_group`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `advertise_runs`
--
ALTER TABLE `advertise_runs`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;

--
-- AUTO_INCREMENT for table `bot_groups`
--
ALTER TABLE `bot_groups`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
