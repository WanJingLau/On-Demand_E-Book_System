from tkinter import *
from tkinter.font import BOLD
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
from db_conn import insertUpdateDeleteToDb, readFromDb
from helpers import check_single_quote
import guli, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def help_center():
    global help_center_screen
    global help_center_icon
    global help_center_image
    global question_scrolledText
    global back_icon
    #variable declaration
    help_center_screen = Toplevel()
    help_center_icon = ImageTk.PhotoImage(Image.open("helpcenter.png").resize((80, 80), Image.ANTIALIAS))
    help_center_image = ImageTk.PhotoImage(Image.open("help_center_image.png").resize((275, 170), Image.ANTIALIAS))
    back_icon = ImageTk.PhotoImage(Image.open("back.png").resize((30, 30), Image.ANTIALIAS))
    #text variable declaration
    txt_help_center = "Help Center"
    geometry_size = "1366x768"
    txt_help = "Do you need help?"
    txt_user_question = "Enter Your Question:"
    txt_submit = "Submit"
    #screen title,size, maximize windows
    help_center_screen.title(txt_help_center)
    help_center_screen.geometry(geometry_size)
    help_center_screen.state("zoomed")
    #back button
    Button(help_center_screen, image = back_icon, cursor="hand2", command = close_page).place(x=15,y=15)
    #page title
    Label(help_center_screen, image = help_center_icon).place(x=80, y=40)
    Label(help_center_screen, image = help_center_image).place(x=1040, y=90)
    Label(help_center_screen, text = txt_help_center, font = ("Helvetica", 14, BOLD)).place(x=180, y = 70)
    #help
    Label(help_center_screen, text = txt_help, font = ("Helvetica", 12, BOLD), foreground = "black").place(x=80, y = 140)
    #user_question
    Label(help_center_screen, text = txt_user_question, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=80,y=180)
    question_scrolledText = scrolledtext.ScrolledText(help_center_screen, font = ("Helvetica", 12), width=105, height=10)
    question_scrolledText.place(x=80,y=210)
    question_scrolledText.focus_set()
    #Submit button
    Button(help_center_screen, text= txt_submit, font = ("Helvetica", 12, BOLD), foreground="white", background="blue", width=20, height=1, cursor="hand2", command = question_verify).place(x=590,y=500)

def close_page():
    help_center_screen.destroy()

def question_verify():
    if len(question_scrolledText.get("1.0", "end-1c")) == 0 or question_scrolledText.get("1.0", "end-1c").isspace():
        entry("Question is empty. Please enter a question.")
    else:
        question = check_single_quote(question_scrolledText.get("1.0", "end-1c"))
        email_address = guli.GuliVariable("email_add").get()
        dbQuery = """INSERT INTO [dbo].[UserHelpCenter] ([UserId], [Question])
                     SELECT Id, N'""" +question+"""'
                     FROM dbo.Users WITH(NOLOCK)
                     WHERE email = N'"""+email_address+"""'"""
        result = insertUpdateDeleteToDb(dbQuery)
        if result == 1:
            send_email(email_address)
            messagebox.showinfo("Success", "Question submitted. Kindly allow 3-5 working days for a response via e-mail. Thank you and have fun.", parent = help_center_screen)
            close_page()
        else:
            entry("Question submission Error occurred. Please try again.")

def entry(entry):
   messagebox.showerror("Failed Submit", entry, parent = help_center_screen)

def send_email(email):
    sender_email = "ebook4006@gmail.com"
    sender_password = "ebookwjwc"
    receiver_email = "lauwan08@gmail.com"
    dbQuery = "SELECT username FROM dbo.Users WITH(NOLOCK) WHERE email = N'"+email+"'"
    username = readFromDb(dbQuery)
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "NEW QUESTION SUBMITTED IN E-BOOK SYSTEM" 
    email_body_info = """Hi, user/admin has submitted new question via help center. 

Please find details below:


Username        : """+username[0]+"""

Email address : """+email+"""

Question          : """+question_scrolledText.get("1.0", "end-1c")+"""


Thanks.


***** THIS IS AN AUTOMATED EMAIL. DO NOT REPLY *****"""

    message.attach(MIMEText(email_body_info, 'plain'))

    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(sender_email,sender_password)
    server.sendmail(sender_email,receiver_email,message.as_string())
    server.quit()
