def add_category(conn, server_id: str, category_name: str):
    curr = conn.cursor()
    curr.execute("INSERT INTO smashcords2blog.category (serverid, catname) VALUES (%s, %s)", (server_id, category_name))
    conn.commit()
    curr.close()


def get_server_categories(conn, server_id) -> list:
    curr = conn.cursor()
    curr.execute("SELECT catname FROM smashcords2blog.category WHERE serverid = %s", (server_id,))
    result = curr.fetchall()
    curr.close()
    return [role_tuple[0] for role_tuple in result]


def remove_category(conn, server_id: int, category_name: str):
    curr = conn.cursor()
    curr.execute("DELETE FROM smashcords2blog.category WHERE serverid = %s AND catname = %s",
                 (server_id, category_name))
    conn.commit()
    curr.close()
