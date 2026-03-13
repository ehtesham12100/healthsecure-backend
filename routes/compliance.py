from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from backend.database import compliance_collection
from backend.auth_utils import get_current_user, require_admin
from bson import ObjectId

router = APIRouter(prefix="/compliance", tags=["Compliance"])

class ComplianceItem(BaseModel):
    requirement: str
    category: str
    status: str   # Compliant / Non-Compliant / Partial
    notes: str | None = None

@router.post("/", dependencies=[Depends(require_admin)])
def add_compliance(item: ComplianceItem, current_user: dict = Depends(require_admin)):
    compliance_collection.insert_one(item.dict())
    return {"message": "Compliance item added successfully"}

@router.get("/")
def get_compliance(current_user: dict = Depends(get_current_user)):
    items = list(compliance_collection.find({}, {"_id": 0}))
    return items

@router.delete("/{item_id}", dependencies=[Depends(require_admin)])
def delete_compliance(item_id: str, current_user: dict = Depends(require_admin)):
    result = compliance_collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Compliance item not found")
    return {"message": "Compliance item deleted successfully"}
