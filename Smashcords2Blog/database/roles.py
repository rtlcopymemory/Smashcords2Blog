def add_role(conn, server_id: str, role_id):
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


def remove_role(conn, server_id: int, role_id: int):
    curr = conn.cursor()
    curr.execute("DELETE FROM smashcords2blog.role WHERE serverid = %s AND roleid = %s", (server_id, role_id))
    conn.commit()
    curr.close()
