from flask import Flask, render_template, request
import pandas as pd
from faker import Faker
from tempmail import TempMail
import random

app = Flask(__name__)

# Create objects
fake = Faker('fr_FR')
tm = TempMail()

def generate_insee_number(sexe: int, year: int, month: int, department: int, commune: int, birth_order: int):
    return f"{sexe:02d}{year:02d}{month:02d}{department:02d}{commune:02d}{birth_order:03d}"

def generate_random_insee():
    sexe = random.choice([1, 2])  # 1 for male, 2 for female
    year = random.randint(50, 99)  # for years 1950-1999
    month = random.randint(1, 12)
    department = int(fake.department_number())
    commune = random.randint(1, 999)
    birth_order = random.randint(1, 999)
    return generate_insee_number(sexe, year, month, department, commune, birth_order)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Number of identities to generate
        num_identities = int(request.form.get('num_identities'))

        # Generate fake data
        fakeData = []
        for _ in range(num_identities):
            identity = {
                'name': fake.name(),
                ' email': fake.email(),
                'phone_number': fake.phone_number(),
                'address': fake.address(),
                'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=90),
                'insee_number': generate_random_insee(),
                'credit_card': {
                    'number': fake.credit_card_number(),
                    'expiry_date': fake.credit_card_expire(start="now", end="+10y"),
                    'cvv': fake.credit_card_security_code(),
                    'provider': fake.credit_card_provider()
                }
            }
            fakeData.append(identity)

        return render_template('index.html', fakeData=fakeData)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
