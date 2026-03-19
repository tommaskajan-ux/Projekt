from app import app, db, bcrypt
from app.models import User, Faculty

with app.app_context():
    fai = Faculty.query.filter_by(code='FAI').first()

    if not fai:
        print("FAI faculty does not exist. Run seed.py first.")
    else:
        existing_user = User.query.filter_by(email='t_kajan@utb.cz').first()

        if existing_user:
            print("Test user already exists.")
        else:
            hashed_password = bcrypt.generate_password_hash('Password123').decode('utf-8')

            user = User(
                first_name='Tomas',
                last_name='Kajan',
                username='tkajan',
                email='t_kajan@utb.cz',
                password=hashed_password,
                faculty_id=fai.id,
                is_active=True,
                failed_logins=0
            )

            db.session.add(user)
            db.session.commit()
            print("Test user created successfully.")