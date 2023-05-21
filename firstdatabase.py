from pymongo import MongoClient
from webscraping import *

# Connect to MongoDB
client = MongoClient("mongodb+srv://moomoo:munch@moomoodb.kx1wt2m.mongodb.net/")
db = client["DCMacros"]
collection = db["Aggie"]

# Insert each struct into the collection
collection.insert_many(getAllMealsAndMacros())

# Close the connection
client.close()