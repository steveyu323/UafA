import mysql.connector

def TryMySQL():

    cnx = mysql.connector.connect(user='root', password='tiger323',
                              host='localhost',
                              database='UafA')
    cursor = cnx.cursor()

    cmd = "INSERT INTO RawSequence VALUES(1,'aaa')"

    cursor.execute(cmd)

    cnx.commit()

    cursor.close()
    cnx.close()
    return
