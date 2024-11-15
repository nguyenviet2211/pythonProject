from tkinter import *
from tkinter import filedialog, messagebox, ttk
import pandas
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import DataBase

# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import ssl
# from plyer import notification


# Hàm gửi thông báo
# def send_windows_notification(title, message):
#     notification.notify(
#         title=title,  # Tiêu đề của thông báo
#         message=message,  # Nội dung thông báo
#         timeout=10  # Thời gian thông báo hiển thị (tính bằng giây)
#     )
#
#
# def send_mail_notification(title, text, receiver_email):
#     email = "pythonnoticesystem@gmail.com"
#     # Khởi tạo đối tượng msg
#     msg = MIMEMultipart()
#     msg['From'] = email
#     msg['To'] = receiver_email
#     msg['Subject'] = title
#
#     # Đính kèm nội dung vào email, sử dụng mã hóa UTF-8
#     msg.attach(MIMEText(text, 'plain', 'utf-8'))
#     try:
#
#         # Kết nối tới Gmail với SSL (cổng 465)
#         context = ssl.create_default_context()
#         server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
#
#         # Đăng nhập với email và mật khẩu ứng dụng
#         server.login(email, "zurt sebu kufn pnsj")
#
#         # Gửi email bằng cách sử dụng msg.as_string()
#         server.sendmail(email, receiver_email, msg.as_string())
#         print("Email đã được gửi thành công!")
#
#     except Exception as e:
#         print(f"Đã xảy ra lỗi: {e}")
#
#     finally:
#         server.quit()  # Đảm bảo đóng kết nối với server
#
#
# # lấy thông tin giá sản phẩm
# production = input("PRODUCTION: ")
# price_stone = input("PRICE STONE: ")
# new_price = input("NEW PRICE: ")
# if (price_stone >= new_price):
#     # lấy thông tin tin nhắn và thông báo
#     title = "THÔNG BÁO"
#     text = f"THÔNG BÁO:\nGiá sản phẩm {production} đã chạm mốc giá {price_stone}"
#
#     # lấy thông tin mail nhận
#     receiver_email = input("RECEIVER EMAIL: ")
#
#     # 1.Thông báo qua mail
#     send_mail_notification(title, text, receiver_email)
#
#     # 2. Thông báo qua windows
#     send_windows_notification(title, text)

root = Tk()
root.title("Shopee")
root.minsize(1200, 600)
root.geometry("1200x600")
root.iconbitmap("icon.ico")
ReceiveEmail = BooleanVar(value=False)
Category = DataBase.CategoryList()

def showTable(window, data, pos):
    window.grid_columnconfigure(pos[1], weight=1)
    table = ttk.Treeview(window, columns=('name', 'price', 'description', 'link', 'category'), height=15, selectmode="extended")

    table.heading("#0", text="ID")
    table.heading('name', text="Tên")
    table.heading('price', text="Giá")
    table.heading('description', text="Mô tả")
    table.heading('link', text="link")
    table.heading('category', text="Phân loại")

    table.column("#0", anchor=W, minwidth=50)
    table.column('name', anchor=W, minwidth=50)
    table.column('price', anchor=CENTER)
    table.column('description', anchor=W, minwidth=100)
    table.column('link', anchor=W, minwidth=100)
    table.column('category', anchor=W, minwidth=100)

    # lấy dữ liệu chèn vào bảng
    for index, row in data.iterrows():
        table.insert("", "end", text=row["ID"],
                     values=(row["name"], row["gia"], row["description"], row["link"], row["category"]))

    Menu_right_click = Menu(window, tearoff=0)
    Menu_right_click.add_command(label="Thêm", command=lambda: add_data_window(table))
    Menu_right_click.add_command(label="Sửa", command=lambda: update_data_window(table))
    Menu_right_click.add_command(label="Xóa", command=lambda: delete_data(table))
    Menu_right_click.add_command(label="Xóa Hết", command=lambda: delete_all_data())

    table.grid(row=pos[0], column=pos[1], sticky="news")

    def show_right_click_menu(event):
        Menu_right_click.post(event.x_root, event.y_root)

    # chuột phải
    table.bind("<Button-3>", show_right_click_menu)

    def resize_columns(event):
        total_width = event.width
        list_size = [1/10, 2/10, 1/10, 2/10, 2/10, 2/10]
        i = 1
        table.column("#0", width=int(total_width * list_size[0]))
        for col in table["columns"]:
            table.column(col, width=int(total_width * list_size[i]))
            i += 1

    # Kết nối sự kiện "Configure" với hàm resize_columns
    table.bind("<Configure>", resize_columns)

    table.bind("<<TreeviewSelect>>", lambda event: draw_graph(table))

    return table

def add_data_window(tree):
    AddWindow = Toplevel(root)
    AddWindow.grab_set()
    AddWindow.title("Add Window")
    AddWindow.resizable(False, False)

    name = StringVar()
    price = StringVar()
    description = StringVar()
    link = StringVar()
    category = StringVar(value=Category[0])

    Entry(AddWindow, textvariable=name).grid(row=0, column=0)
    Entry(AddWindow, textvariable=price).grid(row=0, column=1)
    Entry(AddWindow, textvariable=description, width=40).grid(row=0, column=2)
    Entry(AddWindow, textvariable=link, width=40).grid(row=0, column=3)
    ttk.Combobox(AddWindow, textvariable=category, values=DataBase.CategoryList()).grid(row=0, column=4)

    def AddData():
        try:
            ID = DataBase.Add(name.get(), float(price.get()), description.get(), link.get(), category.get())
            tree.insert("", "end", text= ID, values=(name.get(), float(price.get()), description.get(), link.get(), category.get()))
            AddWindow.destroy()
        except ValueError:
            messagebox.showerror(message="Vui lòng nhập dữ liệu hợp lệ", parent=AddWindow, title="Error")

    Button(AddWindow, text="Thêm", command=AddData).grid(row=1, column=0, columnspan=5, sticky="we")
    AddWindow.mainloop()

def update_data_window(tree):
    # Lấy item đang được chọn
    selected_item = tree.selection()
    data = tree.item(selected_item, "values")
    ID = tree.item(selected_item, "text")
    if data:
        EditWindow = Toplevel(root)
        EditWindow.grab_set()
        EditWindow.title("Edit Window")
        EditWindow.resizable(False, False)
        name = StringVar(value=data[0])
        price = StringVar(value=data[1])
        description = StringVar(value=data[2])
        link = StringVar(value=data[3])
        category = StringVar(value=data[4])

        Entry(EditWindow, textvariable=name).grid(row=0, column=0)
        Entry(EditWindow, textvariable=price).grid(row=0, column=1)
        Entry(EditWindow, textvariable=description, width=39).grid(row=0, column=2)
        Entry(EditWindow, textvariable=link, width=40).grid(row=0, column=3)
        ttk.Combobox(EditWindow, textvariable=category, values=DataBase.CategoryList()).grid(row=0, column=4)

        def updateData():
            try:
                DataBase.UpdateByID(ID, name.get(), float(price.get()), description.get(), link.get(), category.get())
                tree.item(selected_item, values=(name.get(), float(price.get()), description.get(), link.get(), category.get()))
                EditWindow.destroy()
            except ValueError:
                messagebox.showerror(message="Vui lòng nhập dữ liệu hợp lệ", parent=EditWindow, title="Error")

        Button(EditWindow, text="Xác nhận", command=updateData).grid(row = 1, column = 0, columnspan=5, sticky="we")
        EditWindow.mainloop()

def delete_data(tree):
    selected_items = tree.selection()
    # Lấy giá trị ở cột đầu
    for selected_item in selected_items:
        ID = tree.item(selected_item, "text")
        DataBase.DeleteByID(ID)
        if selected_item:
            # Xoa dữ liệu trong bảng
            tree.delete(selected_item)

def delete_all_data():
    DataBase.deleteAll()

def GetDataFromWeb():
    pass

def schedule():
    pass

def email_entry():
    Email_Box = Toplevel(root)
    Email_Box.title("Email")
    Email_Box.iconbitmap("icon.ico")
    Email_Box.grab_set() # Khóa thao tác với cửa sổ khác
    Label(Email_Box, text="Nhập Email của bạn:").grid(row=0, column=0, columnspan=2)
    Checkbutton(Email_Box, text="Nhận Email khi giá giảm", variable=ReceiveEmail, onvalue=True, offvalue=False).grid(row=2, column=0)
    def get_email():
        if email.get() == "Email":
            messagebox.showinfo(message="Thay đổi Email thành công!", parent=Email_Box)
            Email_Box.grab_release()
            Email_Box.destroy()
            return
        else:
            messagebox.showerror(message="Nhập sai định dạng Email. Vui lòng nhập lại", parent=Email_Box)
            email.delete(0, END)

    Button(Email_Box, text="Xác Nhận", command=get_email).grid(row=1, column=1)
    email = Entry(Email_Box, width=50)
    email.grid(row=1, column=0)

    Email_Box.mainloop()

def import_data():
    FilePath = filedialog.askopenfilename(
        title="Import Data",
        filetypes=(("CSV files", "*.csv"), ("All Files", "*.*"))
    )

    if FilePath:
        data = pandas.read_csv(FilePath)

        for index, row in data.iterrows():
            DataBase.Add(row["name"], row["gia"], row["description"], row["link"])
        messagebox.showinfo(message="Nhập dữ liệu thành công")

def open_file():
    DataBase.getAllData("output.csv")
    data = pandas.read_csv("output.csv")  # Đọc dữ liêu từ file csv
    load_data(data)

def save_as_file():
    # mở cửa sổ lưu File
    File_Path = filedialog.asksaveasfilename(
        title="Save File",
        defaultextension=".csv",
        filetypes = (
            ("CSV files", "*.csv"),
            ("txt File", ".txt"),
            ("All Files", "*.*"))
    )

    if File_Path:
        try:
            DataBase.getAllData(File_Path)
        except Exception as e:
            messagebox.showerror(title="Error", message=str(e))

def load_data(data):
    select_data_window = Toplevel(root)
    select_data_window.title("Load Data")
    select_data_window.iconbitmap("icon.ico")
    select_data_window.grab_set()
    select_data_window.resizable(False, False)

    showTable(select_data_window, data, (0, 0))

    Button(select_data_window, text="Exit", command=select_data_window.destroy).grid(row = 2, column = 0, sticky="we", columnspan=2)
    select_data_window.mainloop()

def draw_graph(table):
    selected_items = table.selection()
    ID = table.item(selected_items, "text")

    data_list = DataBase.GetPriceByID(ID)

    x = []
    y = []

    for data in data_list:
        x.append(data[1])
        y.append(data[0])

    # Tạo figure và vẽ đồ thị đường
    fig, ax = plt.subplots()
    ax.plot(x, y, label='Đồ thị đường', color='blue')

    # Thêm tiêu đề và nhãn trục
    ax.set_title("Đồ thị đường trong Tkinter")
    ax.set_xlabel("Ngày")
    ax.set_ylabel("Giá")
    ax.legend()

    # Nhúng đồ thị vào Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)  # Khung giao diện Tkinter
    canvas.draw()
    canvas.get_tk_widget().grid(column=0, row=0)

def change_category(category, combobox):
    DataBase.getDataByCategory(category)
    table = showTable(root, pandas.read_csv("output.csv"), (0, 1))
    combobox.config(values=DataBase.CategoryList())
    draw_graph(table)

def main_window():
    # Menu
    MenuBar = Menu(root)
    FileMenu = Menu(MenuBar, tearoff=0) # không tách menu ra khỏi root
    FileMenu.add_command(label="Open", command=open_file)
    FileMenu.add_command(label="Export", command=save_as_file)
    FileMenu.add_command(label="Import", command=import_data)
    FileMenu.add_separator()
    FileMenu.add_command(label="Exit", command=root.destroy)
    SettingMenu = Menu(MenuBar, tearoff=0)
    SettingMenu.add_command(label="Email", command=email_entry)
    MenuBar.add_cascade(label="File", menu=FileMenu) # Thêm FileMenu vào menu bar
    MenuBar.add_cascade(label="Setting", menu=SettingMenu)
    root.config(menu=MenuBar)

    cate = StringVar()
    # Danh sach tha xuong
    combobox = ttk.Combobox(root, values=Category, textvariable=cate, state="readonly")
    combobox.set(Category[0])
    combobox.grid(column=0, row=1, sticky="we")
    # Sự kiện khi chọn 1 item trong combo box
    combobox.bind("<<ComboboxSelected>>", lambda event: change_category(cate.get(), combobox))
    change_category(Category[0], combobox)
    root.mainloop()

if __name__ == '__main__':
    main_window()

