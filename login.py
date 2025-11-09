from tkinter import *
from tkinter import messagebox
from PIL import ImageTk

def login():
    if usernameEntry.get() == "" or passwordEntry.get() == "":
        messagebox.showerror("Error","Please enter both fields")
    elif usernameEntry.get() == 'Nithesh' and passwordEntry.get() == 'ASVNITHESH@005':
        messagebox.showinfo('Success','Welcome')
        window.destroy()
        import SMS

    else:
        messagebox.showerror("Error","Please enter correct credentials")

window=Tk()

window.geometry("1280x700+0+0")
window.title("Login System of Student Management System")

window.resizable(False,False)

background_Image=ImageTk.PhotoImage(file='bg img.jpg')

bg_lable=Label(window,image=background_Image)
bg_lable.pack()

loginFrame=Frame(window)
loginFrame.place(x=400,y=160)

logoImg=ImageTk.PhotoImage(file='logo.png')
logolable= Label(loginFrame,image=logoImg)
logolable.grid(row=0,column=0,columnspan=2,pady=10)

usernameImage=PhotoImage(file='userprofile.png')
usernameLabel=Label(loginFrame,image=usernameImage, text="Username",compound=LEFT,font=("Times New Roman",17,"bold"))
usernameLabel.grid(row=1,column=0,pady=10,padx=20)

usernameEntry=Entry(loginFrame,font=("Times New Roman",20,"bold"),bd=5)
usernameEntry.grid(row=1,column=1,pady=10,padx=20)

passwordImage=PhotoImage(file='password.png')
passwordLabel=Label(loginFrame,image=passwordImage, text="Password",compound=LEFT,font=("Times New Roman",17,"bold"))
passwordLabel.grid(row=2,column=0,pady=10,padx=20)

passwordEntry=Entry(loginFrame,font=("Times New Roman",20,"bold"),bd=5)
passwordEntry.grid(row=2,column=1,pady=10,padx=20)

loginButton=Button(loginFrame,text='login',font=("Times New Roman",13,"bold"),bd=5,width=15
                   ,fg="white", bg="cornflower blue",activebackground="cornflower blue"
                   ,activeforeground='white',cursor='hand2',command=login)
loginButton.grid(row=3,column=1,pady=10,padx=20)

window.mainloop()
