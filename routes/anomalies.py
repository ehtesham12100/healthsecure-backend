from fastapi import APIRouter, Depends, HTTPException
from database import anomalies_collection
from auth_utils import get_current_user, require_admin
from bson import ObjectId

router = APIRouter(prefix="/anomalies", tags=["Anomalies"])

@router.get("/")
def get_anomalies(current_user: dict = Depends(get_current_user)):
    anomalies = list(anomalies_collection.find({}))
    for anomaly in anomalies:
        anomaly["_id"] = str(anomaly["_id"])
    return anomalies

@router.post("/", dependencies=[Depends(require_admin)])
def add_anomaly(anomaly: dict, current_user: dict = Depends(require_admin)):
    anomalies_collection.insert_one(anomaly)
    return {"message": "Anomaly added successfully"}

@router.delete("/{anomaly_id}", dependencies=[Depends(require_admin)])
def delete_anomaly(anomaly_id: str, current_user: dict = Depends(require_admin)):
    result = anomalies_collection.delete_one({"_id": ObjectId(anomaly_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Anomaly not found")
    return {"message": "Anomaly deleted successfully"}
