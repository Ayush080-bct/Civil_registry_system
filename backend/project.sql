CREATE TABLE IF NOT EXISTS District (
    district_id INT AUTO_INCREMENT PRIMARY KEY,
    district_name VARCHAR(100) NOT NULL,
    province VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Address (
    address_id INT AUTO_INCREMENT PRIMARY KEY,
    district_id INT NOT NULL,
    municipality VARCHAR(100),
    ward VARCHAR(50),
    tole VARCHAR(100),
    CONSTRAINT fk_address_district FOREIGN KEY (district_id)
        REFERENCES District(district_id)
);

CREATE TABLE IF NOT EXISTS Person (
    person_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender ENUM('M', 'F', 'O'),
    citizenship_no VARCHAR(20) UNIQUE,
    address_id INT,
    district_id INT,
    CONSTRAINT fk_person_address FOREIGN KEY (address_id)
        REFERENCES Address(address_id),
    CONSTRAINT fk_person_district FOREIGN KEY (district_id)
        REFERENCES District(district_id)
);

CREATE TABLE IF NOT EXISTS Profession (
    profession_id INT AUTO_INCREMENT PRIMARY KEY,
    profession_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Employment (
    emp_id INT AUTO_INCREMENT PRIMARY KEY,
    organization VARCHAR(100) NOT NULL,
    salary DECIMAL(10, 2),
    person_id INT,
    profession_id INT,
    CONSTRAINT fk_emp_person FOREIGN KEY (person_id)
        REFERENCES Person(person_id),
    CONSTRAINT fk_emp_profession FOREIGN KEY (profession_id)
        REFERENCES Profession(profession_id)
);

CREATE TABLE IF NOT EXISTS Education (
    education_id INT AUTO_INCREMENT PRIMARY KEY,
    degree_name VARCHAR(100),
    level ENUM('Primary', 'Secondary', 'Bachelor', 'Master', 'PhD'),
    institution_name VARCHAR(150),
    years_completed INT,
    person_id INT,
    CONSTRAINT fk_education_person FOREIGN KEY (person_id)
        REFERENCES Person(person_id)
);

CREATE TABLE IF NOT EXISTS BirthRegistration (
    birth_id INT AUTO_INCREMENT PRIMARY KEY,
    birth_date DATE NOT NULL,
    ward_office VARCHAR(100),
    child_id INT NOT NULL,
    mother_id INT,
    father_id INT,
    CONSTRAINT fk_birth_child FOREIGN KEY (child_id)
        REFERENCES Person(person_id),
    CONSTRAINT fk_birth_mother FOREIGN KEY (mother_id)
        REFERENCES Person(person_id),
    CONSTRAINT fk_birth_father FOREIGN KEY (father_id)
        REFERENCES Person(person_id)
);

CREATE TABLE IF NOT EXISTS MarriageRegistration (
    marriage_id INT AUTO_INCREMENT PRIMARY KEY,
    marriage_date DATE NOT NULL,
    ward_office VARCHAR(100),
    person1_id INT NOT NULL,
    person2_id INT NOT NULL,
    CONSTRAINT fk_marriage_p1 FOREIGN KEY (person1_id)
        REFERENCES Person(person_id),
    CONSTRAINT fk_marriage_p2 FOREIGN KEY (person2_id)
        REFERENCES Person(person_id)
);

CREATE TABLE IF NOT EXISTS ParentChild (
    relation_id INT AUTO_INCREMENT PRIMARY KEY,
    child_id INT NOT NULL,
    parent_id INT NOT NULL,
    relation_type ENUM('father', 'mother', 'guardian') NOT NULL,
    is_biological BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_pc_child FOREIGN KEY (child_id)
        REFERENCES Person(person_id),
    CONSTRAINT fk_pc_parent FOREIGN KEY (parent_id)
        REFERENCES Person(person_id)
);
ALTER TABLE district MODIFY district_name VARCHAR(100) UNIQUE NOT NULL;
