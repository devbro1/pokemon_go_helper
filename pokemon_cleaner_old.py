import pytesseract
from PIL import Image
import csv
import sqlite3
import subprocess
import re


def readPokemonDetails(filename):
    rc = {}
    img = Image.open(filename)

    cropped_img = img.crop((398, 1039, 681, 1108))
    rc['name'] = re.sub(r'\s', '', pytesseract.image_to_string(cropped_img))

    cropped_img = img.crop((250, 253, 800, 351))
    rc['cp'] = re.sub(r'\D', '', pytesseract.image_to_string(cropped_img))

    cropped_img = img.crop((410, 1164, 705, 1204))
    rc['health'] = re.findall(r'\d+',pytesseract.image_to_string(cropped_img))[1]

    rc['attack'] = 0
    rc['defense'] = 0
    rc['hp'] = 0

    return rc

def calculateMaxStatProduct(pokemon_name,max_cp):

    base_values = getBaseValues(pokemon_name)

    rc = {}
    rc['stat_product'] = 0
    rc['level'] = 0
    rc['attack'] = 0
    rc['defense'] = 0
    rc['stamina'] = 0
    rc['cp'] = 0

    rc2 = []
    

    for level in range(50):
        for ind_attack in range(16):
            for ind_defense in range(16):
                for ind_stamina in range(16):
                    attack = ind_attack + base_values['attack']
                    defense = ind_defense + base_values['defense']
                    stamina = ind_stamina + base_values['stamina']
                    cp_multiplier = getCPMultiplier(level)

                    cp = pow(attack,1) * pow(defense,0.5) * pow(stamina,0.5) * pow(cp_multiplier) / 10
                    if(max_cp < cp):
                        break
                    
                    cp_attack = attack * cp_multiplier
                    cp_defense = defense * cp_multiplier
                    cp_stamina = stamina * cp_multiplier

                    stat_product = cp_attack * cp_defense * cp_stamina
                    

                    if(rc['stat_product'] == stat_product):
                        rc2.push({'level': level, 'cp': cp, 'stat_product': stat_product, 'attack': attack, 'defense': defense, 'stamina': stamina})
                    elif(rc['stat_product'] <stat_product):
                        rc = {'level': level, 'cp': cp, 'stat_product': stat_product, 'attack': attack, 'defense': defense, 'stamina': stamina}
                        rc2 = []

    if 0 == rc2.length:
        rc = [rc]

    return rc


def loadPokegenieData(conn):
    with open('poke_genie_export.csv', 'r') as file:

        # Create a CSV reader
        reader = csv.reader(file)

        # Connect to the SQLite database

        # Create a cursor
        c = conn.cursor()

        c.execute('''DROP TABLE IF EXISTS pokemons;''')

        # Create a table to store the data
        c.execute('''CREATE TABLE IF NOT EXISTS pokemons
                    (id INTEGER,
    name TEXT,
    form TEXT,
    pokemon TEXT,
    gender TEXT,
    cp INTEGER,
    hp INTEGER,
    atk_iv INTEGER,
    def_iv INTEGER,
    sta_iv INTEGER,
    iv_avg REAL,
    level_min REAL,
    level_max REAL,
    quick_move TEXT,
    charge_move TEXT,
    charge_move_2 TEXT,
    scan_date DATE,
    catch_date DATE,
    weight REAL,
    height REAL,
    lucky INTEGER,
    shadow_purified TEXT,
    favorite INTEGER,
    dust INTEGER,
    rank_percent_g REAL,
    rank_number_g INTEGER,
    stat_product_g INTEGER,
    dust_cost_g INTEGER,
    candy_cost_g INTEGER,
    name_g TEXT,
    form_g TEXT,
    sha_pur_g TEXT,
    rank_percent_u REAL,
    rank_number_u INTEGER,
    stat_product_u INTEGER,
    dust_cost_u INTEGER,
    candy_cost_u INTEGER,
    name_u TEXT,
    form_u TEXT,
    sha_pur_u TEXT,
    rank_percent_l REAL,
    rank_number_l INTEGER,
    stat_product_l INTEGER,
    dust_cost_l INTEGER,
    candy_cost_l INTEGER,
    name_l TEXT,
    form_l TEXT,
    sha_pur_l TEXT,
    marked_for_pvp_use INTEGER);''')

        # Loop over the rows in the CSV file and insert them into the database
        for row in reader:
            c.execute('INSERT INTO pokemons VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       row)

        # Commit the changes and close the connection
        conn.commit()




marked_for_transfer = set()
conn = sqlite3.connect('example.db')

loadPokegenieData(conn)

c = conn.cursor()

for i in range(20):
    pokemon = {}
    try:
        takeScreenshot()
        pokemon = readPokemonDetails('screenshot.png')
        print(pokemon)
        c.execute("SELECT * FROM pokemons where name = '"+pokemon['name']+"' and cp = "+pokemon['cp']+";")
    except:
        continue

    #find pokemon in export file
    rows = c.fetchall()
    column_names = [description[0] for description in c.description]

    if (len(rows) > 1):
        print("too many matches")
    elif (len(rows) == 0):
        print("not found")
    else:
        row = {}
        for i, value in enumerate(rows[0]):
            row[column_names[i]] = value

        print(row)

        if(row['iv_avg'] < 90.0 and row['rank_percent_g'] < 90.0 and row['rank_percent_u'] < 90.0 and row['rank_percent_l'] < 90.0):
            tagDelete()

    gotoNext()
        





# Close the connection
conn.close()

#decide if want to keep or delete


    #if delete mark add tag for delete