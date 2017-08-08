from dropboxphotos import *

root_directory_dropbox = '/photos et videos'
root_directory_local = 'f:\photos et videos'

# read the dropbox token that is used to access the user's account
file = open('token.txt', 'r')
token = file.read()
file.close()

print("connexion a Dropbox", flush = True)
dbx = connect_to_dropbox(token)
print("comparaison des arborescences", flush = True)
missing = compare_dropbox_and_local(dbx, root_directory_dropbox, root_directory_local)

for year in sorted(missing.keys()):
    number = 0
    for elem in missing[year]:
        print (year + ' numero ' + str(number) + ' : ' + elem)
        number += 1

year = input ('annee :')
index = int (input('numero de repertoire : '))
source_folder = root_directory_local + '\\'+ year + '\\' + missing[year][index]
dest_folder = root_directory_dropbox + '/'+ year + '/' + missing[year][index]
print(" copie de " + source_folder + " vers " + dest_folder, flush = True)
upload_new_folder(dbx, source_folder , dest_folder)

