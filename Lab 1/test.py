import mysql.connector


conn = mysql.connector.connect(host="localhost",
                               user="root",
                               password="cpsc408",
                               auth_plugin='mysql_native_password',
                               database="RideShare")

#create cursor object
cur_obj = conn.cursor()


#select data
cur_obj.execute('''
SELECT * FROM tablename
''')
result = cur_obj.fetchall()
for row in result:
    print(row)

'''
#create database schema
cur_obj.execute("CREATE SCHEMA RideShare;")
#confirm execution worked by printing result
cur_obj.execute("SHOW DATABASES;")
for row in cur_obj:
    print(row)
#Print out connection to verify and close
print(conn)
'''
conn.close()
