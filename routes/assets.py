from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from database import assets_collection
from auth_utils import get_current_user, require_admin

router = APIRouter(prefix="/assets", tags=["Assets"])

class Asset(BaseModel):
    name: str
    type: str
    criticality: str
    status: str
    ip: str
    owner: str

@router.post("/", dependencies=[Depends(require_admin)])
def add_asset(asset: Asset, current_user: dict = Depends(require_admin)):
    asset_dict = asset.dict()
    assets_collection.insert_one(asset_dict)
    return {"message": "Asset added successfully"}

@router.get("/")
def get_assets(current_user: dict = Depends(get_current_user)):
    assets = list(assets_collection.find({}, {"_id": 0}))
    return assets

@router.delete("/{asset_id}", dependencies=[Depends(require_admin)])
def delete_asset(asset_id: str, current_user: dict = Depends(require_admin)):
    from bson import ObjectId
    result = assets_collection.delete_one({"_id": ObjectId(asset_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {"message": "Asset deleted successfully"}
