import sqlite3

class MemoryStore:
    def __init__(self, path="memory.db"):
        self.conn = sqlite3.connect(path)

    def recall(self, categories=None, limit=5):
        query = "SELECT category, content, confidence FROM memory"
        params = []

        if categories:
            query += " WHERE category IN ({})".format(
                ",".join("?" * len(categories))
            )
            params.extend(categories)

        query += " ORDER BY last_used DESC LIMIT ?"
        params.append(limit)

        cur = self.conn.execute(query, params)
        return cur.fetchall()

    def store(self, category, content, confidence=0.8):
        self.conn.execute(
            """INSERT INTO memory
               VALUES (NULL, ?, ?, ?, datetime('now'), datetime('now'))""",
            (category, content, confidence)
        )
        self.conn.commit()
