import pymysql

def conectarbd():
    try:
        return pymysql.connect(
            host='mysql-3e74c755-julonerick1-1f47.k.aivencloud.com',
            user='avnadmin',
            password='AVNS_sQSLY3fyNxJnuZ8zU_O',
            database='hacka',
            port=24299,
            cursorclass=pymysql.cursors.DictCursor
        )
    
    except pymysql.Error as error:
        print(error)
        return False