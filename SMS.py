from tkinter import *
import time
from tkinter import ttk, messagebox, filedialog
import ttkthemes
import pymysql
import pandas

# ---------------- Functionality Part ---------------- #

def iexit():
    result = messagebox.askyesno('Confirm', 'Do you want to exit?')
    if result:
        root.destroy()
    else:
        pass


def export_data():
    url = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV files", "*.csv")])
    indexing = studentTable.get_children()  # fixed typo: get_childern -> get_children
    newlist = []
    for index in indexing:
        content = studentTable.item(index)
        datalist = content['values']
        newlist.append(datalist)

    table = pandas.DataFrame(newlist,
                             columns=['Id', 'Name', 'Phone', 'Email', 'Address', 'Gender', 'DOB', 'Added Date',
                                      'Added Time'])
    table.to_csv(url, index=False)
    messagebox.showinfo("Success", "Data is saved Successfully")


def toplevel_data(title, button_text, command):
    global idEntry, phoneEntry, nameEntry, emailEntry, addressEntry, genderEntry, dobEntry, screen
    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(False, False)

    idLabel = Label(screen, text="ID", font=('times new roman', 18, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=10, sticky=W)
    idEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, padx=15, pady=10)

    NameLabel = Label(screen, text="Name", font=('times new roman', 18, 'bold'))
    NameLabel.grid(row=1, column=0, padx=30, pady=10, sticky=W)
    nameEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, padx=15, pady=10)

    phoneLabel = Label(screen, text="Phone", font=('times new roman', 18, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=10, sticky=W)
    phoneEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, padx=15, pady=10)

    emailLabel = Label(screen, text="Email", font=('times new roman', 18, 'bold'))
    emailLabel.grid(row=3, column=0, padx=30, pady=10, sticky=W)
    emailEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, padx=15, pady=10)

    addressLabel = Label(screen, text="Address", font=('times new roman', 18, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=10, sticky=W)
    addressEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, padx=15, pady=10)

    genderLabel = Label(screen, text="Gender", font=('times new roman', 18, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=10, sticky=W)
    genderEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, padx=15, pady=10)

    dobLabel = Label(screen, text="D.O.B", font=('times new roman', 18, 'bold'))
    dobLabel.grid(row=6, column=0, padx=30, pady=10, sticky=W)
    dobEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, padx=15, pady=10)

    student_button = ttk.Button(screen, text=button_text, command=command)
    student_button.grid(row=7, columnspan=2, pady=15)

    if title == 'Update Student':
        indexing = studentTable.focus()
        content = studentTable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        phoneEntry.insert(0, listdata[2])
        emailEntry.insert(0, listdata[3])
        addressEntry.insert(0, listdata[4])
        genderEntry.insert(0, listdata[5])
        dobEntry.insert(0, listdata[6])


def update_data():
    query = 'update student set name=%s, mobile=%s, email=%s, address=%s, gender=%s, dob=%s, date_field=%s, added_time=%s where id=%s'
    mycursor.execute(query, (
        nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(),
        dobEntry.get(), date, currenttime, idEntry.get()))

    con.commit()
    messagebox.showinfo("Success", f'{idEntry.get()} is modified successfully', parent=screen)
    screen.destroy()
    show_student()


def show_student():
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def delete_student():
    indexing = studentTable.focus()
    if not indexing:
        messagebox.showerror("Error", "Please select a student to delete.")
        return
    content = studentTable.item(indexing)
    content_id = content['values'][0]
    query = 'DELETE FROM student WHERE id=%s'
    mycursor.execute(query, (content_id,))
    con.commit()
    messagebox.showinfo('Deleted', f'ID {content_id} deleted successfully.')
    show_student()


def search_data():
    query = '''SELECT * FROM student WHERE 
               id=%s OR name=%s OR mobile=%s OR email=%s OR 
               address=%s OR gender=%s OR dob=%s'''
    mycursor.execute(query, (
        idEntry.get(), nameEntry.get(), phoneEntry.get(), emailEntry.get(),
        addressEntry.get(), genderEntry.get(), dobEntry.get()
    ))
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def add_data():
    if idEntry.get() == '' or nameEntry.get() == '' or phoneEntry.get() == '' or emailEntry.get() == '' or addressEntry.get() == '' or genderEntry.get() == '' or dobEntry.get() == '':
        messagebox.showerror('Error', 'All fields are required', parent=screen)
    else:
        try:
            query = '''INSERT INTO student VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            mycursor.execute(query, (
                idEntry.get(), nameEntry.get(), phoneEntry.get(), emailEntry.get(),
                addressEntry.get(), genderEntry.get(), dobEntry.get(), date, currenttime))
            con.commit()
            result = messagebox.askyesno('Confirm', 'Data added successfully. Do you want to clear the form?',
                                         parent=screen)
            if result:
                idEntry.delete(0, END)
                nameEntry.delete(0, END)
                phoneEntry.delete(0, END)
                emailEntry.delete(0, END)
                addressEntry.delete(0, END)
                genderEntry.delete(0, END)
                dobEntry.delete(0, END)
        except pymysql.err.IntegrityError:
            messagebox.showerror('Error', 'ID already exists', parent=screen)
            return

        show_student()


# ---------------- GUI Part ---------------- #

root = ttkthemes.ThemedTk()
root.set_theme('radiance')

root.title("Student Management System")
root.geometry("1174x680+0+0")
root.resizable(False, False)

datetimeLabel = Label(root, font=('Times New Roman', 16, 'bold'))
datetimeLabel.place(x=5, y=5)


def clock():
    global date, currenttime
    date = time.strftime("%d:%m:%Y")
    currenttime = time.strftime("%H:%M:%S")
    datetimeLabel.config(text=f'    Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000, clock)


clock()

s = 'Student Management System'
count = 0
text = ''


def slider():
    global text, count
    if count == len(s):
        count = 0
        text = ''
    text = text + s[count]
    sliderLabel.config(text=text)
    count += 1
    sliderLabel.after(200, slider)


sliderLabel = Label(root, font=('Arial', 28, 'italic bold'), width=30)
sliderLabel.place(x=200, y=0)
slider()


def connect_database():
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(host=hostEntry.get(), user=usernameEntry.get(), password=passwordEntry.get())
            mycursor = con.cursor()
        except:
            messagebox.showerror("Error", "Invalid Details", parent=connectWindow)
            return
        try:
            query = 'CREATE DATABASE studentmanagementsystem;'
            mycursor.execute(query)
            mycursor.execute('USE studentmanagementsystem')
            mycursor.execute('''CREATE TABLE student (
                id INT PRIMARY KEY,
                name VARCHAR(30),
                mobile VARCHAR(10),
                email VARCHAR(30),
                address VARCHAR(100),
                gender VARCHAR(20),
                dob VARCHAR(20),
                date_field VARCHAR(50),
                added_time VARCHAR(50)
            )''')
        except:
            mycursor.execute('USE studentmanagementsystem')

        messagebox.showinfo("Success", "Database Connected", parent=connectWindow)
        connectWindow.destroy()

        addstudentButton.config(state=NORMAL)
        searchstudentButton.config(state=NORMAL)
        deletestudentButton.config(state=NORMAL)
        updatestudentButton.config(state=NORMAL)
        showstudentButton.config(state=NORMAL)
        exportstudentButton.config(state=NORMAL)

    connectWindow = Toplevel()
    connectWindow.grab_set()
    connectWindow.title("Database Connection")
    connectWindow.geometry("470x250+730+230")
    connectWindow.resizable(0, 0)

    hostnameLabel = Label(connectWindow, text="Host Name", font=('Arial',18 , 'bold'))
    hostnameLabel.grid(row=0, column=0, padx=20)
    hostEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    hostEntry.grid(row=0, column=1, padx=20)

    usernameLabel = Label(connectWindow, text="User Name", font=('Arial', 18, 'bold'))
    usernameLabel.grid(row=1, column=0, padx=20)
    usernameEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    usernameEntry.grid(row=1, column=1, padx=20)

    passwordLabel = Label(connectWindow, text="Password", font=('Arial', 18, 'bold'))
    passwordLabel.grid(row=2, column=0, padx=20)
    passwordEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2, show="*")
    passwordEntry.grid(row=2, column=1, padx=20)

    connectButton = ttk.Button(connectWindow, text="Connect", command=connect)
    connectButton.grid(row=3, columnspan=2)


connectButton = ttk.Button(root, text="Connect Database", command=connect_database)
connectButton.place(x=980, y=0)

leftFrame = ttk.Frame(root)
leftFrame.place(x=50, y=80, width=245, height=600)

logo_image = PhotoImage(file='students.png')
logo_Label = Label(leftFrame, image=logo_image)
logo_Label.grid(row=0, column=0, pady=10)

addstudentButton = ttk.Button(leftFrame, text="Add Student", width=25, state=DISABLED,
                              command=lambda: toplevel_data('Add Student', 'Add', add_data))
addstudentButton.grid(row=1, column=0, pady=10)

searchstudentButton = ttk.Button(leftFrame, text="Search Student", width=25, state=DISABLED,
                                 command=lambda: toplevel_data('Search Student', 'Search', search_data))
searchstudentButton.grid(row=2, column=0, pady=10)

updatestudentButton = ttk.Button(leftFrame, text="Update Student", width=25, state=DISABLED,
                                 command=lambda: toplevel_data('Update Student', 'Update', update_data))
updatestudentButton.grid(row=3, column=0, pady=10)

deletestudentButton = ttk.Button(leftFrame, text="Delete Student", width=25, state=DISABLED, command=delete_student)
deletestudentButton.grid(row=4, column=0, pady=10)

showstudentButton = ttk.Button(leftFrame, text="Show Student", width=25, state=DISABLED, command=show_student)
showstudentButton.grid(row=5, column=0, pady=10)

exportstudentButton = ttk.Button(leftFrame, text="Export Database", width=25, state=DISABLED, command=export_data)
exportstudentButton.grid(row=6, column=0, pady=10)

exitButton = ttk.Button(leftFrame, text="Exit", width=25, command=iexit)
exitButton.grid(row=7, column=0, pady=10)

rightFrame = ttk.Frame(root)
rightFrame.place(x=320, y=80, width=800, height=600)

scrollBarX = ttk.Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = ttk.Scrollbar(rightFrame, orient=VERTICAL)

studentTable = ttk.Treeview(
    rightFrame,
    columns=("Id", "Name", "Mobile No", "Email", "Address", "Gender", "D.O.B", "Added Date", "Added Time"),
    xscrollcommand=scrollBarX.set,
    yscrollcommand=scrollBarY.set
)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)
studentTable.pack(fill=BOTH, expand=1)

studentTable.heading('Id', text="Id")
studentTable.heading('Name', text="Name")
studentTable.heading('Mobile No', text="Mobile No")
studentTable.heading('Email', text="Email")
studentTable.heading('Address', text="Address")
studentTable.heading('Gender', text="Gender")
studentTable.heading('D.O.B', text="D.O.B")
studentTable.heading('Added Date', text="Added Date")
studentTable.heading('Added Time', text="Added Time")

studentTable.column('Id', width=50, anchor=CENTER)
studentTable.column('Name', width=300, anchor=CENTER)
studentTable.column('Email', width=300, anchor=CENTER)
studentTable.column('Mobile No', width=200, anchor=CENTER)
studentTable.column('Address', width=300, anchor=CENTER)
studentTable.column('Gender', width=100, anchor=CENTER)
studentTable.column('D.O.B', width=100, anchor=CENTER)
studentTable.column('Added Date', width=100, anchor=CENTER)
studentTable.column('Added Time', width=100, anchor=CENTER)

style = ttk.Style()

style.configure('Treeview', rowheight=40, font=('arial', 12, 'bold'), foreground='red4',
                background='white', fieldbackground='white')
style.configure('Treeview.Heading', font=('arial', 12, 'bold'), foreground='red')

studentTable.config(show='headings')

root.mainloop()
