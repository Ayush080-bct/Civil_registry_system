"""
generate_seed.py
Generates realistic seed data for all 6 tables with aligned FKs.
Output: seed_data.txt (ready to paste into phpMyAdmin SQL tab)

Install: pip install faker
Run:     python generate_seed.py
"""

from faker import Faker
import random

fake = Faker()


districts = {
    1:"Bhojpur",2:"Dhankuta",3:"Ilam",4:"Jhapa",5:"Khotang",
    6:"Morang",7:"Okhaldhunga",8:"Panchthar",9:"Sankhuwasabha",10:"Solukhumbu",
    11:"Sunsari",12:"Taplejung",13:"Terhathum",14:"Udayapur",
    15:"Bara",16:"Dhanusha",17:"Mahottari",18:"Parsa",19:"Rautahat",
    20:"Saptari",21:"Sarlahi",22:"Siraha",
    23:"Bhaktapur",24:"Chitwan",25:"Dhading",26:"Dolakha",27:"Kathmandu",
    28:"Kavrepalanchok",29:"Lalitpur",30:"Makwanpur",31:"Nuwakot",
    32:"Ramechhap",33:"Rasuwa",34:"Sindhuli",35:"Sindhupalchok",
    36:"Baglung",37:"Gorkha",38:"Kaski",39:"Lamjung",40:"Manang",
    41:"Mustang",42:"Myagdi",43:"Nawalpur",44:"Parbat",45:"Syangja",46:"Tanahun",
    47:"Arghakhanchi",48:"Banke",49:"Bardiya",50:"Dang",
    51:"Eastern Rukum",52:"Gulmi",53:"Kapilvastu",54:"Palpa",55:"Parasi",
    56:"Pyuthan",57:"Rolpa",58:"Rupandehi",
    59:"Dolpa",60:"Humla",61:"Jajarkot",62:"Jumla",63:"Kalikot",
    64:"Mugu",65:"Salyan",66:"Surkhet",67:"Western Rukum",
    68:"Achham",69:"Baitadi",70:"Bajhang",71:"Bajura",72:"Dadeldhura",
    73:"Darchula",74:"Doti",75:"Kailali",76:"Kanchanpur"
}

professions = {
    1:"Teacher",2:"Engineer",3:"Doctor",4:"Nurse",5:"Farmer",
    6:"Government Officer",7:"Police Officer",8:"Army Officer",
    9:"Lawyer",10:"Accountant",11:"Business",12:"Driver",
    13:"Laborer",14:"Journalist",15:"Pharmacist",16:"Lab technician",17:"Pilot"
}


salary_range = {
    1:(20000,35000),  2:(40000,70000),  3:(60000,100000), 4:(25000,40000),
    5:(8000,20000),   6:(25000,45000),  7:(28000,40000),  8:(30000,50000),
    9:(45000,80000),  10:(30000,55000), 11:(20000,80000), 12:(12000,22000),
    13:(10000,18000), 14:(22000,40000), 15:(30000,50000), 16:(25000,45000),
    17:(80000,150000)
}

# address_id range already in your DB (1 to ~500 from your address.sql)
# We use only addresses that are confirmed to exist
ADDRESS_MAX = 500  # conservative — adjust if your address table has more

# Nepali first names
male_first   = ["Ram","Hari","Bikash","Gopal","Sanjay","Dipak","Nabin",
                 "Prakash","Rajesh","Kamal","Santosh","Manoj","Dinesh","Lokesh",
                 "Prabhat","Umesh","Raju","Krishna","Bimal","Suman","Ganesh",
                 "Ashok","Narayan","Bijay","Surya","Rabindra","Tilak","Anil",
                 "Binod","Suresh","Arjun","Yam","Kiran","Puskar","Mukesh",
                 "Ramesh","Sunil","Bishnu","Pawan","Sagar","Rupak","Mandip"]

female_first = ["Sita","Kamala","Sunita","Anita","Priya","Gita","Sarita",
                 "Mina","Rekha","Puja","Asha","Nirmala","Sapana","Kabita",
                 "Manjushree","Sangita","Prabha","Kopila","Dipa","Lalita",
                 "Indira","Binita","Urmila","Chameli","Radha","Laxmi","Samjhana",
                 "Menuka","Sirjana","Pratibha","Rupa","Mamata","Ambika","Srijana",
                 "Nisha","Babita","Kripa","Juna","Anju","Sushila","Durga","Meena"]

last_names   = ["Shrestha","Adhikari","Gurung","Joshi","Tamang","Sharma","Karki",
                 "Thapa","Rai","Maharjan","Bhandari","Hamal","Koirala","Ghimire",
                 "Pandey","Upreti","Basnet","Lama","Magar","Chaudhary","Regmi",
                 "Pokhrel","Bhattarai","Dahal","Gautam","Silwal","Subedi","Sapkota",
                 "Aryal","Neupane","KC","Rijal","Chhetri","Timilsina","Limbu",
                 "Sunuwar","Rana","Luitel","Giri","Duwadi","Shah","Mandal","Tharu"]

toles = ["Baneshwor","Thamel","Lazimpat","Baluwatar","Chabahil","Koteshwor",
         "Kalanki","Kirtipur","Boudha","Naxal","Pulchowk","Jawalakhel",
         "Lakeside","Mahendrapool","Birtamod","Damak","Itahari","Dharan",
         "Butwal","Bhairahawa","Nepalgunj","Dhangadhi","Mahendranagar"]

organizations = [
    "Kathmandu Model School","Tribhuvan University","Patan Hospital",
    "Nepal Telecom","Lalitpur Engineering Office","Chitwan Medical College",
    "Nepal Police Headquarters","Nepal Army","Department of Revenue",
    "Kathmandu Nursing Home","Nepal Agriculture Office","Surkhet Government Office",
    "Morang Secondary School","Kathmandu Press","Jhapa Transport Company",
    "Rupandehi Road Project","Banke Hospital","Kaski Business Center",
    "Sunsari Pharmacy","Bhaktapur Hospital","Kathmandu Construction Company",
    "Lalitpur Legal Firm","Nepal Law Campus","Pokhara Campus",
    "Chitwan Secondary School","Dang Agriculture Cooperative",
    "Kailali Government Office","Dhanusha Municipality","Saptari Agriculture",
    "Kathmandu NGO Office","Western Region Hospital","Eastern Cooperative"
]

degree_by_level = {
    "Primary":   ["Grade 1","Grade 2","Grade 3","Grade 4","Grade 5",
                  "Grade 6","Grade 7","Grade 8"],
    "Secondary": ["SLC","SEE","Grade 9","Grade 10","+2 Science",
                  "+2 Management","+2 Humanities"],
    "Bachelor":  ["B.Ed","BBS","B.E. Civil","B.E. Computer","MBBS",
                  "B.Sc CSIT","B.Sc Nursing","LLB","BPA","B.Pharm",
                  "B.A.","B.Sc","B.Tech"],
    "Master":    ["M.Ed","MBS","M.E.","MD","M.Sc","LLM","MPA","MBA"],
    "PhD":       ["PhD Education","PhD Engineering","PhD Medicine",
                  "PhD Economics","PhD Science"]
}

institutions = [
    "Tribhuvan University","Kathmandu University","Pokhara University",
    "Purbanchal University","Mid-Western University","Far-Western University",
    "Pulchowk Engineering Campus","BPKIHS Dharan","Kathmandu Medical College",
    "Manipal College of Medical Sciences","Nepal Law Campus",
    "Mahendra Multiple Campus","Mahendra Morang Campus","Janakpur Campus",
    "Pokhara Campus","Western Regional Campus","Butwal Campus",
    "Dhangadhi Campus","Nepalgunj Campus","Birendra Campus"
]

ward_offices = [
    "Kathmandu Ward 10 Office","Lalitpur Ward 3 Office","Pokhara Ward 6 Office",
    "Chitwan Ward 8 Office","Bhaktapur Ward 1 Office","Jhapa Ward 2 Office",
    "Morang Ward 5 Office","Surkhet Ward 9 Office","Banke Ward 8 Office",
    "Rupandehi Ward 11 Office","Dhanusha Ward 2 Office","Kailali Ward 9 Office",
    "Saptari Ward 2 Office","Dang Ward 6 Office","Sunsari Ward 5 Office"
]


def rand_name(gender):
    first = random.choice(male_first if gender == 'M' else female_first)
    last  = random.choice(last_names)
    return f"{first} {last}"

def rand_citizenship(district_id, birth_year, has_citizenship):
    if not has_citizenship:
        return "NULL"
    code = districts[district_id][:3].upper()
    num  = random.randint(1000, 9999)
    return f"'{code}-{num}-{birth_year}'"

def rand_date(start_year, end_year):
    year  = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day   = random.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"

def esc(s):
    """Escape single quotes in strings."""
    return s.replace("'", "''")

# ────────────────────────────────────────
# GENERATION CONFIG
# ────────────────────────────────────────
# person_id starts at 101 (your existing data is 1-100)
START_ID     = 101
TOTAL        = 200   # how many new persons to generate
# tweak ratios below
MINOR_RATIO      = 0.15  # 15% minors (no citizenship, born after 2008)
ELDERLY_RATIO    = 0.08  # 8%  elderly (born before 1960)
OTHER_G_RATIO    = 0.05  # 5%  other gender
EMPLOYED_RATIO   = 0.60  # 60% of adults get employment
ORPHAN_RATIO     = 0.20  # 20% of minors are orphans in birth registration
UNEDUCATED_RATIO = 0.15  # 15% have no education row

# ────────────────────────────────────────
# BUILD PERSONS
# ────────────────────────────────────────
persons       = []   # (person_id, name, gender, citizenship, address_id, district_id, birth_year, is_minor, is_elderly)
employment    = []
education     = []
birth_regs    = []
marriages     = []
parent_child  = []

# track married persons to avoid duplicate marriages
married = set()
# track adults available as parents (person_id, gender)
adult_males   = []
adult_females = []

person_id = START_ID

for i in range(TOTAL):
    # decide type
    r = random.random()
    if r < MINOR_RATIO:
        ptype = "minor"
    elif r < MINOR_RATIO + ELDERLY_RATIO:
        ptype = "elderly"
    elif r < MINOR_RATIO + ELDERLY_RATIO + OTHER_G_RATIO:
        ptype = "other"
    else:
        ptype = "adult"

    # gender
    if ptype == "other":
        gender = "O"
    else:
        gender = random.choice(["M", "F"])

    # birth year
    if ptype == "minor":
        birth_year = random.randint(2008, 2015)
        has_cit    = False
    elif ptype == "elderly":
        birth_year = random.randint(1935, 1959)
        has_cit    = True
    else:
        birth_year = random.randint(1960, 2000)
        has_cit    = True

    district_id = random.choice(list(districts.keys()))
    address_id  = random.randint(1, ADDRESS_MAX)
    name        = rand_name(gender)
    citizenship = rand_citizenship(district_id, birth_year, has_cit)

    persons.append({
        "id":         person_id,
        "name":       name,
        "gender":     gender,
        "cit":        citizenship,
        "address_id": address_id,
        "district_id":district_id,
        "birth_year": birth_year,
        "type":       ptype,
    })

    if ptype in ("adult", "elderly") and gender == "M":
        adult_males.append(person_id)
    if ptype in ("adult", "elderly") and gender == "F":
        adult_females.append(person_id)

    person_id += 1

# ────────────────────────────────────────
# BUILD EMPLOYMENT (adults + elderly only)
# ────────────────────────────────────────
for p in persons:
    if p["type"] == "minor":
        continue
    if p["gender"] == "O" and random.random() > 0.5:
        continue
    if random.random() > EMPLOYED_RATIO:
        continue   # unemployed

    prof_id  = random.choice(list(professions.keys()))
    lo, hi   = salary_range[prof_id]
    salary   = round(random.uniform(lo, hi), 2)
    org      = random.choice(organizations)
    employment.append((org, salary, p["id"], prof_id))

# ────────────────────────────────────────
# BUILD EDUCATION
# ────────────────────────────────────────
for p in persons:
    if random.random() < UNEDUCATED_RATIO:
        continue  # intentionally uneducated

    if p["type"] == "minor":
        # only primary
        deg  = random.choice(degree_by_level["Primary"])
        inst = random.choice(institutions)
        yrs  = random.randint(1, 8)
        education.append((deg, "Primary", inst, yrs, p["id"]))

    elif p["type"] == "elderly":
        # SLC only
        education.append(("SLC", "Secondary", random.choice(institutions), 10, p["id"]))

    else:
        # adults — build up levels
        levels = ["Secondary"]
        r = random.random()
        if r < 0.7:
            levels.append("Bachelor")
        if r < 0.4:
            levels.append("Master")
        if r < 0.05:
            levels.append("PhD")

        for lvl in levels:
            deg  = random.choice(degree_by_level[lvl])
            inst = random.choice(institutions)
            yrs  = {"Secondary":10,"Bachelor":4,"Master":2,"PhD":4}[lvl]
            education.append((deg, lvl, inst, yrs, p["id"]))

# ────────────────────────────────────────
# BUILD BIRTH REGISTRATION
# ────────────────────────────────────────
# pair some adult males + females as parents for minors
minor_ids = [p["id"] for p in persons if p["type"] == "minor"]

for pid in [p["id"] for p in persons]:
    p = next(x for x in persons if x["id"] == pid)
    birth_date = rand_date(p["birth_year"], p["birth_year"])

    if p["type"] == "minor":
        r = random.random()
        if r < ORPHAN_RATIO:
            # orphan
            birth_regs.append((birth_date, random.choice(ward_offices), pid, "NULL", "NULL"))
        elif r < ORPHAN_RATIO + 0.1:
            # single mother
            mother = random.choice(adult_females) if adult_females else "NULL"
            birth_regs.append((birth_date, random.choice(ward_offices), pid, mother, "NULL"))
        elif r < ORPHAN_RATIO + 0.2:
            # single father
            father = random.choice(adult_males) if adult_males else "NULL"
            birth_regs.append((birth_date, random.choice(ward_offices), pid, "NULL", father))
        else:
            # both parents
            mother = random.choice(adult_females) if adult_females else "NULL"
            father = random.choice(adult_males)   if adult_males   else "NULL"
            birth_regs.append((birth_date, random.choice(ward_offices), pid, mother, father))
    else:
        # adults/elderly — no parent records (born before system)
        birth_regs.append((birth_date, random.choice(ward_offices), pid, "NULL", "NULL"))

# ────────────────────────────────────────
# BUILD MARRIAGE REGISTRATION
# ────────────────────────────────────────
# pair adult males and females randomly
# some get married twice (remarriage)
available_males   = [p["id"] for p in persons if p["type"] == "adult" and p["gender"] == "M"]
available_females = [p["id"] for p in persons if p["type"] == "adult" and p["gender"] == "F"]

random.shuffle(available_males)
random.shuffle(available_females)

pairs = min(len(available_males), len(available_females))
pairs = int(pairs * 0.65)  # 65% of adults get married

for i in range(pairs):
    m  = available_males[i]
    f  = available_females[i]
    yr = random.randint(1990, 2023)
    marriages.append((rand_date(yr, yr), random.choice(ward_offices), m, f))
    married.add(m)
    married.add(f)

# remarriage — pick 10% of married males and marry again
remarry_count = max(1, int(pairs * 0.10))
remarry_males = random.sample([m for m in available_males[:pairs] if m in married], min(remarry_count, len(available_males[:pairs])))
extra_females  = [p["id"] for p in persons if p["type"] == "adult" and p["gender"] == "F" and p["id"] not in married]

for m in remarry_males:
    if not extra_females:
        break
    f  = random.choice(extra_females)
    yr = random.randint(2010, 2024)
    marriages.append((rand_date(yr, yr), random.choice(ward_offices), m, f))
    extra_females.remove(f)

# ────────────────────────────────────────
# BUILD PARENT-CHILD
# ────────────────────────────────────────
# use birth registration data to derive parent-child rows
for (bd, wo, child, mother, father) in birth_regs:
    p = next(x for x in persons if x["id"] == child)
    if p["type"] != "minor":
        continue
    if father != "NULL":
        parent_child.append((child, father, "father", "TRUE"))
    if mother != "NULL":
        parent_child.append((child, mother, "mother", "TRUE"))

# add some guardian rows for orphans
orphan_ids    = [br[2] for br in birth_regs if br[3] == "NULL" and br[4] == "NULL"
                 and next(x for x in persons if x["id"] == br[2])["type"] == "minor"]
guardian_pool = [p["id"] for p in persons if p["type"] == "adult"]

for oid in orphan_ids[:10]:  # assign guardians to first 10 orphans
    if not guardian_pool:
        break
    guardian = random.choice(guardian_pool)
    parent_child.append((oid, guardian, "guardian", "FALSE"))

# ────────────────────────────────────────
# WRITE OUTPUT FILE
# ────────────────────────────────────────
with open("seed_data.txt", "w", encoding="utf-8") as f:

    f.write("-- ============================================================\n")
    f.write(f"-- seed_data.txt — Auto generated {TOTAL} persons\n")
    f.write(f"-- person_id range: {START_ID} to {START_ID + TOTAL - 1}\n")
    f.write("-- Run AFTER all existing seed files\n")
    f.write("-- ============================================================\n\n")

    # ── Person ──
    f.write(f"-- ── PERSON ({len(persons)} rows) ──────────────────────────\n")
    for p in persons:
        f.write(
            f"INSERT INTO Person(name, gender, citizenship_no, address_id, district_id) "
            f"VALUES('{esc(p['name'])}', '{p['gender']}', {p['cit']}, "
            f"{p['address_id']}, {p['district_id']});\n"
        )

    # ── Employment ──
    f.write(f"\n-- ── EMPLOYMENT ({len(employment)} rows) ─────────────────\n")
    for org, sal, pid, prof in employment:
        f.write(
            f"INSERT INTO Employment(organization, salary, person_id, profession_id) "
            f"VALUES('{esc(org)}', {sal}, {pid}, {prof});\n"
        )

    # ── Education ──
    f.write(f"\n-- ── EDUCATION ({len(education)} rows) ───────────────────\n")
    for deg, lvl, inst, yrs, pid in education:
        f.write(
            f"INSERT INTO Education(degree_name, level, institution_name, years_completed, person_id) "
            f"VALUES('{esc(deg)}', '{lvl}', '{esc(inst)}', {yrs}, {pid});\n"
        )

    # ── BirthRegistration ──
    f.write(f"\n-- ── BIRTH REGISTRATION ({len(birth_regs)} rows) ─────────\n")
    for bd, wo, child, mother, father in birth_regs:
        f.write(
            f"INSERT INTO BirthRegistration(birth_date, ward_office, child_id, mother_id, father_id) "
            f"VALUES('{bd}', '{esc(wo)}', {child}, {mother}, {father});\n"
        )

    # ── MarriageRegistration ──
    f.write(f"\n-- ── MARRIAGE REGISTRATION ({len(marriages)} rows) ───────\n")
    for md, wo, p1, p2 in marriages:
        f.write(
            f"INSERT INTO MarriageRegistration(marriage_date, ward_office, person1_id, person2_id) "
            f"VALUES('{md}', '{esc(wo)}', {p1}, {p2});\n"
        )

    # ── ParentChild ──
    f.write(f"\n-- ── PARENT CHILD ({len(parent_child)} rows) ─────────────\n")
    for child, parent, rel, bio in parent_child:
        f.write(
            f"INSERT INTO ParentChild(child_id, parent_id, relation_type, is_biological) "
            f"VALUES({child}, {parent}, '{rel}', {bio});\n"
        )

    f.write("\n-- ============================================================\n")
    f.write(f"-- Summary\n")
    f.write(f"-- Persons        : {len(persons)}\n")
    f.write(f"-- Employment     : {len(employment)}\n")
    f.write(f"-- Education      : {len(education)}\n")
    f.write(f"-- BirthReg       : {len(birth_regs)}\n")
    f.write(f"-- MarriageReg    : {len(marriages)}\n")
    f.write(f"-- ParentChild    : {len(parent_child)}\n")
    f.write("-- ============================================================\n")

print("Done! seed_data.txt generated.")
print(f"  Persons     : {len(persons)}")
print(f"  Employment  : {len(employment)}")
print(f"  Education   : {len(education)}")
print(f"  BirthReg    : {len(birth_regs)}")
print(f"  MarriageReg : {len(marriages)}")
print(f"  ParentChild : {len(parent_child)}")