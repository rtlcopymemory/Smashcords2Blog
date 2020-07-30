import psycopg2


def add_role(conn: psycopg2._psycopg.connection, server_id: str, role_id):
    curr = conn.cursor()
    curr.execute("INSERT INTO smashcords2blog.role (serverid, roleid) VALUES (%s, %s)", (server_id, role_id))
    conn.commit()
    curr.close()


def get_server_roles(conn, server_id) -> list:
    curr = conn.cursor()
    curr.execute("SELECT roleid FROM smashcords2blog.role WHERE serverid = %s", (server_id,))
    result = curr.fetchall()
    curr.close()
    return [role_tuple[0] for role_tuple in result]
