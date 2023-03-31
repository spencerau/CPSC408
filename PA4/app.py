from helper import helper

from db_operations import db_operations

import sqlite3


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
    
    # prompt to load in new songs from Assignment04_songs_update.csv
    print("Do you want to load in new songs? Y/N")
    choice = input()
    if choice == 'Y'.lower():
        try: 
            data = helper.data_cleaner("Assignment04_songs_update.csv")
            attributeCount = len(data[0])
            placeholders = ("?," * attributeCount)[:-1]
            query = "INSERT INTO songs VALUES(" + placeholders + ")"
            dbOps.bulkInsert(query, data)
            print("New songs loaded")
        except sqlite3.IntegrityError:
            print("Error: The record already exists in the database.")
        
def options():
    print('''Select from the following menu options:
    1. Find songs by artist
    2. Find songs by genre
    3. Find songs by feature
    4. Update a Song by Song Name
    5. Delete a Song by Song Name
    6. Delete all Songs with Null values
    7. Exit
    ''')
    return helper.get_choice([1, 2, 3, 4, 5, 6, 7])

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

    # prompt user for a limit
    print("How many songs do you want for " + choices[index] + "?")
    print("Enter 1, 5, or enter 0 for all songs")
    num = helper.get_choice([1, 5, 0])

    # print results of search
    query = '''
    SELECT DISTINCT name
    FROM songs
    WHERE Artist =:artist
    ORDER BY RANDOM()
    '''
    dictionary = {"artist":choices[index]}
    if num != 0:
        query += "LIMIT:lim"
        dictionary["lim"] = num
    results = dbOps.namePlaceholderQuery(query, dictionary)
    helper.pretty_print(results)

def searchByGenre():
    # print all genres from songs
    query = '''
    SELECT DISTINCT Genre
    FROM songs;
    '''
    print("Genres in playlist: ")
    genres = dbOps.singleAttribute(query)

    # show all genres and make a dictonary to their number
    choices = {}
    for i in range(len(genres)):
        print(i, genres[i])
        choices[i] = genres[i]
    index = helper.get_choice(choices.keys())

    # prompt user for a limit
    print("How many songs do you want for " + choices[index] + "?")
    print("Enter 1, 5, or enter 0 for all songs")
    num = helper.get_choice([1, 5, 0])

    # print results of search
    query = '''
    SELECT DISTINCT name
    FROM songs
    WHERE Genre =:genre
    ORDER BY RANDOM()
    '''
    dictionary = {"genre":choices[index]}
    if num != 0:
        query += "LIMIT:lim"
        dictionary["lim"] = num
    results = dbOps.namePlaceholderQuery(query, dictionary)
    helper.pretty_print(results)

def searchByFeat():
    # list of all features to search by
    features = ['Danceability', 'Liveness', 'Loudness']

    # show features to user and create dictionary
    choices = {}
    for i in range(len(features)):
        print(i, features[i])
        choices[i] = features[i]
    index = helper.get_choice(choices.keys())

    # prompt user for a limit
    print("How many songs do you want for " + choices[index] + "?")
    print("Enter 1, 5, or enter 0 for all songs")
    num = helper.get_choice([1, 5, 0])

    # ascending or descending order
    print("Do you want the results sorted ascending or descending order")
    order = input("ASC or DESC: ")

    # run query and print results
    query = '''
    SELECT DISTINCT name
    FROM songs;
    ORDER BY 
    ''' + choices[index] + " " + order
    dictionary = {}
    if num != 0:
        query += " LIMIT:lim"
        dictionary["lim"] = num
    results = dbOps.namePlaceholderQuery(query, dictionary)
    helper.pretty_print(results)

# Add a new choice in the main application that asks the user if they want to update any information for a song, given a song name. 
    # For that song, print all attributes to the user and allow the user to make a choice about what information they want to modify. 
    # (Only song name, album name, artist name, release date, and Explicit attributes can be modified). 
    # Then ask the user for a new value and carry out the update. Incorrect values should be ignored, and the user should be prompted 
    # again. Note that while the user is going to make their choice based on the song name, your update query will be using songID in 
    # the WHERE clause.

def promptUpdate():
    
    print("Enter the name of the song you want to update")
    print()
    songName = input()
    songID = -1
    try:
        songID = dbOps.getSongID(songName)
        
    except TypeError:
        print()
        print("Error: The song does not exist in the database.")
        print()
        return
    print()

    dbOps.printSongInfo(songID)

    choice = helper.get_choice([1, 2, 3, 4, 5])
    if choice == 1:
        print("Enter the new song name")
        songName = input()
        dbOps.updateSongName(songID, songName)
    elif choice == 2:
        print("Enter the new album name")
        albumName = input()
        dbOps.updateAlbumName(songID, albumName)
    elif choice == 3:
        print("Enter the new artist name")
        artistName = input()
        dbOps.updateArtistName(songID, artistName)
    elif choice == 4:
        print("Enter the new release date")
        releaseDate = input()
        dbOps.updateReleaseDate(songID, releaseDate)
    elif choice == 5:
        print("Enter the new explicit value")
        explicit = input()
        dbOps.updateExplicit(songID, explicit)
    else:
        print("Invalid choice")


def deleteSong():
    print("Enter the name of the song you want to remove")
    songName = input()
    try:
        songID = dbOps.getSongID(songName)
        dbOps.deleteSong(songID)
        print("Song removed")
    except TypeError:
        print("Error: The song does not exist in the database.")
    print()

def deleteAllNull():
    dbOps.deleteAllNull()
    print("All null values removed")
    print()

 # Add a new choice in the main application that asks the user if they want to remove a song from the playlist. Given a song name, 
    # you will then remove the song from the table.
    # Note that while the user is going to make their choice based on the song name, your delete query will be using songID in the 
    # WHERE clause.


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
        promptUpdate()
    if userChoice == 5:
        deleteSong()
    if userChoice == 6:
        deleteAllNull()
    if userChoice == 7:
        print("Goodbye")
        break
    


dbOps.destructor()