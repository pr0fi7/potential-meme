from datetime import datetime, timezone
import sqlite3
from app.models import Item


def create_item(conn: sqlite3.Connection, name: str) -> Item:
    created_at = datetime.now(timezone.utc).isoformat()
    cur = conn.execute(
    "INSERT INTO items (name, created_at) VALUES (?, ?)", (name, created_at)
    )
    conn.commit()
    item_id = cur.lastrowid
    row = conn.execute(
    "SELECT id, name, created_at FROM items WHERE id = ?", (item_id,)
    ).fetchone()
    return Item(
    id=row["id"], name=row["name"], created_at=datetime.fromisoformat(row["created_at"])
    )




def list_items(conn: sqlite3.Connection) -> list[Item]:
    rows = conn.execute("SELECT id, name, created_at FROM items ORDER BY id").fetchall()
    return [
    Item(id=r["id"], name=r["name"], created_at=datetime.fromisoformat(r["created_at"]))
    for r in rows
    ]




def get_item(conn: sqlite3.Connection, item_id: int) -> Item | None:
    row = conn.execute(
    "SELECT id, name, created_at FROM items WHERE id = ?", (item_id,)
    ).fetchone()
    if not row:
        return None
    return Item(id=row["id"], name=row["name"], created_at=datetime.fromisoformat(row["created_at"]))