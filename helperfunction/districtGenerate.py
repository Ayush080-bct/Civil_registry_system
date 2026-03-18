districts_by_province = {
    "Koshi Province": [
        "Bhojpur", "Dhankuta", "Ilam", "Jhapa", "Khotang", "Morang",
        "Okhaldhunga", "Panchthar", "Sankhuwasabha", "Solukhumbu",
        "Sunsari", "Taplejung", "Terhathum", "Udayapur"
    ],
    "Madhesh Province": [
        "Bara", "Dhanusha", "Mahottari", "Parsa", "Rautahat",
        "Saptari", "Sarlahi", "Siraha"
    ],
    "Bagmati Province": [
        "Bhaktapur", "Chitwan", "Dhading", "Dolakha", "Kathmandu",
        "Kavrepalanchok", "Lalitpur", "Makwanpur", "Nuwakot",
        "Ramechhap", "Rasuwa", "Sindhuli", "Sindhupalchok"
    ],
    "Gandaki Province": [
        "Baglung", "Gorkha", "Kaski", "Lamjung", "Manang",
        "Mustang", "Myagdi", "Nawalpur", "Parbat", "Syangja",
        "Tanahun"
    ],
    "Lumbini Province": [
        "Arghakhanchi", "Banke", "Bardiya", "Dang", "Eastern Rukum",
        "Gulmi", "Kapilvastu", "Palpa", "Parasi", "Pyuthan",
        "Rolpa", "Rupandehi"
    ],
    "Karnali Province": [
        "Dolpa", "Humla", "Jajarkot", "Jumla", "Kalikot",
        "Mugu", "Salyan", "Surkhet", "Western Rukum"
    ],
    "Sudurpashchim Province": [
        "Achham", "Baitadi", "Bajhang", "Bajura", "Dadeldhura",
        "Darchula", "Doti", "Kailali", "Kanchanpur"
    ]
}
with open("district.txt","a") as f:
    for province,districts in districts_by_province.items():
        for district in districts:
            f.write(f"INSERT IGNORE INTO district(district_name,province) values('{district}','{province}');\n")
        
        