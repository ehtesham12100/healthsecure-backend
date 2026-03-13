from fastapi import APIRouter, Depends, HTTPException
from backend.database import phi_risks_collection
from backend.auth_utils import get_current_user, require_admin
from bson import ObjectId

router = APIRouter(prefix="/phi-risks", tags=["PHI Risks"])

@router.get("/")
def get_phi_risks(current_user: dict = Depends(get_current_user)):
    risks = list(phi_risks_collection.find({}))
    for risk in risks:
        risk["_id"] = str(risk["_id"])
    return risks

@router.post("/", dependencies=[Depends(require_admin)])
def add_phi_risk(risk: dict, current_user: dict = Depends(require_admin)):
    phi_risks_collection.insert_one(risk)
    return {"message": "PHI risk added successfully"}

@router.delete("/{risk_id}", dependencies=[Depends(require_admin)])
def delete_phi_risk(risk_id: str, current_user: dict = Depends(require_admin)):
    result = phi_risks_collection.delete_one({"_id": ObjectId(risk_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="PHI risk not found")
    return {"message": "PHI risk deleted successfully"}
