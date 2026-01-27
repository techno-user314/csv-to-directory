import pandas as pd
import json

try:
    with open("special_cases.json", "r", encoding="utf-8") as file:
        special_cases = json.load(file)
except FileNotFoundError:
    print("File not found: special_cases.json")
except json.JSONDecodeError as e:
    print("Invalid JSON:", e)

class Person:
    def __init__(self, first_name, last_name, is_primary=False, is_spouse=False):
        self.lastname = last_name
        self.firstname = first_name
        self.formalname = first_name

        self.is_primary = is_primary
        self.is_spouse = is_spouse
        self.family_id = None
        self.family = []

        self.mobile_number = ""
        self.email = ""
        self.address = ""
        self.city = ""
        self.state = ""
        self.zip_code = ""

    def set_preferred_name(self, name):
        self.firstname = name
        
    def set_contact(self, phone, email):
        self.mobile_number = phone
        self.email = email

    def set_address(self, address, city, state, zip_code):
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def set_family(self, fid_num, family_member_names):
        self.family_id = fid_num
        self.family = family_member_names

    def __str__(self):
        return (f"{self.firstname} {self.lastname}")

def read_data(csv_path):
    df = pd.read_csv(csv_path)

    people = []  # List of People objects
    families = {}  # Dictionary of unique family ID's with thier lastname
    no_family = 0 # Count of people without a famliy ID number. Used to give them a fake ID
    for index, row in df.iterrows():
        # Create a new person with information that will
        # be compiled later for the contact info section
        if not pd.isnull(row["Died On"]):
            continue  # Skip dead people
        firstname = row["First Name"]
        lastname = row["Last Name"]

        # Create info for the person
        fam_rel = row["Family Relationship"]
        new_person = Person(firstname, lastname,
                            is_primary=(fam_rel == "Primary" or fam_rel == "Husband"),
                            is_spouse=(fam_rel == "Wife"))
        if not pd.isnull(row["Preferred Name"]):
            new_person.set_preferred_name(row["Preferred Name"])
        new_person.set_contact(row["Cell Phone"], row["Email"])
        new_person.set_address(row["Address"], row["City"], row["State"], row["Zip Code"])

        # Update family info
        if not pd.isnull(row["Family ID"]):
            if not pd.isnull(row["Family Members"]):
                new_person.set_family(row["Family ID"], row["Family Members"].split(", "))
            else:
                new_person.set_family(row["Family ID"], [firstname])
            if row["Family ID"] not in families.keys():
                families.update({row["Family ID"]:lastname})
        else:
            no_family += 1
            new_person.set_family(-no_family, [firstname])
            new_person.is_primary = True
            families.update({-no_family: lastname})

        people.append(new_person)

    # Ignore people/families who have requested it
    dont_include = special_cases["ignore family"]
    for person in people:
        if person.formalname + " " + person.lastname in dont_include \
                or person.firstname + " " + person.lastname in dont_include:
            print(f"Excluding the family of {person} from directory")
            families.pop(person.family_id)
    people = [p for p in people if p.family_id in families.keys()]

    # Change the info for people who have requested it
    change = special_cases["change info"]
    for info in ["email", "phone", "address"]:
        for update in change[info]:
            for person in people:
                if person.formalname + " " + person.lastname == update["name"] \
                        or person.firstname + " " + person.lastname == update["name"]:
                    setattr(person, info, update["new info"])
                    break

    return people, families
