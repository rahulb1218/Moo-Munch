from pymongo import MongoClient

# Establish a connection to MongoDB
client = MongoClient("mongodb+srv://moomoo:munch@moomoodb.kx1wt2m.mongodb.net/")

# Select the database to empty
db = client["DCMacros"]

# Drop the entire database
client.drop_database(db.name)

# Close the MongoDB connection
client.close()
