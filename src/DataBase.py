import sqlite3
import csv

connection = sqlite3.connect('san_pham.db')
cursor = connection.cursor()

def SendToCsvFile(File, rows):
    # Lấy tên các cột
    column_names = [description[0] for description in cursor.description]
    with open(File, 'w', newline='', encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(column_names)
        csv_writer.writerows(rows)

def getAllData(File):
    cursor.execute("SELECT * FROM san_pham")
    rows = cursor.fetchall()
    SendToCsvFile(File, rows)

def UpdateByID(ID, name, price, description, link, category):
    cursor.execute("UPDATE san_pham SET name = ?, gia = ?, description = ?, link = ?, category = ? WHERE ID = ?"
                   , (name, price, description, link, category, ID))
    connection.commit()

def DeleteByID(ID):
    cursor.execute("DELETE FROM san_pham WHERE id=?", (ID,))
    connection.commit()

def Add(name, price, description, link, category=None):
    cursor.execute("INSERT INTO san_pham (name, gia, description, link, category) VALUES (?, ?, ?, ?, ?)"
                   , (name, price, description, link, category))
    connection.commit()
    return cursor.lastrowid

def deleteAll():
    cursor.execute("DELETE FROM san_pham")
    connection.commit()

def getDataByCategory(category):
    cursor.execute("SELECT * FROM san_pham WHERE category = ?", (category,))
    rows = cursor.fetchall()
    SendToCsvFile("output.csv", rows)

def CategoryList():
    cursor.execute("SELECT DISTINCT category FROM san_pham")
    data = cursor.fetchall()
    data = [''.join(map(str, Tuple)) if Tuple is not None else '' for Tuple in data]
    return data

def GetPriceByID(ID):
    cursor.execute("SELECT gia, Time FROM gia_mat_hang WHERE ID = ?", (ID,))
    rows = cursor.fetchall()
    return rows

def GetPriceByTimeAndCategory(ID, category):
    pass

# cursor.execute("SELECT name, sql FROM sqlite_master WHERE type IN ('trigger', 'table');")
# rows = cursor.fetchall()
# for row in rows:
#     print(row)

# Khi san pham duoc them vao thi them 1 ban ghi vao gia moi ngay
# cursor.execute("""
# CREATE TRIGGER insert_gia_moi_ngay
# AFTER INSERT ON san_pham
# FOR EACH ROW
# BEGIN
#     INSERT INTO gia_moi_ngay (ID, gia, Time)
#     VALUES (NEW.ID, NEW.gia, date('now'));
# END;
# """)

# Khi Cap nhat du lieu trong san_pham, cap nhat hoac them moi ban ghi trong gia_moi_ngay
# cursor.execute("DROP TRIGGER update_gia_moi_ngay")
# cursor.execute("""
# CREATE TRIGGER update_gia_moi_ngay
# AFTER UPDATE ON san_pham
# FOR EACH ROW
# BEGIN
#     INSERT OR REPLACE INTO gia_moi_ngay (ID, Time, gia)
#     VALUES (NEW.ID, date('now'), NEW.gia);
# END;
# """)

# khi xoa ban ghi trong san_pham thi ban ghi tuong ung trong gia_moi_ngay cung bi xoa
# cursor.execute("""
# CREATE TRIGGER delete_gia_moi_ngay
# AFTER DELETE ON san_pham
# FOR EACH ROW
# BEGIN
#     DELETE FROM gia_moi_ngay WHERE ID = OLD.ID;
# END;""")



