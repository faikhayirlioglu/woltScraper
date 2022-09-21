import mysql.connector as mysql

db = mysql.connect(
    host='uzeyirxt.beget.tech',
    user='uzeyirxt_test',
    passwd='3FvQ*2ps',
    database='uzeyirxt_test'
)

cursor = db.cursor(buffered=True, dictionary=True)

def resetData():
    cursor.execute("DELETE FROM qr_menu")
    cursor.execute("ALTER TABLE qr_menu AUTO_INCREMENT = 1;")

    cursor.execute("DELETE FROM qr_catagory_main")
    cursor.execute("ALTER TABLE qr_catagory_main AUTO_INCREMENT = 1;")
    
    db.commit()

resetData()