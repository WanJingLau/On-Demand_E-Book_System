import random
import smtplib
from tkinter import *
from tkinter.font import BOLD
from tkinter import messagebox
from tkinter.constants import N
from PIL import Image, ImageTk
from db_conn import readFromDb, insertUpdateDeleteToDb
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def forget_password():
    global forget_pw_screen
    global forget_pw_icon
    global back_icon
    global forget_password_image
    forget_pw_screen = Toplevel()
    forget_pw_icon = ImageTk.PhotoImage(Image.open("forget_password.png").resize((80, 80), Image.ANTIALIAS))
    forget_password_image = ImageTk.PhotoImage(Image.open("forget_password_image.png").resize((430, 320), Image.ANTIALIAS))

    #define text
    txt_forget_pw = "Forget Password?"
    txt_provide = "Please provide your email address to reset your password."
    txt_email = "Enter your email address"
    txt_submit = "Submit"
    txt_title = "E-Book System"
    geometry_size = "1366x768"
    global email
    global email_entry
    email = StringVar()
    Label(forget_pw_screen, image = forget_pw_icon).place(x=80, y=40)
    Label(forget_pw_screen, text = txt_forget_pw, font = ("Helvetica", 14, BOLD)).place(x=180, y = 70)
    Label(forget_pw_screen, image = forget_password_image).place(x=900, y=400)
    Label(forget_pw_screen, text = txt_provide, font = ("Helvetica", 12, BOLD)).place(x=80, y = 200)
    Label(forget_pw_screen, text = txt_email, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=80, y = 260) 
    email_entry = Entry(forget_pw_screen, font = "Helvetica 12", textvariable = email, width=50)
    email_entry.place(x=80,y=290)
    email_entry.focus_set()
    Button(forget_pw_screen, text=txt_submit, font = ("Helvetica", 12, BOLD), foreground="white", background="blue", width=20, height=1, cursor="hand2", command = reset_verify).place(x=590,y=500) 
    back_icon = ImageTk.PhotoImage(Image.open("back.png").resize((30, 30), Image.ANTIALIAS))
    Button(forget_pw_screen, image = back_icon, cursor="hand2", command = close_page).place(x=15,y=15)
    forget_pw_screen.title(txt_title)
    forget_pw_screen.state("zoomed")
    forget_pw_screen.geometry(geometry_size)
    forget_pw_screen.bind("<Return>", lambda e: reset_verify())

def reset_verify():
    if len(email.get()) == 0 or email.get().isspace():
        entry("Email address is empty. Please enter an email address.")
    else:
        dbQuery = "SELECT TOP 1 1 FROM dbo.Users WITH(NOLOCK) WHERE email = N'"+email.get().lower()+"'"
        result = readFromDb(dbQuery)
        if result == None:
            email_entry.delete(0, END)
            entry("Email address not found. Please re-enter your email address.")
        else:
            reset_password()

def entry(entry):
    messagebox.showerror("Failed Reset", entry, parent = forget_pw_screen)

def reset_password():
    try:
        email_info = email.get().lower()
        new_pw = pw_generator()
        dbQuery = """UPDATE dbo.Users 
                 SET password_hash = HASHBYTES('SHA2_512', '"""+new_pw+"""')
                 WHERE email = N'"""+email_info+"""'"""
    
        result = insertUpdateDeleteToDb(dbQuery)
        if result == 1:
            email_entry.delete(0, END)
            send_email(email_info, new_pw)
            reset_success()
    except:    
        entry("Reset failed. Please try again.")

def pw_generator():
    digits = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()"
    password =""

    for i in range(0, 8):
        password = password + random.choice(digits)
    return password

def send_email(email, password):
    sender_email = "ebook4006@gmail.com"
    sender_password = "ebookwjwc"
    dbQuery = "SELECT username FROM dbo.Users WITH(NOLOCK) WHERE email = N'"+email+"'"
    username = readFromDb(dbQuery)
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = "RESET PASSWORD FOR E-BOOK ACCCOUNT" 
    email_body_info = """Hi """+username[0]+""",

Reset Password Successfully. You may login with your new password.

Your new password: """+password+""" 


Thanks.


***** THIS IS AN AUTOMATED EMAIL. DO NOT REPLY *****"""

    message.attach(MIMEText(email_body_info, 'plain'))

    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(sender_email,sender_password)
    server.sendmail(sender_email,email,message.as_string())
    server.quit()

def reset_success():
    messagebox.showinfo("Success", "Password reset success. An email has been sent. Kindly check your email.", parent = forget_pw_screen)
    forget_pw_screen.destroy()

def close_page():
    forget_pw_screen.destroy()