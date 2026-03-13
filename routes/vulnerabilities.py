from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.database import vulnerabilities_collection
from backend.auth_utils import get_current_user, require_admin
from bson import ObjectId

router = APIRouter(prefix="/vulnerabilities", tags=["Vulnerabilities"])

class Vulnerability(BaseModel):
    asset_name: str
    title: str
    severity: str   # Critical / High / Medium
    cvss_score: float
    status: str     # Open / Fixed

@router.post("/", dependencies=[Depends(require_admin)])
def add_vulnerability(vuln: dict, current_user: dict = Depends(require_admin)):
    result = vulnerabilities_collection.insert_one(vuln)
    return {
        "message": "Vulnerability added successfully",
        "id": str(result.inserted_id)
    }

@router.get("/")
def get_vulnerabilities(current_user: dict = Depends(get_current_user)):
    vulns = list(vulnerabilities_collection.find({}))
    # Convert ObjectId to string for each vulnerability
    for vuln in vulns:
        vuln["_id"] = str(vuln["_id"])
    return vulns


@router.put("/{vuln_id}", dependencies=[Depends(require_admin)])
def update_vulnerability_status(vuln_id: str, status: str, current_user: dict = Depends(require_admin)):
    result = vulnerabilities_collection.update_one(
        {"_id": ObjectId(vuln_id)},
        {"$set": {"status": status}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Vulnerability not found")

    return {"message": "Vulnerability status updated successfully"}

@router.delete("/{vuln_id}", dependencies=[Depends(require_admin)])
def delete_vulnerability(vuln_id: str, current_user: dict = Depends(require_admin)):
    result = vulnerabilities_collection.delete_one({"_id": ObjectId(vuln_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Vulnerability not found")

    return {"message": "Vulnerability deleted successfully"}
