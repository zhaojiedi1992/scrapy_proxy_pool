import sqlite3
import random
from abc import ABC
from loguru import logger
from schemas.proxy import Proxy
from settings import SQLITE_DB_PATH, PROXY_SCORE_MAX, PROXY_SCORE_MIN, PROXY_SCORE_INIT, SQLITE_STORAGE_LIMIT
from utils.proxy import extract_auth_proxy, is_valid_proxy

class SQLiteStorage(ABC):
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS proxies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                host TEXT NOT NULL,
                port INTEGER NOT NULL,
                score INTEGER NOT NULL DEFAULT 0
            )
        ''')
        self.conn.commit()

    def max(self, proxy: Proxy):
        self.cursor.execute('UPDATE proxies SET score = ? WHERE host = ? AND port = ?', (PROXY_SCORE_MAX, proxy.host, proxy.port))
        self.conn.commit()

    def count(self) -> int:
        self.cursor.execute('SELECT COUNT(*) FROM proxies')
        return self.cursor.fetchone()[0]

    def decrease(self, proxy: Proxy):
        self.cursor.execute('UPDATE proxies SET score = score - 1 WHERE host = ? AND port = ?', (proxy.host, proxy.port))
        self.conn.commit()
        self.cursor.execute('SELECT score FROM proxies WHERE host = ? AND port = ?', (proxy.host, proxy.port))
        score = self.cursor.fetchone()
        if score and score[0] <= PROXY_SCORE_MIN:
            self.remove(proxy)

    def remove(self, proxy: Proxy):
        self.cursor.execute('DELETE FROM proxies WHERE host = ? AND port = ?', (proxy.host, proxy.port))
        self.conn.commit()
        logger.info(f'Proxy {proxy} removed')

    def exists(self, proxy: Proxy) -> bool:
        self.cursor.execute('SELECT COUNT(*) FROM proxies WHERE host = ? AND port = ?', (proxy.host, proxy.port))
        return self.cursor.fetchone()[0] > 0

    def add(self, proxy: Proxy, score=PROXY_SCORE_INIT) -> int:
        if not is_valid_proxy(str(proxy)):
            logger.info(f'Invalid proxy: {proxy}')
            return 0
        self.cursor.execute('INSERT OR REPLACE INTO proxies (host, port, score) VALUES (?, ?, ?)', (proxy.host, proxy.port, score))
        self.conn.commit()
        return self.cursor.rowcount

    def random(self) -> Proxy:
        self.cursor.execute('SELECT * FROM proxies WHERE score >= ? ORDER BY RANDOM() LIMIT 1', (PROXY_SCORE_MIN,))
        proxy = self.cursor.fetchone()
        if proxy:
            return Proxy(host=proxy[1], port=proxy[2])  # Assuming proxy[1] is host and proxy[2] is port
        self.cursor.execute('SELECT * FROM proxies ORDER BY RANDOM() LIMIT 1')
        proxy = self.cursor.fetchone()
        if proxy:
            return Proxy(host=proxy[1], port=proxy[2])  # Assuming proxy[1] is host and proxy[2] is port
        raise Exception('No proxy available')

    def batch(self, cursor, count):
        query = f"SELECT * FROM proxies LIMIT {count} OFFSET {cursor}"
        self.cursor.execute(query)
        proxies = self.cursor.fetchall()
        cursor += count
        #return cursor, data
        return cursor, [Proxy(host=proxy[1], port=proxy[2]) for proxy in proxies]
        #return [ for proxy in proxies]  # Assuming proxy[1] is host and proxy[2] is port

    def is_full(self):
        return self.count() >= SQLITE_STORAGE_LIMIT

    # def __del__(self):
    #     self.conn.close()

    @classmethod
    def get_client_from_config(cls):
        # client = sqlite3.connect(database = )
        return cls(SQLITE_DB_PATH)

# Example usage (for testing purposes)
if __name__ == '__main__':
    storage = SQLiteStorage(SQLITE_DB_PATH)
    proxy = Proxy(host='127.0.0.1', port=80)
    storage.add(proxy=proxy, score=10)
    storage.max(proxy=proxy)
    result = storage.random()
    batch_proxies = storage.batch(2)
    print(batch_proxies)
    print(result)