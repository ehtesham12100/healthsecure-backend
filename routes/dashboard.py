from fastapi import APIRouter, Depends
from ..database import vulnerabilities_collection
from ..auth_utils import get_current_user, require_admin

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats")
def get_dashboard_stats(current_user: dict = Depends(get_current_user)):
    vulns = list(vulnerabilities_collection.find({}))

    total = len(vulns)
    critical = sum(1 for v in vulns if v.get("severity") == "Critical")
    high = sum(1 for v in vulns if v.get("severity") == "High")
    medium = sum(1 for v in vulns if v.get("severity") == "Medium")

    # Risk score formula
    risk_score = (critical * 5) + (high * 3) + (medium * 2)

    # Security score out of 100
    security_score = max(0, 100 - risk_score)

    return {
        "total_vulnerabilities": total,
        "critical_vulnerabilities": critical,
        "high_vulnerabilities": high,
        "medium_vulnerabilities": medium,
        "risk_score": risk_score,
        "security_score": security_score
    }
