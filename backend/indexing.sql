EXPLAIN SELECT * from person
WHERE citizenship_no = 'KAT-0001-1985';
CREATE index if not exists idx_citizenship
on person(citizenship_no);

EXPLAIN SELECT * from person
where citizenship_no='KAT-0001-1985';

CREATE index if not exists idx_person_name
on person(name);
CREATE index if not exists idx_birth_child
on birthregistration(child_id);

CREATE index if not exists idx_emp_person
on employment(person_id);

SHOW INDEX FROM person;
SHOW INDEX FROM birthregistration;
SHOW INDEX FROM employment;

EXPLAIN SELECT * FROM person 
WHERE name = 'Ram Bahadur Shrestha';

CREATE INDEX IF NOT EXISTS idx_emp_salary
ON employment(salary);

CREATE INDEX IF NOT EXISTS idx_edu_level
ON education(level);

EXPLAIN SELECT * FROM employment
WHERE salary > 50000;

-- Without index → full table scan (reads all 100+ rows)
-- With index    → jumps directly to matching rows