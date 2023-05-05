import requests
import json
import mysql.connector

conn = mysql.connector.connect(host="localhost",
                                user="root",
                                password="cpsc408",
                                auth_plugin='mysql_native_password',
                                database="MadeInChinaYelp")

#create cursor object
cursor = conn.cursor()

with open("yelp_api_key.json") as f:
    key = json.load(f)
    api_key = key["api_key"]

url = "https://api.yelp.com/v3/businesses/search"

headers = {
    "Authorization": f"Bearer {api_key}"
}

parameters = {
    "term": "restaurant",
    "location": "Los Angeles",
    "limit": 100,
    "sort_by": "review_count,rating"
}

response = requests.get(url, headers=headers, params=parameters)

if response.status_code == 200:
    data = response.json()
    businesses = data["businesses"]
    for business in businesses:
        name = business["name"]
        review_count = business["review_count"]
        price = business["price"]
        rating = business["rating"]
        address = business["location"]["address1"]
        culture = "N/A"
        website = business.get("url", "N/A")

        hours = business["hours"]
        for day in hours:
            if day["day"] == 0: # Monday is represented by the number 0
                monStart = day["start"]
                monEnd = day["end"]
            elif day["day"] == 1: # Tuesday
                tuesStart = day["start"]
                tuesEnd = day["end"]
            elif day["day"] == 2: # Wednesday
                wedStart = day["start"]
                wedEnd = day["end"]
            elif day["day"] == 3: # Thursday
                thursStart = day["start"]
                thursEnd = day["end"]
            elif day["day"] == 4: # Friday
                friStart = day["start"]
                friEnd = day["end"]
            elif day["day"] == 5: # Saturday
                satStart = day["start"]
                satEnd = day["end"]
            elif day["day"] == 6: # Sunday
                sunStart = day["start"]
                sunEnd = day["end"]
            else:
                print("An error occurred while getting times")
        # insert into OperatingTime table
        timesQuery = f"INSERT INTO OperatingTime (MondayStart, MondayEnd, TuesdayStart, TuesdayEnd, WednesdayStart, WednesdayEnd, ThursdayStart, ThursdayEnd, FridayStart, FridayEnd, SaturdayStart, SaturdayEnd, SundayStart, SundayEnd) VALUES ('{monStart}', '{monEnd}', '{tuesStart}', '{tuesEnd}', '{wedStart}', '{wedEnd}', '{thursStart}', '{thursEnd}', '{friStart}', '{friEnd}', '{satStart}', '{satEnd}', '{sunStart}', '{sunEnd}')"
        cursor.execute(timesQuery)
        # get the OperatingTimeID
        op_id = cursor.lastrowid
        # Prepare SQL query to insert restaurant data
        query = f"INSERT INTO Restaurant (Score, Price, Address, Culture, Op_ID, Website) VALUES ('{rating}', '{price}', '{address}', '{culture}', '{op_id}', '{website}')"
        cursor.execute(query)
        # Commit changes to the database
        cursor.commit()
else:
    print("An error occurred")
