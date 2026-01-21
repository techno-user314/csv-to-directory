import os

def get_photo_path(family_member_list, lastname):
    # Create a label for the family in the form `lastname, firstname, firstname...`
    # and find what the filename should be for the family photo
    label = lastname
    photo_path = None

    family_member_list.sort(key=lambda p: p.is_primary, reverse=True)
    if family_member_list[0].is_primary:
        member = family_member_list[0]
        label += ", " + member.firstname
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
        family_member_list.pop(0)

    if len(family_member_list) > 0:
        family_member_list.sort(key=lambda p: p.is_spouse, reverse=True)
        if family_member_list[0].is_spouse:
            member = family_member_list[0]
            label += ", " + member.firstname
            if photo_path is None:
                try_path1 = f"Images/{lastname} {member.formalname}"
                try_path2 = f"Images/{lastname} {member.firstname}"
                if os.path.exists(f"{try_path1} family.jpg"):
                    photo_path = f"{try_path1} family.jpg"
                elif os.path.exists(f"{try_path2} family.jpg"):
                    photo_path = f"{try_path2} family.jpg"
            family_member_list.pop(0)

    for member in family_member_list:
        label += ", " + family_member_list[0].firstname
        family_member_list.pop(0)

    if photo_path is None:
        print(f"No photo found for the {lastname}")
    
    return photo_path, label
