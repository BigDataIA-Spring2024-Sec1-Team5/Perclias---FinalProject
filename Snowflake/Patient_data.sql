USE PERCLIAS
CREATE TABLE PATIENT (
    patient_id NUMBER AUTOINCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    age INTEGER,
    gender VARCHAR(10),
    insurance_provider VARCHAR(100),
    medical_history TEXT,
    medications TEXT
);

-- Insert data into Patient table
INSERT INTO Patient (FIRST_NAME, LAST_NAME, DATE_OF_BIRTH, AGE, GENDER, INSURANCE_PROVIDER, MEDICAL_HISTORY, MEDICATIONS) VALUES
('John', 'Doe', '1990-05-15', 34, 'Male', 'BlueCross', 'None', 'Aspirin'),
('Jane', 'Smith', '1988-09-22', 36, 'Female', 'Aetna', 'High blood pressure', 'Lisinopril'),
('Michael', 'Johnson', '1995-12-10', 29, 'Male', 'Cigna', 'Allergies', 'Allegra'),
('Emily', 'Brown', '1992-07-08', 32, 'Female', 'UnitedHealthcare', 'Asthma', 'Ventolin'),
('David', 'Wilson', '1998-03-20', 26, 'Male', 'Anthem', 'Diabetes', 'Insulin'),
('Sarah', 'Garcia', '1991-11-28', 33, 'Female', 'Humana', 'None', 'None'),
('Daniel', 'Martinez', '1993-06-25', 31, 'Male', 'Kaiser Permanente', 'Anxiety', 'Xanax'),
('Jessica', 'Lee', '1997-02-14', 27, 'Female', 'Cigna', 'Depression', 'Prozac'),
('Christopher', 'Lopez', '1990-10-05', 33, 'Male', 'BlueCross', 'High cholesterol', 'Lipitor'),
('Amanda', 'Taylor', '1989-04-30', 35, 'Female', 'Aetna', 'None', 'None'),
('James', 'Harris', '1994-08-18', 30, 'Male', 'UnitedHealthcare', 'Acid reflux', 'Prilosec'),
(212, 'Matthew', 'Anderson', '1993-04-12', 31, 'Male', 'BlueCross', 'None', 'Aspirin'),
    (213, 'Olivia', 'Wilson', '1996-11-25', 28, 'Female', 'Aetna', 'High blood pressure', 'Lisinopril'),
    (214, 'Ethan', 'Thompson', '1990-08-30', 34, 'Male', 'Cigna', 'Allergies', 'Allegra'),
    (215, 'Isabella', 'Martinez', '1987-02-18', 37, 'Female', 'UnitedHealthcare', 'Asthma', 'Ventolin'),
    (216, 'Noah', 'Brown', '1994-06-05', 30, 'Male', 'Anthem', 'Diabetes', 'Insulin'),
    (217, 'Emma', 'Garcia', '1988-12-22', 36, 'Female', 'Humana', 'None', 'None'),
    (218, 'Liam', 'Lee', '1991-10-17', 29, 'Male', 'Kaiser Permanente', 'Anxiety', 'Xanax'),
    (219, 'Sophia', 'Harris', '1998-07-03', 26, 'Female', 'Cigna', 'Depression', 'Prozac'),
    (220, 'Alexander', 'Lopez', '1995-03-14', 29, 'Male', 'BlueCross', 'High cholesterol', 'Lipitor'),
    (221, 'Mia', 'Taylor', '1992-09-09', 32, 'Female', 'Aetna', 'None', 'None'),
    (222, 'Charlotte', 'Johnson', '1989-05-24', 35, 'Female', 'UnitedHealthcare', 'Acid reflux', 'Prilosec');

