from shortener import shortner
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_long_url

class Url(BaseModel):
	long_url : str
	short_url : str

class longUrl(BaseModel):
	long_url : str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/api/post-url")
async def posturl(long_url : longUrl): #url shorten
	short_url = shortner(long_url.long_url)
	return short_url

@app.get("/api/get-url/{short_id}")
async def geturl(short_id : str):
    row, error = get_long_url(short_id)
    if error or row is None:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    return {"long_url": row} # row is already the string from the fix above