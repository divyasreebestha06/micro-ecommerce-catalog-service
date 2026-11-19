import sqlite3
from typing import List, Optional, Dict, Any

class CatalogDatabase:
    def __init__(self, db_path: str = "catalog.db"):
        self.db_path = db_path
        self._init_db()

    def _execute(self, query: str, params: tuple = (), fetchone=False, fetchall=False, commit=False):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if commit:
                conn.commit()
            if fetchone:
                row = cursor.fetchone()
                return dict(row) if row else None
            if fetchall:
                return [dict(r) for r in cursor.fetchall()]
            return cursor.lastrowid
        finally:
            conn.close()

    def _init_db(self):
        query = '''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL,
                description TEXT
            )
        '''
        self._execute(query, commit=True)

    def add_product(self, name: str, category: str, price: float, stock: int, desc: Optional[str]) -> Dict[str, Any]:
        q = 'INSERT INTO products (name, category, price, stock, description) VALUES (?, ?, ?, ?, ?)'
        pid = self._execute(q, (name, category, price, stock, desc), commit=True)
        return self.get_product(pid)

    def get_product(self, pid: int) -> Optional[Dict[str, Any]]:
        return self._execute('SELECT * FROM products WHERE id = ?', (pid,), fetchone=True)

    def search_products(self, category: Optional[str] = None, q: Optional[str] = None) -> List[Dict[str, Any]]:
        query = 'SELECT * FROM products WHERE 1=1'
        params = []
        if category:
            query += ' AND category = ?'
            params.append(category)
        if q:
            query += ' AND name LIKE ?'
            params.append(f'%{q}%')
        return self._execute(query, tuple(params), fetchall=True)

    def update_stock(self, pid: int, delta: int) -> Optional[Dict[str, Any]]:
        prod = self.get_product(pid)
        if not prod or (prod["stock"] + delta < 0):
            return None
        self._execute('UPDATE products SET stock = stock + ? WHERE id = ?', (delta, pid), commit=True)
        return self.get_product(pid)
