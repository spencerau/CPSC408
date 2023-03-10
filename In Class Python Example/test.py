#import library
import sqlite3

print()
#print('import')
#add path to chinook.db to connect to it
connection = sqlite3.connect("chinook.db")
#print('Connect to Chinook.db')

#cursor object that executes SQL commands
cur_obj = connection.cursor()
#print('init cursor')
#print()


def createTable():
    # query to create a table called tweet
    new_table = '''
    CREATE TABLE tweet(
        tweetID INTEGER NOT NULL PRIMARY KEY,
        Text VARCHAR(280),
        creationDate DATETIME,
        User VARCHAR(20),
        Likes INTEGER,
        Retweets INTEGER,
        Comments INTEGER
    );
    '''
    # execute query to create table
    cur_obj.execute(new_table)
    # commit modification to database
    connection.commit
    print("Table has been created")


def insertHCQuery():
    # query to insert a hardcoded value into tweet
    query = '''
    INSERT INTO tweet VALUES(1, 'This is a Tweet', '2023-01-01', '@Bob', 1,2,3)
    '''
    cur_obj.execute(query)
    connection.commit()
    print("Tweet has been inserted into table")


def insertQ_Query():
    record = (2, 'This is not a tweet', '2023-01-02', '@Alice')
    query = '''
    INSERT INTO tweet(tweetID, Text, creationDate, User)
    VALUES(?,?,?,?)
    '''
    cur_obj.execute(query, record)
    connection.commit()
    print("QTweet has been inserted into table")


def insertExecuteMany():
    records = [
        (3, 'Hello World', '2023-01-03', '@Eve'),
        (4, 'Hello Universe', '2023-01-04', '@Bob'),
        (5, 'This is Patrick', '2023-01-05', '@pStar')
    ]
    query = '''
    INSERT INTO tweet(tweetID, Text, creationDate, User)
    VALUES(?,?,?,?)
    '''
    # execute many objects
    cur_obj.executemany(query, records)
    connection.commit()
    print("Multiple tweets have been inserted")


def updateExecuteMany():
    newData = [
        # 4 likes, 5 comments, 10 comments, for id 2
        (4, 5, 10, 2),
        (10, 15, 20, 3),
        (500000, 0, 1, 5)
    ]
    query = '''
    UPDATE tweet
    SET Likes = ?, Comments = ?, Retweets = ?
    WHERE tweetID = ?
    '''
    cur_obj.executemany(query, newData)
    connection.commit()
    print("Tweets have been updated")


def selectTweets():
    query = '''
    SELECT *
    FROM tweet;
    '''
    # result is a cursor object
    result = cur_obj.execute(query)
    #connection.commit()

    for row in result:
        print(row)


def selectPlaceholder():
    # name to fetch result for
    name = '@pStar'

    query = '''
    SELECT *
    FROM tweet
    WHERE User = '%s'
    '''
    result = cur_obj.execute(query % name)
    for row in result:
        print(row)


def selectNamedPlaceholder():
    # name and id to fetch
    name = '@Bob'
    id = 1

    # using named placeholders, search tweet
    query = '''
    SELECT *
    FROM tweet
    WHERE User =:username
    AND tweetID =:tID
    '''

    # pass parameters as a dictionary
    # in {name1:var}, where it finds name1 in query, replace with var
    result = cur_obj.execute(query, {'username':name, 'tID':id})
    for row in result:
        print(row)
    

def selectFetchAll():
    query = '''
    SELECT *
    FROM tweet;
    '''

    cur_obj.execute(query)

    for row in cur_obj.fetchall():
        print(row)


def selectFetchOne():
    query = '''
    SELECT *
    FROM tweet;
    '''
    cur_obj.execute(query)
    print(cur_obj.fetchone())
    print("Something")
    print(cur_obj.fetchone())


def insertSQLInjection():
    #text to insert into table
    text = "Another tweet\);DROP TABLE Astronaut;--"
    #insert tweet
    query = '''
    INSERT INTO tweet(tweetID, Text)
    VALUES(20, '%s')
    ''' % text

    cur_obj.executescript(query)
    connection.commit()

insertSQLInjection()



print()