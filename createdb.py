import sqlite3
con = sqlite3.connect("clinic.db")
from random import randint,randrange
from datetime import date

c = con.cursor()

# Build entire list for lastNames, femaleNames, maleNames, swab_test, serology_test, genders
lastNames = ["Wilson","Vance","Smith","Rees","Peter","Oliver","Miller","Jones","Ince","Gray"]
femaleNames = ["Audrey","Carol","Fiona","Karen","Mary"]
maleNames = ["Boris","David","Jack","Liam","Nicholas"]
names = [femaleNames,maleNames]
swab_test = ["P","N"]
serology_test = ["P","N"]
genders = ["M","F"]
patients = []

# Genereate 10 patients with random attributes
for i in range(10):
    lastName = lastNames[randint(0,9)]
    gender = randint(0,1)
    firstName = names[gender][randint(0,9)]
    sex = genders[gender]
    age = randint(18,60)
    birthdate = date((2020 - age), randint(1,12), randint(1,31)).isoformat()
    swab = randint(0,1)
    serology = randint(0,1)
    st = swab_test[swab]
    srlt = serology_test[serology]
    patient = (i,firstName,lastName,birthdate,age,sex,st,srlt)
    print(patient)
    patients.append(patient)

# Drop previous Table
c.execute('''DROP TABLE patient''')

# Create next Table
c.execute('''CREATE TABLE patient
         (id integer primary key autoincrement, firstname text, lastname text, birthdate text, age integer, sex text, st text, srlt text)''')

# Insert entire 10 rows of data
c.executemany('INSERT INTO patient VALUES (?,?,?,?,?,?,?,?)', patient)

# Save (commit) the changes
con.commit()

con.close()