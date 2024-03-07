from main import User, fake_hash_password, SessionLocal

fake_user = User(username="fakeuser", email="fakeuser@example.com", hashed_password=fake_hash_password("password"))

db = SessionLocal()
db.add(fake_user)
db.commit()
db.close()



























# from faker import Faker
# from main import User, fake_hash_password, db

# fake_user = User(username="fakeuser", email="fakeuser@example.com", hashed_password=fake_hash_password("password"))

# # db.add(fake_user)
# # db.commit()
# fake = Faker()

# def generate_fake_user():
#     return User(
#         username=fake.user_name(),
#         email=fake.email(),
#         hashed_password=fake_hash_password(fake.password()),
#     )

# # Generar 10 usuarios aleatorios e insertarlos en la base de datos
# for _ in range(10):
#     db_user = generate_fake_user()
#     db.add(db_user)
#     db.commit()
