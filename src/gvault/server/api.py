import fastapi
import uvicorn

from gvault.server import model


app = fastapi.FastAPI()

@app.get("/get-account-by-username")
async def get_account_by_username(username: str) -> dict:
    account_model = model.try_get_account_model_by_username(username)
    
    return {
        
    }