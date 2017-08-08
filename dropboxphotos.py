import dropbox
from os import listdir


def connect_to_dropbox(token):
    return dropbox.Dropbox(token)


def get_missing_category(list_dropbox, list_local):
    missing = []
    lower_case_list_local = []
    for elem in list_local:
        lower_case_list_local.append(elem.lower())

    for elem in lower_case_list_local:
        if elem not in list_dropbox:
            missing.append(elem)
    return missing


def compare_dropbox_and_local(dbx, root_directory_dropbox, root_directory_local):
    missing = {}
    for year in dbx.files_list_folder(root_directory_dropbox).entries:
        list_dropbox = []
        list_local = listdir(root_directory_local + '\\' + year.name)
        for category in dbx.files_list_folder(root_directory_dropbox + '/' + year.name).entries:
            list_dropbox.append(category.name.lower())
        missing_categories = get_missing_category(list_dropbox, list_local)
        if (missing_categories != []):
            missing[year.name] = missing_categories
    return missing


def upload_new_folder(dbx, from_folder, to_folder, display_progress = True):
    list_files = listdir(from_folder)

    #remove thumbs.db if it exists
    try:
        index = list_files.index("Thumbs.db")
        if index != -1:
            del(list_files[index])
    except ValueError as e:
        pass

    if display_progress == True:
        print("copie de : " + str(len(list_files)) + " fichiers", flush = True)

    try:
        dbx.files_create_folder(to_folder)
    except Exception as e:
        print(e)
        return

    number = 1
    for file_name in list_files:
        try:
            file = open(from_folder + '\\' + file_name, "rb")
            bytes_read = file.read(100*1024*1024)
            file.close()
            dbx.files_upload(bytes_read, to_folder + '/' + file_name)
            if display_progress == True:
                print(str(number), flush = True)
                number += 1
        except Exception as e:
            print(e, flush = True)
            if display_progress == True:
                print("echec de transfert du fichier " + file_name, flush = True)
    if display_progress == True:
        print("copie du repertoire finie")

