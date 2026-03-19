import json
import random
district_id_map = {
    # Koshi Province
    "Bhojpur": 1, "Dhankuta": 2, "Ilam": 3, "Jhapa": 4,
    "Khotang": 5, "Morang": 6, "Okhaldhunga": 7, "Panchthar": 8,
    "Sankhuwasabha": 9, "Solukhumbu": 10, "Sunsari": 11,
    "Taplejung": 12, "Terhathum": 13, "Udayapur": 14,
    # Madhesh Province
    "Bara": 15, "Dhanusa": 16, "Mahottari": 17, "Parsa": 18,
    "Rautahat": 19, "Saptari": 20, "Sarlahi": 21, "Siraha": 22,
    # Bagmati Province
    "Bhaktapur": 23, "Chitwan": 24, "Dhading": 25, "Dolakha": 26,
    "Kathmandu": 27, "Kavrepalanchok": 28, "Lalitpur": 29,
    "Makwanpur": 30, "Nuwakot": 31, "Ramechhap": 32,
    "Rasuwa": 33, "Sindhuli": 34, "Sindhupalchok": 35,
    # Gandaki Province
    "Baglung": 36, "Gorkha": 37, "Kaski": 38, "Lamjung": 39,
    "Manag": 40, "Mustang": 41, "Myagdi": 42, "Nawalpur": 43,
    "Parbat": 44, "Syangja": 45, "Tanahu": 46,
    # Lumbini Province
    "Arghakhanchi": 47, "Banke": 48, "Bardiya": 49, "Dang": 50,
    "Eastern Rukum": 51, "Gulmi": 52, "Kapilbastu": 53,
    "Palpa": 54, "Parasi": 55, "Pyuthan": 56, "Rolpa": 57,
    "Rupandehi": 58,
    # Karnali Province
    "Dolpa": 59, "Humla": 60, "Jajarkot": 61, "Jumla": 62,
    "Kalikot": 63, "Mugu": 64, "Salyan": 65, "Surkhet": 66,
    "Western Rukum": 67,
    # Sudurpashchim Province
    "Achham": 68, "Baitadi": 69, "Bajhang": 70, "Bajura": 71,
    "Dadeldhura": 72, "Darchula": 73, "Doti": 74,
    "Kailali": 75, "Kanchanpur": 76
}
try:
    with open("Address.json",'r',encoding='utf-8') as f:
        data=json.load(f)
except FileNotFoundError:
    print("Error: english.Json not found.")
    exit(1)
addresses=set()
skipped_district=set()
for province,districts in data.items():
    for district,municipalities in districts.items():
        if district not in district_id_map:
            skipped_district.add(district)
            continue
    for municipality,wards in municipalities.items():
        for ward in wards:
            addresses.add((district,municipality,str(ward)))

addresses=list(addresses)
if skipped_district:
    print(f"WARNING: These districts in english.json were not found in your map:")
    for d in sorted(skipped_district):
        print(f" {d}")
    print("Fix spelling in district_id_map to include them.\n")
 
print(f"Total available address combinations: {len(addresses)}")
SAMPLE_SIZE = 500
 
if len(addresses) < SAMPLE_SIZE:
    print(f"WARNING: Only {len(addresses)} addresses available, using all of them.")
    sample = addresses
else:
    sample = random.sample(addresses, SAMPLE_SIZE)
 
print(f"Generating {len(sample)} address rows...\n")

with open("address.txt", "a", encoding="utf-8") as f:
    for i, (district, municipality, ward) in enumerate(sample, start=1):
        district_id = district_id_map[district]
        tole = f"Tole {i}"
        f.write(
            f"INSERT IGNORE INTO Address(district_id, municipality, ward, tole) "
            f"VALUES({district_id}, '{municipality}', '{ward}', '{tole}');\n"
        )

    