from flask import Flask, render_template, request
import random
from faker import Faker

app = Flask(__name__)

# Create objects
fake = Faker('fr_FR')

def generate_insee_number(date_of_birth, department, commune, birth_order):
    year = str(date_of_birth.year % 100).zfill(2)  # Year in YY format with leading zero
    month = date_of_birth.month
    day = date_of_birth.day
    sexe = 1 if date_of_birth.year >= 2000 else 2  # 1 for male, 2 for female
    return f"{sexe}{year}{month:02d}{department:02d}{commune:03d}{birth_order:03d}"

def generate_random_insee(date_of_birth):
    department = int(fake.department_number())
    commune = random.randint(1, 999)
    birth_order = random.randint(1, 999)
    return generate_insee_number(date_of_birth, department, commune, birth_order)

def generate_mobile_number():
    return "https://online-sms.org/fr/Free-FR-Phone-Number"

def generate_temp_email_address():
    return "https://temp-mail.org/en/"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Number of identities to generate
        num_identities = int(request.form.get('num_identities'))

        # Generate fake data
        fakeData = []
        for _ in range(num_identities):
            date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=90)
            identity = {
                'name': fake.name(),
                'email': fake.email(),
                'phone_number': fake.phone_number(),
                'mobile_number': generate_mobile_number(),
                'address': fake.address(),
                'date_of_birth': date_of_birth.strftime("%Y-%m-%d"),
                'insee_number': generate_random_insee(date_of_birth),
                'credit_card': {
                    'number': fake.credit_card_number(),
                    'expiry_date': fake.credit_card_expire(start="now", end="+10y"),
                    'cvv': fake.credit_card_security_code(),
                    'provider': fake.credit_card_provider()
                }
            }
            fakeData.append(identity)

        return render_template('index.html', fakeData=fakeData, num_identities=num_identities, temp_email_url=generate_temp_email_address())
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
