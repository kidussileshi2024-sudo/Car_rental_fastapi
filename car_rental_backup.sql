-- MySQL dump 10.13  Distrib 9.6.0, for macos26.4 (arm64)
--
-- Host: localhost    Database: Car_Rental_original
-- ------------------------------------------------------
-- Server version	9.6.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '8fef7e06-5b71-11f1-bdaa-56838c366b74:1-965';

--
-- Table structure for table `Booking`
--

DROP TABLE IF EXISTS `Booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking` (
  `B_id` int NOT NULL AUTO_INCREMENT,
  `Cu_id` int NOT NULL,
  `Car_id` int NOT NULL,
  `Start_date` date NOT NULL,
  `End_date` date DEFAULT NULL,
  `Emp_id` int NOT NULL,
  PRIMARY KEY (`B_id`),
  KEY `FK_Car_id` (`Car_id`),
  KEY `Fk_user_id` (`Cu_id`),
  KEY `Fk_user` (`Emp_id`),
  CONSTRAINT `FK_Car_id` FOREIGN KEY (`Car_id`) REFERENCES `Cars` (`C_id`),
  CONSTRAINT `Fk_user` FOREIGN KEY (`Emp_id`) REFERENCES `Employees` (`Emp_id`),
  CONSTRAINT `Fk_user_id` FOREIGN KEY (`Cu_id`) REFERENCES `Customers` (`C_id`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking`
--

LOCK TABLES `Booking` WRITE;
/*!40000 ALTER TABLE `Booking` DISABLE KEYS */;
INSERT INTO `Booking` VALUES (5,1,1,'2026-02-06','2026-06-03',3),(6,2,20,'2026-02-06','2026-06-03',10),(7,4,24,'2026-02-06','2026-06-03',12),(8,2,10,'2026-02-07','2026-06-03',2),(10,2,20,'2026-02-07','2026-06-03',7),(11,5,4,'2026-02-07','2026-06-03',2),(12,4,16,'2026-02-07','2026-06-03',2),(13,7,12,'2026-02-07','2026-06-03',12),(14,2,11,'2026-02-07','2026-06-03',7),(15,8,19,'2026-02-07','2026-06-03',2),(16,4,23,'2026-02-07','2026-06-03',7),(17,12,4,'2026-02-07','2026-06-03',2),(18,15,13,'2026-02-07','2026-06-03',2),(19,2,3,'2026-02-07','2026-06-03',12),(20,2,6,'2026-02-07','2026-06-03',12),(21,2,7,'2026-02-07','2026-06-03',2),(22,16,13,'2026-02-07','2026-06-03',2),(23,17,3,'2026-02-08','2026-06-03',12),(24,2,25,'2026-02-08','2026-06-03',2),(27,20,1,'2026-02-08','2026-06-03',2),(28,21,25,'2026-02-08','2026-06-03',2),(29,21,2,'2026-02-08','2026-06-03',7),(30,2,10,'2026-02-09','2026-06-03',2),(31,2,10,'2026-02-09','2026-06-03',2),(32,22,13,'2026-02-09','2026-06-03',2),(33,23,3,'2026-02-09','2026-06-03',12),(34,24,10,'2026-02-09','2026-06-03',2),(35,25,7,'2026-02-09','2026-06-03',2),(36,26,11,'2026-02-09','2026-06-03',7),(37,26,7,'2026-02-09','2026-06-03',2),(38,27,24,'2026-02-09','2026-06-03',12),(39,2,13,'2026-02-09','2026-06-03',2),(40,7,13,'2026-02-09','2026-06-03',2),(41,13,11,'2026-02-09','2026-06-03',7),(42,2,22,'2026-02-10','2026-06-03',2),(43,18,6,'2026-02-10','2026-06-03',12),(44,28,12,'2026-02-10','2026-06-03',12),(45,2,15,'2026-02-11','2026-06-03',12),(46,29,5,'2026-02-11','2026-06-03',7),(47,32,21,'2026-02-11','2026-06-03',12),(48,2,16,'2026-02-11','2026-06-03',2),(49,33,13,'2026-02-11','2026-06-03',2),(50,34,8,'2026-02-11','2026-06-03',7),(51,35,12,'2026-02-11','2026-06-03',12),(52,2,16,'2026-02-11','2026-06-03',2),(53,36,24,'2026-02-11','2026-06-03',12),(54,2,21,'2026-02-11','2026-06-03',12),(55,2,1,'2026-02-11','2026-06-03',2),(56,37,3,'2026-02-11','2026-06-03',12),(57,38,2,'2026-02-11','2026-06-03',7),(58,4,20,'2026-03-07','2026-06-03',7),(59,40,21,'2026-05-01','2026-06-03',12),(60,41,22,'2026-05-01','2026-06-03',2),(61,2,1,'2026-06-03','2026-06-03',2),(62,1,1,'2026-10-07','2026-10-07',2),(63,1,2,'2026-10-08','2026-10-08',3),(64,1,3,'2026-10-08','2026-10-08',3),(65,1,5,'2026-10-08','2026-10-08',3);
/*!40000 ALTER TABLE `Booking` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `double booking` BEFORE INSERT ON `booking` FOR EACH ROW IF EXISTS (
  SELECT 1 
  FROM Booking 
  WHERE Cu_id = NEW.cu_id 
    AND Car_id = NEW.Car_id 
    AND End_date IS NULL
) THEN
  SIGNAL SQLSTATE '45000' 
  SET MESSAGE_TEXT = 'Car already rented by this customer.';
END IF */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `Branch`
--

DROP TABLE IF EXISTS `Branch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Branch` (
  `B_id` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `Phone_No` varchar(11) COLLATE utf8mb4_general_ci NOT NULL,
  `Address` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`B_id`),
  UNIQUE KEY `Name` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='where customers and cars are found ';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Branch`
--

LOCK TABLES `Branch` WRITE;
/*!40000 ALTER TABLE `Branch` DISABLE KEYS */;
INSERT INTO `Branch` VALUES (1,'Dire Dawa','293848572','Sabian_10 3000'),(2,'Addis Ababa','39842093','bole_82 2000'),(3,'Messina','8389283','via Francesco Basile 98158');
/*!40000 ALTER TABLE `Branch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Cars`
--

DROP TABLE IF EXISTS `Cars`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Cars` (
  `C_id` int NOT NULL AUTO_INCREMENT,
  `Plate_no` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Price_adjs` decimal(10,2) DEFAULT '0.00' COMMENT 'to adjust the price that come form model based on the specific car condition \r\n',
  `Model_id` int NOT NULL,
  `Branch_id` int NOT NULL,
  `Color` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `IS_available` tinyint(1) NOT NULL,
  PRIMARY KEY (`C_id`),
  UNIQUE KEY `Plate_no` (`Plate_no`),
  KEY `FK_Branch` (`Branch_id`),
  KEY `FK_Models` (`Model_id`),
  CONSTRAINT `FK_Branch` FOREIGN KEY (`Branch_id`) REFERENCES `Branch` (`B_id`),
  CONSTRAINT `FK_Models` FOREIGN KEY (`Model_id`) REFERENCES `Models` (`M_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cars`
--

LOCK TABLES `Cars` WRITE;
/*!40000 ALTER TABLE `Cars` DISABLE KEYS */;
INSERT INTO `Cars` VALUES (1,'AB123CD',0.10,1,1,'White',0),(2,'AB124CD',0.00,1,2,'Silver',0),(3,'AB125CD',0.10,1,3,'Black',0),(4,'BM201AA',0.15,2,1,'Red',0),(5,'BM202AA',0.00,2,2,'Blue',0),(6,'BM203AA',0.00,2,3,'White',0),(7,'TS301EV',0.10,3,1,'Red',0),(8,'TS302EV',0.01,3,2,'White',1),(9,'TS303EV',0.00,3,3,'Grey',0),(10,'FD401DD',0.02,4,1,'Blue',0),(11,'FD402DD',0.15,4,2,'Black',1),(12,'FD403DD',0.01,4,3,'White',0),(13,'AU501ZZ',0.05,5,1,'Black',0),(14,'AU502ZZ',0.00,5,2,'Grey',0),(15,'AU503ZZ',0.06,5,3,'White',0),(16,'TY901GH',0.00,1,1,'Blue',0),(17,'BM777KK',0.12,2,2,'Grey',1),(18,'TS909EV',0.00,3,3,'Black',0),(19,'FD888LL',0.09,4,1,'Red',1),(20,'AU606MM',0.00,5,2,'Silver',1),(21,'YA101EC',0.02,6,3,'White',0),(22,'YA102EC',0.50,6,1,'Blue',1),(23,'HY701SU',0.04,7,2,'Grey',1),(24,'HY702SU',0.01,7,3,'Black',1),(25,'TS404EV',0.50,4,1,'White',1);
/*!40000 ALTER TABLE `Cars` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Category`
--

DROP TABLE IF EXISTS `Category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Category` (
  `C_id` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `Description` varchar(500) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`C_id`),
  UNIQUE KEY `Name` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='the customer see based on this category ';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Category`
--

LOCK TABLES `Category` WRITE;
/*!40000 ALTER TABLE `Category` DISABLE KEYS */;
INSERT INTO `Category` VALUES (1,'Economy','Affordable cars with low running costs, suitable for daily commuting and short trips.'),(2,'Compact','Small to mid-size cars offering a balance between efficiency and comfort.'),(3,'Sedan','Comfortable cars with more space, ideal for long-distance and business travel.'),(4,'SUV','Sport utility vehicles with higher seating and larger cargo capacity, suitable for families and rough terrain.'),(5,'Luxury','Premium vehicles with high comfort, advanced features, and superior performance.');
/*!40000 ALTER TABLE `Category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Customers`
--

DROP TABLE IF EXISTS `Customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Customers` (
  `C_id` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `Address` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `License_num` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `Age` int DEFAULT NULL,
  `Phone_no` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`C_id`),
  UNIQUE KEY `License_num` (`License_num`),
  UNIQUE KEY `Phone_on` (`Phone_no`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='This is the customer table with user info ';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Customers`
--

LOCK TABLES `Customers` WRITE;
/*!40000 ALTER TABLE `Customers` DISABLE KEYS */;
INSERT INTO `Customers` VALUES (1,'fikir adem','francesco basile','20393',21,'73838373'),(2,'Chapi ','dire','93728',23,'0948635120'),(4,'yisak ','sebategna','729283',24,'0934306038'),(5,'amde birhan','francesco ','1324567',25,'45678921'),(7,'konjit','direfa','793792',30,'0915753592'),(8,'Amdebirhan Workeye Abebe','Via Feacessico Basil','1231',23,'3935134257'),(10,'Amdebirhan Workeye Abebe ','Via Fracessico ','1234',23,'321412341234'),(11,'Amdebirhan Wokreye Abebe','Via Fracesico Bassil','132356',23,'393513425737'),(12,'addis sileshi','dkire dawa ','735894',53,'0915730989'),(13,'elfazm','dkoi','83742j',24,'0948118181'),(15,'markot','sebta','83y57',25,'0973899880'),(16,'kia ps king','kldif','374929',45,'1234567890'),(17,'alazar ','tuludimtu','3749293874',21,'0919328812'),(18,'somet','jkshdg','374938',43,'0987654321'),(20,'jlkgcd','asldgh','2346588',74,'2345'),(21,'sileshi','aldfh','7479323',21,'090909'),(22,'fikir adem mohammed ','skdhgi','8743892',22,'09876543211'),(23,'jam ','franche','37492938744',42,'3514199631'),(24,'seweyew ','harar','84923',24,'678905'),(25,'surafel','buaganza','374829745',24,'3514062506'),(26,'dagi man','via francesoc','784239',30,'87654321'),(27,'adoni','akhdgi','364292',21,'23456789'),(28,'asdfghj','messina ','1290209',20,'0912091209'),(29,'miki','gendekore','384203',23,'234567890'),(32,'mama','akdhadhfu83','938423082L',18,'4567890'),(33,'Nahom','ras agez','93842033',24,'0949841399'),(34,'Nahom','annuziata','74938294T',24,'3524610640'),(35,'mercy','jadhife','72837khdd',18,'3514103831'),(36,'Roba','annuxizta','9843509A',23,'567890'),(37,'Nanbon ','annuxi','8239249i',23,'3565'),(38,'napoli ','messina','83749208',23,'52537563'),(40,'99','99','3344',16,'0922'),(41,'dd','ff','dik8jny',23,'88'),(42,'jhon','war','dhosd',93,'3893948345');
/*!40000 ALTER TABLE `Customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Employee_Maintenance`
--

DROP TABLE IF EXISTS `Employee_Maintenance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Employee_Maintenance` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Emp_Id` int NOT NULL,
  `Ment_id` int NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `maintenance_fk` (`Ment_id`),
  KEY `emp_fk` (`Emp_Id`),
  CONSTRAINT `emp_fk` FOREIGN KEY (`Emp_Id`) REFERENCES `Employees` (`Emp_id`),
  CONSTRAINT `maintenance_fk` FOREIGN KEY (`Ment_id`) REFERENCES `Maintenance` (`M_id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Employee_Maintenance`
--

LOCK TABLES `Employee_Maintenance` WRITE;
/*!40000 ALTER TABLE `Employee_Maintenance` DISABLE KEYS */;
INSERT INTO `Employee_Maintenance` VALUES (1,13,1),(2,14,1),(4,14,2),(5,15,2),(6,8,3),(7,10,3),(8,3,13),(9,4,13),(10,4,14),(11,5,14),(12,4,10),(13,14,4),(14,15,4),(15,5,21),(16,4,23),(17,5,23),(18,4,22),(19,5,22),(20,3,25),(21,5,25),(22,9,26),(23,10,26),(24,14,27),(25,15,27),(26,14,27),(27,15,27),(28,4,11),(29,5,11),(30,9,12),(31,10,12),(32,9,12),(33,10,12),(34,9,12),(35,10,12),(36,9,12),(37,10,12),(38,4,17),(39,5,17),(40,4,17),(41,5,17),(42,14,32),(43,15,32),(44,9,29),(45,10,29),(46,3,16),(47,4,16),(48,5,16),(49,3,33);
/*!40000 ALTER TABLE `Employee_Maintenance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Employees`
--

DROP TABLE IF EXISTS `Employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Employees` (
  `Emp_id` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  `B_id` int NOT NULL,
  `Role` enum('Manager','Mechanic','Receptionist') COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`Emp_id`),
  KEY `B_id` (`B_id`),
  CONSTRAINT `employees_ibfk_1` FOREIGN KEY (`B_id`) REFERENCES `Branch` (`B_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='employees of the company ';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Employees`
--

LOCK TABLES `Employees` WRITE;
/*!40000 ALTER TABLE `Employees` DISABLE KEYS */;
INSERT INTO `Employees` VALUES (1,'Kidus Addis',1,'Manager'),(2,'Marco Bianchi',1,'Receptionist'),(3,'Paolo Conti',1,'Mechanic'),(4,'Davide Greco',1,'Mechanic'),(5,'Andrea Romano',1,'Mechanic'),(6,'Degelaw',2,'Manager'),(7,'Stefano Moretti',2,'Receptionist'),(8,'Matteo Gallo',2,'Mechanic'),(9,'Simone Ferri',2,'Mechanic'),(10,'Alessandro Riva',2,'Mechanic'),(11,'Pupusha',3,'Manager'),(12,'Riccardo Sala',3,'Receptionist'),(13,'Lorenzo Villa',3,'Mechanic'),(14,'Nicola Marchetti',3,'Mechanic'),(15,'Fabio De Luca',3,'Mechanic');
/*!40000 ALTER TABLE `Employees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Inspection`
--

DROP TABLE IF EXISTS `Inspection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Inspection` (
  `I_id` int NOT NULL AUTO_INCREMENT,
  `Car_id` int NOT NULL,
  `Em_id` int DEFAULT NULL,
  `Book_id` int NOT NULL,
  `date` date NOT NULL,
  `Damages` varchar(300) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Fine` float DEFAULT NULL,
  `Inspection_done` tinyint(1) NOT NULL,
  PRIMARY KEY (`I_id`),
  UNIQUE KEY `book_unique` (`Book_id`),
  KEY `FK_Emp_` (`Em_id`),
  CONSTRAINT `FK_Emp_` FOREIGN KEY (`Em_id`) REFERENCES `Employees` (`Emp_id`),
  CONSTRAINT `inspection_ibfk_1` FOREIGN KEY (`Book_id`) REFERENCES `Booking` (`B_id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Inspection`
--

LOCK TABLES `Inspection` WRITE;
/*!40000 ALTER TABLE `Inspection` DISABLE KEYS */;
INSERT INTO `Inspection` VALUES (1,20,3,6,'2026-02-07','good',0,1),(3,24,13,7,'2026-02-07','head lights not working',20,1),(6,10,3,8,'2026-02-07','wind shield',40,1),(12,20,3,10,'2026-02-07','all good ',0,1),(13,4,3,11,'2026-02-07','all good ',0,1),(14,16,3,12,'2026-02-07','scratched ',10,1),(15,12,13,13,'2026-02-07','all good',0,1),(16,11,8,14,'2026-02-07','good ',0,1),(17,19,3,15,'2026-02-07','no',0,1),(18,23,8,16,'2026-02-07','no head light ',25,1),(19,13,3,18,'2026-02-07','every thing good ',0,1),(20,3,13,19,'2026-02-07','good',0,1),(21,6,13,20,'2026-02-07','good ',0,1),(22,13,3,22,'2026-02-07','good',0,1),(23,3,13,23,'2026-02-08','good ',0,1),(24,25,3,24,'2026-02-08','good ',0,1),(25,1,3,5,'2026-02-08','all good ',0,1),(26,7,8,21,'2026-02-08','dirty ',13,1),(28,25,3,28,'2026-02-08','no spochioo',50,1),(29,2,8,29,'2026-02-08','good ',0,1),(30,10,3,30,'2026-02-09','bad shape',200,1),(31,10,3,31,'2026-02-09','dirty ',20,1),(32,13,3,32,'2026-02-09','spochioo bad ',500,1),(33,3,13,33,'2026-02-09','head light ',13,1),(34,7,3,35,'2026-02-09','spocchio',45,1),(35,11,8,36,'2026-02-09','head high ',45,1),(36,24,13,38,'2026-02-09','wind shield ',60,1),(37,13,3,39,'2026-02-09','good',0,1),(38,13,3,40,'2026-02-09','all fine',0,1),(39,11,8,41,'2026-02-09','some damage on ht evade',60,1),(40,12,3,44,'2026-02-10','no',0,1),(41,5,8,46,'2026-02-11','bad sets ',35,1),(42,21,3,47,'2026-02-11','all good',0,1),(43,16,3,48,'2026-02-11','all god',0,1),(44,13,3,49,'2026-02-11','all good ',0,1),(45,8,8,50,'2026-02-11','All good',0,1),(46,12,8,51,'2026-02-11','head light ',200,1),(47,16,3,52,'2026-02-11','bad condition ',50,1),(48,24,8,53,'2026-02-11','All good ',0,1),(49,21,13,54,'2026-02-11','bad',15,1),(50,3,8,56,'2026-02-11','',0,1),(51,2,8,57,'2026-02-11','good',0,1),(52,20,3,58,'2026-03-07','',0,1),(53,22,3,60,'2026-05-01','fghhh',20,1),(54,1,3,61,'2026-06-03','good',0,1),(55,3,NULL,64,'2026-10-08',NULL,NULL,0),(56,5,NULL,65,'2026-10-08',NULL,NULL,0);
/*!40000 ALTER TABLE `Inspection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Maintenance`
--

DROP TABLE IF EXISTS `Maintenance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Maintenance` (
  `M_id` int NOT NULL AUTO_INCREMENT,
  `Car_id` int NOT NULL,
  `Start_date` date NOT NULL,
  `End_date` date DEFAULT NULL,
  `Description` varchar(300) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`M_id`),
  KEY `FK_CAR` (`Car_id`),
  CONSTRAINT `FK_CAR` FOREIGN KEY (`Car_id`) REFERENCES `Cars` (`C_id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='a car might be on maintenance service';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Maintenance`
--

LOCK TABLES `Maintenance` WRITE;
/*!40000 ALTER TABLE `Maintenance` DISABLE KEYS */;
INSERT INTO `Maintenance` VALUES (1,9,'2026-02-01',NULL,'some thing happened'),(2,18,'2026-01-30',NULL,'working on it '),(3,14,'2026-02-02',NULL,NULL),(4,24,'2026-02-07','2026-02-08','good '),(10,10,'2026-02-07','2026-02-08','all fine now '),(11,16,'2026-02-07','2026-02-10','good '),(12,23,'2026-02-07','2026-02-11','all good '),(13,7,'2026-02-08','2026-02-08','all fixed '),(14,7,'2026-02-08','2026-02-08','All Good'),(16,25,'2026-02-08','2026-03-07',''),(17,25,'2026-02-08','2026-02-11',''),(21,10,'2026-02-09','2026-02-09','all done '),(22,10,'2026-02-09','2026-02-09','good '),(23,13,'2026-02-09','2026-02-09','all good'),(24,3,'2026-02-09',NULL,'Damage from inspection'),(25,7,'2026-02-09','2026-02-09','all good '),(26,11,'2026-02-09','2026-02-09','all good '),(27,24,'2026-02-09','2026-02-09','akk giid '),(28,11,'2026-02-09',NULL,'Damage from inspection'),(29,5,'2026-02-11','2026-02-11','GOOD'),(30,12,'2026-02-11',NULL,'Damage from inspection'),(31,16,'2026-02-11',NULL,'Damage from inspection: bad condition '),(32,21,'2026-02-11','2026-02-11','now fine'),(33,22,'2026-05-01','2026-05-01','fab');
/*!40000 ALTER TABLE `Maintenance` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `id_enddate` BEFORE INSERT ON `maintenance` FOR EACH ROW BEGIN
    IF EXISTS (
        SELECT 1
        FROM maintenance
        WHERE Car_id = NEW.Car_id
          AND End_date IS NULL
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot create new record: this car already has an open entry (End_date is NULL)';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `Models`
--

DROP TABLE IF EXISTS `Models`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Models` (
  `M_id` int NOT NULL AUTO_INCREMENT,
  `Brand` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  `Name` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `Price_per_day` float NOT NULL COMMENT 'This is the base price for all cars of this model \r\n',
  `Fule_type` varchar(11) COLLATE utf8mb4_general_ci NOT NULL,
  `Cat_id` int NOT NULL,
  PRIMARY KEY (`M_id`),
  KEY `FK_cat` (`Cat_id`),
  CONSTRAINT `FK_cat` FOREIGN KEY (`Cat_id`) REFERENCES `Category` (`C_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='description about cars models';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Models`
--

LOCK TABLES `Models` WRITE;
/*!40000 ALTER TABLE `Models` DISABLE KEYS */;
INSERT INTO `Models` VALUES (1,'Toyota','Corolla',45,'Petrol',2),(2,'BMW','320i',85,'Petrol',3),(3,'Tesla','Model 3',110,'Electric',3),(4,'Ford','Focus',50,'Diesel',2),(5,'Audi','A6',95,'Diesel',5),(6,'Toyota','Yaris',35,'Petrol',1),(7,'Hyundai','Tucson',75,'Hybrid',4);
/*!40000 ALTER TABLE `Models` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Payment`
--

DROP TABLE IF EXISTS `Payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Payment` (
  `P_id` int NOT NULL AUTO_INCREMENT,
  `B_id` int NOT NULL,
  `Method` varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Amount` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `Type` enum('Booking','Fine') COLLATE utf8mb4_general_ci NOT NULL COMMENT 'weather the payment come form booking or Inspection fine',
  `Emp_id` int NOT NULL,
  `Invoice` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`P_id`),
  UNIQUE KEY `unique_invoice` (`Invoice`),
  KEY `FK_employee` (`Emp_id`),
  KEY `FK_booking` (`B_id`),
  CONSTRAINT `FK_booking` FOREIGN KEY (`B_id`) REFERENCES `Booking` (`B_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_employee` FOREIGN KEY (`Emp_id`) REFERENCES `Employees` (`Emp_id`)
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='this is all the records of payments to the company ';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Payment`
--

LOCK TABLES `Payment` WRITE;
/*!40000 ALTER TABLE `Payment` DISABLE KEYS */;
INSERT INTO `Payment` VALUES (5,5,'Cash','40.5','Booking',3,'83j9o202js'),(6,6,'Cash','95','Booking',10,'jei93h92jdd'),(7,7,'Cash','74.25','Booking',12,'jeih82742'),(15,7,'Cash','20','Fine',2,'38ifji3914'),(16,8,'Cash','50','Booking',2,'8ji93jjjffs'),(18,10,'Cash','95','Booking',7,'ieon38uds'),(19,8,'Cash','40','Fine',2,'hdsote8374'),(20,11,'Cash','72.25','Booking',2,'ajhidne736f'),(21,12,'Card','45','Booking',2,'jlkadhfo3793'),(22,12,'Cash','10','Fine',2,'9djk7djks'),(23,13,'Cash','49.5','Booking',12,'ldfhe839'),(24,14,'Cash','46','Booking',7,'sdahoah8374h'),(25,15,'Cash','45.5','Booking',2,'Invoic'),(26,16,'Cash','72','Booking',7,'dhsoeiu7264'),(27,16,'Card','25','Fine',7,'kadhf872494'),(28,17,'Cash','72.25','Booking',2,'skdhf'),(29,18,'Cash','92.15','Booking',2,'dklsah8349'),(30,19,'Cash','40.5','Booking',12,'Invoice'),(31,20,'Cash','85','Booking',12,'kaldshoei84792'),(32,21,'Cash','104.5','Booking',2,'djahei8'),(33,22,'Cash','92.15','Booking',2,'ajfhue3764'),(34,23,'Cash','40.5','Booking',12,'djayr88923'),(35,24,'Cash','44','Booking',2,'886t54'),(36,5,'Cash','81','Booking',2,'jdhgidal847'),(37,21,'Cash','104.5','Booking',7,'ljdkha984394'),(41,24,'Cash','44','Booking',2,'dshi83743'),(42,28,'Card','44','Booking',2,'ksdlhg874'),(43,28,'Card','50','Fine',2,'adhfi8748'),(44,29,'Cash','45','Booking',7,'dsjh8743847'),(45,30,'Card','49.5','Booking',2,'fdlkhgdoi83'),(46,30,'Card','200','Fine',2,'dfiejfure72'),(47,31,'Cash','49.5','Booking',2,'fkjhdif8273'),(48,31,'Cash','20','Fine',2,'ehreriu874'),(49,32,'Cash','92.15','Booking',2,'aldhfdkhkd3764'),(50,32,'Cash','500','Fine',2,'dlhfi8374'),(51,33,'Cash','40.5','Booking',12,'dlkhfih734'),(52,33,'Cash','13','Fine',12,'hfei493'),(53,35,'Card','104.5','Booking',2,'jkdhieu82734'),(54,35,'Cash','45','Fine',2,'djhfie8723'),(55,36,'Cash','46','Booking',7,'aodgy873h83u'),(56,36,'Card','45','Fine',7,'adkfjeiu7284'),(57,38,'Cash','74.25','Booking',12,'dkahfiei7493'),(58,38,'Card','60','Fine',12,'kldfheoeiwo'),(59,39,'Cash','90.25','Booking',2,'ldfjk9823'),(60,40,'Cash','90.25','Booking',2,'kdahf9283'),(61,41,'Cash','42.5','Booking',7,'3499rhijsjdsiw'),(62,41,'Cash','60','Fine',7,'3u4938hf4h74f'),(63,44,'Cash','49.5','Booking',2,'d0vkop'),(64,46,'Card','85','Booking',7,'hjsodihsk82'),(65,46,'Card','35','Fine',7,'akdhfie768'),(66,47,'Cash','34.3','Booking',2,'dklfhoak37432'),(67,48,'Cash','45','Booking',2,'adjfhhiifu78329'),(68,50,'Card','108.9','Booking',7,'kdshafkd743749'),(69,51,'Card','49.5','Booking',7,'kldhsflkehri799833'),(70,51,'Cash','200','Fine',7,'hjdhfhksk'),(71,52,'Cash','45','Booking',2,'djlfh34394'),(72,52,'Cash','50','Fine',2,'oeroi3749u49'),(73,53,'Cash','74.25','Booking',7,'jkdhfgeu874'),(74,54,'Cash','34.3','Booking',12,'akfhhfiu34u89'),(75,54,'Cash','15','Fine',12,'dfheri48898328'),(76,56,'Cash','40.5','Booking',7,'hgiufuyyvhur'),(77,57,'Card','45','Booking',7,'dofhlahoei'),(78,58,'Cash','95','Booking',2,'okay'),(79,60,'Cash','35','Booking',2,'u7jouyy'),(80,60,'Cash','20','Fine',2,'ikuyt'),(81,61,'Cash','40.5','Booking',2,'ehfejifjojs');
/*!40000 ALTER TABLE `Payment` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-11 17:49:42
