SELECT COUNT(*) FROM address;
SELECT COUNT(*) FROM district;
SELECT COUNT(*) FROM employment;
SELECT COUNT(*) FROM education;
SELECT COUNT(*) FROM birthregistration;
SELECT COUNT(*) FROM marriageregistration;
SELECT COUNT(*) FROM parentchild;
SELECT COUNT(*) FROM profession;
SELECT COUNT(*) FROM person;

SELECT gender, COUNT(*) AS total
FROM Person
GROUP BY gender;


SELECT p.name as person_name ,p.gender as gender,
 d.district_name as lives_at,d.province as province
from person p
JOIN district d ON p.district_id=d.district_id;

SELECT name,citizenship_no FROM person WHERE citizenship_no is NOT NULL;
SELECT name,gender from person WHERE citizenship_no is NULL;

SELECT d.district_name,COUNT(p.person_id) As total
from district d
LEFT JOIN person p on d.district_id=p.district_id
GROUP BY d.district_name
ORDER BY total DESC;

SELECT d.province,COUNT(p.person_id) as total
from district d
LEFT JOIN person p on d.district_id=p.district_id
GROUP BY d.province
ORDER BY total DESC;

SELECT avg(salary) as avg_salary,
       MAX(salary) as max_salary,
       MIN(salary) as min_salary,
       SUM(salary) as total_salary
FROM employment;

SELECT pr.profession_name,
       COUNT(e.emp_id)  AS employed,
       AVG(e.salary)    AS avg_salary,
       MAX(e.salary)    AS max_salary,
       MIN(e.salary)    AS min_salary
FROM Profession pr
LEFT JOIN Employment e ON pr.profession_id = e.profession_id
GROUP BY pr.profession_name
ORDER BY avg_salary DESC;

SELECT p.name as name,p.gender as gender,
e.salary as salary
FROM person p
JOIN employment e on p.person_id=e.person_id;

SELECT d.district_name, COUNT(p.person_id) as total
FROM district d
LEFT JOIN person p on d.district_id=p.district_id
GROUP BY d.district_name
HAVING total>3
ORDER BY total DESC;

SELECT pr.profession_name,AVG(e.salary) as avg_salary
from profession pr 
JOIN employment e on pr.profession_id=e.profession_id
GROUP BY pr.profession_name
HAVING avg_salary>30000
ORDER BY avg_salary DESC;

SELECT pr.profession_name, count(e.emp_id) as total_employed
FROM profession pr 
join employment e on pr.profession_id=e.profession_id
GROUP BY profession_name
HAVING total_employed>2;

#umeployed person
SELECT p.name,p.gender,d.district_name
from person p
LEFT JOIN employment e on p.person_id=e.person_id
LEFT JOIN district d on p.district_id=d.district_id
WHERE e.emp_id IS NULL;

#uneducated person
SELECT p.name,p.person_id,d.district_name
FROM person p
LEFT JOIN education ed on p.person_id=ed.person_id
LEFT JOIN district d on p.district_id=d.district_id
WHERE ed.education_id is NULL;

-- Unmarried persons
SELECT 
    p.name,
    p.gender,
    d.district_name
FROM person p
LEFT JOIN district d ON p.district_id = d.district_id
WHERE p.person_id NOT IN (
    SELECT person1_id FROM marriageregistration
    UNION
    SELECT person2_id FROM marriageregistration
);


#orphans
SELECT p.name,br.birth_date,br.ward_office
from birthregistration br
JOIN person p on br.child_id=p.person_id
WHERE br.father_id is NULL 
and  br.mother_id is NULL;

#children with guardians(but not biological)
SELECT 
    child.name as child_name,
    guard.name as guardian_name,
    pc.relation_type
from parentchild pc
join person child on pc.child_id=child.person_id
join person guard on pc.parent_id=guard.person_id
where pc.is_biological=FALSE;

-- Remarried persons
SELECT 
    p.name,
    COUNT(m.marriage_id) AS times_married
FROM person p
JOIN marriageregistration m
    ON p.person_id = m.person1_id
GROUP BY p.person_id, p.name
HAVING times_married > 1

UNION

SELECT 
    p.name,
    COUNT(m.marriage_id) AS times_married
FROM person p
JOIN marriageregistration m
    ON p.person_id = m.person2_id
GROUP BY p.person_id, p.name
HAVING times_married > 1;

SELECT 
    child.name as child_name,
    br.birth_date,
    father.name as father_name,
    mother.name as mother_name,
    br.ward_office
from birthregistration br
join person child on br.child_id=child.person_id
LEFT JOIN person mother on br.mother_id=mother.person_id
LEFT JOIN person father on br.father_id=father.person_id;

SELECT p.name,e.salary
from person p
JOIN employment e on p.person_id=e.person_id
where e.salary>(SELECT avg(salary) from employment);

-- Age calculation 
SELECT p.name,
    TIMESTAMPDIFF(YEAR,br.birth_date,CURDATE()) as age
    FROM person p
join birthregistration br on p.person_id=br.child_id
ORDER BY age DESC;

-- AGE Groups 
SELECT 
    CASE
        when TIMESTAMPDIFF(YEAR,br.birth_date,CURDATE()) BETWEEN 0 and 18 THEN '0-18' -- curdate() gives you current date
        when TIMESTAMPDIFF(YEAR,br.birth_date,CURDATE()) BETWEEN 19 and 35 THEN '19-35'
        when TIMESTAMPDIFF(YEAR,br.birth_date,CURDATE()) BETWEEN 36 and 60 THEN '36-60'
        ELSE '60+'
    END as age_group,
    count(*) as total
from person p
join birthregistration br on p.person_id=br.child_id
GROUP BY age_group
ORDER BY age_group;

-- Educated but unemployed -combine 3 tables
SELECT p.name,p.gender
from person p
join education ed on p.person_id=ed.person_id
LEFT join employment e on p.person_id=e.person_id
where e.emp_id is NULL;

-- orphan per district
SELECT d.district_name,count(br.child_id) as orphan_count
from birthregistration br
join person p on br.child_id=p.person_id
join district d on p.district_id=d.district_id
where br.mother_id is NULL and br.father_id is NULL
GROUP BY d.district_name
order by orphan_count DESC;

SELECT p.name,e.salary,pr.profession_name,
    TIMESTAMPDIFF(YEAR,br.birth_date,curdate()) as age
    FROM person p
join birthregistration br on p.person_id=br.child_id
join employment e on p.person_id=e.person_id
join profession pr on e.profession_id=pr.profession_id
HAVING age>60;