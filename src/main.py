from tkinter import *
from tkinter import filedialog, messagebox, ttk
import pandas
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import DataBase
import GetPrice
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
from plyer import notification

root = Tk()
root.title("Shopee")
root.minsize(1200, 600)
root.geometry("1200x600")
root.iconbitmap("icon.ico")
Category = DataBase.CategoryList()
cate = StringVar()
combobox = ttk.Combobox(root, values=Category, textvariable=cate, state="readonly")

# Hàm gửi thông báo
def send_windows_notification(Title, TEXT):
    notification.notify(
        title=Title,  # Tiêu đề của thông báo
        message=TEXT,  # Nội dung thông báo
        timeout=10  # Thời gian thông báo hiển thị (tính bằng giây)
    )

def send_mail_notification(Title, TEXT):
    server = ""
    email = "pythonnoticesystem@gmail.com"
    Receiver_email = pandas.read_csv("Email.csv").loc[0, 'Email']
    # Khởi tạo đối tượng msg
    msg = MIMEMultipart("alternative")
    msg['From'] = email
    msg['To'] = Receiver_email
    msg['Subject'] = Title
    # Thêm nội dung vào mail

    html_part = MIMEText(TEXT, "html")
    msg.attach(html_part)
    try:
        # Kết nối tới Gmail với SSL (cổng 465)
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)

        # Đăng nhập với email và mật khẩu ứng dụng
        server.login(email, "zurt sebu kufn pnsj")

        # Gửi email bằng cách sử dụng msg.as_string()
        server.sendmail(email, Receiver_email, msg.as_string())

    except Exception as e:
        messagebox.showerror(title="Lỗi", message=f"Đã xảy ra lỗi: {e}")
    finally:
        server.quit()  # Đảm bảo đóng kết nối với server

def GetDataFromWeb():
    DataBase.GetIdAndLink()
    dataFrame = pandas.read_csv("output.csv")

    for index, row in dataFrame.iterrows():
        GetPrice.GetPrice(row['link'], row['ID'])
    check_price()
    change_category()

def check_price():
    text = ""
    title = "THÔNG BÁO"

    DataBase.getAllData("output.csv")
    dataFrame1 = pandas.read_csv("output.csv")
    dataFrame2 = pandas.read_csv("Email.csv")

    for index, row in dataFrame1.iterrows():
        if pandas.isnull(row['category']):
            category = 'None'
        else:
            category = row['category']

        if dataFrame2.loc[0, category] == 't' and int(row['gia']) < int(dataFrame2.loc[1, category]):
            text += f"Giá sản phẩm <a href='{row['link']}' target='_blank'>{row['name']}</a> đã chạm mốc giá {dataFrame2.loc[1, category]} {category}.<br><br>"
    if text != "":
        # 1.Thông báo qua mail
        send_mail_notification(title, text)

        # 2. Thông báo qua windows
        send_windows_notification(title, "Có sản phẩm đã giảm giá")

def showTable(window, dataFrame, pos):
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
    for index, row in dataFrame.iterrows():
        table.insert("", "end", text=row["ID"],
                     values=(row["name"], row["gia"], row["description"], row["link"], row["category"]))

    Menu_right_click = Menu(window, tearoff=0)
    Menu_right_click.add_command(label="Thêm", command=lambda: add_data_window(table))
    Menu_right_click.add_command(label="Sửa", command=lambda: update_data_window(table))
    Menu_right_click.add_command(label="Xóa", command=lambda: delete_data(table))
    Menu_right_click.add_command(label="Xóa Hết", command=lambda: delete_all_data(dataFrame.loc[0, 'category']))

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

    def Item():
        selected_items = table.selection()
        if selected_items:
            ID = table.item(selected_items[0], "text")
            draw_graph(DataBase.GetPriceByID(ID))

    table.bind("<<TreeviewSelect>>", lambda event: Item())

def add_data_window(tree = None):
    AddWindow = Toplevel(root)
    AddWindow.grab_set()
    AddWindow.title("Add Window")
    AddWindow.resizable(False, False)

    name = StringVar(value="Tên")
    price = StringVar(value="0")
    description = StringVar(value="Mô Tả")
    link = StringVar(value="link")
    category = StringVar(value=cate.get())

    Entry(AddWindow, textvariable=name).grid(row=0, column=0)
    Entry(AddWindow, textvariable=price).grid(row=0, column=1)
    Entry(AddWindow, textvariable=description, width=40).grid(row=0, column=2)
    Entry(AddWindow, textvariable=link, width=40).grid(row=0, column=3)
    ttk.Combobox(AddWindow, textvariable=category, values=DataBase.CategoryList()).grid(row=0, column=4)

    def AddData():
        try:
            ID = DataBase.Add(name.get(), int(price.get()), description.get(), link.get(), category.get())
            if tree:
                tree.insert("", "end", text= ID, values=(name.get(), int(price.get()), description.get(), link.get(), category.get()))
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

def delete_all_data(category):
    DataBase.deleteAll(category)
    change_category()

def email_entry():
    global Category
    Email_Box = Toplevel(root)
    Email_Box.title("Email")
    Email_Box.iconbitmap("icon.ico")
    Email_Box.grab_set() # Khóa thao tác với cửa sổ khác
    Label(Email_Box, text="Nhập Email của bạn:").grid(row=0, column=0, columnspan=3)
    dataFrame = pandas.read_csv("Email.csv")
    Email = StringVar()
    Email.set(dataFrame.loc[0, 'Email'])
    Category = DataBase.CategoryList()

    for category in Category:
        if category not in dataFrame.columns:
            dataFrame[category] = ['f', 0]

    for column in dataFrame.columns:
        if column =='Email': continue
        if column not in Category:
            dataFrame.drop(column, axis=1, inplace=True)

    Label(Email_Box, text="Nhận Email khi giá đạt ngưỡng: ").grid(row=2,column=0, sticky="w")
    Label(Email_Box, text="Giá mong muốn").grid(row=2, column=1, sticky="e")

    checkbox_vars = [BooleanVar(value=False)]
    for i, val in enumerate(dataFrame.loc[0]):
        if i == 0: continue
        var = BooleanVar(value= val == 't')
        checkbox_vars.append(var)
        Checkbutton(Email_Box, text=dataFrame.columns[i], variable=var).grid(row=i + 2, column=0, sticky="w")

    Price = [0]
    for i, val in enumerate(dataFrame.loc[1]):
        if i == 0: continue
        varPrice = IntVar(value=val)
        Price.append(varPrice)
        Entry(Email_Box, textvariable=varPrice).grid(row=i + 2, column=1, sticky="w")

    def get_email():
        if Email.get() != "":
            messagebox.showinfo(message="Thay đổi Email thành công!", parent=Email_Box)
            dataFrame.loc[0, "Email"] = Email.get()
            # update checkbox
            for index, var_check_box in enumerate(checkbox_vars):
                if index == 0: continue
                dataFrame.loc[0, dataFrame.columns[index]] = 't' if var_check_box.get() else 'f'

            for index, VarPrice in enumerate(Price):
                if index == 0: continue
                dataFrame.loc[1, dataFrame.columns[index]] = VarPrice.get()

            #update csv file
            dataFrame.to_csv("Email.csv", index=False)
            Email_Box.destroy()
            return
        else:
            messagebox.showerror(message="Nhập sai định dạng Email. Vui lòng nhập lại", parent=Email_Box)
            email.delete(0, END)

    Button(Email_Box, text="Xác Nhận", command=get_email).grid(row=1, column=1, columnspan=3)
    email = Entry(Email_Box, textvariable=Email, width=50)
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

def draw_graph(data_list):
    x = []
    y = []

    for data in data_list:
        x.append(data[1])
        y.append(data[0])

    # print(plt.style.available)

    fig, ax = plt.subplots()
    ax.plot(x, y, color='red')
    plt.style.use('seaborn-v0_8-bright')
    fig.autofmt_xdate()

    # ax.set_title("")
    ax.set_xlabel("Ngày")
    ax.set_ylabel("Giá")
    # ax.legend(loc='best', fontsize=12, title="Legend Title", labels=['Label1', 'Label2'])


    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(column=0, row=0)
    plt.close(fig)

def change_category():
    # lưu danh sách các sản phẩm trong cùng 1 category
    DataBase.getDataByCategory(cate.get())
    showTable(root, pandas.read_csv("output.csv"), (0, 1))
    # Cập Nhật lại category list
    combobox.config(values=DataBase.CategoryList())
    draw_graph(DataBase.GetPriceByCategory(cate.get()))

def main_window():
    # Menu
    MenuBar = Menu(root)
    FileMenu = Menu(MenuBar, tearoff=0) # không tách menu ra khỏi root
    FileMenu.add_command(label="Thêm", command=add_data_window)
    FileMenu.add_command(label="Export", command=save_as_file)
    FileMenu.add_command(label="Import", command=import_data)
    FileMenu.add_separator()
    FileMenu.add_command(label="Exit", command=root.destroy)
    SettingMenu = Menu(MenuBar, tearoff=0)
    SettingMenu.add_command(label="Email", command=email_entry)
    MenuBar.add_cascade(label="File", menu=FileMenu) # Thêm FileMenu vào menu bar
    MenuBar.add_cascade(label="Setting", menu=SettingMenu)
    root.config(menu=MenuBar)

    # Danh sach tha xuong
    if Category:
        combobox.set(Category[0])
    else:
        combobox.set("Thêm danh mục")
    combobox.grid(column=0, row=1, sticky="we")
    # Sự kiện khi chọn 1 item trong combo box
    combobox.bind("<<ComboboxSelected>>", lambda event: change_category())
    change_category()
    Button(root, text="Cập nhật", command=GetDataFromWeb).grid(column=1, row=1, sticky="we")
    root.mainloop()

if __name__ == '__main__':
    main_window()
