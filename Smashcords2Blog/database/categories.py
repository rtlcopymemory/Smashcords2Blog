def add_category(conn, server_id: str, category_name):
    curr = conn.cursor()
    curr.execute("INSERT INTO smashcords2blog.category (serverid, catname) VALUES (%s, %s)", (server_id, category_name))
    conn.commit()
    curr.close()
