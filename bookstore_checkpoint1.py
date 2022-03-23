#Computer Science Team Project 2 CS492
#Bookstore Application - "By the Books"
#Nathan Carballo, Tyler Pollock, Eric Cunningham, Roemen Schlotfeldt, Marcus Colquitt, Trevor Sharp
#March 13th, 2022
import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

root = tk.Tk()       #Create root window to prompt employee or customer login
root.title('By The Books')

window_width = 900
window_height = 506
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
message = ttk.Label(root, text="Hello, welcome to By The Books!").pack()
root.iconbitmap('bythebooks.ico')
img = ImageTk.PhotoImage(Image.open("bookstoregradient.png"))
panel = tk.Label(root, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")


def user_login(type, user, password):
    if type == 'cust':
        if user == "customerexample@gmail.com" and password == "1234567890":
            show_store_customer(user, password)
        else:
            messagebox.showerror("Invalid", "Invalid Email or Phone Number")
    elif type == 'emp':
        if user == 'admin' and password == 'admin':
            show_store_employee()
        else:
            messagebox.showerror("Invalid", "Invalid Username And Or Password")


def customer_click():
    login_window = tk.Tk()
    login_window.title('By The Books Customer Login')
    login_window.iconbitmap('bythebooks.ico')
    window_width = 600
    window_height = 200
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    login_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    def customer_login():
        user, password, type = usernameEntry.get(), passwordEntry.get(), 'cust'
        login_window.destroy()
        user_login(type, user, password)

    usernameLabel = ttk.Label(login_window, text="Email Address")
    usernameLabel.grid(row=0, column=0)
    usernameEntry = ttk.Entry(login_window)
    usernameEntry.grid(row=0, column=1)
    passwordLabel = ttk.Label(login_window, text="Phone Number ")
    passwordLabel.grid(row=1, column=0)
    passwordEntry = ttk.Entry(login_window, show='')
    passwordEntry.grid(row=1, column=1)
    loginButton = ttk.Button(login_window, text="Login", command=customer_login).grid(row=1, column=2)

def employee_click():
    login_window = tk.Tk()
    login_window.title('By The Books Employee Login')
    login_window.iconbitmap('bythebooks.ico')
    window_width = 600
    window_height = 200
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    login_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    def emp_login():
        user, password, type = usernameEntry.get(), passwordEntry.get(), 'emp'
        login_window.destroy()
        user_login(type, user, password)

    usernameLabel = ttk.Label(login_window, text="User Name")
    usernameLabel.grid(row=0, column=0)
    usernameEntry = ttk.Entry(login_window)
    usernameEntry.grid(row=0, column=1)
    passwordLabel = ttk.Label(login_window, text="Password")
    passwordLabel.grid(row=1, column=0)
    passwordEntry = ttk.Entry(login_window, show='*')
    passwordEntry.grid(row=1, column=1)
    loginButton = ttk.Button(login_window, text="Login", command=emp_login).grid(row=1, column=2)

user_button = ttk.Button(root, text='Customer login', command=customer_click).place(x = 400, y = 100)

employee_button = ttk.Button(root, text='Employee login', command=employee_click).place(x = 400, y = 150)

def show_store_customer(user, password):      #Function to create window with customer functions and establish connection to db's
    cust = user
    phone = password
    class DB:
        def __init__(self):
            self.conn = sqlite3.connect("bookstore.db")
            self.cur = self.conn.cursor()
            self.cur.execute(
                "CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY, title TEXT, author TEXT, isbn TEXT, quantity INTEGER)")
            self.conn.commit()
        def __del__(self):
            self.conn.close()
        def view(self):
            self.cur.execute("SELECT * FROM book")
            rows = self.cur.fetchall()
            return rows
        def search(self, title, author, isbn):
            self.cur.execute("SELECT * FROM book WHERE title=? OR author=? OR isbn=?", (title, author, isbn))
            rows = self.cur.fetchall()
            return rows
        def purchase(self, title, author, quantity):
            self.cur.execute("UPDATE book SET quantity=quantity-? WHERE title=? AND author=?", (quantity, title, author,))
            self.conn.commit()
    db = DB()
    class SDB:
        def __init__(self):
            self.conn = sqlite3.connect("sales.db")
            self.cur = self.conn.cursor()
            self.cur.execute(
                "CREATE TABLE IF NOT EXISTS sales (orderID INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author TEXT, isbn TEXT, cust TEXT, phone TEXT)")
            self.conn.commit()
        def __del__(self):
            self.conn.close()
        def purchase(self, title, author, isbn, cust, phone):
            self.cur.execute("INSERT INTO sales VALUES (NULL,?,?,?,?,?)", (title, author, isbn, cust, phone,))
            self.conn.commit()

    sdb = SDB()

    def get_selected_row(event):
        global selected_tuple
        index = list1.curselection()[0]
        selected_tuple = list1.get(index)
        e1.delete(0, END)
        e1.insert(END, selected_tuple[1])
        e2.delete(0, END)
        e2.insert(END, selected_tuple[2])
        e3.delete(0, END)
        e3.insert(END, selected_tuple[3])
        e4.delete(0, END)
        e4.insert(END, selected_tuple[4])

    def view_command():
        list1.delete(0, END)
        for row in db.view():
            list1.insert(END, row)

    def search_command():
        list1.delete(0, END)
        for row in db.search(e1.get(), e2.get()):
            list1.insert(END, row)

    def purchase_command():
        db.purchase(e1.get(), e2.get(), e4.get())
        sdb.purchase(e1.get(), e2.get(), e3.get(), cust, phone)
        messagebox.showinfo(title="Purchase", message="Purchase Successful!")

    window = Tk()
    window.title("Customer View")
    window.iconbitmap('bythebooks.ico')

    def on_closing():
        dd = db
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            window.destroy()
            del dd

    window.protocol("WM_DELETE_WINDOW", on_closing)
    l1 = Label(window, text="Title")
    l1.grid(row=0, column=0)

    l2 = Label(window, text="Author")
    l2.grid(row=0, column=2)

    l3 = Label(window, text="ISBN")
    l3.grid(row=1, column=0)

    l4 = Label(window, text="Quantity")
    l4.grid(row=1, column=2)

    title_text = StringVar()
    e1 = Entry(window, textvariable=title_text)
    e1.grid(row=0, column=1)

    author_text = StringVar()
    e2 = Entry(window, textvariable=author_text)
    e2.grid(row=0, column=3)

    isbn_text = StringVar()
    e3 = Entry(window, textvariable=isbn_text)
    e3.grid(row=1, column=1)

    quantity_text = StringVar()
    e4 = Entry(window, textvariable=quantity_text)
    e4.grid(row=1, column=3)

    list1 = Listbox(window, height=25, width=65)
    list1.grid(row=2, column=0, rowspan=6, columnspan=2)

    sb1 = Scrollbar(window)
    sb1.grid(row=2, column=2, rowspan=6)

    list1.configure(yscrollcommand=sb1.set)
    sb1.configure(command=list1.yview)
    list1.bind('<<ListboxSelect>>', get_selected_row)

    b1 = Button(window, text="View all", width=12, command=view_command)
    b1.grid(row=2, column=3)

    b2 = Button(window, text="Search entry", width=12, command=search_command)
    b2.grid(row=3, column=3)

    b3 = Button(window, text="Purchase book", width=12, command=purchase_command)
    b3.grid(row=4, column=3)

    b4 = Button(window, text="Close", width=12, command=window.destroy)
    b4.grid(row=5, column=3)

def show_store_employee():  # Function to create window for employee functions and establish db connections
    class DB:
        def __init__(self):
            self.conn = sqlite3.connect("bookstore.db")
            self.cur = self.conn.cursor()
            self.cur.execute(
                "CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY, title TEXT, author TEXT, isbn TEXT, quantity TEXT)")
            self.conn.commit()

        def __del__(self):
            self.conn.close()

        def view(self):
            self.cur.execute("SELECT * FROM book")
            rows = self.cur.fetchall()
            return rows

        def insert(self, title, author, isbn, quantity):
            self.cur.execute("INSERT INTO book VALUES (NULL,?,?,?,?)", (title, author, isbn, quantity,))
            self.conn.commit()
            self.view()

        def update(self, id, title, author, isbn, quantity):
            self.cur.execute("UPDATE book SET title=?, author=?, isbn=?, quantity=? WHERE id=?",
                                 (title, author, isbn, quantity, id,))
            self.conn.commit()
            self.view()

        def delete(self, id):
            self.cur.execute("DELETE FROM book WHERE id=?", (id,))
            self.conn.commit()
            self.view()

        def search(self, title="", author=""):
            self.cur.execute("SELECT * FROM book WHERE title=? OR author=?", (title, author,))
            rows = self.cur.fetchall()
            return rows

    db = DB()

    class SDB:
        def __init__(self):
            self.conn = sqlite3.connect("sales.db")
            self.cur = self.conn.cursor()
            self.cur.execute(
                    "CREATE TABLE IF NOT EXISTS sales (orderID INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author TEXT, isbn TEXT, cust TEXT, phone TEXT)")
            self.conn.commit()

        def __del__(self):
            self.conn.close()

        def view(self):
            self.cur.execute("SELECT * FROM sales")
            rows = self.cur.fetchall()
            return rows

        def search(self, customer="", itemPurchased=""):
            self.cur.execute("SELECT * FROM sales WHERE customer=? OR itemPurchased=?", (customer, itemPurchased,))
            rows = self.cur.fetchall()
            return rows

    sdb = SDB()

    class MDB:
        def __init__(self):
            self.conn = sqlite3.connect("manufacturer.db")
            self.cur = self.conn.cursor()
            self.cur.execute(
                "CREATE TABLE IF NOT EXISTS manufacturer (manufacturerID INTEGER PRIMARY KEY, title TEXT, author TEXT, isbn TEXT, quantity TEXT)")
            self.conn.commit()
        def __del__(self):
            self.conn.close()
        def view(self):
            self.cur.execute("SELECT * FROM manufacturer")
            rows = self.cur.fetchall()
            return rows
        def insert(self, title, author, isbn, quantity):
            self.cur.execute("INSERT INTO manufacturer VALUES (NULL,?,?,?,?)", (title, author, isbn, quantity,))
            self.conn.commit()
            self.view()
    mdb = MDB()
    def get_selected_row(event):
        global selected_tuple
        index = list1.curselection()[0]
        selected_tuple = list1.get(index)
        e1.delete(0, END)
        e1.insert(END, selected_tuple[1])
        e2.delete(0, END)
        e2.insert(END, selected_tuple[2])
        e3.delete(0, END)
        e3.insert(END, selected_tuple[3])
        e4.delete(0, END)
        e4.insert(END, selected_tuple[4])
    def view_command():
        list1.delete(0, END)
        for row in db.view():
            list1.insert(END, row)
    def search_command():
        list1.delete(0, END)
        for row in db.search(e1.get(), e2.get()):
            list1.insert(END, row)

    def update_command():
        db.update(selected_tuple[0], e1.get(), e2.get(), e3.get(), e4.get())
        list1.delete(0, END)
        for row in db.view():
            list1.insert(END, row)

    def add_command():
        if db.search(e1.get(), e2.get()) != []:
            for row in db.search(e1.get(), e2.get()):
                bookcount = 0
                exdata = row[1],row[2]
                addData = e1.get(), e2.get()
                if exdata == addData:
                    if 'Soon' in row[4]:
                        db.delete(row[0])
                    else:
                        bookcount = bookcount + int(row[4])
                        db.delete(row[0])
            if 'Soon' in row[4]:
                db.insert(e1.get(), e2.get(), e3.get(), e4.get())
            else:
                numBooks = bookcount + int(e4.get())
                db.insert(e1.get(), e2.get(), e3.get(),numBooks)
        else:
            db.insert(e1.get(), e2.get(), e3.get(), e4.get())
        list1.delete(0, END)
        for row in db.view():
            list1.insert(END, row)

    def delete_command():
        db.delete(selected_tuple[0])
        list1.delete(0, END)
        for row in db.view():
            list1.insert(END, row)

    def delete_manufacturer():
        mdb.delete(selected_tuple[0])

    def sales_command():
        list1.delete(0, END)
        for row in sdb.view():
            list1.insert(END, row)

    def order_command():

        def add_manufacturer():
            mdb.insert(e1.get(), e2.get(), e3.get(), e4.get())
            if db.search(e1.get(), e2.get()) != []:
                for row in db.search(e1.get(), e2.get()):
                    bookcount = 0
                    exdata = row[1], row[2]
                    addData = e1.get(), e2.get()
                    if exdata == addData:
                        if 'Soon' in row[4]:
                            db.delete(row[0])
                        else:
                            bookcount = bookcount + int(row[4])
                            db.delete(row[0])
                if 'Soon' in row[4]:
                    db.insert(e1.get(), e2.get(), e3.get(), e4.get())
                else:
                    numBooks = bookcount + int(e4.get())
                    db.insert(e1.get(), e2.get(), e3.get(), numBooks)
            else:
                db.insert(e1.get(), e2.get(), e3.get(), e4.get())
            list1.delete(0, END)
            for row in db.view():
                list1.insert(END, row)

        def view_manufacturer():
            list2.delete(0, END)
            for row in mdb.view():
                list2.insert(END, row)

        manufacturerWindow = Tk()
        manufacturerWindow.title("Manufacturer Order")
        manufacturerWindow.iconbitmap('bythebooks.ico')

        l1 = Label(manufacturerWindow, text="Title")
        l1.grid(row=0, column=0)
        l2 = Label(manufacturerWindow, text="Author")
        l2.grid(row=0, column=2)
        l3 = Label(manufacturerWindow, text="ISBN")
        l3.grid(row=1, column=0)
        l4 = Label(manufacturerWindow, text="Quantity")
        l4.grid(row=1, column=2)
        title_text = StringVar()
        e1 = Entry(manufacturerWindow, textvariable=title_text)
        e1.grid(row=0, column=1)
        author_text = StringVar()
        e2 = Entry(manufacturerWindow, textvariable=author_text)
        e2.grid(row=0, column=3)
        isbn_text = StringVar()
        e3 = Entry(manufacturerWindow, textvariable=isbn_text)
        e3.grid(row=1, column=1)
        quantity_text = StringVar()
        e4 = Entry(manufacturerWindow, textvariable=quantity_text)
        e4.grid(row=1, column=3)
        list2 = Listbox(manufacturerWindow, height=25, width=65)
        list2.grid(row=2, column=0, rowspan=6, columnspan=2)
        sb2 = Scrollbar(manufacturerWindow)
        sb2.grid(row=2, column=2, rowspan=6)
        list2.configure(yscrollcommand=sb2.set)
        sb2.configure(command=list2.yview)
        list2.bind('<<ListboxSelect>>', get_selected_row)
        b1 = Button(manufacturerWindow, text="View orders", width=12, command=view_manufacturer)
        b1.grid(row=2, column=3)
        b3 = Button(manufacturerWindow, text="Add order", width=12, command=add_manufacturer)
        b3.grid(row=4, column=3)
        b5 = Button(manufacturerWindow, text="Delete selected", width=12, command=delete_manufacturer)
        b5.grid(row=6, column=3)

    window = Tk()
    window.title("Employee View")
    window.iconbitmap('bythebooks.ico')

    def on_closing():
        dd = db
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            window.destroy()
            del dd

    window.protocol("WM_DELETE_WINDOW", on_closing)

    l1 = Label(window, text="Title")
    l1.grid(row=0, column=0)

    l2 = Label(window, text="Author")
    l2.grid(row=0, column=2)

    l3 = Label(window, text="ISBN")
    l3.grid(row=1, column=0)

    l4 = Label(window, text="Quantity")
    l4.grid(row=1, column=2)

    title_text = StringVar()
    e1 = Entry(window, textvariable=title_text)
    e1.grid(row=0, column=1)

    author_text = StringVar()
    e2 = Entry(window, textvariable=author_text)
    e2.grid(row=0, column=3)

    isbn_text = StringVar()
    e3 = Entry(window, textvariable=isbn_text)
    e3.grid(row=1, column=1)

    quantity_text = StringVar()
    e4 = Entry(window, textvariable=quantity_text)
    e4.grid(row=1, column=3)

    list1 = Listbox(window, height=25, width=65)
    list1.grid(row=2, column=0, rowspan=6, columnspan=2)

    sb1 = Scrollbar(window)
    sb1.grid(row=2, column=2, rowspan=6)
    list1.configure(yscrollcommand=sb1.set)
    sb1.configure(command=list1.yview)
    list1.bind('<<ListboxSelect>>', get_selected_row)

    b1 = Button(window, text="View all", width=12, command=view_command)
    b1.grid(row=2, column=3)

    b2 = Button(window, text="Search entry", width=12, command=search_command)
    b2.grid(row=3, column=3)

    b3 = Button(window, text="Add entry", width=12, command=add_command)
    b3.grid(row=4, column=3)

    b4 = Button(window, text="View Sales", width=12, command=sales_command)
    b4.grid(row=5, column=3)

    b5 = Button(window, text="Delete selected", width=12, command=delete_command)
    b5.grid(row=6, column=3)

    b6 = Button(window, text="Close", width=12, command=window.destroy)
    b6.grid(row=7, column=3)

    b7 = Button(window, text="Manufacturer", width=12, command=order_command)
    b7.grid(row=8, column=3)

    b8 = Button(window, text="Update Selection", width=12, command=update_command)
    b8.grid(row=9, column=3)


root.mainloop()

