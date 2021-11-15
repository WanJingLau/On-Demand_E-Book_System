from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter.font import BOLD
from db_conn import readFromDb, insertUpdateDeleteToDb

def register():
    global register_screen
    global register_icon
    global register_image
    register_screen = Toplevel()
    register_icon = ImageTk.PhotoImage(Image.open("register.png").resize((80, 80), Image.ANTIALIAS))
    register_image = ImageTk.PhotoImage(Image.open("register_image.png").resize((350, 350), Image.ANTIALIAS))

    txt_register = "Register"
    txt_title = "E-Book System"
    geometry_size = "1366x768"
    txt_complete_form = "Complete the form below to create a new e-book account."
    txt_field_required = "Each field is required"
    txt_email = "Enter an email address"
    txt_screen_name = "Enter a display name"
    txt_enter_password = "Enter a password"
    txt_confirm_password = "Confirm password"
    txt_agree = "I agree to the Term of Services and Privacy Policy."
    txt_have_account = "Already have an account?"
    txt_sign_in = "Sign in here"

    global email
    global username
    global password
    global confirm_password
    global agree
    global email_entry
    global username_entry
    global password_entry
    global confirm_password_entry
    email = StringVar()
    username = StringVar()
    password = StringVar()
    confirm_password = StringVar()
    agree = IntVar()

    Label(register_screen, image = register_icon).place(x=80, y=40)
    Label(register_screen, image = register_image).place(x=950, y=210)
    Label(register_screen, text = txt_register, font = ("Helvetica", 14, BOLD)).place(x=180, y = 70)
    Label(register_screen, text = txt_complete_form, font = ("Helvetica", 12, BOLD)).place(x=80, y = 130)
    Label(register_screen, text = txt_field_required, font = ("Helvetica", 12, BOLD), foreground = "red").place(x=525, y = 130)
    Label(register_screen, text = txt_email, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=80, y = 190) 
    email_entry = Entry(register_screen, font = "Helvetica 12", textvariable = email, width=50)
    email_entry.place(x=80,y=220)
    email_entry.focus_set()  
    Label(register_screen, text = txt_screen_name, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=80, y = 260) 
    username_entry = Entry(register_screen, font = "Helvetica 12", textvariable = username, width=50)
    username_entry.place(x=80,y=290) 
    Label(register_screen, text = txt_enter_password, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=80, y = 330) 
    password_entry = Entry(register_screen, font = "Helvetica 12", textvariable = password, width=50,show= '*')
    password_entry.place(x=80,y=360) 
    Label(register_screen, text = txt_confirm_password, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=80, y = 400) 
    confirm_password_entry = Entry(register_screen, font = "Helvetica 12", textvariable = confirm_password, width=50,show= '*')
    confirm_password_entry.place(x=80,y=430) 
    Checkbutton(register_screen, font = ("Helvetica", 12, BOLD), text = txt_agree, variable=agree).place(x=80,y=470)
    Button(register_screen, text=txt_register, font = ("Helvetica", 12, BOLD), foreground="white", background="blue", width=20, height=1, cursor="hand2", command = register_verify).place(x=590,y=550)
    Label(register_screen, text = txt_have_account, font = ("Helvetica", 12, BOLD)).place(x=550, y = 590)
    lbl_sign_in = Label(register_screen, text = txt_sign_in, font = ("Helvetica", 12, BOLD), cursor="hand2",foreground = "blue")
    lbl_sign_in.place(x=750, y = 590)
    lbl_sign_in.bind("<Button-1>", lambda e: register_screen.destroy())
    
    register_screen.title(txt_title)
    register_screen.state("zoomed")
    register_screen.geometry(geometry_size)
    register_screen.bind("<Return>", lambda e: register_verify())

def register_verify():
    if len(email.get()) == 0 or email.get().isspace():
        entry("Email is empty. Please enter an email.")
    elif len(username.get()) == 0 or username.get().isspace():
        entry("Username is empty. Please enter a username.")
    elif len(password.get()) == 0 or password.get().isspace():
        entry("Password is empty. Please enter a password.")
    elif len(confirm_password.get()) == 0 or confirm_password.get().isspace():
        entry("Confirm Password is empty. Please enter confirm password.")
    elif password.get() != confirm_password.get():
        entry("Password and Confirm Password not matched. Please reenter password.")
    elif agree.get() != 1:
        entry("Please tick to agree the Terms of Services and Privacy Policy.")
    else:
        dbQuery = "SELECT TOP 1 1 FROM dbo.Users WITH(NOLOCK) WHERE email = N'"+email.get().lower()+"'"
        result = readFromDb(dbQuery)
        if result == None:
            register_user()
        else:
            entry("Email address registered before. Please enter a new email address.")

def entry(entry):
    messagebox.showerror("Failed Register", entry, parent = register_screen)

def register_user():
    email_info = email.get().lower()
    username_info = username.get()
    password_info = password.get()

    dbQueryInsertUser = """INSERT INTO dbo.Users (username, password_hash, email) 
                           VALUES(N'"""+username_info+"""', 
                                  HASHBYTES('SHA2_512', '"""+password_info+"""'), 
                                  N'"""+email_info+"""')"""

    dbQueryDeleteUser = """DELETE FROM dbo.Users 
                           WHERE email=N'"""+email_info+"""'
                           AND username=N'"""+username_info+"""'"""

    dbQueryInsertRole = """INSERT INTO dbo.UserRole (UserId, RoleId)
                           SELECT U.Id, R.Id
                           FROM dbo.Users U WITH(NOLOCK)
                           OUTER APPLY
                           (
                                SELECT Id FROM dbo.Roles WITH(NOLOCK)
                                WHERE Name = 'user'
                           )R
                           WHERE U.email = '"""+email_info+"""'"""
    
    result_insert_user = insertUpdateDeleteToDb(dbQueryInsertUser)
    if result_insert_user == 1:
        result_insert_role = insertUpdateDeleteToDb(dbQueryInsertRole)
        if result_insert_role == 1:
                email_entry.delete(0, END)
                username_entry.delete(0, END)
                password_entry.delete(0, END)
                confirm_password_entry.delete(0, END)
                register_success()
                return
        else:
            insertUpdateDeleteToDb(dbQueryDeleteUser)

    entry("Register failed. Please try again.")

def register_success():
    messagebox.showinfo("Success", "Register Success", parent = register_screen)
    register_screen.destroy()
