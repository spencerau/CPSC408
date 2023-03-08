#import library
import sqlite3
print('import')
#add path to chinook.db to connect to it
# /Users/spencerau/Documents/GitHub/CPSC408/In Class Python Example/chinook.db
connection = sqlite3.connect("chinook.db")
print('Connect to Chinook.db')
#cursor object that executes SQL commands
cur_obj = connection.cursor()
print('init cursor')


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

"""

def createQuery():
    #query to create the table tweet
    create_query = '''
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
    #execute query using cursor object
    cur_obj.execute(create_query)
    #commit modification made to database
    connection.commit()
    print('Tweet Table Successfully Created')
"""

def insertQueryHardCode():
    #query to insert a record (hard coded values)
    insert_query = '''
    INSERT INTO tweet VALUES(1, 'This is a tweet', '2022-01-01', "@Clibourne", 1,2,3);
    '''

    cur_obj.execute(insert_query)
    connection.commit()
    print ('Inserted hard coded values successfully')

def insertQueryQmark():
    #A tuple with 4 values to be inserted
    record = (2, 'This is not a tweet', '2021-01-02', '@Alice')

    #insert query with q-mark placeholders
    insert_query = '''
    INSERT INTO tweet(tweetID, Text, creationDate, User)
    VALUES (?,?,?,?)
    '''
    #in execute function, pass query and tuple to fill in
    cur_obj.execute(insert_query, record)
    connection.commit()

def insertManyQuery():
    #a list of tuples to be added
    records = [(3, 'hello world', '2021-01-03', '@Eve'),
        (4, 'hello universe', '2021-01-04', '@Bob'),
        (5, 'this is patrick', '2021-01-05', '@pStar')]

    #insert query with q-mark placeholders
    insert_query = '''
    INSERT INTO tweet(tweetID, Text, creationDate, User)
    VALUES (?,?,?,?)
    '''

    #use executemany function for multiple records
    cur_obj.executemany(insert_query, records)
    connection.commit()

def updateQuery():
    #New likes, comments, retweets, tweetID data
    new_data = [(4,5,10,2),
            (10, 15, 20, 3),
            (500000, 0, 1, 5)]

    #Update query with placeholders for respective VALUES
    update_query = '''
    UPDATE tweet
    SET Likes = ?, Comments = ?, Retweets = ?
    WHERE tweetID = ?
    '''

    cur_obj.executemany(update_query, new_data)
    connection.commit()

def selectQuery():
    #select query
    select_query = '''
    SELECT *
    FROM tweet;
    '''

    #store returned records into a result object
    #result is also a cursor object
    result = cur_obj.execute(select_query)

    #records are returned as tuples
    for row in result:
        print(row)

def selectQueryPlaceholder():
    #name to fetch results for
    search_name = '@pStar'

    #Select Query with name as a placeholder
    select_query = '''
    SELECT *
    FROM tweet
    WHERE User = '%s'
    '''

    #passing search_name using python string functions
    result = cur_obj.execute(select_query % search_name)

    #print results
    for row in result:
        print(row)

def selectQuerySQLInjection():
    #SQL Injection to drop astronaut table
    #text = 'Another tweet'
    text = 'Another tweet\');DROP TABLE astronaut;--'

    #use a string placeholder for text
    update_query = '''
    INSERT INTO tweet(tweetID, Text) VALUES (20, '%s');
    ''' % text

    #executescript is used when you have a large
    #sized query to execute with different operations
    cur_obj.executescript(update_query)
    connection.commit()

def selectQueryQmark():
    #name to fetch results for
    search_name = '@pStar'

    #using qmark placeholder
    select_query = '''
    SELECT *
    FROM tweet
    WHERE User = ?;
    '''

    #passing search_name as a tuple
    result = cur_obj.execute(select_query, (search_name,))
    #print results
    for row in result:
        print(row)

def selectQueryNamed():
    #name and ID to fetch results
    name = '@Clibourne'
    id = 1
    #using named placeholder
    select_query = '''
    SELECT *
    FROM tweet
    WHERE User = :username
    AND tweetID = :tID;
    '''
    #passing parameters as a dictionary
    result = cur_obj.execute(select_query,{'username':name, 'tID':id})
    #print results
    for row in result:
        print(row)

def selectQueryFetchall():
    #select Query
    select_query = '''
    SELECT *
    FROM tweet;
    '''

    #don't need intermediary cursor
    cur_obj.execute(select_query)

    #fetchall() will return all records FROM
    #previous execution as a list of tuples
    for row in cur_obj.fetchall():
        print(row)

def selectQueryFetchone():
    #select query
    select_query = '''
    SELECT *
    FROM tweet;
    '''

    #don't need intermediary cursor
    cur_obj.execute(select_query)

    #fetchone() will return records from execution
    #one by one whenever called
    print(cur_obj.fetchone())
    print(cur_obj.fetchone())

#createQuery()
#insertQueryHardCode()
#insertQueryQmark()
#insertManyQuery()
#selectQuery()
#selectQueryPlaceholder()
#selectQuerySQLInjection();
#selectQueryQmark()
#selectQueryNamed()
#selectQueryFetchall()
#selectQueryFetchone()

connection.close()