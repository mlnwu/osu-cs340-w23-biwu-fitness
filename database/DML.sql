--
-- Get a list of all members
--
SELECT * FROM Members;

--
-- Get all trainers and all classes they teach
--
SELECT * FROM Trainers INNER JOIN Classes ON Trainers.trainer_id = Classes.trainer_id;

--
-- Get all classes that start after a certain time
--
SELECT * FROM Classes WHERE Classes.start_time >= :start_time_input;

--
-- Get names of all members and what classes they're in on what day
--
SELECT Members.first_name, Members.last_name, Classes.class_type, Classes.day_scheduled
FROM Classes_has_Members
INNER JOIN Members ON Classes_has_Members.members_member_id = Members.member_id
INNER JOIN Classes ON Classes_has_Members.classes_class_id = Classes.class_id;

--
-- Get all transactions with amounts from a certain day and who did the transaction
--
SELECT Transactions.transaction_id, Transactions.transaction_amount, Members.first_name, Members.last_name
FROM Transactions 
INNER JOIN Members_has_Transactions ON Transactions.transaction_id = Members_has_Transactions.transactions_transaction_id
INNER JOIN Members ON Members_has_Transactions.members_member_id = Members.member_id
WHERE Transactions.transaction_date = :transaction_date_input;

--
-- Get all transactions made by a certain member
--
SELECT * FROM Members_has_Transactions WHERE Members_has_Transactions.members_member_id = :members_member_id_input;

--
-- Adding a new member
--
INSERT INTO Members(first_name, last_name, tier_type, phone_number, email)
VALUES (:first_name_input, :last_name_input, :tier_type_input, :phone_number_input, :email_input);

--
-- Recording a transaction
--
INSERT INTO Transactions(transaction_amount, transaction_date)
    VALUES
        (:transaction_amount_input, :transaction_date_input);
INSERT INTO Members_has_Transactions(members_member_id, transactions_transaction_id)
    VALUES
        ((SELECT member_id FROM Members WHERE first_name = :first_name_input AND last_name = :last_name_input), LAST_INSERT_ID());

--
-- Adding a new trainer
--
INSERT INTO Trainers(first_name, last_name, phone_number, email)
    VALUES
        (:first_name_input, :last_name_input, :phone_number_input, :email_input);

--
-- Adding a new class
--
INSERT INTO Classes(class_type, trainer_id, day_scheduled, start_time, end_time)
    VALUES
        (:class_type_input, :trainer_id_input, :day_scheduled_input, :start_time_input, :end_time_input);

--
-- Enrolling a member in a class
--
INSERT INTO Classes_has_Members(Classes_class_id, Members_member_id)
    VALUES
        ((SELECT class_id FROM Classes WHERE class_type = :class_type_input AND day_scheduled = :day_scheduled_input AND start_time = :start_time_input), 
        (SELECT member_id FROM Members WHERE first_name = :first_name_input AND last_name = :last_name_input));

--
-- Updating the meeting time of a class
--
UPDATE Classes SET day_scheduled = :day_scheduled_input, start_time = :start_time_input, end_time = :end_time_input WHERE class_id = :class_id_input;

--
-- Deleting a member who is no longer enrolled
--
DELETE FROM Members WHERE member_id = :member_id_input;