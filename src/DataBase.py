import sqlite3
import csv

connection = sqlite3.connect('san_pham.db')
cursor = connection.cursor()

def getAllData(File):
    cursor.execute("SELECT * FROM gia_mat_hang")
    rows = cursor.fetchall()

    # Lấy tên các cột
    column_names = [description[0] for description in cursor.description]

    with open(File, 'w', newline='', encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)

        # Ghi hàng đầu tiên là tên các cột
        csv_writer.writerow(column_names)

        # Ghi các hàng dữ liệu
        csv_writer.writerows(rows)

def UpdateByID(ID, name, price, description, link):
    cursor.execute("UPDATE gia_mat_hang SET name = ?, gia = ?, description = ?, link = ? WHERE ID = ?"
                   , (name, price, description, link, ID))
    connection.commit()

def DeleteByID(ID):
    cursor.execute("DELETE FROM gia_mat_hang WHERE id=?", (ID,))
    connection.commit()

def Add(name, price, description, link):
    cursor.execute("INSERT INTO gia_mat_hang (name, gia, description, link) VALUES (?, ?, ?, ?)"
                   , (name, price, description, link))
    connection.commit()
