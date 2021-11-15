from tkinter import *
from tkinter import messagebox
from tkinter.constants import N
from tkinter.font import BOLD
from PIL import Image, ImageTk
from register import register
from forget_password import forget_password
from homePage import homepage
from db_conn import readFromDb
import guli

def login():
    global login_screen
    global logo
    global login_image
    login_screen = Tk()
    logo = ImageTk.PhotoImage(Image.open("logo.png").resize((80, 80), Image.ANTIALIAS))
    login_image = ImageTk.PhotoImage(Image.open("login_image.png").resize((360, 300), Image.ANTIALIAS))

    #define text
    txt_login = "Login"
    txt_title = "E-Book System"
    txt_welcome = "Welcome to E-Book System!"
    geometry_size = "1366x768"
    txt_greet = "Hi there! Nice to see you."
    txt_enter = "Please enter your email address and password to access your e-books account."
    txt_email = "Email"
    txt_password = "Password"
    txt_forget_pw  = "Forget your password?"
    txt_register_acc = "No account? Click here to register."
    global email 
    global password
    global email_entry
    global password_entry
    email = StringVar()
    password = StringVar()

    Label(login_screen, image = logo).place(x=649, y=20)
    Label(login_screen, image = login_image).place(x=1150, y=470)
    Label(login_screen, text = txt_welcome, font = ("Helvetica", 14, BOLD)).place(x=562, y = 110)
    Label(login_screen, text = txt_login, font = ("Helvetica", 12, BOLD)).place(x=80, y=180)
    Label(login_screen, text = txt_greet, font = ("Helvetica", 12)).place(x=80,y=210)
    Label(login_screen, text = txt_enter, font = ("Helvetica", 12, BOLD)).place(x=80,y=240)
    Label(login_screen, text = txt_email, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=80,y=280)
    email_entry = Entry(login_screen, font = "Helvetica 12", textvariable = email, width=50)
    email_entry.place(x=80,y=310)
    email_entry.focus_set()
    Label(login_screen, text = txt_password, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=80,y=350)
    password_entry = Entry(login_screen,font = "Helvetica 12", textvariable = password, width=50, show= '*')
    password_entry.place(x=80,y=380)
    lbl_forget_pw = Label(login_screen, text = txt_forget_pw, font = ("Helvetica", 12), foreground = "blue", cursor="hand2")
    lbl_forget_pw.place(x=80,y=420)
    lbl_forget_pw.bind("<Button-1>", lambda e: forget_password())
    Button(login_screen, text=txt_login, font = ("Helvetica", 12, BOLD), foreground="white", background="blue", width=20, height=1, cursor="hand2", command = login_verify).place(x=590,y=500)
    lbl_register_acc = Label(login_screen, text = txt_register_acc, font = ("Helvetica", 12), foreground = "blue", cursor="hand2")
    lbl_register_acc.place(x=575,y=550)
    lbl_register_acc.bind("<Button-1>", lambda e: register())
    login_screen.bind("<Return>", lambda e: login_verify())

    #login screen
    login_screen.title(txt_title)
    login_screen.state("zoomed")
    login_screen.geometry(geometry_size)
    login_screen.mainloop()

def login_verify():
    if len(email.get()) == 0 or len(password.get()) == 0 or email.get().isspace() or password.get().isspace():
        entry("Email/ Password is Empty.")
    else:
        email1 = email.get().lower()
        password1 = password.get()
    
        dbQuery = """SELECT TOP 1 1 FROM dbo.Users WITH(NOLOCK) 
                     WHERE email = N'"""+email1+"""' 
                     AND password_hash = HASHBYTES('SHA2_512', '"""+password1+"""')"""
        
        result = readFromDb(dbQuery)
        if result == None:
            entry("Wrong Email/ Invalid Password")
        else:
            guli.GuliVariable("email_add").setValue(email1)
            email_entry.delete(0, END)
            password_entry.delete(0, END)
            email_entry.focus_set()
            homepage()

 # Designing popup for entry empty/ login invalid password
def entry(entry):
    messagebox.showerror("Failed Login", entry, parent = login_screen)

login()