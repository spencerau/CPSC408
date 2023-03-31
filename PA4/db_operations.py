import sqlite3

class db_operations():

    #constructor with connection path to db
    def __init__(self, conn_path):
        self.connection = sqlite3.connect(conn_path)
        self.cursor = self.connection.cursor()
        print("Connection Established")

    #destructor that closes path to db
    def destructor(self):
        self.connection.close()

    def create_songs_table(self):
        query = '''
        CREATE TABLE songs(
        songID VARCHAR(22) NOT NULL PRIMARY KEY,
        Name VARCHAR(20),
        Artist VARCHAR(20),
        Album VARCHAR(20),
        releaseDate DATETIME,
        Genre VARCHAR(20),
        Explicit BOOLEAN,
        Duration DOUBLE,
        Energy DOUBLE,
        Danceability DOUBLE,
        Acousticness DOUBLE,
        Liveness DOUBLE,
        Loudness DOUBLE
        );
        '''
        self.cursor.execute(query)
        print("Table Created")

    def single_record(self, query):
        self.cursor.execute(query)
        #gives you the first col at first tuple/row
        return self.cursor.fetchone()[0]
    
    def bulkInsert(self, query, records):
        self.cursor.executemany(query, records)
        self.connection.commit()
        print("Query Executed")

    def singleAttribute(self, query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        # convert list of lists to a list
        results = [i[0] for i in results]
        results.remove(None)
        return results
    
    def namePlaceholderQuery(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        results = self.cursor.fetchall()
        # convert list of lists to a list
        results = [i[0] for i in results]
        return results
    
    def printSongInfo(self, songID):
        querySongName = '''
        SELECT DISTINCT name
        FROM songs 
        WHERE songID =:songID
        '''
        self.cursor.execute(querySongName, {"songID":songID})
        name = self.cursor.fetchall()

        queryAlbumName = '''
        SELECT DISTINCT album
        FROM songs
        WHERE songID =:songID
        '''
        self.cursor.execute(queryAlbumName, {"songID":songID})
        albumName = self.cursor.fetchall()

        queryArtistName = '''
        SELECT DISTINCT artist
        FROM songs
        WHERE songID =:songID
        '''
        self.cursor.execute(queryArtistName, {"songID":songID})
        artistName = self.cursor.fetchall()

        queryReleaseDate = '''
        SELECT DISTINCT releaseDate
        FROM songs
        WHERE songID =:songID
        '''
        self.cursor.execute(queryReleaseDate, {"songID":songID})
        releaseDate = self.cursor.fetchall()

        queryExplicit = '''
        SELECT DISTINCT explicit
        FROM songs
        WHERE songID =:songID
        '''
        self.cursor.execute(queryExplicit, {"songID":songID})
        explicit = self.cursor.fetchall()
        print('''
        Choose which option to update:
        1. Song Name - %s
        2. Album Name - %s
        3. Artist Name - %s
        4. Release Date - %s
        5. Explicit - %s
        ''' % (name, albumName, artistName, releaseDate, explicit))
    
    # get songID from song name
    def getSongID(self, songName):
        query = '''
        SELECT songID
        FROM songs
        WHERE Name = ?
        '''
        self.cursor.execute(query, (songName,))
        result = self.cursor.fetchone()[0]
        if result is None:
            return None
        else:
            return result[0]
    
    # Add a new choice in the main application that asks the user if they want to update any information for a song, given a song name. 
    # For that song, print all attributes to the user and allow the user to make a choice about what information they want to modify. 
    # (Only song name, album name, artist name, release date, and Explicit attributes can be modified). 
    # Then ask the user for a new value and carry out the update. Incorrect values should be ignored, and the user should be prompted 
    # again. Note that while the user is going to make their choice based on the song name, your update query will be using songID in 
    # the WHERE clause.

    def updateSongName(self, songID, newName):
        query = '''
        UPDATE songs
        SET Name = ?
        WHERE songID = ?
        '''
        self.cursor.execute(query, (newName, songID))
        self.connection.commit()
        print("Query Executed")

    def updateAlbumName(self, songID, newAlbum):
        query = '''
        UPDATE songs
        SET Album = ?
        WHERE songID = ?
        '''
        self.cursor.execute(query, (newAlbum, songID))
        self.connection.commit()
        print("Query Executed")

    def updateArtistName(self, songID, newArtist):
        query = '''
        UPDATE songs
        SET Artist = ?
        WHERE songID = ?
        '''
        self.cursor.execute(query, (newArtist, songID))
        self.connection.commit()
        print("Query Executed")

    def updateReleaseDate(self, songID, newDate):
        query = '''
        UPDATE songs
        SET releaseDate = ?
        WHERE songID = ?
        '''
        self.cursor.execute(query, (newDate, songID))
        self.connection.commit()
        print("Query Executed")

    def updateExplicit(self, songID, newExplicit):
        query = '''
        UPDATE songs
        SET Explicit = ?
        WHERE songID = ?
        '''
        self.cursor.execute(query, (newExplicit, songID))
        self.connection.commit()
        print("Query Executed")

    # Add a new choice in the main application that asks the user if they want to remove a song from the playlist. Given a song name, 
    # you will then remove the song from the table.
    # Note that while the user is going to make their choice based on the song name, your delete query will be using songID in the 
    # WHERE clause.

    def deleteSong(self, songID):
        query = '''
        DELETE FROM songs
        WHERE songID = ?
        '''
        self.cursor.execute(query, (songID,))
        self.connection.commit()
        print("Query Executed")

    # Add a new choice in the main application. If the user selects this option, then remove all records from the table that have 
    # at least 1 NULL value.
    def deleteAllNull(self):
        query = '''
        DELETE FROM songs
        WHERE Name IS NULL OR Artist IS NULL OR Album IS NULL OR releaseDate IS NULL OR Genre IS NULL OR Explicit IS NULL OR Duration 
        IS NULL OR Energy IS NULL OR Danceability IS NULL OR Acousticness IS NULL OR Liveness IS NULL OR Loudness IS NULL
        '''
        self.cursor.execute(query)
        self.connection.commit()
        print("Query Executed")

