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


