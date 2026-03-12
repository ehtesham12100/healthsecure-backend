from pymongo import MongoClient
from passlib.hash import bcrypt
import os

# Connect to MongoDB
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://ahmed_db1:Ul00m%239XqP%2172%40Db@cluster0.3i5uuip.mongodb.net/healthcare?retryWrites=true&w=majority")
client = MongoClient(MONGO_URL)
db = client["healthcare"]

# Clear existing users
db["users"].delete_many({})
db["assets"].delete_many({})
db["vulnerabilities"].delete_many({})
db["phi_risks"].delete_many({})
db["compliance_controls"].delete_many({})
db["anomalies"].delete_many({})

# Create users with properly hashed passwords
users = [
    {
        "username": "admin",
        "email": "admin@healthsecure.com",
        "password": bcrypt.hash("admin123"),
        "role": "admin"
    },
    {
        "username": "user",
        "email": "user@healthsecure.com",
        "password": bcrypt.hash("user123"),
        "role": "user"
    }
]

db["users"].insert_many(users)
print("Users created successfully!")

# Verify passwords work
admin_user = db["users"].find_one({"username": "admin"})
print(f"Admin hash: {admin_user['password']}")
print(f"Verify admin123: {bcrypt.verify('admin123', admin_user['password'])}")

# Add sample data
assets = [
    {"name": "Patient Records DB", "type": "database", "status": "active", "risk_level": "high"},
    {"name": "Web Application", "type": "webapp", "status": "active", "risk_level": "medium"},
    {"name": "MRI Scanner", "type": "medical_device", "status": "active", "risk_level": "low"},
    {"name": "Email Server", "type": "server", "status": "active", "risk_level": "medium"},
    {"name": "Backup Storage", "type": "storage", "status": "active", "risk_level": "high"},
    {"name": "Lab Equipment", "type": "medical_device", "status": "active", "risk_level": "low"},
    {"name": "HR Portal", "type": "webapp", "status": "active", "risk_level": "medium"},
    {"name": "VPN Server", "type": "server", "status": "active", "risk_level": "high"},
]
db["assets"].insert_many(assets)

vulnerabilities = [
    {"title": "SQL Injection", "severity": "critical", "status": "open", "cvss": 9.8},
    {"title": "Outdated SSL/TLS", "severity": "high", "status": "open", "cvss": 7.5},
    {"title": "Weak Password Policy", "severity": "medium", "status": "open", "cvss": 5.3},
    {"title": "Missing Security Headers", "severity": "low", "status": "open", "cvss": 3.1},
    {"title": "Unpatched System", "severity": "critical", "status": "open", "cvss": 9.1},
    {"title": "Insecure API Endpoints", "severity": "high", "status": "open", "cvss": 8.2},
    {"title": "Cross-Site Scripting", "severity": "medium", "status": "open", "cvss": 6.1},
    {"title": "Improper Access Control", "severity": "high", "status": "open", "cvss": 7.8},
]
db["vulnerabilities"].insert_many(vulnerabilities)

phi_risks = [
    {"description": "Unencrypted PHI in transit", "category": "encryption", "severity": "high", "status": "open"},
    {"description": "Unauthorized access to patient records", "category": "access_control", "severity": "critical", "status": "open"},
    {"description": "Improper PHI disposal", "category": "data_retention", "severity": "medium", "status": "open"},
    {"description": "Lack of audit logging", "category": "monitoring", "severity": "high", "status": "open"},
    {"description": "Unsecured mobile devices", "category": "device_security", "severity": "medium", "status": "open"},
]
db["phi_risks"].insert_many(phi_risks)

compliance = [
    {"control": "Access Control", "requirement": "HIPAA 164.312(a)", "status": "compliant", "last_audit": "2024-01-15"},
    {"control": "Audit Controls", "requirement": "HIPAA 164.312(b)", "status": "partial", "last_audit": "2024-01-20"},
    {"control": "Transmission Security", "requirement": "HIPAA 164.312(e)", "status": "compliant", "last_audit": "2024-01-10"},
    {"control": "Person or Entity Authentication", "requirement": "HIPAA 164.312(d)", "status": "compliant", "last_audit": "2024-01-18"},
    {"control": "Integrity Controls", "requirement": "HIPAA 164.312(c)", "status": "non_compliant", "last_audit": "2024-01-22"},
    {"control": "Backup and Disaster Recovery", "requirement": "HIPAA 164.308(a)", "status": "compliant", "last_audit": "2024-01-12"},
    {"control": "Risk Analysis", "requirement": "HIPAA 164.308(a)", "status": "partial", "last_audit": "2024-01-25"},
    {"control": "Workforce Security", "requirement": "HIPAA 164.308(a)", "status": "compliant", "last_audit": "2024-01-14"},
]
db["compliance_controls"].insert_many(compliance)

anomalies = [
    {"type": "unusual_access", "description": "Multiple failed login attempts", "severity": "high", "timestamp": "2024-01-26T10:30:00"},
    {"type": "data_exfiltration", "description": "Large data transfer to external IP", "severity": "critical", "timestamp": "2024-01-26T14:22:00"},
    {"type": "privilege_escalation", "description": "Admin access from unknown device", "severity": "high", "timestamp": "2024-01-26T09:15:00"},
    {"type": "unusual_network", "description": "Connection to suspicious domain", "severity": "medium", "timestamp": "2024-01-26T16:45:00"},
    {"type": "system_change", "description": "Firewall rules modified", "severity": "high", "timestamp": "2024-01-26T11:00:00"},
]
db["anomalies"].insert_many(anomalies)

print("\n✅ Database seeded successfully!")
print(f"   - Users: {len(users)}")
print(f"   - Assets: {len(assets)}")
print(f"   - Vulnerabilities: {len(vulnerabilities)}")
print(f"   - PHI Risks: {len(phi_risks)}")
print(f"   - Compliance: {len(compliance)}")
print(f"   - Anomalies: {len(anomalies)}")
