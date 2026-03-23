
from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# DB connection 
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",          # XAMPP default has no password
        database="civil_registry"
    )

def query(sql, params=None):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, params or ())
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# helpers
def ok(data):
    return jsonify({"status": "success", "count": len(data), "data": data})

def err(msg, code=500):
    return jsonify({"status": "error", "message": msg}), code

#  1. DISTRICT

@app.route("/districts", methods=["GET"])
def get_districts():
    """
    GET /districts
    GET /districts?province=Koshi Province
    """
    try:
        province = request.args.get("province")
        if province:
            rows = query("SELECT * FROM district WHERE province = %s ORDER BY district_name", (province,))
        else:
            rows = query("SELECT * FROM district ORDER BY province, district_name")
        return ok(rows)
    except Error as e:
        return err(str(e))

@app.route("/districts/<int:district_id>", methods=["GET"])
def get_district(district_id):
    try:
        rows = query("SELECT * FROM district WHERE district_id = %s", (district_id,))
        if not rows:
            return err("District not found", 404)
        return ok(rows)
    except Error as e:
        return err(str(e))

#  2. ADDRESS
@app.route("/addresses", methods=["GET"])
def get_addresses():
    """
    GET /addresses
    GET /addresses?district_id=27
    """
    try:
        district_id = request.args.get("district_id")
        if district_id:
            rows = query("""
                SELECT a.*, d.district_name, d.province
                FROM address a
                JOIN district d ON a.district_id = d.district_id
                WHERE a.district_id = %s
            """, (district_id,))
        else:
            rows = query("""
                SELECT a.*, d.district_name, d.province
                FROM address a
                JOIN district d ON a.district_id = d.district_id
                ORDER BY d.district_name
            """)
        return ok(rows)
    except Error as e:
        return err(str(e))

@app.route("/addresses/<int:address_id>", methods=["GET"])
def get_address(address_id):
    try:
        rows = query("""
            SELECT a.*, d.district_name, d.province
            FROM address a
            JOIN district d ON a.district_id = d.district_id
            WHERE a.address_id = %s
        """, (address_id,))
        if not rows:
            return err("Address not found", 404)
        return ok(rows)
    except Error as e:
        return err(str(e))

#  3. PERSON
@app.route("/persons", methods=["GET"])
def get_persons():
    """
    GET /persons
    GET /persons?gender=M
    GET /persons?district_id=27
    GET /persons?citizenship=KAT-0001-1985
    GET /persons?has_citizenship=true   (only persons with citizenship)
    GET /persons?has_citizenship=false  (minors / no citizenship)
    """
    try:
        gender         = request.args.get("gender")
        district_id    = request.args.get("district_id")
        citizenship    = request.args.get("citizenship")
        has_citizenship = request.args.get("has_citizenship")

        base = """
            SELECT p.person_id, p.name, p.gender, p.citizenship_no,
                   a.municipality, a.ward, a.tole,
                   d.district_name, d.province
            FROM person p
            LEFT JOIN address  a ON p.address_id  = a.address_id
            LEFT JOIN district d ON p.district_id = d.district_id
            WHERE 1=1
        """
        params = []

        if gender:
            base += " AND p.gender = %s"
            params.append(gender.upper())
        if district_id:
            base += " AND p.district_id = %s"
            params.append(district_id)
        if citizenship:
            base += " AND p.citizenship_no = %s"
            params.append(citizenship)
        if has_citizenship == "true":
            base += " AND p.citizenship_no IS NOT NULL"
        elif has_citizenship == "false":
            base += " AND p.citizenship_no IS NULL"
        if citizenship:
            base += " AND p.citizenship_no = %s"
            params.append(citizenship)

        base += " ORDER BY p.name"
        rows = query(base, params)
        return ok(rows)
    except Error as e:
        return err(str(e))

@app.route("/persons/<int:person_id>", methods=["GET"])
def get_person(person_id):
    try:
        rows = query("""
            SELECT p.*, a.municipality, a.ward, a.tole,
                   d.district_name, d.province
            FROM person p
            LEFT JOIN address  a ON p.address_id  = a.address_id
            LEFT JOIN district d ON p.district_id = d.district_id
            WHERE p.person_id = %s
        """, (person_id,))
        if not rows:
            return err("Person not found", 404)
        return ok(rows)
    except Error as e:
        return err(str(e))

#  4. PROFESSION
@app.route("/professions", methods=["GET"])
def get_professions():
    try:
        rows = query("SELECT * FROM profession ORDER BY profession_name")
        return ok(rows)
    except Error as e:
        return err(str(e))

@app.route("/professions/<int:profession_id>", methods=["GET"])
def get_profession(profession_id):
    try:
        rows = query("SELECT * FROM profession WHERE profession_id = %s", (profession_id,))
        if not rows:
            return err("Profession not found", 404)
        return ok(rows)
    except Error as e:
        return err(str(e))

#  5. EMPLOYMENT
@app.route("/employment", methods=["GET"])
def get_employment():
    """
    GET /employment
    GET /employment?person_id=1
    GET /employment?profession_id=3
    GET /employment?min_salary=50000
    GET /employment?max_salary=30000
    """
    try:
        person_id     = request.args.get("person_id")
        profession_id = request.args.get("profession_id")
        min_salary    = request.args.get("min_salary")
        max_salary    = request.args.get("max_salary")

        base = """
            SELECT e.emp_id, e.organization, e.salary,
                   p.name AS person_name, p.gender,
                   pr.profession_name
            FROM employment e
            JOIN person     p  ON e.person_id     = p.person_id
            JOIN profession pr ON e.profession_id = pr.profession_id
            WHERE 1=1
        """
        params = []

        if person_id:
            base += " AND e.person_id = %s"
            params.append(person_id)
        if profession_id:
            base += " AND e.profession_id = %s"
            params.append(profession_id)
        if min_salary:
            base += " AND e.salary >= %s"
            params.append(min_salary)
        if max_salary:
            base += " AND e.salary <= %s"
            params.append(max_salary)

        base += " ORDER BY e.salary DESC"
        rows = query(base, params)
        return ok(rows)
    except Error as e:
        return err(str(e))

@app.route("/employment/<int:emp_id>", methods=["GET"])
def get_employment_by_id(emp_id):
    try:
        rows = query("""
            SELECT e.*, p.name AS person_name, pr.profession_name
            FROM employment e
            JOIN person     p  ON e.person_id     = p.person_id
            JOIN profession pr ON e.profession_id = pr.profession_id
            WHERE e.emp_id = %s
        """, (emp_id,))
        if not rows:
            return err("Employment record not found", 404)
        return ok(rows)
    except Error as e:
        return err(str(e))

#  6. EDUCATION
@app.route("/education", methods=["GET"])
def get_education():
    """
    GET /education
    GET /education?person_id=3
    GET /education?level=PhD
      levels: Primary | Secondary | Bachelor | Master | PhD
    """
    try:
        person_id = request.args.get("person_id")
        level     = request.args.get("level")

        base = """
            SELECT ed.education_id, ed.degree_name, ed.level,
                   ed.institution_name, ed.years_completed,
                   p.name AS person_name
            FROM education ed
            JOIN person p ON ed.person_id = p.person_id
            WHERE 1=1
        """
        params = []

        if person_id:
            base += " AND ed.person_id = %s"
            params.append(person_id)
        if level:
            base += " AND ed.level = %s"
            params.append(level)

        base += " ORDER BY p.name, ed.years_completed"
        rows = query(base, params)
        return ok(rows)
    except Error as e:
        return err(str(e))

@app.route("/education/<int:education_id>", methods=["GET"])
def get_education_by_id(education_id):
    try:
        rows = query("""
            SELECT ed.*, p.name AS person_name
            FROM education ed
            JOIN person p ON ed.person_id = p.person_id
            WHERE ed.education_id = %s
        """, (education_id,))
        if not rows:
            return err("Education record not found", 404)
        return ok(rows)
    except Error as e:
        return err(str(e))

#  7. BIRTH REGISTRATION
@app.route("/births", methods=["GET"])
def get_births():
    """
    GET /births
    GET /births?child_id=9
    GET /births?orphans=true   (both mother and father unknown)
    """
    try:
        child_id = request.args.get("child_id")
        orphans  = request.args.get("orphans")

        base = """
            SELECT br.birth_id, br.birth_date, br.ward_office,
                   child.name   AS child_name,
                   mother.name  AS mother_name,
                   father.name  AS father_name
            FROM birthregistration br
            JOIN   person child  ON br.child_id  = child.person_id
            LEFT JOIN person mother ON br.mother_id = mother.person_id
            LEFT JOIN person father ON br.father_id = father.person_id
            WHERE 1=1
        """
        params = []

        if child_id:
            base += " AND br.child_id = %s"
            params.append(child_id)
        if orphans == "true":
            base += " AND br.mother_id IS NULL AND br.father_id IS NULL"

        base += " ORDER BY br.birth_date DESC"
        rows = query(base, params)
        return ok(rows)
    except Error as e:
        return err(str(e))

@app.route("/births/<int:birth_id>", methods=["GET"])
def get_birth(birth_id):
    try:
        rows = query("""
            SELECT br.*,
                   child.name  AS child_name,
                   mother.name AS mother_name,
                   father.name AS father_name
            FROM birthregistration br
            JOIN   person child  ON br.child_id  = child.person_id
            LEFT JOIN person mother ON br.mother_id = mother.person_id
            LEFT JOIN person father ON br.father_id = father.person_id
            WHERE br.birth_id = %s
        """, (birth_id,))
        if not rows:
            return err("Birth record not found", 404)
        return ok(rows)
    except Error as e:
        return err(str(e))

#  8. MARRIAGE REGISTRATION
@app.route("/marriages", methods=["GET"])
def get_marriages():
    """
    GET /marriages
    GET /marriages?person_id=1   (marriages involving this person)
    """
    try:
        person_id = request.args.get("person_id")

        base = """
            SELECT m.marriage_id, m.marriage_date, m.ward_office,
                   p1.name AS person1_name,
                   p2.name AS person2_name
            FROM marriageregistration m
            JOIN person p1 ON m.person1_id = p1.person_id
            JOIN person p2 ON m.person2_id = p2.person_id
            WHERE 1=1
        """
        params = []

        if person_id:
            base += " AND (m.person1_id = %s OR m.person2_id = %s)"
            params.extend([person_id, person_id])

        base += " ORDER BY m.marriage_date DESC"
        rows = query(base, params)
        return ok(rows)
    except Error as e:
        return err(str(e))

@app.route("/marriages/<int:marriage_id>", methods=["GET"])
def get_marriage(marriage_id):
    try:
        rows = query("""
            SELECT m.*,
                   p1.name AS person1_name,
                   p2.name AS person2_name
            FROM marriageregistration m
            JOIN person p1 ON m.person1_id = p1.person_id
            JOIN person p2 ON m.person2_id = p2.person_id
            WHERE m.marriage_id = %s
        """, (marriage_id,))
        if not rows:
            return err("Marriage record not found", 404)
        return ok(rows)
    except Error as e:
        return err(str(e))

#  9. PARENT-CHILD
@app.route("/parentchild", methods=["GET"])
def get_parentchild():
    """
    GET /parentchild
    GET /parentchild?child_id=9
    GET /parentchild?parent_id=1
    GET /parentchild?relation_type=guardian
      types: father | mother | guardian
    GET /parentchild?is_biological=false
    """
    try:
        child_id      = request.args.get("child_id")
        parent_id     = request.args.get("parent_id")
        relation_type = request.args.get("relation_type")
        is_biological = request.args.get("is_biological")

        base = """
            SELECT pc.relation_id, pc.relation_type, pc.is_biological,
                   child.name  AS child_name,
                   parent.name AS parent_name
            FROM parentchild pc
            JOIN person child  ON pc.child_id  = child.person_id
            JOIN person parent ON pc.parent_id = parent.person_id
            WHERE 1=1
        """
        params = []

        if child_id:
            base += " AND pc.child_id = %s"
            params.append(child_id)
        if parent_id:
            base += " AND pc.parent_id = %s"
            params.append(parent_id)
        if relation_type:
            base += " AND pc.relation_type = %s"
            params.append(relation_type)
        if is_biological is not None:
            val = 1 if is_biological == "true" else 0
            base += " AND pc.is_biological = %s"
            params.append(val)

        base += " ORDER BY child.name"
        rows = query(base, params)
        return ok(rows)
    except Error as e:
        return err(str(e))

@app.route("/parentchild/<int:relation_id>", methods=["GET"])
def get_parentchild_by_id(relation_id):
    try:
        rows = query("""
            SELECT pc.*,
                   child.name  AS child_name,
                   parent.name AS parent_name
            FROM parentchild pc
            JOIN person child  ON pc.child_id  = child.person_id
            JOIN person parent ON pc.parent_id = parent.person_id
            WHERE pc.relation_id = %s
        """, (relation_id,))
        if not rows:
            return err("Relation not found", 404)
        return ok(rows)
    except Error as e:
        return err(str(e))

#  ANALYTICS ENDPOINTS
@app.route("/analytics/gender-count", methods=["GET"])
def gender_count():
    try:
        rows = query("SELECT gender, COUNT(*) AS total FROM person GROUP BY gender")
        return ok(rows)
    except Error as e:
        return err(str(e))

@app.route("/analytics/salary-stats", methods=["GET"])
def salary_stats():
    try:
        rows = query("""
            SELECT AVG(salary) AS avg_salary,
                   MAX(salary) AS max_salary,
                   MIN(salary) AS min_salary,
                   SUM(salary) AS total_salary
            FROM employment
        """)
        return ok(rows)
    except Error as e:
        return err(str(e))

@app.route("/analytics/orphans", methods=["GET"])
def orphans():
    try:
        rows = query("""
            SELECT p.name, br.birth_date, br.ward_office
            FROM birthregistration br
            JOIN person p ON br.child_id = p.person_id
            WHERE br.father_id IS NULL AND br.mother_id IS NULL
        """)
        return ok(rows)
    except Error as e:
        return err(str(e))

@app.route("/analytics/unemployed", methods=["GET"])
def unemployed():
    try:
        rows = query("""
            SELECT p.name, p.gender, d.district_name
            FROM person p
            LEFT JOIN employment e ON p.person_id = e.person_id
            LEFT JOIN district   d ON p.district_id = d.district_id
            WHERE e.emp_id IS NULL
        """)
        return ok(rows)
    except Error as e:
        return err(str(e))

@app.route("/analytics/age-groups", methods=["GET"])
def age_groups():
    try:
        rows = query("""
            SELECT
                CASE
                    WHEN TIMESTAMPDIFF(YEAR, br.birth_date, CURDATE()) BETWEEN 0  AND 18 THEN '0-18'
                    WHEN TIMESTAMPDIFF(YEAR, br.birth_date, CURDATE()) BETWEEN 19 AND 35 THEN '19-35'
                    WHEN TIMESTAMPDIFF(YEAR, br.birth_date, CURDATE()) BETWEEN 36 AND 60 THEN '36-60'
                    ELSE '60+'
                END AS age_group,
                COUNT(*) AS total
            FROM person p
            JOIN birthregistration br ON p.person_id = br.child_id
            GROUP BY age_group
            ORDER BY age_group
        """)
        return ok(rows)
    except Error as e:
        return err(str(e))

@app.route("/analytics/province-population", methods=["GET"])
def province_population():
    try:
        rows = query("""
            SELECT d.province, COUNT(p.person_id) AS total
            FROM district d
            LEFT JOIN person p ON d.district_id = p.district_id
            GROUP BY d.province
            ORDER BY total DESC
        """)
        return ok(rows)
    except Error as e:
        return err(str(e))

@app.route("/analytics/remarried", methods=["GET"])
def remarried():
    try:
        rows = query("""
            SELECT p.name, COUNT(m.marriage_id) AS times_married
            FROM person p
            JOIN marriageregistration m ON p.person_id = m.person1_id
            GROUP BY p.person_id, p.name HAVING times_married > 1
            UNION
            SELECT p.name, COUNT(m.marriage_id) AS times_married
            FROM person p
            JOIN marriageregistration m ON p.person_id = m.person2_id
            GROUP BY p.person_id, p.name HAVING times_married > 1
        """)
        return ok(rows)
    except Error as e:
        return err(str(e))

# ADDED: salary by profession for chart
@app.route("/analytics/salary-by-profession", methods=["GET"])
def salary_by_profession():
    try:
        rows = query("""
            SELECT pr.profession_name,
                   ROUND(AVG(e.salary), 0) AS avg_salary
            FROM profession pr
            JOIN employment e ON pr.profession_id = e.profession_id
            GROUP BY pr.profession_name
            ORDER BY avg_salary DESC
        """)
        return ok(rows)
    except Error as e:
        return err(str(e))

# ADDED: universal person search
@app.route("/search", methods=["GET"])
def search():
    try:
        name         = request.args.get("name")
        district_id  = request.args.get("district_id")
        municipality = request.args.get("municipality")
        citizenship  = request.args.get("citizenship")
        base = """
            SELECT DISTINCT p.person_id, p.name, p.gender, p.citizenship_no,
                   a.municipality, a.ward, a.tole, d.district_name, d.province
            FROM person p
            LEFT JOIN address  a ON p.address_id  = a.address_id
            LEFT JOIN district d ON p.district_id = d.district_id
            WHERE 1=1
        """
        params = []
        if name:
            base += " AND p.name LIKE %s"
            params.append(f"%{name}%")
        if district_id:
            base += " AND p.district_id = %s"
            params.append(district_id)
        if municipality:
            base += " AND a.municipality LIKE %s"
            params.append(f"%{municipality}%")
        if citizenship:
            base += " AND p.citizenship_no = %s"
            params.append(citizenship)
        base += " ORDER BY p.name LIMIT 50"
        rows = query(base, params)
        return ok(rows)
    except Error as e:
        return err(str(e))

# ADDED: full person profile from all 9 tables
@app.route("/search/<int:person_id>/full", methods=["GET"])
def search_full(person_id):
    try:
        person = query("""
            SELECT p.*, a.municipality, a.ward, a.tole, d.district_name, d.province
            FROM person p
            LEFT JOIN address  a ON p.address_id  = a.address_id
            LEFT JOIN district d ON p.district_id = d.district_id
            WHERE p.person_id = %s
        """, (person_id,))
        if not person:
            return err("Person not found", 404)
        employment = query("""
            SELECT e.organization, e.salary, pr.profession_name
            FROM employment e
            JOIN profession pr ON e.profession_id = pr.profession_id
            WHERE e.person_id = %s
        """, (person_id,))
        education = query("""
            SELECT degree_name, level, institution_name, years_completed
            FROM education WHERE person_id = %s
            ORDER BY FIELD(level,'Primary','Secondary','Bachelor','Master','PhD')
        """, (person_id,))
        birth = query("""
            SELECT br.birth_date, br.ward_office,
                   mother.name AS mother_name, father.name AS father_name
            FROM birthregistration br
            LEFT JOIN person mother ON br.mother_id = mother.person_id
            LEFT JOIN person father ON br.father_id = father.person_id
            WHERE br.child_id = %s
        """, (person_id,))
        marriages = query("""
            SELECT m.marriage_date, m.ward_office,
                   p1.name AS person1_name, p2.name AS person2_name
            FROM marriageregistration m
            JOIN person p1 ON m.person1_id = p1.person_id
            JOIN person p2 ON m.person2_id = p2.person_id
            WHERE m.person1_id = %s OR m.person2_id = %s
        """, (person_id, person_id))
        children = query("""
            SELECT child.name AS child_name, pc.relation_type, pc.is_biological
            FROM parentchild pc
            JOIN person child ON pc.child_id = child.person_id
            WHERE pc.parent_id = %s
        """, (person_id,))
        parents = query("""
            SELECT parent.name AS parent_name, pc.relation_type, pc.is_biological
            FROM parentchild pc
            JOIN person parent ON pc.parent_id = parent.person_id
            WHERE pc.child_id = %s
        """, (person_id,))
        return jsonify({
            "status":     "success",
            "person":     person[0],
            "employment": employment,
            "education":  education,
            "birth":      birth[0] if birth else None,
            "marriages":  marriages,
            "children":   children,
            "parents":    parents,
        })
    except Error as e:
        return err(str(e))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
