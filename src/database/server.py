import psycopg2


class Server:
    def __init__(self, conn):
        self.conn: psycopg2._psycopg.connection = conn

    @property
    def server_list(self):
        curr: psycopg2._psycopg.cursor = self.conn.cursor()
        curr.execute("SELECT * FROM smashcords2blog.server")
        result = curr.fetchall()
        curr.close()
        return result

    def get_server_from_id(self, server_id: int):
        curr: psycopg2._psycopg.cursor = self.conn.cursor()
        curr.execute("SELECT * FROM smashcords2blog.server WHERE serverid = %s", (server_id,))
        result = curr.fetchone()
        curr.close()
        return result
