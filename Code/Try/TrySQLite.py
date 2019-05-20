import sqlite3;

def try_sql():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    db_file = "../db/uafa.db"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cmd = ''' delete from raw_sequence where hap_id = 1'''
    cur.execute(cmd)
    conn.commit()
    return None
