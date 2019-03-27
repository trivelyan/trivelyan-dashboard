import heroku3 as h3

def test_connection (conn):
    try:
        conn.apps()
        return True
    except Exception as e:
        return False

conn = h3.from_key('key')

print conn
print test_connection(conn)
