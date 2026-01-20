import pandas as pd

from data_parsing import read_data

DATA_PATH = "data.csv"

people, families = read_data(DATA_PATH)

# Sort people by family ID for faster search lookup
people.sort(key=lambda p: p.family_id)

photos = []
family_labels = []
for family_num in families.keys():
    family = []

    # Search for people with same family ID assuming the list is sorted
    found_someone = False
    for person in people:
        if person.family_id == family_num:
            found_someone = True
            family.append(person)
        elif found_someone:
            break

    # Create a label for the family in the form:
    # `lastname, primary firstname, spouse firstname, other firstname...`
    # and find what the filename should be for the family photo
    label = families[family_num]  # Start with the the lastname

    family.sort(key=lambda p: p.is_primary, reverse=True)
    if family[0].is_primary:
        label += ", " + family[0].firstname
        family.pop(0)

    if len(family) > 0:
        family.sort(key=lambda p: p.is_spouse, reverse=True)
        if family[0].is_spouse:
            label += ", " + family[0].firstname
            family.pop(0)

    for member in family:
        label += ", " + family[0].firstname
        family.pop(0)


    family_labels.append(label)
    print(label)
