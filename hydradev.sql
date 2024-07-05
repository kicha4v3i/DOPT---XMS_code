-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 04, 2023 at 11:58 AM
-- Server version: 8.0.33-0ubuntu0.20.04.2
-- PHP Version: 7.4.3-4ubuntu2.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hydradev`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(1, 'Admin'),
(2, 'Creator'),
(3, 'Editor'),
(4, 'Viewer');

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add permission', 1, 'add_permission'),
(2, 'Can change permission', 1, 'change_permission'),
(3, 'Can delete permission', 1, 'delete_permission'),
(4, 'Can view permission', 1, 'view_permission'),
(5, 'Can add group', 2, 'add_group'),
(6, 'Can change group', 2, 'change_group'),
(7, 'Can delete group', 2, 'delete_group'),
(8, 'Can view group', 2, 'view_group'),
(9, 'Can add content type', 3, 'add_contenttype'),
(10, 'Can change content type', 3, 'change_contenttype'),
(11, 'Can delete content type', 3, 'delete_contenttype'),
(12, 'Can view content type', 3, 'view_contenttype'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add basecountries', 5, 'add_basecountries'),
(18, 'Can change basecountries', 5, 'change_basecountries'),
(19, 'Can delete basecountries', 5, 'delete_basecountries'),
(20, 'Can view basecountries', 5, 'view_basecountries'),
(21, 'Can add companies', 6, 'add_companies'),
(22, 'Can change companies', 6, 'change_companies'),
(23, 'Can delete companies', 6, 'delete_companies'),
(24, 'Can view companies', 6, 'view_companies'),
(25, 'Can add countries', 7, 'add_countries'),
(26, 'Can change countries', 7, 'change_countries'),
(27, 'Can delete countries', 7, 'delete_countries'),
(28, 'Can view countries', 7, 'view_countries'),
(29, 'Can add enquiry', 8, 'add_enquiry'),
(30, 'Can change enquiry', 8, 'change_enquiry'),
(31, 'Can delete enquiry', 8, 'delete_enquiry'),
(32, 'Can view enquiry', 8, 'view_enquiry'),
(33, 'Can add modules', 9, 'add_modules'),
(34, 'Can change modules', 9, 'change_modules'),
(35, 'Can delete modules', 9, 'delete_modules'),
(36, 'Can view modules', 9, 'view_modules'),
(37, 'Can add package concurrent users', 10, 'add_packageconcurrentusers'),
(38, 'Can change package concurrent users', 10, 'change_packageconcurrentusers'),
(39, 'Can delete package concurrent users', 10, 'delete_packageconcurrentusers'),
(40, 'Can view package concurrent users', 10, 'view_packageconcurrentusers'),
(41, 'Can add packages', 11, 'add_packages'),
(42, 'Can change packages', 11, 'change_packages'),
(43, 'Can delete packages', 11, 'delete_packages'),
(44, 'Can view packages', 11, 'view_packages'),
(45, 'Can add userlog', 12, 'add_userlog'),
(46, 'Can change userlog', 12, 'change_userlog'),
(47, 'Can delete userlog', 12, 'delete_userlog'),
(48, 'Can view userlog', 12, 'view_userlog'),
(49, 'Can add rights', 13, 'add_rights'),
(50, 'Can change rights', 13, 'change_rights'),
(51, 'Can delete rights', 13, 'delete_rights'),
(52, 'Can view rights', 13, 'view_rights'),
(53, 'Can add payments', 14, 'add_payments'),
(54, 'Can change payments', 14, 'change_payments'),
(55, 'Can delete payments', 14, 'delete_payments'),
(56, 'Can view payments', 14, 'view_payments'),
(57, 'Can add package users', 15, 'add_packageusers'),
(58, 'Can change package users', 15, 'change_packageusers'),
(59, 'Can delete package users', 15, 'delete_packageusers'),
(60, 'Can view package users', 15, 'view_packageusers'),
(61, 'Can add company packages', 16, 'add_companypackages'),
(62, 'Can change company packages', 16, 'change_companypackages'),
(63, 'Can delete company packages', 16, 'delete_companypackages'),
(64, 'Can view company packages', 16, 'view_companypackages'),
(65, 'Can add projects', 17, 'add_projects'),
(66, 'Can change projects', 17, 'change_projects'),
(67, 'Can delete projects', 17, 'delete_projects'),
(68, 'Can view projects', 17, 'view_projects'),
(69, 'Can add userrights', 18, 'add_userrights'),
(70, 'Can change userrights', 18, 'change_userrights'),
(71, 'Can delete userrights', 18, 'delete_userrights'),
(72, 'Can view userrights', 18, 'view_userrights'),
(73, 'Can add projectuserrights', 19, 'add_projectuserrights'),
(74, 'Can change projectuserrights', 19, 'change_projectuserrights'),
(75, 'Can delete projectuserrights', 19, 'delete_projectuserrights'),
(76, 'Can view projectuserrights', 19, 'view_projectuserrights'),
(77, 'Can add project block', 20, 'add_projectblock'),
(78, 'Can change project block', 20, 'change_projectblock'),
(79, 'Can delete project block', 20, 'delete_projectblock'),
(80, 'Can view project block', 20, 'view_projectblock'),
(81, 'Can add project field', 21, 'add_projectfield'),
(82, 'Can change project field', 21, 'change_projectfield'),
(83, 'Can delete project field', 21, 'delete_projectfield'),
(84, 'Can view project field', 21, 'view_projectfield'),
(85, 'Can add project users', 22, 'add_projectusers'),
(86, 'Can change project users', 22, 'change_projectusers'),
(87, 'Can delete project users', 22, 'delete_projectusers'),
(88, 'Can view project users', 22, 'view_projectusers'),
(89, 'Can add coordinate systems', 23, 'add_coordinatesystems'),
(90, 'Can change coordinate systems', 23, 'change_coordinatesystems'),
(91, 'Can delete coordinate systems', 23, 'delete_coordinatesystems'),
(92, 'Can view coordinate systems', 23, 'view_coordinatesystems'),
(93, 'Can add projections', 24, 'add_projections'),
(94, 'Can change projections', 24, 'change_projections'),
(95, 'Can delete projections', 24, 'delete_projections'),
(96, 'Can view projections', 24, 'view_projections'),
(97, 'Can add wells', 25, 'add_wells'),
(98, 'Can change wells', 25, 'change_wells'),
(99, 'Can delete wells', 25, 'delete_wells'),
(100, 'Can view wells', 25, 'view_wells'),
(101, 'Can add well users', 26, 'add_wellusers'),
(102, 'Can change well users', 26, 'change_wellusers'),
(103, 'Can delete well users', 26, 'delete_wellusers'),
(104, 'Can view well users', 26, 'view_wellusers'),
(105, 'Can add mud pump', 27, 'add_mudpump'),
(106, 'Can change mud pump', 27, 'change_mudpump'),
(107, 'Can delete mud pump', 27, 'delete_mudpump'),
(108, 'Can view mud pump', 27, 'view_mudpump'),
(109, 'Can add mud pump speed', 28, 'add_mudpumpspeed'),
(110, 'Can change mud pump speed', 28, 'change_mudpumpspeed'),
(111, 'Can delete mud pump speed', 28, 'delete_mudpumpspeed'),
(112, 'Can view mud pump speed', 28, 'view_mudpumpspeed'),
(113, 'Can add mud pump flow rate', 29, 'add_mudpumpflowrate'),
(114, 'Can change mud pump flow rate', 29, 'change_mudpumpflowrate'),
(115, 'Can delete mud pump flow rate', 29, 'delete_mudpumpflowrate'),
(116, 'Can view mud pump flow rate', 29, 'view_mudpumpflowrate'),
(117, 'Can add mud pump data', 30, 'add_mudpumpdata'),
(118, 'Can change mud pump data', 30, 'change_mudpumpdata'),
(119, 'Can delete mud pump data', 30, 'delete_mudpumpdata'),
(120, 'Can view mud pump data', 30, 'view_mudpumpdata'),
(121, 'Can add pump manufacturer', 31, 'add_pumpmanufacturer'),
(122, 'Can change pump manufacturer', 31, 'change_pumpmanufacturer'),
(123, 'Can delete pump manufacturer', 31, 'delete_pumpmanufacturer'),
(124, 'Can view pump manufacturer', 31, 'view_pumpmanufacturer'),
(125, 'Can add pumps', 32, 'add_pumps'),
(126, 'Can change pumps', 32, 'change_pumps'),
(127, 'Can delete pumps', 32, 'delete_pumps'),
(128, 'Can view pumps', 32, 'view_pumps'),
(129, 'Can add mud pump master speed', 33, 'add_mudpumpmasterspeed'),
(130, 'Can change mud pump master speed', 33, 'change_mudpumpmasterspeed'),
(131, 'Can delete mud pump master speed', 33, 'delete_mudpumpmasterspeed'),
(132, 'Can view mud pump master speed', 33, 'view_mudpumpmasterspeed'),
(133, 'Can add mud pump master flow rate', 34, 'add_mudpumpmasterflowrate'),
(134, 'Can change mud pump master flow rate', 34, 'change_mudpumpmasterflowrate'),
(135, 'Can delete mud pump master flow rate', 34, 'delete_mudpumpmasterflowrate'),
(136, 'Can view mud pump master flow rate', 34, 'view_mudpumpmasterflowrate'),
(137, 'Can add mud pump master data', 35, 'add_mudpumpmasterdata'),
(138, 'Can change mud pump master data', 35, 'change_mudpumpmasterdata'),
(139, 'Can delete mud pump master data', 35, 'delete_mudpumpmasterdata'),
(140, 'Can view mud pump master data', 35, 'view_mudpumpmasterdata'),
(141, 'Can add surface name models', 36, 'add_surfacenamemodels'),
(142, 'Can change surface name models', 36, 'change_surfacenamemodels'),
(143, 'Can delete surface name models', 36, 'delete_surfacenamemodels'),
(144, 'Can view surface name models', 36, 'view_surfacenamemodels'),
(145, 'Can add surface pipe data', 37, 'add_surfacepipedata'),
(146, 'Can change surface pipe data', 37, 'change_surfacepipedata'),
(147, 'Can delete surface pipe data', 37, 'delete_surfacepipedata'),
(148, 'Can view surface pipe data', 37, 'view_surfacepipedata'),
(149, 'Can add surface pipe', 38, 'add_surfacepipe'),
(150, 'Can change surface pipe', 38, 'change_surfacepipe'),
(151, 'Can delete surface pipe', 38, 'delete_surfacepipe'),
(152, 'Can view surface pipe', 38, 'view_surfacepipe'),
(153, 'Can add pressure', 39, 'add_pressure'),
(154, 'Can change pressure', 39, 'change_pressure'),
(155, 'Can delete pressure', 39, 'delete_pressure'),
(156, 'Can view pressure', 39, 'view_pressure'),
(157, 'Can add well phases', 40, 'add_wellphases'),
(158, 'Can change well phases', 40, 'change_wellphases'),
(159, 'Can delete well phases', 40, 'delete_wellphases'),
(160, 'Can view well phases', 40, 'view_wellphases'),
(161, 'Can add casing types', 41, 'add_casingtypes'),
(162, 'Can change casing types', 41, 'change_casingtypes'),
(163, 'Can delete casing types', 41, 'delete_casingtypes'),
(164, 'Can view casing types', 41, 'view_casingtypes'),
(165, 'Can add casinggrade', 42, 'add_casinggrade'),
(166, 'Can change casinggrade', 42, 'change_casinggrade'),
(167, 'Can delete casinggrade', 42, 'delete_casinggrade'),
(168, 'Can view casinggrade', 42, 'view_casinggrade'),
(169, 'Can add casingrange', 43, 'add_casingrange'),
(170, 'Can change casingrange', 43, 'change_casingrange'),
(171, 'Can delete casingrange', 43, 'delete_casingrange'),
(172, 'Can view casingrange', 43, 'view_casingrange'),
(173, 'Can add casing', 44, 'add_casing'),
(174, 'Can change casing', 44, 'change_casing'),
(175, 'Can delete casing', 44, 'delete_casing'),
(176, 'Can view casing', 44, 'view_casing'),
(177, 'Can add well trajectory', 45, 'add_welltrajectory'),
(178, 'Can change well trajectory', 45, 'change_welltrajectory'),
(179, 'Can delete well trajectory', 45, 'delete_welltrajectory'),
(180, 'Can view well trajectory', 45, 'view_welltrajectory'),
(181, 'Can add mud data', 46, 'add_muddata'),
(182, 'Can change mud data', 46, 'change_muddata'),
(183, 'Can delete mud data', 46, 'delete_muddata'),
(184, 'Can view mud data', 46, 'view_muddata'),
(185, 'Can add mud type', 47, 'add_mudtype'),
(186, 'Can change mud type', 47, 'change_mudtype'),
(187, 'Can delete mud type', 47, 'delete_mudtype'),
(188, 'Can view mud type', 47, 'view_mudtype'),
(189, 'Can add sections', 48, 'add_sections'),
(190, 'Can change sections', 48, 'change_sections'),
(191, 'Can delete sections', 48, 'delete_sections'),
(192, 'Can view sections', 48, 'view_sections'),
(193, 'Can add pressureloss_data', 49, 'add_pressureloss_data'),
(194, 'Can change pressureloss_data', 49, 'change_pressureloss_data'),
(195, 'Can delete pressureloss_data', 49, 'delete_pressureloss_data'),
(196, 'Can view pressureloss_data', 49, 'view_pressureloss_data'),
(197, 'Can add rheogram', 50, 'add_rheogram'),
(198, 'Can change rheogram', 50, 'change_rheogram'),
(199, 'Can delete rheogram', 50, 'delete_rheogram'),
(200, 'Can view rheogram', 50, 'view_rheogram'),
(201, 'Can add rheogram name models', 51, 'add_rheogramnamemodels'),
(202, 'Can change rheogram name models', 51, 'change_rheogramnamemodels'),
(203, 'Can delete rheogram name models', 51, 'delete_rheogramnamemodels'),
(204, 'Can view rheogram name models', 51, 'view_rheogramnamemodels'),
(205, 'Can add rheogram date', 52, 'add_rheogramdate'),
(206, 'Can change rheogram date', 52, 'change_rheogramdate'),
(207, 'Can delete rheogram date', 52, 'delete_rheogramdate'),
(208, 'Can view rheogram date', 52, 'view_rheogramdate'),
(209, 'Can add rheogram sections', 53, 'add_rheogramsections'),
(210, 'Can change rheogram sections', 53, 'change_rheogramsections'),
(211, 'Can delete rheogram sections', 53, 'delete_rheogramsections'),
(212, 'Can view rheogram sections', 53, 'view_rheogramsections'),
(213, 'Can add hydraulic data', 54, 'add_hydraulicdata'),
(214, 'Can change hydraulic data', 54, 'change_hydraulicdata'),
(215, 'Can delete hydraulic data', 54, 'delete_hydraulicdata'),
(216, 'Can view hydraulic data', 54, 'view_hydraulicdata'),
(217, 'Can add planwell_data', 55, 'add_planwell_data'),
(218, 'Can change planwell_data', 55, 'change_planwell_data'),
(219, 'Can delete planwell_data', 55, 'delete_planwell_data'),
(220, 'Can view planwell_data', 55, 'view_planwell_data'),
(221, 'Can add drill bit', 56, 'add_drillbit'),
(222, 'Can change drill bit', 56, 'change_drillbit'),
(223, 'Can delete drill bit', 56, 'delete_drillbit'),
(224, 'Can view drill bit', 56, 'view_drillbit'),
(225, 'Can add bit types names', 57, 'add_bittypesnames'),
(226, 'Can change bit types names', 57, 'change_bittypesnames'),
(227, 'Can delete bit types names', 57, 'delete_bittypesnames'),
(228, 'Can view bit types names', 57, 'view_bittypesnames'),
(229, 'Can add drill bit nozzle', 58, 'add_drillbitnozzle'),
(230, 'Can change drill bit nozzle', 58, 'change_drillbitnozzle'),
(231, 'Can delete drill bit nozzle', 58, 'delete_drillbitnozzle'),
(232, 'Can view drill bit nozzle', 58, 'view_drillbitnozzle'),
(233, 'Can add drillpipe', 59, 'add_drillpipe'),
(234, 'Can change drillpipe', 59, 'change_drillpipe'),
(235, 'Can delete drillpipe', 59, 'delete_drillpipe'),
(236, 'Can view drillpipe', 59, 'view_drillpipe'),
(237, 'Can add drillcollers', 60, 'add_drillcollers'),
(238, 'Can change drillcollers', 60, 'change_drillcollers'),
(239, 'Can delete drillcollers', 60, 'delete_drillcollers'),
(240, 'Can view drillcollers', 60, 'view_drillcollers'),
(241, 'Can add drillpipe hwdp', 61, 'add_drillpipehwdp'),
(242, 'Can change drillpipe hwdp', 61, 'change_drillpipehwdp'),
(243, 'Can delete drillpipe hwdp', 61, 'delete_drillpipehwdp'),
(244, 'Can view drillpipe hwdp', 61, 'view_drillpipehwdp'),
(245, 'Can add specifications', 62, 'add_specifications'),
(246, 'Can change specifications', 62, 'change_specifications'),
(247, 'Can delete specifications', 62, 'delete_specifications'),
(248, 'Can view specifications', 62, 'view_specifications'),
(249, 'Can add pressuredroptool', 63, 'add_pressuredroptool'),
(250, 'Can change pressuredroptool', 63, 'change_pressuredroptool'),
(251, 'Can delete pressuredroptool', 63, 'delete_pressuredroptool'),
(252, 'Can view pressuredroptool', 63, 'view_pressuredroptool'),
(253, 'Can add empirical', 64, 'add_empirical'),
(254, 'Can change empirical', 64, 'change_empirical'),
(255, 'Can delete empirical', 64, 'delete_empirical'),
(256, 'Can view empirical', 64, 'view_empirical'),
(257, 'Can add differential_pressure', 65, 'add_differential_pressure'),
(258, 'Can change differential_pressure', 65, 'change_differential_pressure'),
(259, 'Can delete differential_pressure', 65, 'delete_differential_pressure'),
(260, 'Can view differential_pressure', 65, 'view_differential_pressure'),
(261, 'Can add bha data', 66, 'add_bhadata'),
(262, 'Can change bha data', 66, 'change_bhadata'),
(263, 'Can delete bha data', 66, 'delete_bhadata'),
(264, 'Can view bha data', 66, 'view_bhadata'),
(265, 'Can add bha element', 67, 'add_bhaelement'),
(266, 'Can change bha element', 67, 'change_bhaelement'),
(267, 'Can delete bha element', 67, 'delete_bhaelement'),
(268, 'Can view bha element', 67, 'view_bhaelement'),
(269, 'Can add rig', 68, 'add_rig'),
(270, 'Can change rig', 68, 'change_rig'),
(271, 'Can delete rig', 68, 'delete_rig'),
(272, 'Can view rig', 68, 'view_rig'),
(273, 'Can add session', 69, 'add_session'),
(274, 'Can change session', 69, 'change_session'),
(275, 'Can delete session', 69, 'delete_session'),
(276, 'Can view session', 69, 'view_session'),
(277, 'Can add notification', 70, 'add_notification'),
(278, 'Can change notification', 70, 'change_notification'),
(279, 'Can delete notification', 70, 'delete_notification'),
(280, 'Can view notification', 70, 'view_notification'),
(281, 'Can add log entry', 71, 'add_logentry'),
(282, 'Can change log entry', 71, 'change_logentry'),
(283, 'Can delete log entry', 71, 'delete_logentry'),
(284, 'Can view log entry', 71, 'view_logentry'),
(285, 'Can add query model', 72, 'add_querymodel'),
(286, 'Can change query model', 72, 'change_querymodel'),
(287, 'Can delete query model', 72, 'delete_querymodel'),
(288, 'Can view query model', 72, 'view_querymodel'),
(289, 'Can add tickets', 73, 'add_tickets'),
(290, 'Can change tickets', 73, 'change_tickets'),
(291, 'Can delete tickets', 73, 'delete_tickets'),
(292, 'Can view tickets', 73, 'view_tickets'),
(293, 'Can add licensepackage', 74, 'add_licensepackage'),
(294, 'Can change licensepackage', 74, 'change_licensepackage'),
(295, 'Can delete licensepackage', 74, 'delete_licensepackage'),
(296, 'Can view licensepackage', 74, 'view_licensepackage');

-- --------------------------------------------------------

--
-- Table structure for table `bhadata_bhadata`
--

CREATE TABLE `bhadata_bhadata` (
  `id` int NOT NULL,
  `date` date DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) DEFAULT NULL,
  `timestamp` int DEFAULT NULL,
  `time` time(6) DEFAULT NULL,
  `bhaname` varchar(30) DEFAULT NULL,
  `depth` double DEFAULT NULL,
  `company_id` int DEFAULT NULL,
  `well_id` bigint DEFAULT NULL,
  `well_phases_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `bhadata_bhadata`
--

INSERT INTO `bhadata_bhadata` (`id`, `date`, `status`, `created`, `timestamp`, `time`, `bhaname`, `depth`, `company_id`, `well_id`, `well_phases_id`) VALUES
(1, NULL, 1, '2023-07-14 11:21:06.939943', NULL, NULL, NULL, NULL, 2, 2, 3);

-- --------------------------------------------------------

--
-- Table structure for table `bhadata_bhaelement`
--

CREATE TABLE `bhadata_bhaelement` (
  `id` int NOT NULL,
  `element` varchar(30) DEFAULT NULL,
  `od` varchar(30) DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `class_element` varchar(30) DEFAULT NULL,
  `grade` varchar(30) DEFAULT NULL,
  `pipe_type` varchar(30) DEFAULT NULL,
  `connection_type` varchar(30) DEFAULT NULL,
  `tool_od` double DEFAULT NULL,
  `identity` varchar(30) DEFAULT NULL,
  `length` varchar(30) DEFAULT NULL,
  `length_onejoint` double DEFAULT NULL,
  `onejoint_length` varchar(30) DEFAULT NULL,
  `type_name` varchar(30) DEFAULT NULL,
  `box_tj_length` varchar(30) DEFAULT NULL,
  `pin_tj_length` varchar(30) DEFAULT NULL,
  `tool_id` double DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) DEFAULT NULL,
  `calculation_type` int NOT NULL,
  `bhadata_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `bhadata_bhaelement`
--

INSERT INTO `bhadata_bhaelement` (`id`, `element`, `od`, `weight`, `class_element`, `grade`, `pipe_type`, `connection_type`, `tool_od`, `identity`, `length`, `length_onejoint`, `onejoint_length`, `type_name`, `box_tj_length`, `pin_tj_length`, `tool_id`, `status`, `created`, `calculation_type`, `bhadata_id`) VALUES
(1, 'PDC Bit', '8.5', NULL, NULL, NULL, NULL, NULL, NULL, '', '1', 1, NULL, 'Bit', NULL, NULL, NULL, 1, '2023-07-14 11:21:07.008864', 0, 1),
(2, '5\" Drill Pipe', '5.0', 19.5, 'Class I', 'S-135', NULL, 'NC50', 6.625, '4.276', '2303', 2304, '30', 'Drill Pipe', '12', '9', 3.25, 1, '2023-07-14 11:21:07.202530', 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `bhadata_differential_pressure`
--

CREATE TABLE `bhadata_differential_pressure` (
  `id` int NOT NULL,
  `torque` double DEFAULT NULL,
  `diff_pressure` double DEFAULT NULL,
  `status` int NOT NULL,
  `bhadata_id` int DEFAULT NULL,
  `bhadata_element_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bhadata_drillcollers`
--

CREATE TABLE `bhadata_drillcollers` (
  `id` int NOT NULL,
  `normal_od` double DEFAULT NULL,
  `normal_id` double DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `pipe_type` varchar(30) DEFAULT NULL,
  `connection_type` varchar(30) DEFAULT NULL,
  `tool_od` double DEFAULT NULL,
  `tool_id` double DEFAULT NULL,
  `unit` varchar(30) DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) DEFAULT NULL,
  `is_superadmin` int NOT NULL,
  `company_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `bhadata_drillcollers`
--

INSERT INTO `bhadata_drillcollers` (`id`, `normal_od`, `normal_id`, `weight`, `pipe_type`, `connection_type`, `tool_od`, `tool_id`, `unit`, `status`, `created`, `is_superadmin`, `company_id`) VALUES
(1, 2.5, 1.375, 11.5, 'Slick', 'MW20', 2.5, 1.375, 'API', 1, '2021-08-19 05:11:17.785177', 1, NULL),
(2, 3.125, 0.813, 19.83, 'Slick', '2 7/8 HTPAC', 3.125, 1.5, 'API', 1, '2021-08-19 05:11:17.793101', 1, NULL),
(3, 3.125, 1.25, 21.65, 'Spiral', '2 7/8 HTPAC', 3.125, 1.25, 'API', 1, '2021-08-19 05:11:17.801924', 1, NULL),
(4, 3.125, 1.25, 21.65, 'Slick', '2 7/8 HTPAC', 3.125, 1.25, 'API', 1, '2021-08-19 05:11:17.809209', 1, NULL),
(5, 3.125, 1.25, 21.65, 'Slick', '2 3/8 HT-SL-H90', 3.125, 1.25, 'API', 1, '2021-08-19 05:11:17.816229', 1, NULL),
(6, 3.125, 1.25, 21.65, 'Slick', '2 7/8 PAC (Drill Collar)', 3.125, 1.25, 'API', 1, '2021-08-19 05:11:17.822131', 1, NULL),
(7, 3.5, 1.5, 26.39, 'Spiral', 'NC26 (Drill Collar)', 3.5, 1.5, 'API', 1, '2021-08-19 05:11:17.827233', 1, NULL),
(8, 3.5, 1.5, 26.39, 'Slick', 'CTM26', 3.5, 1.5, 'API', 1, '2021-08-19 05:11:17.832369', 1, NULL),
(9, 3.875, 1.75, 31.54, 'Slick', '2 7/8 AOH', 3.875, 1.75, 'API', 1, '2021-08-19 05:11:17.837480', 1, NULL),
(10, 4.125, 2, 34.35, 'Spiral', 'NC31 (Drill Collar)', 4.125, 2, 'API', 1, '2021-08-19 05:11:17.842414', 1, NULL),
(11, 4.125, 2, 34.35, 'Slick', 'NC31 (Drill Collar)', 4.125, 2, 'API', 1, '2021-08-19 05:11:17.847497', 1, NULL),
(12, 4.75, 2.563, 42.21, 'Spiral', 'WT38', 4.75, 2.563, 'API', 1, '2021-08-19 05:11:17.852530', 1, NULL),
(13, 4.75, 2.25, 46.18, 'Spiral', '3 1/2 PH6 (12.95#)', 4.313, 2.25, 'API', 1, '2021-08-19 05:11:17.857918', 1, NULL),
(14, 4.75, 2.25, 46.73, 'Spiral', 'NC38 (Drill Collar)', 4.75, 2.25, 'API', 1, '2021-08-19 05:11:17.863137', 1, NULL),
(15, 4.75, 2.25, 46.18, 'Slick', 'NC38 (Drill Collar)', 4.75, 2.25, 'API', 1, '2021-08-19 05:11:17.868151', 1, NULL),
(16, 4.75, 2.25, 46.18, 'Spiral', 'XT-M38', 4.75, 2.25, 'API', 1, '2021-08-19 05:11:17.873996', 1, NULL),
(17, 4.875, 2.25, 49.36, 'Spiral', 'NC38 (Drill Collar)', 4.875, 2.25, 'API', 1, '2021-08-19 05:11:17.879220', 1, NULL),
(18, 4.875, 2.25, 49.36, 'Slick', 'NC38 (Drill Collar)', 4.875, 2.25, 'API', 1, '2021-08-19 05:11:17.884968', 1, NULL),
(19, 4.875, 2.25, 49.36, 'Spiral', 'XT39', 4.875, 2.25, 'API', 1, '2021-08-19 05:11:17.891053', 1, NULL),
(20, 6.5, 2.813, 90.61, 'Spiral', 'NC46 (Drill Collar)', 6.5, 2.813, 'API', 1, '2021-08-19 05:11:17.896649', 1, NULL),
(21, 6.5, 2.813, 90.61, 'Spiral', 'NC50 (Drill Collar)', 6.5, 2.813, 'API', 1, '2021-08-19 05:11:17.903062', 1, NULL),
(22, 6.75, 2.813, 99.35, 'Spiral', 'NC50 (Drill Collar)', 6.75, 2.813, 'API', 1, '2021-08-19 05:11:17.908719', 1, NULL),
(23, 8, 2.813, 148.01, 'Spiral', '6 5/8 Reg (Drill Collar)', 8, 2.813, 'API', 1, '2021-08-19 05:11:17.914172', 1, NULL),
(24, 8.25, 2.813, 158.73, 'Spiral', '6 5/8 Reg (Drill Collar)', 8.25, 2.813, 'API', 1, '2021-08-19 05:11:17.919416', 1, NULL),
(25, 9.5, 3, 214.41, 'Spiral', '7 5/8 Reg (Drill Collar)', 9.5, 3, 'API', 1, '2021-08-19 05:11:17.923869', 1, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `bhadata_drillpipe`
--

CREATE TABLE `bhadata_drillpipe` (
  `id` int NOT NULL,
  `normal_od` double DEFAULT NULL,
  `class_type` varchar(30) DEFAULT NULL,
  `pipebody_od` double DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `pipebody_id` double DEFAULT NULL,
  `connection_type` varchar(30) DEFAULT NULL,
  `upset` varchar(30) DEFAULT NULL,
  `tool_od` double DEFAULT NULL,
  `tool_id` double DEFAULT NULL,
  `box_length` double DEFAULT NULL,
  `pin_length` double DEFAULT NULL,
  `steel_grade` varchar(30) DEFAULT NULL,
  `unit` varchar(30) DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) DEFAULT NULL,
  `is_superadmin` int NOT NULL,
  `company_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `bhadata_drillpipe`
--

INSERT INTO `bhadata_drillpipe` (`id`, `normal_od`, `class_type`, `pipebody_od`, `weight`, `pipebody_id`, `connection_type`, `upset`, `tool_od`, `tool_id`, `box_length`, `pin_length`, `steel_grade`, `unit`, `status`, `created`, `is_superadmin`, `company_id`) VALUES
(1, 2.375, 'Class I', 2.375, 6.65, 1.815, 'MW20', 'IU', 2.5, 1.375, 15, 10, 'G-105', 'API', 1, NULL, 1, NULL),
(2, 2.875, 'Class I', 2.875, 10.4, 2.151, 'CTM26', 'EU', 3.5, 1.5, 15, 13, 'V-150', 'API', 1, NULL, 1, NULL),
(3, 2.875, 'Class I', 2.875, 10.4, 2.151, '2 7/8 HTPAC', 'IU', 3.125, 1.5, 13, 9, 'G-105', 'API', 1, NULL, 1, NULL),
(4, 2.875, 'Class I', 2.875, 10.4, 2.151, '2 7/8 HTPAC', 'EU', 3.125, 1.5, 14, 9, 'S-135', 'API', 1, NULL, 1, NULL),
(5, 2.875, 'Class I', 2.875, 10.4, 2.151, '2 7/8 AOH', 'EU', 3.875, 2.156, 11, 9, 'S-135', 'API', 1, NULL, 1, NULL),
(6, 2.875, 'Class I', 2.875, 10.4, 2.151, '2 3/8 HT-SL-H90', 'EU', 3.125, 1.975, 14, 10, 'S-135', 'API', 1, NULL, 1, NULL),
(7, 2.875, 'Class I', 2.875, 10.4, 2.151, 'NC31', 'EU', 4.125, 2, 12, 10, 'S-135', 'API', 1, NULL, 1, NULL),
(8, 2.875, 'Class I', 2.875, 10.4, 2.151, 'HT26', 'IEU*', 3.656, 1.5, 13, 9, 'S-135', 'API', 1, NULL, 1, NULL),
(9, 2.875, 'Class I', 2.875, 10.4, 2.151, 'XT27', 'EU', 3.375, 1.844, 17, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(10, 2.875, 'Class I', 2.875, 10.4, 2.151, 'WT26', 'IU', 3.375, 1.75, 10, 7, 'S-135', 'API', 1, NULL, 1, NULL),
(11, 3.5, 'Class I', 3.5, 13.3, 2.764, 'HT38', 'EU', 4.875, 2.563, 15.5, 10, 'S-135', 'API', 1, NULL, 1, NULL),
(12, 3.5, 'Class I', 3.5, 13.3, 2.764, 'NC38', 'EU', 4.875, 2.563, 12.5, 10, 'S-135', 'API', 1, NULL, 1, NULL),
(13, 3.5, 'Class I', 3.5, 13.3, 2.764, 'XT-M34', 'EU*', 4.25, 2.563, 15, 10, 'S-135', 'API', 1, NULL, 1, NULL),
(14, 3.5, 'Class I', 3.5, 13.3, 2.764, 'HT34-256 MPAC', 'EU*', 4.25, 2.563, 15.5, 10, 'S-135', 'API', 1, NULL, 1, NULL),
(15, 3.5, 'Class I', 3.5, 15.5, 2.602, 'NC38', 'EU', 4.75, 2.563, 12.5, 10, 'G-105', 'API', 1, NULL, 1, NULL),
(16, 3.5, 'Class I', 3.5, 15.5, 2.602, 'NC38', 'EU', 4.75, 2.563, 12.5, 10, 'S-135', 'API', 1, NULL, 1, NULL),
(17, 3.5, 'Class I', 3.5, 15.5, 2.602, 'NC38', 'EU', 4.875, 2.563, 12.5, 10, 'S-135', 'API', 1, NULL, 1, NULL),
(18, 3.5, 'Class I', 3.5, 15.5, 2.602, 'NC38', 'EU', 4.875, 2.438, 12.5, 10, 'S-135', 'API', 1, NULL, 1, NULL),
(19, 3.5, 'Class I', 3.5, 15.5, 2.602, 'NC38', 'EU', 5, 2.563, 16, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(20, 3.5, 'Class I', 3.5, 15.5, 2.602, 'TT380', 'EU', 4.813, 2.5, 15, 10, 'S-135', 'API', 1, NULL, 1, NULL),
(21, 4, 'Class I', 4, 14, 3.34, 'XT39', 'IU', 4.875, 2.688, 15, 12, 'CYX-105', 'API', 1, NULL, 1, NULL),
(22, 4, 'Class I', 4, 14, 3.34, 'XT39', 'IU', 4.875, 2.688, 15, 12, 'TSS-105', 'API', 1, NULL, 1, NULL),
(23, 4, 'Class I', 4, 14, 3.34, 'XT39', 'IU', 4.875, 2.688, 17, 12, 'XD-105', 'API', 1, NULL, 1, NULL),
(24, 4, 'Class I', 4, 14, 3.34, 'DS38', 'IU', 4.875, 2.438, 15, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(25, 4, 'Class I', 4, 14, 3.34, 'DS38', 'IU', 4.875, 2.438, 17, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(26, 4, 'Class I', 4, 14, 3.34, 'DS38', 'IU', 4.875, 2.438, 17, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(27, 4, 'Class I', 4, 14, 3.34, 'XT-M38', 'IU', 4.75, 2.688, 17, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(28, 4, 'Class I', 4, 14, 3.34, 'XT38', 'IU', 4.75, 2.688, 17, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(29, 4, 'Class I', 4, 14, 3.34, 'XT39', 'IU', 4.875, 2.688, 15, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(30, 4, 'Class I', 4, 14, 3.34, 'XT-M39', 'IU', 4.875, 2.688, 15, 10, 'S-135', 'API', 1, NULL, 1, NULL),
(31, 4, 'Class I', 4, 14, 3.34, 'TT390', 'IU', 4.875, 2.688, 18, 14, 'S-135', 'API', 1, NULL, 1, NULL),
(32, 4, 'Class I', 4, 14, 3.34, 'HT40', 'IU', 5, 2.688, 15, 9, 'S-135', 'API', 1, NULL, 1, NULL),
(33, 4, 'Class I', 4, 15.7, 3.24, 'CTM39', 'IU', 5, 2.688, 18, 14, 'S-135', 'API', 1, NULL, 1, NULL),
(34, 4, 'Class I', 4, 14, 3.34, 'VX40', 'IU', 5.25, 2.75, 15, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(35, 4.5, 'Class I', 4.5, 16.6, 3.826, 'NC46', 'IEU', 6.25, 3, 12, 9, 'S-135', 'API', 1, NULL, 1, NULL),
(36, 4.5, 'Class I', 4.5, 16.6, 3.826, 'NC46', 'IEU', 6.25, 2.75, 12, 9, 'S-135', 'API', 1, NULL, 1, NULL),
(37, 4.5, 'Class I', 4.5, 16.6, 3.826, 'GPDS40-130', 'IEU*', 5.25, 2.688, 17, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(38, 4.5, 'Class I', 4.5, 16.6, 3.826, 'Delta 425', 'IEU*', 5.25, 3, 15, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(39, 4.5, 'Class I', 4.5, 16.6, 3.826, 'Delta 425', 'IEU*', 5.375, 3, 17, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(40, 4.5, 'Class I', 4.5, 16.6, 3.826, 'uXT40', 'IEU', 5.25, 2.813, 17, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(41, 4.5, 'Class I', 4.5, 16.6, 3.826, 'XT-M40', 'IEU', 5.25, 2.688, 15, 10, 'S-135', 'API', 1, NULL, 1, NULL),
(42, 4.5, 'Class I', 4.5, 16.6, 3.826, 'CTM43', 'IEU', 5.25, 3.25, 18, 12, 'Z-140', 'API', 1, NULL, 1, NULL),
(43, 4.5, 'Class I', 4.5, 16.6, 3.826, 'CTM43', 'IEU', 5.25, 3.25, 17, 12, 'Z-140', 'API', 1, NULL, 1, NULL),
(44, 4.5, 'Class I', 4.5, 16.6, 3.826, 'TT485', 'IEU', 6, 3.438, 17, 12, 'V-150', 'API', 1, NULL, 1, NULL),
(45, 4.5, 'Class I', 4.5, 20, 3.64, 'XT-M40', 'IEU', 5.25, 2.688, 17, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(46, 4.5, 'Class I', 4.5, 20, 3.64, 'XT-M46', 'IEU', 6.25, 3, 17, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(47, 4.5, 'Class I', 4.5, 20, 3.64, 'TT-M485', 'EU', 6, 3.375, 15, 10, 'V-150', 'API', 1, NULL, 1, NULL),
(48, 5, 'Class I', 5, 19.5, 4.276, 'NC50', 'IEU', 6.625, 3.25, 12, 9, 'G-105', 'API', 1, NULL, 1, NULL),
(49, 5, 'Class I', 5, 19.5, 4.276, 'NC50', 'IEU', 6.625, 3.25, 12, 9, 'S-135', 'API', 1, NULL, 1, NULL),
(50, 5, 'Class I', 5, 19.5, 4.276, 'GPDS50', 'IEU', 6.625, 3.25, 17, 14, 'S-135', 'API', 1, NULL, 1, NULL),
(51, 5, 'Class I', 5, 19.5, 4.276, 'XT50', 'IEU', 6.5, 3.75, 15, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(52, 5, 'Class I', 5, 19.5, 4.276, 'XT50', 'IEU', 6.5, 3.5, 17, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(53, 5, 'Class I', 5, 19.5, 4.276, 'NC50', 'IEU', 6.625, 2.75, 12, 9, 'S-135', 'API', 1, NULL, 1, NULL),
(54, 5, 'Class I', 5, 19.5, 4.276, 'GPDS50-130', 'IEU', 6.625, 3.25, 18, 16, 'S-135', 'API', 1, NULL, 1, NULL),
(55, 5, 'Class I', 5, 19.5, 4.276, 'TT525', 'IEU', 6.5, 3.875, 15, 10, 'S-135', 'API', 1, NULL, 1, NULL),
(56, 5, 'Class I', 5, 19.5, 4.276, 'XT50', 'IEU', 6.5, 3.75, 17, 12, 'Z-140', 'API', 1, NULL, 1, NULL),
(57, 5, 'Class I', 5, 19.5, 4.276, 'Delta 527', 'IEU', 6.5, 3.75, 15, 12, 'Z-140', 'API', 1, NULL, 1, NULL),
(58, 5.5, 'Class I', 5.5, 21.9, 4.778, 'TT550', 'IEU', 6.625, 4.25, 17, 12, 'TSS-105', 'API', 1, NULL, 1, NULL),
(59, 5.5, 'Class I', 5.5, 21.9, 4.778, 'XT54', 'IEU', 6.625, 4, 15, 12, 'TSS-105', 'API', 1, NULL, 1, NULL),
(60, 5.5, 'Class I', 5.5, 21.9, 4.778, 'HT55', 'IEU', 7, 4, 15, 10, 'S-135', 'API', 1, NULL, 1, NULL),
(61, 5.5, 'Class I', 5.5, 21.9, 4.778, 'Delta 544', 'IEU', 6.625, 4, 15, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(62, 5.5, 'Class I', 5.5, 21.9, 4.778, '5 1/2 FH DSTJ', 'IEU', 7, 4, 15, 10.5, 'S-135', 'API', 1, NULL, 1, NULL),
(63, 5.5, 'Class I', 5.5, 21.9, 4.778, 'TT550', 'IEU', 6.625, 4.25, 18, 15, 'S-135', 'API', 1, NULL, 1, NULL),
(64, 5.5, 'Class I', 5.5, 21.9, 4.778, 'uGPDS55', 'IEU', 7, 4, 16, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(65, 5.5, 'Class I', 5.5, 21.9, 4.778, 'GPDS55-130', 'IEU', 7, 4, 18, 14, 'S-135', 'API', 1, NULL, 1, NULL),
(66, 5.5, 'Class I', 5.5, 21.9, 4.778, 'GPDS55-130', 'IEU', 7, 4, 15, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(67, 5.5, 'Class I', 5.5, 24.7, 4.67, 'XT54', 'IEU', 6.625, 4, 18, 12, 'HS3-125', 'API', 1, NULL, 1, NULL),
(68, 5.5, 'Class I', 5.5, 24.7, 4.67, 'XT-M57', 'IEU', 7.25, 4.25, 15, 10, 'S-135', 'API', 1, NULL, 1, NULL),
(69, 5.875, 'Class I', 5.875, 0, 5.235, 'VX57', 'IEU', 7.25, 3.875, 15, 12, 'VM-165', 'API', 1, NULL, 1, NULL),
(70, 5.875, 'Class I', 5.875, 23.4, 5.153, 'XT57', 'IEU', 7, 4.25, 18, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(71, 5.875, 'Class I', 5.875, 23.4, 5.153, 'TT585', 'IEU', 7, 4.5, 15, 10, 'S-135', 'API', 1, NULL, 1, NULL),
(72, 5.875, 'Class I', 5.875, 23.4, 5.153, 'XT57', 'IEU', 7, 4.25, 17, 12, 'Z-140', 'API', 1, NULL, 1, NULL),
(73, 5.875, 'Class I', 5.875, 23.4, 5.153, 'CTM57', 'IEU', 7, 4.25, 17, 12, 'Z-140', 'API', 1, NULL, 1, NULL),
(74, 5.875, 'Class I', 5.875, 23.4, 5.153, 'XT57', 'IEU', 7, 4.25, 15, 10, 'V-150', 'API', 1, NULL, 1, NULL),
(75, 5.875, 'Class I', 5.875, 23.4, 5.045, 'XT57', 'IEU', 7, 4.25, 17, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(76, 5.875, 'Class I', 5.875, 23.4, 5.045, 'TT585', 'IEU', 7, 4.5, 17, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(77, 5.875, 'Class I', 5.875, 23.4, 5.045, 'XT-M57', 'IEU', 7, 4.25, 15, 10, 'S-135', 'API', 1, NULL, 1, NULL),
(78, 5.875, 'Class I', 5.875, 23.4, 5.045, 'TT585', 'IEU', 7, 4.25, 17, 12, 'S-135', 'API', 1, NULL, 1, NULL),
(79, 5.875, 'Class I', 5.875, 23.4, 5.045, 'CTM57', 'IEU', 7, 4.25, 18, 14, 'Z-140', 'API', 1, NULL, 1, NULL),
(80, 5.875, 'Class I', 5.875, 23.4, 5.045, 'CTM57', 'IEU', 7, 4.25, 18, 14, 'V-150', 'API', 1, NULL, 1, NULL),
(81, 5.875, 'Class I', 5.875, 23.4, 5.045, 'CTM57', 'IEU', 7, 4.25, 18, 14, 'V-150', 'API', 1, NULL, 1, NULL),
(82, 5.875, 'Class I', 5.875, 23.4, 5.045, 'Delta 576', 'IEU', 7, 4.25, 17, 14, 'V-150', 'API', 1, NULL, 1, NULL),
(83, 5.875, 'Class I', 5.875, 28.7, 4.875, 'CTM57', 'IEU', 7, 4.25, 18, 14, 'S-135', 'API', 1, NULL, 1, NULL),
(84, 5.875, 'Class I', 5.875, 28.7, 4.875, 'CTM57', 'IEU', 7, 4.25, 18, 14, 'Z-140', 'API', 1, NULL, 1, NULL),
(85, 5.875, 'Class I', 5.875, 28.7, 4.875, 'XT-M57', 'IEU', 7, 4.25, 15, 10, 'S-135', 'API', 1, NULL, 1, NULL),
(86, 6.625, 'Class I', 6.625, 25.2, 5.965, 'VX69', 'IEU', 8.5, 5.25, 17, 12, 'VM-165', 'API', 1, NULL, 1, NULL),
(87, 6.625, 'Class I', 6.625, 27.7, 5.901, '6 5/8 FH', 'IEU', 8.5, 4.25, 14, 11, 'S-135', 'API', 1, NULL, 1, NULL),
(88, 6.625, 'Class I', 6.625, 27.7, 5.901, '6 5/8 FH', 'IEU', 8.5, 4.25, 18, 14, 'V-150', 'API', 1, NULL, 1, NULL),
(89, 6.625, 'Class I', 6.625, 27.7, 5.901, 'GPDS65-130', 'IEU', 8.5, 4.25, 18, 14, 'V-150', 'API', 1, NULL, 1, NULL),
(90, 6.625, 'Class I', 6.625, 34.02, 5.581, '6 5/8 FH', 'IEU', 8.5, 4.25, 18, 14, 'S-135', 'API', 1, NULL, 1, NULL),
(91, 6.625, 'Class I', 6.625, 34.02, 5.581, '6 5/8 FH', 'IEU', 8.5, 4.25, 18, 14, 'S-135', 'API', 1, NULL, 1, NULL),
(92, 6.625, 'Class I', 6.625, 34.02, 5.581, '6 5/8 FH', 'IEU', 8.5, 4.25, 18, 14, 'V-150', 'API', 1, NULL, 1, NULL),
(93, 6.625, 'Class I', 6.625, 34.02, 5.581, 'GPDS65-130', 'IEU', 8.5, 4.25, 18, 14, 'V-150', 'API', 1, NULL, 1, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `bhadata_drillpipehwdp`
--

CREATE TABLE `bhadata_drillpipehwdp` (
  `id` int NOT NULL,
  `nominal_od` double DEFAULT NULL,
  `class_type` varchar(30) DEFAULT NULL,
  `pipebody_od` double DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `pipebody_id` double DEFAULT NULL,
  `connection_type` varchar(30) DEFAULT NULL,
  `tool_od` double DEFAULT NULL,
  `tool_id` double DEFAULT NULL,
  `box_length` double DEFAULT NULL,
  `pin_length` double DEFAULT NULL,
  `unit` varchar(30) DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) DEFAULT NULL,
  `is_superadmin` int NOT NULL,
  `company_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `bhadata_drillpipehwdp`
--

INSERT INTO `bhadata_drillpipehwdp` (`id`, `nominal_od`, `class_type`, `pipebody_od`, `weight`, `pipebody_id`, `connection_type`, `tool_od`, `tool_id`, `box_length`, `pin_length`, `unit`, `status`, `created`, `is_superadmin`, `company_id`) VALUES
(1, 3.5, 'Class I', 3.5, 19.191, 2.25, 'NC38', 4.75, 2.25, 24, 24, 'API', 1, NULL, 1, NULL),
(2, 3.5, 'Class I', 3.5, 19.191, 2.25, 'NC38', 4.75, 2.25, 24, 24, 'API', 1, NULL, 1, NULL),
(3, 3.5, 'Class I', 3.5, 19.191, 2.25, 'NC38', 4.75, 2.25, 24, 24, 'API', 1, NULL, 1, NULL),
(4, 3.5, 'Class I', 3.5, 19.191, 2.25, 'NC38', 4.875, 2.25, 24, 24, 'API', 1, NULL, 1, NULL),
(5, 3.5, 'Class I', 3.5, 19.191, 2.25, 'NC38', 4.875, 2.375, 24, 24, 'API', 1, NULL, 1, NULL),
(6, 3.5, 'Class I', 3.5, 19.191, 2.25, 'NC38', 4.875, 2.313, 24, 24, 'API', 1, NULL, 1, NULL),
(7, 3.5, 'Class I', 3.5, 19.191, 2.25, 'NC38', 5, 2.25, 30, 30, 'API', 1, NULL, 1, NULL),
(8, 3.5, 'Class I', 3.5, 19.191, 2.25, 'HT38', 4.875, 2.25, 24, 24, 'API', 1, NULL, 1, NULL),
(9, 3.5, 'Class I', 3.5, 19.191, 2.25, 'HT38', 4.875, 2.563, 24, 24, 'API', 1, NULL, 1, NULL),
(10, 4, 'Class I', 4, 25.188, 2.563, 'XT38', 4.75, 2.563, 24, 24, 'API', 1, NULL, 1, NULL),
(11, 4, 'Class I', 4, 0, 2.563, 'TT390', 4.875, 2.563, 30, 30, 'API', 1, NULL, 1, NULL),
(12, 4, 'Class I', 4, 25.188, 2.563, 'XT39', 4.875, 2.563, 24, 24, 'API', 1, NULL, 1, NULL),
(13, 4, 'Class I', 4, 25.188, 2.563, 'XT39', 4.875, 2.563, 24, 24, 'API', 1, NULL, 1, NULL),
(14, 4, 'Class I', 4, 25.188, 2.563, 'XT39', 4.875, 2.563, 24, 24, 'API', 1, NULL, 1, NULL),
(15, 4, 'Class I', 4, 25.188, 2.563, 'XT39', 4.875, 2.563, 24, 30, 'API', 1, NULL, 1, NULL),
(16, 4, 'Class I', 4, 25.195, 2.563, 'XTM39', 5, 2.563, 24, 30, 'API', 1, NULL, 1, NULL),
(17, 4, 'Class I', 4, 25.188, 2.563, 'XT39', 5, 2.563, 24, 30, 'API', 1, NULL, 1, NULL),
(18, 4, 'Class I', 4, 25.181, 2.563, 'HT40', 5, 2.563, 24, 30, 'API', 1, NULL, 1, NULL),
(19, 4, 'Class I', 4, 25.181, 2.563, 'HT40', 5, 2.563, 24, 30, 'API', 1, NULL, 1, NULL),
(20, 4, 'Class I', 4, 25.188, 2.563, 'WT38', 5, 2.563, 24, 30, 'API', 1, NULL, 1, NULL),
(21, 4, 'Class I', 4, 25.195, 2.563, 'XTM39', 5, 2.562, 24, 30, 'API', 1, NULL, 1, NULL),
(22, 4, 'Class I', 4, 25.188, 2.563, 'XTM39', 5, 2.563, 24, 30, 'API', 1, NULL, 1, NULL),
(23, 4.5, 'Class I', 4.5, 0, 2.75, 'GPDS40', 5.25, 2.75, 27, 27, 'API', 1, NULL, 1, NULL),
(24, 4.5, 'Class I', 4.5, 0, 2.75, 'Delta425', 5.25, 2.75, 30, 30, 'API', 1, NULL, 1, NULL),
(25, 4.5, 'Class I', 4.5, 0, 2.75, 'Delta425', 2.375, 2.75, 27, 27, 'API', 1, NULL, 1, NULL),
(26, 4.5, 'Class I', 4.5, 33.876, 2.75, 'XTM40', 5.25, 2.75, 24, 24, 'API', 1, NULL, 1, NULL),
(27, 4.5, 'Class I', 4.5, 33.876, 2.75, 'TT*485', 6.25, 2.75, 24, 24, 'API', 1, NULL, 1, NULL),
(28, 4.5, 'Class I', 4.5, 34.783, 2.688, 'XTM40', 5.25, 2.688, 24, 24, 'API', 1, NULL, 1, NULL),
(29, 5, 'Class I', 5, 42.72, 3, 'XT50', 6.5, 3, 24, 24, 'API', 1, NULL, 1, NULL),
(30, 5, 'Class I', 5, 42.72, 3, 'NC50 (4-1/2 IF)', 6.5, 3, 24, 24, 'API', 1, NULL, 1, NULL),
(31, 5, 'Class I', 5, 42.72, 3, 'XT50', 6.625, 3, 24, 24, 'API', 1, NULL, 1, NULL),
(32, 5, 'Class I', 5, 42.721, 3, 'NC50 (4-1/2 IF)', 6.625, 3, 24, 24, 'API', 1, NULL, 1, NULL),
(33, 5, 'Class I', 5, 42.72, 3, 'NC50 (4-1/2 IF)', 6.625, 3.063, 24, 24, 'API', 1, NULL, 1, NULL),
(34, 5, 'Class I', 5, 42.675, 3, 'NC50 (4-1/2 IF)', 6.625, 3.063, 24, 24, 'API', 1, NULL, 1, NULL),
(35, 5, 'Class I', 5, 42.72, 3, 'NC50 (4-1/2 IF)', 6.625, 3.063, 24, 24, 'API', 1, NULL, 1, NULL),
(36, 5.5, 'Class I', 5.5, 52.566, 3.25, 'XT54', 6.625, 3.25, 24, 24, 'API', 1, NULL, 1, NULL),
(37, 5.5, 'Class I', 5.5, 52.566, 3.25, 'TT®550', 6.625, 3.25, 24, 24, 'API', 1, NULL, 1, NULL),
(38, 5.5, 'Class I', 5.5, 0, 3.25, 'Delta 544', 6.625, 3.25, 30, 30, 'API', 1, NULL, 1, NULL),
(39, 5.5, 'Class I', 5.5, 52.511, 3.25, 'HT55', 7, 4, 24, 24, 'API', 1, NULL, 1, NULL),
(40, 5.5, 'Class I', 5.5, 52.511, 3.25, 'XT57', 7, 4, 24, 24, 'API', 1, NULL, 1, NULL),
(41, 5.5, 'Class I', 5.5, 52.511, 3.25, 'HT55', 7.125, 3.313, 24, 24, 'API', 1, NULL, 1, NULL),
(42, 5.5, 'Class I', 5.5, 52.566, 3.25, 'HT55', 7.25, 3.25, 24, 24, 'API', 1, NULL, 1, NULL),
(43, 5.5, 'Class I', 5.5, 52.566, 3.25, '5-1/2 FH', 7.5, 3.313, 24, 24, 'API', 1, NULL, 1, NULL),
(44, 5.5, 'Class I', 5.5, 48.06, 3.5, '5-1/2 FH DSTJ', 7, 3.5, 24, 24, 'API', 1, NULL, 1, NULL),
(45, 5.5, 'Class I', 5.5, 38.048, 4, 'HT55', 7.125, 4, 24, 24, 'API', 1, NULL, 1, NULL),
(46, 5.5, 'Class I', 5.5, 49.385, 4, 'XT57', 7, 4, 24, 24, 'API', 1, NULL, 1, NULL),
(47, 5.875, 'Class I', 5.875, 49.385, 4, 'XT57', 7, 4, 24, 24, 'API', 1, NULL, 1, NULL),
(48, 5.875, 'Class I', 5.875, 49.437, 4, 'TT™585', 7, 4, 24, 24, 'API', 1, NULL, 1, NULL),
(49, 6.625, 'Class I', 6.625, 63.079, 4.5, '6-5/8 FH', 8.5, 4.5, 24, 24, 'API', 1, NULL, 1, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `bhadata_empirical`
--

CREATE TABLE `bhadata_empirical` (
  `id` int NOT NULL,
  `formula` varchar(255) DEFAULT NULL,
  `formula_python_text` varchar(255) DEFAULT NULL,
  `status` int NOT NULL,
  `bhadata_id` int DEFAULT NULL,
  `bhadata_element_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bhadata_pressuredroptool`
--

CREATE TABLE `bhadata_pressuredroptool` (
  `id` int NOT NULL,
  `flowrate` double DEFAULT NULL,
  `pressure_drop` double DEFAULT NULL,
  `status` int NOT NULL,
  `bhadata_id` int DEFAULT NULL,
  `bhadata_element_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bhadata_specifications`
--

CREATE TABLE `bhadata_specifications` (
  `id` int NOT NULL,
  `name` varchar(30) DEFAULT NULL,
  `specification_od` double DEFAULT NULL,
  `specification_id` double DEFAULT NULL,
  `specification_length` double DEFAULT NULL,
  `minimum_flowrate` double DEFAULT NULL,
  `maximum_flowrate` double DEFAULT NULL,
  `maximum_rpm` double DEFAULT NULL,
  `minimum_rpm` double DEFAULT NULL,
  `max_dp` double DEFAULT NULL,
  `recom_dp` double DEFAULT NULL,
  `max_wob` double DEFAULT NULL,
  `maximum_hydrostatic_pressure` double DEFAULT NULL,
  `maximum_mud_weight` double DEFAULT NULL,
  `minimum_mud_weight` double DEFAULT NULL,
  `no_load_diff_pressure` double DEFAULT NULL,
  `bhadata_id` int DEFAULT NULL,
  `bhadata_element_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bittype_names`
--

CREATE TABLE `bittype_names` (
  `id` int NOT NULL,
  `bittype_names` varchar(100) DEFAULT NULL,
  `bit_values` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `bittype_names`
--

INSERT INTO `bittype_names` (`id`, `bittype_names`, `bit_values`) VALUES
(1, 'PDC Bit', 0.95),
(2, 'Mill Tooth Bit', 1.03),
(3, 'Tri-Cone Insert', 1.03),
(4, 'Two Cone Bit', 1.03),
(5, 'Diamond Impregnated Bit', 1.03),
(6, 'Drag Bit', 1.03),
(7, 'Bi-Center Bit', 1.03),
(8, 'Core Bit', 1.03),
(9, 'Other', 1.03);

-- --------------------------------------------------------

--
-- Table structure for table `custom_auth_basecountries`
--

CREATE TABLE `custom_auth_basecountries` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `iso3` varchar(255) NOT NULL,
  `numeric_code` varchar(255) NOT NULL,
  `iso2` varchar(255) NOT NULL,
  `phonecode` varchar(255) NOT NULL,
  `capital` varchar(255) NOT NULL,
  `currency` varchar(255) NOT NULL,
  `currency_name` varchar(255) NOT NULL,
  `currency_symbol` varchar(255) NOT NULL,
  `tld` varchar(255) NOT NULL,
  `native` varchar(255) NOT NULL,
  `region` varchar(255) NOT NULL,
  `subregion` varchar(255) NOT NULL,
  `timezones` longtext NOT NULL,
  `translations` longtext NOT NULL,
  `flag` int DEFAULT NULL,
  `latitude` decimal(10,8) NOT NULL,
  `longitude` decimal(11,8) NOT NULL,
  `emoji` varchar(255) NOT NULL,
  `emojiU` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `wikiDataId` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `custom_auth_companies`
--

CREATE TABLE `custom_auth_companies` (
  `id` int NOT NULL,
  `company_name` varchar(255) NOT NULL,
  `cin` varchar(255) DEFAULT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `hydraulics` int DEFAULT NULL,
  `irocks` int DEFAULT NULL,
  `contact_no` varchar(255) NOT NULL,
  `created` datetime(6) NOT NULL,
  `type_of_license` varchar(50) DEFAULT NULL,
  `no_of_users` int NOT NULL,
  `concurrentusers` int NOT NULL,
  `server` varchar(200) NOT NULL,
  `status` int NOT NULL,
  `country_id` int DEFAULT NULL,
  `userid_id` int DEFAULT NULL,
  `end_date` varchar(100) DEFAULT NULL,
  `start_date` varchar(100) DEFAULT NULL,
  `subscription_type` varchar(100) DEFAULT NULL,
  `licence_type` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `custom_auth_companies`
--

INSERT INTO `custom_auth_companies` (`id`, `company_name`, `cin`, `first_name`, `last_name`, `email`, `hydraulics`, `irocks`, `contact_no`, `created`, `type_of_license`, `no_of_users`, `concurrentusers`, `server`, `status`, `country_id`, `userid_id`, `end_date`, `start_date`, `subscription_type`, `licence_type`) VALUES
(2, 'DOPT', 'DOP-002', 'shri', 'krishna', 'krishna.shri25@gmail.com', 0, 0, '', '2023-06-29 14:25:01.751645', NULL, 0, 0, '', 1, NULL, 11, NULL, NULL, NULL, 'CompanyPlan'),
(18, 'DOPT 1', NULL, 'Arujun', 'D', 'arujun@xmedia.in', 0, 0, '', '2023-07-31 15:41:14.246404', NULL, 5, 0, '', 1, NULL, 24, '2023-08-30', '2023-07-31', 'monthly', 'CompanyPlan'),
(19, 'AIR10', NULL, 'jagadish', 'm', 'shrjash1324@gmail.com', 0, 0, '', '2023-07-31 15:48:17.367119', NULL, 25, 0, '', 1, NULL, 25, '2023-08-30', '2023-07-31', 'monthly', 'Enterprise'),
(20, 'iwells', 'IWE-020', 'subash', 'lingam', 'subashlingam1@gmail.com', 0, 0, '', '2023-08-03 15:08:40.242443', NULL, 5, 0, '', 1, NULL, 26, '2024-08-02', '2023-08-03', 'yearly', 'CompanyPlan');

-- --------------------------------------------------------

--
-- Table structure for table `custom_auth_companypackages`
--

CREATE TABLE `custom_auth_companypackages` (
  `id` int NOT NULL,
  `concurrent_users` int NOT NULL,
  `created` datetime(6) NOT NULL,
  `status` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `user_type` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `custom_auth_companypackages`
--

INSERT INTO `custom_auth_companypackages` (`id`, `concurrent_users`, `created`, `status`, `user_id`, `user_type`) VALUES
(1, 1, '2023-07-31 15:38:53.345519', 1, 24, 'Individual'),
(2, 5, '2023-07-31 15:41:14.523997', 1, 18, 'CompanyPlan'),
(3, 25, '2023-07-31 15:48:17.377909', 1, 19, 'Enterprise'),
(4, 5, '2023-08-03 15:08:40.382345', 1, 20, 'CompanyPlan');

-- --------------------------------------------------------

--
-- Table structure for table `custom_auth_countries`
--

CREATE TABLE `custom_auth_countries` (
  `id` int NOT NULL,
  `iso` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `nicename` varchar(255) NOT NULL,
  `iso3` varchar(255) NOT NULL,
  `numcode` varchar(255) NOT NULL,
  `phonecode` varchar(255) NOT NULL,
  `created` datetime(6) NOT NULL,
  `status` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `custom_auth_countries`
--

INSERT INTO `custom_auth_countries` (`id`, `iso`, `name`, `nicename`, `iso3`, `numcode`, `phonecode`, `created`, `status`) VALUES
(1, 'AF', 'AFGHANISTAN', 'Afghanistan', 'AFG', '4', '93', '0000-00-00 00:00:00.000000', 0),
(2, 'AL', 'ALBANIA', 'Albania', 'ALB', '8', '355', '0000-00-00 00:00:00.000000', 0),
(3, 'DZ', 'ALGERIA', 'Algeria', 'DZA', '12', '213', '0000-00-00 00:00:00.000000', 0),
(4, 'AS', 'AMERICAN SAMOA', 'American Samoa', 'ASM', '16', '1684', '0000-00-00 00:00:00.000000', 0),
(5, 'AD', 'ANDORRA', 'Andorra', 'AND', '20', '376', '0000-00-00 00:00:00.000000', 0),
(6, 'AO', 'ANGOLA', 'Angola', 'AGO', '24', '244', '0000-00-00 00:00:00.000000', 0),
(7, 'AI', 'ANGUILLA', 'Anguilla', 'AIA', '660', '1264', '0000-00-00 00:00:00.000000', 0),
(8, 'AQ', 'ANTARCTICA', 'Antarctica', '', '', '0', '0000-00-00 00:00:00.000000', 0),
(9, 'AG', 'ANTIGUA AND BARBUDA', 'Antigua and Barbuda', 'ATG', '28', '1268', '0000-00-00 00:00:00.000000', 0),
(10, 'AR', 'ARGENTINA', 'Argentina', 'ARG', '32', '54', '0000-00-00 00:00:00.000000', 0),
(11, 'AM', 'ARMENIA', 'Armenia', 'ARM', '51', '374', '0000-00-00 00:00:00.000000', 0),
(12, 'AW', 'ARUBA', 'Aruba', 'ABW', '533', '297', '0000-00-00 00:00:00.000000', 0),
(13, 'AU', 'AUSTRALIA', 'Australia', 'AUS', '36', '61', '0000-00-00 00:00:00.000000', 0),
(14, 'AT', 'AUSTRIA', 'Austria', 'AUT', '40', '43', '0000-00-00 00:00:00.000000', 0),
(15, 'AZ', 'AZERBAIJAN', 'Azerbaijan', 'AZE', '31', '994', '0000-00-00 00:00:00.000000', 0),
(16, 'BS', 'BAHAMAS', 'Bahamas', 'BHS', '44', '1242', '0000-00-00 00:00:00.000000', 0),
(17, 'BH', 'BAHRAIN', 'Bahrain', 'BHR', '48', '973', '0000-00-00 00:00:00.000000', 0),
(18, 'BD', 'BANGLADESH', 'Bangladesh', 'BGD', '50', '880', '0000-00-00 00:00:00.000000', 0),
(19, 'BB', 'BARBADOS', 'Barbados', 'BRB', '52', '1246', '0000-00-00 00:00:00.000000', 0),
(20, 'BY', 'BELARUS', 'Belarus', 'BLR', '112', '375', '0000-00-00 00:00:00.000000', 0),
(21, 'BE', 'BELGIUM', 'Belgium', 'BEL', '56', '32', '0000-00-00 00:00:00.000000', 0),
(22, 'BZ', 'BELIZE', 'Belize', 'BLZ', '84', '501', '0000-00-00 00:00:00.000000', 0),
(23, 'BJ', 'BENIN', 'Benin', 'BEN', '204', '229', '0000-00-00 00:00:00.000000', 0),
(24, 'BM', 'BERMUDA', 'Bermuda', 'BMU', '60', '1441', '0000-00-00 00:00:00.000000', 0),
(25, 'BT', 'BHUTAN', 'Bhutan', 'BTN', '64', '975', '0000-00-00 00:00:00.000000', 0),
(26, 'BO', 'BOLIVIA', 'Bolivia', 'BOL', '68', '591', '0000-00-00 00:00:00.000000', 0),
(27, 'BA', 'BOSNIA AND HERZEGOVINA', 'Bosnia and Herzegovina', 'BIH', '70', '387', '0000-00-00 00:00:00.000000', 0),
(28, 'BW', 'BOTSWANA', 'Botswana', 'BWA', '72', '267', '0000-00-00 00:00:00.000000', 0),
(29, 'BV', 'BOUVET ISLAND', 'Bouvet Island', '', '', '0', '0000-00-00 00:00:00.000000', 0),
(30, 'BR', 'BRAZIL', 'Brazil', 'BRA', '76', '55', '0000-00-00 00:00:00.000000', 0),
(31, 'IO', 'BRITISH INDIAN OCEAN TERRITORY', 'British Indian Ocean Territory', '', '', '246', '0000-00-00 00:00:00.000000', 0),
(32, 'BN', 'BRUNEI DARUSSALAM', 'Brunei Darussalam', 'BRN', '96', '673', '0000-00-00 00:00:00.000000', 0),
(33, 'BG', 'BULGARIA', 'Bulgaria', 'BGR', '100', '359', '0000-00-00 00:00:00.000000', 0),
(34, 'BF', 'BURKINA FASO', 'Burkina Faso', 'BFA', '854', '226', '0000-00-00 00:00:00.000000', 0),
(35, 'BI', 'BURUNDI', 'Burundi', 'BDI', '108', '257', '0000-00-00 00:00:00.000000', 0),
(36, 'KH', 'CAMBODIA', 'Cambodia', 'KHM', '116', '855', '0000-00-00 00:00:00.000000', 0),
(37, 'CM', 'CAMEROON', 'Cameroon', 'CMR', '120', '237', '0000-00-00 00:00:00.000000', 0),
(38, 'CA', 'CANADA', 'Canada', 'CAN', '124', '1', '0000-00-00 00:00:00.000000', 0),
(39, 'CV', 'CAPE VERDE', 'Cape Verde', 'CPV', '132', '238', '0000-00-00 00:00:00.000000', 0),
(40, 'KY', 'CAYMAN ISLANDS', 'Cayman Islands', 'CYM', '136', '1345', '0000-00-00 00:00:00.000000', 0),
(41, 'CF', 'CENTRAL AFRICAN REPUBLIC', 'Central African Republic', 'CAF', '140', '236', '0000-00-00 00:00:00.000000', 0),
(42, 'TD', 'CHAD', 'Chad', 'TCD', '148', '235', '0000-00-00 00:00:00.000000', 0),
(43, 'CL', 'CHILE', 'Chile', 'CHL', '152', '56', '0000-00-00 00:00:00.000000', 0),
(44, 'CN', 'CHINA', 'China', 'CHN', '156', '86', '0000-00-00 00:00:00.000000', 0),
(45, 'CX', 'CHRISTMAS ISLAND', 'Christmas Island', '', '', '61', '0000-00-00 00:00:00.000000', 0),
(46, 'CC', 'COCOS (KEELING) ISLANDS', 'Cocos (Keeling) Islands', '', '', '672', '0000-00-00 00:00:00.000000', 0),
(47, 'CO', 'COLOMBIA', 'Colombia', 'COL', '170', '57', '0000-00-00 00:00:00.000000', 0),
(48, 'KM', 'COMOROS', 'Comoros', 'COM', '174', '269', '0000-00-00 00:00:00.000000', 0),
(49, 'CG', 'CONGO', 'Congo', 'COG', '178', '242', '0000-00-00 00:00:00.000000', 0),
(50, 'CD', 'CONGO, THE DEMOCRATIC REPUBLIC OF THE', 'Congo, the Democratic Republic of the', 'COD', '180', '242', '0000-00-00 00:00:00.000000', 0),
(51, 'CK', 'COOK ISLANDS', 'Cook Islands', 'COK', '184', '682', '0000-00-00 00:00:00.000000', 0),
(52, 'CR', 'COSTA RICA', 'Costa Rica', 'CRI', '188', '506', '0000-00-00 00:00:00.000000', 0),
(53, 'CI', 'COTE D\'IVOIRE', 'Cote D\'Ivoire', 'CIV', '384', '225', '0000-00-00 00:00:00.000000', 0),
(54, 'HR', 'CROATIA', 'Croatia', 'HRV', '191', '385', '0000-00-00 00:00:00.000000', 0),
(55, 'CU', 'CUBA', 'Cuba', 'CUB', '192', '53', '0000-00-00 00:00:00.000000', 0),
(56, 'CY', 'CYPRUS', 'Cyprus', 'CYP', '196', '357', '0000-00-00 00:00:00.000000', 0),
(57, 'CZ', 'CZECH REPUBLIC', 'Czech Republic', 'CZE', '203', '420', '0000-00-00 00:00:00.000000', 0),
(58, 'DK', 'DENMARK', 'Denmark', 'DNK', '208', '45', '0000-00-00 00:00:00.000000', 0),
(59, 'DJ', 'DJIBOUTI', 'Djibouti', 'DJI', '262', '253', '0000-00-00 00:00:00.000000', 0),
(60, 'DM', 'DOMINICA', 'Dominica', 'DMA', '212', '1767', '0000-00-00 00:00:00.000000', 0),
(61, 'DO', 'DOMINICAN REPUBLIC', 'Dominican Republic', 'DOM', '214', '1809', '0000-00-00 00:00:00.000000', 0),
(62, 'EC', 'ECUADOR', 'Ecuador', 'ECU', '218', '593', '0000-00-00 00:00:00.000000', 0),
(63, 'EG', 'EGYPT', 'Egypt', 'EGY', '818', '20', '0000-00-00 00:00:00.000000', 0),
(64, 'SV', 'EL SALVADOR', 'El Salvador', 'SLV', '222', '503', '0000-00-00 00:00:00.000000', 0),
(65, 'GQ', 'EQUATORIAL GUINEA', 'Equatorial Guinea', 'GNQ', '226', '240', '0000-00-00 00:00:00.000000', 0),
(66, 'ER', 'ERITREA', 'Eritrea', 'ERI', '232', '291', '0000-00-00 00:00:00.000000', 0),
(67, 'EE', 'ESTONIA', 'Estonia', 'EST', '233', '372', '0000-00-00 00:00:00.000000', 0),
(68, 'ET', 'ETHIOPIA', 'Ethiopia', 'ETH', '231', '251', '0000-00-00 00:00:00.000000', 0),
(69, 'FK', 'FALKLAND ISLANDS (MALVINAS)', 'Falkland Islands (Malvinas)', 'FLK', '238', '500', '0000-00-00 00:00:00.000000', 0),
(70, 'FO', 'FAROE ISLANDS', 'Faroe Islands', 'FRO', '234', '298', '0000-00-00 00:00:00.000000', 0),
(71, 'FJ', 'FIJI', 'Fiji', 'FJI', '242', '679', '0000-00-00 00:00:00.000000', 0),
(72, 'FI', 'FINLAND', 'Finland', 'FIN', '246', '358', '0000-00-00 00:00:00.000000', 0),
(73, 'FR', 'FRANCE', 'France', 'FRA', '250', '33', '0000-00-00 00:00:00.000000', 0),
(74, 'GF', 'FRENCH GUIANA', 'French Guiana', 'GUF', '254', '594', '0000-00-00 00:00:00.000000', 0),
(75, 'PF', 'FRENCH POLYNESIA', 'French Polynesia', 'PYF', '258', '689', '0000-00-00 00:00:00.000000', 0),
(76, 'TF', 'FRENCH SOUTHERN TERRITORIES', 'French Southern Territories', '', '', '0', '0000-00-00 00:00:00.000000', 0),
(77, 'GA', 'GABON', 'Gabon', 'GAB', '266', '241', '0000-00-00 00:00:00.000000', 0),
(78, 'GM', 'GAMBIA', 'Gambia', 'GMB', '270', '220', '0000-00-00 00:00:00.000000', 0),
(79, 'GE', 'GEORGIA', 'Georgia', 'GEO', '268', '995', '0000-00-00 00:00:00.000000', 0),
(80, 'DE', 'GERMANY', 'Germany', 'DEU', '276', '49', '0000-00-00 00:00:00.000000', 0),
(81, 'GH', 'GHANA', 'Ghana', 'GHA', '288', '233', '0000-00-00 00:00:00.000000', 0),
(82, 'GI', 'GIBRALTAR', 'Gibraltar', 'GIB', '292', '350', '0000-00-00 00:00:00.000000', 0),
(83, 'GR', 'GREECE', 'Greece', 'GRC', '300', '30', '0000-00-00 00:00:00.000000', 0),
(84, 'GL', 'GREENLAND', 'Greenland', 'GRL', '304', '299', '0000-00-00 00:00:00.000000', 0),
(85, 'GD', 'GRENADA', 'Grenada', 'GRD', '308', '1473', '0000-00-00 00:00:00.000000', 0),
(86, 'GP', 'GUADELOUPE', 'Guadeloupe', 'GLP', '312', '590', '0000-00-00 00:00:00.000000', 0),
(87, 'GU', 'GUAM', 'Guam', 'GUM', '316', '1671', '0000-00-00 00:00:00.000000', 0),
(88, 'GT', 'GUATEMALA', 'Guatemala', 'GTM', '320', '502', '0000-00-00 00:00:00.000000', 0),
(89, 'GN', 'GUINEA', 'Guinea', 'GIN', '324', '224', '0000-00-00 00:00:00.000000', 0),
(90, 'GW', 'GUINEA-BISSAU', 'Guinea-Bissau', 'GNB', '624', '245', '0000-00-00 00:00:00.000000', 0),
(91, 'GY', 'GUYANA', 'Guyana', 'GUY', '328', '592', '0000-00-00 00:00:00.000000', 0),
(92, 'HT', 'HAITI', 'Haiti', 'HTI', '332', '509', '0000-00-00 00:00:00.000000', 0),
(93, 'HM', 'HEARD ISLAND AND MCDONALD ISLANDS', 'Heard Island and Mcdonald Islands', '', '', '0', '0000-00-00 00:00:00.000000', 0),
(94, 'VA', 'HOLY SEE (VATICAN CITY STATE)', 'Holy See (Vatican City State)', 'VAT', '336', '39', '0000-00-00 00:00:00.000000', 0),
(95, 'HN', 'HONDURAS', 'Honduras', 'HND', '340', '504', '0000-00-00 00:00:00.000000', 0),
(96, 'HK', 'HONG KONG', 'Hong Kong', 'HKG', '344', '852', '0000-00-00 00:00:00.000000', 0),
(97, 'HU', 'HUNGARY', 'Hungary', 'HUN', '348', '36', '0000-00-00 00:00:00.000000', 0),
(98, 'IS', 'ICELAND', 'Iceland', 'ISL', '352', '354', '0000-00-00 00:00:00.000000', 0),
(99, 'IN', 'INDIA', 'India', 'IND', '356', '91', '0000-00-00 00:00:00.000000', 0),
(100, 'ID', 'INDONESIA', 'Indonesia', 'IDN', '360', '62', '0000-00-00 00:00:00.000000', 0),
(101, 'IR', 'IRAN, ISLAMIC REPUBLIC OF', 'Iran, Islamic Republic of', 'IRN', '364', '98', '0000-00-00 00:00:00.000000', 0),
(102, 'IQ', 'IRAQ', 'Iraq', 'IRQ', '368', '964', '0000-00-00 00:00:00.000000', 0),
(103, 'IE', 'IRELAND', 'Ireland', 'IRL', '372', '353', '0000-00-00 00:00:00.000000', 0),
(104, 'IL', 'ISRAEL', 'Israel', 'ISR', '376', '972', '0000-00-00 00:00:00.000000', 0),
(105, 'IT', 'ITALY', 'Italy', 'ITA', '380', '39', '0000-00-00 00:00:00.000000', 0),
(106, 'JM', 'JAMAICA', 'Jamaica', 'JAM', '388', '1876', '0000-00-00 00:00:00.000000', 0),
(107, 'JP', 'JAPAN', 'Japan', 'JPN', '392', '81', '0000-00-00 00:00:00.000000', 0),
(108, 'JO', 'JORDAN', 'Jordan', 'JOR', '400', '962', '0000-00-00 00:00:00.000000', 0),
(109, 'KZ', 'KAZAKHSTAN', 'Kazakhstan', 'KAZ', '398', '7', '0000-00-00 00:00:00.000000', 0),
(110, 'KE', 'KENYA', 'Kenya', 'KEN', '404', '254', '0000-00-00 00:00:00.000000', 0),
(111, 'KI', 'KIRIBATI', 'Kiribati', 'KIR', '296', '686', '0000-00-00 00:00:00.000000', 0),
(112, 'KP', 'KOREA, DEMOCRATIC PEOPLE\'S REPUBLIC OF', 'Korea, Democratic People\'s Republic of', 'PRK', '408', '850', '0000-00-00 00:00:00.000000', 0),
(113, 'KR', 'KOREA, REPUBLIC OF', 'Korea, Republic of', 'KOR', '410', '82', '0000-00-00 00:00:00.000000', 0),
(114, 'KW', 'KUWAIT', 'Kuwait', 'KWT', '414', '965', '0000-00-00 00:00:00.000000', 0),
(115, 'KG', 'KYRGYZSTAN', 'Kyrgyzstan', 'KGZ', '417', '996', '0000-00-00 00:00:00.000000', 0),
(116, 'LA', 'LAO PEOPLE\'S DEMOCRATIC REPUBLIC', 'Lao People\'s Democratic Republic', 'LAO', '418', '856', '0000-00-00 00:00:00.000000', 0),
(117, 'LV', 'LATVIA', 'Latvia', 'LVA', '428', '371', '0000-00-00 00:00:00.000000', 0),
(118, 'LB', 'LEBANON', 'Lebanon', 'LBN', '422', '961', '0000-00-00 00:00:00.000000', 0),
(119, 'LS', 'LESOTHO', 'Lesotho', 'LSO', '426', '266', '0000-00-00 00:00:00.000000', 0),
(120, 'LR', 'LIBERIA', 'Liberia', 'LBR', '430', '231', '0000-00-00 00:00:00.000000', 0),
(121, 'LY', 'LIBYAN ARAB JAMAHIRIYA', 'Libyan Arab Jamahiriya', 'LBY', '434', '218', '0000-00-00 00:00:00.000000', 0),
(122, 'LI', 'LIECHTENSTEIN', 'Liechtenstein', 'LIE', '438', '423', '0000-00-00 00:00:00.000000', 0),
(123, 'LT', 'LITHUANIA', 'Lithuania', 'LTU', '440', '370', '0000-00-00 00:00:00.000000', 0),
(124, 'LU', 'LUXEMBOURG', 'Luxembourg', 'LUX', '442', '352', '0000-00-00 00:00:00.000000', 0),
(125, 'MO', 'MACAO', 'Macao', 'MAC', '446', '853', '0000-00-00 00:00:00.000000', 0),
(126, 'MK', 'MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF', 'Macedonia, the Former Yugoslav Republic of', 'MKD', '807', '389', '0000-00-00 00:00:00.000000', 0),
(127, 'MG', 'MADAGASCAR', 'Madagascar', 'MDG', '450', '261', '0000-00-00 00:00:00.000000', 0),
(128, 'MW', 'MALAWI', 'Malawi', 'MWI', '454', '265', '0000-00-00 00:00:00.000000', 0),
(129, 'MY', 'MALAYSIA', 'Malaysia', 'MYS', '458', '60', '0000-00-00 00:00:00.000000', 0),
(130, 'MV', 'MALDIVES', 'Maldives', 'MDV', '462', '960', '0000-00-00 00:00:00.000000', 0),
(131, 'ML', 'MALI', 'Mali', 'MLI', '466', '223', '0000-00-00 00:00:00.000000', 0),
(132, 'MT', 'MALTA', 'Malta', 'MLT', '470', '356', '0000-00-00 00:00:00.000000', 0),
(133, 'MH', 'MARSHALL ISLANDS', 'Marshall Islands', 'MHL', '584', '692', '0000-00-00 00:00:00.000000', 0),
(134, 'MQ', 'MARTINIQUE', 'Martinique', 'MTQ', '474', '596', '0000-00-00 00:00:00.000000', 0),
(135, 'MR', 'MAURITANIA', 'Mauritania', 'MRT', '478', '222', '0000-00-00 00:00:00.000000', 0),
(136, 'MU', 'MAURITIUS', 'Mauritius', 'MUS', '480', '230', '0000-00-00 00:00:00.000000', 0),
(137, 'YT', 'MAYOTTE', 'Mayotte', '', '', '269', '0000-00-00 00:00:00.000000', 0),
(138, 'MX', 'MEXICO', 'Mexico', 'MEX', '484', '52', '0000-00-00 00:00:00.000000', 0),
(139, 'FM', 'MICRONESIA, FEDERATED STATES OF', 'Micronesia, Federated States of', 'FSM', '583', '691', '0000-00-00 00:00:00.000000', 0),
(140, 'MD', 'MOLDOVA, REPUBLIC OF', 'Moldova, Republic of', 'MDA', '498', '373', '0000-00-00 00:00:00.000000', 0),
(141, 'MC', 'MONACO', 'Monaco', 'MCO', '492', '377', '0000-00-00 00:00:00.000000', 0),
(142, 'MN', 'MONGOLIA', 'Mongolia', 'MNG', '496', '976', '0000-00-00 00:00:00.000000', 0),
(143, 'MS', 'MONTSERRAT', 'Montserrat', 'MSR', '500', '1664', '0000-00-00 00:00:00.000000', 0),
(144, 'MA', 'MOROCCO', 'Morocco', 'MAR', '504', '212', '0000-00-00 00:00:00.000000', 0),
(145, 'MZ', 'MOZAMBIQUE', 'Mozambique', 'MOZ', '508', '258', '0000-00-00 00:00:00.000000', 0),
(146, 'MM', 'MYANMAR', 'Myanmar', 'MMR', '104', '95', '0000-00-00 00:00:00.000000', 0),
(147, 'NA', 'NAMIBIA', 'Namibia', 'NAM', '516', '264', '0000-00-00 00:00:00.000000', 0),
(148, 'NR', 'NAURU', 'Nauru', 'NRU', '520', '674', '0000-00-00 00:00:00.000000', 0),
(149, 'NP', 'NEPAL', 'Nepal', 'NPL', '524', '977', '0000-00-00 00:00:00.000000', 0),
(150, 'NL', 'NETHERLANDS', 'Netherlands', 'NLD', '528', '31', '0000-00-00 00:00:00.000000', 0),
(151, 'AN', 'NETHERLANDS ANTILLES', 'Netherlands Antilles', 'ANT', '530', '599', '0000-00-00 00:00:00.000000', 0),
(152, 'NC', 'NEW CALEDONIA', 'New Caledonia', 'NCL', '540', '687', '0000-00-00 00:00:00.000000', 0),
(153, 'NZ', 'NEW ZEALAND', 'New Zealand', 'NZL', '554', '64', '0000-00-00 00:00:00.000000', 0),
(154, 'NI', 'NICARAGUA', 'Nicaragua', 'NIC', '558', '505', '0000-00-00 00:00:00.000000', 0),
(155, 'NE', 'NIGER', 'Niger', 'NER', '562', '227', '0000-00-00 00:00:00.000000', 0),
(156, 'NG', 'NIGERIA', 'Nigeria', 'NGA', '566', '234', '0000-00-00 00:00:00.000000', 0),
(157, 'NU', 'NIUE', 'Niue', 'NIU', '570', '683', '0000-00-00 00:00:00.000000', 0),
(158, 'NF', 'NORFOLK ISLAND', 'Norfolk Island', 'NFK', '574', '672', '0000-00-00 00:00:00.000000', 0),
(159, 'MP', 'NORTHERN MARIANA ISLANDS', 'Northern Mariana Islands', 'MNP', '580', '1670', '0000-00-00 00:00:00.000000', 0),
(160, 'NO', 'NORWAY', 'Norway', 'NOR', '578', '47', '0000-00-00 00:00:00.000000', 0),
(161, 'OM', 'OMAN', 'Oman', 'OMN', '512', '968', '0000-00-00 00:00:00.000000', 0),
(162, 'PK', 'PAKISTAN', 'Pakistan', 'PAK', '586', '92', '0000-00-00 00:00:00.000000', 0),
(163, 'PW', 'PALAU', 'Palau', 'PLW', '585', '680', '0000-00-00 00:00:00.000000', 0),
(164, 'PS', 'PALESTINIAN TERRITORY, OCCUPIED', 'Palestinian Territory, Occupied', '', '', '970', '0000-00-00 00:00:00.000000', 0),
(165, 'PA', 'PANAMA', 'Panama', 'PAN', '591', '507', '0000-00-00 00:00:00.000000', 0),
(166, 'PG', 'PAPUA NEW GUINEA', 'Papua New Guinea', 'PNG', '598', '675', '0000-00-00 00:00:00.000000', 0),
(167, 'PY', 'PARAGUAY', 'Paraguay', 'PRY', '600', '595', '0000-00-00 00:00:00.000000', 0),
(168, 'PE', 'PERU', 'Peru', 'PER', '604', '51', '0000-00-00 00:00:00.000000', 0),
(169, 'PH', 'PHILIPPINES', 'Philippines', 'PHL', '608', '63', '0000-00-00 00:00:00.000000', 0),
(170, 'PN', 'PITCAIRN', 'Pitcairn', 'PCN', '612', '0', '0000-00-00 00:00:00.000000', 0),
(171, 'PL', 'POLAND', 'Poland', 'POL', '616', '48', '0000-00-00 00:00:00.000000', 0),
(172, 'PT', 'PORTUGAL', 'Portugal', 'PRT', '620', '351', '0000-00-00 00:00:00.000000', 0),
(173, 'PR', 'PUERTO RICO', 'Puerto Rico', 'PRI', '630', '1787', '0000-00-00 00:00:00.000000', 0),
(174, 'QA', 'QATAR', 'Qatar', 'QAT', '634', '974', '0000-00-00 00:00:00.000000', 0),
(175, 'RE', 'REUNION', 'Reunion', 'REU', '638', '262', '0000-00-00 00:00:00.000000', 0),
(176, 'RO', 'ROMANIA', 'Romania', 'ROM', '642', '40', '0000-00-00 00:00:00.000000', 0),
(177, 'RU', 'RUSSIAN FEDERATION', 'Russian Federation', 'RUS', '643', '70', '0000-00-00 00:00:00.000000', 0),
(178, 'RW', 'RWANDA', 'Rwanda', 'RWA', '646', '250', '0000-00-00 00:00:00.000000', 0),
(179, 'SH', 'SAINT HELENA', 'Saint Helena', 'SHN', '654', '290', '0000-00-00 00:00:00.000000', 0),
(180, 'KN', 'SAINT KITTS AND NEVIS', 'Saint Kitts and Nevis', 'KNA', '659', '1869', '0000-00-00 00:00:00.000000', 0),
(181, 'LC', 'SAINT LUCIA', 'Saint Lucia', 'LCA', '662', '1758', '0000-00-00 00:00:00.000000', 0),
(182, 'PM', 'SAINT PIERRE AND MIQUELON', 'Saint Pierre and Miquelon', 'SPM', '666', '508', '0000-00-00 00:00:00.000000', 0),
(183, 'VC', 'SAINT VINCENT AND THE GRENADINES', 'Saint Vincent and the Grenadines', 'VCT', '670', '1784', '0000-00-00 00:00:00.000000', 0),
(184, 'WS', 'SAMOA', 'Samoa', 'WSM', '882', '684', '0000-00-00 00:00:00.000000', 0),
(185, 'SM', 'SAN MARINO', 'San Marino', 'SMR', '674', '378', '0000-00-00 00:00:00.000000', 0),
(186, 'ST', 'SAO TOME AND PRINCIPE', 'Sao Tome and Principe', 'STP', '678', '239', '0000-00-00 00:00:00.000000', 0),
(187, 'SA', 'SAUDI ARABIA', 'Saudi Arabia', 'SAU', '682', '966', '0000-00-00 00:00:00.000000', 0),
(188, 'SN', 'SENEGAL', 'Senegal', 'SEN', '686', '221', '0000-00-00 00:00:00.000000', 0),
(189, 'CS', 'SERBIA AND MONTENEGRO', 'Serbia and Montenegro', '', '', '381', '0000-00-00 00:00:00.000000', 0),
(190, 'SC', 'SEYCHELLES', 'Seychelles', 'SYC', '690', '248', '0000-00-00 00:00:00.000000', 0),
(191, 'SL', 'SIERRA LEONE', 'Sierra Leone', 'SLE', '694', '232', '0000-00-00 00:00:00.000000', 0),
(192, 'SG', 'SINGAPORE', 'Singapore', 'SGP', '702', '65', '0000-00-00 00:00:00.000000', 0),
(193, 'SK', 'SLOVAKIA', 'Slovakia', 'SVK', '703', '421', '0000-00-00 00:00:00.000000', 0),
(194, 'SI', 'SLOVENIA', 'Slovenia', 'SVN', '705', '386', '0000-00-00 00:00:00.000000', 0),
(195, 'SB', 'SOLOMON ISLANDS', 'Solomon Islands', 'SLB', '90', '677', '0000-00-00 00:00:00.000000', 0),
(196, 'SO', 'SOMALIA', 'Somalia', 'SOM', '706', '252', '0000-00-00 00:00:00.000000', 0),
(197, 'ZA', 'SOUTH AFRICA', 'South Africa', 'ZAF', '710', '27', '0000-00-00 00:00:00.000000', 0),
(198, 'GS', 'SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS', 'South Georgia and the South Sandwich Islands', '', '', '0', '0000-00-00 00:00:00.000000', 0),
(199, 'ES', 'SPAIN', 'Spain', 'ESP', '724', '34', '0000-00-00 00:00:00.000000', 0),
(200, 'LK', 'SRI LANKA', 'Sri Lanka', 'LKA', '144', '94', '0000-00-00 00:00:00.000000', 0),
(201, 'SD', 'SUDAN', 'Sudan', 'SDN', '736', '249', '0000-00-00 00:00:00.000000', 0),
(202, 'SR', 'SURINAME', 'Suriname', 'SUR', '740', '597', '0000-00-00 00:00:00.000000', 0),
(203, 'SJ', 'SVALBARD AND JAN MAYEN', 'Svalbard and Jan Mayen', 'SJM', '744', '47', '0000-00-00 00:00:00.000000', 0),
(204, 'SZ', 'SWAZILAND', 'Swaziland', 'SWZ', '748', '268', '0000-00-00 00:00:00.000000', 0),
(205, 'SE', 'SWEDEN', 'Sweden', 'SWE', '752', '46', '0000-00-00 00:00:00.000000', 0),
(206, 'CH', 'SWITZERLAND', 'Switzerland', 'CHE', '756', '41', '0000-00-00 00:00:00.000000', 0),
(207, 'SY', 'SYRIAN ARAB REPUBLIC', 'Syrian Arab Republic', 'SYR', '760', '963', '0000-00-00 00:00:00.000000', 0),
(208, 'TW', 'TAIWAN, PROVINCE OF CHINA', 'Taiwan, Province of China', 'TWN', '158', '886', '0000-00-00 00:00:00.000000', 0),
(209, 'TJ', 'TAJIKISTAN', 'Tajikistan', 'TJK', '762', '992', '0000-00-00 00:00:00.000000', 0),
(210, 'TZ', 'TANZANIA, UNITED REPUBLIC OF', 'Tanzania, United Republic of', 'TZA', '834', '255', '0000-00-00 00:00:00.000000', 0),
(211, 'TH', 'THAILAND', 'Thailand', 'THA', '764', '66', '0000-00-00 00:00:00.000000', 0),
(212, 'TL', 'TIMOR-LESTE', 'Timor-Leste', '', '', '670', '0000-00-00 00:00:00.000000', 0),
(213, 'TG', 'TOGO', 'Togo', 'TGO', '768', '228', '0000-00-00 00:00:00.000000', 0),
(214, 'TK', 'TOKELAU', 'Tokelau', 'TKL', '772', '690', '0000-00-00 00:00:00.000000', 0),
(215, 'TO', 'TONGA', 'Tonga', 'TON', '776', '676', '0000-00-00 00:00:00.000000', 0),
(216, 'TT', 'TRINIDAD AND TOBAGO', 'Trinidad and Tobago', 'TTO', '780', '1868', '0000-00-00 00:00:00.000000', 0),
(217, 'TN', 'TUNISIA', 'Tunisia', 'TUN', '788', '216', '0000-00-00 00:00:00.000000', 0),
(218, 'TR', 'TURKEY', 'Turkey', 'TUR', '792', '90', '0000-00-00 00:00:00.000000', 0),
(219, 'TM', 'TURKMENISTAN', 'Turkmenistan', 'TKM', '795', '7370', '0000-00-00 00:00:00.000000', 0),
(220, 'TC', 'TURKS AND CAICOS ISLANDS', 'Turks and Caicos Islands', 'TCA', '796', '1649', '0000-00-00 00:00:00.000000', 0),
(221, 'TV', 'TUVALU', 'Tuvalu', 'TUV', '798', '688', '0000-00-00 00:00:00.000000', 0),
(222, 'UG', 'UGANDA', 'Uganda', 'UGA', '800', '256', '0000-00-00 00:00:00.000000', 0),
(223, 'UA', 'UKRAINE', 'Ukraine', 'UKR', '804', '380', '0000-00-00 00:00:00.000000', 0),
(224, 'AE', 'UNITED ARAB EMIRATES', 'United Arab Emirates', 'ARE', '784', '971', '0000-00-00 00:00:00.000000', 0),
(225, 'GB', 'UNITED KINGDOM', 'United Kingdom', 'GBR', '826', '44', '0000-00-00 00:00:00.000000', 0),
(226, 'US', 'UNITED STATES', 'United States', 'USA', '840', '1', '0000-00-00 00:00:00.000000', 0),
(227, 'UM', 'UNITED STATES MINOR OUTLYING ISLANDS', 'United States Minor Outlying Islands', '', '', '1', '0000-00-00 00:00:00.000000', 0),
(228, 'UY', 'URUGUAY', 'Uruguay', 'URY', '858', '598', '0000-00-00 00:00:00.000000', 0),
(229, 'UZ', 'UZBEKISTAN', 'Uzbekistan', 'UZB', '860', '998', '0000-00-00 00:00:00.000000', 0),
(230, 'VU', 'VANUATU', 'Vanuatu', 'VUT', '548', '678', '0000-00-00 00:00:00.000000', 0),
(231, 'VE', 'VENEZUELA', 'Venezuela', 'VEN', '862', '58', '0000-00-00 00:00:00.000000', 0),
(232, 'VN', 'VIET NAM', 'Viet Nam', 'VNM', '704', '84', '0000-00-00 00:00:00.000000', 0),
(233, 'VG', 'VIRGIN ISLANDS, BRITISH', 'Virgin Islands, British', 'VGB', '92', '1284', '0000-00-00 00:00:00.000000', 0),
(234, 'VI', 'VIRGIN ISLANDS, U.S.', 'Virgin Islands, U.s.', 'VIR', '850', '1340', '0000-00-00 00:00:00.000000', 0),
(235, 'WF', 'WALLIS AND FUTUNA', 'Wallis and Futuna', 'WLF', '876', '681', '0000-00-00 00:00:00.000000', 0),
(236, 'EH', 'WESTERN SAHARA', 'Western Sahara', 'ESH', '732', '212', '0000-00-00 00:00:00.000000', 0),
(237, 'YE', 'YEMEN', 'Yemen', 'YEM', '887', '967', '0000-00-00 00:00:00.000000', 0),
(238, 'ZM', 'ZAMBIA', 'Zambia', 'ZMB', '894', '260', '0000-00-00 00:00:00.000000', 0),
(239, 'ZW', 'ZIMBABWE', 'Zimbabwe', 'ZWE', '716', '263', '0000-00-00 00:00:00.000000', 0);

-- --------------------------------------------------------

--
-- Table structure for table `custom_auth_packageconcurrentusers`
--

CREATE TABLE `custom_auth_packageconcurrentusers` (
  `id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `concurrent_users` int NOT NULL,
  `created` datetime(6) NOT NULL,
  `status` int NOT NULL,
  `package_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `custom_auth_packageconcurrentusers`
--

INSERT INTO `custom_auth_packageconcurrentusers` (`id`, `name`, `concurrent_users`, `created`, `status`, `package_id`) VALUES
(1, 'One Concurrent User', 1, '2021-05-06 00:07:32.000000', 1, 1),
(2, '2 concurrent users', 2, '2021-05-06 00:07:32.000000', 1, 2),
(3, '5 concurrent users', 5, '2021-05-06 00:07:32.000000', 1, 2),
(4, '10 concurrent users', 10, '2021-05-06 00:07:32.000000', 1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `custom_auth_packages`
--

CREATE TABLE `custom_auth_packages` (
  `id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `types` varchar(50) NOT NULL,
  `created` datetime(6) NOT NULL,
  `status` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `custom_auth_packages`
--

INSERT INTO `custom_auth_packages` (`id`, `name`, `types`, `created`, `status`) VALUES
(1, 'Perpetual', 'predefined', '2021-05-06 00:07:32.000000', 1),
(2, 'Corporate Yearly', 'predefined', '2021-05-06 00:07:32.000000', 1);

-- --------------------------------------------------------

--
-- Table structure for table `custom_auth_packageusers`
--

CREATE TABLE `custom_auth_packageusers` (
  `id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `concurrent_users` int NOT NULL,
  `admins` int NOT NULL,
  `well_managers` int NOT NULL,
  `well_engineers` int NOT NULL,
  `other_users` int NOT NULL,
  `created` datetime(6) NOT NULL,
  `status` int NOT NULL,
  `package_concurrent_users_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `custom_auth_packageusers`
--

INSERT INTO `custom_auth_packageusers` (`id`, `name`, `concurrent_users`, `admins`, `well_managers`, `well_engineers`, `other_users`, `created`, `status`, `package_concurrent_users_id`) VALUES
(1, 'one', 1, 1, 2, 3, 4, '2021-05-06 00:07:32.000000', 1, 1),
(2, 'two', 2, 1, 5, 5, 10, '2021-05-06 00:07:32.000000', 1, 2),
(3, 'three', 5, 1, 5, 5, 10, '2021-05-06 00:07:32.000000', 1, 3),
(4, 'four', 10, 1, 10, 10, 20, '2021-05-06 00:07:32.000000', 1, 4);

-- --------------------------------------------------------

--
-- Table structure for table `custom_auth_payments`
--

CREATE TABLE `custom_auth_payments` (
  `id` int NOT NULL,
  `amount` int NOT NULL,
  `currency` varchar(255) NOT NULL,
  `licensekey` varchar(255) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `payment_status` int NOT NULL,
  `transaction_id` varchar(100) DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `user_type` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `custom_auth_payments`
--

INSERT INTO `custom_auth_payments` (`id`, `amount`, `currency`, `licensekey`, `date`, `payment_status`, `transaction_id`, `user_id`, `user_type`) VALUES
(1, 50, '', NULL, NULL, 0, 'cs_test_a1aPMGGqg5qRpetJsj96A9jknvtVaWvKMTaaawEyZjxejIiuc7H6txpRZP', 24, 'Individual'),
(2, 350, '', NULL, NULL, 0, 'cs_test_a1lHkASPFAc7vYyxWBqRRnNs9hFukpw3Px6HOQumZDZV7yexxxLnea0bji', 18, 'CompanyPlan'),
(3, 250, '', NULL, NULL, 0, 'cs_test_a1MqRHwj7Y4aANwlS4lQb5DbFX80gtUUb1v2Mwmt7gCZkbOKUOe7Wfkxk0', 20, 'CompanyPlan');

-- --------------------------------------------------------

--
-- Table structure for table `custom_auth_user`
--

CREATE TABLE `custom_auth_user` (
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `id` int NOT NULL,
  `title` varchar(15) DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  `name` varchar(50) NOT NULL,
  `lastname` varchar(50) DEFAULT NULL,
  `designation` varchar(50) DEFAULT NULL,
  `is_superadmin` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `licence_type` varchar(50) DEFAULT NULL,
  `company_id` int DEFAULT NULL,
  `end_date` varchar(100) DEFAULT NULL,
  `start_date` varchar(100) DEFAULT NULL,
  `subscription_type` varchar(100) DEFAULT NULL,
  `is_loggedin` tinyint(1) NOT NULL,
  `individual_id` int DEFAULT NULL,
  `is_admin` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `custom_auth_user`
--

INSERT INTO `custom_auth_user` (`password`, `last_login`, `is_superuser`, `id`, `title`, `email`, `name`, `lastname`, `designation`, `is_superadmin`, `is_active`, `is_staff`, `licence_type`, `company_id`, `end_date`, `start_date`, `subscription_type`, `is_loggedin`, `individual_id`, `is_admin`) VALUES
('pbkdf2_sha256$260000$3gIFclPLhQDMhHz3m4iyOo$Pas/TKINJTZlNMRCNZZ+0AbKkkqgRxckJynrqnruKK8=', '2023-08-04 10:09:39.904719', 1, 1, NULL, 'admin@dopt.com', 'admin', NULL, NULL, 1, 1, 1, NULL, NULL, NULL, NULL, NULL, 0, NULL, 0),
('pbkdf2_sha256$260000$k7YI1DRqeQbANF7UHHZjVZ$A2JCfE5Nrm4c1UEczql9KMOQ9+cukiKmIgnt8Pq5Zj0=', '2023-08-03 18:12:19.705299', 0, 11, 'Mr', 'krishna.shri25@gmail.com', 'shri', 'krishna', 'well manager', 0, 1, 1, 'CompanyPlan', 2, NULL, NULL, NULL, 1, NULL, 0),
('pbkdf2_sha256$260000$ZfiTQOBQfo4FWCdmkjVU85$4dsmqosLopTmD3RXpMm1kdJheX6RRwHOY1fMSf6sVl8=', '2023-08-03 11:59:39.486318', 0, 15, 'Mr', 'iwellsmc@outlook.com', 'Iwells', 'Outlook', NULL, 0, 1, 1, 'Individual', NULL, '2023-08-02', '2023-07-03', 'yearly', 0, NULL, 0),
('pbkdf2_sha256$260000$Yk1VEkpmK3nxLUULic0tWa$Pmuns3/DxlU4j0T7nV/JZvbtSqa/jt5BeiRSxd/cf8Q=', '2023-08-04 10:10:29.073850', 0, 24, 'Mr', 'arujun@xmedia.in', 'Arujun', 'D', 'Manager', 0, 1, 1, 'CompanyPlan', 18, '2023-08-30', '2023-07-31', 'monthly', 1, 24, 1),
('pbkdf2_sha256$260000$Jdg93K3zukQcFbwBUjxDIz$OS2W2a3iDd5kMSLoDainRI0Dhfk3fCvCvxjDQsjZCTQ=', NULL, 0, 25, 'Mr', 'shrjash1324@gmail.com', 'jagadish', 'm', 'Admin User', 0, 1, 1, 'Enterprise', 19, '2023-08-30', '2023-07-31', 'monthly', 0, NULL, 0),
('pbkdf2_sha256$260000$u8M4sETcmtrlb0MrLfHyeB$02XBKoybzKEpaZ+BFCxHQNZ6cDEr1F6jS5+4aTteMxQ=', '2023-08-03 15:11:56.639147', 0, 26, 'Mr', 'subashlingam1@gmail.com', 'subash', 'lingam', 'admin', 0, 1, 1, 'CompanyPlan', 20, '2024-08-02', '2023-08-03', 'yearly', 1, NULL, 1);

-- --------------------------------------------------------

--
-- Table structure for table `custom_auth_user_groups`
--

CREATE TABLE `custom_auth_user_groups` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `custom_auth_user_groups`
--

INSERT INTO `custom_auth_user_groups` (`id`, `user_id`, `group_id`) VALUES
(1, 11, 1),
(18, 16, 1),
(19, 17, 1),
(20, 18, 1),
(21, 19, 1),
(22, 20, 1),
(23, 21, 2),
(24, 22, 1),
(25, 23, 2),
(2, 24, 1),
(27, 25, 1),
(28, 26, 1),
(3, 27, 1),
(4, 28, 1),
(6, 31, 1),
(7, 32, 1),
(8, 36, 1),
(9, 37, 1),
(10, 38, 1),
(15, 44, 1),
(16, 45, 1),
(17, 49, 1);

-- --------------------------------------------------------

--
-- Table structure for table `custom_auth_user_user_permissions`
--

CREATE TABLE `custom_auth_user_user_permissions` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL
) ;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(71, 'admin', 'logentry'),
(2, 'auth', 'group'),
(1, 'auth', 'permission'),
(66, 'bhadata', 'bhadata'),
(67, 'bhadata', 'bhaelement'),
(65, 'bhadata', 'differential_pressure'),
(60, 'bhadata', 'drillcollers'),
(59, 'bhadata', 'drillpipe'),
(61, 'bhadata', 'drillpipehwdp'),
(64, 'bhadata', 'empirical'),
(63, 'bhadata', 'pressuredroptool'),
(62, 'bhadata', 'specifications'),
(3, 'contenttypes', 'contenttype'),
(5, 'custom_auth', 'basecountries'),
(6, 'custom_auth', 'companies'),
(16, 'custom_auth', 'companypackages'),
(7, 'custom_auth', 'countries'),
(8, 'custom_auth', 'enquiry'),
(9, 'custom_auth', 'modules'),
(10, 'custom_auth', 'packageconcurrentusers'),
(11, 'custom_auth', 'packages'),
(15, 'custom_auth', 'packageusers'),
(14, 'custom_auth', 'payments'),
(72, 'custom_auth', 'querymodel'),
(13, 'custom_auth', 'rights'),
(4, 'custom_auth', 'user'),
(12, 'custom_auth', 'userlog'),
(57, 'drillbitdata', 'bittypesnames'),
(56, 'drillbitdata', 'drillbit'),
(58, 'drillbitdata', 'drillbitnozzle'),
(74, 'license', 'licensepackage'),
(27, 'mud', 'mudpump'),
(30, 'mud', 'mudpumpdata'),
(29, 'mud', 'mudpumpflowrate'),
(35, 'mud', 'mudpumpmasterdata'),
(34, 'mud', 'mudpumpmasterflowrate'),
(33, 'mud', 'mudpumpmasterspeed'),
(28, 'mud', 'mudpumpspeed'),
(31, 'mud', 'pumpmanufacturer'),
(32, 'mud', 'pumps'),
(54, 'muddata', 'hydraulicdata'),
(46, 'muddata', 'muddata'),
(47, 'muddata', 'mudtype'),
(55, 'muddata', 'planwell_data'),
(49, 'muddata', 'pressureloss_data'),
(50, 'muddata', 'rheogram'),
(52, 'muddata', 'rheogramdate'),
(51, 'muddata', 'rheogramnamemodels'),
(53, 'muddata', 'rheogramsections'),
(48, 'muddata', 'sections'),
(70, 'notifications', 'notification'),
(39, 'pressure', 'pressure'),
(20, 'projects', 'projectblock'),
(21, 'projects', 'projectfield'),
(17, 'projects', 'projects'),
(19, 'projects', 'projectuserrights'),
(22, 'projects', 'projectusers'),
(18, 'projects', 'userrights'),
(68, 'rig', 'rig'),
(69, 'sessions', 'session'),
(36, 'surfacepipe', 'surfacenamemodels'),
(38, 'surfacepipe', 'surfacepipe'),
(37, 'surfacepipe', 'surfacepipedata'),
(73, 'ticket', 'tickets'),
(44, 'wellphases', 'casing'),
(42, 'wellphases', 'casinggrade'),
(43, 'wellphases', 'casingrange'),
(41, 'wellphases', 'casingtypes'),
(40, 'wellphases', 'wellphases'),
(23, 'wells', 'coordinatesystems'),
(24, 'wells', 'projections'),
(25, 'wells', 'wells'),
(26, 'wells', 'wellusers'),
(45, 'welltrajectory', 'welltrajectory');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2023-07-29 10:20:24.799189'),
(2, 'contenttypes', '0002_remove_content_type_name', '2023-07-29 10:20:24.823010'),
(3, 'auth', '0001_initial', '2023-07-29 10:20:24.846417'),
(4, 'auth', '0002_alter_permission_name_max_length', '2023-07-29 10:20:24.880396'),
(5, 'auth', '0003_alter_user_email_max_length', '2023-07-29 10:20:24.889787'),
(6, 'auth', '0004_alter_user_username_opts', '2023-07-29 10:20:24.899977'),
(7, 'auth', '0005_alter_user_last_login_null', '2023-07-29 10:20:24.952533'),
(8, 'auth', '0006_require_contenttypes_0002', '2023-07-29 10:20:24.974030'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2023-07-29 10:20:25.005916'),
(10, 'auth', '0008_alter_user_username_max_length', '2023-07-29 10:20:25.016513'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2023-07-29 10:20:25.124591'),
(12, 'auth', '0010_alter_group_name_max_length', '2023-07-29 10:20:25.135990'),
(13, 'auth', '0011_update_proxy_permissions', '2023-07-29 10:20:25.154273'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2023-07-29 10:20:25.162941'),
(15, 'custom_auth', '0001_initial', '2023-07-29 10:20:25.170725'),
(16, 'custom_auth', '0002_auto_20230729_1024', '2023-07-29 10:24:10.936562'),
(17, 'admin', '0001_initial', '2023-07-29 10:28:14.418315'),
(18, 'admin', '0002_logentry_remove_auto_add', '2023-07-29 10:28:14.493167'),
(19, 'admin', '0003_logentry_add_action_flag_choices', '2023-07-29 10:28:14.860923'),
(20, 'notifications', '0001_initial', '2023-07-29 10:29:32.541521'),
(21, 'notifications', '0002_auto_20150224_1134', '2023-07-29 10:29:32.609823'),
(22, 'notifications', '0003_notification_data', '2023-07-29 10:29:32.621230'),
(23, 'notifications', '0004_auto_20150826_1508', '2023-07-29 10:29:32.886503'),
(24, 'notifications', '0005_auto_20160504_1520', '2023-07-29 10:29:32.919538'),
(25, 'notifications', '0006_indexes', '2023-07-29 10:29:32.929670'),
(26, 'notifications', '0007_add_timestamp_index', '2023-07-29 10:29:32.940600'),
(27, 'notifications', '0008_index_together_recipient_unread', '2023-07-29 10:29:33.017470'),
(28, 'sessions', '0001_initial', '2023-07-29 10:30:28.458978'),
(29, 'custom_auth', '0003_auto_20230729_1036', '2023-07-29 10:36:43.740897'),
(30, 'custom_auth', '0004_auto_20230803_1840', '2023-08-03 18:40:32.635774');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('2mmj7p057n6ehzro7hfiioir91jgpguz', '.eJxVkMFuwyAQRP-Fc2RhO64ht1btoVJT9dibtSwQkxCwbFBlVf33riMqpbfdebODmG82QE7jkBczD06zA6s5292LCvBiwkb0GcIpVhhDmp2qNktV6FIdozb-qXj_BYywjHQtpBBct00nZMMfLMrWwr4XEnFfW6s6rlDzWmjk0MmuVwi25bVByWUDPVcU-mW8nyjOJFDsUO_YFVy4mpApfprj2WBaiq2o2zho8jv_R26_pNscXCLH8fXz5bmgtE6GpI-3x3dSlqzuUtIMW36cV0IYM3WwEpKS1vL2Vh5tyke8lNk642-lsp9fIKt1DA:1qEP97:0X0Y4xTp92oZ6j6wzjWUQSefOC_l7nGArKzQqwuPSRI', '2023-07-12 12:29:21.598799'),
('3etgzmhjnh0nsdsc0f2hgibx3y2a8qfu', '.eJxVjEEOgjAQRe_SNWmA0g5l6d4zkGlnlGothkJcGO9uSVjo9v_33luMuK3TuGVexkBiEKoX1e_o0N857Q_dMF1n6ee0LsHJHZHHm-V5Jo6ng_0LTJinYvdeWzbKE9Xa1tQBIykwxGRbAoOg6aKd4bbp-tpAo9gUBQAUFwZsib44xmfJ8YpODE0lHhjSg9NW8jF4TpnF5wto-UU5:1qNnyf:uejS4wsiHPaSRnBRhcq7etvfuyZPaOP9jOnVmc3PiPU', '2023-08-07 10:49:25.245257'),
('48rbr3ur5fv2h2ieoixkagaprez3sgmm', '.eJxVjDsOgzAQBe_iGln-QTBl-pwB7doLODEmwqAUUe4eI1Ek7bx582Y97NvU75nWPnjWMaNZ9QsR3IPSsfg7pHHhbknbGpAfCj_XzG-Lp3g93b_ABHkq78YJrLWU5JQVSLW3qrWmsTXawVsYGvDFMBfUJNHgIFqlhROgGiU1CVmiL4rxWXK0AbJOVmyGkGZKe8nH4ChlYgfMG60FOcghjezzBV-OSt4:1qOFkt:PrTWXECL3O6DGwFovFj_wqg0-K7luGs1LjYcjJl7mB0', '2023-08-08 16:29:03.664494'),
('8i1bl8i3oj8l5u7vluye70k3mlp3r6ds', '.eJxVjMsOgjAQRf-la9Mw7SCVpXu_oZnOTAUlQHjEhfHfhYSFbu8597xNpHVp4jrrFFsxtYFgTr9jIn5qvxN5UH8fLA_9MrXJ7oo96Gxvg2h3Pdy_QENzs71D4V0pSEDnCn2WCrXMmkW8Q2UJqpQZhchdMkMqSnA-MVNCDAzAW_SlXTduOV0omRo-XzJ9P0U:1qPbjR:c_hyHMbByI12vZSvpixftZn3GV-RsJwxz7skI0ZqIWE', '2023-08-12 10:09:09.499534'),
('9dlna5f211ky15x0cpla7mbo78ve9inh', 'e30:1qGFNY:VPDJGKosSsrOWE6dtEc-4UyeD5INbY5v6WojKyvczaQ', '2023-07-17 14:27:52.764380'),
('9hr3mwrqj4u8z85yabuhnnxkpd6rkj02', '.eJxVjMEOgjAQRP-lZ9IApV3K0bvfQJbuKigthJZ4MP67JeGgt8nMm_cWPe5p7PfIWz-R6IRqRfFbDuieHI6FHhjui3RLSNs0yAOR5xrldSGeLyf7JxgxjvndOm3ZKEdUaltSA4ykwBCTrQkMgqabHgzXVdOWBirFJl8AQHFmwGbpi-d5zTpOOIiuKoTHKXgOe9Z7jIm3KIoz5Wrd_RrF5wszi0sE:1qNY7Q:txbt7fb3oKB5P0zOaFd1SNhan127NH4SiEF9lsf-MQ4', '2023-08-06 17:53:24.483243'),
('ac8f7yqzcr7du4tweaik3h73urb6fkkr', '.eJxVjDkOwjAURO_iGlm2Y2cr6TlD9LeQgOVEWUSBuDuOlALKmXnz3qqDfRu6fZWlG1m1ynl1-S0R6CnpWPgB6T5pmtK2jKgPRJ_rqm8TS7ye7J9ggHU43i4UFRnggMLU1NZwU_fYe_IlogRfNbnwXDBZXzoDTgwE44ocybLL0pfEOGedbICqtZ8vExs-Kg:1qRQEX:HN0VL_NsEruwGOs9_TT-CCOLdcgOH0ZrCeZnmyfLtGQ', '2023-08-17 10:16:45.055948'),
('anaoht3lvjrfdb30535pjo4uyvhrnzwl', '.eJxVjDkOwjAQRe_iGlle4mUo6XMGa8YLDiBHipMKcXcSKQW0773_3yzgttaw9byEKbErk-zyywjjM7dDpAe2-8zj3NZlIn4k_LSdj3PKr9vZ_h1U7HVf5xKBilVSFRPBR2OFzqhJoLbgSEkiHIzw5BDsQAYdeKlIZ6Fg5459vu3eN2w:1qKDVy:FHCRY2fMx708dVnJzB7APO1fLWINUiko6mWuA9W-1ac', '2023-07-28 13:16:58.116596'),
('apbxs0u9bc008p444a2xt0m6vhsy4fxn', '.eJxVzLtOwzAUBuB38VxF8S1Ou7UIBaQi0Q6BskTH9glxLjaKXTog3p1UdOn6X74fkmbwEUxywTfOkg0xsUkYUwO0ftzG3Cn_xA5VVycY9tO7e6suxXPyNhzxFev-pPr9VlTpWHw_DOHQx4_1iaxIA-fUNeeI8z8q5H2owQzor43twX-GzASfZqez6yS7tTF7CRbH3W17B3QQu-WtKStypVmuKdcoypabXLXA1xJLK6hkOVNWCMGVVIyipMgtsoJLanSLpVrQC47j18JhAk02dEUmcH5Cf1740Rn0EcnvH9WlYhk:1qOCQE:pXeobdYtIf2j6tKoe7SyJYfxpglEMBTbIKQruIX0OWs', '2023-08-08 12:55:30.331660'),
('bewbi37bd0gu0egsje2ww12qca9g8s3t', '.eJxVjDkOwjAQRe_iGlle4mUo6XMGa8YLDiBHipMKcXcSKQW0773_3yzgttaw9byEKbErk-zyywjjM7dDpAe2-8zj3NZlIn4k_LSdj3PKr9vZ_h1U7HVf5xKBilVSFRPBR2OFzqhJoLbgSEkiHIzw5BDsQAYdeKlIZ6Fg5459vu3eN2w:1qJohx:YC_nlSnAuqOTFu_nGMuMDScCBsTSFfEGEqsHSwC7YYo', '2023-07-27 10:47:41.302252'),
('caekcqarnj6t3qq0rmse3ftms4z8ta0v', '.eJxVjDkOwjAQRe_iGlle4mUo6XMGa8YLDiBHipMKcXcSKQW0773_3yzgttaw9byEKbErk-zyywjjM7dDpAe2-8zj3NZlIn4k_LSdj3PKr9vZ_h1U7HVf5xKBilVSFRPBR2OFzqhJoLbgSEkiHIzw5BDsQAYdeKlIZ6Fg5459vu3eN2w:1qQlUw:yI5mPYLCwoexTI7W6UYMahjEGFyIi-zkpcrHtIm0qzg', '2023-08-15 14:46:58.797024'),
('di7cdt29g4qwkjbokuq3u4bgcq3oa1ib', 'eyJ0cmFuc2FjdGlvbl9pZCI6ImNzX3Rlc3RfYTF0MG1INlBHY0pNYjBQN1BCUHNUM29MaE1SWnp2cHBkbWExb1RNNmVXWWVQWnN2ZVNoMk00a3VCUCJ9:1qQPIh:sKq-AC0SFCRxa6c5MZjuGs0PpBGhSWE9g9FrUba1F-k', '2023-08-14 15:04:51.991194'),
('eo0cz5ashbsrnshbkfndyn8xe5kfr0a8', '.eJxVjDkOwjAQRe_iGlle4mUo6XMGa8YLDiBHipMKcXcSKQW0773_3yzgttaw9byEKbErk-zyywjjM7dDpAe2-8zj3NZlIn4k_LSdj3PKr9vZ_h1U7HVf5xKBilVSFRPBR2OFzqhJoLbgSEkiHIzw5BDsQAYdeKlIZ6Fg5459vu3eN2w:1qLGNQ:gk8Is3QZsbJnSrAEWdNtG-K8fLl_L2urt4UpoeraKeI', '2023-07-31 10:32:28.289089'),
('h323gm63af3zgem49tw64uvndrd7v154', '.eJxVjEEOgyAURO_C2hgLItBl9z2D-fg_lRbRCKZpmt69mLgxs5t5874sfxZiVwY4-cgq1sOWx35LtPYeSy_UubQwvCjuCz4hPuZ6mGNeva13pD7WVN9npHA72JNghDSWtwaNoE3DnTC8Ex3yDpAsghhaqRrJlTLgyFjgqpUaSyShMo0jh9y5In1TCEvRUQbLrpeKTeDjRHEr-uAHionY7w9-20p5:1qNB4R:0T15wtG0hjf-2wpOrr9WKK15dr5hKzjvEKkLHu8Axms', '2023-08-05 17:16:47.098806'),
('h66mwicvd6dxxlxi3a7s52je6aoo8oua', '.eJxVjssOgjAQRf-la0LaUl4u3fsNZDozCIgt4RFjjP_uYFjorufe25N5qQa2tWu2heemJ3VS1qnkN_SANw57QwOEa0wxhnXufbpP0qNd0kskHs_H9k_QwdLtv22elaiBcs-EdWU01VXrW4eu8J5zV9YSOMoIjSusBssacm0zQTRkRfrgcZxExyt4dTKJukMf7hw20U9zHBjXRWYYN7nwKaEpC-GjEq6E_Bjx9n2_PzjuUco:1qRmcl:RtBe3lazTO-1tppC56VtK9Vr8KIIPnnOtzgLZdy-41w', '2023-08-18 10:11:15.959686'),
('hj7vxor67ow9gaig7nyi7zyjo9kfqsvx', '.eJxVjDkOwjAQRe_iGlle4mUo6XMGa8YLDiBHipMKcXcSKQW0773_3yzgttaw9byEKbErk-zyywjjM7dDpAe2-8zj3NZlIn4k_LSdj3PKr9vZ_h1U7HVf5xKBilVSFRPBR2OFzqhJoLbgSEkiHIzw5BDsQAYdeKlIZ6Fg5459vu3eN2w:1qOCPR:nm1NJFXaGNPgp6dI90u-dhjH6CcrR5d0Eq8pXyyZBMk', '2023-08-08 12:54:41.172563'),
('i9nduz83o1kitt39mksyg8zaq8b923tr', 'eyJ0cmFuc2FjdGlvbl9pZCI6ImNzX3Rlc3RfYTFkRGFHMkNXbklwQnZPRTRGMmRlbmVRS2l3WTI5T2FXNnNjenZ3QUEzWnpBeTNwcGw5Y1hNa2lsdCJ9:1qJpls:O6D7to4Q1ma5vTih2Q53kf5dkBaDkoYEBuVW2BOa5S0', '2023-07-27 11:55:48.094178'),
('i9qkbfdoz5mckkhf0mx1eu2h23ax0lxd', 'eyJ0cmFuc2FjdGlvbl9pZCI6ImNzX3Rlc3RfYTF2b0NwenFiTTZNT1NYbzExQzk0bWdNZTd6TUxRRFBUR1pOd252UmkycFZObHBEUEhaUG0xUmhkMCJ9:1qJpsg:-qnjELVaP812fMfP1mfVNbCc83VUXq7EGUv_DSKM7zY', '2023-07-27 12:02:50.901808'),
('ihmhx3d91t2szneteap67daups7v6m7j', '.eJxVjEEOwiAURO_CuiEVSoEu3XuG5sP_WBSpKW1cGO8uTbrQzG7mzXuzEbZ1GrdCyxiRDUxq1vyWDvyd8r7gDfJ15n7O6xId3xF-rIVfZqR0Ptg_wQRlqm8DBsHYVgRpRS97FD0gOQTpO6VbJbS2EMg6ELpTBmsUobZtoIAihCp9UUrPqqMVHBtODXtAzA_KW9Wn6CkXYp8vdVRFwA:1qNTXf:-X6uKmU0uPJNUVxfcdttv0ul6voP6NxZSyHbRPWZzw4', '2023-08-06 13:00:11.222318'),
('ja6gbstf0a5qphhm1t080ee6z23w6kqw', '.eJxVkM1OwzAQhN_F5xAlMflxb-0NCVDfIFr_EbeOHcW2UIR4d9bgQ7ntzsx-Gu0XmSHFZU5B7bOR5ETallSPIgdxVy478gbuw9fCu7gbXudIXdxQv3mp7KVk_wEWCAte91xNI2cgmaY9E7TTowY90RZaJRuhJ9lD0w9MsUmKkQ5Uc9EK3vFxHKnUGqGfytoNcSoCJydakRWMW5VLiM9ewIzwCesdqDCG67b7mxIR1w43br24l1kbZWWZ83HhLIfcIVkjQtF_v9JVJDmTMefrSzHisSkUrq_nd1RC4oWwJikhwmPfv8_SHMMyxrvZwZqP2TDVzVNHm-e6Id8_sVV-3Q:1qPN6w:TTKGgJVz4yTmMpqDP3k244bLx0aBGa_0UZlSWN9C8bQ', '2023-08-11 18:32:26.909618'),
('k3vvsqehvosqn9hhz0kzfne1ip3jiq7z', '.eJxVkEFvwyAMhf8L5yoiabNAb5u2w6R12nG3yBhoaClEIWiKpv33mYrDdrPfe3y2-WYj5HUaczLL6DQ7spaz3V9RAV5NKI6-QDjHBmNYF6eaEmmqm5pT1MY_1ew_wARpotdCCsH1vuuF7PiDRbm3cBiERDy01qqeK9S8FRo59LIfFILd89ag5LKDgSuCfhnvZ8KZFRQ7tjt2AxduJmTCz0u8GFwTxTBm2nAjUUpqq1NOo075iNdaW2e8rnVhV9S06QWyd5iqfv8YGpeDK5jT6-fLc7XWbTYkfbw9vpOSsqqMu7dAGRxplZ9fGzd0Sw:1qEnq6:sCIe6bDmk0hCnqIXtL_sMKh5nmrrXJ824STPGo0SJbo', '2023-07-13 14:51:22.102804'),
('kc6ep83st2rt13igiq75kytl1np0jmr5', '.eJxVj8tOwzAURP_F6yryI0ndLkFCRUBBCpTCJrrXvmlME6eKHVoJ8e-4ogvYzpw50nyxGqbY1lOgsXaWLVmes9nfEMHsyZ8b-wF-N2Rm8HF0mJ2R7NKG7GGw1F1d2H-CFkKb1gtBSoEsLDaKoLGaLOcLLXMuAQuJpeYAHClXPC-MsEbPlUDkc4GNLbhK0iN13SHpKAKypZixHpzvyU9J3zlDPlCi4gg-gIlu8L-PTKgjhViD2J6EWg2r6lU_9fpuU8ltKcR2_dLwT3W9qdztzfrw_vzmsZK7Rp8SKh_v98eSff8Ak9VhnA:1qOEFq:2bAJnsYKO6FRR6hA9I8AjHVKwo0Md0PveBStX0igtg0', '2023-08-08 14:52:54.564858'),
('kpqrx1wf0mvgqj00ylcr8pvh3q686c4a', 'eyJ0cmFuc2FjdGlvbl9pZCI6ImNzX3Rlc3RfYTE4RkdSYWZEV1JRSWRyT2Nmb3JOeHV0NnRnRThuWHdtc2NPMkR4TG1SV2xHMkhzUWdDTGpaQTNIMSJ9:1qJpvc:h17Y5Iu_aJR-9QqlLIx0gnUKoDdRYQIey0-58QKkpp8', '2023-07-27 12:05:52.196665'),
('kwawwx7915e1kyoeca9ufl6w2glcm15t', '.eJxVkV1PgzAUhv8L19jQdlDYnUYvTJzx0sQY0k9hg0KAxizG_-7bjS3z4rk473l6Sg8_SS3D0tRhtlPdmmSbUJqkt6GS-mB97Ji99F8D0YNfplaRqJC1O5PdYGz3sLr_BjRybnA6V7YUqpKmcjyvNGdOOOlKTiW1JtOuNLnM8qKyVWm04AV3SlOtmBJCcOMchn7brhsxzi5SJVuaJr1sfW99wPhxGvZWL_OqrWlzNJMMXasv-emNRZoE3y7o757fnx7X1nIcLaK3l_tXJHNQ64zrrfPtJ5yXxaOJa9vB11728XxVlCS7YzzbkAzdaezr1o8h3kbZKRnGa5LHYHGynrBanP7ISJ5mpAAClKBKKckABQxwsAE5KIAAJahSBo_BY_AYPAaPwWPwGDwGj8Hj8Dg8Do_D4_A4PEA_41LnxU5xpaEf45v1EPDHj_EBokC9rjrW8fNVN-jDpXCt7cy5-P0D8XOwIw:1qRVat:yPz--BjLO6o4iKTef8tBzhKytMvOoDZYCP9sT3ZQxlI', '2023-08-17 16:00:11.997651'),
('mwhas1z63ry4k6tjqjefg0jwd2s3gb42', '.eJxVjDkOwjAQRe_iGlle4mUo6XMGa8YLDiBHipMKcXcSKQW0773_3yzgttaw9byEKbErk-zyywjjM7dDpAe2-8zj3NZlIn4k_LSdj3PKr9vZ_h1U7HVf5xKBilVSFRPBR2OFzqhJoLbgSEkiHIzw5BDsQAYdeKlIZ6Fg5459vu3eN2w:1qR8sX:0Alj5EMi5fFikNdsqZlBtANXLpBZZXyZZaaLkt2FOg0', '2023-08-16 15:44:53.548824'),
('n8bz4zmqv31ib3uax3lamcfe8bp5narg', '.eJxVjDkOwjAQRe_iGlle4mUo6XMGa8YLDiBHipMKcXcSKQW0773_3yzgttaw9byEKbErk-zyywjjM7dDpAe2-8zj3NZlIn4k_LSdj3PKr9vZ_h1U7HVf5xKBilVSFRPBR2OFzqhJoLbgSEkiHIzw5BDsQAYdeKlIZ6Fg5459vu3eN2w:1qQo1j:-XmSXhGmf5ZdoDhD97_opHAUzTm_LtDmdQVdIfmYjJI', '2023-08-15 17:28:59.821453'),
('nn3nyl2d7b1eut2idp9eciov9dlylx0i', '.eJxVjEEOwiAURO_CuiEVSoEu3XuG5sP_WBSpKW1cGO8uTbrQzG7mzXuzEbZ1GrdCyxiRDUxq1vyWDvyd8r7gDfJ15n7O6xId3xF-rIVfZqR0Ptg_wQRlqm8DBsHYVgRpRS97FD0gOQTpO6VbJbS2EMg6ELpTBmsUobZtoIAihCp9UUrPqqMVHBtODXtAzA_KW9Wn6CkXYp8vdVRFwA:1qNAU3:ZUeLYoQA1lf-9R2yED2Iu6XZAu9aNbZo-UH1y2rveWU', '2023-08-05 16:39:11.093444'),
('nw9iuvp5noibnuvv4gyk9qegftldqmia', 'e30:1qGFMt:PCVamzACJ3aOOeGkuMmVmTqTlrTv8QkPbIbbOgHepW0', '2023-07-17 14:27:11.896965'),
('o2ni2zararzcvdj5uxezsbczz3735d0q', '.eJxVzLtuwjAUBuB38YyiOLZxw1goiCFDS6uWKTrHPiYhwYHYKVKqvnuDysL6X74fFnvwAUysO1_Wli2YCWWkEEvgrlgd591WX8A1XbF7oa9xz7e7w-ZNjt-fzVXiu9lflv1resYB19V6XH6A3mRsxkoYYlUOgfp_lOePIYJpyN8aewR_6BLT-djXmNwmyb0NSdFZap_v2wegglBN71xpnQueZQJQOuHAoHJOYsqFwzmSBWElSvOUOSKlMgBNKNJUCbSKOz2hV2rb88RRBGQLPmMnqP2J_DDxbW3IB2K_f2KUY9E:1qQM8e:sAd6ViOpTRt28Ip42tU-Av5lwgLrCk1znrmUByWzBvY', '2023-08-14 11:42:16.085669'),
('qf0izv5phmzuozkljdzww0jwr9mjx7so', '.eJxVkEFvwyAMhf8L5yoiSdNAb5u2w6R22nG3yBhoaClEIWiKpv33OROatpv93vOH8ScbIC_jkJOZB6fZkdWc7f6KCvBmwuboK4RLrDCGZXaq2iJVcVN1jtr4x5L9BxghjTQtpBBct00nZMMPFmVrYd8LibivrVUdV6h5LTRy6GTXKwTb8tqg5LKBniuCfhjvJ8KZBRQ71jt2BxfuJmTCT3O8GlwSxTBm2nAlUUpqi7N9jTrlI95KbZ3xutQbu6DGVc-QvcNU9J_D0HM5uA1zfnl_firWsk6GpLfTwyspKavC-F01sa9vS4JyiA:1qEnp9:Myf1-YU4f_v82zXfb2oAqXZvjA4hdxWKhK_9Tc49G5g', '2023-07-13 14:50:23.879806'),
('rx8ophqle7bo0u2s35ym15zwsg6aaptj', '.eJxVkE9PxCAQxb8L56YpVGC7N40eTFzj0VvDn-mWXQpNgZjG-N2FDRq9zfze480wn2gUKc5jCrCNRqMjIgw1f6EU6gquKPoi3Nm3yru4GdkWS1vV0J68BvtQvf8CZhHm_Fow6AjDpOso9AxzOnScHnA3UaKmQcGBc6mpmNgd64H3vdRETIozTaggmuEc-gHWrjkOopDoiBu0COMWcCnHr5u_gIqh2iqdd72JZI364bc_0gYlZ2LWT8_vT49VivsKGb293L9mEpKsGb9TS8YiQoStzEvLWoDyKZ9jzwTzcrm6R-6H3Enr1bXWkwGrb_XXNx5td-8:1qRVZy:uCxdWaze94PY8Vq1xqZPZyqv1SvaMSDhpmC6UmOnq8U', '2023-08-17 15:59:14.312406'),
('sotsd45324rc5naamsy17w52w6cnew8z', '.eJxVjMEOwiAQBf-Fc0OgFIo9evcbml1YLIrUlDYejP8uTXrQ65t582YjbOs0boWWMXo2MGlY8zsiuDvlnfgb5OvM3ZzXJSLfFX7Qwi-zp3Q-3L_ABGWqbw2oRd9Dq5QSykm02hjVedP5ShwEAghWCZSt71CAD6RkKwFPNljf6xp9UUrPmqMVkA2yYQ-I-UF5q_kUHeVC7PMFYgJFeQ:1qOwmD:U-Kc5wQeeeCza2n6UukbrEz30BLWRIeru4MzvMF31dc', '2023-08-10 14:25:17.509238'),
('tiom8vbvemucld4s4jfkwtuge5dyh53y', '.eJxVjMEOgyAQBf-FsyEiQcBj7_0Gs8BupUVsRNND038vJh7a65t582Yj7Ns07gXXMQY2MCFY8zs68A_MBwl3yLeF-yVva3T8UPhJC78uAdPldP8CE5SpvpVDo52FYEkq62VHmoCMFCAwtJ5MUNCq3qI1wWvZS3JeeNc5rbUMRDX6wpSeNYcbODaIhs0Q84x5r_kUPeaC7PMFphpGQA:1qRXeu:FpvcfgtlJUgqyuX8kaWWtL0AMyovTeX46GfQRAgmhrY', '2023-08-17 18:12:28.052681'),
('vsaj3h4bg580co1nyxgp0bn4dfw7qupy', '.eJxVjcEOgyAQRP-FszGulQoee-83mGVZKq2iEUzTNP33YuLF67yZN1-RPguLTqCdfBCF6HFLQ79FXntvc37R59AgvTjsxD4xPOaS5pBWb8q9Uh40lvfZ8ng7uifBgHHIawcGaoQGKmqt0Uxoa6OudKmdIqcAsVIkW9RGamha5UCyUQjsCEACZ-mbx3HJOk5oRAeFmNCHicOW9ftVFL8_AEdJxA:1qNtQy:CkFtT97oUxHy_qPb-ZSLMTNlkrP2MU8WgW5zvZLV-2Y', '2023-08-07 16:39:00.812004'),
('wgc2xellw1a4imqwl1u8qjhzfzxandcd', '.eJxVjksOgzAMRO-SNUKEhPJZdt8zIMd2ChQSxEdVVfXuNRKLdjkzz09-qxb2rWv3lZe2J9UoXankt3SADw7HQgOEe0wxhm3pXXog6bmu6S0Sj9eT_RN0sHZyXWUmL8iChktpjafScuHZE5ncMlLFDB4tAeS1R-2yQufGIYKztkKtUaRPHsdZdLyBU41O1AR9mDjsop-XODBuq2AYd_nwJWVdSzwXiUZ9voD7T4M:1qPMoD:fv0hSXDP6wY8uq9WEnMUsTti-TA9hGwlYkCMktiJ8yw', '2023-08-11 18:13:05.683950'),
('x4hc4qd7a3gi8k5rd733ecw03eguk9n7', 'eyJ0cmFuc2FjdGlvbl9pZCI6ImNzX3Rlc3RfYTFHOTI4bUxubDd4QlhPTzVORmFWT3U4OGNPS2c3Rm1mVnR2WEVNR1M3eTdndDRXVW9obXQ4SVJJTSJ9:1qKAUe:xlfypzWqczLwCdtXzuJpA5_OFAGVb0OenUUEYJq6N0w', '2023-07-28 10:03:24.227436'),
('y2ghwec12fvpy9q998vpz2hbnvawo57c', '.eJxVjksOgzAMRO-SNUJJCN9l9z0DcmxToDRBfFRVVe9eI7FolzPz_OS3amHf-nZfeWkHUo2yTiW_pQe8czgWGiHcYooxbMvg0wNJz3VNr5F4upzsn6CHtT-ubZ6VqIFyz4R1ZTTVVec7h67wnnNX1lI4ygiNK6wGyxpybTOJaMiK9MnTNIuON_CqMYl6wBAeHHbRTwNyWFkojLs8-JLOlIXkeYkj4ya5Up8vHz9OEg:1qRRGp:Zm-bzOOjPuWSVdnFP8mJaphI9kWcsBxVMkwLlihov88', '2023-08-17 11:23:11.032946'),
('zih9zl1e72r4i7s2sg3spyxfnqraxw58', '.eJxVjMFOwzAQBf_FZxTFsdPaPQKVEAgJgUSP1np33SRETmQ74YD4d1LRS69v5s2PKAliBiz9FF1P4iAwu8K5OJBvuhwtPVOMBnfyped0ntNx_Viyej_ZbB9kGG19WmOnh7ldPtesnh51HMSdcLCUzi2Z039UmtvRA35xvBAaIJ6nCqdYUu-ri1Jdaa5eJ-Lx_ureBDrI3fY2tWpa0iBht9cq0F5zGzgQqUYzkmGGgJoAGhtQ-rqVjfKI4LU2KCVu0W8ex3nLcQEvDvL3D1lBXPA:1qOa56:-LeG1g6ZDzB4V-Xh81SMGsbUlo4a4erATKSpQ4axZUc', '2023-08-09 14:11:16.118355'),
('zp5r3y7vuojarqs9hiehrn05i8q9h7p8', '.eJxVkMFuwyAQRP-Fc2SBHdeQW6v2ECmpeuzNggVqEgKWAVVR1X_vUnFob7Mzw1vgi8yy5GUuyWyz0-RAGCW7v6aScDWhJvoiw0fsIIa8OdXVStfS1J2jNv6pdf8BFpkWPM0F51QP_chFTx8siMHK_cQFwJ5Zq0aqQFPGNVA5inFSIO1AmQFBRS8nqhD6abxfEWeyVOTAduQmXbiZUBC_bvFiICesQSx4wzuaQuDYkvo0nJSPcG3aOuN105XdUFXOGpc4n1ry-zW4sARXQefj-8tzi_J9NWi9nR5fyfcPPQZrJA:1qEnNb:aXRVRjNIfPQLWyAdSx1kAwUE7Szbkc86_FNrUZP9pvg', '2023-07-13 14:21:55.380455');

-- --------------------------------------------------------

--
-- Table structure for table `drillbitdata_drillbit`
--

CREATE TABLE `drillbitdata_drillbit` (
  `id` int NOT NULL,
  `date` date DEFAULT NULL,
  `no_of_nozzle` int DEFAULT NULL,
  `tfa` double DEFAULT NULL,
  `external_nozzle` tinyint(1) DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) DEFAULT NULL,
  `manufacture` varchar(50) DEFAULT NULL,
  `timestamp` int DEFAULT NULL,
  `time` time(6) DEFAULT NULL,
  `serial_no` varchar(50) DEFAULT NULL,
  `idac_code` varchar(50) DEFAULT NULL,
  `bha_id` int DEFAULT NULL,
  `bit_type_id` int DEFAULT NULL,
  `company_id` int DEFAULT NULL,
  `well_id` bigint DEFAULT NULL,
  `well_phases_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `drillbitdata_drillbit`
--

INSERT INTO `drillbitdata_drillbit` (`id`, `date`, `no_of_nozzle`, `tfa`, `external_nozzle`, `status`, `created`, `manufacture`, `timestamp`, `time`, `serial_no`, `idac_code`, `bha_id`, `bit_type_id`, `company_id`, `well_id`, `well_phases_id`) VALUES
(1, NULL, 7, 0.55, NULL, 1, '2023-07-14 11:20:35.177219', 'Smith', NULL, NULL, NULL, NULL, NULL, 1, 2, 2, 3);

-- --------------------------------------------------------

--
-- Table structure for table `drillbitdata_drillbitnozzle`
--

CREATE TABLE `drillbitdata_drillbitnozzle` (
  `id` int NOT NULL,
  `nozzle_size` double DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) DEFAULT NULL,
  `company_id` int DEFAULT NULL,
  `drillbit_id` int DEFAULT NULL,
  `well_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `drillbitdata_drillbitnozzle`
--

INSERT INTO `drillbitdata_drillbitnozzle` (`id`, `nozzle_size`, `status`, `created`, `company_id`, `drillbit_id`, `well_id`) VALUES
(1, 12, 1, '2023-07-14 11:20:35.207284', 2, 1, 2),
(2, 12, 1, '2023-07-14 11:20:35.285038', 2, 1, 2),
(3, 12, 1, '2023-07-14 11:20:35.375689', 2, 1, 2),
(4, 12, 1, '2023-07-14 11:20:35.508994', 2, 1, 2),
(5, 12, 1, '2023-07-14 11:20:35.531326', 2, 1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `enquiries`
--

CREATE TABLE `enquiries` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `company_name` varchar(100) NOT NULL,
  `gender` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `message` varchar(255) NOT NULL,
  `notification_status` int NOT NULL,
  `status` int NOT NULL,
  `form_type` varchar(50) DEFAULT NULL,
  `no_of_users` int NOT NULL,
  `user_type` varchar(50) DEFAULT NULL,
  `user_type_id` int NOT NULL,
  `designation` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `enquiries`
--

INSERT INTO `enquiries` (`id`, `name`, `last_name`, `company_name`, `gender`, `email`, `message`, `notification_status`, `status`, `form_type`, `no_of_users`, `user_type`, `user_type_id`, `designation`) VALUES
(1, 'Venkat', 'K', 'X-MAS Private Limited', 'Mr', 'venkat100785@gmail.com', '<p>Hello,</p><p>Testing</p>', 0, 0, NULL, 0, NULL, 0, ''),
(2, 'Kumar', 'M', 'DOPT', 'Mr', 'jagdishkumar@xmedia.com', '', 0, 0, NULL, 0, NULL, 0, ''),
(3, 'Kumar', 'M', 'DDR', 'Mr', 'jagdishkumar@xmedia.com', '', 0, 0, NULL, 0, NULL, 0, ''),
(4, 'Kumar', 'M', 'DOPT 3', 'Mrs', 'jagdishkumar@xmedia.com', '', 0, 0, NULL, 0, NULL, 0, ''),
(5, 'Mageshwari', 'K', 'Lilium Candidum Oil and Gas Private Ltd', 'Miss', 'mageshwari@i-bytes.com', '<p>Good Morning</p><p>iWells Testing</p><p><br></p>', 0, 0, NULL, 0, NULL, 0, ''),
(6, 'Subash', 'Lingeshara', 'iWells', 'Mrs', 'subash@i-bytes.com', '<p>Give me software</p>', 0, 0, NULL, 0, NULL, 0, ''),
(7, 'Dev', 'Deva', 'Dev Goup of Companies', 'Miss', 'devayani@xmedia.in', '<p>Need a idea</p>', 0, 0, NULL, 0, NULL, 0, ''),
(8, 'Arujun', 'D', 'AIR 1', '', 'arujun@xmedia.in', '', 0, 0, 'license', 23, 'CompanyPlan', 5, 'Manager'),
(9, 'Arujun', 'D', 'AIR 1', '', 'arujun@xmedia.in', '', 0, 0, 'license', 23, 'CompanyPlan', 5, 'Manager'),
(10, 'Dev', 'Deva', 'Dev Group of Companies', '', 'devayani@xmedia.in', '', 0, 1, 'license', 10, 'Enterprise', 6, 'CEO'),
(11, 'Dev', 'Deva', 'Dev Group of Companies', '', 'devayani@xmedia.in', '', 0, 0, 'license', 10, 'Enterprise', 6, 'CEO'),
(12, 'Dev', 'Deva', 'Dev Group of Companies', '', 'devayani@xmedia.in', '', 0, 0, 'license', 10, 'Enterprise', 6, 'CEO'),
(13, 'Dev', 'Deva', 'Dev Group of Companies', '', 'devayani@xmedia.in', '', 0, 0, 'license', 12, 'Enterprise', 6, 'CEO'),
(14, 'Dev', 'Deva', 'Dev Group of Companies', '', 'devayani@xmedia.in', '', 0, 0, 'license', 12, 'Enterprise', 6, 'CEO'),
(15, 'Dev', 'Deva', 'Dev Group of Companies', '', 'devayani@xmedia.in', '', 0, 0, 'license', 12, 'Enterprise', 6, 'CEO'),
(16, 'Dev', 'Deva', 'Dev Group of Companies', '', 'devayani@xmedia.in', '', 0, 0, 'license', 12, 'Enterprise', 6, 'CEO'),
(17, 'Dev', 'Deva', 'Dev Group of Companies', '', 'devayani@xmedia.in', '', 0, 0, 'license', 12, 'Enterprise', 6, 'CEO'),
(18, 'Arujun', 'D', 'AIR 1', '', 'arujun@xmedia.in', '', 0, 0, 'license', 200, 'CompanyPlan', 8, 'Manager'),
(19, 'Luke', 'S', 'MyCOMP', '', 'deva@gmail.com', '', 0, 0, 'license', 90, 'Individual', 45, 'test'),
(20, 'Jagadish', 'Kumar', 'AIR 10', '', 'shrjash1324@gmail.com', '', 0, 0, 'license', 100, 'Enterprise', 9, 'EO'),
(23, 'Arujun', 'D', '', '', 'arujun@xmedia.in', '', 0, 0, 'license', 200, 'Individual', 16, ''),
(24, 'dev', 'deva', 'devs', '', 'devayani@xmedia.in', '', 0, 1, 'license', 30, 'CompanyPlan', 13, 'Manager'),
(25, 'dev', 'deva', 'devs', '', 'devayani@xmedia.in', '', 0, 0, 'license', 5, 'Enterprise', 13, 'Manager'),
(26, 'Jagadish', 'Kumar', 'AIR 1', '', 'jagdishkumar@xmedia.in', '', 0, 0, 'license', 30, 'CompanyPlan', 16, 'CEO'),
(27, 'Shankar', 'Fire', 'Fire ON', 'Mr', 'sankaranarayanan@xmedia.in', '<p>GP</p>', 0, 0, NULL, 0, NULL, 0, ''),
(28, 'Jagadish', 'M', 'AIR 10', 'Mr', 'shrjash1324@gmail.com', '<p>10</p>', 0, 0, NULL, 0, NULL, 0, ''),
(29, 'Arujun', 'D', 'DOPT 1', '', 'arujun@xmedia.in', '', 0, 0, 'license', 25, 'CompanyPlan', 18, 'Manager');

-- --------------------------------------------------------

--
-- Table structure for table `license_licensepackage`
--

CREATE TABLE `license_licensepackage` (
  `id` int NOT NULL,
  `type_of_license` varchar(25) DEFAULT NULL,
  `no_of_users` int DEFAULT NULL,
  `amount` int DEFAULT NULL,
  `status` int NOT NULL,
  `subscription_type` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `license_licensepackage`
--

INSERT INTO `license_licensepackage` (`id`, `type_of_license`, `no_of_users`, `amount`, `status`, `subscription_type`) VALUES
(1, 'Individual', NULL, 60, 1, 'monthly'),
(2, 'Individual', NULL, 70, 1, 'yearly'),
(3, 'CompanyPlan', 5, 350, 1, 'monthly'),
(4, 'CompanyPlan', 5, 4050, 1, 'yearly'),
(5, 'CompanyPlan', 10, 700, 1, 'monthly');

-- --------------------------------------------------------

--
-- Table structure for table `modules`
--

CREATE TABLE `modules` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `module_type` int NOT NULL,
  `status` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `modules`
--

INSERT INTO `modules` (`id`, `name`, `module_type`, `status`) VALUES
(1, 'Create User', 1, 0),
(2, 'Create Project', 1, 1),
(3, 'Create Well', 1, 1),
(4, 'Create Data', 1, 1),
(5, 'Edit Data', 1, 1),
(6, 'Create Master', 1, 1),
(7, 'Edit Master', 1, 1),
(8, 'View Data', 1, 1),
(9, 'Perform Calculations', 1, 1),
(10, 'View Results', 1, 0),
(11, 'Download Results', 1, 1),
(12, 'Download Reports', 1, 1),
(13, 'Manage License', 1, 1),
(14, 'Manage Users', 1, 1),
(15, 'View Subscription', 1, 1),
(16, 'Customize User Privilege', 1, 0),
(17, 'Change User Type', 1, 1),
(18, 'Create Custom User Types', 1, 0),
(19, 'View Log in and Log out Data of Users', 1, 1),
(20, 'Transfer User', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `muddata_hydraulicdata`
--

CREATE TABLE `muddata_hydraulicdata` (
  `id` int NOT NULL,
  `date` date DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) DEFAULT NULL,
  `timestamp` int DEFAULT NULL,
  `time` time(6) DEFAULT NULL,
  `measured_depth` double DEFAULT NULL,
  `flowrate` double DEFAULT NULL,
  `rop` double DEFAULT NULL,
  `rpm` int DEFAULT NULL,
  `pump_pressure` double DEFAULT NULL,
  `annular_pressure` int DEFAULT NULL,
  `ecd` double DEFAULT NULL,
  `company_id` int DEFAULT NULL,
  `well_id` bigint DEFAULT NULL,
  `well_phase_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `muddata_muddata`
--

CREATE TABLE `muddata_muddata` (
  `id` int NOT NULL,
  `gel_strength_0sec` double DEFAULT NULL,
  `gel_strength_10min` double DEFAULT NULL,
  `gel_strength_30min` double DEFAULT NULL,
  `mud_weight` double DEFAULT NULL,
  `plastic_viscosity` double DEFAULT NULL,
  `yield_point` double DEFAULT NULL,
  `low_shear_rate` double DEFAULT NULL,
  `date` date DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) DEFAULT NULL,
  `section` varchar(255) DEFAULT NULL,
  `from_depth` double DEFAULT NULL,
  `todepth` double DEFAULT NULL,
  `timestamp` int DEFAULT NULL,
  `time` time(6) DEFAULT NULL,
  `company_id` int DEFAULT NULL,
  `mudtype_id` int DEFAULT NULL,
  `well_id` bigint DEFAULT NULL,
  `well_phase_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `muddata_muddata`
--

INSERT INTO `muddata_muddata` (`id`, `gel_strength_0sec`, `gel_strength_10min`, `gel_strength_30min`, `mud_weight`, `plastic_viscosity`, `yield_point`, `low_shear_rate`, `date`, `status`, `created`, `section`, `from_depth`, `todepth`, `timestamp`, `time`, `company_id`, `mudtype_id`, `well_id`, `well_phase_id`) VALUES
(1, NULL, NULL, NULL, 10.4, 25, 20, 15, NULL, 1, '2023-07-14 11:19:38.083464', '968.0-2304.0', 968, 2304, NULL, NULL, 2, 2, 2, 3);

-- --------------------------------------------------------

--
-- Table structure for table `muddata_plandate`
--

CREATE TABLE `muddata_plandate` (
  `id` int NOT NULL,
  `flowrate` int DEFAULT NULL,
  `rop` double DEFAULT NULL,
  `rpm` int DEFAULT NULL,
  `bitdepth` double DEFAULT NULL,
  `surface_pressure` double DEFAULT NULL,
  `ecd` double DEFAULT NULL,
  `section_name` varchar(100) DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) DEFAULT NULL,
  `company_id` int DEFAULT NULL,
  `well_id` bigint DEFAULT NULL,
  `well_phase_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `muddata_pressureloss_data`
--

CREATE TABLE `muddata_pressureloss_data` (
  `id` int NOT NULL,
  `all_data` json DEFAULT NULL,
  `section_name` varchar(100) DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) DEFAULT NULL,
  `company_id` int DEFAULT NULL,
  `well_id` bigint DEFAULT NULL,
  `well_phase_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `muddata_rheogram`
--

CREATE TABLE `muddata_rheogram` (
  `id` int NOT NULL,
  `rpm` int DEFAULT NULL,
  `dial` varchar(255) DEFAULT NULL,
  `modelname` varchar(255) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) DEFAULT NULL,
  `calculateddial` varchar(255) DEFAULT NULL,
  `company_id` int DEFAULT NULL,
  `rheogram_date_id` int DEFAULT NULL,
  `rheogram_sections_id` int DEFAULT NULL,
  `well_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `muddata_rheogram`
--

INSERT INTO `muddata_rheogram` (`id`, `rpm`, `dial`, `modelname`, `date`, `status`, `created`, `calculateddial`, `company_id`, `rheogram_date_id`, `rheogram_sections_id`, `well_id`) VALUES
(1, 3, '0', 'newtonian', NULL, 1, '2023-07-14 11:19:54.562809', NULL, 2, 1, 1, 2),
(2, 6, '1', 'newtonian', NULL, 1, '2023-07-14 11:19:54.631751', NULL, 2, 1, 1, 2),
(3, 100, '8', 'newtonian', NULL, 1, '2023-07-14 11:19:54.696044', NULL, 2, 1, 1, 2),
(4, 200, '17', 'newtonian', NULL, 1, '2023-07-14 11:19:54.708213', NULL, 2, 1, 1, 2),
(5, 300, '25', 'newtonian', NULL, 1, '2023-07-14 11:19:54.718924', NULL, 2, 1, 1, 2),
(6, 600, '50', 'newtonian', NULL, 1, '2023-07-14 11:19:54.727585', NULL, 2, 1, 1, 2),
(7, 3, '20', 'bingham', NULL, 1, '2023-07-14 11:19:54.781722', NULL, 2, 1, 1, 2),
(8, 6, '21', 'bingham', NULL, 1, '2023-07-14 11:19:54.827495', NULL, 2, 1, 1, 2),
(9, 100, '28', 'bingham', NULL, 1, '2023-07-14 11:19:54.859321', NULL, 2, 1, 1, 2),
(10, 200, '37', 'bingham', NULL, 1, '2023-07-14 11:19:54.896411', NULL, 2, 1, 1, 2),
(11, 300, '45', 'bingham', NULL, 1, '2023-07-14 11:19:54.968996', NULL, 2, 1, 1, 2),
(12, 600, '70', 'bingham', NULL, 1, '2023-07-14 11:19:55.122996', NULL, 2, 1, 1, 2),
(13, 3, '2', 'powerlaw', NULL, 1, '2023-07-14 11:19:55.188312', NULL, 2, 1, 1, 2),
(14, 6, '4', 'powerlaw', NULL, 1, '2023-07-14 11:19:55.411202', NULL, 2, 1, 1, 2),
(15, 100, '22', 'powerlaw', NULL, 1, '2023-07-14 11:19:55.550563', NULL, 2, 1, 1, 2),
(16, 200, '35', 'powerlaw', NULL, 1, '2023-07-14 11:19:55.573269', NULL, 2, 1, 1, 2),
(17, 300, '45', 'powerlaw', NULL, 1, '2023-07-14 11:19:55.607137', NULL, 2, 1, 1, 2),
(18, 600, '70', 'powerlaw', NULL, 1, '2023-07-14 11:19:55.615684', NULL, 2, 1, 1, 2),
(19, 3, '16', 'hershel', NULL, 1, '2023-07-14 11:19:55.627052', NULL, 2, 1, 1, 2),
(20, 6, '16', 'hershel', NULL, 1, '2023-07-14 11:19:55.634722', NULL, 2, 1, 1, 2),
(21, 100, '26', 'hershel', NULL, 1, '2023-07-14 11:19:55.642175', NULL, 2, 1, 1, 2),
(22, 200, '36', 'hershel', NULL, 1, '2023-07-14 11:19:55.688431', NULL, 2, 1, 1, 2),
(23, 300, '45', 'hershel', NULL, 1, '2023-07-14 11:19:55.713510', NULL, 2, 1, 1, 2),
(24, 600, '70', 'hershel', NULL, 1, '2023-07-14 11:19:55.767756', NULL, 2, 1, 1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `mudtype`
--

CREATE TABLE `mudtype` (
  `id` int NOT NULL,
  `mud_name` varchar(100) DEFAULT NULL,
  `status` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `mudtype`
--

INSERT INTO `mudtype` (`id`, `mud_name`, `status`) VALUES
(1, 'OBM', 1),
(2, 'SOBM', 1),
(3, 'WBM', 1),
(4, 'NADF', 1),
(5, 'OBM 1', 1);

-- --------------------------------------------------------

--
-- Table structure for table `mud_mudpump`
--

CREATE TABLE `mud_mudpump` (
  `id` int NOT NULL,
  `stroke_length` double DEFAULT NULL,
  `pump_name` varchar(30) DEFAULT NULL,
  `pump_manufacturer` varchar(30) DEFAULT NULL,
  `pump_type` varchar(30) DEFAULT NULL,
  `number_of_pumps` int DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) DEFAULT NULL,
  `company_id` int DEFAULT NULL,
  `well_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `mud_mudpump`
--

INSERT INTO `mud_mudpump` (`id`, `stroke_length`, `pump_name`, `pump_manufacturer`, `pump_type`, `number_of_pumps`, `status`, `created`, `company_id`, `well_id`) VALUES
(1, 12, NULL, 'Cameron Simon 1', 'Triplex', 3, 1, '2023-06-28 12:17:08.744171', 1, 1),
(2, 12, NULL, 'Cameron Simon 1', 'Triplex', 3, 1, '2023-07-20 13:34:31.070332', 2, 2),
(3, 12, NULL, 'Cameron Simon 1', 'Triplex', 3, 0, '2023-08-03 15:32:15.009045', 2, 6),
(4, 12, NULL, 'Cameron Simon 1', 'Triplex', 3, 0, '2023-08-03 15:32:15.630662', 20, 5),
(5, 11, NULL, 'Cameron Simon 1', 'Triplex', 3, 1, '2023-08-03 15:44:13.895892', 2, 6);

-- --------------------------------------------------------

--
-- Table structure for table `mud_mudpumpdata`
--

CREATE TABLE `mud_mudpumpdata` (
  `id` int NOT NULL,
  `linear_size` double DEFAULT NULL,
  `max_discharge_pressure` double DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) NOT NULL,
  `company_id` int DEFAULT NULL,
  `mud_pump_id` int DEFAULT NULL,
  `well_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `mud_mudpumpdata`
--

INSERT INTO `mud_mudpumpdata` (`id`, `linear_size`, `max_discharge_pressure`, `status`, `created`, `company_id`, `mud_pump_id`, `well_id`) VALUES
(1, 4.5, 7500, 1, '2023-06-28 12:17:08.798153', 1, 1, 1),
(2, 5, 8000, 1, '2023-06-28 12:17:08.844944', 1, 1, 1),
(3, 5.5, 8500, 1, '2023-06-28 12:17:08.853133', 1, 1, 1),
(4, 6, 9000, 1, '2023-06-28 12:17:08.859672', 1, 1, 1),
(5, 5, 4500, 1, '2023-07-20 13:34:31.128571', 2, 2, 2),
(6, 5.5, 4000, 1, '2023-07-20 13:34:31.272436', 2, 2, 2),
(7, 6, 3500, 1, '2023-07-20 13:34:31.282037', 2, 2, 2),
(8, 6.5, 3000, 1, '2023-07-20 13:34:31.296416', 2, 2, 2),
(9, 5, 5000, 0, '2023-08-03 15:32:15.214301', 2, 3, 6),
(10, 5.5, 4500, 0, '2023-08-03 15:32:15.236272', 2, 3, 6),
(11, 6, 4000, 0, '2023-08-03 15:32:15.245924', 2, 3, 6),
(12, 6.5, 3500, 0, '2023-08-03 15:32:15.299287', 2, 3, 6),
(13, 5, 5000, 0, '2023-08-03 15:32:16.002997', 20, 4, 5),
(14, 5.5, 4500, 0, '2023-08-03 15:32:16.096678', 20, 4, 5),
(15, 6, 4000, 0, '2023-08-03 15:32:16.141528', 20, 4, 5),
(16, 6.5, 3500, 0, '2023-08-03 15:32:16.197172', 20, 4, 5),
(17, 5, 5000, 1, '2023-08-03 15:44:13.918859', 2, 5, 6),
(18, 5.5, 4500, 1, '2023-08-03 15:44:13.931999', 2, 5, 6),
(19, 6, 4000, 1, '2023-08-03 15:44:13.938918', 2, 5, 6),
(20, 6.5, 3500, 1, '2023-08-03 15:44:13.945594', 2, 5, 6);

-- --------------------------------------------------------

--
-- Table structure for table `mud_mudpumpflowrate`
--

CREATE TABLE `mud_mudpumpflowrate` (
  `id` int NOT NULL,
  `flowrate` double DEFAULT NULL,
  `status` int NOT NULL,
  `order` int DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `company_id` int DEFAULT NULL,
  `mud_pump_speed_id` int DEFAULT NULL,
  `well_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `mud_mudpumpflowrate`
--

INSERT INTO `mud_mudpumpflowrate` (`id`, `flowrate`, `status`, `order`, `created`, `company_id`, `mud_pump_speed_id`, `well_id`) VALUES
(1, 198, 1, NULL, '2023-06-28 12:17:08.899966', 1, 1, 1),
(2, 245, 1, NULL, '2023-06-28 12:17:08.952433', 1, 1, 1),
(3, 296, 1, NULL, '2023-06-28 12:17:08.980279', 1, 1, 1),
(4, 352, 1, NULL, '2023-06-28 12:17:08.996270', 1, 1, 1),
(5, 223, 1, NULL, '2023-06-28 12:17:09.029786', 1, 2, 1),
(6, 275, 1, NULL, '2023-06-28 12:17:09.046830', 1, 2, 1),
(7, 333, 1, NULL, '2023-06-28 12:17:09.070944', 1, 2, 1),
(8, 397, 1, NULL, '2023-06-28 12:17:09.078929', 1, 2, 1),
(9, 248, 1, NULL, '2023-06-28 12:17:09.143057', 1, 3, 1),
(10, 306, 1, NULL, '2023-06-28 12:17:09.150687', 1, 3, 1),
(11, 370, 1, NULL, '2023-06-28 12:17:09.157128', 1, 3, 1),
(12, 441, 1, NULL, '2023-06-28 12:17:09.188560', 1, 3, 1),
(13, 273, 1, NULL, '2023-06-28 12:17:09.359746', 1, 4, 1),
(14, 337, 1, NULL, '2023-06-28 12:17:09.404632', 1, 4, 1),
(15, 407, 1, NULL, '2023-06-28 12:17:09.427744', 1, 4, 1),
(16, 485, 1, NULL, '2023-06-28 12:17:09.437194', 1, 4, 1),
(17, 297, 1, NULL, '2023-06-28 12:17:09.522352', 1, 5, 1),
(18, 367, 1, NULL, '2023-06-28 12:17:09.546900', 1, 5, 1),
(19, 444, 1, NULL, '2023-06-28 12:17:09.580662', 1, 5, 1),
(20, 529, 1, NULL, '2023-06-28 12:17:09.588207', 1, 5, 1),
(21, 275, 1, NULL, '2023-07-20 13:34:31.410285', 2, 6, 2),
(22, 333, 1, NULL, '2023-07-20 13:34:31.417606', 2, 6, 2),
(23, 397, 1, NULL, '2023-07-20 13:34:31.425156', 2, 6, 2),
(24, 465, 1, NULL, '2023-07-20 13:34:31.432041', 2, 6, 2),
(25, 306, 1, NULL, '2023-07-20 13:34:31.446944', 2, 7, 2),
(26, 370, 1, NULL, '2023-07-20 13:34:31.455067', 2, 7, 2),
(27, 441, 1, NULL, '2023-07-20 13:34:31.525774', 2, 7, 2),
(28, 517, 1, NULL, '2023-07-20 13:34:31.533762', 2, 7, 2),
(29, 337, 1, NULL, '2023-07-20 13:34:31.549278', 2, 8, 2),
(30, 407, 1, NULL, '2023-07-20 13:34:31.556624', 2, 8, 2),
(31, 485, 1, NULL, '2023-07-20 13:34:31.563691', 2, 8, 2),
(32, 569, 1, NULL, '2023-07-20 13:34:31.570566', 2, 8, 2),
(33, 367, 1, NULL, '2023-07-20 13:34:31.617603', 2, 9, 2),
(34, 444, 1, NULL, '2023-07-20 13:34:31.658488', 2, 9, 2),
(35, 529, 1, NULL, '2023-07-20 13:34:31.666265', 2, 9, 2),
(36, 621, 1, NULL, '2023-07-20 13:34:31.674232', 2, 9, 2),
(37, 398, 1, NULL, '2023-07-20 13:34:31.690149', 2, 10, 2),
(38, 481, 1, NULL, '2023-07-20 13:34:31.697110', 2, 10, 2),
(39, 573, 1, NULL, '2023-07-20 13:34:31.758167', 2, 10, 2),
(40, 672, 1, NULL, '2023-07-20 13:34:31.766769', 2, 10, 2),
(41, 100, 0, NULL, '2023-08-03 15:32:15.419120', 2, 11, 6),
(42, 120, 0, NULL, '2023-08-03 15:32:15.520517', 2, 11, 6),
(43, 140, 0, NULL, '2023-08-03 15:32:15.731945', 2, 11, 6),
(44, 160, 0, NULL, '2023-08-03 15:32:15.843499', 2, 11, 6),
(45, 180, 0, NULL, '2023-08-03 15:32:16.095203', 2, 12, 6),
(46, 200, 0, NULL, '2023-08-03 15:32:16.140080', 2, 12, 6),
(47, 220, 0, NULL, '2023-08-03 15:32:16.191147', 2, 12, 6),
(48, 240, 0, NULL, '2023-08-03 15:32:16.360246', 2, 12, 6),
(49, 100, 0, NULL, '2023-08-03 15:32:16.599236', 20, 13, 5),
(50, 260, 0, NULL, '2023-08-03 15:32:16.878859', 2, 14, 6),
(51, 120, 0, NULL, '2023-08-03 15:32:16.879702', 20, 13, 5),
(52, 280, 0, NULL, '2023-08-03 15:32:16.893218', 2, 14, 6),
(53, 140, 0, NULL, '2023-08-03 15:32:16.894902', 20, 13, 5),
(54, 300, 0, NULL, '2023-08-03 15:32:16.900698', 2, 14, 6),
(55, 160, 0, NULL, '2023-08-03 15:32:16.904287', 20, 13, 5),
(56, 320, 0, NULL, '2023-08-03 15:32:16.910352', 2, 14, 6),
(57, 180, 0, NULL, '2023-08-03 15:32:17.008783', 20, 15, 5),
(58, 340, 0, NULL, '2023-08-03 15:32:17.011976', 2, 16, 6),
(59, 200, 0, NULL, '2023-08-03 15:32:17.026070', 20, 15, 5),
(60, 360, 0, NULL, '2023-08-03 15:32:17.028859', 2, 16, 6),
(61, 220, 0, NULL, '2023-08-03 15:32:17.037139', 20, 15, 5),
(62, 380, 0, NULL, '2023-08-03 15:32:17.038704', 2, 16, 6),
(63, 240, 0, NULL, '2023-08-03 15:32:17.078844', 20, 15, 5),
(64, 400, 0, NULL, '2023-08-03 15:32:17.080531', 2, 16, 6),
(65, 260, 0, NULL, '2023-08-03 15:32:17.188904', 20, 17, 5),
(66, 420, 0, NULL, '2023-08-03 15:32:17.191508', 2, 18, 6),
(67, 280, 0, NULL, '2023-08-03 15:32:17.197855', 20, 17, 5),
(68, 440, 0, NULL, '2023-08-03 15:32:17.198296', 2, 18, 6),
(69, 300, 0, NULL, '2023-08-03 15:32:17.248456', 20, 17, 5),
(70, 460, 0, NULL, '2023-08-03 15:32:17.277531', 2, 18, 6),
(71, 320, 0, NULL, '2023-08-03 15:32:17.372844', 20, 17, 5),
(72, 480, 0, NULL, '2023-08-03 15:32:17.411425', 2, 18, 6),
(73, 340, 0, NULL, '2023-08-03 15:32:17.433691', 20, 19, 5),
(74, 360, 0, NULL, '2023-08-03 15:32:17.460943', 20, 19, 5),
(75, 380, 0, NULL, '2023-08-03 15:32:17.579564', 20, 19, 5),
(76, 400, 0, NULL, '2023-08-03 15:32:17.607077', 20, 19, 5),
(77, 420, 0, NULL, '2023-08-03 15:32:17.747341', 20, 20, 5),
(78, 440, 0, NULL, '2023-08-03 15:32:17.806046', 20, 20, 5),
(79, 460, 0, NULL, '2023-08-03 15:32:17.815552', 20, 20, 5),
(80, 480, 0, NULL, '2023-08-03 15:32:17.823139', 20, 20, 5),
(81, 200, 1, NULL, '2023-08-03 15:44:13.958982', 2, 21, 6),
(82, 220, 1, NULL, '2023-08-03 15:44:13.967483', 2, 21, 6),
(83, 240, 1, NULL, '2023-08-03 15:44:13.975088', 2, 21, 6),
(84, 260, 1, NULL, '2023-08-03 15:44:13.981789', 2, 21, 6),
(85, 280, 1, NULL, '2023-08-03 15:44:14.025959', 2, 22, 6),
(86, 300, 1, NULL, '2023-08-03 15:44:14.062726', 2, 22, 6),
(87, 320, 1, NULL, '2023-08-03 15:44:14.072050', 2, 22, 6),
(88, 340, 1, NULL, '2023-08-03 15:44:14.114339', 2, 22, 6),
(89, 360, 1, NULL, '2023-08-03 15:44:14.134507', 2, 23, 6),
(90, 380, 1, NULL, '2023-08-03 15:44:14.142293', 2, 23, 6),
(91, 400, 1, NULL, '2023-08-03 15:44:14.254898', 2, 23, 6),
(92, 420, 1, NULL, '2023-08-03 15:44:14.262889', 2, 23, 6),
(93, 440, 1, NULL, '2023-08-03 15:44:14.278741', 2, 24, 6),
(94, 460, 1, NULL, '2023-08-03 15:44:14.344517', 2, 24, 6),
(95, 480, 1, NULL, '2023-08-03 15:44:14.364699', 2, 24, 6),
(96, 500, 1, NULL, '2023-08-03 15:44:14.426227', 2, 24, 6),
(97, 520, 1, NULL, '2023-08-03 15:44:14.512453', 2, 25, 6),
(98, 540, 1, NULL, '2023-08-03 15:44:14.537200', 2, 25, 6),
(99, 560, 1, NULL, '2023-08-03 15:44:14.646394', 2, 25, 6),
(100, 580, 1, NULL, '2023-08-03 15:44:14.657740', 2, 25, 6);

-- --------------------------------------------------------

--
-- Table structure for table `mud_mudpumpmasterdata`
--

CREATE TABLE `mud_mudpumpmasterdata` (
  `id` int NOT NULL,
  `linear_size` double DEFAULT NULL,
  `max_discharge_pressure` double DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) NOT NULL,
  `is_superadmin` int NOT NULL,
  `company_id` int DEFAULT NULL,
  `mud_pump_master_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `mud_mudpumpmasterdata`
--

INSERT INTO `mud_mudpumpmasterdata` (`id`, `linear_size`, `max_discharge_pressure`, `status`, `created`, `is_superadmin`, `company_id`, `mud_pump_master_id`) VALUES
(1, 5, 5000, 1, '2023-08-03 15:35:05.632288', 0, 20, 1),
(2, 5.5, 4500, 1, '2023-08-03 15:35:05.729712', 0, 20, 1),
(3, 6, 4000, 1, '2023-08-03 15:35:05.737450', 0, 20, 1),
(4, 6.5, 3500, 1, '2023-08-03 15:35:05.750298', 0, 20, 1),
(5, 5, 5300, 1, '2023-08-03 15:35:19.721596', 0, 2, 2),
(6, 5.5, 5000, 1, '2023-08-03 15:35:19.732735', 0, 2, 2),
(7, 6, 4800, 1, '2023-08-03 15:35:19.799330', 0, 2, 2),
(8, 6.5, 4200, 1, '2023-08-03 15:35:19.809224', 0, 2, 2),
(9, 5, 5000, 1, '2023-08-03 15:36:23.678033', 0, 20, 3),
(10, 5.5, 4500, 1, '2023-08-03 15:36:23.732242', 0, 20, 3),
(11, 6, 4000, 1, '2023-08-03 15:36:23.743109', 0, 20, 3),
(12, 6.5, 3500, 1, '2023-08-03 15:36:23.770172', 0, 20, 3);

-- --------------------------------------------------------

--
-- Table structure for table `mud_mudpumpmasterflowrate`
--

CREATE TABLE `mud_mudpumpmasterflowrate` (
  `id` int NOT NULL,
  `flowrate` double DEFAULT NULL,
  `status` int NOT NULL,
  `order` int DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `is_superadmin` int NOT NULL,
  `company_id` int DEFAULT NULL,
  `mud_pump_master_speed_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `mud_mudpumpmasterflowrate`
--

INSERT INTO `mud_mudpumpmasterflowrate` (`id`, `flowrate`, `status`, `order`, `created`, `is_superadmin`, `company_id`, `mud_pump_master_speed_id`) VALUES
(1, 252, 1, NULL, '2023-08-03 15:35:06.018576', 0, 20, 1),
(2, 305, 1, NULL, '2023-08-03 15:35:06.220010', 0, 20, 1),
(3, 364, 1, NULL, '2023-08-03 15:35:06.260268', 0, 20, 1),
(4, 427, 1, NULL, '2023-08-03 15:35:06.269938', 0, 20, 1),
(5, 280, 1, NULL, '2023-08-03 15:35:06.316502', 0, 20, 2),
(6, 339, 1, NULL, '2023-08-03 15:35:06.371944', 0, 20, 2),
(7, 404, 1, NULL, '2023-08-03 15:35:06.450931', 0, 20, 2),
(8, 474, 1, NULL, '2023-08-03 15:35:06.526385', 0, 20, 2),
(9, 337, 1, NULL, '2023-08-03 15:35:06.613672', 0, 20, 3),
(10, 407, 1, NULL, '2023-08-03 15:35:06.650021', 0, 20, 3),
(11, 485, 1, NULL, '2023-08-03 15:35:06.799084', 0, 20, 3),
(12, 569, 1, NULL, '2023-08-03 15:35:06.866985', 0, 20, 3),
(13, 365, 1, NULL, '2023-08-03 15:35:07.255638', 0, 20, 4),
(14, 441, 1, NULL, '2023-08-03 15:35:07.303031', 0, 20, 4),
(15, 525, 1, NULL, '2023-08-03 15:35:07.312984', 0, 20, 4),
(16, 616, 1, NULL, '2023-08-03 15:35:07.373489', 0, 20, 4),
(17, 393, 1, NULL, '2023-08-03 15:35:07.455406', 0, 20, 5),
(18, 475, 1, NULL, '2023-08-03 15:35:07.462646', 0, 20, 5),
(19, 565, 1, NULL, '2023-08-03 15:35:07.492345', 0, 20, 5),
(20, 664, 1, NULL, '2023-08-03 15:35:07.503824', 0, 20, 5),
(21, 252, 1, NULL, '2023-08-03 15:35:19.839493', 0, 2, 6),
(22, 305, 1, NULL, '2023-08-03 15:35:19.849630', 0, 2, 6),
(23, 364, 1, NULL, '2023-08-03 15:35:19.880382', 0, 2, 6),
(24, 427, 1, NULL, '2023-08-03 15:35:19.889816', 0, 2, 6),
(25, 280, 1, NULL, '2023-08-03 15:35:19.985618', 0, 2, 7),
(26, 339, 1, NULL, '2023-08-03 15:35:19.993578', 0, 2, 7),
(27, 404, 1, NULL, '2023-08-03 15:35:20.092467', 0, 2, 7),
(28, 474, 1, NULL, '2023-08-03 15:35:20.179769', 0, 2, 7),
(29, 337, 1, NULL, '2023-08-03 15:35:20.294501', 0, 2, 8),
(30, 407, 1, NULL, '2023-08-03 15:35:20.441584', 0, 2, 8),
(31, 485, 1, NULL, '2023-08-03 15:35:20.494729', 0, 2, 8),
(32, 569, 1, NULL, '2023-08-03 15:35:20.542691', 0, 2, 8),
(33, 365, 1, NULL, '2023-08-03 15:35:20.745376', 0, 2, 9),
(34, 441, 1, NULL, '2023-08-03 15:35:20.815005', 0, 2, 9),
(35, 525, 1, NULL, '2023-08-03 15:35:20.823801', 0, 2, 9),
(36, 616, 1, NULL, '2023-08-03 15:35:20.831515', 0, 2, 9),
(37, 393, 1, NULL, '2023-08-03 15:35:20.964643', 0, 2, 10),
(38, 475, 1, NULL, '2023-08-03 15:35:20.972350', 0, 2, 10),
(39, 565, 1, NULL, '2023-08-03 15:35:20.980337', 0, 2, 10),
(40, 664, 1, NULL, '2023-08-03 15:35:21.037751', 0, 2, 10),
(41, 252, 1, NULL, '2023-08-03 15:36:23.845996', 0, 20, 11),
(42, 305, 1, NULL, '2023-08-03 15:36:23.852914', 0, 20, 11),
(43, 364, 1, NULL, '2023-08-03 15:36:23.862162', 0, 20, 11),
(44, 427, 1, NULL, '2023-08-03 15:36:23.867737', 0, 20, 11),
(45, 280, 1, NULL, '2023-08-03 15:36:23.900340', 0, 20, 12),
(46, 339, 1, NULL, '2023-08-03 15:36:23.907761', 0, 20, 12),
(47, 404, 1, NULL, '2023-08-03 15:36:23.915625', 0, 20, 12),
(48, 474, 1, NULL, '2023-08-03 15:36:23.921655', 0, 20, 12),
(49, 337, 1, NULL, '2023-08-03 15:36:23.965851', 0, 20, 13),
(50, 407, 1, NULL, '2023-08-03 15:36:23.976806', 0, 20, 13),
(51, 485, 1, NULL, '2023-08-03 15:36:23.986027', 0, 20, 13),
(52, 569, 1, NULL, '2023-08-03 15:36:23.993229', 0, 20, 13),
(53, 365, 1, NULL, '2023-08-03 15:36:24.007671', 0, 20, 14),
(54, 441, 1, NULL, '2023-08-03 15:36:24.013675', 0, 20, 14),
(55, 525, 1, NULL, '2023-08-03 15:36:24.020653', 0, 20, 14),
(56, 616, 1, NULL, '2023-08-03 15:36:24.028250', 0, 20, 14),
(57, 393, 1, NULL, '2023-08-03 15:36:24.090561', 0, 20, 15),
(58, 475, 1, NULL, '2023-08-03 15:36:24.101612', 0, 20, 15),
(59, 565, 1, NULL, '2023-08-03 15:36:24.126069', 0, 20, 15),
(60, 664, 1, NULL, '2023-08-03 15:36:24.133183', 0, 20, 15);

-- --------------------------------------------------------

--
-- Table structure for table `mud_mudpumpmasterspeed`
--

CREATE TABLE `mud_mudpumpmasterspeed` (
  `id` int NOT NULL,
  `pump_speed` int DEFAULT NULL,
  `is_superadmin` int NOT NULL,
  `company_id` int DEFAULT NULL,
  `mud_pump_master_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `mud_mudpumpmasterspeed`
--

INSERT INTO `mud_mudpumpmasterspeed` (`id`, `pump_speed`, `is_superadmin`, `company_id`, `mud_pump_master_id`) VALUES
(1, 90, 0, 20, 1),
(2, 100, 0, 20, 1),
(3, 120, 0, 20, 1),
(4, 130, 0, 20, 1),
(5, 140, 0, 20, 1),
(6, 90, 0, 2, 2),
(7, 100, 0, 2, 2),
(8, 120, 0, 2, 2),
(9, 130, 0, 2, 2),
(10, 140, 0, 2, 2),
(11, 90, 0, 20, 3),
(12, 100, 0, 20, 3),
(13, 120, 0, 20, 3),
(14, 130, 0, 20, 3),
(15, 140, 0, 20, 3);

-- --------------------------------------------------------

--
-- Table structure for table `mud_mudpumpspeed`
--

CREATE TABLE `mud_mudpumpspeed` (
  `id` int NOT NULL,
  `pump_speed` int DEFAULT NULL,
  `status` int NOT NULL,
  `company_id` int DEFAULT NULL,
  `mud_pump_id` int DEFAULT NULL,
  `well_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `mud_mudpumpspeed`
--

INSERT INTO `mud_mudpumpspeed` (`id`, `pump_speed`, `status`, `company_id`, `mud_pump_id`, `well_id`) VALUES
(1, 80, 1, 1, 1, 1),
(2, 90, 1, 1, 1, 1),
(3, 100, 1, 1, 1, 1),
(4, 110, 1, 1, 1, 1),
(5, 120, 1, 1, 1, 1),
(6, 90, 1, 2, 2, 2),
(7, 100, 1, 2, 2, 2),
(8, 110, 1, 2, 2, 2),
(9, 120, 1, 2, 2, 2),
(10, 130, 1, 2, 2, 2),
(11, 80, 0, 2, 3, 6),
(12, 90, 0, 2, 3, 6),
(13, 80, 0, 20, 4, 5),
(14, 100, 0, 2, 3, 6),
(15, 90, 0, 20, 4, 5),
(16, 120, 0, 2, 3, 6),
(17, 100, 0, 20, 4, 5),
(18, 130, 0, 2, 3, 6),
(19, 120, 0, 20, 4, 5),
(20, 130, 0, 20, 4, 5),
(21, 90, 1, 2, 5, 6),
(22, 100, 1, 2, 5, 6),
(23, 110, 1, 2, 5, 6),
(24, 120, 1, 2, 5, 6),
(25, 130, 1, 2, 5, 6);

-- --------------------------------------------------------

--
-- Table structure for table `mud_pumpmanufacturer`
--

CREATE TABLE `mud_pumpmanufacturer` (
  `id` int NOT NULL,
  `is_superadmin` int NOT NULL,
  `name` varchar(250) DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) NOT NULL,
  `company_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `mud_pumpmanufacturer`
--

INSERT INTO `mud_pumpmanufacturer` (`id`, `is_superadmin`, `name`, `status`, `created`, `company_id`) VALUES
(1, 0, 'Cameron Simon 1', 1, '2023-06-28 12:11:13.210585', 1),
(2, 0, 'Cameron', 1, '2023-08-03 15:33:29.358905', 2),
(3, 0, 'Cameron', 1, '2023-08-03 15:33:31.045162', 20);

-- --------------------------------------------------------

--
-- Table structure for table `mud_pumps`
--

CREATE TABLE `mud_pumps` (
  `id` int NOT NULL,
  `name` varchar(250) DEFAULT NULL,
  `type` varchar(250) DEFAULT NULL,
  `unit` varchar(255) DEFAULT NULL,
  `stroke_length` double DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) NOT NULL,
  `is_superadmin` int NOT NULL,
  `company_id` int DEFAULT NULL,
  `pump_manufacturer_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `mud_pumps`
--

INSERT INTO `mud_pumps` (`id`, `name`, `type`, `unit`, `stroke_length`, `status`, `created`, `is_superadmin`, `company_id`, `pump_manufacturer_id`) VALUES
(1, 'OPPY Pump', 'Triplex', 'API', 11, 1, '2023-08-03 15:35:05.549342', 0, 20, 3),
(2, 'EX Pump', 'Triplex', 'API', 11, 1, '2023-08-03 15:35:19.592709', 0, 2, 2),
(3, 'OPPY Pump', 'Triplex', 'API', 11, 1, '2023-08-03 15:36:23.634698', 0, 20, 3);

-- --------------------------------------------------------

--
-- Table structure for table `notifications_notification`
--

CREATE TABLE `notifications_notification` (
  `id` int NOT NULL,
  `level` varchar(20) NOT NULL,
  `unread` tinyint(1) NOT NULL,
  `actor_object_id` varchar(255) NOT NULL,
  `verb` varchar(255) NOT NULL,
  `description` longtext,
  `target_object_id` varchar(255) DEFAULT NULL,
  `action_object_object_id` varchar(255) DEFAULT NULL,
  `timestamp` datetime(6) NOT NULL,
  `public` tinyint(1) NOT NULL,
  `action_object_content_type_id` int DEFAULT NULL,
  `actor_content_type_id` int NOT NULL,
  `recipient_id` int NOT NULL,
  `target_content_type_id` int DEFAULT NULL,
  `deleted` tinyint(1) NOT NULL,
  `emailed` tinyint(1) NOT NULL,
  `data` longtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `notifications_notification`
--

INSERT INTO `notifications_notification` (`id`, `level`, `unread`, `actor_object_id`, `verb`, `description`, `target_object_id`, `action_object_object_id`, `timestamp`, `public`, `action_object_content_type_id`, `actor_content_type_id`, `recipient_id`, `target_content_type_id`, `deleted`, `emailed`, `data`) VALUES
(1, 'info', 1, '1', 'New enquiry have been received', 'New Enquiry received Name Venkat', NULL, '1', '2023-07-03 16:50:28.662382', 1, 8, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/enquiries\\\"}\"}'),
(2, 'info', 1, '1', 'New enquiry have been received', 'New Enquiry received Name Kumar', NULL, '2', '2023-07-06 11:17:29.993420', 1, 8, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/enquiries\\\"}\"}'),
(3, 'info', 1, '1', 'New enquiry have been received', 'New Enquiry received Name Kumar', NULL, '3', '2023-07-06 11:33:05.052539', 1, 8, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/enquiries\\\"}\"}'),
(4, 'info', 1, '1', 'New enquiry have been received', 'New Enquiry received Name Kumar', NULL, '4', '2023-07-06 11:35:28.248001', 1, 8, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/enquiries\\\"}\"}'),
(5, 'info', 1, '1', 'New enquiry have been received', 'New Enquiry received Name Mageshwari', NULL, '5', '2023-07-14 12:34:46.268311', 1, 8, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/enquiries\\\"}\"}'),
(6, 'info', 1, '1', 'New enquiry have been received', 'New Enquiry received Name Subash', NULL, '6', '2023-07-20 13:39:19.089558', 1, 8, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/enquiries\\\"}\"}'),
(7, 'info', 0, '1', 'New enquiry have been received', 'New Enquiry received Name Dev', NULL, '7', '2023-07-22 16:25:08.055244', 1, 8, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/enquiries\\\"}\"}'),
(8, 'info', 1, '37', 'License upgraded', 'Received License Upgrade request from Arujun', NULL, NULL, '2023-07-23 16:56:17.476041', 1, NULL, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/company/views/5/CompanyPlan\\\"}\"}'),
(9, 'info', 1, '37', 'License upgraded', 'Received License Upgrade request from Arujun', NULL, NULL, '2023-07-23 16:56:32.645126', 1, NULL, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/company/views/5/CompanyPlan\\\"}\"}'),
(10, 'info', 1, '38', 'License upgraded', 'Received License Upgrade request from Dev', NULL, NULL, '2023-07-23 17:15:58.564158', 1, NULL, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/company/views/6/Enterprise\\\"}\"}'),
(11, 'info', 1, '38', 'License upgraded', 'Received License Upgrade request from Dev', NULL, NULL, '2023-07-23 17:16:00.835063', 1, NULL, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/company/views/6/Enterprise\\\"}\"}'),
(12, 'info', 1, '38', 'License upgraded', 'Received License Upgrade request from Dev', NULL, NULL, '2023-07-23 17:16:01.028312', 1, NULL, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/company/views/6/Enterprise\\\"}\"}'),
(13, 'info', 1, '38', 'License upgraded', 'Received License Upgrade request from Dev', NULL, NULL, '2023-07-23 17:16:10.916765', 1, NULL, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/company/views/6/Enterprise\\\"}\"}'),
(14, 'info', 1, '38', 'License upgraded', 'Received License Upgrade request from Dev', NULL, NULL, '2023-07-23 17:16:22.406136', 1, NULL, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/company/views/6/Enterprise\\\"}\"}'),
(15, 'info', 1, '38', 'License upgraded', 'Received License Upgrade request from Dev', NULL, NULL, '2023-07-23 17:16:22.574948', 1, NULL, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/company/views/6/Enterprise\\\"}\"}'),
(16, 'info', 1, '38', 'License upgraded', 'Received License Upgrade request from Dev', NULL, NULL, '2023-07-23 17:16:22.740174', 1, NULL, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/company/views/6/Enterprise\\\"}\"}'),
(17, 'info', 1, '38', 'License upgraded', 'Received License Upgrade request from Dev', NULL, NULL, '2023-07-23 17:16:46.974890', 1, NULL, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/company/views/6/Enterprise\\\"}\"}'),
(18, 'info', 1, '38', 'New Ticket', 'New Ticket Received From Dev', NULL, '1', '2023-07-23 17:17:24.237938', 1, 73, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/ticket/queries\\\"}\"}'),
(20, 'info', 0, '40', 'License upgraded', 'Received License Upgrade request from Arujun', NULL, NULL, '2023-07-25 10:50:22.223733', 1, NULL, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/company/views/8/CompanyPlan\\\"}\"}'),
(21, 'info', 1, '45', 'License upgraded', 'Received License Upgrade request from Luke', NULL, NULL, '2023-07-25 12:55:27.307589', 1, NULL, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/company/views/45/Individual\\\"}\"}'),
(22, 'info', 0, '43', 'License upgraded', 'Received License Upgrade request from Jagadish Kumar JK', NULL, NULL, '2023-07-25 14:55:06.473145', 1, NULL, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/company/views/9/Enterprise\\\"}\"}'),
(23, 'info', 1, '49', 'License upgraded', 'Received License Upgrade request from Arujun', NULL, NULL, '2023-07-26 11:42:38.251872', 1, NULL, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/company/views/12/CompanyPlan\\\"}\"}'),
(24, 'info', 0, '49', 'License upgraded', 'Received License Upgrade request from Arujun', NULL, NULL, '2023-07-26 11:43:47.253891', 1, NULL, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/company/views/12/Enterprise\\\"}\"}'),
(25, 'info', 1, '16', 'License upgraded', 'Received License Upgrade request from Arujun', NULL, NULL, '2023-07-26 12:24:50.717371', 1, NULL, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/company/views/16/Individual\\\"}\"}'),
(26, 'info', 1, '17', 'License upgraded', 'Received License Upgrade request from dev', NULL, NULL, '2023-07-26 13:49:03.599876', 1, NULL, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/company/views/13/CompanyPlan\\\"}\"}'),
(27, 'info', 0, '17', 'License upgraded', 'Received License Upgrade request from dev', NULL, NULL, '2023-07-26 16:53:00.828526', 1, NULL, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/company/views/13/Enterprise\\\"}\"}'),
(28, 'info', 1, '20', 'New User', 'assigned as Creator', NULL, '21', '2023-07-31 12:22:34.580365', 1, 4, 4, 21, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/users\\\"}\"}'),
(29, 'info', 0, '20', 'License upgraded', 'Received License Upgrade request from Jagadish', NULL, NULL, '2023-07-31 12:25:22.041650', 1, NULL, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/company/views/16/CompanyPlan\\\"}\"}'),
(30, 'info', 1, '1', 'New enquiry have been received', 'New Enquiry received Name Shankar', NULL, '27', '2023-07-31 14:30:29.598098', 1, 8, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/enquiries\\\"}\"}'),
(31, 'info', 1, '20', 'New User', 'assigned as Creator', NULL, '23', '2023-07-31 15:11:26.987190', 1, 4, 4, 23, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/users\\\"}\"}'),
(32, 'info', 1, '1', 'New enquiry have been received', 'New Enquiry received Name Jagadish', NULL, '28', '2023-07-31 15:47:05.309597', 1, 8, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/enquiries\\\"}\"}'),
(33, 'info', 1, '24', 'License upgraded', 'Received License Upgrade request from Arujun', NULL, NULL, '2023-07-31 15:49:49.555944', 1, NULL, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/company/views/18/CompanyPlan\\\"}\"}'),
(34, 'info', 0, '24', 'New Ticket', 'New Ticket Received From Arujun', NULL, '3', '2023-08-02 14:41:02.536562', 1, 73, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/ticket/queries\\\"}\"}'),
(35, 'info', 0, '24', 'New Ticket', 'New Ticket Received From Arujun', NULL, '5', '2023-08-02 15:45:39.460723', 1, 73, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/ticket/queries\\\"}\"}'),
(36, 'info', 0, '15', 'New Ticket', 'New Ticket Received From Iwells', NULL, '6', '2023-08-03 12:15:28.280240', 1, 73, 4, 1, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/ticket/queries\\\"}\"}'),
(37, 'info', 1, '26', 'Project got assigned', 'You have been assigned to Poduri', NULL, '9', '2023-08-03 15:18:21.455033', 1, 17, 4, 26, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/projects/9\\\"}\"}'),
(38, 'info', 1, '11', 'Project got assigned', 'You have been assigned to Poduri', NULL, '10', '2023-08-03 15:18:25.460142', 1, 17, 4, 11, NULL, 0, 0, '{\"extra_data\": \"{\\\"url\\\": \\\"http://dev.hydraulics.mo.vc/projects/10\\\"}\"}');

-- --------------------------------------------------------

--
-- Table structure for table `pressure_pressure`
--

CREATE TABLE `pressure_pressure` (
  `id` int NOT NULL,
  `measured_depth` double DEFAULT NULL,
  `true_vertical_depth` double DEFAULT NULL,
  `pore_pressure` double DEFAULT NULL,
  `fracture_pressure` double DEFAULT NULL,
  `comments` varchar(250) DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) DEFAULT NULL,
  `pressure_unit` varchar(250) DEFAULT NULL,
  `company_id` int DEFAULT NULL,
  `well_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `projects_projectblock`
--

CREATE TABLE `projects_projectblock` (
  `id` int NOT NULL,
  `block_name` varchar(255) NOT NULL,
  `status` int NOT NULL,
  `project_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `projects_projectblock`
--

INSERT INTO `projects_projectblock` (`id`, `block_name`, `status`, `project_id`) VALUES
(1, 'Block 1', 1, 1),
(2, 'OML 112', 1, 2),
(3, 'Block 1', 1, 3),
(6, 'Block N1', 1, 6),
(7, 'EV-1 Moinesti', 1, 7),
(8, 'EV-1 Moinesti', 1, 8),
(9, 'EV-1 Moinesti', 1, 9),
(10, 'EV-1 Moinesti', 1, 10),
(11, 'blk', 1, 11),
(12, 'blk', 1, 12);

-- --------------------------------------------------------

--
-- Table structure for table `projects_projectfield`
--

CREATE TABLE `projects_projectfield` (
  `id` int NOT NULL,
  `field_name` varchar(255) NOT NULL,
  `status` int NOT NULL,
  `block_id` int DEFAULT NULL,
  `project_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `projects_projectfield`
--

INSERT INTO `projects_projectfield` (`id`, `field_name`, `status`, `block_id`, `project_id`) VALUES
(1, 'Field', 1, 1, 1),
(2, 'Okoro', 1, 2, 2),
(3, 'Field1', 1, 3, 3),
(6, 'Field N1', 1, 6, 6),
(7, 'Poduri', 1, 7, 7),
(8, 'Poduri', 1, 8, 8),
(9, 'Poduri', 1, 9, 9),
(10, 'Poduri', 1, 10, 10),
(11, 'fld', 1, 11, 11),
(12, 'flk', 1, 12, 12);

-- --------------------------------------------------------

--
-- Table structure for table `projects_projects`
--

CREATE TABLE `projects_projects` (
  `id` int NOT NULL,
  `project_name` varchar(255) NOT NULL,
  `block` varchar(255) DEFAULT NULL,
  `field` varchar(255) DEFAULT NULL,
  `unit` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `status` int NOT NULL,
  `company_id` int DEFAULT NULL,
  `country_id` int DEFAULT NULL,
  `created_by_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `projects_projects`
--

INSERT INTO `projects_projects` (`id`, `project_name`, `block`, `field`, `unit`, `created`, `status`, `company_id`, `country_id`, `created_by_id`) VALUES
(1, 'Project 1', NULL, NULL, 'MIXED', '2023-06-27 18:11:24.149243', 1, 1, 99, 10),
(2, 'Okoro', NULL, NULL, 'API', '2023-06-29 14:31:26.299619', 1, 2, 99, 11),
(3, 'Sample Project', NULL, NULL, 'API', '2023-07-28 18:10:45.753084', 1, 14, 99, 18),
(6, 'PRO 1', NULL, NULL, 'API', '2023-07-28 18:26:17.844598', 1, 14, 99, 18),
(7, 'Test Project', NULL, NULL, 'MIXED', '2023-07-29 12:12:02.470497', 1, 14, 176, 18),
(8, 'Test Project', 'EV-1 Moinesti', NULL, 'MIXED', '2023-08-01 14:50:36.281920', 1, 18, 176, NULL),
(9, 'Poduri', 'EV-1 Moinesti', NULL, 'MIXED', '2023-08-03 15:17:25.082681', 1, 20, 176, NULL),
(10, 'Poduri', 'EV-1 Moinesti', NULL, 'MIXED', '2023-08-03 15:17:26.293560', 1, 2, 176, NULL),
(11, 'PLK', NULL, NULL, 'MIXED', '2023-08-04 10:12:09.845009', 1, 18, 99, 24),
(12, 'PLK', NULL, NULL, 'MIXED', '2023-08-04 10:13:49.845713', 1, 18, 99, 24);

-- --------------------------------------------------------

--
-- Table structure for table `projects_projectusers`
--

CREATE TABLE `projects_projectusers` (
  `id` int NOT NULL,
  `created` datetime(6) NOT NULL,
  `status` int NOT NULL,
  `project_id` int DEFAULT NULL,
  `role_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `projects_projectusers`
--

INSERT INTO `projects_projectusers` (`id`, `created`, `status`, `project_id`, `role_id`, `user_id`) VALUES
(1, '2023-06-27 18:11:24.199207', 1, 1, 2, NULL),
(2, '2023-06-29 14:31:26.417921', 1, 2, 2, NULL),
(3, '2023-07-28 18:10:45.766012', 1, 3, 2, NULL),
(6, '2023-07-28 18:26:17.883337', 1, 6, 2, NULL),
(7, '2023-07-29 12:12:07.012365', 1, 7, 2, NULL),
(11, '2023-08-03 15:19:35.438685', 1, 9, 2, NULL),
(12, '2023-08-03 15:19:48.323971', 1, 10, 2, NULL),
(14, '2023-08-04 10:11:37.723756', 1, 8, 2, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `rheogram_date`
--

CREATE TABLE `rheogram_date` (
  `id` int NOT NULL,
  `selected_model` varchar(255) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) DEFAULT NULL,
  `timestamp` int DEFAULT NULL,
  `time` time(6) DEFAULT NULL,
  `company_id` int DEFAULT NULL,
  `muddata_id` int DEFAULT NULL,
  `well_id` bigint DEFAULT NULL,
  `well_phase_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `rheogram_date`
--

INSERT INTO `rheogram_date` (`id`, `selected_model`, `date`, `status`, `created`, `timestamp`, `time`, `company_id`, `muddata_id`, `well_id`, `well_phase_id`) VALUES
(1, '4', NULL, 1, '2023-07-14 11:19:54.110439', NULL, NULL, 2, NULL, 2, 3);

-- --------------------------------------------------------

--
-- Table structure for table `rheogram_rpm`
--

CREATE TABLE `rheogram_rpm` (
  `id` int NOT NULL,
  `rheogram_rpm` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `rheogram_rpm`
--

INSERT INTO `rheogram_rpm` (`id`, `rheogram_rpm`) VALUES
(1, '3'),
(2, '6'),
(3, '100'),
(4, '200'),
(5, '300'),
(6, '600');

-- --------------------------------------------------------

--
-- Table structure for table `rheogram_sections`
--

CREATE TABLE `rheogram_sections` (
  `id` int NOT NULL,
  `section_name` varchar(100) DEFAULT NULL,
  `from_depth` double DEFAULT NULL,
  `todepth` double DEFAULT NULL,
  `status` int NOT NULL,
  `rheogram_date_id` int DEFAULT NULL,
  `well_phase_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `rheogram_sections`
--

INSERT INTO `rheogram_sections` (`id`, `section_name`, `from_depth`, `todepth`, `status`, `rheogram_date_id`, `well_phase_id`) VALUES
(1, '968.0-2304.0', 968, 2304, 1, 1, 3);

-- --------------------------------------------------------

--
-- Table structure for table `rights`
--

CREATE TABLE `rights` (
  `id` int NOT NULL,
  `status` int NOT NULL,
  `company_id` int DEFAULT NULL,
  `module_id` int DEFAULT NULL,
  `role_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `rights`
--

INSERT INTO `rights` (`id`, `status`, `company_id`, `module_id`, `role_id`) VALUES
(1, 1, 2, 1, 1),
(2, 1, 2, 2, 1),
(3, 1, 2, 3, 1),
(4, 1, 2, 4, 1),
(5, 1, 2, 5, 1),
(6, 1, 2, 6, 1),
(7, 1, 2, 7, 1),
(8, 1, 2, 8, 1),
(9, 1, 2, 9, 1),
(10, 1, 2, 10, 1),
(11, 1, 2, 11, 1),
(12, 1, 2, 12, 1),
(13, 1, 2, 13, 1),
(14, 1, 2, 14, 1),
(15, 1, 2, 15, 1),
(16, 1, 2, 16, 1),
(17, 1, 2, 17, 1),
(18, 1, 2, 18, 1),
(19, 1, 2, 19, 1);

-- --------------------------------------------------------

--
-- Table structure for table `rig_information`
--

CREATE TABLE `rig_information` (
  `id` int NOT NULL,
  `rig_name` varchar(60) DEFAULT NULL,
  `rig_contractor` varchar(60) DEFAULT NULL,
  `rig_type` varchar(60) DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) DEFAULT NULL,
  `company_id` int DEFAULT NULL,
  `well_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `rig_information`
--

INSERT INTO `rig_information` (`id`, `rig_name`, `rig_contractor`, `rig_type`, `status`, `created`, `company_id`, `well_id`) VALUES
(1, 'Test Rig 1', 'Contractor 1', 'Jack Up', 1, '2023-07-20 13:25:18.201299', 2, 2),
(2, 'Bentec E250', 'MND Drilling Services', 'Land Rig', 1, '2023-08-03 15:28:05.702837', 2, 6),
(3, 'Bentec E250', 'MND Drilling Services', 'Land Rig', 1, '2023-08-03 15:28:15.684119', 20, 5);

-- --------------------------------------------------------

--
-- Table structure for table `Sections`
--

CREATE TABLE `Sections` (
  `id` int NOT NULL,
  `section_name` varchar(100) DEFAULT NULL,
  `from_depth` double DEFAULT NULL,
  `todepth` double DEFAULT NULL,
  `selected_model` varchar(255) DEFAULT NULL,
  `status` int NOT NULL,
  `date` date DEFAULT NULL,
  `timestamp` int DEFAULT NULL,
  `time` time(6) DEFAULT NULL,
  `company_id` int DEFAULT NULL,
  `well_id` bigint DEFAULT NULL,
  `well_phase_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Sections`
--

INSERT INTO `Sections` (`id`, `section_name`, `from_depth`, `todepth`, `selected_model`, `status`, `date`, `timestamp`, `time`, `company_id`, `well_id`, `well_phase_id`) VALUES
(1, '968.0-2304.0', 968, 2304, '4', 1, NULL, NULL, NULL, 2, 2, 3);

-- --------------------------------------------------------

--
-- Table structure for table `surfacepipe_surfacepipe`
--

CREATE TABLE `surfacepipe_surfacepipe` (
  `id` int NOT NULL,
  `rating` int DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) DEFAULT NULL,
  `company_id` int DEFAULT NULL,
  `well_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `surfacepipe_surfacepipe`
--

INSERT INTO `surfacepipe_surfacepipe` (`id`, `rating`, `status`, `created`, `company_id`, `well_id`) VALUES
(1, 5000, 1, '2023-07-20 13:25:47.580061', 2, 2),
(2, 5000, 1, '2023-08-03 15:29:07.608303', 2, 6),
(3, 5000, 1, '2023-08-03 15:29:08.143072', 20, 5);

-- --------------------------------------------------------

--
-- Table structure for table `surfacepipe_surfacepipedata`
--

CREATE TABLE `surfacepipe_surfacepipedata` (
  `id` int NOT NULL,
  `name` varchar(30) DEFAULT NULL,
  `length` varchar(30) DEFAULT NULL,
  `identity` varchar(30) DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) DEFAULT NULL,
  `company_id` int DEFAULT NULL,
  `surfacepipe_id` int DEFAULT NULL,
  `well_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `surfacepipe_surfacepipedata`
--

INSERT INTO `surfacepipe_surfacepipedata` (`id`, `name`, `length`, `identity`, `status`, `created`, `company_id`, `surfacepipe_id`, `well_id`) VALUES
(1, 'Mud Pump to Rig Floor', '100', '4.276', 1, '2023-07-20 13:25:47.662730', 2, 1, 2),
(2, 'Standpipe to Kelly Hose', '100', '4.276', 1, '2023-07-20 13:25:47.731968', 2, 1, 2),
(3, 'Kelly Hose to Top Drive', '30', '2.5', 1, '2023-07-20 13:25:47.746553', 2, 1, 2),
(4, 'Top Drive', '20', '2.5', 1, '2023-07-20 13:25:47.768033', 2, 1, 2),
(5, 'Mud Pump to Rig Floor', '100', '4.276', 1, '2023-08-03 15:29:07.669446', 2, 2, 6),
(6, 'Standpipe to Kelly Hose', '100', '4.276', 1, '2023-08-03 15:29:07.708730', 2, 2, 6),
(7, 'Kelly Hose to Top Drive', '90', '2.5', 1, '2023-08-03 15:29:07.717068', 2, 2, 6),
(8, 'Top Drive', '20', '2.5', 1, '2023-08-03 15:29:07.872347', 2, 2, 6),
(9, 'Mud Pump to Rig Floor', '100', '4.276', 1, '2023-08-03 15:29:08.220461', 20, 3, 5),
(10, 'Standpipe to Kelly Hose', '100', '4.276', 1, '2023-08-03 15:29:08.282768', 20, 3, 5),
(11, 'Kelly Hose to Top Drive', '90', '2.5', 1, '2023-08-03 15:29:08.358702', 20, 3, 5),
(12, 'Top Drive', '20', '2.5', 1, '2023-08-03 15:29:08.364742', 20, 3, 5);

-- --------------------------------------------------------

--
-- Table structure for table `surfacepiping_names`
--

CREATE TABLE `surfacepiping_names` (
  `id` int NOT NULL,
  `surfacepiping_name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `surfacepiping_names`
--

INSERT INTO `surfacepiping_names` (`id`, `surfacepiping_name`) VALUES
(1, 'Mud Pump to Rig Floor'),
(2, 'Standpipe to Kelly Hose'),
(3, 'Kelly Hose to Top Drive'),
(4, 'Kelly'),
(5, 'Top Drive');

-- --------------------------------------------------------

--
-- Table structure for table `tickets`
--

CREATE TABLE `tickets` (
  `id` int NOT NULL,
  `title` varchar(50) DEFAULT NULL,
  `message` longtext,
  `sender` int DEFAULT NULL,
  `recipient` int DEFAULT NULL,
  `message_id` int DEFAULT NULL,
  `file_field` varchar(100) DEFAULT NULL,
  `status` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tickets`
--

INSERT INTO `tickets` (`id`, `title`, `message`, `sender`, `recipient`, `message_id`, `file_field`, `status`) VALUES
(1, '', '', 38, 1, NULL, '', 0),
(2, '', 'ij', 1, 38, 1, '', 0),
(3, 'app not working', 'app not working', 24, 1, NULL, '', 0),
(4, 'app not working', 'i will check', 1, 24, 3, '', 0),
(5, 'test', 'test', 24, 1, NULL, '', 0),
(6, 'Issues with Resolution ', 'Hello Team How are things going ', 15, 1, NULL, '', 0),
(7, 'Issues with Resolution ', 'Good and Not bad ', 1, 15, 6, '', 0),
(8, 'Issues with Resolution ', 'Good and Not bad ', 1, 15, 6, '', 0),
(9, 'Issues with Resolution ', 'Hello world ', 1, 15, 6, '', 0),
(10, 'Issues with Resolution ', 'No way', 15, 1, 6, '', 0),
(11, 'Issues with Resolution ', 'Hello world ', 1, 15, 6, '', 0);

-- --------------------------------------------------------

--
-- Table structure for table `userlog`
--

CREATE TABLE `userlog` (
  `id` int NOT NULL,
  `message` varchar(50) NOT NULL,
  `source_id` varchar(50) NOT NULL,
  `source_Type` varchar(50) NOT NULL,
  `time` datetime(6) NOT NULL,
  `user_id` int DEFAULT NULL,
  `from_id` int DEFAULT NULL,
  `licence_type` varchar(30) DEFAULT NULL,
  `project_id` int DEFAULT NULL,
  `well_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `userlog`
--

INSERT INTO `userlog` (`id`, `message`, `source_id`, `source_Type`, `time`, `user_id`, `from_id`, `licence_type`, `project_id`, `well_id`) VALUES
(1, 'Project Created', '1', 'Project', '2023-06-27 18:11:24.258912', 10, NULL, NULL, NULL, NULL),
(2, 'Well Created', '1', 'Well', '2023-06-27 18:17:20.473908', 10, NULL, NULL, NULL, NULL),
(3, 'Mud Pump Created', '1', 'Rig', '2023-06-28 12:17:09.594919', 10, NULL, NULL, NULL, NULL),
(4, 'Welltrajectory Created', '1', 'Welltrajectory', '2023-06-28 12:28:59.667627', 10, NULL, NULL, NULL, NULL),
(5, 'Project Created', '2', 'Project', '2023-06-29 14:31:26.511483', 11, NULL, NULL, NULL, NULL),
(6, 'Well Created', '2', 'Well', '2023-06-29 14:32:17.395569', 11, NULL, NULL, NULL, NULL),
(7, 'Welltrajectory Created', '2', 'Welltrajectory', '2023-07-11 10:38:11.644579', 11, NULL, NULL, NULL, NULL),
(8, 'Wellphases Created', '3', 'Wellphases', '2023-07-11 10:42:37.002882', 11, NULL, NULL, NULL, NULL),
(9, 'Wellphases Edited', '2', 'Wellphases', '2023-07-14 11:16:21.447085', 11, NULL, NULL, NULL, NULL),
(10, 'Wellphases Edited', '2', 'Wellphases', '2023-07-14 11:19:11.265903', 11, NULL, NULL, NULL, NULL),
(11, 'Mud Data Created', '3', 'Mud Data', '2023-07-14 11:19:38.210002', 11, NULL, NULL, NULL, NULL),
(12, 'Rheogram Created', '3', 'Rheogram', '2023-07-14 11:19:55.778577', 11, NULL, NULL, NULL, NULL),
(13, 'Drillbit Created', '1', 'Drillbit', '2023-07-14 11:20:35.559965', 11, NULL, NULL, NULL, NULL),
(14, 'BHA data Created', '1', 'BHA data', '2023-07-14 11:21:07.224290', 11, NULL, NULL, NULL, NULL),
(15, 'Rig Informations Created', '1', 'Rig', '2023-07-20 13:25:18.251949', 11, NULL, NULL, NULL, NULL),
(16, 'Surface pipe Created', '1', 'Rig', '2023-07-20 13:25:48.064856', 11, NULL, NULL, NULL, NULL),
(17, 'Mud Pump Created', '2', 'Rig', '2023-07-20 13:34:31.774266', 11, NULL, NULL, NULL, NULL),
(18, 'Project Deleted', '4', 'Project', '2023-07-29 11:01:18.693091', 18, 14, 'CompanyPlan', NULL, NULL),
(19, 'Project Deleted', '5', 'Project', '2023-07-29 11:01:34.937954', 18, 14, 'CompanyPlan', NULL, NULL),
(20, 'Project Created', '7', 'Project', '2023-07-29 12:12:07.471071', 18, 14, 'CompanyPlan', NULL, NULL),
(21, 'Well Created', '3', 'Well', '2023-07-29 12:14:18.103655', 18, 14, 'CompanyPlan', NULL, NULL),
(22, 'User Created', '21', 'User', '2023-07-31 12:22:34.597159', 20, 16, 'CompanyPlan', NULL, NULL),
(23, 'User Created', '23', 'User', '2023-07-31 15:11:27.367956', 20, 16, 'CompanyPlan', NULL, NULL),
(24, 'Project Created', '8', 'Project', '2023-08-01 14:50:36.375042', 24, 18, 'CompanyPlan', NULL, NULL),
(25, 'Well Created', '4', 'Well', '2023-08-01 14:52:12.591278', 24, 18, 'CompanyPlan', NULL, NULL),
(26, 'Project Created', '9', 'Project', '2023-08-03 15:17:25.202035', 26, 20, 'CompanyPlan', NULL, NULL),
(27, 'Project Created', '10', 'Project', '2023-08-03 15:17:26.404564', 11, 2, 'CompanyPlan', NULL, NULL),
(28, 'Project Edited', '9', 'Project', '2023-08-03 15:19:35.479420', 26, 20, 'CompanyPlan', NULL, NULL),
(29, 'Project Edited', '10', 'Project', '2023-08-03 15:19:48.332508', 11, 2, 'CompanyPlan', NULL, NULL),
(30, 'Well Created', '5', 'Well', '2023-08-03 15:26:34.379793', 26, 20, 'CompanyPlan', NULL, NULL),
(31, 'Well Created', '6', 'Well', '2023-08-03 15:26:35.512934', 11, 2, 'CompanyPlan', NULL, NULL),
(32, 'Rig Informations Created', '2', 'Rig', '2023-08-03 15:28:05.724813', 11, 2, 'CompanyPlan', NULL, NULL),
(33, 'Rig Informations Created', '3', 'Rig', '2023-08-03 15:28:15.749786', 26, 20, 'CompanyPlan', NULL, NULL),
(34, 'Surface pipe Created', '2', 'Rig', '2023-08-03 15:29:07.976263', 11, 2, 'CompanyPlan', NULL, NULL),
(35, 'Surface pipe Created', '3', 'Rig', '2023-08-03 15:29:08.432806', 26, 20, 'CompanyPlan', NULL, NULL),
(36, 'Mud Pump Created', '3', 'Rig', '2023-08-03 15:32:17.429849', 11, 2, 'CompanyPlan', NULL, NULL),
(37, 'Mud Pump Created', '4', 'Rig', '2023-08-03 15:32:17.830387', 26, 20, 'CompanyPlan', NULL, NULL),
(38, 'Mud Pump Deleted', '4', 'Rig', '2023-08-03 15:39:03.745625', 26, 20, 'CompanyPlan', NULL, NULL),
(39, 'Mud Pump Deleted', '3', 'Rig', '2023-08-03 15:39:05.885026', 11, 2, 'CompanyPlan', NULL, NULL),
(40, 'Mud Pump Created', '5', 'Rig', '2023-08-03 15:44:14.670676', 11, 2, 'CompanyPlan', NULL, NULL),
(41, 'Welltrajectory Created', '6', 'Welltrajectory', '2023-08-03 15:49:48.138913', 11, 2, 'CompanyPlan', NULL, NULL),
(42, 'Welltrajectory Created', '5', 'Welltrajectory', '2023-08-03 15:49:55.846366', 26, 20, 'CompanyPlan', NULL, NULL),
(43, 'Welltrajectory Edited', '5', 'Welltrajectory', '2023-08-03 15:57:05.668920', 26, 20, 'CompanyPlan', NULL, NULL),
(44, 'Welltrajectory Edited', '5', 'Welltrajectory', '2023-08-03 15:57:42.428367', 26, 20, 'CompanyPlan', NULL, NULL),
(45, 'Welltrajectory Edited', '5', 'Welltrajectory', '2023-08-03 15:58:32.664126', 26, 20, 'CompanyPlan', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `wellphases_casing`
--

CREATE TABLE `wellphases_casing` (
  `id` int NOT NULL,
  `nominal_od` double DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `inside_diameter` double DEFAULT NULL,
  `grade` varchar(30) DEFAULT NULL,
  `casing_range` varchar(30) DEFAULT NULL,
  `connection_type` varchar(30) DEFAULT NULL,
  `connection_od` double DEFAULT NULL,
  `is_superadmin` int NOT NULL,
  `unit` varchar(30) DEFAULT NULL,
  `drift_id` double DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) DEFAULT NULL,
  `company_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `wellphases_casing`
--

INSERT INTO `wellphases_casing` (`id`, `nominal_od`, `weight`, `inside_diameter`, `grade`, `casing_range`, `connection_type`, `connection_od`, `is_superadmin`, `unit`, `drift_id`, `status`, `created`, `company_id`) VALUES
(1, 20, 133, 18.73, NULL, NULL, 'BTC', 21.001, 1, 'API', 18.544, 1, '2021-08-09 11:14:06.291199', NULL),
(2, 20, 133, 18.73, NULL, NULL, 'STC', 21.001, 1, 'API', 18.544, 1, '2021-08-09 11:14:06.298805', NULL),
(3, 20, 133, 18.73, NULL, NULL, 'LTC', 21.001, 1, 'API', 18.544, 1, '2021-08-09 11:14:06.305284', NULL),
(4, 20, 106.5, 19, NULL, NULL, 'BTC', 21.001, 1, 'API', 18.812, 1, '2021-08-09 11:14:06.311315', NULL),
(5, 20, 106.5, 19, NULL, NULL, 'STC', 21.001, 1, 'API', 18.812, 1, '2021-08-09 11:14:06.316897', NULL),
(6, 20, 106.5, 19, NULL, NULL, 'LTC', 21.001, 1, 'API', 18.812, 1, '2021-08-09 11:14:06.322030', NULL),
(7, 20, 94, 19.124, NULL, NULL, 'BTC', 21.001, 1, 'API', 18.938, 1, '2021-08-09 11:14:06.327177', NULL),
(8, 20, 94, 19.124, NULL, NULL, 'STC', 21.001, 1, 'API', 18.938, 1, '2021-08-09 11:14:06.331768', NULL),
(9, 20, 94, 19.124, NULL, NULL, 'LTC', 21.001, 1, 'API', 18.938, 1, '2021-08-09 11:14:06.336557', NULL),
(10, 18.625, 87.5, 17.755, NULL, NULL, 'BTC', 20.001, 1, 'API', 17.568, 1, '2021-08-09 11:14:06.341050', NULL),
(11, 18.625, 87.5, 17.755, NULL, NULL, 'STC', 20.001, 1, 'API', 17.568, 1, '2021-08-09 11:14:06.345646', NULL),
(12, 18.625, 87.5, 17.755, NULL, NULL, 'Hydril 563', 20.001, 1, 'API', 17.568, 1, '2021-08-09 11:14:06.350238', NULL),
(13, 18.625, 87.5, 17.755, NULL, NULL, 'Hydril 521', 18.855, 1, 'API', 17.568, 1, '2021-08-09 11:14:06.354977', NULL),
(14, 16, 128, 14.438, NULL, NULL, 'BTC', 17.001, 1, 'API', 14.253, 1, '2021-08-09 11:14:06.359551', NULL),
(15, 16, 109, 14.688, NULL, NULL, 'BTC', 17.001, 1, 'API', 14.501, 1, '2021-08-09 11:14:06.364148', NULL),
(16, 16, 109, 14.688, NULL, NULL, 'Hydril 563', 17.001, 1, 'API', 14.501, 1, '2021-08-09 11:14:06.370699', NULL),
(17, 16, 109, 14.688, NULL, NULL, 'Hydril 521', 16.465, 1, 'API', 14.501, 1, '2021-08-09 11:14:06.375384', NULL),
(18, 16, 94.5, 14.876, NULL, NULL, 'BTC', 17.001, 1, 'API', 14.69, 1, '2021-08-09 11:14:06.380063', NULL),
(19, 16, 84, 15.01, NULL, NULL, 'BTC', 17.001, 1, 'API', 14.824, 1, '2021-08-09 11:14:06.384774', NULL),
(20, 16, 84, 15.01, NULL, NULL, 'STC', 17.001, 1, 'API', 14.824, 1, '2021-08-09 11:14:06.389582', NULL),
(21, 16, 84, 15.01, NULL, NULL, 'Hydril 563', 17.001, 1, 'API', 14.824, 1, '2021-08-09 11:14:06.394381', NULL),
(22, 16, 84, 15.01, NULL, NULL, 'Hydril 521', 16.257, 1, 'API', 14.824, 1, '2021-08-09 11:14:06.399275', NULL),
(23, 16, 75, 15.124, NULL, NULL, 'BTC', 17.001, 1, 'API', 14.938, 1, '2021-08-09 11:14:06.403762', NULL),
(24, 16, 75, 15.124, NULL, NULL, 'STC', 17.001, 1, 'API', 14.938, 1, '2021-08-09 11:14:06.408296', NULL),
(25, 16, 75, 15.124, NULL, NULL, 'Hydril 563', 17.001, 1, 'API', 14.938, 1, '2021-08-09 11:14:06.413258', NULL),
(26, 16, 75, 15.124, NULL, NULL, 'Hydril 521', 16.154, 1, 'API', 14.938, 1, '2021-08-09 11:14:06.417755', NULL),
(27, 16, 65, 15.25, NULL, NULL, 'BTC', 17.001, 1, 'API', 15.064, 1, '2021-08-09 11:14:06.422561', NULL),
(28, 14, 114, 12.4, NULL, NULL, 'Hydril 563', 15.001, 1, 'API', 12.213, 1, '2021-08-09 11:14:06.427335', NULL),
(29, 14, 99, 12.624, NULL, NULL, NULL, NULL, 1, 'API', NULL, 1, '2021-08-09 11:14:06.433690', NULL),
(30, 14, 94.8, 12.688, NULL, NULL, NULL, NULL, 1, 'API', NULL, 1, '2021-08-09 11:14:06.438261', NULL),
(31, 14, 82.5, 12.876, NULL, NULL, NULL, NULL, 1, 'API', NULL, 1, '2021-08-09 11:14:06.443202', NULL),
(32, 13.625, 88.2, 12.375, NULL, NULL, 'Grant Prideco STL', 13.627, 1, 'API', 12.19, 1, '2021-08-09 11:14:06.447876', NULL),
(33, 13.625, 88.2, 12.375, NULL, NULL, 'Hydril 563', 14.627, 1, 'API', 12.19, 1, '2021-08-09 11:14:06.452586', NULL),
(34, 13.625, 88.2, 12.375, NULL, NULL, 'Hydril 521', 14.04, 1, 'API', 12.19, 1, '2021-08-09 11:14:06.457309', NULL),
(35, 13.625, 88.2, 12.375, NULL, NULL, 'Valluorec VAM New', 14.398, 1, 'API', 12.19, 1, '2021-08-09 11:14:06.461918', NULL),
(36, 13.375, 80.7, 12.215, NULL, NULL, 'BTC', 14.375, 1, 'API', 12.06, 1, '2021-08-09 11:14:06.466347', NULL),
(37, 13.375, 80.7, 12.215, NULL, NULL, 'Grant Prideco TCII', 14.3, 1, 'API', 12.06, 1, '2021-08-09 11:14:06.470920', NULL),
(38, 13.375, 80.7, 12.215, NULL, NULL, 'Hydril LX', 13.615, 1, 'API', 12.06, 1, '2021-08-09 11:14:06.475926', NULL),
(39, 13.375, 80.7, 12.215, NULL, NULL, 'Hydril 563', 14.375, 1, 'API', 12.06, 1, '2021-08-09 11:14:06.480258', NULL),
(40, 13.375, 80.7, 12.215, NULL, NULL, 'Hydril 521', 13.737, 1, 'API', 12.06, 1, '2021-08-09 11:14:06.485043', NULL),
(41, 13.375, 80.7, 12.215, NULL, NULL, 'Valluorec VAM New', 14.398, 1, 'API', 12.06, 1, '2021-08-09 11:14:06.490319', NULL),
(42, 13.375, 80.7, 12.215, NULL, NULL, 'Valluorec VAM ACE', 14.375, 1, 'API', 12.06, 1, '2021-08-09 11:14:06.495163', NULL),
(43, 13.375, 80.7, 12.215, NULL, NULL, 'Valluorec VAM TOP', 14.351, 1, 'API', 12.06, 1, '2021-08-09 11:14:06.500132', NULL),
(44, 13.375, 77, 12.275, NULL, NULL, 'BTC', 14.375, 1, 'API', 12.119, 1, '2021-08-09 11:14:06.505291', NULL),
(45, 13.375, 77, 12.275, NULL, NULL, 'Grant Prideco TCII', 14.249, 1, 'API', 12.119, 1, '2021-08-09 11:14:06.510272', NULL),
(46, 13.375, 77, 12.275, NULL, NULL, 'Grant Prideco STL', 13.375, 1, 'API', 12.119, 1, '2021-08-09 11:14:06.515573', NULL),
(47, 13.375, 77, 12.275, NULL, NULL, 'Hydril LX', 13.611, 1, 'API', 12.119, 1, '2021-08-09 11:14:06.521919', NULL),
(48, 13.375, 77, 12.275, NULL, NULL, 'Hydril 563', 14.375, 1, 'API', 12.119, 1, '2021-08-09 11:14:06.526976', NULL),
(49, 13.375, 77, 12.275, NULL, NULL, 'Hydril 521', 13.686, 1, 'API', 12.119, 1, '2021-08-09 11:14:06.532275', NULL),
(50, 13.375, 77, 12.275, NULL, NULL, 'Valluorec VAM New', 14.398, 1, 'API', 12.119, 1, '2021-08-09 11:14:06.537492', NULL),
(51, 13.375, 77, 12.275, NULL, NULL, 'Valluorec VAM ACE', 14.375, 1, 'API', 12.119, 1, '2021-08-09 11:14:06.542560', NULL),
(52, 13.375, 77, 12.275, NULL, NULL, 'Valluorec VAM TOP', 14.3, 1, 'API', 12.119, 1, '2021-08-09 11:14:06.547847', NULL),
(53, 13.375, 72, 12.347, NULL, NULL, 'BTC', 14.375, 1, 'API', 12.19, 1, '2021-08-09 11:14:06.553351', NULL),
(54, 13.375, 72, 12.347, NULL, NULL, 'STC', 14.375, 1, 'API', 12.19, 1, '2021-08-09 11:14:06.558352', NULL),
(55, 13.375, 72, 12.347, NULL, NULL, 'Grant Prideco TCII', 14.186, 1, 'API', 12.19, 1, '2021-08-09 11:14:06.563545', NULL),
(56, 13.375, 72, 12.347, NULL, NULL, 'Grant Prideco STL', 13.375, 1, 'API', 12.19, 1, '2021-08-09 11:14:06.568559', NULL),
(57, 13.375, 72, 12.347, NULL, NULL, 'Hydril LX', 13.603, 1, 'API', 12.19, 1, '2021-08-09 11:14:06.573922', NULL),
(58, 13.375, 72, 12.347, NULL, NULL, 'Hydril 563', 14.375, 1, 'API', 12.19, 1, '2021-08-09 11:14:06.578870', NULL),
(59, 13.375, 72, 12.347, NULL, NULL, 'Hydril 521', 13.768, 1, 'API', 12.19, 1, '2021-08-09 11:14:06.583995', NULL),
(60, 13.375, 72, 12.347, NULL, NULL, 'Valluorec VAM New', 14.398, 1, 'API', 12.19, 1, '2021-08-09 11:14:06.589255', NULL),
(61, 13.375, 72, 12.347, NULL, NULL, 'Valluorec VAM ACE', 14.375, 1, 'API', 12.19, 1, '2021-08-09 11:14:06.594685', NULL),
(62, 13.375, 72, 12.347, NULL, NULL, 'Valluorec VAM TOP', 14.237, 1, 'API', 12.19, 1, '2021-08-09 11:14:06.599956', NULL),
(63, 13.375, 68, 12.415, NULL, NULL, 'BTC', 14.375, 1, 'API', 12.26, 1, '2021-08-09 11:14:06.605360', NULL),
(64, 13.375, 68, 12.415, NULL, NULL, 'STC', 14.375, 1, 'API', 12.26, 1, '2021-08-09 11:14:06.610254', NULL),
(65, 13.375, 68, 12.415, NULL, NULL, 'Grant Prideco TCII', 14.127, 1, 'API', 12.26, 1, '2021-08-09 11:14:06.615636', NULL),
(66, 13.375, 68, 12.415, NULL, NULL, 'Grant Prideco STL', 13.375, 1, 'API', 12.26, 1, '2021-08-09 11:14:06.620710', NULL),
(67, 13.375, 68, 12.415, NULL, NULL, 'Hydril LX', 13.564, 1, 'API', 12.26, 1, '2021-08-09 11:14:06.625737', NULL),
(68, 13.375, 68, 12.415, NULL, NULL, 'Hydril 563', 14.375, 1, 'API', 12.26, 1, '2021-08-09 11:14:06.630799', NULL),
(69, 13.375, 68, 12.415, NULL, NULL, 'Hydril 521', 13.709, 1, 'API', 12.26, 1, '2021-08-09 11:14:06.636075', NULL),
(70, 13.375, 68, 12.415, NULL, NULL, 'Valluorec VAM New', 14.398, 1, 'API', 12.26, 1, '2021-08-09 11:14:06.641080', NULL),
(71, 13.375, 68, 12.415, NULL, NULL, 'Valluorec VAM ACE', 14.375, 1, 'API', 12.26, 1, '2021-08-09 11:14:06.645602', NULL),
(72, 13.375, 68, 12.415, NULL, NULL, 'Valluorec VAM TOP', 14.174, 1, 'API', 12.26, 1, '2021-08-09 11:14:06.650921', NULL),
(73, 13.375, 61, 12.515, NULL, NULL, 'BTC', 14.375, 1, 'API', 12.359, 1, '2021-08-09 11:14:06.656060', NULL),
(74, 13.375, 61, 12.515, NULL, NULL, 'STC', 14.375, 1, 'API', 12.359, 1, '2021-08-09 11:14:06.661298', NULL),
(75, 13.375, 61, 12.515, NULL, NULL, 'Grant Prideco TCII', 14.036, 1, 'API', 12.359, 1, '2021-08-09 11:14:06.666766', NULL),
(76, 13.375, 61, 12.515, NULL, NULL, 'Grant Prideco STL', 13.375, 1, 'API', 12.359, 1, '2021-08-09 11:14:06.671879', NULL),
(77, 13.375, 61, 12.515, NULL, NULL, 'Hydril 563', 14.375, 1, 'API', 12.359, 1, '2021-08-09 11:14:06.677078', NULL),
(78, 13.375, 61, 12.515, NULL, NULL, 'Hydril 521', 12.619, 1, 'API', 12.359, 1, '2021-08-09 11:14:06.682141', NULL),
(79, 13.375, 61, 12.515, NULL, NULL, 'Valluorec VAM New', 14.398, 1, 'API', 12.359, 1, '2021-08-09 11:14:06.687310', NULL),
(80, 13.375, 61, 12.515, NULL, NULL, 'Valluorec VAM ACE', 14.375, 1, 'API', 12.359, 1, '2021-08-09 11:14:06.692276', NULL),
(81, 13.375, 61, 12.515, NULL, NULL, 'Valluorec VAM TOP', 14.087, 1, 'API', 12.359, 1, '2021-08-09 11:14:06.697521', NULL),
(82, 13.375, 54.5, 12.615, NULL, NULL, 'BTC', 14.375, 1, 'API', 12.461, 1, '2021-08-09 11:14:06.702971', NULL),
(83, 13.375, 54.5, 12.615, NULL, NULL, 'STC', 14.375, 1, 'API', 12.461, 1, '2021-08-09 11:14:06.708311', NULL),
(84, 13.375, 54.5, 12.615, NULL, NULL, 'Grant Prideco TCII', 13.949, 1, 'API', 12.461, 1, '2021-08-09 11:14:06.713080', NULL),
(85, 13.375, 54.5, 12.615, NULL, NULL, 'Hydril 563', 14.375, 1, 'API', 12.461, 1, '2021-08-09 11:14:06.718431', NULL),
(86, 13.375, 54.5, 12.615, NULL, NULL, 'Hydril 521', 13.532, 1, 'API', 12.461, 1, '2021-08-09 11:14:06.723840', NULL),
(87, 13.375, 54.5, 12.615, NULL, NULL, 'Valluorec VAM New', 14.398, 1, 'API', 12.461, 1, '2021-08-09 11:14:06.728994', NULL),
(88, 13.375, 54.5, 12.615, NULL, NULL, 'Valluorec VAM ACE', 14.375, 1, 'API', 12.461, 1, '2021-08-09 11:14:06.734556', NULL),
(89, 11.75, 71, 10.586, NULL, NULL, 'BTC', 12.753, 1, 'API', 10.43, 1, '2021-08-09 11:14:06.740241', NULL),
(90, 11.75, 71, 10.586, NULL, NULL, 'Grant Prideco TCII', 12.682, 1, 'API', 10.43, 1, '2021-08-09 11:14:06.745593', NULL),
(91, 11.75, 71, 10.586, NULL, NULL, 'Grant Prideco STL', 11.749, 1, 'API', 10.43, 1, '2021-08-09 11:14:06.750902', NULL),
(92, 11.75, 71, 10.586, NULL, NULL, 'Hydril LX', 11.977, 1, 'API', 10.43, 1, '2021-08-09 11:14:06.756277', NULL),
(93, 11.75, 71, 10.586, NULL, NULL, 'Hydril 563', 12.753, 1, 'API', 10.43, 1, '2021-08-09 11:14:06.761438', NULL),
(94, 11.75, 71, 10.586, NULL, NULL, 'Hydril 521', 12.127, 1, 'API', 10.43, 1, '2021-08-09 11:14:06.766657', NULL),
(95, 11.75, 65, 10.682, NULL, NULL, 'BTC', 12.753, 1, 'API', 10.528, 1, '2021-08-09 11:14:06.771782', NULL),
(96, 11.75, 65, 10.682, NULL, NULL, 'Grant Prideco TCII', 12.599, 1, 'API', 10.528, 1, '2021-08-09 11:14:06.776968', NULL),
(97, 11.75, 65, 10.682, NULL, NULL, 'Grant Prideco STL', 11.749, 1, 'API', 10.528, 1, '2021-08-09 11:14:06.782369', NULL),
(98, 11.75, 65, 10.682, NULL, NULL, 'Hydril LX', 11.965, 1, 'API', 10.528, 1, '2021-08-09 11:14:06.787853', NULL),
(99, 11.75, 65, 10.682, NULL, NULL, 'Hydril 563', 12.753, 1, 'API', 10.528, 1, '2021-08-09 11:14:06.792708', NULL),
(100, 11.75, 65, 10.682, NULL, NULL, 'Hydril 511', 11.749, 1, 'API', 10.528, 1, '2021-08-09 11:14:06.797729', NULL),
(101, 11.75, 65, 10.682, NULL, NULL, 'Hydril 521', 11.965, 1, 'API', 10.528, 1, '2021-08-09 11:14:06.803000', NULL),
(102, 11.75, 65, 10.682, NULL, NULL, 'Valluorec VAM New', 12.772, 1, 'API', 10.528, 1, '2021-08-09 11:14:06.808034', NULL),
(103, 11.75, 65, 10.682, NULL, NULL, 'Valluorec VAM ACE', 12.753, 1, 'API', 10.528, 1, '2021-08-09 11:14:06.812952', NULL),
(104, 11.75, 65, 10.682, NULL, NULL, 'Valluorec VAM TOP', 12.638, 1, 'API', 10.528, 1, '2021-08-09 11:14:06.817806', NULL),
(105, 11.75, 65, 10.682, NULL, NULL, 'Valluorec FJL', 11.749, 1, 'API', 10.528, 1, '2021-08-09 11:14:06.822726', NULL),
(106, 11.75, 60, 10.772, NULL, NULL, 'BTC', 12.753, 1, 'API', 10.615, 1, '2021-08-09 11:14:06.827720', NULL),
(107, 11.75, 60, 10.772, NULL, NULL, 'STC', 12.753, 1, 'API', 10.615, 1, '2021-08-09 11:14:06.832726', NULL),
(108, 11.75, 60, 10.772, NULL, NULL, 'Grant Prideco TCII', 12.524, 1, 'API', 10.615, 1, '2021-08-09 11:14:06.837853', NULL),
(109, 11.75, 60, 10.772, NULL, NULL, 'Grant Prideco STL', 11.749, 1, 'API', 10.615, 1, '2021-08-09 11:14:06.842958', NULL),
(110, 11.75, 60, 10.772, NULL, NULL, 'Hydril LX', 11.93, 1, 'API', 10.615, 1, '2021-08-09 11:14:06.847648', NULL),
(111, 11.75, 60, 10.772, NULL, NULL, 'Hydril 563', 12.753, 1, 'API', 10.615, 1, '2021-08-09 11:14:06.853186', NULL),
(112, 11.75, 60, 10.772, NULL, NULL, 'Hydril 511', 11.749, 1, 'API', 10.615, 1, '2021-08-09 11:14:06.858686', NULL),
(113, 11.75, 60, 10.772, NULL, NULL, 'Hydril 521', 11.93, 1, 'API', 10.615, 1, '2021-08-09 11:14:06.863796', NULL),
(114, 11.75, 60, 10.772, NULL, NULL, 'Valluorec VAM New', 12.772, 1, 'API', 10.615, 1, '2021-08-09 11:14:06.868775', NULL),
(115, 11.75, 60, 10.772, NULL, NULL, 'Valluorec VAM ACE', 12.753, 1, 'API', 10.615, 1, '2021-08-09 11:14:06.874101', NULL),
(116, 11.75, 60, 10.772, NULL, NULL, 'Valluorec VAM TOP', 12.556, 1, 'API', 10.615, 1, '2021-08-09 11:14:06.879467', NULL),
(117, 11.75, 60, 10.772, NULL, NULL, 'Valluorec FJL', 11.749, 1, 'API', 10.615, 1, '2021-08-09 11:14:06.884753', NULL),
(118, 11.75, 54, 10.88, NULL, NULL, 'BTC', 12.753, 1, 'API', 10.725, 1, '2021-08-09 11:14:06.890092', NULL),
(119, 11.75, 54, 10.88, NULL, NULL, 'STC', 12.753, 1, 'API', 10.725, 1, '2021-08-09 11:14:06.895611', NULL),
(120, 11.75, 54, 10.88, NULL, NULL, 'Grant Prideco TCII', 12.43, 1, 'API', 10.725, 1, '2021-08-09 11:14:06.900927', NULL),
(121, 11.75, 54, 10.88, NULL, NULL, 'Hydril 563', 12.753, 1, 'API', 10.725, 1, '2021-08-09 11:14:06.906255', NULL),
(122, 11.75, 54, 10.88, NULL, NULL, 'Hydril 521', 11.997, 1, 'API', 10.725, 1, '2021-08-09 11:14:06.911668', NULL),
(123, 11.75, 54, 10.88, NULL, NULL, 'Valluorec VAM New', 12.772, 1, 'API', 10.725, 1, '2021-08-09 11:14:06.916890', NULL),
(124, 11.75, 54, 10.88, NULL, NULL, 'Valluorec VAM ACE', 12.753, 1, 'API', 10.725, 1, '2021-08-09 11:14:06.922023', NULL),
(125, 11.75, 54, 10.88, NULL, NULL, 'Valluorec VAM TOP', 12.465, 1, 'API', 10.725, 1, '2021-08-09 11:14:06.927516', NULL),
(126, 11.75, 54, 10.88, NULL, NULL, 'Valluorec FJL', 11.749, 1, 'API', 10.725, 1, '2021-08-09 11:14:06.932658', NULL),
(127, 11.75, 47, 11, NULL, NULL, 'BTC', 12.753, 1, 'API', 10.843, 1, '2021-08-09 11:14:06.938133', NULL),
(128, 11.75, 47, 11, NULL, NULL, 'STC', 12.753, 1, 'API', 10.843, 1, '2021-08-09 11:14:06.943641', NULL),
(129, 11.75, 47, 11, NULL, NULL, 'Grant Prideco TCII', 12.323, 1, 'API', 10.843, 1, '2021-08-09 11:14:06.948897', NULL),
(130, 11.75, 47, 11, NULL, NULL, 'Hydril 563', 12.753, 1, 'API', 10.843, 1, '2021-08-09 11:14:06.954210', NULL),
(131, 11.75, 47, 11, NULL, NULL, 'Hydril 521', 11.894, 1, 'API', 10.843, 1, '2021-08-09 11:14:06.959623', NULL),
(132, 11.75, 47, 11, NULL, NULL, 'Valluorec VAM New', 12.772, 1, 'API', 10.843, 1, '2021-08-09 11:14:06.965036', NULL),
(133, 11.75, 47, 11, NULL, NULL, 'Valluorec VAM ACE', 12.753, 1, 'API', 10.843, 1, '2021-08-09 11:14:06.970457', NULL),
(134, 11.75, 47, 11, NULL, NULL, 'Valluorec FJL', 11.749, 1, 'API', 10.843, 1, '2021-08-09 11:14:06.975818', NULL),
(135, 10.75, 65.7, 9.56, NULL, NULL, 'BTC', 11.749, 1, 'API', 9.406, 1, '2021-08-09 11:14:06.981080', NULL),
(136, 10.75, 65.7, 9.56, NULL, NULL, 'BTC Special', 11.253, 1, 'API', 9.406, 1, '2021-08-09 11:14:06.986445', NULL),
(137, 10.75, 65.7, 9.56, NULL, NULL, 'STC', 11.753, 1, 'API', 9.406, 1, '2021-08-09 11:14:06.991584', NULL),
(138, 10.75, 65.7, 9.56, NULL, NULL, 'Grant Prideco TCII', 11.701, 1, 'API', 9.406, 1, '2021-08-09 11:14:06.997112', NULL),
(139, 10.75, 65.7, 9.56, NULL, NULL, 'Grant Prideco STL', 10.749, 1, 'API', 9.406, 1, '2021-08-09 11:14:07.002124', NULL),
(140, 10.75, 65.7, 9.56, NULL, NULL, 'Hydril LX', 10.965, 1, 'API', 9.406, 1, '2021-08-09 11:14:07.007248', NULL),
(141, 10.75, 65.7, 9.56, NULL, NULL, 'Hydril 563', 11.749, 1, 'API', 9.406, 1, '2021-08-09 11:14:07.013270', NULL),
(142, 10.75, 65.7, 9.56, NULL, NULL, 'Hydril 511', 10.749, 1, 'API', 9.406, 1, '2021-08-09 11:14:07.018745', NULL),
(143, 10.75, 65.7, 9.56, NULL, NULL, 'Hydril 521', 11.178, 1, 'API', 9.406, 1, '2021-08-09 11:14:07.024364', NULL),
(144, 10.75, 65.7, 9.56, NULL, NULL, 'Valluorec VAM New', 11.772, 1, 'API', 9.406, 1, '2021-08-09 11:14:07.029655', NULL),
(145, 10.75, 65.7, 9.56, NULL, NULL, 'Valluorec VAM ACE', 11.749, 1, 'API', 9.406, 1, '2021-08-09 11:14:07.034938', NULL),
(146, 10.75, 65.7, 9.56, NULL, NULL, 'Valluorec VAM TOP', 11.733, 1, 'API', 9.406, 1, '2021-08-09 11:14:07.040309', NULL),
(147, 10.75, 65.7, 9.56, NULL, NULL, 'Valluorec FJL', 10.749, 1, 'API', 9.406, 1, '2021-08-09 11:14:07.045980', NULL),
(148, 10.75, 60.7, 9.66, NULL, NULL, 'BTC', 11.749, 1, 'API', 9.504, 1, '2021-08-09 11:14:07.051475', NULL),
(149, 10.75, 60.7, 9.66, NULL, NULL, 'BTC Special', 11.253, 1, 'API', 9.504, 1, '2021-08-09 11:14:07.056776', NULL),
(150, 10.75, 60.7, 9.66, NULL, NULL, 'STC', 11.753, 1, 'API', 9.504, 1, '2021-08-09 11:14:07.062161', NULL),
(151, 10.75, 60.7, 9.66, NULL, NULL, 'Grant Prideco TCII', 11.619, 1, 'API', 9.504, 1, '2021-08-09 11:14:07.067208', NULL),
(152, 10.75, 60.7, 9.66, NULL, NULL, 'Grant Prideco STL', 10.749, 1, 'API', 9.504, 1, '2021-08-09 11:14:07.072483', NULL),
(153, 10.75, 60.7, 9.66, NULL, NULL, 'Hydril LX', 10.93, 1, 'API', 9.504, 1, '2021-08-09 11:14:07.087971', NULL),
(154, 10.75, 60.7, 9.66, NULL, NULL, 'Hydril 563', 11.749, 1, 'API', 9.504, 1, '2021-08-09 11:14:07.095170', NULL),
(155, 10.75, 60.7, 9.66, NULL, NULL, 'Hydril 511', 10.749, 1, 'API', 9.504, 1, '2021-08-09 11:14:07.101258', NULL),
(156, 10.75, 60.7, 9.66, NULL, NULL, 'Hydril 521', 11.095, 1, 'API', 9.504, 1, '2021-08-09 11:14:07.107158', NULL),
(157, 10.75, 60.7, 9.66, NULL, NULL, 'Valluorec VAM New', 11.772, 1, 'API', 9.504, 1, '2021-08-09 11:14:07.113151', NULL),
(158, 10.75, 60.7, 9.66, NULL, NULL, 'Valluorec VAM ACE', 11.749, 1, 'API', 9.504, 1, '2021-08-09 11:14:07.119182', NULL),
(159, 10.75, 60.7, 9.66, NULL, NULL, 'Valluorec VAM TOP', 11.654, 1, 'API', 9.504, 1, '2021-08-09 11:14:07.125031', NULL),
(160, 10.75, 60.7, 9.66, NULL, NULL, 'Valluorec FJL', 10.749, 1, 'API', 9.504, 1, '2021-08-09 11:14:07.131145', NULL),
(161, 10.75, 55.5, 9.76, NULL, NULL, 'BTC', 11.749, 1, 'API', 9.603, 1, '2021-08-09 11:14:07.137228', NULL),
(162, 10.75, 55.5, 9.76, NULL, NULL, 'BTC Special', 11.253, 1, 'API', 9.603, 1, '2021-08-09 11:14:07.143746', NULL),
(163, 10.75, 55.5, 9.76, NULL, NULL, 'STC', 11.753, 1, 'API', 9.603, 1, '2021-08-09 11:14:07.150517', NULL),
(164, 10.75, 55.5, 9.76, NULL, NULL, 'Grant Prideco TCII', 11.536, 1, 'API', 9.603, 1, '2021-08-09 11:14:07.157370', NULL),
(165, 10.75, 55.5, 9.76, NULL, NULL, 'Grant Prideco STL', 10.749, 1, 'API', 9.603, 1, '2021-08-09 11:14:07.163595', NULL),
(166, 10.75, 55.5, 9.76, NULL, NULL, 'Hydril LX', 10.922, 1, 'API', 9.603, 1, '2021-08-09 11:14:07.169653', NULL),
(167, 10.75, 55.5, 9.76, NULL, NULL, 'Hydril 563', 11.749, 1, 'API', 9.603, 1, '2021-08-09 11:14:07.176931', NULL),
(168, 10.75, 55.5, 9.76, NULL, NULL, 'Hydril 511', 10.749, 1, 'API', 9.603, 1, '2021-08-09 11:14:07.183437', NULL),
(169, 10.75, 55.5, 9.76, NULL, NULL, 'Hydril 521', 11.012, 1, 'API', 9.603, 1, '2021-08-09 11:14:07.189743', NULL),
(170, 10.75, 55.5, 9.76, NULL, NULL, 'Valluorec VAM New', 11.772, 1, 'API', 9.603, 1, '2021-08-09 11:14:07.196521', NULL),
(171, 10.75, 55.5, 9.76, NULL, NULL, 'Valluorec VAM ACE', 11.749, 1, 'API', 9.603, 1, '2021-08-09 11:14:07.203203', NULL),
(172, 10.75, 55.5, 9.76, NULL, NULL, 'Valluorec VAM TOP', 11.567, 1, 'API', 9.603, 1, '2021-08-09 11:14:07.209696', NULL),
(173, 10.75, 55.5, 9.76, NULL, NULL, 'Valluorec FJL', 10.749, 1, 'API', 9.603, 1, '2021-08-09 11:14:07.215999', NULL),
(174, 10.75, 51, 9.85, NULL, NULL, 'BTC', 11.749, 1, 'API', 9.693, 1, '2021-08-09 11:14:07.222114', NULL),
(175, 10.75, 51, 9.85, NULL, NULL, 'BTC Special', 11.253, 1, 'API', 9.693, 1, '2021-08-09 11:14:07.228266', NULL),
(176, 10.75, 51, 9.85, NULL, NULL, 'STC', 11.753, 1, 'API', 9.693, 1, '2021-08-09 11:14:07.234576', NULL),
(177, 10.75, 51, 9.85, NULL, NULL, 'Grant Prideco TCII', 11.457, 1, 'API', 9.693, 1, '2021-08-09 11:14:07.240589', NULL),
(178, 10.75, 51, 9.85, NULL, NULL, 'Grant Prideco STL', 10.749, 1, 'API', 9.693, 1, '2021-08-09 11:14:07.246657', NULL),
(179, 10.75, 51, 9.85, NULL, NULL, 'Hydril LX', 10.914, 1, 'API', 9.693, 1, '2021-08-09 11:14:07.252709', NULL),
(180, 10.75, 51, 9.85, NULL, NULL, 'Hydril 563', 11.749, 1, 'API', 9.693, 1, '2021-08-09 11:14:07.258727', NULL),
(181, 10.75, 51, 9.85, NULL, NULL, 'Hydril 511', 10.749, 1, 'API', 9.693, 1, '2021-08-09 11:14:07.264917', NULL),
(182, 10.75, 51, 9.85, NULL, NULL, 'Hydril 521', 11.036, 1, 'API', 9.693, 1, '2021-08-09 11:14:07.271042', NULL),
(183, 10.75, 51, 9.85, NULL, NULL, 'Valluorec VAM New', 11.772, 1, 'API', 9.693, 1, '2021-08-09 11:14:07.277176', NULL),
(184, 10.75, 51, 9.85, NULL, NULL, 'Valluorec VAM ACE', 11.749, 1, 'API', 9.693, 1, '2021-08-09 11:14:07.283452', NULL),
(185, 10.75, 51, 9.85, NULL, NULL, 'Valluorec VAM TOP', 11.489, 1, 'API', 9.693, 1, '2021-08-09 11:14:07.289700', NULL),
(186, 10.75, 51, 9.85, NULL, NULL, 'Valluorec FJL', 10.749, 1, 'API', 9.693, 1, '2021-08-09 11:14:07.296006', NULL),
(187, 10.75, 45.5, 9.95, NULL, NULL, 'BTC', 11.749, 1, 'API', 9.796, 1, '2021-08-09 11:14:07.302143', NULL),
(188, 10.75, 45.5, 9.95, NULL, NULL, 'BTC Special', 11.253, 1, 'API', 9.796, 1, '2021-08-09 11:14:07.308223', NULL),
(189, 10.75, 45.5, 9.95, NULL, NULL, 'STC', 11.753, 1, 'API', 9.796, 1, '2021-08-09 11:14:07.314158', NULL),
(190, 10.75, 45.5, 9.95, NULL, NULL, 'Grant Prideco TCII', 11.371, 1, 'API', 9.796, 1, '2021-08-09 11:14:07.321249', NULL),
(191, 10.75, 45.5, 9.95, NULL, NULL, 'Grant Prideco STL', 10.749, 1, 'API', 9.796, 1, '2021-08-09 11:14:07.327966', NULL),
(192, 10.75, 45.5, 9.95, NULL, NULL, 'Hydril 563', 11.749, 1, 'API', 9.796, 1, '2021-08-09 11:14:07.334568', NULL),
(193, 10.75, 45.5, 9.95, NULL, NULL, 'Hydril 511', 10.749, 1, 'API', 9.796, 1, '2021-08-09 11:14:07.340348', NULL),
(194, 10.75, 45.5, 9.95, NULL, NULL, 'Hydril 521', 10.949, 1, 'API', 9.796, 1, '2021-08-09 11:14:07.346077', NULL),
(195, 10.75, 45.5, 9.95, NULL, NULL, 'Valluorec VAM New', 11.772, 1, 'API', 9.796, 1, '2021-08-09 11:14:07.351706', NULL),
(196, 10.75, 45.5, 9.95, NULL, NULL, 'Valluorec VAM ACE', 11.749, 1, 'API', 9.796, 1, '2021-08-09 11:14:07.358035', NULL),
(197, 10.75, 45.5, 9.95, NULL, NULL, 'Valluorec VAM TOP', 11.402, 1, 'API', 9.796, 1, '2021-08-09 11:14:07.364018', NULL),
(198, 10.75, 45.5, 9.95, NULL, NULL, 'Valluorec FJL', 10.749, 1, 'API', 9.796, 1, '2021-08-09 11:14:07.369754', NULL),
(199, 10.75, 40.5, 10.05, NULL, NULL, 'BTC', 11.749, 1, 'API', 9.894, 1, '2021-08-09 11:14:07.375512', NULL),
(200, 10.75, 40.5, 10.05, NULL, NULL, 'BTC Special', 11.253, 1, 'API', 9.894, 1, '2021-08-09 11:14:07.381566', NULL),
(201, 10.75, 40.5, 10.05, NULL, NULL, 'STC', 11.753, 1, 'API', 9.894, 1, '2021-08-09 11:14:07.388500', NULL),
(202, 10.75, 40.5, 10.05, NULL, NULL, 'Grant Prideco TCII', 11.284, 1, 'API', 9.894, 1, '2021-08-09 11:14:07.394960', NULL),
(203, 10.75, 40.5, 10.05, NULL, NULL, 'Grant Prideco STL', 10.749, 1, 'API', 9.894, 1, '2021-08-09 11:14:07.401531', NULL),
(204, 10.75, 40.5, 10.05, NULL, NULL, 'Hydril 563', 11.749, 1, 'API', 9.894, 1, '2021-08-09 11:14:07.408044', NULL),
(205, 10.75, 40.5, 10.05, NULL, NULL, 'Hydril 521', 10.863, 1, 'API', 9.894, 1, '2021-08-09 11:14:07.414549', NULL),
(206, 10.75, 40.5, 10.05, NULL, NULL, 'Valluorec VAM New', 11.772, 1, 'API', 9.894, 1, '2021-08-09 11:14:07.420813', NULL),
(207, 10.75, 40.5, 10.05, NULL, NULL, 'Valluorec VAM ACE', 11.749, 1, 'API', 9.894, 1, '2021-08-09 11:14:07.427347', NULL),
(208, 10.75, 40.5, 10.05, NULL, NULL, 'Valluorec FJL', 10.749, 1, 'API', 9.894, 1, '2021-08-09 11:14:07.433710', NULL),
(209, 9.875, 62.8, 8.625, NULL, NULL, 'Grant Prideco TCII', 10.859, 1, 'API', 8.469, 1, '2021-08-09 11:14:07.440137', NULL),
(210, 9.875, 62.8, 8.625, NULL, NULL, 'Grant Prideco STL', 9.874, 1, 'API', 8.469, 1, '2021-08-09 11:14:07.446618', NULL),
(211, 9.875, 62.8, 8.625, NULL, NULL, 'Hydril LX', 10.067, 1, 'API', 8.469, 1, '2021-08-09 11:14:07.453217', NULL),
(212, 9.875, 62.8, 8.625, NULL, NULL, 'Hydril 563', 10.627, 1, 'API', 8.469, 1, '2021-08-09 11:14:07.459733', NULL),
(213, 9.875, 62.8, 8.625, NULL, NULL, 'Valluorec VAM ACE', 10.898, 1, 'API', 8.469, 1, '2021-08-09 11:14:07.466244', NULL),
(214, 9.875, 62.8, 8.625, NULL, NULL, 'Valluorec VAM PRO', 10.627, 1, 'API', 8.469, 1, '2021-08-09 11:14:07.472717', NULL),
(215, 9.875, 62.8, 8.625, NULL, NULL, 'Valluorec VAM TOP', 10.906, 1, 'API', 8.469, 1, '2021-08-09 11:14:07.479184', NULL),
(216, 9.875, 62.8, 8.625, NULL, NULL, 'Valluorec FJL', 9.874, 1, 'API', 8.469, 1, '2021-08-09 11:14:07.485662', NULL),
(217, 9.625, 61.1, 8.375, NULL, NULL, 'BTC', 10.627, 1, 'API', 8.221, 1, '2021-08-09 11:14:07.492530', NULL),
(218, 9.625, 61.1, 8.375, NULL, NULL, 'BTC Special', 10.126, 1, 'API', 8.221, 1, '2021-08-09 11:14:07.499215', NULL),
(219, 9.625, 61.1, 8.375, NULL, NULL, 'Hydril 563', 10.627, 1, 'API', 8.221, 1, '2021-08-09 11:14:07.505811', NULL),
(220, 9.625, 61.1, 8.375, NULL, NULL, 'Valluorec VAM New', 10.65, 1, 'API', 8.221, 1, '2021-08-09 11:14:07.512721', NULL),
(221, 9.625, 61.1, 8.375, NULL, NULL, 'Valluorec VAM ACE', 10.638, 1, 'API', 8.221, 1, '2021-08-09 11:14:07.519157', NULL),
(222, 9.625, 61.1, 8.375, NULL, NULL, 'Valluorec VAM PRO', 10.627, 1, 'API', 8.221, 1, '2021-08-09 11:14:07.525639', NULL),
(223, 9.625, 61.1, 8.375, NULL, NULL, 'Valluorec FJL', 9.626, 1, 'API', 8.221, 1, '2021-08-09 11:14:07.543782', NULL),
(224, 9.625, 59.4, 8.407, NULL, NULL, 'BTC', 10.627, 1, 'API', 8.252, 1, '2021-08-09 11:14:07.550946', NULL),
(225, 9.625, 59.4, 8.407, NULL, NULL, 'BTC Special', 10.126, 1, 'API', 8.252, 1, '2021-08-09 11:14:07.557519', NULL),
(226, 9.625, 59.4, 8.407, NULL, NULL, 'Hydril 563', 10.627, 1, 'API', 8.252, 1, '2021-08-09 11:14:07.563821', NULL),
(227, 9.625, 59.4, 8.407, NULL, NULL, 'Valluorec VAM New', 10.65, 1, 'API', 8.252, 1, '2021-08-09 11:14:07.570174', NULL),
(228, 9.625, 59.4, 8.407, NULL, NULL, 'Valluorec VAM ACE', 10.627, 1, 'API', 8.252, 1, '2021-08-09 11:14:07.576533', NULL),
(229, 9.625, 59.4, 8.407, NULL, NULL, 'Valluorec VAM PRO', 10.627, 1, 'API', 8.252, 1, '2021-08-09 11:14:07.582888', NULL),
(230, 9.625, 59.4, 8.407, NULL, NULL, 'Valluorec FJL', 9.626, 1, 'API', 8.252, 1, '2021-08-09 11:14:07.589287', NULL),
(231, 9.625, 58.4, 8.435, NULL, NULL, 'BTC', 10.627, 1, 'API', 8.28, 1, '2021-08-09 11:14:07.595917', NULL),
(232, 9.625, 58.4, 8.435, NULL, NULL, 'BTC Special', 10.126, 1, 'API', 8.28, 1, '2021-08-09 11:14:07.602217', NULL),
(233, 9.625, 58.4, 8.435, NULL, NULL, 'Grant Prideco TCII', 10.567, 1, 'API', 8.28, 1, '2021-08-09 11:14:07.608509', NULL),
(234, 9.625, 58.4, 8.435, NULL, NULL, 'Grant Prideco STL', 9.626, 1, 'API', 8.28, 1, '2021-08-09 11:14:07.614905', NULL),
(235, 9.625, 58.4, 8.435, NULL, NULL, 'Hydril LX', 9.831, 1, 'API', 8.28, 1, '2021-08-09 11:14:07.621217', NULL),
(236, 9.625, 58.4, 8.435, NULL, NULL, 'Hydril 563', 10.627, 1, 'API', 8.28, 1, '2021-08-09 11:14:07.627647', NULL),
(237, 9.625, 58.4, 8.435, NULL, NULL, 'Valluorec VAM New', 10.65, 1, 'API', 8.28, 1, '2021-08-09 11:14:07.634003', NULL),
(238, 9.625, 58.4, 8.435, NULL, NULL, 'Valluorec VAM ACE', 10.627, 1, 'API', 8.28, 1, '2021-08-09 11:14:07.640288', NULL),
(239, 9.625, 58.4, 8.435, NULL, NULL, 'Valluorec VAM PRO', 10.627, 1, 'API', 8.28, 1, '2021-08-09 11:14:07.646728', NULL),
(240, 9.625, 58.4, 8.435, NULL, NULL, 'Valluorec VAM TOP', 10.599, 1, 'API', 8.28, 1, '2021-08-09 11:14:07.653097', NULL),
(241, 9.625, 58.4, 8.435, NULL, NULL, 'Valluorec FJL', 9.626, 1, 'API', 8.28, 1, '2021-08-09 11:14:07.660977', NULL),
(242, 9.625, 53.5, 8.535, NULL, NULL, 'BTC', 10.627, 1, 'API', 8.378, 1, '2021-08-09 11:14:07.669705', NULL),
(243, 9.625, 53.5, 8.535, NULL, NULL, 'BTC Special', 10.126, 1, 'API', 8.378, 1, '2021-08-09 11:14:07.676325', NULL),
(244, 9.625, 53.5, 8.535, NULL, NULL, 'LTC', 10.627, 1, 'API', 8.378, 1, '2021-08-09 11:14:07.684086', NULL),
(245, 9.625, 53.5, 8.535, NULL, NULL, 'Grant Prideco TCII', 10.489, 1, 'API', 8.378, 1, '2021-08-09 11:14:07.690617', NULL),
(246, 9.625, 53.5, 8.535, NULL, NULL, 'Grant Prideco STL', 9.626, 1, 'API', 8.378, 1, '2021-08-09 11:14:07.700018', NULL),
(247, 9.625, 53.5, 8.535, NULL, NULL, 'Hydril LX', 9.823, 1, 'API', 8.378, 1, '2021-08-09 11:14:07.706553', NULL),
(248, 9.625, 53.5, 8.535, NULL, NULL, 'Hydril 563', 10.627, 1, 'API', 8.378, 1, '2021-08-09 11:14:07.712491', NULL),
(249, 9.625, 53.5, 8.535, NULL, NULL, 'Hydril 521', 10.205, 1, 'API', 8.378, 1, '2021-08-09 11:14:07.718618', NULL),
(250, 9.625, 53.5, 8.535, NULL, NULL, 'Valluorec VAM New', 10.65, 1, 'API', 8.378, 1, '2021-08-09 11:14:07.724324', NULL),
(251, 9.625, 53.5, 8.535, NULL, NULL, 'Valluorec VAM ACE', 10.627, 1, 'API', 8.378, 1, '2021-08-09 11:14:07.730105', NULL),
(252, 9.625, 53.5, 8.535, NULL, NULL, 'Valluorec VAM PRO', 10.627, 1, 'API', 8.378, 1, '2021-08-09 11:14:07.737667', NULL),
(253, 9.625, 53.5, 8.535, NULL, NULL, 'Valluorec VAM TOP', 10.52, 1, 'API', 8.378, 1, '2021-08-09 11:14:07.744035', NULL),
(254, 9.625, 53.5, 8.535, NULL, NULL, 'Valluorec FJL', 9.626, 1, 'API', 8.378, 1, '2021-08-09 11:14:07.751044', NULL),
(255, 9.625, 47, 8.681, NULL, NULL, 'BTC', 10.627, 1, 'API', 8.524, 1, '2021-08-09 11:14:07.757606', NULL),
(256, 9.625, 47, 8.681, NULL, NULL, 'BTC Special', 10.126, 1, 'API', 8.524, 1, '2021-08-09 11:14:07.764204', NULL),
(257, 9.625, 47, 8.681, NULL, NULL, 'LTC', 10.627, 1, 'API', 8.524, 1, '2021-08-09 11:14:07.770554', NULL),
(258, 9.625, 47, 8.681, NULL, NULL, 'Grant Prideco TCII', 10.367, 1, 'API', 8.524, 1, '2021-08-09 11:14:07.776762', NULL),
(259, 9.625, 47, 8.681, NULL, NULL, 'Grant Prideco STL', 9.626, 1, 'API', 8.524, 1, '2021-08-09 11:14:07.783096', NULL),
(260, 9.625, 47, 8.681, NULL, NULL, 'Hydril LX', 9.784, 1, 'API', 8.524, 1, '2021-08-09 11:14:07.789887', NULL),
(261, 9.625, 47, 8.681, NULL, NULL, 'Hydril 563', 10.627, 1, 'API', 8.524, 1, '2021-08-09 11:14:07.796260', NULL),
(262, 9.625, 47, 8.681, NULL, NULL, 'Hydril 511', 9.626, 1, 'API', 8.524, 1, '2021-08-09 11:14:07.802811', NULL),
(263, 9.625, 47, 8.681, NULL, NULL, 'Hydril 521', 10.087, 1, 'API', 8.524, 1, '2021-08-09 11:14:07.809107', NULL),
(264, 9.625, 47, 8.681, NULL, NULL, 'Valluorec VAM New', 10.65, 1, 'API', 8.524, 1, '2021-08-09 11:14:07.815661', NULL),
(265, 9.625, 47, 8.681, NULL, NULL, 'Valluorec VAM ACE', 10.627, 1, 'API', 8.524, 1, '2021-08-09 11:14:07.821821', NULL),
(266, 9.625, 47, 8.681, NULL, NULL, 'Valluorec VAM PRO', 10.627, 1, 'API', 8.524, 1, '2021-08-09 11:14:07.827785', NULL),
(267, 9.625, 47, 8.681, NULL, NULL, 'Valluorec VAM TOP', 10.398, 1, 'API', 8.524, 1, '2021-08-09 11:14:07.834104', NULL),
(268, 9.625, 47, 8.681, NULL, NULL, 'Valluorec FJL', 9.626, 1, 'API', 8.524, 1, '2021-08-09 11:14:07.840111', NULL),
(269, 9.625, 43.5, 8.755, NULL, NULL, 'BTC', 10.627, 1, 'API', 8.599, 1, '2021-08-09 11:14:07.846265', NULL),
(270, 9.625, 43.5, 8.755, NULL, NULL, 'BTC Special', 10.126, 1, 'API', 8.599, 1, '2021-08-09 11:14:07.852678', NULL),
(271, 9.625, 43.5, 8.755, NULL, NULL, 'LTC', 10.627, 1, 'API', 8.599, 1, '2021-08-09 11:14:07.859368', NULL),
(272, 9.625, 43.5, 8.755, NULL, NULL, 'Grant Prideco TCII', 10.304, 1, 'API', 8.599, 1, '2021-08-09 11:14:07.866207', NULL),
(273, 9.625, 43.5, 8.755, NULL, NULL, 'Grant Prideco STL', 9.626, 1, 'API', 8.599, 1, '2021-08-09 11:14:07.872969', NULL),
(274, 9.625, 43.5, 8.755, NULL, NULL, 'Hydril LX', 9.78, 1, 'API', 8.599, 1, '2021-08-09 11:14:07.879701', NULL),
(275, 9.625, 43.5, 8.755, NULL, NULL, 'Hydril 563', 10.627, 1, 'API', 8.599, 1, '2021-08-09 11:14:07.886347', NULL),
(276, 9.625, 43.5, 8.755, NULL, NULL, 'Hydril 511', 9.626, 1, 'API', 8.599, 1, '2021-08-09 11:14:07.892764', NULL),
(277, 9.625, 43.5, 8.755, NULL, NULL, 'Hydril 521', 10.024, 1, 'API', 8.599, 1, '2021-08-09 11:14:07.899231', NULL),
(278, 9.625, 43.5, 8.755, NULL, NULL, 'Valluorec VAM New', 10.65, 1, 'API', 8.599, 1, '2021-08-09 11:14:07.905666', NULL),
(279, 9.625, 43.5, 8.755, NULL, NULL, 'Valluorec VAM ACE', 10.627, 1, 'API', 8.599, 1, '2021-08-09 11:14:07.912108', NULL),
(280, 9.625, 43.5, 8.755, NULL, NULL, 'Valluorec VAM PRO', 10.627, 1, 'API', 8.599, 1, '2021-08-09 11:14:07.918806', NULL),
(281, 9.625, 43.5, 8.755, NULL, NULL, 'Valluorec VAM TOP', 10.335, 1, 'API', 8.599, 1, '2021-08-09 11:14:07.925530', NULL),
(282, 9.625, 43.5, 8.755, NULL, NULL, 'Valluorec FJL', 9.626, 1, 'API', 8.599, 1, '2021-08-09 11:14:07.931660', NULL),
(283, 9.625, 40, 8.835, NULL, NULL, 'BTC', 10.627, 1, 'API', 8.678, 1, '2021-08-09 11:14:07.937244', NULL),
(284, 9.625, 40, 8.835, NULL, NULL, 'BTC Special', 10.126, 1, 'API', 8.678, 1, '2021-08-09 11:14:07.942994', NULL),
(285, 9.625, 40, 8.835, NULL, NULL, 'STC', 10.627, 1, 'API', 8.678, 1, '2021-08-09 11:14:07.948980', NULL),
(286, 9.625, 40, 8.835, NULL, NULL, 'LTC', 10.627, 1, 'API', 8.678, 1, '2021-08-09 11:14:07.955179', NULL),
(287, 9.625, 40, 8.835, NULL, NULL, 'Grant Prideco TCII', 10.237, 1, 'API', 8.678, 1, '2021-08-09 11:14:07.961257', NULL),
(288, 9.625, 40, 8.835, NULL, NULL, 'Grant Prideco STL', 9.626, 1, 'API', 8.678, 1, '2021-08-09 11:14:07.967364', NULL),
(289, 9.625, 40, 8.835, NULL, NULL, 'Hydril 563', 10.627, 1, 'API', 8.678, 1, '2021-08-09 11:14:07.973110', NULL),
(290, 9.625, 40, 8.835, NULL, NULL, 'Hydril 511', 9.626, 1, 'API', 8.678, 1, '2021-08-09 11:14:07.978613', NULL),
(291, 9.625, 40, 8.835, NULL, NULL, 'Hydril 521', 9.957, 1, 'API', 8.678, 1, '2021-08-09 11:14:07.984103', NULL),
(292, 9.625, 40, 8.835, NULL, NULL, 'Valluorec VAM New', 10.65, 1, 'API', 8.678, 1, '2021-08-09 11:14:07.989546', NULL),
(293, 9.625, 40, 8.835, NULL, NULL, 'Valluorec VAM ACE', 10.627, 1, 'API', 8.678, 1, '2021-08-09 11:14:07.995697', NULL),
(294, 9.625, 40, 8.835, NULL, NULL, 'Valluorec VAM PRO', 10.627, 1, 'API', 8.678, 1, '2021-08-09 11:14:08.001482', NULL),
(295, 9.625, 40, 8.835, NULL, NULL, 'Valluorec VAM TOP', 10.264, 1, 'API', 8.678, 1, '2021-08-09 11:14:08.007865', NULL),
(296, 9.625, 40, 8.835, NULL, NULL, 'Valluorec FJL', 9.626, 1, 'API', 8.678, 1, '2021-08-09 11:14:08.013789', NULL),
(297, 9.625, 36, 8.921, NULL, NULL, 'BTC', 10.627, 1, 'API', 8.764, 1, '2021-08-09 11:14:08.019048', NULL),
(298, 9.625, 36, 8.921, NULL, NULL, 'BTC Special', 10.126, 1, 'API', 8.764, 1, '2021-08-09 11:14:08.025267', NULL),
(299, 9.625, 36, 8.921, NULL, NULL, 'STC', 10.627, 1, 'API', 8.764, 1, '2021-08-09 11:14:08.030969', NULL),
(300, 9.625, 36, 8.921, NULL, NULL, 'LTC', 10.627, 1, 'API', 8.764, 1, '2021-08-09 11:14:08.038227', NULL),
(301, 9.625, 36, 8.921, NULL, NULL, 'Grant Prideco TCII', 10.162, 1, 'API', 8.764, 1, '2021-08-09 11:14:08.044059', NULL),
(302, 9.625, 36, 8.921, NULL, NULL, 'Hydril 563', 10.627, 1, 'API', 8.764, 1, '2021-08-09 11:14:08.050253', NULL),
(303, 9.625, 36, 8.921, NULL, NULL, 'Hydril 521', 9.882, 1, 'API', 8.764, 1, '2021-08-09 11:14:08.056147', NULL),
(304, 9.625, 36, 8.921, NULL, NULL, 'Valluorec VAM New', 10.65, 1, 'API', 8.764, 1, '2021-08-09 11:14:08.061849', NULL),
(305, 9.625, 36, 8.921, NULL, NULL, 'Valluorec VAM ACE', 10.627, 1, 'API', 8.764, 1, '2021-08-09 11:14:08.067813', NULL),
(306, 9.625, 36, 8.921, NULL, NULL, 'Valluorec VAM PRO', 10.627, 1, 'API', 8.764, 1, '2021-08-09 11:14:08.074020', NULL),
(307, 9.625, 36, 8.921, NULL, NULL, 'Valluorec FJL', 9.626, 1, 'API', 8.764, 1, '2021-08-09 11:14:08.078839', NULL),
(308, 8.625, 52, 7.435, NULL, NULL, 'BTC', 9.626, 1, 'API', 7.311, 1, '2021-08-09 11:14:08.083693', NULL),
(309, 8.625, 52, 7.435, NULL, NULL, 'BTC Special', 9.126, 1, 'API', 7.311, 1, '2021-08-09 11:14:08.089292', NULL),
(310, 8.625, 52, 7.435, NULL, NULL, 'Hydril LX', 8.8, 1, 'API', 7.311, 1, '2021-08-09 11:14:08.094778', NULL),
(311, 8.625, 52, 7.435, NULL, NULL, 'Hydril 563', 9.626, 1, 'API', 7.311, 1, '2021-08-09 11:14:08.100482', NULL),
(312, 8.625, 52, 7.435, NULL, NULL, 'Valluorec VAM New', 9.65, 1, 'API', 7.311, 1, '2021-08-09 11:14:08.105904', NULL),
(313, 8.625, 52, 7.435, NULL, NULL, 'Valluorec VAM ACE', 9.626, 1, 'API', 7.311, 1, '2021-08-09 11:14:08.111036', NULL),
(314, 8.625, 52, 7.435, NULL, NULL, 'Valluorec VAM PRO', 9.626, 1, 'API', 7.311, 1, '2021-08-09 11:14:08.116087', NULL),
(315, 8.625, 52, 7.435, NULL, NULL, 'Valluorec VAM TOP', 9.587, 1, 'API', 7.311, 1, '2021-08-09 11:14:08.120590', NULL),
(316, 8.625, 52, 7.435, NULL, NULL, 'Valluorec FJL', 8.626, 1, 'API', 7.311, 1, '2021-08-09 11:14:08.125658', NULL),
(317, 8.625, 49, 7.511, NULL, NULL, 'BTC', 9.626, 1, 'API', 7.386, 1, '2021-08-09 11:14:08.130907', NULL),
(318, 8.625, 49, 7.511, NULL, NULL, 'BTC Special', 9.126, 1, 'API', 7.386, 1, '2021-08-09 11:14:08.136238', NULL),
(319, 8.625, 49, 7.511, NULL, NULL, 'LTC', 9.626, 1, 'API', 7.386, 1, '2021-08-09 11:14:08.141252', NULL),
(320, 8.625, 49, 7.511, NULL, NULL, 'Grant Prideco TCII', 9.508, 1, 'API', 7.386, 1, '2021-08-09 11:14:08.146661', NULL),
(321, 8.625, 49, 7.511, NULL, NULL, 'Grant Prideco STL', 8.626, 1, 'API', 7.386, 1, '2021-08-09 11:14:08.151585', NULL),
(322, 8.625, 49, 7.511, NULL, NULL, 'Hydril LX', 8.792, 1, 'API', 7.386, 1, '2021-08-09 11:14:08.156638', NULL),
(323, 8.625, 49, 7.511, NULL, NULL, 'Hydril 563', 9.626, 1, 'API', 7.386, 1, '2021-08-09 11:14:08.161435', NULL),
(324, 8.625, 49, 7.511, NULL, NULL, 'Valluorec VAM New', 9.65, 1, 'API', 7.386, 1, '2021-08-09 11:14:08.166485', NULL),
(325, 8.625, 49, 7.511, NULL, NULL, 'Valluorec VAM ACE', 9.626, 1, 'API', 7.386, 1, '2021-08-09 11:14:08.171196', NULL),
(326, 8.625, 49, 7.511, NULL, NULL, 'Valluorec VAM PRO', 9.626, 1, 'API', 7.386, 1, '2021-08-09 11:14:08.176144', NULL),
(327, 8.625, 49, 7.511, NULL, NULL, 'Valluorec VAM TOP', 9.528, 1, 'API', 7.386, 1, '2021-08-09 11:14:08.181247', NULL),
(328, 8.625, 49, 7.511, NULL, NULL, 'Valluorec FJL', 8.626, 1, 'API', 7.386, 1, '2021-08-09 11:14:08.187518', NULL),
(329, 8.625, 44, 7.625, NULL, NULL, 'BTC', 9.626, 1, 'API', 7.5, 1, '2021-08-09 11:14:08.193928', NULL),
(330, 8.625, 44, 7.625, NULL, NULL, 'BTC Special', 9.126, 1, 'API', 7.5, 1, '2021-08-09 11:14:08.200580', NULL),
(331, 8.625, 44, 7.625, NULL, NULL, 'LTC', 9.626, 1, 'API', 7.5, 1, '2021-08-09 11:14:08.205589', NULL),
(332, 8.625, 44, 7.625, NULL, NULL, 'Grant Prideco TCII', 9.414, 1, 'API', 7.5, 1, '2021-08-09 11:14:08.211637', NULL),
(333, 8.625, 44, 7.625, NULL, NULL, 'Grant Prideco STL', 8.626, 1, 'API', 7.5, 1, '2021-08-09 11:14:08.219629', NULL),
(334, 8.625, 44, 7.625, NULL, NULL, 'Hydril LX', 8.784, 1, 'API', 7.5, 1, '2021-08-09 11:14:08.227953', NULL),
(335, 8.625, 44, 7.625, NULL, NULL, 'Hydril 563', 9.626, 1, 'API', 7.5, 1, '2021-08-09 11:14:08.235715', NULL),
(336, 8.625, 44, 7.625, NULL, NULL, 'Hydril 521', 9.134, 1, 'API', 7.5, 1, '2021-08-09 11:14:08.242087', NULL),
(337, 8.625, 44, 7.625, NULL, NULL, 'Valluorec VAM New', 9.65, 1, 'API', 7.5, 1, '2021-08-09 11:14:08.248203', NULL),
(338, 8.625, 44, 7.625, NULL, NULL, 'Valluorec VAM ACE', 9.626, 1, 'API', 7.5, 1, '2021-08-09 11:14:08.254057', NULL),
(339, 8.625, 44, 7.625, NULL, NULL, 'Valluorec VAM PRO', 9.626, 1, 'API', 7.5, 1, '2021-08-09 11:14:08.259852', NULL),
(340, 8.625, 44, 7.625, NULL, NULL, 'Valluorec VAM TOP', 9.434, 1, 'API', 7.5, 1, '2021-08-09 11:14:08.265687', NULL),
(341, 8.625, 44, 7.625, NULL, NULL, 'Valluorec FJL', 8.626, 1, 'API', 7.5, 1, '2021-08-09 11:14:08.271699', NULL),
(342, 8.625, 40, 7.725, NULL, NULL, 'BTC', 9.626, 1, 'API', 7.599, 1, '2021-08-09 11:14:08.277543', NULL),
(343, 8.625, 40, 7.725, NULL, NULL, 'BTC Special', 9.126, 1, 'API', 7.599, 1, '2021-08-09 11:14:08.283484', NULL),
(344, 8.625, 40, 7.725, NULL, NULL, 'LTC', 9.626, 1, 'API', 7.599, 1, '2021-08-09 11:14:08.289261', NULL),
(345, 8.625, 40, 7.725, NULL, NULL, 'Grant Prideco TCII', 9.335, 1, 'API', 7.599, 1, '2021-08-09 11:14:08.295122', NULL),
(346, 8.625, 40, 7.725, NULL, NULL, 'Grant Prideco STL', 8.626, 1, 'API', 7.599, 1, '2021-08-09 11:14:08.301089', NULL),
(347, 8.625, 40, 7.725, NULL, NULL, 'Hydril LX', 8.772, 1, 'API', 7.599, 1, '2021-08-09 11:14:08.307075', NULL),
(348, 8.625, 40, 7.725, NULL, NULL, 'Hydril 563', 9.626, 1, 'API', 7.599, 1, '2021-08-09 11:14:08.312822', NULL),
(349, 8.625, 40, 7.725, NULL, NULL, 'Hydril 511', 8.626, 1, 'API', 7.599, 1, '2021-08-09 11:14:08.318515', NULL),
(350, 8.625, 40, 7.725, NULL, NULL, 'Hydril 521', 9.052, 1, 'API', 7.599, 1, '2021-08-09 11:14:08.324547', NULL),
(351, 8.625, 40, 7.725, NULL, NULL, 'Valluorec VAM New', 9.65, 1, 'API', 7.599, 1, '2021-08-09 11:14:08.330749', NULL),
(352, 8.625, 40, 7.725, NULL, NULL, 'Valluorec VAM ACE', 9.626, 1, 'API', 7.599, 1, '2021-08-09 11:14:08.336607', NULL),
(353, 8.625, 40, 7.725, NULL, NULL, 'Valluorec VAM PRO', 9.626, 1, 'API', 7.599, 1, '2021-08-09 11:14:08.342641', NULL),
(354, 8.625, 40, 7.725, NULL, NULL, 'Valluorec VAM TOP', 9.351, 1, 'API', 7.599, 1, '2021-08-09 11:14:08.348561', NULL),
(355, 8.625, 40, 7.725, NULL, NULL, 'Valluorec FJL', 8.626, 1, 'API', 7.599, 1, '2021-08-09 11:14:08.354750', NULL),
(356, 8.625, 36, 7.825, NULL, NULL, 'BTC', 9.626, 1, 'API', 7.701, 1, '2021-08-09 11:14:08.361208', NULL),
(357, 8.625, 36, 7.825, NULL, NULL, 'BTC Special', 9.126, 1, 'API', 7.701, 1, '2021-08-09 11:14:08.367294', NULL),
(358, 8.625, 36, 7.825, NULL, NULL, 'STC', 9.626, 1, 'API', 7.701, 1, '2021-08-09 11:14:08.373259', NULL),
(359, 8.625, 36, 7.825, NULL, NULL, 'LTC', 9.626, 1, 'API', 7.701, 1, '2021-08-09 11:14:08.379440', NULL),
(360, 8.625, 36, 7.825, NULL, NULL, 'Grant Prideco TCII', 9.248, 1, 'API', 7.701, 1, '2021-08-09 11:14:08.385262', NULL),
(361, 8.625, 36, 7.825, NULL, NULL, 'Grant Prideco STL', 8.626, 1, 'API', 7.701, 1, '2021-08-09 11:14:08.391276', NULL),
(362, 8.625, 36, 7.825, NULL, NULL, 'Hydril LX', 8.764, 1, 'API', 7.701, 1, '2021-08-09 11:14:08.397248', NULL),
(363, 8.625, 36, 7.825, NULL, NULL, 'Hydril 563', 9.626, 1, 'API', 7.701, 1, '2021-08-09 11:14:08.403075', NULL),
(364, 8.625, 36, 7.825, NULL, NULL, 'Hydril 511', 8.626, 1, 'API', 7.701, 1, '2021-08-09 11:14:08.408897', NULL),
(365, 8.625, 36, 7.825, NULL, NULL, 'Hydril 521', 8.969, 1, 'API', 7.701, 1, '2021-08-09 11:14:08.414993', NULL),
(366, 8.625, 36, 7.825, NULL, NULL, 'Valluorec VAM New', 9.65, 1, 'API', 7.701, 1, '2021-08-09 11:14:08.420973', NULL),
(367, 8.625, 36, 7.825, NULL, NULL, 'Valluorec VAM ACE', 9.626, 1, 'API', 7.701, 1, '2021-08-09 11:14:08.426892', NULL),
(368, 8.625, 36, 7.825, NULL, NULL, 'Valluorec VAM PRO', 9.626, 1, 'API', 7.701, 1, '2021-08-09 11:14:08.433212', NULL),
(369, 8.625, 36, 7.825, NULL, NULL, 'Valluorec VAM TOP', 9.268, 1, 'API', 7.701, 1, '2021-08-09 11:14:08.439475', NULL),
(370, 8.625, 36, 7.825, NULL, NULL, 'Valluorec FJL', 8.626, 1, 'API', 7.701, 1, '2021-08-09 11:14:08.445119', NULL),
(371, 8.625, 32, 7.921, NULL, NULL, 'BTC', 9.626, 1, 'API', 7.796, 1, '2021-08-09 11:14:08.451460', NULL),
(372, 8.625, 32, 7.921, NULL, NULL, 'BTC Special', 9.126, 1, 'API', 7.796, 1, '2021-08-09 11:14:08.457705', NULL),
(373, 8.625, 32, 7.921, NULL, NULL, 'STC', 9.626, 1, 'API', 7.796, 1, '2021-08-09 11:14:08.463666', NULL),
(374, 8.625, 32, 7.921, NULL, NULL, 'LTC', 9.626, 1, 'API', 7.796, 1, '2021-08-09 11:14:08.469475', NULL),
(375, 8.625, 32, 7.921, NULL, NULL, 'Grant Prideco TCII', 9.166, 1, 'API', 7.796, 1, '2021-08-09 11:14:08.475516', NULL),
(376, 8.625, 32, 7.921, NULL, NULL, 'Grant Prideco STL', 8.626, 1, 'API', 7.796, 1, '2021-08-09 11:14:08.482019', NULL),
(377, 8.625, 32, 7.921, NULL, NULL, 'Hydril 563', 9.626, 1, 'API', 7.796, 1, '2021-08-09 11:14:08.488264', NULL),
(378, 8.625, 32, 7.921, NULL, NULL, 'Hydril 511', 8.626, 1, 'API', 7.796, 1, '2021-08-09 11:14:08.494593', NULL),
(379, 8.625, 32, 7.921, NULL, NULL, 'Hydril 521', 8.89, 1, 'API', 7.796, 1, '2021-08-09 11:14:08.500627', NULL),
(380, 8.625, 32, 7.921, NULL, NULL, 'Valluorec VAM New', 9.65, 1, 'API', 7.796, 1, '2021-08-09 11:14:08.506331', NULL),
(381, 8.625, 32, 7.921, NULL, NULL, 'Valluorec VAM ACE', 9.626, 1, 'API', 7.796, 1, '2021-08-09 11:14:08.512492', NULL),
(382, 8.625, 32, 7.921, NULL, NULL, 'Valluorec VAM PRO', 9.626, 1, 'API', 7.796, 1, '2021-08-09 11:14:08.517953', NULL),
(383, 8.625, 32, 7.921, NULL, NULL, 'Valluorec FJL', 8.626, 1, 'API', 7.796, 1, '2021-08-09 11:14:08.523854', NULL),
(384, 8.625, 28, 8.017, NULL, NULL, 'BTC', 9.626, 1, 'API', 7.894, 1, '2021-08-09 11:14:08.529988', NULL),
(385, 8.625, 28, 8.017, NULL, NULL, 'BTC Special', 9.126, 1, 'API', 7.894, 1, '2021-08-09 11:14:08.535973', NULL),
(386, 8.625, 28, 8.017, NULL, NULL, 'Grant Prideco TCII', 9.083, 1, 'API', 7.894, 1, '2021-08-09 11:14:08.541521', NULL),
(387, 8.625, 28, 8.017, NULL, NULL, 'Grant Prideco STL', 8.626, 1, 'API', 7.894, 1, '2021-08-09 11:14:08.546991', NULL),
(388, 8.625, 28, 8.017, NULL, NULL, 'Valluorec VAM New', 9.65, 1, 'API', 7.894, 1, '2021-08-09 11:14:08.553239', NULL),
(389, 8.625, 28, 8.017, NULL, NULL, 'Valluorec VAM ACE', 9.626, 1, 'API', 7.894, 1, '2021-08-09 11:14:08.559367', NULL),
(390, 8.625, 28, 8.017, NULL, NULL, 'Valluorec VAM PRO', 9.626, 1, 'API', 7.894, 1, '2021-08-09 11:14:08.565438', NULL),
(391, 7.625, 47.1, 6.375, NULL, NULL, 'BTC', 8.5, 1, 'API', 6.252, 1, '2021-08-09 11:14:08.571630', NULL),
(392, 7.625, 47.1, 6.375, NULL, NULL, 'BTC Special', 8.126, 1, 'API', 6.252, 1, '2021-08-09 11:14:08.578100', NULL),
(393, 7.625, 47.1, 6.375, NULL, NULL, 'LTC', 8.5, 1, 'API', 6.252, 1, '2021-08-09 11:14:08.584723', NULL),
(394, 7.625, 47.1, 6.375, NULL, NULL, 'Grant Prideco TCII', 8.851, 1, 'API', 6.252, 1, '2021-08-09 11:14:08.590928', NULL),
(395, 7.625, 47.1, 6.375, NULL, NULL, 'Grant Prideco STL', 7.626, 1, 'API', 6.252, 1, '2021-08-09 11:14:08.597368', NULL),
(396, 7.625, 47.1, 6.375, NULL, NULL, 'Hydril LX', 7.8, 1, 'API', 6.252, 1, '2021-08-09 11:14:08.603696', NULL),
(397, 7.625, 47.1, 6.375, NULL, NULL, 'Valluorec VAM New', 8.528, 1, 'API', 6.252, 1, '2021-08-09 11:14:08.609879', NULL),
(398, 7.625, 47.1, 6.375, NULL, NULL, 'Valluorec VAM PRO', 8.52, 1, 'API', 6.252, 1, '2021-08-09 11:14:08.616181', NULL),
(399, 7.625, 45.3, 6.435, NULL, NULL, 'BTC', 8.5, 1, 'API', 6.311, 1, '2021-08-09 11:14:08.622134', NULL),
(400, 7.625, 45.3, 6.435, NULL, NULL, 'BTC Special', 8.126, 1, 'API', 6.311, 1, '2021-08-09 11:14:08.628688', NULL),
(401, 7.625, 45.3, 6.435, NULL, NULL, 'Grant Prideco STL', 7.626, 1, 'API', 6.311, 1, '2021-08-09 11:14:08.635779', NULL),
(402, 7.625, 45.3, 6.435, NULL, NULL, 'Hydril LX', 7.792, 1, 'API', 6.311, 1, '2021-08-09 11:14:08.642569', NULL),
(403, 7.625, 45.3, 6.435, NULL, NULL, 'Hydril 563', 8.5, 1, 'API', 6.311, 1, '2021-08-09 11:14:08.649787', NULL),
(404, 7.625, 45.3, 6.435, NULL, NULL, 'Valluorec VAM New', 8.528, 1, 'API', 6.311, 1, '2021-08-09 11:14:08.656979', NULL),
(405, 7.625, 45.3, 6.435, NULL, NULL, 'Valluorec VAM ACE', 8.563, 1, 'API', 6.311, 1, '2021-08-09 11:14:08.663949', NULL),
(406, 7.625, 45.3, 6.435, NULL, NULL, 'Valluorec VAM PRO', 8.52, 1, 'API', 6.311, 1, '2021-08-09 11:14:08.670598', NULL),
(407, 7.625, 45.3, 6.435, NULL, NULL, 'Valluorec FJL', 7.626, 1, 'API', 6.311, 1, '2021-08-09 11:14:08.677280', NULL),
(408, 7.625, 42.8, 6.501, NULL, NULL, 'BTC', 8.5, 1, 'API', 6.378, 1, '2021-08-09 11:14:08.686011', NULL),
(409, 7.625, 42.8, 6.501, NULL, NULL, 'BTC Special', 8.126, 1, 'API', 6.378, 1, '2021-08-09 11:14:08.693207', NULL),
(410, 7.625, 42.8, 6.501, NULL, NULL, 'LTC', 8.5, 1, 'API', 6.378, 1, '2021-08-09 11:14:08.699437', NULL),
(411, 7.625, 42.8, 6.501, NULL, NULL, 'Grant Prideco TCII', 8.489, 1, 'API', 6.378, 1, '2021-08-09 11:14:08.705475', NULL),
(412, 7.625, 42.8, 6.501, NULL, NULL, 'Grant Prideco STL', 7.626, 1, 'API', 6.378, 1, '2021-08-09 11:14:08.710819', NULL),
(413, 7.625, 42.8, 6.501, NULL, NULL, 'Hydril LX', 7.788, 1, 'API', 6.378, 1, '2021-08-09 11:14:08.716574', NULL),
(414, 7.625, 42.8, 6.501, NULL, NULL, 'Hydril 563', 8.5, 1, 'API', 6.378, 1, '2021-08-09 11:14:08.722455', NULL),
(415, 7.625, 42.8, 6.501, NULL, NULL, 'Valluorec VAM New', 8.528, 1, 'API', 6.378, 1, '2021-08-09 11:14:08.728498', NULL),
(416, 7.625, 42.8, 6.501, NULL, NULL, 'Valluorec VAM ACE', 8.512, 1, 'API', 6.378, 1, '2021-08-09 11:14:08.734643', NULL),
(417, 7.625, 42.8, 6.501, NULL, NULL, 'Valluorec VAM PRO', 8.52, 1, 'API', 6.378, 1, '2021-08-09 11:14:08.740603', NULL),
(418, 7.625, 42.8, 6.501, NULL, NULL, 'Valluorec FJL', 7.626, 1, 'API', 6.378, 1, '2021-08-09 11:14:08.746788', NULL),
(419, 7.625, 39, 6.625, NULL, NULL, 'BTC', 8.5, 1, 'API', 6.5, 1, '2021-08-09 11:14:08.752749', NULL),
(420, 7.625, 39, 6.625, NULL, NULL, 'BTC Special', 8.126, 1, 'API', 6.5, 1, '2021-08-09 11:14:08.758771', NULL),
(421, 7.625, 39, 6.625, NULL, NULL, 'LTC', 8.5, 1, 'API', 6.5, 1, '2021-08-09 11:14:08.765018', NULL),
(422, 7.625, 39, 6.625, NULL, NULL, 'Grant Prideco TCII', 8.39, 1, 'API', 6.5, 1, '2021-08-09 11:14:08.771180', NULL),
(423, 7.625, 39, 6.625, NULL, NULL, 'Grant Prideco STL', 7.626, 1, 'API', 6.5, 1, '2021-08-09 11:14:08.777782', NULL),
(424, 7.625, 39, 6.625, NULL, NULL, 'Hydril LX', 7.776, 1, 'API', 6.5, 1, '2021-08-09 11:14:08.784631', NULL),
(425, 7.625, 39, 6.625, NULL, NULL, 'Hydril 563', 8.5, 1, 'API', 6.5, 1, '2021-08-09 11:14:08.791540', NULL),
(426, 7.625, 39, 6.625, NULL, NULL, 'Hydril 521', 8.15, 1, 'API', 6.5, 1, '2021-08-09 11:14:08.798279', NULL),
(427, 7.625, 39, 6.625, NULL, NULL, 'Valluorec VAM New', 8.528, 1, 'API', 6.5, 1, '2021-08-09 11:14:08.804640', NULL),
(428, 7.625, 39, 6.625, NULL, NULL, 'Valluorec VAM ACE', 8.5, 1, 'API', 6.5, 1, '2021-08-09 11:14:08.811212', NULL),
(429, 7.625, 39, 6.625, NULL, NULL, 'Valluorec VAM PRO', 8.52, 1, 'API', 6.5, 1, '2021-08-09 11:14:08.817185', NULL),
(430, 7.625, 39, 6.625, NULL, NULL, 'Valluorec VAM TOP', 8.418, 1, 'API', 6.5, 1, '2021-08-09 11:14:08.822453', NULL),
(431, 7.625, 39, 6.625, NULL, NULL, 'Valluorec FJL', 7.628, 1, 'API', 6.5, 1, '2021-08-09 11:14:08.827776', NULL),
(432, 7.625, 35.8, 6.695, NULL, NULL, 'BTC', 8.5, 1, 'API', 6.571, 1, '2021-08-09 11:14:08.833373', NULL),
(433, 7.625, 35.8, 6.695, NULL, NULL, 'BTC Special', 8.126, 1, 'API', 6.571, 1, '2021-08-09 11:14:08.838613', NULL);
INSERT INTO `wellphases_casing` (`id`, `nominal_od`, `weight`, `inside_diameter`, `grade`, `casing_range`, `connection_type`, `connection_od`, `is_superadmin`, `unit`, `drift_id`, `status`, `created`, `company_id`) VALUES
(438, 7, 46, 5.66, NULL, NULL, 'BTC', 7.658, 1, 'API', 5.536, 1, '2023-07-23 16:03:51.372297', NULL),
(439, 7, 46, 5.66, NULL, NULL, 'BTC Special', 7.374, 1, 'API', 5.536, 1, '2023-07-23 16:03:51.398115', NULL),
(440, 7, 46, 5.66, NULL, NULL, 'Grant Prideco STL', 7, 1, 'API', 5.536, 1, '2023-07-23 16:03:51.409023', NULL),
(441, 7, 46, 5.66, NULL, NULL, 'Valluorec VAM New', 7.681, 1, 'API', 5.536, 1, '2023-07-23 16:03:51.431808', NULL),
(442, 7, 46, 5.66, NULL, NULL, 'Valluorec VAM PRO', 7.678, 1, 'API', 5.536, 1, '2023-07-23 16:03:51.484777', NULL),
(443, 7, 44, 5.72, NULL, NULL, 'BTC', 7.658, 1, 'API', 5.595, 1, '2023-07-23 16:03:51.502114', NULL),
(444, 7, 44, 5.72, NULL, NULL, 'BTC Special', 7.374, 1, 'API', 5.595, 1, '2023-07-23 16:03:51.525775', NULL),
(445, 7, 44, 5.72, NULL, NULL, 'Grant Prideco STL', 7, 1, 'API', 5.595, 1, '2023-07-23 16:03:51.534508', NULL),
(446, 7, 44, 5.72, NULL, NULL, 'Valluorec VAM New', 7.681, 1, 'API', 5.595, 1, '2023-07-23 16:03:51.550818', NULL),
(447, 7, 44, 5.72, NULL, NULL, 'Valluorec VAM PRO', 7.678, 1, 'API', 5.595, 1, '2023-07-23 16:03:51.560047', NULL),
(448, 7, 41, 5.82, NULL, NULL, 'BTC', 7.658, 1, 'API', 5.697, 1, '2023-07-23 16:03:51.579518', NULL),
(449, 7, 41, 5.82, NULL, NULL, 'BTC Special', 7.374, 1, 'API', 5.697, 1, '2023-07-23 16:03:51.646860', NULL),
(450, 7, 41, 5.82, NULL, NULL, 'Grant Prideco TCII', 7.882, 1, 'API', 5.697, 1, '2023-07-23 16:03:51.655617', NULL),
(451, 7, 41, 5.82, NULL, NULL, 'Grant Prideco STL', 7, 1, 'API', 5.697, 1, '2023-07-23 16:03:51.712338', NULL),
(452, 7, 41, 5.82, NULL, NULL, 'Hydril LX', 7.162, 1, 'API', 5.697, 1, '2023-07-23 16:03:51.721269', NULL),
(453, 7, 41, 5.82, NULL, NULL, 'Hydril 563', 7.748, 1, 'API', 5.697, 1, '2023-07-23 16:03:51.734691', NULL),
(454, 7, 41, 5.82, NULL, NULL, 'Valluorec VAM New', 7.681, 1, 'API', 5.697, 1, '2023-07-23 16:03:51.742967', NULL),
(455, 7, 41, 5.82, NULL, NULL, 'Valluorec VAM ACE', 7.941, 1, 'API', 5.697, 1, '2023-07-23 16:03:51.762783', NULL),
(456, 7, 41, 5.82, NULL, NULL, 'Valluorec VAM PRO', 7.678, 1, 'API', 5.697, 1, '2023-07-23 16:03:51.795610', NULL),
(457, 7, 41, 5.82, NULL, NULL, 'Valluorec VAM TOP', 7.93, 1, 'API', 5.697, 1, '2023-07-23 16:03:51.804251', NULL),
(458, 7, 41, 5.82, NULL, NULL, 'Valluorec FJL', 7, 1, 'API', 5.697, 1, '2023-07-23 16:03:51.811377', NULL),
(459, 7, 38, 5.92, NULL, NULL, 'BTC', 7.658, 1, 'API', 5.796, 1, '2023-07-23 16:03:51.847936', NULL),
(460, 7, 38, 5.92, NULL, NULL, 'BTC Special', 7.374, 1, 'API', 5.796, 1, '2023-07-23 16:03:51.856551', NULL),
(461, 7, 38, 5.92, NULL, NULL, 'LTC', 7.658, 1, 'API', 5.796, 1, '2023-07-23 16:03:51.876010', NULL),
(462, 7, 38, 5.92, NULL, NULL, 'Grant Prideco TCII', 7.807, 1, 'API', 5.796, 1, '2023-07-23 16:03:51.908127', NULL),
(463, 7, 38, 5.92, NULL, NULL, 'Grant Prideco STL', 7, 1, 'API', 5.796, 1, '2023-07-23 16:03:51.916937', NULL),
(464, 7, 38, 5.92, NULL, NULL, 'Hydril LX', 7.17, 1, 'API', 5.796, 1, '2023-07-23 16:03:51.926236', NULL),
(465, 7, 38, 5.92, NULL, NULL, 'Hydril 563', 7.748, 1, 'API', 5.796, 1, '2023-07-23 16:03:51.943875', NULL),
(466, 7, 38, 5.92, NULL, NULL, 'Valluorec VAM New', 7.681, 1, 'API', 5.796, 1, '2023-07-23 16:03:51.950976', NULL),
(467, 7, 38, 5.92, NULL, NULL, 'Valluorec VAM ACE', 7.91, 1, 'API', 5.796, 1, '2023-07-23 16:03:51.959414', NULL),
(468, 7, 38, 5.92, NULL, NULL, 'Valluorec VAM PRO', 7.678, 1, 'API', 5.796, 1, '2023-07-23 16:03:51.981622', NULL),
(469, 7, 38, 5.92, NULL, NULL, 'Valluorec VAM TOP', 7.851, 1, 'API', 5.796, 1, '2023-07-23 16:03:52.043960', NULL),
(470, 7, 38, 5.92, NULL, NULL, 'Valluorec FJL', 7, 1, 'API', 5.796, 1, '2023-07-23 16:03:52.158698', NULL),
(471, 7, 35, 6.004, NULL, NULL, 'BTC', 7.658, 1, 'API', 5.878, 1, '2023-07-23 16:03:52.275702', NULL),
(472, 7, 35, 6.004, NULL, NULL, 'BTC Special', 7.374, 1, 'API', 5.878, 1, '2023-07-23 16:03:52.367872', NULL),
(473, 7, 35, 6.004, NULL, NULL, 'LTC', 7.658, 1, 'API', 5.878, 1, '2023-07-23 16:03:52.376900', NULL),
(474, 7, 35, 6.004, NULL, NULL, 'Grant Prideco TCII', 7.744, 1, 'API', 5.878, 1, '2023-07-23 16:03:52.741955', NULL),
(475, 7, 35, 6.004, NULL, NULL, 'Grant Prideco STL', 7, 1, 'API', 5.878, 1, '2023-07-23 16:03:52.774495', NULL),
(476, 7, 35, 6.004, NULL, NULL, 'Hydril LX', 7.146, 1, 'API', 5.878, 1, '2023-07-23 16:03:52.782930', NULL),
(477, 7, 35, 6.004, NULL, NULL, 'Hydril 563', 7.748, 1, 'API', 5.878, 1, '2023-07-23 16:03:52.799804', NULL),
(478, 7, 35, 6.004, NULL, NULL, 'Valluorec VAM New', 7.681, 1, 'API', 5.878, 1, '2023-07-23 16:03:52.807897', NULL),
(479, 7, 35, 6.004, NULL, NULL, 'Valluorec VAM ACE', 7.91, 1, 'API', 5.878, 1, '2023-07-23 16:03:52.815704', NULL),
(480, 7, 35, 6.004, NULL, NULL, 'Valluorec VAM PRO', 7.678, 1, 'API', 5.878, 1, '2023-07-23 16:03:52.822863', NULL),
(481, 7, 35, 6.004, NULL, NULL, 'Valluorec VAM TOP', 7.788, 1, 'API', 5.878, 1, '2023-07-23 16:03:52.832106', NULL),
(482, 7, 35, 6.004, NULL, NULL, 'Valluorec FJL', 7, 1, 'API', 5.878, 1, '2023-07-23 16:03:52.873258', NULL),
(483, 7, 32, 6.094, NULL, NULL, 'BTC', 7.658, 1, 'API', 5.969, 1, '2023-07-23 16:03:52.882760', NULL),
(484, 7, 32, 6.094, NULL, NULL, 'BTC Special', 7.374, 1, 'API', 5.969, 1, '2023-07-23 16:03:52.923398', NULL),
(485, 7, 32, 6.094, NULL, NULL, 'LTC', 7.658, 1, 'API', 5.969, 1, '2023-07-23 16:03:52.987252', NULL),
(486, 7, 32, 6.094, NULL, NULL, 'Grant Prideco TCII', 7.674, 1, 'API', 5.969, 1, '2023-07-23 16:03:53.012359', NULL),
(487, 7, 32, 6.094, NULL, NULL, 'Grant Prideco STL', 7, 1, 'API', 5.969, 1, '2023-07-23 16:03:53.023040', NULL),
(488, 7, 32, 6.094, NULL, NULL, 'Hydril LX', 7.154, 1, 'API', 5.969, 1, '2023-07-23 16:03:53.043857', NULL),
(489, 7, 32, 6.094, NULL, NULL, 'Hydril 563', 7.658, 1, 'API', 5.969, 1, '2023-07-23 16:03:53.086898', NULL),
(490, 7, 32, 6.094, NULL, NULL, 'Hydril 521', 7.449, 1, 'API', 5.969, 1, '2023-07-23 16:03:53.096468', NULL),
(491, 7, 32, 6.094, NULL, NULL, 'Valluorec VAM New', 7.681, 1, 'API', 5.969, 1, '2023-07-23 16:03:53.105549', NULL),
(492, 7, 32, 6.094, NULL, NULL, 'Valluorec VAM ACE', 7.91, 1, 'API', 5.969, 1, '2023-07-23 16:03:53.115240', NULL),
(493, 7, 32, 6.094, NULL, NULL, 'Valluorec VAM PRO', 7.678, 1, 'API', 5.969, 1, '2023-07-23 16:03:53.125808', NULL),
(494, 7, 32, 6.094, NULL, NULL, 'Valluorec VAM TOP', 7.717, 1, 'API', 5.969, 1, '2023-07-23 16:03:53.136270', NULL),
(495, 7, 32, 6.094, NULL, NULL, 'Valluorec FJL', 7, 1, 'API', 5.969, 1, '2023-07-23 16:03:53.146079', NULL),
(496, 7, 29, 6.184, NULL, NULL, 'BTC', 7.658, 1, 'API', 6.059, 1, '2023-07-23 16:03:53.156423', NULL),
(497, 7, 29, 6.184, NULL, NULL, 'BTC Special', 7.374, 1, 'API', 6.059, 1, '2023-07-23 16:03:53.177134', NULL),
(498, 7, 29, 6.184, NULL, NULL, 'LTC', 7.654, 1, 'API', 6.059, 1, '2023-07-23 16:03:53.205720', NULL),
(499, 7, 29, 6.184, NULL, NULL, 'Grant Prideco TCII', 7.599, 1, 'API', 6.059, 1, '2023-07-23 16:03:53.252116', NULL),
(500, 7, 29, 6.184, NULL, NULL, 'Grant Prideco STL', 7, 1, 'API', 6.059, 1, '2023-07-23 16:03:53.294966', NULL),
(501, 7, 29, 6.184, NULL, NULL, 'Hydril LX', 7.13, 1, 'API', 6.059, 1, '2023-07-23 16:03:53.304060', NULL),
(502, 7, 29, 6.184, NULL, NULL, 'Hydril 563', 7.658, 1, 'API', 6.059, 1, '2023-07-23 16:03:53.310950', NULL),
(503, 7, 29, 6.184, NULL, NULL, 'Hydril 511', 7, 1, 'API', 6.059, 1, '2023-07-23 16:03:53.318874', NULL),
(504, 7, 29, 6.184, NULL, NULL, 'Hydril 521', 7.374, 1, 'API', 6.059, 1, '2023-07-23 16:03:53.342662', NULL),
(505, 7, 29, 6.184, NULL, NULL, 'Valluorec VAM New', 7.681, 1, 'API', 6.059, 1, '2023-07-23 16:03:53.352307', NULL),
(506, 7, 29, 6.184, NULL, NULL, 'Valluorec VAM ACE', 7.658, 1, 'API', 6.059, 1, '2023-07-23 16:03:53.385169', NULL),
(507, 7, 29, 6.184, NULL, NULL, 'Valluorec VAM PRO', 7.678, 1, 'API', 6.059, 1, '2023-07-23 16:03:53.399519', NULL),
(508, 7, 29, 6.184, NULL, NULL, 'Valluorec VAM TOP', 7.646, 1, 'API', 6.059, 1, '2023-07-23 16:03:53.406130', NULL),
(509, 7, 29, 6.184, NULL, NULL, 'Valluorec FJL', 7, 1, 'API', 6.059, 1, '2023-07-23 16:03:53.420959', NULL),
(510, 7, 26, 6.276, NULL, NULL, 'BTC', 7.658, 1, 'API', 6.15, 1, '2023-07-23 16:03:53.428911', NULL),
(511, 7, 26, 6.276, NULL, NULL, 'BTC Special', 7.374, 1, 'API', 6.15, 1, '2023-07-23 16:03:53.437023', NULL),
(512, 7, 26, 6.276, NULL, NULL, 'STC', 7.658, 1, 'API', 6.15, 1, '2023-07-23 16:03:53.444458', NULL),
(513, 7, 26, 6.276, NULL, NULL, 'LTC', 7.654, 1, 'API', 6.15, 1, '2023-07-23 16:03:53.455024', NULL),
(514, 7, 26, 6.276, NULL, NULL, 'Grant Prideco TCII', 7.524, 1, 'API', 6.15, 1, '2023-07-23 16:03:53.464278', NULL),
(515, 7, 26, 6.276, NULL, NULL, 'Grant Prideco STL', 7, 1, 'API', 6.15, 1, '2023-07-23 16:03:53.475960', NULL),
(516, 7, 26, 6.276, NULL, NULL, 'Hydril LX', 7.118, 1, 'API', 6.15, 1, '2023-07-23 16:03:53.484180', NULL),
(517, 7, 26, 6.276, NULL, NULL, 'Hydril 563', 7.658, 1, 'API', 6.15, 1, '2023-07-23 16:03:53.491304', NULL),
(518, 7, 26, 6.276, NULL, NULL, 'Hydril 511', 7, 1, 'API', 6.15, 1, '2023-07-23 16:03:53.498340', NULL),
(519, 7, 26, 6.276, NULL, NULL, 'Hydril 521', 7.3, 1, 'API', 6.15, 1, '2023-07-23 16:03:53.506288', NULL),
(520, 7, 26, 6.276, NULL, NULL, 'Valluorec VAM New', 7.681, 1, 'API', 6.15, 1, '2023-07-23 16:03:53.514113', NULL),
(521, 7, 26, 6.276, NULL, NULL, 'Valluorec VAM ACE', 7.658, 1, 'API', 6.15, 1, '2023-07-23 16:03:53.524115', NULL),
(522, 7, 26, 6.276, NULL, NULL, 'Valluorec VAM PRO', 7.678, 1, 'API', 6.15, 1, '2023-07-23 16:03:53.534475', NULL),
(523, 7, 26, 6.276, NULL, NULL, 'Valluorec VAM TOP', 7.567, 1, 'API', 6.15, 1, '2023-07-23 16:03:53.544066', NULL),
(524, 7, 26, 6.276, NULL, NULL, 'Valluorec FJL', 7, 1, 'API', 6.15, 1, '2023-07-23 16:03:53.550724', NULL),
(525, 7, 23, 6.366, NULL, NULL, 'BTC', 7.658, 1, 'API', 6.24, 1, '2023-07-23 16:03:53.558022', NULL),
(526, 7, 23, 6.366, NULL, NULL, 'BTC Special', 7.374, 1, 'API', 6.24, 1, '2023-07-23 16:03:53.565147', NULL),
(527, 7, 23, 6.366, NULL, NULL, 'STC', 7.658, 1, 'API', 6.24, 1, '2023-07-23 16:03:53.572566', NULL),
(528, 7, 23, 6.366, NULL, NULL, 'LTC', 7.658, 1, 'API', 6.24, 1, '2023-07-23 16:03:53.579832', NULL),
(529, 7, 23, 6.366, NULL, NULL, 'Grant Prideco TCII', 7.449, 1, 'API', 6.24, 1, '2023-07-23 16:03:53.586169', NULL),
(530, 7, 23, 6.366, NULL, NULL, 'Grant Prideco STL', 7, 1, 'API', 6.24, 1, '2023-07-23 16:03:53.595304', NULL),
(531, 7, 23, 6.366, NULL, NULL, 'Hydril LX', 7.111, 1, 'API', 6.24, 1, '2023-07-23 16:03:53.603555', NULL),
(532, 7, 23, 6.366, NULL, NULL, 'Hydril 563', 7.658, 1, 'API', 6.24, 1, '2023-07-23 16:03:53.611081', NULL),
(533, 7, 23, 6.366, NULL, NULL, 'Hydril 511', 7, 1, 'API', 6.24, 1, '2023-07-23 16:03:53.618829', NULL),
(534, 7, 23, 6.366, NULL, NULL, 'Hydril 521', 7.225, 1, 'API', 6.24, 1, '2023-07-23 16:03:53.625603', NULL),
(535, 7, 23, 6.366, NULL, NULL, 'Valluorec VAM New', 7.681, 1, 'API', 6.24, 1, '2023-07-23 16:03:53.641655', NULL),
(536, 7, 23, 6.366, NULL, NULL, 'Valluorec VAM ACE', 7.658, 1, 'API', 6.24, 1, '2023-07-23 16:03:53.651682', NULL),
(537, 7, 23, 6.366, NULL, NULL, 'Valluorec VAM PRO', 7.678, 1, 'API', 6.24, 1, '2023-07-23 16:03:53.659686', NULL),
(538, 7, 23, 6.366, NULL, NULL, 'Valluorec VAM TOP', 7.489, 1, 'API', 6.24, 1, '2023-07-23 16:03:53.668428', NULL),
(539, 7, 23, 6.366, NULL, NULL, 'Valluorec FJL', 7, 1, 'API', 6.24, 1, '2023-07-23 16:03:53.676997', NULL),
(540, 7, 20, 6.456, NULL, NULL, 'BTC', 7.658, 1, 'API', 6.331, 1, '2023-07-23 16:03:53.684758', NULL),
(541, 7, 20, 6.456, NULL, NULL, 'BTC Special', 7.374, 1, 'API', 6.331, 1, '2023-07-23 16:03:53.693062', NULL),
(542, 7, 20, 6.456, NULL, NULL, 'STC', 7.658, 1, 'API', 6.331, 1, '2023-07-23 16:03:53.702613', NULL),
(543, 7, 20, 6.456, NULL, NULL, 'Grant Prideco STL', 7, 1, 'API', 6.331, 1, '2023-07-23 16:03:53.710589', NULL),
(544, 7, 20, 6.456, NULL, NULL, 'Hydril 563', 7.658, 1, 'API', 6.331, 1, '2023-07-23 16:03:53.718230', NULL),
(545, 7, 20, 6.456, NULL, NULL, 'Hydril 521', 7.15, 1, 'API', 6.331, 1, '2023-07-23 16:03:53.725820', NULL),
(546, 7, 20, 6.456, NULL, NULL, 'Valluorec VAM PRO', 7.678, 1, 'API', 6.331, 1, '2023-07-23 16:03:53.734096', NULL),
(547, 6.625, 35, 5.575, NULL, NULL, 'BTC', 7.3901244, 1, 'API', 5.4490848, 1, '2023-07-23 16:10:18.795534', NULL),
(548, 6.625, 35, 5.575, NULL, NULL, 'BTC Special', 7.0003416, 1, 'API', 5.4490848, 1, '2023-07-23 16:10:18.806107', NULL),
(549, 6.625, 35, 5.575, NULL, NULL, 'Grant PridecoTCII', 7.421622, 1, 'API', 5.4490848, 1, '2023-07-23 16:10:18.815730', NULL),
(550, 6.625, 35, 5.575, NULL, NULL, 'Hydril LX', 6.771984, 1, 'API', 5.4490848, 1, '2023-07-23 16:10:18.913637', NULL),
(551, 6.625, 35, 5.575, NULL, NULL, 'Valluorec VAM New', 7.4137476, 1, 'API', 5.4490848, 1, '2023-07-23 16:10:18.922716', NULL),
(552, 6.625, 35, 5.575, NULL, NULL, 'Valluorec VAM ACE', 7.4649312, 1, 'API', 5.4490848, 1, '2023-07-23 16:10:18.931670', NULL),
(553, 6.625, 35, 5.575, NULL, NULL, 'Valluorec VAM PRO', 7.4098104, 1, 'API', 5.4490848, 1, '2023-07-23 16:10:18.940676', NULL),
(554, 6.625, 35, 5.575, NULL, NULL, 'Valluorec FJL', 6.6263076, 1, 'API', 5.4490848, 1, '2023-07-23 16:10:18.949297', NULL),
(555, 6.625, 32, 5.675, NULL, NULL, 'BTC', 7.3901244, 1, 'API', 5.551452, 1, '2023-07-23 16:10:18.957178', NULL),
(556, 6.625, 32, 5.675, NULL, NULL, 'BTC Special', 7.0003416, 1, 'API', 5.551452, 1, '2023-07-23 16:10:18.965726', NULL),
(557, 6.625, 32, 5.675, NULL, NULL, 'LTC', 7.3901244, 1, 'API', 5.551452, 1, '2023-07-23 16:10:18.974286', NULL),
(558, 6.625, 32, 5.675, NULL, NULL, 'Grant Prideco TCII', 7.3468152, 1, 'API', 5.551452, 1, '2023-07-23 16:10:18.982867', NULL),
(559, 6.625, 32, 5.675, NULL, NULL, 'Grant Prideco STL', 6.6263076, 1, 'API', 5.551452, 1, '2023-07-23 16:10:18.991605', NULL),
(560, 6.625, 32, 5.675, NULL, NULL, 'Hydril LX', 6.7641096, 1, 'API', 5.551452, 1, '2023-07-23 16:10:18.999645', NULL),
(561, 6.625, 32, 5.675, NULL, NULL, 'Hydril 563', 7.3901244, 1, 'API', 5.551452, 1, '2023-07-23 16:10:19.006491', NULL),
(562, 6.625, 32, 5.675, NULL, NULL, 'Hydril 521', 7.1184576, 1, 'API', 5.551452, 1, '2023-07-23 16:10:19.015696', NULL),
(563, 6.625, 32, 5.675, NULL, NULL, 'Valluorec VAM New', 7.4137476, 1, 'API', 5.551452, 1, '2023-07-23 16:10:19.023666', NULL),
(564, 6.625, 32, 5.675, NULL, NULL, 'Valluorec VAM ACE', 7.3901244, 1, 'API', 5.551452, 1, '2023-07-23 16:10:19.056014', NULL),
(565, 6.625, 32, 5.675, NULL, NULL, 'Valluorec VAM PRO', 7.4098104, 1, 'API', 5.551452, 1, '2023-07-23 16:10:19.086028', NULL),
(566, 6.625, 32, 5.675, NULL, NULL, 'Valluorec FJL', 6.6263076, 1, 'API', 5.551452, 1, '2023-07-23 16:10:19.096572', NULL),
(567, 6.625, 28, 5.791, NULL, NULL, 'BTC', 7.3901244, 1, 'API', 5.6656308, 1, '2023-07-23 16:10:19.104894', NULL),
(568, 6.625, 28, 5.791, NULL, NULL, 'BTC Special', 7.0003416, 1, 'API', 5.6656308, 1, '2023-07-23 16:10:19.112814', NULL),
(569, 6.625, 28, 5.791, NULL, NULL, 'LTC', 7.3901244, 1, 'API', 5.6656308, 1, '2023-07-23 16:10:19.121977', NULL),
(570, 6.625, 28, 5.791, NULL, NULL, 'Grant Prideco TCII', 7.2562596, 1, 'API', 5.6656308, 1, '2023-07-23 16:10:19.176595', NULL),
(571, 6.625, 28, 5.791, NULL, NULL, 'Grant Prideco STL', 6.6263076, 1, 'API', 5.6656308, 1, '2023-07-23 16:10:19.185212', NULL),
(572, 6.625, 28, 5.791, NULL, NULL, 'Hydril LX', 6.752298, 1, 'API', 5.6656308, 1, '2023-07-23 16:10:19.193471', NULL),
(573, 6.625, 28, 5.791, NULL, NULL, 'Hydril 563', 7.3901244, 1, 'API', 5.6656308, 1, '2023-07-23 16:10:19.201263', NULL),
(574, 6.625, 28, 5.791, NULL, NULL, 'Hydril 511', 6.6263076, 1, 'API', 5.6656308, 1, '2023-07-23 16:10:19.208854', NULL),
(575, 6.625, 28, 5.791, NULL, NULL, 'Hydril 521', 7.027902, 1, 'API', 5.6656308, 1, '2023-07-23 16:10:19.216730', NULL),
(576, 6.625, 28, 5.791, NULL, NULL, 'Valluorec VAM New', 7.4137476, 1, 'API', 5.6656308, 1, '2023-07-23 16:10:19.224736', NULL),
(577, 6.625, 28, 5.791, NULL, NULL, 'Valluorec VAM ACE', 7.3901244, 1, 'API', 5.6656308, 1, '2023-07-23 16:10:19.232187', NULL),
(578, 6.625, 28, 5.791, NULL, NULL, 'Valluorec VAM PRO', 7.4098104, 1, 'API', 5.6656308, 1, '2023-07-23 16:10:19.238413', NULL),
(579, 6.625, 28, 5.791, NULL, NULL, 'Valluorec VAM TOP', 7.2956316, 1, 'API', 5.6656308, 1, '2023-07-23 16:10:19.246018', NULL),
(580, 6.625, 28, 5.791, NULL, NULL, 'Valluorec FJL', 6.6263076, 1, 'API', 5.6656308, 1, '2023-07-23 16:10:19.254131', NULL),
(581, 6.625, 24, 5.921, NULL, NULL, 'BTC', 7.3901244, 1, 'API', 5.7955584, 1, '2023-07-23 16:10:19.261872', NULL),
(582, 6.625, 24, 5.921, NULL, NULL, 'BTC Special', 7.0003416, 1, 'API', 5.7955584, 1, '2023-07-23 16:10:19.270044', NULL),
(583, 6.625, 24, 5.921, NULL, NULL, 'STC', 7.3901244, 1, 'API', 5.7955584, 1, '2023-07-23 16:10:19.277456', NULL),
(584, 6.625, 24, 5.921, NULL, NULL, 'LTC', 7.3901244, 1, 'API', 5.7955584, 1, '2023-07-23 16:10:19.285480', NULL),
(585, 6.625, 24, 5.921, NULL, NULL, 'Grant Prideco TCII', 7.1499552, 1, 'API', 5.7955584, 1, '2023-07-23 16:10:19.292471', NULL),
(586, 6.625, 24, 5.921, NULL, NULL, 'Grant Prideco STL', 6.6263076, 1, 'API', 5.7955584, 1, '2023-07-23 16:10:19.298904', NULL),
(587, 6.625, 24, 5.921, NULL, NULL, 'Hydril LX', 6.7404864, 1, 'API', 5.7955584, 1, '2023-07-23 16:10:19.306331', NULL),
(588, 6.625, 24, 5.921, NULL, NULL, 'Hydril 563', 7.3901244, 1, 'API', 5.7955584, 1, '2023-07-23 16:10:19.314759', NULL),
(589, 6.625, 24, 5.921, NULL, NULL, 'Hydril 511', 6.6263076, 1, 'API', 5.7955584, 1, '2023-07-23 16:10:19.321606', NULL),
(590, 6.625, 24, 5.921, NULL, NULL, 'Hydril 521', 6.9255348, 1, 'API', 5.7955584, 1, '2023-07-23 16:10:19.346208', NULL),
(591, 6.625, 24, 5.921, NULL, NULL, 'Valluorec VAM New', 7.4137476, 1, 'API', 5.7955584, 1, '2023-07-23 16:10:19.355034', NULL),
(592, 6.625, 24, 5.921, NULL, NULL, 'Valluorec VAM ACE', 7.3901244, 1, 'API', 5.7955584, 1, '2023-07-23 16:10:19.361805', NULL),
(593, 6.625, 24, 5.921, NULL, NULL, 'Valluorec VAM PRO', 7.4098104, 1, 'API', 5.7955584, 1, '2023-07-23 16:10:19.370061', NULL),
(594, 6.625, 24, 5.921, NULL, NULL, 'Valluorec VAM TOP', 7.1932644, 1, 'API', 5.7955584, 1, '2023-07-23 16:10:19.377806', NULL),
(595, 6.625, 24, 5.921, NULL, NULL, 'Valluorec FJL', 6.6263076, 1, 'API', 5.7955584, 1, '2023-07-23 16:10:19.385421', NULL),
(596, 6.625, 23.2, 5.965, NULL, NULL, 'BTC', 7.3901244, 1, 'API', 5.8388676, 1, '2023-07-23 16:10:19.394419', NULL),
(597, 6.625, 23.2, 5.965, NULL, NULL, 'BTC Special', 7.0003416, 1, 'API', 5.8388676, 1, '2023-07-23 16:10:19.401941', NULL),
(598, 6.625, 23.2, 5.965, NULL, NULL, 'Grant Prideco TCII', 7.1105832, 1, 'API', 5.8388676, 1, '2023-07-23 16:10:19.410165', NULL),
(599, 6.625, 23.2, 5.965, NULL, NULL, 'Hydril LX', 6.7365492, 1, 'API', 5.8388676, 1, '2023-07-23 16:10:19.425062', NULL),
(600, 6.625, 23.2, 5.965, NULL, NULL, 'Valluorec VAM New', 7.4137476, 1, 'API', 5.8388676, 1, '2023-07-23 16:10:19.433614', NULL),
(601, 6.625, 23.2, 5.965, NULL, NULL, 'Valluorec VAM PRO', 7.4098104, 1, 'API', 5.8388676, 1, '2023-07-23 16:10:19.441771', NULL),
(602, 6.625, 23.2, 5.965, NULL, NULL, 'Valluorec VAM TOP', 7.1538924, 1, 'API', 5.8388676, 1, '2023-07-23 16:10:19.448937', NULL),
(603, 6.625, 23.2, 5.965, NULL, NULL, 'Valluorec FJL', 6.6263076, 1, 'API', 5.8388676, 1, '2023-07-23 16:10:19.456423', NULL),
(604, 6.625, 20, 6.049, NULL, NULL, 'BTC', 7.3901244, 1, 'API', 5.925486, 1, '2023-07-23 16:10:19.462819', NULL),
(605, 6.625, 20, 6.049, NULL, NULL, 'BTC Special', 7.0003416, 1, 'API', 5.925486, 1, '2023-07-23 16:10:19.469124', NULL),
(606, 6.625, 20, 6.049, NULL, NULL, 'STC', 7.3901244, 1, 'API', 5.925486, 1, '2023-07-23 16:10:19.476498', NULL),
(607, 6.625, 20, 6.049, NULL, NULL, 'LTC', 7.3901244, 1, 'API', 5.925486, 1, '2023-07-23 16:10:19.484552', NULL),
(608, 6.625, 20, 6.049, NULL, NULL, 'Grant Prideco TCII', 7.0397136, 1, 'API', 5.925486, 1, '2023-07-23 16:10:19.492770', NULL),
(609, 6.625, 20, 6.049, NULL, NULL, 'Grant Prideco STL', 6.6263076, 1, 'API', 5.925486, 1, '2023-07-23 16:10:19.501770', NULL),
(610, 6.625, 20, 6.049, NULL, NULL, 'Hydril 563', 7.3901244, 1, 'API', 5.925486, 1, '2023-07-23 16:10:19.510808', NULL),
(611, 6.625, 20, 6.049, NULL, NULL, 'Hydril 521', 6.8192304, 1, 'API', 5.925486, 1, '2023-07-23 16:10:19.518683', NULL),
(612, 6.625, 20, 6.049, NULL, NULL, 'Valluorec VAM New', 7.4137476, 1, 'API', 5.925486, 1, '2023-07-23 16:10:19.525510', NULL),
(613, 6.625, 20, 6.049, NULL, NULL, 'Valluorec VAM ACE', 7.3901244, 1, 'API', 5.925486, 1, '2023-07-23 16:10:19.533156', NULL),
(614, 6.625, 20, 6.049, NULL, NULL, 'Valluorec VAM PRO', 7.4098104, 1, 'API', 5.925486, 1, '2023-07-23 16:10:19.541023', NULL),
(615, 6.625, 20, 6.049, NULL, NULL, 'Valluorec VAM TOP', 7.0830228, 1, 'API', 5.925486, 1, '2023-07-23 16:10:19.548975', NULL),
(616, 5.5, 26.8, 4.5, NULL, NULL, 'BTC', 6.0514764, 1, 'API', 4.3742292, 1, '2023-07-23 16:10:19.572382', NULL),
(617, 5.5, 26.8, 4.5, NULL, NULL, 'BTC Special', 5.8743024, 1, 'API', 4.3742292, 1, '2023-07-23 16:10:19.578758', NULL),
(618, 5.5, 26.8, 4.5, NULL, NULL, 'Grant Prideco TCII', 6.2483364, 1, 'API', 4.3742292, 1, '2023-07-23 16:10:19.586726', NULL),
(619, 5.5, 26.8, 4.5, NULL, NULL, 'Grant Prideco STL', 5.5002684, 1, 'API', 4.3742292, 1, '2023-07-23 16:10:19.594173', NULL),
(620, 5.5, 26.8, 4.5, NULL, NULL, 'Hydril LX', 5.6341332, 1, 'API', 4.3742292, 1, '2023-07-23 16:10:19.602981', NULL),
(621, 5.5, 26.8, 4.5, NULL, NULL, 'Hydril 563', 6.1262832, 1, 'API', 4.3742292, 1, '2023-07-23 16:10:19.610650', NULL),
(622, 5.5, 26.8, 4.5, NULL, NULL, 'Valluorec VAM ACE', 6.279834, 1, 'API', 4.3742292, 1, '2023-07-23 16:10:19.619571', NULL),
(623, 5.5, 26.8, 4.5, NULL, NULL, 'Valluorec FJL', 5.5002684, 1, 'API', 4.3742292, 1, '2023-07-23 16:10:19.626991', NULL),
(624, 5.5, 26, 4.548, NULL, NULL, 'BTC', 6.0514764, 1, 'API', 4.4214756, 1, '2023-07-23 16:10:19.634017', NULL),
(625, 5.5, 26, 4.548, NULL, NULL, 'BTC Special', 5.8743024, 1, 'API', 4.4214756, 1, '2023-07-23 16:10:19.642743', NULL),
(626, 5.5, 26, 4.548, NULL, NULL, 'Grant Prideco TCII', 6.2129016, 1, 'API', 4.4214756, 1, '2023-07-23 16:10:19.650235', NULL),
(627, 5.5, 26, 4.548, NULL, NULL, 'Grant Prideco STL', 5.5002684, 1, 'API', 4.4214756, 1, '2023-07-23 16:10:19.657988', NULL),
(628, 5.5, 26, 4.548, NULL, NULL, 'Hydril LX', 5.630196, 1, 'API', 4.4214756, 1, '2023-07-23 16:10:19.666544', NULL),
(629, 5.5, 26, 4.548, NULL, NULL, 'Hydril 563', 6.1262832, 1, 'API', 4.4214756, 1, '2023-07-23 16:10:19.674822', NULL),
(630, 5.5, 26, 4.548, NULL, NULL, 'Valluorec VAM New', 6.0750996, 1, 'API', 4.4214756, 1, '2023-07-23 16:10:19.682337', NULL),
(631, 5.5, 26, 4.548, NULL, NULL, 'Valluorec VAM ACE', 6.2443992, 1, 'API', 4.4214756, 1, '2023-07-23 16:10:19.690361', NULL),
(632, 5.5, 26, 4.548, NULL, NULL, 'Valluorec VAM PRO', 6.0711624, 1, 'API', 4.4214756, 1, '2023-07-23 16:10:19.697981', NULL),
(633, 5.5, 26, 4.548, NULL, NULL, 'Valluorec VAM TOP', 6.2483364, 1, 'API', 4.4214756, 1, '2023-07-23 16:10:19.705034', NULL),
(634, 5.5, 26, 4.548, NULL, NULL, 'Valluorec FJL', 5.5002684, 1, 'API', 4.4214756, 1, '2023-07-23 16:10:19.712425', NULL),
(635, 5.5, 23, 4.67, NULL, NULL, 'BTC', 6.0514764, 1, 'API', 4.5435288, 1, '2023-07-23 16:10:19.718468', NULL),
(636, 5.5, 23, 4.67, NULL, NULL, 'BTC Special', 5.8743024, 1, 'API', 4.5435288, 1, '2023-07-23 16:10:19.725638', NULL),
(637, 5.5, 23, 4.67, NULL, NULL, 'LTC', 6.0514764, 1, 'API', 4.5435288, 1, '2023-07-23 16:10:19.733591', NULL),
(638, 5.5, 23, 4.67, NULL, NULL, 'Grant Prideco TCII', 6.1184088, 1, 'API', 4.5435288, 1, '2023-07-23 16:10:19.740485', NULL),
(639, 5.5, 23, 4.67, NULL, NULL, 'Grant Prideco STL', 5.5002684, 1, 'API', 4.5435288, 1, '2023-07-23 16:10:19.748582', NULL),
(640, 5.5, 23, 4.67, NULL, NULL, 'Hydril LX', 5.6183844, 1, 'API', 4.5435288, 1, '2023-07-23 16:10:19.756368', NULL),
(641, 5.5, 23, 4.67, NULL, NULL, 'Hydril 563', 6.0514764, 1, 'API', 4.5435288, 1, '2023-07-23 16:10:19.762585', NULL),
(642, 5.5, 23, 4.67, NULL, NULL, 'Hydril 521', 5.9372976, 1, 'API', 4.5435288, 1, '2023-07-23 16:10:19.769762', NULL),
(643, 5.5, 23, 4.67, NULL, NULL, 'Valluorec VAM New', 6.0750996, 1, 'API', 4.5435288, 1, '2023-07-23 16:10:19.776895', NULL),
(644, 5.5, 23, 4.67, NULL, NULL, 'Valluorec VAM ACE', 6.1499064, 1, 'API', 4.5435288, 1, '2023-07-23 16:10:19.784091', NULL),
(645, 5.5, 23, 4.67, NULL, NULL, 'Valluorec VAM PRO', 6.0711624, 1, 'API', 4.5435288, 1, '2023-07-23 16:10:19.791335', NULL),
(646, 5.5, 23, 4.67, NULL, NULL, 'Valluorec VAM TOP', 6.1577808, 1, 'API', 4.5435288, 1, '2023-07-23 16:10:19.799497', NULL),
(647, 5.5, 23, 4.67, NULL, NULL, 'Valluorec FJL', 5.5002684, 1, 'API', 4.5435288, 1, '2023-07-23 16:10:19.806454', NULL),
(648, 5.5, 20, 4.778, NULL, NULL, 'BTC', 6.0514764, 1, 'API', 4.6537704, 1, '2023-07-23 16:10:19.814009', NULL),
(649, 5.5, 20, 4.778, NULL, NULL, 'BTC Special', 5.8743024, 1, 'API', 4.6537704, 1, '2023-07-23 16:10:19.822024', NULL),
(650, 5.5, 20, 4.778, NULL, NULL, 'LTC', 6.0514764, 1, 'API', 4.6537704, 1, '2023-07-23 16:10:19.830593', NULL),
(651, 5.5, 20, 4.778, NULL, NULL, 'Grant Prideco TCII', 6.0357276, 1, 'API', 4.6537704, 1, '2023-07-23 16:10:19.839195', NULL),
(652, 5.5, 20, 4.778, NULL, NULL, 'Grant Prideco STL', 5.5002684, 1, 'API', 4.6537704, 1, '2023-07-23 16:10:19.879671', NULL),
(653, 5.5, 20, 4.778, NULL, NULL, 'Hydril LX', 5.6065728, 1, 'API', 4.6537704, 1, '2023-07-23 16:10:19.885963', NULL),
(654, 5.5, 20, 4.778, NULL, NULL, 'Hydril 563', 6.0514764, 1, 'API', 4.6537704, 1, '2023-07-23 16:10:19.893642', NULL),
(655, 5.5, 20, 4.778, NULL, NULL, 'Hydril 511', 5.5002684, 1, 'API', 4.6537704, 1, '2023-07-23 16:10:19.901124', NULL),
(656, 5.5, 20, 4.778, NULL, NULL, 'Hydril 521', 5.8506792, 1, 'API', 4.6537704, 1, '2023-07-23 16:10:19.908677', NULL),
(657, 5.5, 20, 4.778, NULL, NULL, 'Valluorec VAM New', 6.0750996, 1, 'API', 4.6537704, 1, '2023-07-23 16:10:19.916131', NULL),
(658, 5.5, 20, 4.778, NULL, NULL, 'Valluorec VAM ACE', 6.1499064, 1, 'API', 4.6537704, 1, '2023-07-23 16:10:19.922447', NULL),
(659, 5.5, 20, 4.778, NULL, NULL, 'Valluorec VAM PRO', 6.0711624, 1, 'API', 4.6537704, 1, '2023-07-23 16:10:19.949360', NULL),
(660, 5.5, 20, 4.778, NULL, NULL, 'Valluorec VAM TOP', 6.0711624, 1, 'API', 4.6537704, 1, '2023-07-23 16:10:19.957081', NULL),
(661, 5.5, 20, 4.778, NULL, NULL, 'Valluorec FJL', 5.5002684, 1, 'API', 4.6537704, 1, '2023-07-23 16:10:19.964595', NULL),
(662, 5.5, 17, 4.892, NULL, NULL, 'BTC', 6.0514764, 1, 'API', 4.7679492, 1, '2023-07-23 16:10:19.971587', NULL),
(663, 5.5, 17, 4.892, NULL, NULL, 'BTC Special', 5.8743024, 1, 'API', 4.7679492, 1, '2023-07-23 16:10:19.980147', NULL),
(664, 5.5, 17, 4.892, NULL, NULL, 'STC', 6.0514764, 1, 'API', 4.7679492, 1, '2023-07-23 16:10:19.988376', NULL),
(665, 5.5, 17, 4.892, NULL, NULL, 'LTC', 6.0514764, 1, 'API', 4.7679492, 1, '2023-07-23 16:10:20.000120', NULL),
(666, 5.5, 17, 4.892, NULL, NULL, 'Grant Prideco TCII', 5.945172, 1, 'API', 4.7679492, 1, '2023-07-23 16:10:20.007776', NULL),
(667, 5.5, 17, 4.892, NULL, NULL, 'Grant Prideco STL', 5.5002684, 1, 'API', 4.7679492, 1, '2023-07-23 16:10:20.015802', NULL),
(668, 5.5, 17, 4.892, NULL, NULL, 'Hydril LX', 5.5986984, 1, 'API', 4.7679492, 1, '2023-07-23 16:10:20.022998', NULL),
(669, 5.5, 17, 4.892, NULL, NULL, 'Hydril 563', 6.0514764, 1, 'API', 4.7679492, 1, '2023-07-23 16:10:20.040110', NULL),
(670, 5.5, 17, 4.892, NULL, NULL, 'Hydril 511', 5.5002684, 1, 'API', 4.7679492, 1, '2023-07-23 16:10:20.048152', NULL),
(671, 5.5, 17, 4.892, NULL, NULL, 'Hydril 521', 5.7601236, 1, 'API', 4.7679492, 1, '2023-07-23 16:10:20.057026', NULL),
(672, 5.5, 17, 4.892, NULL, NULL, 'Valluorec VAM New', 6.0750996, 1, 'API', 4.7679492, 1, '2023-07-23 16:10:20.065847', NULL),
(673, 5.5, 17, 4.892, NULL, NULL, 'Valluorec VAM ACE', 6.0514764, 1, 'API', 4.7679492, 1, '2023-07-23 16:10:20.074046', NULL),
(674, 5.5, 17, 4.892, NULL, NULL, 'Valluorec VAM PRO', 6.0711624, 1, 'API', 4.7679492, 1, '2023-07-23 16:10:20.081568', NULL),
(675, 5.5, 17, 4.892, NULL, NULL, 'Valluorec VAM TOP', 5.9766696, 1, 'API', 4.7679492, 1, '2023-07-23 16:10:20.095147', NULL),
(676, 5.5, 17, 4.892, NULL, NULL, 'Valluorec FJL', 5.5002684, 1, 'API', 4.7679492, 1, '2023-07-23 16:10:20.102001', NULL),
(677, 5.5, 15.5, 4.95, NULL, NULL, 'BTC', 6.0514764, 1, 'API', 4.8270072, 1, '2023-07-23 16:10:20.135107', NULL),
(678, 5.5, 15.5, 4.95, NULL, NULL, 'BTC Special', 5.8743024, 1, 'API', 4.8270072, 1, '2023-07-23 16:10:20.143492', NULL),
(679, 5.5, 15.5, 4.95, NULL, NULL, 'STC', 6.0514764, 1, 'API', 4.8270072, 1, '2023-07-23 16:10:20.152904', NULL),
(680, 5.5, 15.5, 4.95, NULL, NULL, 'LTC', 6.0514764, 1, 'API', 4.8270072, 1, '2023-07-23 16:10:20.162751', NULL),
(681, 5.5, 15.5, 4.95, NULL, NULL, 'Grant Prideco TCII', 5.8979256, 1, 'API', 4.8270072, 1, '2023-07-23 16:10:20.171426', NULL),
(682, 5.5, 15.5, 4.95, NULL, NULL, 'Grant Prideco STL', 5.5002684, 1, 'API', 4.8270072, 1, '2023-07-23 16:10:20.179223', NULL),
(683, 5.5, 15.5, 4.95, NULL, NULL, 'Hydril 563', 6.0514764, 1, 'API', 4.8270072, 1, '2023-07-23 16:10:20.188057', NULL),
(684, 5.5, 15.5, 4.95, NULL, NULL, 'Hydril 511', 5.5002684, 1, 'API', 4.8270072, 1, '2023-07-23 16:10:20.196331', NULL),
(685, 5.5, 15.5, 4.95, NULL, NULL, 'Hydril 521', 5.7128772, 1, 'API', 4.8270072, 1, '2023-07-23 16:10:20.203414', NULL),
(686, 5.5, 15.5, 4.95, NULL, NULL, 'Valluorec VAM New', 6.0750996, 1, 'API', 4.8270072, 1, '2023-07-23 16:10:20.210946', NULL),
(687, 5.5, 15.5, 4.95, NULL, NULL, 'Valluorec VAM ACE', 6.0514764, 1, 'API', 4.8270072, 1, '2023-07-23 16:10:20.217839', NULL),
(688, 5.5, 15.5, 4.95, NULL, NULL, 'Valluorec VAM PRO', 6.0711624, 1, 'API', 4.8270072, 1, '2023-07-23 16:10:20.225458', NULL),
(689, 5.5, 15.5, 4.95, NULL, NULL, 'Valluorec VAM TOP', 5.9294232, 1, 'API', 4.8270072, 1, '2023-07-23 16:10:20.247275', NULL),
(690, 5.5, 15.5, 4.95, NULL, NULL, 'Valluorec FJL', 5.5002684, 1, 'API', 4.8270072, 1, '2023-07-23 16:10:20.254741', NULL),
(691, 5.5, 14, 5.012, NULL, NULL, 'BTC', 6.0514764, 1, 'API', 4.8860652, 1, '2023-07-23 16:10:20.261514', NULL),
(692, 5.5, 14, 5.012, NULL, NULL, 'BTC Special', 5.8743024, 1, 'API', 4.8860652, 1, '2023-07-23 16:10:20.270498', NULL),
(693, 5.5, 14, 5.012, NULL, NULL, 'STC', 6.0514764, 1, 'API', 4.8860652, 1, '2023-07-23 16:10:20.279954', NULL),
(694, 5.5, 14, 5.012, NULL, NULL, 'Grant Prideco STL', 5.5002684, 1, 'API', 4.8860652, 1, '2023-07-23 16:10:20.287714', NULL),
(695, 5.5, 14, 5.012, NULL, NULL, 'Hydril 563', 6.0514764, 1, 'API', 4.8860652, 1, '2023-07-23 16:10:20.294783', NULL),
(696, 5.5, 14, 5.012, NULL, NULL, 'Hydril 521', 5.6616936, 1, 'API', 4.8860652, 1, '2023-07-23 16:10:20.313463', NULL),
(697, 5.5, 14, 5.012, NULL, NULL, 'Valluorec VAM New', 6.0750996, 1, 'API', 4.8860652, 1, '2023-07-23 16:10:20.322085', NULL),
(698, 5.5, 14, 5.012, NULL, NULL, 'Valluorec VAM PRO', 6.0711624, 1, 'API', 4.8860652, 1, '2023-07-23 16:10:20.330058', NULL),
(699, 5, 24.1, 4, NULL, NULL, 'BTC', 5.5632636, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:20.349041', NULL),
(700, 5, 24.1, 4, NULL, NULL, 'BTC Special', 5.374278, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:20.356725', NULL),
(701, 5, 24.1, 4, NULL, NULL, 'LTC', 5.5632636, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:20.366070', NULL),
(702, 5, 24.1, 4, NULL, NULL, 'Grant Priedco TCII', 5.7365004, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:20.375656', NULL),
(703, 5, 24.1, 4, NULL, NULL, 'Grant Priedco STL', 5.000244, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:20.383528', NULL),
(704, 5, 24.1, 4, NULL, NULL, 'Hydril LX', 5.1341088, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:20.391181', NULL),
(705, 5, 24.1, 4, NULL, NULL, 'Hydril 563', 5.7522492, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:20.403193', NULL),
(706, 5, 24.1, 4, NULL, NULL, 'Valluorec VAM New', 5.5868868, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:20.412270', NULL),
(707, 5, 24.1, 4, NULL, NULL, 'Valluorec VAM ACE', 5.80737, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:20.422819', NULL),
(708, 5, 24.1, 4, NULL, NULL, 'Valluorec VAM PRO', 5.5829496, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:20.432402', NULL),
(709, 5, 24.1, 4, NULL, NULL, 'Valluorec FJL', 5.000244, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:20.439713', NULL),
(710, 5, 23.2, 4.044, NULL, NULL, 'BTC', 5.5632636, 1, 'API', 3.917514, 1, '2023-07-23 16:10:20.447113', NULL),
(711, 5, 23.2, 4.044, NULL, NULL, 'BTC Special', 5.374278, 1, 'API', 3.917514, 1, '2023-07-23 16:10:20.455383', NULL),
(712, 5, 23.2, 4.044, NULL, NULL, 'Grant Priedco TCII', 5.7050028, 1, 'API', 3.917514, 1, '2023-07-23 16:10:20.462026', NULL),
(713, 5, 23.2, 4.044, NULL, NULL, 'Grant Priedco STL', 5.000244, 1, 'API', 3.917514, 1, '2023-07-23 16:10:20.469999', NULL),
(714, 5, 23.2, 4.044, NULL, NULL, 'Hydril LX', 5.1301716, 1, 'API', 3.917514, 1, '2023-07-23 16:10:20.477964', NULL),
(715, 5, 23.2, 4.044, NULL, NULL, 'Hydril 563', 5.7522492, 1, 'API', 3.917514, 1, '2023-07-23 16:10:20.486013', NULL),
(716, 5, 23.2, 4.044, NULL, NULL, 'Valluorec VAM New', 5.5868868, 1, 'API', 3.917514, 1, '2023-07-23 16:10:20.494999', NULL),
(717, 5, 23.2, 4.044, NULL, NULL, 'Valluorec VAM ACE', 5.7522492, 1, 'API', 3.917514, 1, '2023-07-23 16:10:20.502682', NULL),
(718, 5, 23.2, 4.044, NULL, NULL, 'Valluorec VAM PRO', 5.5829496, 1, 'API', 3.917514, 1, '2023-07-23 16:10:20.509732', NULL),
(719, 5, 23.2, 4.044, NULL, NULL, 'Valluorec VAM TOP', 5.7522492, 1, 'API', 3.917514, 1, '2023-07-23 16:10:20.519268', NULL),
(720, 5, 23.2, 4.044, NULL, NULL, 'Valluorec FJL', 5.000244, 1, 'API', 3.917514, 1, '2023-07-23 16:10:20.527089', NULL),
(721, 5, 21.4, 4.126, NULL, NULL, 'BTC', 5.5632636, 1, 'API', 4.0001952, 1, '2023-07-23 16:10:20.534415', NULL),
(722, 5, 21.4, 4.126, NULL, NULL, 'BTC Special', 5.374278, 1, 'API', 4.0001952, 1, '2023-07-23 16:10:20.542525', NULL),
(723, 5, 21.4, 4.126, NULL, NULL, 'LTC', 5.5632636, 1, 'API', 4.0001952, 1, '2023-07-23 16:10:20.551713', NULL),
(724, 5, 21.4, 4.126, NULL, NULL, 'Grant Priedco TCII', 5.6459448, 1, 'API', 4.0001952, 1, '2023-07-23 16:10:20.559432', NULL),
(725, 5, 21.4, 4.126, NULL, NULL, 'Hydril LX', 5.11836, 1, 'API', 4.0001952, 1, '2023-07-23 16:10:20.566257', NULL),
(726, 5, 21.4, 4.126, NULL, NULL, 'Hydril 563', 5.7522492, 1, 'API', 4.0001952, 1, '2023-07-23 16:10:20.573970', NULL),
(727, 5, 21.4, 4.126, NULL, NULL, 'Valluorec VAM New', 5.5868868, 1, 'API', 4.0001952, 1, '2023-07-23 16:10:20.581393', NULL),
(728, 5, 21.4, 4.126, NULL, NULL, 'Valluorec VAM ACE', 5.7522492, 1, 'API', 4.0001952, 1, '2023-07-23 16:10:20.589047', NULL),
(729, 5, 21.4, 4.126, NULL, NULL, 'Valluorec VAM PRO', 5.5829496, 1, 'API', 4.0001952, 1, '2023-07-23 16:10:20.596866', NULL),
(730, 5, 21.4, 4.126, NULL, NULL, 'Valluorec VAM TOP', 5.6931912, 1, 'API', 4.0001952, 1, '2023-07-23 16:10:20.604746', NULL),
(731, 5, 21.4, 4.126, NULL, NULL, 'Valluorec FJL', 5.000244, 1, 'API', 4.0001952, 1, '2023-07-23 16:10:20.612439', NULL),
(732, 5, 18, 4.276, NULL, NULL, 'BTC', 5.5632636, 1, 'API', 4.1498088, 1, '2023-07-23 16:10:20.619403', NULL),
(733, 5, 18, 4.276, NULL, NULL, 'BTC Special', 5.374278, 1, 'API', 4.1498088, 1, '2023-07-23 16:10:20.627609', NULL),
(734, 5, 18, 4.276, NULL, NULL, 'LTC', 5.5632636, 1, 'API', 4.1498088, 1, '2023-07-23 16:10:20.634099', NULL),
(735, 5, 18, 4.276, NULL, NULL, 'Grant Priedco TCII', 5.531766, 1, 'API', 4.1498088, 1, '2023-07-23 16:10:20.642218', NULL),
(736, 5, 18, 4.276, NULL, NULL, 'Grant Priedco STL', 5.000244, 1, 'API', 4.1498088, 1, '2023-07-23 16:10:20.650345', NULL),
(737, 5, 18, 4.276, NULL, NULL, 'Hydril LX', 5.1065484, 1, 'API', 4.1498088, 1, '2023-07-23 16:10:20.658652', NULL),
(738, 5, 18, 4.276, NULL, NULL, 'Hydril 563', 5.5632636, 1, 'API', 4.1498088, 1, '2023-07-23 16:10:20.666797', NULL),
(739, 5, 18, 4.276, NULL, NULL, 'Hydril 511', 5.000244, 1, 'API', 4.1498088, 1, '2023-07-23 16:10:20.675187', NULL),
(740, 5, 18, 4.276, NULL, NULL, 'Hydril 521', 5.3585292, 1, 'API', 4.1498088, 1, '2023-07-23 16:10:20.684205', NULL),
(741, 5, 18, 4.276, NULL, NULL, 'Valluorec VAM New', 5.5868868, 1, 'API', 4.1498088, 1, '2023-07-23 16:10:20.690963', NULL),
(742, 5, 18, 4.276, NULL, NULL, 'Valluorec VAM ACE', 5.571138, 1, 'API', 4.1498088, 1, '2023-07-23 16:10:20.700268', NULL),
(743, 5, 18, 4.276, NULL, NULL, 'Valluorec VAM PRO', 5.5829496, 1, 'API', 4.1498088, 1, '2023-07-23 16:10:20.708321', NULL),
(744, 5, 18, 4.276, NULL, NULL, 'Valluorec VAM TOP', 5.5790124, 1, 'API', 4.1498088, 1, '2023-07-23 16:10:20.715561', NULL),
(745, 5, 18, 4.276, NULL, NULL, 'Valluorec FJL', 5.000244, 1, 'API', 4.1498088, 1, '2023-07-23 16:10:20.722970', NULL),
(746, 5, 15, 4.408, NULL, NULL, 'BTC', 5.5632636, 1, 'API', 4.2836736, 1, '2023-07-23 16:10:20.729550', NULL),
(747, 5, 15, 4.408, NULL, NULL, 'BTC Special', 5.374278, 1, 'API', 4.2836736, 1, '2023-07-23 16:10:20.737159', NULL),
(748, 5, 15, 4.408, NULL, NULL, 'STC', 5.5632636, 1, 'API', 4.2836736, 1, '2023-07-23 16:10:20.745748', NULL),
(749, 5, 15, 4.408, NULL, NULL, 'LTC', 5.5632636, 1, 'API', 4.2836736, 1, '2023-07-23 16:10:20.753546', NULL),
(750, 5, 15, 4.408, NULL, NULL, 'Grant Priedco TCII', 5.4293988, 1, 'API', 4.2836736, 1, '2023-07-23 16:10:20.761358', NULL),
(751, 5, 15, 4.408, NULL, NULL, 'Grant Priedco STL', 5.000244, 1, 'API', 4.2836736, 1, '2023-07-23 16:10:20.768618', NULL),
(752, 5, 15, 4.408, NULL, NULL, 'Hydril LX', 5.0907996, 1, 'API', 4.2836736, 1, '2023-07-23 16:10:20.774770', NULL),
(753, 5, 15, 4.408, NULL, NULL, 'Hydril 563', 5.5632636, 1, 'API', 4.2836736, 1, '2023-07-23 16:10:20.782151', NULL),
(754, 5, 15, 4.408, NULL, NULL, 'Hydril 511', 5.000244, 1, 'API', 4.2836736, 1, '2023-07-23 16:10:20.789802', NULL),
(755, 5, 15, 4.408, NULL, NULL, 'Hydril 521', 5.256162, 1, 'API', 4.2836736, 1, '2023-07-23 16:10:20.796978', NULL),
(756, 5, 15, 4.408, NULL, NULL, 'Valluorec VAM New', 5.5868868, 1, 'API', 4.2836736, 1, '2023-07-23 16:10:20.804799', NULL),
(757, 5, 15, 4.408, NULL, NULL, 'Valluorec VAM ACE', 5.5632636, 1, 'API', 4.2836736, 1, '2023-07-23 16:10:20.812303', NULL),
(758, 5, 15, 4.408, NULL, NULL, 'Valluorec VAM PRO', 5.5829496, 1, 'API', 4.2836736, 1, '2023-07-23 16:10:20.819268', NULL),
(759, 5, 15, 4.408, NULL, NULL, 'Valluorec VAM TOP', 5.4687708, 1, 'API', 4.2836736, 1, '2023-07-23 16:10:20.829859', NULL),
(760, 5, 15, 4.408, NULL, NULL, 'Valluorec FJL', 5.000244, 1, 'API', 4.2836736, 1, '2023-07-23 16:10:20.840076', NULL),
(761, 5, 13, 4.494, NULL, NULL, 'BTC', 5.5632636, 1, 'API', 4.370292, 1, '2023-07-23 16:10:20.847277', NULL),
(762, 5, 13, 4.494, NULL, NULL, 'BTC Special', 5.374278, 1, 'API', 4.370292, 1, '2023-07-23 16:10:20.855291', NULL),
(763, 5, 13, 4.494, NULL, NULL, 'STC', 5.5632636, 1, 'API', 4.370292, 1, '2023-07-23 16:10:20.861796', NULL),
(764, 5, 13, 4.494, NULL, NULL, 'LTC', 5.5632636, 1, 'API', 4.370292, 1, '2023-07-23 16:10:20.869653', NULL),
(765, 5, 13, 4.494, NULL, NULL, 'Grant Piedco STL', 5.000244, 1, 'API', 4.370292, 1, '2023-07-23 16:10:20.879155', NULL),
(766, 5, 13, 4.494, NULL, NULL, 'Hydril 563', 5.5632636, 1, 'API', 4.370292, 1, '2023-07-23 16:10:20.887816', NULL),
(767, 5, 13, 4.494, NULL, NULL, 'Hydril 521', 5.1852924, 1, 'API', 4.370292, 1, '2023-07-23 16:10:20.895105', NULL),
(768, 5, 13, 4.494, NULL, NULL, 'Valluorec VAM New', 5.5868868, 1, 'API', 4.370292, 1, '2023-07-23 16:10:20.915208', NULL),
(769, 5, 13, 4.494, NULL, NULL, 'Valluorec VAM ACE', 5.5632636, 1, 'API', 4.370292, 1, '2023-07-23 16:10:20.923618', NULL),
(770, 5, 13, 4.494, NULL, NULL, 'Valluorec VAM PRO', 5.5829496, 1, 'API', 4.370292, 1, '2023-07-23 16:10:20.930804', NULL),
(771, 5, 13, 4.494, NULL, NULL, 'Valluorec FJL', 5.000244, 1, 'API', 4.370292, 1, '2023-07-23 16:10:20.939905', NULL),
(772, 4.5, 15.1, 3.826, NULL, NULL, 'BTC', 5.000244, 1, 'API', 3.700968, 1, '2023-07-23 16:10:20.949043', NULL),
(773, 4.5, 15.1, 3.826, NULL, NULL, 'BTC Special', 4.8742536, 1, 'API', 3.700968, 1, '2023-07-23 16:10:20.957594', NULL),
(774, 4.5, 15.1, 3.826, NULL, NULL, 'LTC', 5.000244, 1, 'API', 3.700968, 1, '2023-07-23 16:10:20.965636', NULL),
(775, 4.5, 15.1, 3.826, NULL, NULL, 'Grant Piedco TCII', 5.0356788, 1, 'API', 3.700968, 1, '2023-07-23 16:10:20.973696', NULL),
(776, 4.5, 15.1, 3.826, NULL, NULL, 'Grant Piedco STL', 4.5002196, 1, 'API', 3.700968, 1, '2023-07-23 16:10:20.983301', NULL),
(777, 4.5, 15.1, 3.826, NULL, NULL, 'Hydril LX', 4.5986496, 1, 'API', 3.700968, 1, '2023-07-23 16:10:20.993333', NULL),
(778, 4.5, 15.1, 3.826, NULL, NULL, 'Hydril 563', 5.2010412, 1, 'API', 3.700968, 1, '2023-07-23 16:10:21.002440', NULL),
(779, 4.5, 15.1, 3.826, NULL, NULL, 'Hydril 511', 4.5002196, 1, 'API', 3.700968, 1, '2023-07-23 16:10:21.011842', NULL),
(780, 4.5, 15.1, 3.826, NULL, NULL, 'Valluorec VAM New', 5.0120556, 1, 'API', 3.700968, 1, '2023-07-23 16:10:21.020297', NULL),
(781, 4.5, 15.1, 3.826, NULL, NULL, 'Valluorec VAM ACE', 5.0041812, 1, 'API', 3.700968, 1, '2023-07-23 16:10:21.026849', NULL),
(782, 4.5, 15.1, 3.826, NULL, NULL, 'Valluorec VAM PRO', 4.9333116, 1, 'API', 3.700968, 1, '2023-07-23 16:10:21.037559', NULL),
(783, 4.5, 15.1, 3.826, NULL, NULL, 'Valluorec FJL', 4.5002196, 1, 'API', 3.700968, 1, '2023-07-23 16:10:21.045101', NULL),
(784, 4.5, 13.5, 3.92, NULL, NULL, 'BTC', 5.000244, 1, 'API', 3.7954608, 1, '2023-07-23 16:10:21.054715', NULL),
(785, 4.5, 13.5, 3.92, NULL, NULL, 'BTC Special', 4.8742536, 1, 'API', 3.7954608, 1, '2023-07-23 16:10:21.063806', NULL),
(786, 4.5, 13.5, 3.92, NULL, NULL, 'LTC', 5.000244, 1, 'API', 3.7954608, 1, '2023-07-23 16:10:21.073506', NULL),
(787, 4.5, 13.5, 3.92, NULL, NULL, 'Grant Piedco TCII', 4.960872, 1, 'API', 3.7954608, 1, '2023-07-23 16:10:21.082000', NULL),
(788, 4.5, 13.5, 3.92, NULL, NULL, 'Grant Piedco STL', 4.5002196, 1, 'API', 3.7954608, 1, '2023-07-23 16:10:21.090383', NULL),
(789, 4.5, 13.5, 3.92, NULL, NULL, 'Hydril LX', 4.586838, 1, 'API', 3.7954608, 1, '2023-07-23 16:10:21.099824', NULL),
(790, 4.5, 13.5, 3.92, NULL, NULL, 'Hydril 563', 5.2010412, 1, 'API', 3.7954608, 1, '2023-07-23 16:10:21.108640', NULL),
(791, 4.5, 13.5, 3.92, NULL, NULL, 'Hydril 511', 4.5002196, 1, 'API', 3.7954608, 1, '2023-07-23 16:10:21.139548', NULL),
(792, 4.5, 13.5, 3.92, NULL, NULL, 'Hydril 521', 4.7600748, 1, 'API', 3.7954608, 1, '2023-07-23 16:10:21.147022', NULL),
(793, 4.5, 13.5, 3.92, NULL, NULL, 'Valluorec VAM New', 4.960872, 1, 'API', 3.7954608, 1, '2023-07-23 16:10:21.155885', NULL),
(794, 4.5, 13.5, 3.92, NULL, NULL, 'Valluorec VAM ACE', 4.960872, 1, 'API', 3.7954608, 1, '2023-07-23 16:10:21.163465', NULL),
(795, 4.5, 13.5, 3.92, NULL, NULL, 'Valluorec VAM PRO', 4.9451232, 1, 'API', 3.7954608, 1, '2023-07-23 16:10:21.171551', NULL),
(796, 4.5, 13.5, 3.92, NULL, NULL, 'Valluorec FJL', 4.5002196, 1, 'API', 3.7954608, 1, '2023-07-23 16:10:21.182348', NULL),
(797, 4.5, 11.6, 4, NULL, NULL, 'BTC', 5.000244, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:21.191215', NULL),
(798, 4.5, 11.6, 4, NULL, NULL, 'BTC Special', 4.8742536, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:21.199608', NULL),
(799, 4.5, 11.6, 4, NULL, NULL, 'STC', 5.000244, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:21.207419', NULL),
(800, 4.5, 11.6, 4, NULL, NULL, 'LTC', 5.000244, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:21.216216', NULL),
(801, 4.5, 11.6, 4, NULL, NULL, 'Grant Piedco TCII', 4.8978768, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:21.222738', NULL),
(802, 4.5, 11.6, 4, NULL, NULL, 'Grant Piedco STL', 4.5002196, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:21.231510', NULL),
(803, 4.5, 11.6, 4, NULL, NULL, 'Hydril 563', 5.2010412, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:21.239466', NULL),
(804, 4.5, 11.6, 4, NULL, NULL, 'Hydril 511', 4.5002196, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:21.245892', NULL),
(805, 4.5, 11.6, 4, NULL, NULL, 'Hydril 521', 4.6970796, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:21.253213', NULL),
(806, 4.5, 11.6, 4, NULL, NULL, 'Valluorec VAM New', 4.862442, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:21.260061', NULL),
(807, 4.5, 11.6, 4, NULL, NULL, 'Valluorec VAM ACE', 4.8742536, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:21.267338', NULL),
(808, 4.5, 11.6, 4, NULL, NULL, 'Valluorec VAM PRO', 4.882128, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:21.286812', NULL),
(809, 4.5, 11.6, 4, NULL, NULL, 'Valluorec FJL', 4.5002196, 1, 'API', 3.8742048, 1, '2023-07-23 16:10:21.295675', NULL),
(810, 4.5, 10.5, 4.052, NULL, NULL, 'BTC', 5.000244, 1, 'API', 3.9253884, 1, '2023-07-23 16:10:21.302955', NULL),
(811, 4.5, 10.5, 4.052, NULL, NULL, 'BTC Special', 4.8742536, 1, 'API', 3.9253884, 1, '2023-07-23 16:10:21.309678', NULL),
(812, 4.5, 10.5, 4.052, NULL, NULL, 'STC', 5.000244, 1, 'API', 3.9253884, 1, '2023-07-23 16:10:21.317533', NULL),
(813, 4.5, 10.5, 4.052, NULL, NULL, 'Grant Piedco TCII', 4.8545676, 1, 'API', 3.9253884, 1, '2023-07-23 16:10:21.326794', NULL),
(814, 4.5, 10.5, 4.052, NULL, NULL, 'Grant Piedco STL', 4.5002196, 1, 'API', 3.9253884, 1, '2023-07-23 16:10:21.334664', NULL),
(815, 4.5, 10.5, 4.052, NULL, NULL, 'Hydril 511', 4.5002196, 1, 'API', 3.9253884, 1, '2023-07-23 16:10:21.341960', NULL),
(816, 4.5, 10.5, 4.052, NULL, NULL, 'Hydril 521', 4.6498332, 1, 'API', 3.9253884, 1, '2023-07-23 16:10:21.350242', NULL),
(817, 4.5, 10.5, 4.052, NULL, NULL, 'Valluorec VAM New', 4.862442, 1, 'API', 3.9253884, 1, '2023-07-23 16:10:21.358556', NULL),
(818, 4.5, 10.5, 4.052, NULL, NULL, 'Valluorec VAM ACE', 4.862442, 1, 'API', 3.9253884, 1, '2023-07-23 16:10:21.365516', NULL),
(819, 4.5, 10.5, 4.052, NULL, NULL, 'Valluorec VAM PRO', 4.8388188, 1, 'API', 3.9253884, 1, '2023-07-23 16:10:21.372865', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `wellphases_casinggrade`
--

CREATE TABLE `wellphases_casinggrade` (
  `id` int NOT NULL,
  `status` int NOT NULL,
  `is_superadmin` int NOT NULL,
  `grade_name` varchar(250) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `company_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `wellphases_casingrange`
--

CREATE TABLE `wellphases_casingrange` (
  `id` int NOT NULL,
  `status` int NOT NULL,
  `is_superadmin` int NOT NULL,
  `range_name` varchar(250) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `company_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `wellphases_casingtypes`
--

CREATE TABLE `wellphases_casingtypes` (
  `id` int NOT NULL,
  `name` varchar(250) DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `wellphases_casingtypes`
--

INSERT INTO `wellphases_casingtypes` (`id`, `name`, `status`, `created`) VALUES
(1, 'Conductor Casing ', 1, NULL),
(2, 'Drive Pipe', 1, NULL),
(3, 'Surface Casing 1', 1, NULL),
(4, 'Surface Casing 2', 1, NULL),
(5, 'Intermediate Casing 1', 1, NULL),
(6, 'Intermediate Casing 2', 1, NULL),
(7, 'Intermediate Liner 1', 1, NULL),
(8, 'Intermediate Liner 2', 1, NULL),
(9, 'Production Casing 1', 1, NULL),
(10, 'Production Casing 2', 1, NULL),
(11, 'Production Liner 1', 1, NULL),
(12, 'Production Liner 2 ', 1, NULL),
(13, 'Open Hole ', 1, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `wellphases_wellphases`
--

CREATE TABLE `wellphases_wellphases` (
  `id` int NOT NULL,
  `phase_name` varchar(250) DEFAULT NULL,
  `hole_size` double DEFAULT NULL,
  `casing_size` double DEFAULT NULL,
  `measured_depth` double DEFAULT NULL,
  `true_vertical_depth` double DEFAULT NULL,
  `lineartop` double DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) DEFAULT NULL,
  `nominal_od` double DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `grade` varchar(250) DEFAULT NULL,
  `connection_type` varchar(250) DEFAULT NULL,
  `casing_range` int DEFAULT NULL,
  `drift_id` double DEFAULT NULL,
  `date` date DEFAULT NULL,
  `timestamp` int DEFAULT NULL,
  `time` time(6) DEFAULT NULL,
  `casing_type_id` int DEFAULT NULL,
  `company_id` int DEFAULT NULL,
  `well_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `wellphases_wellphases`
--

INSERT INTO `wellphases_wellphases` (`id`, `phase_name`, `hole_size`, `casing_size`, `measured_depth`, `true_vertical_depth`, `lineartop`, `status`, `created`, `nominal_od`, `weight`, `grade`, `connection_type`, `casing_range`, `drift_id`, `date`, `timestamp`, `time`, `casing_type_id`, `company_id`, `well_id`) VALUES
(1, '17-1/2\" Phase', 17.5, 13.375, 400, 400, NULL, 1, '2023-07-11 10:42:36.408522', 13.375, 68, NULL, 'BTC', NULL, 12.415, NULL, NULL, NULL, 3, 2, 2),
(2, '12-1/4\" Phase', 12.25, 9.625, 968, 733.15, NULL, 1, '2023-07-11 10:42:36.735311', 9.625, 47, NULL, 'BTC', NULL, 8.681, NULL, NULL, NULL, 5, 2, 2),
(3, '8-1/2\" Phase', 8.5, 7, 2304, 1938.52, NULL, 1, '2023-07-11 10:42:36.840460', 7, 29, 'N 80', 'BTC', 34, 6.184, NULL, NULL, NULL, 9, 2, 2);

-- --------------------------------------------------------

--
-- Table structure for table `wells_coordinatesystems`
--

CREATE TABLE `wells_coordinatesystems` (
  `id` int NOT NULL,
  `name` varchar(60) NOT NULL,
  `status` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `wells_coordinatesystems`
--

INSERT INTO `wells_coordinatesystems` (`id`, `name`, `status`) VALUES
(1, 'WGS84', 1),
(2, 'NAD27', 1),
(3, 'WGS 66', 1),
(4, 'WGS 60', 1),
(5, 'NAD 27', 1),
(6, 'OSGB 36', 1),
(7, 'ETRS 89', 1),
(8, 'GDA 94', 1),
(9, 'JGD 2011', 1),
(10, 'Tokyo 97', 1),
(11, 'KGD 2002', 1),
(12, 'TWD 67', 1),
(13, 'TWD 97', 1),
(14, 'PZ-90.11', 1),
(15, 'GTRF', 1),
(16, 'CGS-2000', 1),
(17, 'ITRF-2014', 1),
(18, 'ITRF-2008', 1),
(19, 'ED 50', 1),
(20, 'Minna Nigeria East Belt', 1),
(21, 'Minna Nigeria West Belt', 1),
(22, 'Minna Nigeria Mid Belt', 1);

-- --------------------------------------------------------

--
-- Table structure for table `wells_projections`
--

CREATE TABLE `wells_projections` (
  `id` int NOT NULL,
  `name` varchar(60) NOT NULL,
  `status` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `wells_projections`
--

INSERT INTO `wells_projections` (`id`, `name`, `status`) VALUES
(1, 'Aitoff', 1),
(2, 'Albers Equal Area Conic', 1),
(3, 'Azimuthal Equdistant', 1),
(4, 'Behrmann Equal Area Cylindrical', 1),
(5, 'Bipolar Oblique Conformal Conic', 1),
(6, 'Bonne', 1),
(7, 'Cassini-Soldner', 1),
(8, 'Chamberlin Trimetric', 1),
(9, 'Craster Parabolic', 1),
(10, 'Cylindrical Equal Area', 1),
(11, 'Double Sterographic', 1),
(12, 'Eckert I', 1),
(13, 'Eckert II', 1),
(14, 'Eckert III', 1),
(15, 'Eckert IV', 1),
(16, 'Eckert V', 1),
(17, 'Eckert VI', 1),
(18, 'Equidistant Conic', 1),
(19, 'Equidistant Cylindrical', 1),
(20, 'Equirectangular', 1),
(21, 'Gall\'s Stereographic', 1),
(22, 'Gauss-Krüger', 1),
(23, 'Geocentric Coordinate System', 1),
(24, 'Geographic Coordinate System', 1),
(25, 'Gnomonic', 1),
(26, 'Great Britain National Grid', 1),
(27, 'Hammer-Aitoff', 1),
(28, 'Hotine Oblique Mercator', 1),
(29, 'Krovak', 1),
(30, 'Lambert Azimuthal Equal Area', 1),
(31, 'Lambert Conformal Conic', 1),
(32, 'Local Cartesian Projection', 1),
(33, 'Loximuthal', 1),
(34, 'McBryde-Thomas Flat-Polar Quartic', 1),
(35, 'Mercator', 1),
(36, 'Miller Cylindrical', 1),
(37, 'Mollweide', 1),
(38, 'New Zeland National Grid ', 1),
(39, 'Orthographic', 1),
(40, 'Perspective', 1),
(41, 'Plate Carrée', 1),
(42, 'Polar Stereographic', 1),
(43, 'Polyconic', 1),
(44, 'Quartic Authalic', 1),
(45, 'Rectified Skewed Orthomorphic', 1),
(46, 'Robinson', 1),
(47, 'Simple Conic', 1),
(48, 'Sinusoidal', 1),
(49, 'Space Oblique Mercator', 1),
(50, 'State Plane Coordinate System', 1),
(51, 'Stereographic', 1),
(52, 'Times', 1),
(53, 'Transverse Mercator', 1),
(54, 'Two-Point Equidistant', 1),
(55, 'Universal Polar Stereographic', 1),
(56, 'Universal Transverse Mercator', 1),
(57, 'Van Der Grinten I', 1),
(58, 'Vertical Near-Side Perspective', 1),
(59, 'Winkel I', 1),
(60, 'Winkel II', 1),
(61, 'Winkel Tripel', 1);

-- --------------------------------------------------------

--
-- Table structure for table `wells_wells`
--

CREATE TABLE `wells_wells` (
  `id` bigint NOT NULL,
  `number_of_well_pads` double DEFAULT NULL,
  `ground_elevation` double DEFAULT NULL,
  `air_gap` double DEFAULT NULL,
  `slot_longtitude` varchar(60) DEFAULT NULL,
  `name` varchar(60) NOT NULL,
  `environment` varchar(30) DEFAULT NULL,
  `longtitude` varchar(60) DEFAULT NULL,
  `zone` varchar(30) DEFAULT NULL,
  `rkb_wellhead` double DEFAULT NULL,
  `well_type` varchar(30) DEFAULT NULL,
  `number_of_well_slots_in_pad` double DEFAULT NULL,
  `latitude` varchar(60) DEFAULT NULL,
  `slot_easting` double DEFAULT NULL,
  `water_depth` double DEFAULT NULL,
  `number_of_slots_in_platform` double DEFAULT NULL,
  `wellhead_to_datum` double DEFAULT NULL,
  `platform_name` varchar(30) DEFAULT NULL,
  `slot_no` double DEFAULT NULL,
  `slot_latitude` varchar(60) DEFAULT NULL,
  `datum` varchar(60) DEFAULT NULL,
  `pad_name` varchar(30) DEFAULT NULL,
  `northing` varchar(10) DEFAULT NULL,
  `rkb_datum` double DEFAULT NULL,
  `cluster_name` varchar(60) DEFAULT NULL,
  `well_slot_no_or_name` varchar(60) DEFAULT NULL,
  `environment_sub_type` varchar(60) DEFAULT NULL,
  `easting` varchar(10) DEFAULT NULL,
  `slot_northing` double DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `status` int NOT NULL,
  `block_id` int DEFAULT NULL,
  `company_id` int DEFAULT NULL,
  `coordinate_system_id` int DEFAULT NULL,
  `created_by_id` int DEFAULT NULL,
  `field_id` int DEFAULT NULL,
  `plan_well_list_id` bigint DEFAULT NULL,
  `project_id` int DEFAULT NULL,
  `projection_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `wells_wells`
--

INSERT INTO `wells_wells` (`id`, `number_of_well_pads`, `ground_elevation`, `air_gap`, `slot_longtitude`, `name`, `environment`, `longtitude`, `zone`, `rkb_wellhead`, `well_type`, `number_of_well_slots_in_pad`, `latitude`, `slot_easting`, `water_depth`, `number_of_slots_in_platform`, `wellhead_to_datum`, `platform_name`, `slot_no`, `slot_latitude`, `datum`, `pad_name`, `northing`, `rkb_datum`, `cluster_name`, `well_slot_no_or_name`, `environment_sub_type`, `easting`, `slot_northing`, `created`, `status`, `block_id`, `company_id`, `coordinate_system_id`, `created_by_id`, `field_id`, `plan_well_list_id`, `project_id`, `projection_id`) VALUES
(1, NULL, 339.48, NULL, NULL, 'Poduri-3', 'Onshore', '26° 36\' 48\" W', 'S 70', NULL, 'PLAN', NULL, '46° 27\' 55\" S', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Ground Level', NULL, '51', 8.55, NULL, NULL, 'standalone', '4', NULL, '2023-06-27 18:17:20.300008', 1, 1, 1, 1, NULL, 1, NULL, 1, 56),
(2, NULL, NULL, NULL, NULL, 'Okoro 16', 'Offshore', '10° 10\' 10\" E', '31 N', NULL, 'PLAN', NULL, '10° 10\' 10\" N', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'MSL', NULL, '43.33', NULL, NULL, NULL, 'standalone', '12.12', NULL, '2023-06-29 14:32:17.139142', 1, 2, 2, 1, NULL, 2, NULL, 2, 56),
(3, NULL, NULL, NULL, NULL, 'Poduri-3', 'Onshore', '46° 27\' 55\" E', 'S 70', NULL, 'PLAN', NULL, '26° 36\' 48\" N', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Ground Level', NULL, NULL, NULL, NULL, NULL, 'standalone', NULL, NULL, '2023-07-29 12:14:16.387359', 1, 7, 14, 1, NULL, 7, NULL, 7, 56),
(4, NULL, NULL, NULL, NULL, 'Poduri 3', 'Onshore', '46° 27\' 55\" E', 'S 70', NULL, 'PLAN', NULL, '26° 36\' 48\" S', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Ground Level', NULL, NULL, NULL, NULL, NULL, 'standalone', NULL, NULL, '2023-08-01 14:52:12.540820', 1, 8, 18, 1, NULL, 8, NULL, 8, 56),
(5, NULL, 339.48, NULL, NULL, 'Poduri-3', 'Onshore', '26° 36\' 48\" E', '5.70', NULL, 'PLAN', NULL, '46° 27\' 55\" N', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Ground Level', NULL, '552.97', 8.55, NULL, NULL, 'standalone', '623.90', NULL, '2023-08-03 15:26:34.166922', 1, 9, 20, 1, NULL, 9, NULL, 9, 56),
(6, NULL, 339.48, NULL, NULL, 'Poduri - 3', 'Onshore', '26° 36\' 48\" E', 'S 70', NULL, 'PLAN', NULL, '46° 27\' 55\" N', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Ground Level', NULL, '552.97', 8.55, NULL, NULL, 'standalone', '623.90', NULL, '2023-08-03 15:26:35.327554', 1, 10, 2, 1, NULL, 10, NULL, 10, 56);

-- --------------------------------------------------------

--
-- Table structure for table `wells_wellusers`
--

CREATE TABLE `wells_wellusers` (
  `id` int NOT NULL,
  `created` datetime(6) NOT NULL,
  `status` int NOT NULL,
  `role_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `well_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `wells_wellusers`
--

INSERT INTO `wells_wellusers` (`id`, `created`, `status`, `role_id`, `user_id`, `well_id`) VALUES
(1, '2023-06-27 18:17:20.375876', 1, 3, NULL, 1),
(2, '2023-06-29 14:32:17.348109', 1, 3, NULL, 2),
(3, '2023-07-29 12:14:18.086840', 1, 3, NULL, 3),
(4, '2023-08-01 14:52:12.565016', 1, 3, NULL, 4),
(5, '2023-08-03 15:26:34.290679', 1, 3, NULL, 5),
(6, '2023-08-03 15:26:35.504000', 1, 3, NULL, 6);

-- --------------------------------------------------------

--
-- Table structure for table `welltrajectory_welltrajectory`
--

CREATE TABLE `welltrajectory_welltrajectory` (
  `id` int NOT NULL,
  `measured_depth` double DEFAULT NULL,
  `inclination` double DEFAULT NULL,
  `azimuth` double DEFAULT NULL,
  `true_vertical_depth` double DEFAULT NULL,
  `dls` double DEFAULT NULL,
  `delta_e` double DEFAULT NULL,
  `delta_n` double DEFAULT NULL,
  `east` double DEFAULT NULL,
  `north` double DEFAULT NULL,
  `easting` double DEFAULT NULL,
  `northing` double DEFAULT NULL,
  `vertical_section` double DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime(6) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `timestamp` int DEFAULT NULL,
  `time` time(6) DEFAULT NULL,
  `company_id` int DEFAULT NULL,
  `well_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `welltrajectory_welltrajectory`
--

INSERT INTO `welltrajectory_welltrajectory` (`id`, `measured_depth`, `inclination`, `azimuth`, `true_vertical_depth`, `dls`, `delta_e`, `delta_n`, `east`, `north`, `easting`, `northing`, `vertical_section`, `status`, `created`, `date`, `timestamp`, `time`, `company_id`, `well_id`) VALUES
(1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 51, 0, 1, '2023-06-28 12:28:59.498642', NULL, NULL, NULL, 1, 1),
(2, 400, 0, 0, 400, 0, NULL, NULL, 0, 0, 4, 51, 0, 1, '2023-06-28 12:28:59.545382', NULL, NULL, NULL, 1, 1),
(3, 430, 0, 0, 430, 0, NULL, NULL, 0, 0, 4, 51, 0, 1, '2023-06-28 12:28:59.554402', NULL, NULL, NULL, 1, 1),
(4, 736.68, 15.33, 326.64, 733.03, 1.5235, NULL, NULL, -22.43, 34.06, 4, 51, 40.78, 1, '2023-06-28 12:28:59.576822', NULL, NULL, NULL, 1, 1),
(5, 1136.68, 15.33, 326.4, 1118.8, 0.00483, NULL, NULL, -80.76, 122.27, 4, 51, 146.53, 1, '2023-06-28 12:28:59.583921', NULL, NULL, NULL, 1, 1),
(6, 1443.37, 0, 0, 1421.85, 1.52345, NULL, NULL, -103.33, 156.24, NULL, NULL, 187.32, 1, '2023-06-28 12:28:59.591980', NULL, NULL, NULL, 1, 1),
(7, 1960.04, 0, 0, 1938.52, 0, NULL, NULL, -103.33, 156.24, NULL, NULL, 187.32, 1, '2023-06-28 12:28:59.598330', NULL, NULL, NULL, 1, 1),
(8, 3287.54, 0, 0, 3266.02, 0, NULL, NULL, -103.33, 156.24, NULL, NULL, 187.32, 1, '2023-06-28 12:28:59.656533', NULL, NULL, NULL, 1, 1),
(9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12.12, 43.33, 0, 1, '2023-07-11 10:38:11.069914', NULL, NULL, NULL, 2, 2),
(10, 400, 0, 0, 400, 0, NULL, NULL, 0, 0, 12.12, 43.33, 0, 1, '2023-07-11 10:38:11.530701', NULL, NULL, NULL, 2, 2),
(11, 430, 0, 0, 430, 0, NULL, NULL, 0, 0, 12.12, 43.33, 0, 1, '2023-07-11 10:38:11.540770', NULL, NULL, NULL, 2, 2),
(12, 736.8, 15.33, 326.64, 733.15, 4.99674, NULL, NULL, -22.44, 34.08, 12.12, 43.33, 40.8, 1, '2023-07-11 10:38:11.550267', NULL, NULL, NULL, 2, 2),
(13, 1136.68, 15.33, 326.64, 1118.8, 0, NULL, NULL, -80.57, 122.38, NULL, NULL, 146.52, 1, '2023-07-11 10:38:11.567372', NULL, NULL, NULL, 2, 2),
(14, 1443.37, 0, 0, 1421.85, 4.99853, NULL, NULL, -103, 156.44, NULL, NULL, 187.3, 1, '2023-07-11 10:38:11.576460', NULL, NULL, NULL, 2, 2),
(15, 1960.04, 0, 0, 1938.52, 0, NULL, NULL, -103, 156.44, NULL, NULL, 187.3, 1, '2023-07-11 10:38:11.587967', NULL, NULL, NULL, 2, 2),
(16, 3287.54, 0, 0, 3266.02, 0, NULL, NULL, -103, 156.44, 12.12, 43.33, 187.3, 1, '2023-07-11 10:38:11.597213', NULL, NULL, NULL, 2, 2),
(17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 623.9, 552.97, 0, 1, '2023-08-03 15:49:47.736282', NULL, NULL, NULL, 2, 6),
(18, 400, 0, 0, 400, 0, NULL, NULL, 0, 0, 623.9, 552.97, 0, 1, '2023-08-03 15:49:47.792186', NULL, NULL, NULL, 2, 6),
(19, 430, 0, 0, 430, 0, NULL, NULL, 0, 0, 623.9, 552.97, 0, 1, '2023-08-03 15:49:47.869247', NULL, NULL, NULL, 2, 6),
(20, 736.68, 15.33, 326.64, 733.03, 1.5235, NULL, NULL, -22.43, 34.06, 623.9, 552.97, 40.78, 1, '2023-08-03 15:49:47.879338', NULL, NULL, NULL, 2, 6),
(21, 1136.68, 15.33, 326.64, 1118.8, 0, NULL, NULL, -80.58, 122.39, 623.9, 552.97, 146.53, 1, '2023-08-03 15:49:47.887653', NULL, NULL, NULL, 2, 6),
(22, 1443.37, 0, 0, 1421.85, 1.52345, NULL, NULL, -103.01, 156.45, NULL, NULL, 187.32, 1, '2023-08-03 15:49:48.016363', NULL, NULL, NULL, 2, 6),
(23, 1960.04, 0, 0, 1938.52, 0, NULL, NULL, -103.01, 156.45, NULL, NULL, 187.32, 1, '2023-08-03 15:49:48.040583', NULL, NULL, NULL, 2, 6),
(24, 3287.54, 0, 0, 3266.02, 0, NULL, NULL, -103.01, 156.45, NULL, NULL, 187.32, 1, '2023-08-03 15:49:48.081830', NULL, NULL, NULL, 2, 6),
(25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 623.9, 552.97, 0, 0, '2023-08-03 15:49:55.539941', NULL, NULL, NULL, 20, 5),
(26, 4, 0, 0, 4, 0, NULL, NULL, 0, 0, 623.9, 552.97, 0, 0, '2023-08-03 15:49:55.579721', NULL, NULL, NULL, 20, 5),
(27, 4.3, 0, 0, 4.3, 0, NULL, NULL, 0, 0, 623.9, 552.97, 0, 0, '2023-08-03 15:49:55.664503', NULL, NULL, NULL, 20, 5),
(28, 7.36, 15.33, 326.64, 7.32, 152.6888, NULL, NULL, -0.22, 0.34, 623.9, 552.97, 0.41, 0, '2023-08-03 15:49:55.675824', NULL, NULL, NULL, 20, 5),
(29, 113, 15.33, 326.64, 109.2, 0, NULL, NULL, -15.58, 23.67, 623.9, 552.97, 28.34, 0, '2023-08-03 15:49:55.731756', NULL, NULL, NULL, 20, 5),
(30, 196, 0, 0, 191.221, 5.62925, NULL, NULL, -21.65, 32.89, NULL, NULL, 39.37, 0, '2023-08-03 15:49:55.791551', NULL, NULL, NULL, 20, 5),
(31, 3287.54, 0, 0, 3282.76, 0, NULL, NULL, -21.65, 32.89, NULL, NULL, 39.37, 0, '2023-08-03 15:49:55.837836', NULL, NULL, NULL, 20, 5),
(32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '2023-08-03 15:57:04.205033', NULL, NULL, NULL, 20, 5),
(33, 400, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, '2023-08-03 15:57:04.732223', NULL, NULL, NULL, 20, 5),
(34, 430, 0, 0, 4.3, 0, 0, 0, 0, 0, 0, 0, 0, 0, '2023-08-03 15:57:05.065422', NULL, NULL, NULL, 20, 5),
(35, 736.8, 15.33, 326.64, 7.32, 152.6888, 0, 0, -0.22, 0.34, 0, 0, 0.41, 0, '2023-08-03 15:57:05.170112', NULL, NULL, NULL, 20, 5),
(36, 1136.68, 15.33, 326.64, 109.2, 0, 0, 0, -15.58, 23.67, 0, 0, 28.34, 0, '2023-08-03 15:57:05.235643', NULL, NULL, NULL, 20, 5),
(37, 1960.04, 0, 0, 191.221, 5.62925, 0, 0, -21.65, 32.89, 0, 0, 39.37, 0, '2023-08-03 15:57:05.399254', NULL, NULL, NULL, 20, 5),
(38, 3287.54, 0, 0, 3282.76, 0, 0, 0, -21.65, 32.89, 0, 0, 39.37, 0, '2023-08-03 15:57:05.498243', NULL, NULL, NULL, 20, 5),
(39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '2023-08-03 15:57:41.160642', NULL, NULL, NULL, 20, 5),
(40, 400, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, '2023-08-03 15:57:41.252369', NULL, NULL, NULL, 20, 5),
(41, 430, 0, 0, 4.3, 0, 0, 0, 0, 0, 0, 0, 0, 0, '2023-08-03 15:57:41.503068', NULL, NULL, NULL, 20, 5),
(42, 736.8, 15.33, 326.64, 7.32, 152.6888, 0, 0, -0.22, 0.34, 0, 0, 0.41, 0, '2023-08-03 15:57:42.172076', NULL, NULL, NULL, 20, 5),
(43, 1136.68, 15.33, 326.64, 109.2, 0, 0, 0, -15.58, 23.67, 0, 0, 28.34, 0, '2023-08-03 15:57:42.249123', NULL, NULL, NULL, 20, 5),
(44, 1960.04, 0, 0, 191.221, 5.62925, 0, 0, -21.65, 32.89, 0, 0, 39.37, 0, '2023-08-03 15:57:42.316726', NULL, NULL, NULL, 20, 5),
(45, 3287.54, 0, 0, 3282.76, 0, 0, 0, -21.65, 32.89, 0, 0, 39.37, 0, '2023-08-03 15:57:42.345441', NULL, NULL, NULL, 20, 5),
(46, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, '2023-08-03 15:58:32.486183', NULL, NULL, NULL, 20, 5),
(47, 400, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1, '2023-08-03 15:58:32.518683', NULL, NULL, NULL, 20, 5),
(48, 430, 0, 0, 4.3, 0, 0, 0, 0, 0, 0, 0, 0, 1, '2023-08-03 15:58:32.528681', NULL, NULL, NULL, 20, 5),
(49, 736.8, 15.33, 326.64, 7.32, 152.6888, 0, 0, -0.22, 0.34, 0, 0, 0.41, 1, '2023-08-03 15:58:32.553261', NULL, NULL, NULL, 20, 5),
(50, 1136.68, 15.33, 326.64, 109.2, 0, 0, 0, -15.58, 23.67, 0, 0, 28.34, 1, '2023-08-03 15:58:32.572507', NULL, NULL, NULL, 20, 5),
(51, 1960.04, 0, 0, 191.221, 5.62925, 0, 0, -21.65, 32.89, 0, 0, 39.37, 1, '2023-08-03 15:58:32.584475', NULL, NULL, NULL, 20, 5),
(52, 3287.54, 0, 0, 3282.76, 0, 0, 0, -21.65, 32.89, 0, 0, 39.37, 1, '2023-08-03 15:58:32.595775', NULL, NULL, NULL, 20, 5);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `bhadata_bhadata`
--
ALTER TABLE `bhadata_bhadata`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bhadata_bhadata_company_id_be488a32_fk_custom_auth_companies_id` (`company_id`),
  ADD KEY `bhadata_bhadata_well_id_8b59c70d_fk_wells_wells_id` (`well_id`),
  ADD KEY `bhadata_bhadata_well_phases_id_3a05dd32_fk_wellphase` (`well_phases_id`);

--
-- Indexes for table `bhadata_bhaelement`
--
ALTER TABLE `bhadata_bhaelement`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bhadata_bhaelement_bhadata_id_eb188ee6_fk_bhadata_bhadata_id` (`bhadata_id`);

--
-- Indexes for table `bhadata_differential_pressure`
--
ALTER TABLE `bhadata_differential_pressure`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bhadata_differential_bhadata_id_6f67e117_fk_bhadata_b` (`bhadata_id`),
  ADD KEY `bhadata_differential_bhadata_element_id_761b364a_fk_bhadata_b` (`bhadata_element_id`);

--
-- Indexes for table `bhadata_drillcollers`
--
ALTER TABLE `bhadata_drillcollers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bhadata_drillcollers_company_id_b49bc23a_fk_custom_au` (`company_id`);

--
-- Indexes for table `bhadata_drillpipe`
--
ALTER TABLE `bhadata_drillpipe`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bhadata_drillpipe_company_id_e8c8112e_fk_custom_au` (`company_id`);

--
-- Indexes for table `bhadata_drillpipehwdp`
--
ALTER TABLE `bhadata_drillpipehwdp`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bhadata_drillpipehwd_company_id_56b28f85_fk_custom_au` (`company_id`);

--
-- Indexes for table `bhadata_empirical`
--
ALTER TABLE `bhadata_empirical`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bhadata_empirical_bhadata_id_21dd8da6_fk_bhadata_bhadata_id` (`bhadata_id`),
  ADD KEY `bhadata_empirical_bhadata_element_id_9e680369_fk_bhadata_b` (`bhadata_element_id`);

--
-- Indexes for table `bhadata_pressuredroptool`
--
ALTER TABLE `bhadata_pressuredroptool`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bhadata_pressuredrop_bhadata_id_24c50852_fk_bhadata_b` (`bhadata_id`),
  ADD KEY `bhadata_pressuredrop_bhadata_element_id_31016c26_fk_bhadata_b` (`bhadata_element_id`);

--
-- Indexes for table `bhadata_specifications`
--
ALTER TABLE `bhadata_specifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bhadata_specifications_bhadata_id_76fd1d37_fk_bhadata_bhadata_id` (`bhadata_id`),
  ADD KEY `bhadata_specificatio_bhadata_element_id_3ba950d9_fk_bhadata_b` (`bhadata_element_id`);

--
-- Indexes for table `bittype_names`
--
ALTER TABLE `bittype_names`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `custom_auth_basecountries`
--
ALTER TABLE `custom_auth_basecountries`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `custom_auth_companies`
--
ALTER TABLE `custom_auth_companies`
  ADD PRIMARY KEY (`id`),
  ADD KEY `custom_auth_companie_country_id_d62c18b8_fk_custom_au` (`country_id`),
  ADD KEY `custom_auth_companies_userid_id_c3901378_fk_custom_auth_user_id` (`userid_id`);

--
-- Indexes for table `custom_auth_companypackages`
--
ALTER TABLE `custom_auth_companypackages`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `custom_auth_countries`
--
ALTER TABLE `custom_auth_countries`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `custom_auth_packageconcurrentusers`
--
ALTER TABLE `custom_auth_packageconcurrentusers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `custom_auth_packagec_package_id_ad6d7684_fk_custom_au` (`package_id`);

--
-- Indexes for table `custom_auth_packages`
--
ALTER TABLE `custom_auth_packages`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `custom_auth_packageusers`
--
ALTER TABLE `custom_auth_packageusers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `custom_auth_packageu_package_concurrent_u_a1f8b6dd_fk_custom_au` (`package_concurrent_users_id`);

--
-- Indexes for table `custom_auth_payments`
--
ALTER TABLE `custom_auth_payments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `custom_auth_user`
--
ALTER TABLE `custom_auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `custom_auth_user_company_id_28fd7d9a_fk_custom_auth_companies_id` (`company_id`);

--
-- Indexes for table `custom_auth_user_groups`
--
ALTER TABLE `custom_auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `custom_auth_user_groups_user_id_group_id_07773560_uniq` (`user_id`,`group_id`),
  ADD KEY `custom_auth_user_groups_group_id_be8803b9_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `custom_auth_user_user_permissions`
--
ALTER TABLE `custom_auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `custom_auth_user_user_pe_user_id_permission_id_e2cda069_uniq` (`user_id`,`permission_id`),
  ADD KEY `custom_auth_user_use_permission_id_0427cb51_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_custom_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `drillbitdata_drillbit`
--
ALTER TABLE `drillbitdata_drillbit`
  ADD PRIMARY KEY (`id`),
  ADD KEY `drillbitdata_drillbit_bha_id_f7db12dc_fk_bhadata_bhadata_id` (`bha_id`),
  ADD KEY `drillbitdata_drillbit_bit_type_id_f8e722b2_fk_bittype_names_id` (`bit_type_id`),
  ADD KEY `drillbitdata_drillbi_company_id_32e9f10b_fk_custom_au` (`company_id`),
  ADD KEY `drillbitdata_drillbit_well_id_77df5677_fk_wells_wells_id` (`well_id`),
  ADD KEY `drillbitdata_drillbi_well_phases_id_5aaa3a7d_fk_wellphase` (`well_phases_id`);

--
-- Indexes for table `drillbitdata_drillbitnozzle`
--
ALTER TABLE `drillbitdata_drillbitnozzle`
  ADD PRIMARY KEY (`id`),
  ADD KEY `drillbitdata_drillbi_company_id_326a3212_fk_custom_au` (`company_id`),
  ADD KEY `drillbitdata_drillbi_drillbit_id_0d26bf00_fk_drillbitd` (`drillbit_id`),
  ADD KEY `drillbitdata_drillbitnozzle_well_id_8d288a79_fk_wells_wells_id` (`well_id`);

--
-- Indexes for table `enquiries`
--
ALTER TABLE `enquiries`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `license_licensepackage`
--
ALTER TABLE `license_licensepackage`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `modules`
--
ALTER TABLE `modules`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `muddata_hydraulicdata`
--
ALTER TABLE `muddata_hydraulicdata`
  ADD PRIMARY KEY (`id`),
  ADD KEY `muddata_hydraulicdat_company_id_b8c6b857_fk_custom_au` (`company_id`),
  ADD KEY `muddata_hydraulicdata_well_id_9107a45f_fk_wells_wells_id` (`well_id`),
  ADD KEY `muddata_hydraulicdat_well_phase_id_f1a6e055_fk_wellphase` (`well_phase_id`);

--
-- Indexes for table `muddata_muddata`
--
ALTER TABLE `muddata_muddata`
  ADD PRIMARY KEY (`id`),
  ADD KEY `muddata_muddata_mudtype_id_c27aed9e_fk_mudtype_id` (`mudtype_id`),
  ADD KEY `muddata_muddata_well_id_9c8afa8e_fk_wells_wells_id` (`well_id`),
  ADD KEY `muddata_muddata_well_phase_id_eccd4e33_fk_wellphase` (`well_phase_id`),
  ADD KEY `muddata_muddata_company_id_75115c62_fk_custom_auth_companies_id` (`company_id`);

--
-- Indexes for table `muddata_plandate`
--
ALTER TABLE `muddata_plandate`
  ADD PRIMARY KEY (`id`),
  ADD KEY `muddata_plandate_company_id_d617e37b_fk_custom_auth_companies_id` (`company_id`),
  ADD KEY `muddata_plandate_well_id_95719af8_fk_wells_wells_id` (`well_id`),
  ADD KEY `muddata_plandate_well_phase_id_09da4025_fk_wellphase` (`well_phase_id`);

--
-- Indexes for table `muddata_pressureloss_data`
--
ALTER TABLE `muddata_pressureloss_data`
  ADD PRIMARY KEY (`id`),
  ADD KEY `muddata_pressureloss_company_id_762dda3d_fk_custom_au` (`company_id`),
  ADD KEY `muddata_pressureloss_data_well_id_209c2b05_fk_wells_wells_id` (`well_id`),
  ADD KEY `muddata_pressureloss_well_phase_id_ca1854a7_fk_wellphase` (`well_phase_id`);

--
-- Indexes for table `muddata_rheogram`
--
ALTER TABLE `muddata_rheogram`
  ADD PRIMARY KEY (`id`),
  ADD KEY `muddata_rheogram_company_id_9a47eb36_fk_custom_auth_companies_id` (`company_id`),
  ADD KEY `muddata_rheogram_rheogram_date_id_246aed67_fk_rheogram_date_id` (`rheogram_date_id`),
  ADD KEY `muddata_rheogram_rheogram_sections_id_aac5a66b_fk_rheogram_` (`rheogram_sections_id`),
  ADD KEY `muddata_rheogram_well_id_d1911b11_fk_wells_wells_id` (`well_id`);

--
-- Indexes for table `mudtype`
--
ALTER TABLE `mudtype`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `mud_mudpump`
--
ALTER TABLE `mud_mudpump`
  ADD PRIMARY KEY (`id`),
  ADD KEY `mud_mudpump_company_id_c4a4eda8_fk_custom_auth_companies_id` (`company_id`),
  ADD KEY `mud_mudpump_well_id_561493d0_fk_wells_wells_id` (`well_id`);

--
-- Indexes for table `mud_mudpumpdata`
--
ALTER TABLE `mud_mudpumpdata`
  ADD PRIMARY KEY (`id`),
  ADD KEY `mud_mudpumpdata_company_id_f3701a05_fk_custom_auth_companies_id` (`company_id`),
  ADD KEY `mud_mudpumpdata_mud_pump_id_31db6e2b_fk_mud_mudpump_id` (`mud_pump_id`),
  ADD KEY `mud_mudpumpdata_well_id_ad617cf1_fk_wells_wells_id` (`well_id`);

--
-- Indexes for table `mud_mudpumpflowrate`
--
ALTER TABLE `mud_mudpumpflowrate`
  ADD PRIMARY KEY (`id`),
  ADD KEY `mud_mudpumpflowrate_company_id_688dbbe7_fk_custom_au` (`company_id`),
  ADD KEY `mud_mudpumpflowrate_mud_pump_speed_id_a4078ada_fk_mud_mudpu` (`mud_pump_speed_id`),
  ADD KEY `mud_mudpumpflowrate_well_id_f0249f3a_fk_wells_wells_id` (`well_id`);

--
-- Indexes for table `mud_mudpumpmasterdata`
--
ALTER TABLE `mud_mudpumpmasterdata`
  ADD PRIMARY KEY (`id`),
  ADD KEY `mud_mudpumpmasterdat_company_id_576274e8_fk_custom_au` (`company_id`),
  ADD KEY `mud_mudpumpmasterdat_mud_pump_master_id_27e9e1bc_fk_mud_pumps` (`mud_pump_master_id`);

--
-- Indexes for table `mud_mudpumpmasterflowrate`
--
ALTER TABLE `mud_mudpumpmasterflowrate`
  ADD PRIMARY KEY (`id`),
  ADD KEY `mud_mudpumpmasterflo_company_id_3ba2a50e_fk_custom_au` (`company_id`),
  ADD KEY `mud_mudpumpmasterflo_mud_pump_master_spee_a39e611c_fk_mud_mudpu` (`mud_pump_master_speed_id`);

--
-- Indexes for table `mud_mudpumpmasterspeed`
--
ALTER TABLE `mud_mudpumpmasterspeed`
  ADD PRIMARY KEY (`id`),
  ADD KEY `mud_mudpumpmasterspe_company_id_69907ef1_fk_custom_au` (`company_id`),
  ADD KEY `mud_mudpumpmasterspe_mud_pump_master_id_dd1369e8_fk_mud_pumps` (`mud_pump_master_id`);

--
-- Indexes for table `mud_mudpumpspeed`
--
ALTER TABLE `mud_mudpumpspeed`
  ADD PRIMARY KEY (`id`),
  ADD KEY `mud_mudpumpspeed_company_id_0ddc71d2_fk_custom_auth_companies_id` (`company_id`),
  ADD KEY `mud_mudpumpspeed_mud_pump_id_3e688c14_fk_mud_mudpump_id` (`mud_pump_id`),
  ADD KEY `mud_mudpumpspeed_well_id_151556d2_fk_wells_wells_id` (`well_id`);

--
-- Indexes for table `mud_pumpmanufacturer`
--
ALTER TABLE `mud_pumpmanufacturer`
  ADD PRIMARY KEY (`id`),
  ADD KEY `mud_pumpmanufacturer_company_id_9443e605_fk_custom_au` (`company_id`);

--
-- Indexes for table `mud_pumps`
--
ALTER TABLE `mud_pumps`
  ADD PRIMARY KEY (`id`),
  ADD KEY `mud_pumps_company_id_720f8d1a_fk_custom_auth_companies_id` (`company_id`),
  ADD KEY `mud_pumps_pump_manufacturer_id_c64dd4d6_fk_mud_pumpm` (`pump_manufacturer_id`);

--
-- Indexes for table `notifications_notification`
--
ALTER TABLE `notifications_notification`
  ADD PRIMARY KEY (`id`),
  ADD KEY `notifications_notifi_action_object_conten_7d2b8ee9_fk_django_co` (`action_object_content_type_id`),
  ADD KEY `notifications_notifi_actor_content_type_i_0c69d7b7_fk_django_co` (`actor_content_type_id`),
  ADD KEY `notifications_notifi_target_content_type__ccb24d88_fk_django_co` (`target_content_type_id`),
  ADD KEY `notifications_notification_deleted_b32b69e6` (`deleted`),
  ADD KEY `notifications_notification_emailed_23a5ad81` (`emailed`),
  ADD KEY `notifications_notification_public_1bc30b1c` (`public`),
  ADD KEY `notifications_notification_unread_cce4be30` (`unread`),
  ADD KEY `notifications_notification_timestamp_6a797bad` (`timestamp`),
  ADD KEY `notifications_notification_recipient_id_unread_253aadc9_idx` (`recipient_id`,`unread`);

--
-- Indexes for table `pressure_pressure`
--
ALTER TABLE `pressure_pressure`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pressure_pressure_company_id_f4fa362c_fk_custom_au` (`company_id`),
  ADD KEY `pressure_pressure_well_id_3d3ea8f1_fk_wells_wells_id` (`well_id`);

--
-- Indexes for table `projects_projectblock`
--
ALTER TABLE `projects_projectblock`
  ADD PRIMARY KEY (`id`),
  ADD KEY `projects_projectbloc_project_id_c72d553d_fk_projects_` (`project_id`);

--
-- Indexes for table `projects_projectfield`
--
ALTER TABLE `projects_projectfield`
  ADD PRIMARY KEY (`id`),
  ADD KEY `projects_projectfiel_block_id_859423a2_fk_projects_` (`block_id`),
  ADD KEY `projects_projectfiel_project_id_69a5535f_fk_projects_` (`project_id`);

--
-- Indexes for table `projects_projects`
--
ALTER TABLE `projects_projects`
  ADD PRIMARY KEY (`id`),
  ADD KEY `projects_projects_company_id_152710b0_fk_custom_au` (`company_id`),
  ADD KEY `projects_projects_country_id_6095fc7f_fk_custom_au` (`country_id`),
  ADD KEY `projects_projects_created_by_id_c1843844_fk_custom_auth_user_id` (`created_by_id`);

--
-- Indexes for table `projects_projectusers`
--
ALTER TABLE `projects_projectusers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `projects_projectuser_project_id_6f15c346_fk_projects_` (`project_id`),
  ADD KEY `projects_projectusers_role_id_5c317385_fk_auth_group_id` (`role_id`),
  ADD KEY `projects_projectusers_user_id_aa48835f_fk_custom_auth_user_id` (`user_id`);

--
-- Indexes for table `rheogram_date`
--
ALTER TABLE `rheogram_date`
  ADD PRIMARY KEY (`id`),
  ADD KEY `rheogram_date_company_id_e20cd0d9_fk_custom_auth_companies_id` (`company_id`),
  ADD KEY `rheogram_date_muddata_id_d166d0f5_fk_muddata_muddata_id` (`muddata_id`),
  ADD KEY `rheogram_date_well_id_8f0a134f_fk_wells_wells_id` (`well_id`),
  ADD KEY `rheogram_date_well_phase_id_4d909c11_fk_wellphases_wellphases_id` (`well_phase_id`);

--
-- Indexes for table `rheogram_rpm`
--
ALTER TABLE `rheogram_rpm`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `rheogram_sections`
--
ALTER TABLE `rheogram_sections`
  ADD PRIMARY KEY (`id`),
  ADD KEY `rheogram_sections_rheogram_date_id_9175fc20_fk_rheogram_date_id` (`rheogram_date_id`),
  ADD KEY `rheogram_sections_well_phase_id_29160549_fk_wellphase` (`well_phase_id`);

--
-- Indexes for table `rights`
--
ALTER TABLE `rights`
  ADD PRIMARY KEY (`id`),
  ADD KEY `rights_company_id_82151295_fk_custom_auth_companies_id` (`company_id`),
  ADD KEY `rights_module_id_78eaff8b_fk_modules_id` (`module_id`),
  ADD KEY `rights_role_id_59aa8b33_fk_auth_group_id` (`role_id`);

--
-- Indexes for table `rig_information`
--
ALTER TABLE `rig_information`
  ADD PRIMARY KEY (`id`),
  ADD KEY `rig_information_company_id_24757dab_fk_custom_auth_companies_id` (`company_id`),
  ADD KEY `rig_information_well_id_09e911b9_fk_wells_wells_id` (`well_id`);

--
-- Indexes for table `Sections`
--
ALTER TABLE `Sections`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Sections_company_id_f1b0f633_fk_custom_auth_companies_id` (`company_id`),
  ADD KEY `Sections_well_id_709a2c5a_fk_wells_wells_id` (`well_id`),
  ADD KEY `Sections_well_phase_id_56fd3f9e_fk_wellphases_wellphases_id` (`well_phase_id`);

--
-- Indexes for table `surfacepipe_surfacepipe`
--
ALTER TABLE `surfacepipe_surfacepipe`
  ADD PRIMARY KEY (`id`),
  ADD KEY `surfacepipe_surfacep_company_id_f02b1ecd_fk_custom_au` (`company_id`),
  ADD KEY `surfacepipe_surfacepipe_well_id_a726c0e6_fk_wells_wells_id` (`well_id`);

--
-- Indexes for table `surfacepipe_surfacepipedata`
--
ALTER TABLE `surfacepipe_surfacepipedata`
  ADD PRIMARY KEY (`id`),
  ADD KEY `surfacepipe_surfacep_company_id_61aff29a_fk_custom_au` (`company_id`),
  ADD KEY `surfacepipe_surfacep_surfacepipe_id_238b8769_fk_surfacepi` (`surfacepipe_id`),
  ADD KEY `surfacepipe_surfacepipedata_well_id_a9114cc2_fk_wells_wells_id` (`well_id`);

--
-- Indexes for table `surfacepiping_names`
--
ALTER TABLE `surfacepiping_names`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tickets`
--
ALTER TABLE `tickets`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `userlog`
--
ALTER TABLE `userlog`
  ADD PRIMARY KEY (`id`),
  ADD KEY `userlog_user_id_id_85d963df_fk_custom_auth_user_id` (`user_id`);

--
-- Indexes for table `wellphases_casing`
--
ALTER TABLE `wellphases_casing`
  ADD PRIMARY KEY (`id`),
  ADD KEY `wellphases_casing_company_id_9d137d8d_fk_custom_au` (`company_id`);

--
-- Indexes for table `wellphases_casinggrade`
--
ALTER TABLE `wellphases_casinggrade`
  ADD PRIMARY KEY (`id`),
  ADD KEY `wellphases_casinggra_company_id_86797a48_fk_custom_au` (`company_id`);

--
-- Indexes for table `wellphases_casingrange`
--
ALTER TABLE `wellphases_casingrange`
  ADD PRIMARY KEY (`id`),
  ADD KEY `wellphases_casingran_company_id_c65a66ed_fk_custom_au` (`company_id`);

--
-- Indexes for table `wellphases_casingtypes`
--
ALTER TABLE `wellphases_casingtypes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `wellphases_wellphases`
--
ALTER TABLE `wellphases_wellphases`
  ADD PRIMARY KEY (`id`),
  ADD KEY `wellphases_wellphase_casing_type_id_c13c5642_fk_wellphase` (`casing_type_id`),
  ADD KEY `wellphases_wellphase_company_id_9281c3ac_fk_custom_au` (`company_id`),
  ADD KEY `wellphases_wellphases_well_id_d1b53bf3_fk_wells_wells_id` (`well_id`);

--
-- Indexes for table `wells_coordinatesystems`
--
ALTER TABLE `wells_coordinatesystems`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `wells_projections`
--
ALTER TABLE `wells_projections`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `wells_wells`
--
ALTER TABLE `wells_wells`
  ADD PRIMARY KEY (`id`),
  ADD KEY `wells_wells_block_id_fe91dd24_fk_projects_projectblock_id` (`block_id`),
  ADD KEY `wells_wells_company_id_9a250b42_fk_custom_auth_companies_id` (`company_id`),
  ADD KEY `wells_wells_coordinate_system_id_641f4163_fk_wells_coo` (`coordinate_system_id`),
  ADD KEY `wells_wells_created_by_id_e5790602_fk_custom_auth_user_id` (`created_by_id`),
  ADD KEY `wells_wells_field_id_6f53d317_fk_projects_projectfield_id` (`field_id`),
  ADD KEY `wells_wells_plan_well_list_id_f7c5bfff_fk_wells_wells_id` (`plan_well_list_id`),
  ADD KEY `wells_wells_project_id_5059cde5_fk_projects_projects_id` (`project_id`),
  ADD KEY `wells_wells_projection_id_ad448707_fk_wells_projections_id` (`projection_id`);

--
-- Indexes for table `wells_wellusers`
--
ALTER TABLE `wells_wellusers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `wells_wellusers_role_id_cb2901c0_fk_auth_group_id` (`role_id`),
  ADD KEY `wells_wellusers_user_id_4ce9a5cf_fk_custom_auth_user_id` (`user_id`),
  ADD KEY `wells_wellusers_well_id_58681a0b_fk_wells_wells_id` (`well_id`);

--
-- Indexes for table `welltrajectory_welltrajectory`
--
ALTER TABLE `welltrajectory_welltrajectory`
  ADD PRIMARY KEY (`id`),
  ADD KEY `welltrajectory_wellt_company_id_b426b736_fk_custom_au` (`company_id`),
  ADD KEY `welltrajectory_welltrajectory_well_id_20465038_fk_wells_wells_id` (`well_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=297;

--
-- AUTO_INCREMENT for table `bhadata_bhadata`
--
ALTER TABLE `bhadata_bhadata`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `bhadata_bhaelement`
--
ALTER TABLE `bhadata_bhaelement`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `bhadata_differential_pressure`
--
ALTER TABLE `bhadata_differential_pressure`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `bhadata_drillcollers`
--
ALTER TABLE `bhadata_drillcollers`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `bhadata_drillpipe`
--
ALTER TABLE `bhadata_drillpipe`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=94;

--
-- AUTO_INCREMENT for table `bhadata_drillpipehwdp`
--
ALTER TABLE `bhadata_drillpipehwdp`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=50;

--
-- AUTO_INCREMENT for table `bhadata_empirical`
--
ALTER TABLE `bhadata_empirical`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `bhadata_pressuredroptool`
--
ALTER TABLE `bhadata_pressuredroptool`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `bhadata_specifications`
--
ALTER TABLE `bhadata_specifications`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `bittype_names`
--
ALTER TABLE `bittype_names`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `custom_auth_basecountries`
--
ALTER TABLE `custom_auth_basecountries`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `custom_auth_companies`
--
ALTER TABLE `custom_auth_companies`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `custom_auth_companypackages`
--
ALTER TABLE `custom_auth_companypackages`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `custom_auth_countries`
--
ALTER TABLE `custom_auth_countries`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=240;

--
-- AUTO_INCREMENT for table `custom_auth_packageconcurrentusers`
--
ALTER TABLE `custom_auth_packageconcurrentusers`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `custom_auth_packages`
--
ALTER TABLE `custom_auth_packages`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `custom_auth_packageusers`
--
ALTER TABLE `custom_auth_packageusers`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `custom_auth_payments`
--
ALTER TABLE `custom_auth_payments`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `custom_auth_user`
--
ALTER TABLE `custom_auth_user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `custom_auth_user_groups`
--
ALTER TABLE `custom_auth_user_groups`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `custom_auth_user_user_permissions`
--
ALTER TABLE `custom_auth_user_user_permissions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=75;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `drillbitdata_drillbit`
--
ALTER TABLE `drillbitdata_drillbit`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `drillbitdata_drillbitnozzle`
--
ALTER TABLE `drillbitdata_drillbitnozzle`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `enquiries`
--
ALTER TABLE `enquiries`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `license_licensepackage`
--
ALTER TABLE `license_licensepackage`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `modules`
--
ALTER TABLE `modules`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `muddata_hydraulicdata`
--
ALTER TABLE `muddata_hydraulicdata`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `muddata_muddata`
--
ALTER TABLE `muddata_muddata`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `muddata_plandate`
--
ALTER TABLE `muddata_plandate`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `muddata_pressureloss_data`
--
ALTER TABLE `muddata_pressureloss_data`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `muddata_rheogram`
--
ALTER TABLE `muddata_rheogram`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `mudtype`
--
ALTER TABLE `mudtype`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `mud_mudpump`
--
ALTER TABLE `mud_mudpump`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `mud_mudpumpdata`
--
ALTER TABLE `mud_mudpumpdata`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `mud_mudpumpflowrate`
--
ALTER TABLE `mud_mudpumpflowrate`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=101;

--
-- AUTO_INCREMENT for table `mud_mudpumpmasterdata`
--
ALTER TABLE `mud_mudpumpmasterdata`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `mud_mudpumpmasterflowrate`
--
ALTER TABLE `mud_mudpumpmasterflowrate`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT for table `mud_mudpumpmasterspeed`
--
ALTER TABLE `mud_mudpumpmasterspeed`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `mud_mudpumpspeed`
--
ALTER TABLE `mud_mudpumpspeed`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `mud_pumpmanufacturer`
--
ALTER TABLE `mud_pumpmanufacturer`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `mud_pumps`
--
ALTER TABLE `mud_pumps`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `notifications_notification`
--
ALTER TABLE `notifications_notification`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT for table `pressure_pressure`
--
ALTER TABLE `pressure_pressure`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `projects_projectblock`
--
ALTER TABLE `projects_projectblock`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `projects_projectfield`
--
ALTER TABLE `projects_projectfield`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `projects_projects`
--
ALTER TABLE `projects_projects`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `projects_projectusers`
--
ALTER TABLE `projects_projectusers`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `rheogram_date`
--
ALTER TABLE `rheogram_date`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `rheogram_rpm`
--
ALTER TABLE `rheogram_rpm`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `rheogram_sections`
--
ALTER TABLE `rheogram_sections`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `rights`
--
ALTER TABLE `rights`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `rig_information`
--
ALTER TABLE `rig_information`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `Sections`
--
ALTER TABLE `Sections`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `surfacepipe_surfacepipe`
--
ALTER TABLE `surfacepipe_surfacepipe`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `surfacepipe_surfacepipedata`
--
ALTER TABLE `surfacepipe_surfacepipedata`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `surfacepiping_names`
--
ALTER TABLE `surfacepiping_names`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `tickets`
--
ALTER TABLE `tickets`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `userlog`
--
ALTER TABLE `userlog`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `wellphases_casing`
--
ALTER TABLE `wellphases_casing`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=820;

--
-- AUTO_INCREMENT for table `wellphases_casinggrade`
--
ALTER TABLE `wellphases_casinggrade`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `wellphases_casingrange`
--
ALTER TABLE `wellphases_casingrange`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `wellphases_casingtypes`
--
ALTER TABLE `wellphases_casingtypes`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `wellphases_wellphases`
--
ALTER TABLE `wellphases_wellphases`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `wells_coordinatesystems`
--
ALTER TABLE `wells_coordinatesystems`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `wells_projections`
--
ALTER TABLE `wells_projections`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=62;

--
-- AUTO_INCREMENT for table `wells_wells`
--
ALTER TABLE `wells_wells`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `wells_wellusers`
--
ALTER TABLE `wells_wellusers`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `welltrajectory_welltrajectory`
--
ALTER TABLE `welltrajectory_welltrajectory`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `bhadata_bhadata`
--
ALTER TABLE `bhadata_bhadata`
  ADD CONSTRAINT `bhadata_bhadata_company_id_be488a32_fk_custom_auth_companies_id` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `bhadata_bhadata_well_id_8b59c70d_fk_wells_wells_id` FOREIGN KEY (`well_id`) REFERENCES `wells_wells` (`id`),
  ADD CONSTRAINT `bhadata_bhadata_well_phases_id_3a05dd32_fk_wellphase` FOREIGN KEY (`well_phases_id`) REFERENCES `wellphases_wellphases` (`id`);

--
-- Constraints for table `bhadata_bhaelement`
--
ALTER TABLE `bhadata_bhaelement`
  ADD CONSTRAINT `bhadata_bhaelement_bhadata_id_eb188ee6_fk_bhadata_bhadata_id` FOREIGN KEY (`bhadata_id`) REFERENCES `bhadata_bhadata` (`id`);

--
-- Constraints for table `bhadata_differential_pressure`
--
ALTER TABLE `bhadata_differential_pressure`
  ADD CONSTRAINT `bhadata_differential_bhadata_element_id_761b364a_fk_bhadata_b` FOREIGN KEY (`bhadata_element_id`) REFERENCES `bhadata_bhaelement` (`id`),
  ADD CONSTRAINT `bhadata_differential_bhadata_id_6f67e117_fk_bhadata_b` FOREIGN KEY (`bhadata_id`) REFERENCES `bhadata_bhadata` (`id`);

--
-- Constraints for table `bhadata_drillcollers`
--
ALTER TABLE `bhadata_drillcollers`
  ADD CONSTRAINT `bhadata_drillcollers_company_id_b49bc23a_fk_custom_au` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`);

--
-- Constraints for table `bhadata_drillpipe`
--
ALTER TABLE `bhadata_drillpipe`
  ADD CONSTRAINT `bhadata_drillpipe_company_id_e8c8112e_fk_custom_au` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`);

--
-- Constraints for table `bhadata_drillpipehwdp`
--
ALTER TABLE `bhadata_drillpipehwdp`
  ADD CONSTRAINT `bhadata_drillpipehwd_company_id_56b28f85_fk_custom_au` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`);

--
-- Constraints for table `bhadata_empirical`
--
ALTER TABLE `bhadata_empirical`
  ADD CONSTRAINT `bhadata_empirical_bhadata_element_id_9e680369_fk_bhadata_b` FOREIGN KEY (`bhadata_element_id`) REFERENCES `bhadata_bhaelement` (`id`),
  ADD CONSTRAINT `bhadata_empirical_bhadata_id_21dd8da6_fk_bhadata_bhadata_id` FOREIGN KEY (`bhadata_id`) REFERENCES `bhadata_bhadata` (`id`);

--
-- Constraints for table `bhadata_pressuredroptool`
--
ALTER TABLE `bhadata_pressuredroptool`
  ADD CONSTRAINT `bhadata_pressuredrop_bhadata_element_id_31016c26_fk_bhadata_b` FOREIGN KEY (`bhadata_element_id`) REFERENCES `bhadata_bhaelement` (`id`),
  ADD CONSTRAINT `bhadata_pressuredrop_bhadata_id_24c50852_fk_bhadata_b` FOREIGN KEY (`bhadata_id`) REFERENCES `bhadata_bhadata` (`id`);

--
-- Constraints for table `bhadata_specifications`
--
ALTER TABLE `bhadata_specifications`
  ADD CONSTRAINT `bhadata_specificatio_bhadata_element_id_3ba950d9_fk_bhadata_b` FOREIGN KEY (`bhadata_element_id`) REFERENCES `bhadata_bhaelement` (`id`),
  ADD CONSTRAINT `bhadata_specifications_bhadata_id_76fd1d37_fk_bhadata_bhadata_id` FOREIGN KEY (`bhadata_id`) REFERENCES `bhadata_bhadata` (`id`);

--
-- Constraints for table `custom_auth_companies`
--
ALTER TABLE `custom_auth_companies`
  ADD CONSTRAINT `custom_auth_companie_country_id_d62c18b8_fk_custom_au` FOREIGN KEY (`country_id`) REFERENCES `custom_auth_countries` (`id`),
  ADD CONSTRAINT `custom_auth_companies_userid_id_c3901378_fk_custom_auth_user_id` FOREIGN KEY (`userid_id`) REFERENCES `custom_auth_user` (`id`);

--
-- Constraints for table `custom_auth_packageconcurrentusers`
--
ALTER TABLE `custom_auth_packageconcurrentusers`
  ADD CONSTRAINT `custom_auth_packagec_package_id_ad6d7684_fk_custom_au` FOREIGN KEY (`package_id`) REFERENCES `custom_auth_packages` (`id`);

--
-- Constraints for table `custom_auth_packageusers`
--
ALTER TABLE `custom_auth_packageusers`
  ADD CONSTRAINT `custom_auth_packageu_package_concurrent_u_a1f8b6dd_fk_custom_au` FOREIGN KEY (`package_concurrent_users_id`) REFERENCES `custom_auth_packageconcurrentusers` (`id`);

--
-- Constraints for table `custom_auth_user`
--
ALTER TABLE `custom_auth_user`
  ADD CONSTRAINT `custom_auth_user_company_id_28fd7d9a_fk_custom_auth_companies_id` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`);

--
-- Constraints for table `custom_auth_user_groups`
--
ALTER TABLE `custom_auth_user_groups`
  ADD CONSTRAINT `custom_auth_user_groups_group_id_be8803b9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `custom_auth_user_groups_user_id_0e71eb5f_fk_custom_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `custom_auth_user` (`id`);

--
-- Constraints for table `custom_auth_user_user_permissions`
--
ALTER TABLE `custom_auth_user_user_permissions`
  ADD CONSTRAINT `custom_auth_user_use_permission_id_0427cb51_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `custom_auth_user_use_user_id_f8893b66_fk_custom_au` FOREIGN KEY (`user_id`) REFERENCES `custom_auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_custom_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `custom_auth_user` (`id`);

--
-- Constraints for table `drillbitdata_drillbit`
--
ALTER TABLE `drillbitdata_drillbit`
  ADD CONSTRAINT `drillbitdata_drillbi_company_id_32e9f10b_fk_custom_au` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `drillbitdata_drillbi_well_phases_id_5aaa3a7d_fk_wellphase` FOREIGN KEY (`well_phases_id`) REFERENCES `wellphases_wellphases` (`id`),
  ADD CONSTRAINT `drillbitdata_drillbit_bha_id_f7db12dc_fk_bhadata_bhadata_id` FOREIGN KEY (`bha_id`) REFERENCES `bhadata_bhadata` (`id`),
  ADD CONSTRAINT `drillbitdata_drillbit_bit_type_id_f8e722b2_fk_bittype_names_id` FOREIGN KEY (`bit_type_id`) REFERENCES `bittype_names` (`id`),
  ADD CONSTRAINT `drillbitdata_drillbit_well_id_77df5677_fk_wells_wells_id` FOREIGN KEY (`well_id`) REFERENCES `wells_wells` (`id`);

--
-- Constraints for table `drillbitdata_drillbitnozzle`
--
ALTER TABLE `drillbitdata_drillbitnozzle`
  ADD CONSTRAINT `drillbitdata_drillbi_company_id_326a3212_fk_custom_au` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `drillbitdata_drillbi_drillbit_id_0d26bf00_fk_drillbitd` FOREIGN KEY (`drillbit_id`) REFERENCES `drillbitdata_drillbit` (`id`),
  ADD CONSTRAINT `drillbitdata_drillbitnozzle_well_id_8d288a79_fk_wells_wells_id` FOREIGN KEY (`well_id`) REFERENCES `wells_wells` (`id`);

--
-- Constraints for table `muddata_hydraulicdata`
--
ALTER TABLE `muddata_hydraulicdata`
  ADD CONSTRAINT `muddata_hydraulicdat_company_id_b8c6b857_fk_custom_au` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `muddata_hydraulicdat_well_phase_id_f1a6e055_fk_wellphase` FOREIGN KEY (`well_phase_id`) REFERENCES `wellphases_wellphases` (`id`),
  ADD CONSTRAINT `muddata_hydraulicdata_well_id_9107a45f_fk_wells_wells_id` FOREIGN KEY (`well_id`) REFERENCES `wells_wells` (`id`);

--
-- Constraints for table `muddata_muddata`
--
ALTER TABLE `muddata_muddata`
  ADD CONSTRAINT `muddata_muddata_company_id_75115c62_fk_custom_auth_companies_id` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `muddata_muddata_mudtype_id_c27aed9e_fk_mudtype_id` FOREIGN KEY (`mudtype_id`) REFERENCES `mudtype` (`id`),
  ADD CONSTRAINT `muddata_muddata_well_id_9c8afa8e_fk_wells_wells_id` FOREIGN KEY (`well_id`) REFERENCES `wells_wells` (`id`),
  ADD CONSTRAINT `muddata_muddata_well_phase_id_eccd4e33_fk_wellphase` FOREIGN KEY (`well_phase_id`) REFERENCES `wellphases_wellphases` (`id`);

--
-- Constraints for table `muddata_plandate`
--
ALTER TABLE `muddata_plandate`
  ADD CONSTRAINT `muddata_plandate_company_id_d617e37b_fk_custom_auth_companies_id` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `muddata_plandate_well_id_95719af8_fk_wells_wells_id` FOREIGN KEY (`well_id`) REFERENCES `wells_wells` (`id`),
  ADD CONSTRAINT `muddata_plandate_well_phase_id_09da4025_fk_wellphase` FOREIGN KEY (`well_phase_id`) REFERENCES `wellphases_wellphases` (`id`);

--
-- Constraints for table `muddata_pressureloss_data`
--
ALTER TABLE `muddata_pressureloss_data`
  ADD CONSTRAINT `muddata_pressureloss_company_id_762dda3d_fk_custom_au` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `muddata_pressureloss_data_well_id_209c2b05_fk_wells_wells_id` FOREIGN KEY (`well_id`) REFERENCES `wells_wells` (`id`),
  ADD CONSTRAINT `muddata_pressureloss_well_phase_id_ca1854a7_fk_wellphase` FOREIGN KEY (`well_phase_id`) REFERENCES `wellphases_wellphases` (`id`);

--
-- Constraints for table `muddata_rheogram`
--
ALTER TABLE `muddata_rheogram`
  ADD CONSTRAINT `muddata_rheogram_company_id_9a47eb36_fk_custom_auth_companies_id` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `muddata_rheogram_rheogram_date_id_246aed67_fk_rheogram_date_id` FOREIGN KEY (`rheogram_date_id`) REFERENCES `rheogram_date` (`id`),
  ADD CONSTRAINT `muddata_rheogram_rheogram_sections_id_aac5a66b_fk_rheogram_` FOREIGN KEY (`rheogram_sections_id`) REFERENCES `rheogram_sections` (`id`),
  ADD CONSTRAINT `muddata_rheogram_well_id_d1911b11_fk_wells_wells_id` FOREIGN KEY (`well_id`) REFERENCES `wells_wells` (`id`);

--
-- Constraints for table `mud_mudpump`
--
ALTER TABLE `mud_mudpump`
  ADD CONSTRAINT `mud_mudpump_company_id_c4a4eda8_fk_custom_auth_companies_id` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `mud_mudpump_well_id_561493d0_fk_wells_wells_id` FOREIGN KEY (`well_id`) REFERENCES `wells_wells` (`id`);

--
-- Constraints for table `mud_mudpumpdata`
--
ALTER TABLE `mud_mudpumpdata`
  ADD CONSTRAINT `mud_mudpumpdata_company_id_f3701a05_fk_custom_auth_companies_id` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `mud_mudpumpdata_mud_pump_id_31db6e2b_fk_mud_mudpump_id` FOREIGN KEY (`mud_pump_id`) REFERENCES `mud_mudpump` (`id`),
  ADD CONSTRAINT `mud_mudpumpdata_well_id_ad617cf1_fk_wells_wells_id` FOREIGN KEY (`well_id`) REFERENCES `wells_wells` (`id`);

--
-- Constraints for table `mud_mudpumpflowrate`
--
ALTER TABLE `mud_mudpumpflowrate`
  ADD CONSTRAINT `mud_mudpumpflowrate_company_id_688dbbe7_fk_custom_au` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `mud_mudpumpflowrate_mud_pump_speed_id_a4078ada_fk_mud_mudpu` FOREIGN KEY (`mud_pump_speed_id`) REFERENCES `mud_mudpumpspeed` (`id`),
  ADD CONSTRAINT `mud_mudpumpflowrate_well_id_f0249f3a_fk_wells_wells_id` FOREIGN KEY (`well_id`) REFERENCES `wells_wells` (`id`);

--
-- Constraints for table `mud_mudpumpmasterdata`
--
ALTER TABLE `mud_mudpumpmasterdata`
  ADD CONSTRAINT `mud_mudpumpmasterdat_company_id_576274e8_fk_custom_au` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `mud_mudpumpmasterdat_mud_pump_master_id_27e9e1bc_fk_mud_pumps` FOREIGN KEY (`mud_pump_master_id`) REFERENCES `mud_pumps` (`id`);

--
-- Constraints for table `mud_mudpumpmasterflowrate`
--
ALTER TABLE `mud_mudpumpmasterflowrate`
  ADD CONSTRAINT `mud_mudpumpmasterflo_company_id_3ba2a50e_fk_custom_au` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `mud_mudpumpmasterflo_mud_pump_master_spee_a39e611c_fk_mud_mudpu` FOREIGN KEY (`mud_pump_master_speed_id`) REFERENCES `mud_mudpumpmasterspeed` (`id`);

--
-- Constraints for table `mud_mudpumpmasterspeed`
--
ALTER TABLE `mud_mudpumpmasterspeed`
  ADD CONSTRAINT `mud_mudpumpmasterspe_company_id_69907ef1_fk_custom_au` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `mud_mudpumpmasterspe_mud_pump_master_id_dd1369e8_fk_mud_pumps` FOREIGN KEY (`mud_pump_master_id`) REFERENCES `mud_pumps` (`id`);

--
-- Constraints for table `mud_mudpumpspeed`
--
ALTER TABLE `mud_mudpumpspeed`
  ADD CONSTRAINT `mud_mudpumpspeed_company_id_0ddc71d2_fk_custom_auth_companies_id` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `mud_mudpumpspeed_mud_pump_id_3e688c14_fk_mud_mudpump_id` FOREIGN KEY (`mud_pump_id`) REFERENCES `mud_mudpump` (`id`),
  ADD CONSTRAINT `mud_mudpumpspeed_well_id_151556d2_fk_wells_wells_id` FOREIGN KEY (`well_id`) REFERENCES `wells_wells` (`id`);

--
-- Constraints for table `mud_pumpmanufacturer`
--
ALTER TABLE `mud_pumpmanufacturer`
  ADD CONSTRAINT `mud_pumpmanufacturer_company_id_9443e605_fk_custom_au` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`);

--
-- Constraints for table `mud_pumps`
--
ALTER TABLE `mud_pumps`
  ADD CONSTRAINT `mud_pumps_company_id_720f8d1a_fk_custom_auth_companies_id` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `mud_pumps_pump_manufacturer_id_c64dd4d6_fk_mud_pumpm` FOREIGN KEY (`pump_manufacturer_id`) REFERENCES `mud_pumpmanufacturer` (`id`);

--
-- Constraints for table `notifications_notification`
--
ALTER TABLE `notifications_notification`
  ADD CONSTRAINT `notifications_notifi_action_object_conten_7d2b8ee9_fk_django_co` FOREIGN KEY (`action_object_content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `notifications_notifi_actor_content_type_i_0c69d7b7_fk_django_co` FOREIGN KEY (`actor_content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `notifications_notifi_recipient_id_d055f3f0_fk_custom_au` FOREIGN KEY (`recipient_id`) REFERENCES `custom_auth_user` (`id`),
  ADD CONSTRAINT `notifications_notifi_target_content_type__ccb24d88_fk_django_co` FOREIGN KEY (`target_content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `pressure_pressure`
--
ALTER TABLE `pressure_pressure`
  ADD CONSTRAINT `pressure_pressure_company_id_f4fa362c_fk_custom_au` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `pressure_pressure_well_id_3d3ea8f1_fk_wells_wells_id` FOREIGN KEY (`well_id`) REFERENCES `wells_wells` (`id`);

--
-- Constraints for table `projects_projectblock`
--
ALTER TABLE `projects_projectblock`
  ADD CONSTRAINT `projects_projectbloc_project_id_c72d553d_fk_projects_` FOREIGN KEY (`project_id`) REFERENCES `projects_projects` (`id`);

--
-- Constraints for table `projects_projectfield`
--
ALTER TABLE `projects_projectfield`
  ADD CONSTRAINT `projects_projectfiel_block_id_859423a2_fk_projects_` FOREIGN KEY (`block_id`) REFERENCES `projects_projectblock` (`id`),
  ADD CONSTRAINT `projects_projectfiel_project_id_69a5535f_fk_projects_` FOREIGN KEY (`project_id`) REFERENCES `projects_projects` (`id`);

--
-- Constraints for table `projects_projects`
--
ALTER TABLE `projects_projects`
  ADD CONSTRAINT `projects_projects_company_id_152710b0_fk_custom_au` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `projects_projects_country_id_6095fc7f_fk_custom_au` FOREIGN KEY (`country_id`) REFERENCES `custom_auth_countries` (`id`),
  ADD CONSTRAINT `projects_projects_created_by_id_c1843844_fk_custom_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `custom_auth_user` (`id`);

--
-- Constraints for table `projects_projectusers`
--
ALTER TABLE `projects_projectusers`
  ADD CONSTRAINT `projects_projectuser_project_id_6f15c346_fk_projects_` FOREIGN KEY (`project_id`) REFERENCES `projects_projects` (`id`),
  ADD CONSTRAINT `projects_projectusers_role_id_5c317385_fk_auth_group_id` FOREIGN KEY (`role_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `projects_projectusers_user_id_aa48835f_fk_custom_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `custom_auth_user` (`id`);

--
-- Constraints for table `rheogram_date`
--
ALTER TABLE `rheogram_date`
  ADD CONSTRAINT `rheogram_date_company_id_e20cd0d9_fk_custom_auth_companies_id` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `rheogram_date_muddata_id_d166d0f5_fk_muddata_muddata_id` FOREIGN KEY (`muddata_id`) REFERENCES `muddata_muddata` (`id`),
  ADD CONSTRAINT `rheogram_date_well_id_8f0a134f_fk_wells_wells_id` FOREIGN KEY (`well_id`) REFERENCES `wells_wells` (`id`),
  ADD CONSTRAINT `rheogram_date_well_phase_id_4d909c11_fk_wellphases_wellphases_id` FOREIGN KEY (`well_phase_id`) REFERENCES `wellphases_wellphases` (`id`);

--
-- Constraints for table `rheogram_sections`
--
ALTER TABLE `rheogram_sections`
  ADD CONSTRAINT `rheogram_sections_rheogram_date_id_9175fc20_fk_rheogram_date_id` FOREIGN KEY (`rheogram_date_id`) REFERENCES `rheogram_date` (`id`),
  ADD CONSTRAINT `rheogram_sections_well_phase_id_29160549_fk_wellphase` FOREIGN KEY (`well_phase_id`) REFERENCES `wellphases_wellphases` (`id`);

--
-- Constraints for table `rights`
--
ALTER TABLE `rights`
  ADD CONSTRAINT `rights_company_id_82151295_fk_custom_auth_companies_id` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `rights_module_id_78eaff8b_fk_modules_id` FOREIGN KEY (`module_id`) REFERENCES `modules` (`id`),
  ADD CONSTRAINT `rights_role_id_59aa8b33_fk_auth_group_id` FOREIGN KEY (`role_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `rig_information`
--
ALTER TABLE `rig_information`
  ADD CONSTRAINT `rig_information_company_id_24757dab_fk_custom_auth_companies_id` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `rig_information_well_id_09e911b9_fk_wells_wells_id` FOREIGN KEY (`well_id`) REFERENCES `wells_wells` (`id`);

--
-- Constraints for table `Sections`
--
ALTER TABLE `Sections`
  ADD CONSTRAINT `Sections_company_id_f1b0f633_fk_custom_auth_companies_id` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `Sections_well_id_709a2c5a_fk_wells_wells_id` FOREIGN KEY (`well_id`) REFERENCES `wells_wells` (`id`),
  ADD CONSTRAINT `Sections_well_phase_id_56fd3f9e_fk_wellphases_wellphases_id` FOREIGN KEY (`well_phase_id`) REFERENCES `wellphases_wellphases` (`id`);

--
-- Constraints for table `surfacepipe_surfacepipe`
--
ALTER TABLE `surfacepipe_surfacepipe`
  ADD CONSTRAINT `surfacepipe_surfacep_company_id_f02b1ecd_fk_custom_au` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `surfacepipe_surfacepipe_well_id_a726c0e6_fk_wells_wells_id` FOREIGN KEY (`well_id`) REFERENCES `wells_wells` (`id`);

--
-- Constraints for table `surfacepipe_surfacepipedata`
--
ALTER TABLE `surfacepipe_surfacepipedata`
  ADD CONSTRAINT `surfacepipe_surfacep_company_id_61aff29a_fk_custom_au` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `surfacepipe_surfacep_surfacepipe_id_238b8769_fk_surfacepi` FOREIGN KEY (`surfacepipe_id`) REFERENCES `surfacepipe_surfacepipe` (`id`),
  ADD CONSTRAINT `surfacepipe_surfacepipedata_well_id_a9114cc2_fk_wells_wells_id` FOREIGN KEY (`well_id`) REFERENCES `wells_wells` (`id`);

--
-- Constraints for table `wellphases_casing`
--
ALTER TABLE `wellphases_casing`
  ADD CONSTRAINT `wellphases_casing_company_id_9d137d8d_fk_custom_au` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`);

--
-- Constraints for table `wellphases_casinggrade`
--
ALTER TABLE `wellphases_casinggrade`
  ADD CONSTRAINT `wellphases_casinggra_company_id_86797a48_fk_custom_au` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`);

--
-- Constraints for table `wellphases_casingrange`
--
ALTER TABLE `wellphases_casingrange`
  ADD CONSTRAINT `wellphases_casingran_company_id_c65a66ed_fk_custom_au` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`);

--
-- Constraints for table `wellphases_wellphases`
--
ALTER TABLE `wellphases_wellphases`
  ADD CONSTRAINT `wellphases_wellphase_casing_type_id_c13c5642_fk_wellphase` FOREIGN KEY (`casing_type_id`) REFERENCES `wellphases_casingtypes` (`id`),
  ADD CONSTRAINT `wellphases_wellphase_company_id_9281c3ac_fk_custom_au` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `wellphases_wellphases_well_id_d1b53bf3_fk_wells_wells_id` FOREIGN KEY (`well_id`) REFERENCES `wells_wells` (`id`);

--
-- Constraints for table `wells_wells`
--
ALTER TABLE `wells_wells`
  ADD CONSTRAINT `wells_wells_block_id_fe91dd24_fk_projects_projectblock_id` FOREIGN KEY (`block_id`) REFERENCES `projects_projectblock` (`id`),
  ADD CONSTRAINT `wells_wells_company_id_9a250b42_fk_custom_auth_companies_id` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `wells_wells_coordinate_system_id_641f4163_fk_wells_coo` FOREIGN KEY (`coordinate_system_id`) REFERENCES `wells_coordinatesystems` (`id`),
  ADD CONSTRAINT `wells_wells_created_by_id_e5790602_fk_custom_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `custom_auth_user` (`id`),
  ADD CONSTRAINT `wells_wells_field_id_6f53d317_fk_projects_projectfield_id` FOREIGN KEY (`field_id`) REFERENCES `projects_projectfield` (`id`),
  ADD CONSTRAINT `wells_wells_plan_well_list_id_f7c5bfff_fk_wells_wells_id` FOREIGN KEY (`plan_well_list_id`) REFERENCES `wells_wells` (`id`),
  ADD CONSTRAINT `wells_wells_project_id_5059cde5_fk_projects_projects_id` FOREIGN KEY (`project_id`) REFERENCES `projects_projects` (`id`),
  ADD CONSTRAINT `wells_wells_projection_id_ad448707_fk_wells_projections_id` FOREIGN KEY (`projection_id`) REFERENCES `wells_projections` (`id`);

--
-- Constraints for table `wells_wellusers`
--
ALTER TABLE `wells_wellusers`
  ADD CONSTRAINT `wells_wellusers_role_id_cb2901c0_fk_auth_group_id` FOREIGN KEY (`role_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `wells_wellusers_user_id_4ce9a5cf_fk_custom_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `custom_auth_user` (`id`),
  ADD CONSTRAINT `wells_wellusers_well_id_58681a0b_fk_wells_wells_id` FOREIGN KEY (`well_id`) REFERENCES `wells_wells` (`id`);

--
-- Constraints for table `welltrajectory_welltrajectory`
--
ALTER TABLE `welltrajectory_welltrajectory`
  ADD CONSTRAINT `welltrajectory_wellt_company_id_b426b736_fk_custom_au` FOREIGN KEY (`company_id`) REFERENCES `custom_auth_companies` (`id`),
  ADD CONSTRAINT `welltrajectory_welltrajectory_well_id_20465038_fk_wells_wells_id` FOREIGN KEY (`well_id`) REFERENCES `wells_wells` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
