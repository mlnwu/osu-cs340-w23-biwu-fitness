/* 
 * Group 106
 * Members: Mia Bilka & Maggie Wu
 */

SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;

--
-- CREATE TABLES
--

CREATE OR REPLACE TABLE Members(
    member_id int(10) AUTO_INCREMENT UNIQUE NOT NULL,
    first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL,
    tier_type ENUM('standard', 'premium') NOT NULL,
    phone_number varchar(10) NOT NULL,
    email varchar(100) NOT NULL,
    PRIMARY KEY (member_id)
);

CREATE OR REPLACE TABLE Transactions(
    transaction_id int(10) AUTO_INCREMENT UNIQUE NOT NULL,
    members_member_id int(10) NOT NULL,
    transaction_amount decimal(15,2) NOT NULL,
    transaction_date DATE NOT NULL,
    PRIMARY KEY (transaction_id),
    FOREIGN KEY (members_member_id) REFERENCES Members(member_id) ON DELETE CASCADE
);

CREATE OR REPLACE TABLE Members_has_Transactions(
    transactions_transaction_id int(10) NOT NULL,
    members_member_id int(10) NOT NULL,
    FOREIGN KEY (transactions_transaction_id) REFERENCES Transactions(transaction_id) ON DELETE CASCADE,
    FOREIGN KEY (members_member_id) REFERENCES Members(member_id) ON DELETE CASCADE
);

CREATE OR REPLACE TABLE Trainers(
    trainer_id int(10) AUTO_INCREMENT UNIQUE NOT NULL,
    first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL,
    phone_number varchar(10) NOT NULL,
    email varchar(100) NOT NULL,
    PRIMARY KEY (trainer_id)
);

CREATE OR REPLACE TABLE Classes(
    class_id int(10) AUTO_INCREMENT UNIQUE NOT NULL,
    class_type varchar(50) NOT NULL,
    trainer_id int(10) NULL,
    day_scheduled ENUM('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday') NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    PRIMARY KEY (class_id),
    FOREIGN KEY (trainer_id) REFERENCES Trainers(trainer_id) ON DELETE CASCADE
);

CREATE OR REPLACE TABLE Classes_has_Members(
    classes_class_id int(10) NOT NULL,
    members_member_id int(10) NOT NULL,
    FOREIGN KEY (classes_class_id) REFERENCES Classes(class_id) ON DELETE CASCADE,
    FOREIGN KEY (members_member_id) REFERENCES Members(member_id) ON DELETE CASCADE
);

--
-- INSERT SAMPLE DATA
--

INSERT INTO Members (first_name, last_name, tier_type, phone_number, email)
    VALUES
        ('Katherine', 'Gonzales', 'standard', '5551234567', 'katherinegonzales@example.com'),
        ('Myla', 'Chen', 'premium', '5557654321', 'mylachen@example.com'),
        ('Tom', 'Barber', 'standard', '5551237654', 'tombarber@example.com'),
        ('Michael', 'McDonald', 'standard', '5551234123', 'michaelmcdonald@example.com');


-- Update transactions + Members_has_Transactions simultaneously to keep track of most recent Transactions id
INSERT INTO Transactions(transaction_amount, transaction_date)
    VALUES
        (40.00, '2022-07-01');
INSERT INTO Members_has_Transactions(members_member_id, transactions_transaction_id)
    VALUES
        ((SELECT member_id FROM Members WHERE first_name = 'Katherine' AND last_name = 'Gonzales'), LAST_INSERT_ID());

INSERT INTO Transactions(transaction_amount, transaction_date)
    VALUES
        (50.00, '2022-08-01');
INSERT INTO Members_has_Transactions(members_member_id, transactions_transaction_id)
    VALUES
        ((SELECT member_id FROM Members WHERE first_name = 'Myla' AND last_name = 'Chen'), LAST_INSERT_ID());

INSERT INTO Transactions(transaction_amount, transaction_date)
    VALUES
        (40.00, '2023-01-01');
INSERT INTO Members_has_Transactions(members_member_id, transactions_transaction_id)
    VALUES
        ((SELECT member_id FROM Members WHERE first_name = 'Tom' AND last_name = 'Barber'), LAST_INSERT_ID());

INSERT INTO Transactions(transaction_amount, transaction_date)
    VALUES
        (40.00, '2022-02-01');
INSERT INTO Members_has_Transactions(members_member_id, transactions_transaction_id)
    VALUES
        ((SELECT member_id FROM Members WHERE first_name = 'Michael' AND last_name = 'McDonald'), LAST_INSERT_ID());

INSERT INTO Trainers(first_name, last_name, phone_number, email)
    VALUES
        ('Sandra', 'Williams', '5550000000', 'sandrawilliams@example.com'),
        ('Garrett', 'Norton', '5551234543', 'garrettnorton@example.com'),
        ('Julia', 'Fuertes', '5551234123', 'juliafuertes@example.com');

INSERT INTO Classes(class_type, trainer_id, day_scheduled, start_time, end_time)
    VALUES
        ('weight training', (SELECT trainer_id FROM Trainers WHERE first_name = 'Sandra' AND last_name = 'Williams'), 'Monday', '14:30:00', '15:30:00'),
        ('cardio', (SELECT trainer_id FROM Trainers WHERE first_name = 'Garrett' AND last_name = 'Norton'), 'Saturday', '10:30:00', '12:00:00'),
        ('yoga', (SELECT trainer_id FROM Trainers WHERE first_name = 'Julia' AND last_name = 'Fuertes'), 'Sunday', '08:30:00', '09:45:00');

INSERT INTO Classes_has_Members(Classes_class_id, Members_member_id)
    VALUES
        ((SELECT class_id FROM Classes WHERE class_type = 'yoga' AND day_scheduled = 'Sunday' AND start_time = '08:30:00' AND end_time = '09:45:00'), (SELECT member_id FROM Members WHERE first_name = 'Katherine' AND last_name = 'Gonzales')),
        ((SELECT class_id FROM Classes WHERE class_type = 'cardio' AND day_scheduled = 'Saturday' AND start_time = '10:30:00' AND end_time = '12:00:00'), (SELECT member_id FROM Members WHERE first_name = 'Katherine' AND last_name = 'Gonzales')),
        ((SELECT class_id FROM Classes WHERE class_type = 'weight training' AND day_scheduled = 'Monday' AND start_time = '14:30:00' AND end_time = '15:30:00'), (SELECT member_id FROM Members WHERE first_name = 'Tom' AND last_name = 'Barber')),
        ((SELECT class_id FROM Classes WHERE class_type = 'cardio' AND day_scheduled = 'Saturday' AND start_time = '10:30:00' AND end_time = '12:00:00'), (SELECT member_id FROM Members WHERE first_name = 'Myla' AND last_name = 'Chen'));

SET FOREIGN_KEY_CHECKS = 1;
COMMIT;