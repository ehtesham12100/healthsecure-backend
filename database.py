from pymongo import MongoClient
# ============================================
# MONGODB ATLAS CONNECTION (CLOUD) - HARDCODED
# ============================================

MONGO_URL = "mongodb+srv://ahmed_db1:Ul00m%239XqP%2172%40Db@cluster0.3i5uuip.mongodb.net/healthcare?retryWrites=true&w=majority"

try:
    # Configure MongoDB client with timeout settings
    client = MongoClient(
        MONGO_URL,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=5000,
    )
    
    # Test the connection
    client.admin.command('ping')
    print("Successfully connected to MongoDB Atlas!")
    
    # Get database name from connection string
    db_name = MONGO_URL.split('/')[-1].split('?')[0] if '/' in MONGO_URL else "healthcare"
    db = client[db_name]
    
except Exception as e:
    print(f"Failed to connect to MongoDB Atlas: {e}")
    # Fallback to a basic client without connection test
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    db = client["healthcare"]

assets_collection = db["assets"]
vulnerabilities_collection = db["vulnerabilities"]
phi_risks_collection = db["phi_risks"]
compliance_collection = db["compliance_controls"]
anomalies_collection = db["anomalies"]
users_collection = db["users"]

# Export db for use in other modules
__all__ = [
    "db",
    "assets_collection",
    "vulnerabilities_collection",
    "phi_risks_collection",
    "compliance_collection",
    "anomalies_collection",
    "users_collection",
]
