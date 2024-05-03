import fastapi
import asyncio
import uvicorn
import json

from gvault.server import model
from gvault.data import account, vault


app = fastapi.FastAPI()


@app.get("/get-account-by-username")
async def get_account_by_username(username: str) -> dict:
    account_model = model.try_get_account_model_by_username(username)
    
    if account_model is None:
        return {"success": False}
    
    return {
        "success": True,
        
        "username": account_model.username,
        "email": account_model.email,
        
        "authorization_key": account_model.authorization_key,
        
        "hash": json.dumps(account_model.hash),
        "public": json.dumps(account_model.public),
        "private": json.dumps(account_model.private)
    }


@app.get("/create-account")
async def create_account(
    username: str,
    email: str,
    
    authorization_key: str,
    
    hash: str,
    public: str,
    private: str,
) -> dict:
    result = await get_account_by_username(username)
    
    if result["success"]:
        return { 
            "success": False, 
            "message": "An account with that username already exists!"
        }
    
    new_account = model.AccountModel.create(
        username=username,
        email=email,
        
        authorization_key=authorization_key,
        
        hash=hash,
        
        public=public,
        private=private
    )
    
    new_account.save()
    
    return { "success": True }
