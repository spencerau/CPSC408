from helper import helper

from db_operations import db_operations

dbOps = db_operations("playlist.db")
data = helper.data_cleaner("songs.csv")

#start message
def startScreen():
    print("Welcome to your Playlist!")

#check if songs table is empty
def isEmpty():
    query = '''
    SELECT COUNT(*)
    FROM songs
    '''
    result = dbOps.single_record(query)
    return result == 0

def preProcess():
    if isEmpty():
        attributeCount = len(data[0])
        placeholders = ("?," * attributeCount)[:-1]
        query = "INSERT INTO songs VALUES(" + placeholders + ")"
        dbOps.bulkInsert(query, data)

def options():
    print('''Select from the following menu options:
    1. Find songs by artist
    2. Find songs by genre
    3. Find songs by feature
    4. Exit
    ''')
    return helper.get_choice([1, 2, 3, 4])

def searchByArtist():
    query = '''
    SELECT DISTINCT Artist
    FROM songs;
    '''
    print("Artists in playlist: ")
    artists = dbOps.singleAttribute(query)

    # show all artists and make a dictonary to their number
    choices = {}
    for i in range(len(artists)):
        print(i, artists[i])
        choices[i] = artists[i]
    index = helper.get_choice(choices.keys())

    # print results of search
    query = '''
    SELECT DISTINCT name
    FROM songs
    WHERE Artist =:artist
    ORDER BY RANDOM()
    '''
    dictionary = {"artist":choices[index]}
    results = dbOps.namePlaceholderQuery(query, dictionary)
    helper.pretty_print(results)

def searchByGenre():
    f

def searchByFeat():
    test = 'f'


startScreen()
#db_ops.create_songs_table()
#print(isEmpty())
preProcess()
print()

while True:
    userChoice = options()
    if userChoice == 1:
        searchByArtist()
    if userChoice == 2:
        searchByGenre()
    if userChoice == 3:
        searchByFeat()
    if userChoice == 4:
        print("Goodbye")
        break



dbOps.destructor()