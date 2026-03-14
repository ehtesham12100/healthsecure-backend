import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pymongo import MongoClient
from auth_utils import get_password_hash
import os

# Use environment variable or default to MongoDB Atlas
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://ahmed_db1:Ul00m%239XqP%2172%40Db@cluster0.3i5uuip.mongodb.net/healthcare?retryWrites=true&w=majority")
client = MongoClient(MONGO_URL)
db = client["healthcare"]

# Clear existing data
db.assets.drop()
db.vulnerabilities.drop()
db.phi_risks.drop()
db.compliance_controls.drop()
db.anomalies.drop()
db.users.drop()

# Seed Users with hashed password
# Default admin credentials: admin / admin123
# Default user credentials: user / user123
users = [
    {
        "username": "admin",
        "password": get_password_hash("admin123"),
        "email": "admin@healthsecure.com",
        "role": "admin"
    },
    {
        "username": "user",
        "password": get_password_hash("user123"),
        "email": "user@healthsecure.com",
        "role": "user"
    }
]
db.users.insert_many(users)

# Seed Assets
assets = [
    {"name": "Patient Records Server", "type": "Server", "criticality": "Critical", "status": "Online", "ip": "192.168.1.10", "owner": "IT Department"},
    {"name": "MRI Scanner Workstation", "type": "Medical Device", "criticality": "Critical", "status": "Online", "ip": "192.168.1.15", "owner": "Radiology"},
    {"name": "Electronic Health Records (EHR)", "type": "Application", "criticality": "Critical", "status": "Online", "ip": "192.168.1.20", "owner": "Clinical Team"},
    {"name": "Laboratory Information System", "type": "Application", "criticality": "High", "status": "Online", "ip": "192.168.1.25", "owner": "Lab Department"},
    {"name": "Pharmacy Management System", "type": "Application", "criticality": "High", "status": "Online", "ip": "192.168.1.30", "owner": "Pharmacy"},
    {"name": "Security Camera NVR", "type": "Security System", "criticality": "Medium", "status": "Online", "ip": "192.168.1.40", "owner": "Security"},
    {"name": "Backup Storage Server", "type": "Server", "criticality": "High", "status": "Online", "ip": "192.168.1.50", "owner": "IT Department"},
    {"name": "Legacy Patient Portal", "type": "Application", "criticality": "Low", "status": "Offline", "ip": "192.168.1.60", "owner": "IT Department"},
]

# Seed Vulnerabilities
vulnerabilities = [
    {"asset_name": "Patient Records Server", "title": "SQL Injection in Login Form", "severity": "Critical", "cvss_score": 9.8, "status": "Open"},
    {"asset_name": "EHR System", "title": "Missing Authentication for Critical Function", "severity": "Critical", "cvss_score": 9.1, "status": "Open"},
    {"asset_name": "MRI Scanner Workstation", "title": "Outdated Windows Version", "severity": "High", "cvss_score": 7.5, "status": "Open"},
    {"asset_name": "Laboratory Information System", "title": "Weak SSL/TLS Configuration", "severity": "High", "cvss_score": 6.8, "status": "Open"},
    {"asset_name": "Pharmacy Management System", "title": "Cross-Site Scripting (XSS)", "severity": "Medium", "cvss_score": 5.4, "status": "Open"},
    {"asset_name": "Security Camera NVR", "title": "Default Credentials Enabled", "severity": "High", "cvss_score": 8.2, "status": "Open"},
    {"asset_name": "Patient Records Server", "title": "Unpatched OpenSSL Vulnerability", "severity": "Critical", "cvss_score": 8.9, "status": "Fixed"},
    {"asset_name": "Backup Storage Server", "title": "Insufficient Access Controls", "severity": "Medium", "cvss_score": 5.3, "status": "Open"},
]

# Seed PHI Risks
phi_risks = [
    {"title": "Unauthorized Access to Patient Records", "category": "Access Control", "severity": "Critical", "description": "Multiple failed login attempts detected from external IP"},
    {"title": "Unencrypted PHI Email Sent", "category": "Data Transmission", "severity": "High", "description": "Patient data sent without encryption"},
    {"title": "PHI Printout Left Unattended", "category": "Physical Security", "severity": "Medium", "description": "Printed records found in common area"},
    {"title": "Unauthorized USB Device", "category": "Device Control", "severity": "High", "description": "Unknown USB device connected to EHR workstation"},
    {"title": "Missing Audit Logs", "category": "Audit Trails", "severity": "Medium", "description": "Audit logging disabled for 24 hours"},
]

# Seed Compliance
compliance = [
    {"requirement": "Access Controls (HIPAA 164.312(a)(1))", "category": "Access Control", "status": "compliant", "notes": "All access controls implemented"},
    {"requirement": "Encryption of PHI at Rest (HIPAA 164.312(a)(2)(iv))", "category": "Encryption", "status": "compliant", "notes": "AES-256 encryption enabled"},
    {"requirement": "Audit Logging (HIPAA 164.312(b))", "category": "Audit Controls", "status": "compliant", "notes": "All access logged"},
    {"requirement": "Transmission Security (HIPAA 164.312(e)(1))", "category": "Transmission", "status": "partial", "notes": "TLS 1.2 enforced, upgrade to 1.3 recommended"},
    {"requirement": "Password Policy (HIPAA 164.312(d))", "category": "Authentication", "status": "compliant", "notes": "Complex passwords required"},
    {"requirement": "Employee Training", "category": "Administrative", "status": "non-compliant", "notes": "15% of staff pending security training"},
    {"requirement": "Business Associate Agreements", "category": "Administrative", "status": "compliant", "notes": "All BAA agreements in place"},
    {"requirement": "Disaster Recovery Plan", "category": "Contingency", "status": "partial", "notes": "Plan exists but not tested in 6 months"},
]

# Seed Anomalies
anomalies = [
    {"title": "Unusual Data Access Pattern", "type": "Behavioral", "severity": "High", "description": "User accessed 500+ records in 5 minutes"},
    {"title": "Off-Hours Login Attempt", "type": "Authentication", "severity": "Medium", "description": "Login attempt at 3 AM from unusual location"},
    {"title": "Large Data Export", "type": "Data Exfiltration", "severity": "Critical", "description": "User exported 10MB of patient data"},
    {"title": "Multiple Failed Logins", "type": "Authentication", "severity": "Medium", "description": "10 failed login attempts in 1 minute"},
    {"title": "Privilege Escalation", "type": "Authorization", "severity": "High", "description": "User granted admin access unexpectedly"},
]

# Insert data
db.assets.insert_many(assets)
db.vulnerabilities.insert_many(vulnerabilities)
db.phi_risks.insert_many(phi_risks)
db.compliance_controls.insert_many(compliance)
db.anomalies.insert_many(anomalies)

print("✅ Database seeded successfully!")
print(f"   - Users: {len(users)} (admin/admin123, user/user123)")
print(f"   - Assets: {len(assets)}")
print(f"   - Vulnerabilities: {len(vulnerabilities)}")
print(f"   - PHI Risks: {len(phi_risks)}")
print(f"   - Compliance: {len(compliance)}")
print(f"   - Anomalies: {len(anomalies)}")
