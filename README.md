# Civil Registration DBMS Project

This project is a database design for a civil registration system (Nepal context), built in MySQL. The model is centered on a single Person entity and tracks identity, location, family relationships, education, employment, and legal registration events.

## Project Status

Current implementation includes 9 core tables with foreign key relationships and district seed data.

Implemented:
- Core schema in backend/project.sql
- Nepal district seed inserts in backend/District_data.sql
- ER and modeling diagrams in docs/
- Frontend layer in frontend/ 

Not implemented yet:
- Query set in backend/queries.sql (currently empty)
- Index tuning in backend/indexing.sql (currently empty)
- API/server logic in server/main.py (currently empty)

## Database Schema (9 Tables)

1. District
2. Address
3. Person
4. Profession
5. Employment
6. Education
7. BirthRegistration
8. MarriageRegistration
9. ParentChild

Relationship flow:
- District -> Address -> Person
- Person -> Employment -> Profession
- Person -> Education
- Person -> BirthRegistration (child_id, mother_id, father_id)
- Person -> MarriageRegistration (person1_id, person2_id)
- Person -> ParentChild (child_id, parent_id)

## Design Decisions

- FK on many side:
   address_id is stored in Person (not person_id in Address).
- Nullable mother/father in birth records:
   mother_id and father_id are nullable to support unknown-parent/orphan cases.
- ParentChild separated from BirthRegistration:
   supports non-biological/legal relations such as guardianship and adoption.
- Profession as a lookup table:
   avoids inconsistent free-text profession values.
- citizenship_no is UNIQUE but nullable:
   allows records for minors before citizenship issuance.

## Table Highlights

- District:
   district_id (PK), district_name (UNIQUE), province
- Address:
   address_id (PK), district_id (FK), municipality, ward, tole
- Person:
   person_id (PK), name, gender (M/F/O), citizenship_no (UNIQUE, nullable), address_id (FK), district_id (FK)
- Profession:
   profession_id (PK), profession_name
- Employment:
   emp_id (PK), organization, salary, person_id (FK), profession_id (FK)
- Education:
   education_id (PK), degree_name, level (Primary/Secondary/Bachelor/Master/PhD), institution_name, years_completed, person_id (FK)
- BirthRegistration:
   birth_id (PK), birth_date, ward_office, child_id (FK), mother_id (FK, nullable), father_id (FK, nullable)
- MarriageRegistration:
   marriage_id (PK), marriage_date, ward_office, person1_id (FK), person2_id (FK)
- ParentChild:
   relation_id (PK), child_id (FK), parent_id (FK), relation_type (father/mother/guardian), is_biological

## Folder Structure

- backend/
   SQL schema, seed, indexing, and query files
- helperfunction/
   small scripts used to generate district insert statements
- docs/
   ER diagram and notation references
- server/
   placeholder for backend service code
- frontend/
   placeholder for UI layer

## Setup and Execution

1. Create a MySQL database (for example: civil_registry).
2. Run backend/project.sql to create all tables.
3. Run backend/District_data.sql to seed district and province values.
4. Optionally add indexes in backend/indexing.sql as the query workload grows.
5. Add and test queries in backend/queries.sql.

## How Others Can Run This (Simple)

Prerequisites:
- MySQL Server 8.0+ installed
- A MySQL client (MySQL Workbench or command line)

Option 1: Using MySQL command line

1. Open terminal in the project root.
2. Connect to MySQL:
   mysql -u root -p
3. Inside MySQL, run:
   CREATE DATABASE civil_registry;
   USE civil_registry;
   SOURCE backend/project.sql;
   SOURCE backend/District_data.sql;
4. Verify tables:
   SHOW TABLES;

Option 2: Using MySQL Workbench

1. Open MySQL Workbench and connect to your local server.
2. Create schema `civil_registry`.
3. Open and run `backend/project.sql`.
4. Open and run `backend/District_data.sql`.
5. Refresh schema and confirm all tables are created.

Expected result:
- 9 core tables are created.
- District data is inserted safely (re-running is okay because `INSERT IGNORE` is used).

## Diagrams

Available in docs/:
- docs/ER_diagram.jpeg
- docs/Architecture.png
- docs/Cardinality.png
- docs/Notation.png

## Notes

- District inserts use INSERT IGNORE for safe re-runs.
- The schema focuses on normalization and relationship correctness first; query optimization and application layer are planned next.
