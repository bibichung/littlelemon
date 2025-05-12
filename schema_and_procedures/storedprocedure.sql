USE `littlelemon`;
DROP procedure IF EXISTS `GetMaxQuantity`;

DELIMITER $$
USE `littlelemon`$$
CREATE PROCEDURE `GetMaxQuantity` ()
BEGIN
	SELECT MAX(Quantity) AS MaxQuantity FROM OrderItems;
END$$

CREATE PROCEDURE AddBooking(
    IN newBookingID VARCHAR(255),
    IN newOrderDate DATE,
    IN newDeliveryDate DATE,
    IN newCustomerID VARCHAR(255),
    IN newDeliveryCost DECIMAL(10,2)
)
BEGIN
    INSERT INTO Bookings (BookingID, OrderDate, DeliveryDate, CustomerID, DeliveryCost)
    VALUES (newBookingID, newOrderDate, newDeliveryDate, newCustomerID, newDeliveryCost);
    SELECT CONCAT('Booking ', newBookingID, ' added successfully.') AS Status;
END$$

CREATE PROCEDURE UpdateBooking(
    IN targetBookingID VARCHAR(255),
    IN newDeliveryDate DATE
)
BEGIN
    UPDATE Bookings
    SET DeliveryDate = newDeliveryDate
    WHERE BookingID = targetBookingID;
    -- Check if the update was successful
    IF ROW_COUNT() > 0 THEN
        SELECT CONCAT('Booking ', targetBookingID, ' updated successfully.') AS Status;
    ELSE
        SELECT CONCAT('Booking ', targetBookingID, ' not found or no changes made.') AS Status;
    END IF;
END$$

CREATE PROCEDURE CancelBooking(
    IN targetBookingID VARCHAR(255)
)
BEGIN
    DELETE FROM Bookings WHERE BookingID = targetBookingID;
    -- Check if the delete was successful
    IF ROW_COUNT() > 0 THEN
        SELECT CONCAT('Booking ', targetBookingID, ' canceled successfully.') AS Status;
    ELSE
        SELECT CONCAT('Booking ', targetBookingID, ' not found.') AS Status;
    END IF;
END$$

CREATE PROCEDURE ManageBooking(
    IN targetBookingID VARCHAR(255)
)
BEGIN
    -- Select booking details
    SELECT * FROM Bookings WHERE BookingID = targetBookingID;
    -- Select associated order items
    SELECT * FROM OrderItems WHERE BookingID = targetBookingID;
END$$

DELIMITER ;


