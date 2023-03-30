from random import choice as rc
from faker import Faker
from app import app
from models import Owner, Pet, db

fake = Faker()

with app.app_context():
    print("Destroying existing pets")
    Pet.query.delete()
    print("Done ✅")

    print("Destroying existing owners")
    Owner.query.delete()
    print("Done ✅")

    owners = []
    print("Creating owners")
    for n in range(50):
        owner = Owner(name=fake.name())
        owners.append(owner)
    print("Done ✅")

    print("Adding Owners to the session")
    db.session.add_all(owners)
    print("Done ✅")

    pets = []
    species = ['Dog', 'Cat', 'Chicken', 'Hamster', 'Turtle']
    print("Creating pets")
    for n in range(50):
        pet = Pet(name=fake.first_name(), species=rc(species), owner=rc(owners))
        pets.append(pet)
    print("Done ✅")
    
    print("Adding Pets to the session")
    db.session.add_all(pets)
    print("Done ✅")

    print("Committing the session")
    db.session.commit()
    print("All Done ✅")