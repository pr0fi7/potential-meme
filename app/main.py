from fastapi import FastAPI, Depends, HTTPException
import sqlite3
from app.db import get_conn, init_db
from app.schemas import ItemCreate, Item
from app import crud


app = FastAPI(title="Items API", version="1.0.0")


@app.on_event("startup")
def startup():
    init_db()


class DBConn:
    def __enter__(self):
        self.conn = get_conn()
        return self.conn

    def __exit__(self, exc_type, exc, tb):
        self.conn.close()


def get_db():
    with DBConn() as conn:
        yield conn


@app.post("/items", response_model=Item, status_code=201)
def create_item(payload: ItemCreate, conn: sqlite3.Connection = Depends(get_db)):
    return crud.create_item(conn, payload.name)


@app.get("/items", response_model=list[Item])
def list_items(conn: sqlite3.Connection = Depends(get_db)):
    return crud.list_items(conn)


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int, conn: sqlite3.Connection = Depends(get_db)):
    item = crud.get_item(conn, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get("/")
def root():
    return {"service": "Items API", "endpoints": ["POST /items", "GET /items", "GET /items/{id}"]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)