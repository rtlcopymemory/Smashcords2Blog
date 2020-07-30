def get_server_from_id(conn, server_id: int):
    curr = conn.cursor()
    curr.execute("SELECT * FROM smashcords2blog.server WHERE serverid = %s", (server_id,))
    result = curr.fetchone()
    curr.close()
    return result


def add_server(conn, server_id: int, server_name: str, server_invite: str = None):
    curr = conn.cursor()
    if server_invite is not None:
        curr.execute("INSERT INTO smashcords2blog.server (serverid, name, invitelink) VALUES (%s, %s, %s)",
                     (server_id, server_name, server_invite))
    else:
        curr.execute("INSERT INTO smashcords2blog.server (serverid, name) VALUES (%s, %s)", (server_id, server_name))
    conn.commit()
    curr.close()
