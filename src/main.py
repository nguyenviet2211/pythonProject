from tkinter import *
from tkinter import filedialog, messagebox, ttk
import pandas
import DataBase

root = Tk()
root.title("Software")
root.geometry("1200x600")
root.iconbitmap("icon.ico")
ReceiveEmail = BooleanVar()
ReceiveEmail.set(False)

def add_data(tree):
    AddWindow = Toplevel(root)
    AddWindow.grab_set()
    AddWindow.title("Add Window")
    AddWindow.resizable(False, False)


    name = StringVar()
    price = StringVar()
    description = StringVar()
    link = StringVar()

    Entry(AddWindow, textvariable=name).grid(row=0, column=0)
    Entry(AddWindow, textvariable=price).grid(row=0, column=1)
    Entry(AddWindow, textvariable=description, width=40).grid(row=0, column=2)
    Entry(AddWindow, textvariable=link, width=40).grid(row=0, column=3)

    def AddData():
        tree.insert("", "end", text="", values=(name.get(), float(price.get()), description.get(), link.get()))
        DataBase.Add(name.get(), float(price.get()), description.get(), link.get())
        AddWindow.destroy()

    Button(AddWindow, text="Thêm", command=AddData).grid(row=1, column=0, columnspan=4, sticky="we")
    AddWindow.mainloop()

def update_data(tree):
    EditWindow = Toplevel(root)
    EditWindow.grab_set()
    EditWindow.title("Edit Window")
    EditWindow.resizable(False, False)

    # Lấy item đang được chọn
    selected_item = tree.selection()
    data = tree.item(selected_item, "values")
    ID = tree.item(selected_item, "text")

    name = StringVar(value=data[0])
    price = StringVar(value=data[1])
    description = StringVar(value=data[2])
    link = StringVar(value=data[3])

    Entry(EditWindow, textvariable=name).grid(row=0, column=0)
    Entry(EditWindow, textvariable=price).grid(row=0, column=1)
    Entry(EditWindow, textvariable=description, width=40).grid(row=0, column=2)
    Entry(EditWindow, textvariable=link, width=40).grid(row=0, column=3)

    def updateData():
        DataBase.UpdateByID(ID, name.get(), float(price.get()), description.get(), link.get())
        EditWindow.destroy()

    Button(EditWindow, text="Xác nhận", command=updateData).grid(row = 1, column = 0, columnspan=4, sticky="we")
    EditWindow.mainloop()

def delete_data(tree):
    selected_item = tree.selection()
    # Lấy giá trị ở cột đầu
    ID = tree.item(selected_item, "text")
    DataBase.DeleteByID(ID)
    if selected_item:
        # Xoa dữ liệu trong bảng
        tree.delete(selected_item)
    print("xóa")

def print_result():
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

    table = ttk.Treeview(select_data_window, columns=('name', 'price', 'description', 'link'), height=15)
    # Thêm cột chính
    table.heading("#0", text="ID")
    table.heading('name', text="Tên")
    table.heading('price', text="Giá")
    table.heading('description', text="Mô tả")
    table.heading('link', text="link")

    # Đặt cột phụ
    table.column("#0", width=60, anchor=W)
    table.column('name', width=100, anchor=W)
    table.column('price', width=150, anchor=CENTER)
    table.column('description', width=400, anchor=W)
    table.column('link', width=400, anchor=W)
    # lấy dữ liệu chèn vào bảng
    for index, row in data.iterrows():
        table.insert("", "end", text=row["ID"], values=(row["name"], row["gia"], row["description"], row["link"]))

    Menu_right_click = Menu(select_data_window, tearoff=0)
    Menu_right_click.add_command(label="Thêm", command=lambda: add_data(table))
    Menu_right_click.add_command(label="Sửa", command=lambda: update_data(table))
    Menu_right_click.add_command(label="Xóa", command=lambda: delete_data(table))

    table.grid(row = 0, column = 0, columnspan=2, rowspan=2)
    Button(select_data_window, text="Exit", command=select_data_window.destroy).grid(row = 2, column = 0, sticky="we", columnspan=2)

    def show_right_click_menu(event):
        Menu_right_click.post(event.x_root, event.y_root)

    # Gắn sự kiện chuột phải vào Treeview
    table.bind("<Button-3>", show_right_click_menu)
    select_data_window.mainloop()


# Menu
MenuBar = Menu(root)

FileMenu = Menu(MenuBar, tearoff=0) # không tách menu ra khỏi root
FileMenu.add_command(label="Open", command=open_file)
FileMenu.add_command(label="Save As...", command=save_as_file)
FileMenu.add_separator()
FileMenu.add_command(label="Exit", command=root.destroy)

SettingMenu = Menu(MenuBar, tearoff=0)
SettingMenu.add_command(label="Email", command=email_entry)

MenuBar.add_cascade(label="File", menu=FileMenu) # Thêm FileMenu vào menu bar
MenuBar.add_cascade(label="Setting", menu=SettingMenu)
root.config(menu=MenuBar)


root.mainloop()
