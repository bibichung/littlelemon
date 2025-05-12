-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema littlelemon
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema littlelemon
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `littlelemon` DEFAULT CHARACTER SET utf8 ;
USE `littlelemon` ;

-- -----------------------------------------------------
-- Table `littlelemon`.`Customers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `littlelemon`.`Customers` (
  `CustomerID` VARCHAR(45) NOT NULL,
  `CustomerName` VARCHAR(255) NULL,
  `City` VARCHAR(255) NULL,
  `Country` VARCHAR(255) NULL,
  `PostalCode` VARCHAR(45) NULL,
  `CountryCode` VARCHAR(10) NULL,
  PRIMARY KEY (`CustomerID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `littlelemon`.`Bookings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `littlelemon`.`Bookings` (
  `BookingID` VARCHAR(45) NOT NULL,
  `CustomerID` VARCHAR(45) NULL,
  `OrderDate` DATE NULL,
  `DeliveryDate` DATE NULL,
  `DeliveryCost` DECIMAL NULL,
  PRIMARY KEY (`BookingID`),
  INDEX `BookingCustomer_idx` (`CustomerID` ASC) VISIBLE,
  CONSTRAINT `BookingCustomer`
    FOREIGN KEY (`CustomerID`)
    REFERENCES `littlelemon`.`Customers` (`CustomerID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `littlelemon`.`OrderItems`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `littlelemon`.`OrderItems` (
  `OrderItemID` INT NOT NULL AUTO_INCREMENT,
  `BookingID` VARCHAR(45) NULL,
  `CourseName` VARCHAR(255) NULL,
  `CuisineName` VARCHAR(255) NULL,
  `StarterName` VARCHAR(255) NULL,
  `DesertName` VARCHAR(255) NULL,
  `Drink` VARCHAR(255) NULL,
  `Sides` VARCHAR(255) NULL,
  `ItemCost` DECIMAL NULL,
  `ItemSales` DECIMAL NULL,
  `Quantity` INT NULL,
  `Discount` DECIMAL NULL,
  PRIMARY KEY (`OrderItemID`),
  INDEX `OrderItemBooking_idx` (`BookingID` ASC) VISIBLE,
  CONSTRAINT `OrderItemBooking`
    FOREIGN KEY (`BookingID`)
    REFERENCES `littlelemon`.`Bookings` (`BookingID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
