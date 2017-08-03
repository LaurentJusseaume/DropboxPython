import dropbox
from os import listdir


def connect_to_dropbox(token):
    return dropbox.Dropbox(token)


def print_missing_category(list_dropbox, list_local):
    missing = []
    for elem in list_dropbox:
        if elem not in list_local:
            missing.append(elem)
    return missing


def compare_dropbox_and_local(dbx, root_directory_dropbox, root_directory_local):
    missing = {}
    for year in dbx.files_list_folder(root_directory_dropbox).entries:
        list_dropbox = []
        list_local = listdir(root_directory_local + '\\' + year.name)
        for category in dbx.files_list_folder(root_directory_dropbox + '/' + year.name).entries:
            list_dropbox.append(category.name)
        missing_categories = print_missing_category(list_dropbox, list_local)
        if (missing_categories != []):
            missing[year.name] = missing_categories
    return missing

