-- MySQL dump 10.13  Distrib 8.0.16, for macos10.14 (x86_64)
--
-- Host: 127.0.0.1    Database: MozobBot
-- ------------------------------------------------------
-- Server version	5.7.25

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Factory`
--

DROP TABLE IF EXISTS `Factory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Factory` (
  `IdFactory` int(11) NOT NULL AUTO_INCREMENT,
  `Author` bigint(18) NOT NULL,
  `Name` text NOT NULL,
  `Product` int(11) NOT NULL,
  PRIMARY KEY (`IdFactory`),
  KEY `fk_Product_Factory_idx` (`Product`),
  CONSTRAINT `fk_Product_Factory` FOREIGN KEY (`Product`) REFERENCES `product` (`idproduct`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Inventory`
--

DROP TABLE IF EXISTS `Inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Inventory` (
  `Owner` bigint(18) NOT NULL,
  `Product` int(11) NOT NULL,
  `Amount` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`Owner`,`Product`),
  KEY `fk_Product_idx` (`Product`),
  CONSTRAINT `fk_Product` FOREIGN KEY (`Product`) REFERENCES `product` (`idproduct`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Market`
--

DROP TABLE IF EXISTS `Market`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Market` (
  `MarketEntryId` int(11) NOT NULL AUTO_INCREMENT,
  `Product` int(11) NOT NULL,
  `Amount` int(11) NOT NULL DEFAULT '0',
  `SellPrice` int(11) NOT NULL DEFAULT '1',
  `BuyPrice` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`MarketEntryId`),
  KEY `fk_Procut_Maket_idx` (`Product`),
  CONSTRAINT `fk_Procut_Maket` FOREIGN KEY (`Product`) REFERENCES `product` (`idproduct`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `NPC`
--

DROP TABLE IF EXISTS `NPC`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `NPC` (
  `IdNPC` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  `Role` int(11) NOT NULL,
  PRIMARY KEY (`IdNPC`),
  KEY `fk_NPC_Role_idx` (`Role`),
  CONSTRAINT `fk_NPC_Role` FOREIGN KEY (`Role`) REFERENCES `npcrole` (`idnpcrole`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `NPCProducts`
--

DROP TABLE IF EXISTS `NPCProducts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `NPCProducts` (
  `NPC` int(11) NOT NULL,
  `Product` int(11) NOT NULL,
  `Amount` varchar(45) NOT NULL DEFAULT '0',
  KEY `fk_NPC_Products_idx` (`NPC`),
  CONSTRAINT `fk_NPC_Products` FOREIGN KEY (`NPC`) REFERENCES `npc` (`IdNPC`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `NPCRole`
--

DROP TABLE IF EXISTS `NPCRole`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `NPCRole` (
  `IdNPCRole` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  PRIMARY KEY (`IdNPCRole`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Product`
--

DROP TABLE IF EXISTS `Product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Product` (
  `IdProduct` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  `Inventor` bigint(18) NOT NULL,
  `Tier` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`IdProduct`,`Name`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  UNIQUE KEY `IdProduct_UNIQUE` (`IdProduct`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-03-12 14:11:51
