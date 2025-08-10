from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 
from typing import List ,Optional

app = FastAPI()

class Create_Quote(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None


class Quote(Create_Quote):
    id: int

class QuoteUpdate(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None

DB: List[Quote] = []  
NEXT_ID = 1

@app.post("/quotes/",response_model=Quote, status_code=201)
def create_quote(quote: Create_Quote):
    global NEXT_ID
    new_quote = Quote(id=NEXT_ID, **quote.dict())
    DB.append(new_quote)
    NEXT_ID += 1
    return new_quote

@app.get("/quotes/", response_model=List[Quote])
def list_quotes():
    """Return all quotes."""
    return DB

@app.get("/quotes/{quote_id}",response_model=Quote)
def get_quotes(quote_id: int):
    for quote in DB:
        if quote.id == quote_id:
            return quote
    raise HTTPException(status_code=404, detail="Quote not found")

@app.delete("/quotes/{quote_id}",status_code=204)
def del_quote(quote_id:int):
    for i, quote in enumerate(DB):
        if quote.id == quote_id:
            del DB[i]
            return
    raise HTTPException(status_code=404, detail="Quote not found")


@app.patch("/quotes/{quote_id}", response_model=Quote)
def update_quote(quote_id: int, q_update: QuoteUpdate):
    for q in DB:
        if q.id == quote_id:
            if q_update.name is not None:
                q.name = q_update.name
            if q_update.author is not None:
                q.author = q_update.author
            return q
    raise HTTPException(status_code=404, detail="Quote not found")
