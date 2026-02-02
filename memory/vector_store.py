import faiss
import numpy as np
import faiss
import numpy as np
import sqlite3
from memory.embedder import embed

DIM = 384
INDEX_PATH = "memory/faiss.index"
DB_PATH = "memory/memory.db"

class VectorStore:
    def __init__(self):
        self.index = faiss.IndexFlatL2(DIM)
        self._load_db()

    def _load_db(self):
        self.conn = sqlite3.connect(DB_PATH)
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY,
                content TEXT
            )
        """)
        self.conn.commit()

    def add(self, text: str):
        vec = np.array([embed(text)]).astype("float32")
        self.index.add(vec)

        cur = self.conn.cursor()
        cur.execute("INSERT INTO memory (content) VALUES (?)", (text,))
        self.conn.commit()

    def search(self, query: str, k=3):
        qvec = np.array([embed(query)]).astype("float32")
        distances, indices = self.index.search(qvec, k)

        cur = self.conn.cursor()
        results = []

        for idx in indices[0]:
            if idx == -1:
                continue
            cur.execute(
                "SELECT content FROM memory WHERE id = ?",
                (idx + 1,)
            )
            row = cur.fetchone()
            if row:
                results.append(row[0])

        return results
