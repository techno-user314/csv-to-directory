import os

def get_photo_path(family_member_list, lastname):
    # Create a label for the family in the form `lastname, firstname, firstname...`
    # and find what the filename should be for the family photo
    label = lastname
    photo_path = None

    # Check that all members expect the same family members
    expected_members = set(family_member_list[0].family)
    for member in family_member_list:
        if set(member.family) != expected_members:
            print(f"WARNING: {member} expected family={member.family} but directory is using: {expected_members}")

    # Add list of family members' firstnames to `label`
    for name in family_member_list[0].family:
        label += ", " + name

    # Find the family photo
    family_member_list.sort(key=lambda p: p.is_primary, reverse=True)
    if family_member_list[0].is_primary:
        member = family_member_list[0]

        try_path1 = f"Images/{lastname} {member.formalname}"
        try_path2 = f"Images/{lastname} {member.firstname}"
        if os.path.exists(f"{try_path1} family.jpg"):
            photo_path = f"{try_path1} family.jpg"
        elif os.path.exists(f"{try_path1}.jpg"):
            photo_path = f"{try_path1}.jpg"
        elif os.path.exists(f"{try_path2} family.jpg"):
            photo_path = f"{try_path2} family.jpg"
        elif os.path.exists(f"{try_path2}.jpg"):
            photo_path = f"{try_path2}.jpg"

    if photo_path is None:
        family_member_list.sort(key=lambda p: p.is_spouse, reverse=True)
        if family_member_list[0].is_spouse:
            member = family_member_list[0]
            try_path1 = f"Images/{lastname} {member.formalname}"
            try_path2 = f"Images/{lastname} {member.firstname}"
            if os.path.exists(f"{try_path1} family.jpg"):
                photo_path = f"{try_path1} family.jpg"
            elif os.path.exists(f"{try_path2} family.jpg"):
                photo_path = f"{try_path2} family.jpg"

    if photo_path is None:
        print(f"WARNING: No photo found for {lastname} {[str(p) for p in family_member_list]}")

    return photo_path, label
