from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkinter.font import BOLD
from db_conn import readFromDb, insertUpdateDeleteToDb
import guli

def edit_profile():
    global edit_profile_screen
    global option_combobox
    global edit_profile_image
    global profile_icon
    global back_icon
    global txt_username
    global txt_password
    global lbl1
    global lbl2
    global lbl3
    global entry1
    global entry2
    global entry3
    global submit_button
    edit_profile_screen = Toplevel()
    profile_icon = ImageTk.PhotoImage(Image.open("profile.png").resize((80, 80), Image.ANTIALIAS))
    edit_profile_image = ImageTk.PhotoImage(Image.open("edit_profile_image.png").resize((150, 125), Image.ANTIALIAS))
    back_icon = ImageTk.PhotoImage(Image.open("back.png").resize((30, 30), Image.ANTIALIAS))
    #text declaration
    txt_edit_profile = "Edit Profile"
    geometry_size = "1366x768"
    txt_username = "Change Display Username"
    txt_password = "Change Password"
    txt_save = "Submit"
    #screen title, size, maximize screen
    edit_profile_screen.title(txt_edit_profile)
    edit_profile_screen.state("zoomed")
    edit_profile_screen.geometry(geometry_size)
    #back button
    Button(edit_profile_screen, image = back_icon, cursor="hand2", command = close_page).place(x=15,y=15)
    #page title
    Label(edit_profile_screen, image = profile_icon).place(x=80, y=40)
    Label(edit_profile_screen, image = edit_profile_image).place(x=1150, y=90)
    Label(edit_profile_screen, text = txt_edit_profile, font = ("Helvetica", 14, BOLD)).place(x=180, y = 70)
    #option to change
    Label(edit_profile_screen, text = "Select option to change",font = ("Helvetica", 12, BOLD), foreground="blue").place(x = 80, y=140)
    option_combobox = ttk.Combobox(edit_profile_screen, values=(txt_username,txt_password), state = "readonly", width=30) 
    option_combobox.place(x=80,y=170)
    option_combobox.bind("<<ComboboxSelected>>", lambda e : get_option())
    #entry1
    lbl1 = Label(edit_profile_screen, font = ("Helvetica", 12, BOLD), foreground = "blue")
    entry1 = Entry(edit_profile_screen, font = "Helvetica 12", width=50)
    #entry2
    lbl2 = Label(edit_profile_screen, font = ("Helvetica", 12, BOLD), foreground = "blue")
    entry2 = Entry(edit_profile_screen, font = "Helvetica 12", width=50)
    #entry3
    lbl3 = Label(edit_profile_screen, font = ("Helvetica", 12, BOLD), foreground = "blue")    
    entry3 = Entry(edit_profile_screen, font = "Helvetica 12", width=50)
    #submit button
    submit_button = Button(edit_profile_screen, text= txt_save, font = ("Helvetica", 12, BOLD), foreground="white", background="blue", width=20, height=1, cursor="hand2")
    
def close_page():
    edit_profile_screen.destroy()

def get_option():
    lbl1.place(x=80,y=270)
    entry1.place(x=80,y=300)
    lbl2.place(x=80,y=340)
    entry2.place(x=80,y=370)
    submit_button.place(x=590,y=550)

    if option_combobox.get() == txt_username:
        txt_old_username = "Current username"
        txt_new_username = "Enter new username"
        global username
        username = StringVar()
        edit_profile_screen.bind("<Return>", lambda e: username_verify())
        #Current username
        lbl1.config(text = txt_old_username)
        entry1.delete(0,END)
        entry1.config(show="")
        #new username
        lbl2.config(text = txt_new_username)
        entry2.delete(0,END)
        entry2.config(textvariable=username, show="")
        entry2.focus_set()
        #hide lbl3 & entry3
        lbl3.place_forget()
        entry3.place_forget()
        #config button
        submit_button.config(command=username_verify)
        #get current username
        getCurrentUsername()
    else:
        txt_old_password = "Enter old password"
        txt_new_password = "Enter new password"
        txt_confirm_password = "Confirm password"
        global old_password
        global new_password
        global confirm_new_password
        old_password = StringVar()
        new_password = StringVar()
        confirm_new_password = StringVar()
        edit_profile_screen.bind("<Return>", lambda e: password_verify())
        #entry1
        lbl1.config(text = txt_old_password)
        entry1.config(state=NORMAL, textvariable=old_password,show= '*')
        entry1.delete(0,END)
        entry1.focus_set()
        #entry2
        lbl2.config(text=txt_new_password)
        entry2.delete(0,END)
        entry2.config(textvariable=new_password,show= '*')
        #entry3
        lbl3.place(x=80,y=410)
        entry3.place(x=80,y=440)
        lbl3.config(text=txt_confirm_password)
        entry3.delete(0,END)
        entry3.config(textvariable=confirm_new_password,show= '*')
        #config button
        submit_button.config(command=password_verify)


def getCurrentUsername():
    global email_address
    email_address = guli.GuliVariable("email_add").get()
    dbQuery = """SELECT username FROM dbo.Users WITH(NOLOCK) WHERE email = N'"""+email_address+"""'"""
    result = readFromDb(dbQuery)
    entry1.insert(0, result[0])
    entry1.config(state=DISABLED)

def username_verify():
        if len(username.get()) == 0:
            entry("New username is empty. Please enter username")
        else:
            dbQuery = """UPDATE dbo.Users
                         SET username = N'"""+username.get()+"""'
                         WHERE email = N'"""+email_address+"""'"""
            result1 = insertUpdateDeleteToDb(dbQuery)
            if result1 == 1:
                change_success("Change Username Successfully")
                return
            
            entry("Change username failed. Please retry.")

def entry(entry):
    messagebox.showerror("Failed Edit Profile", entry, parent = edit_profile_screen)

def change_success(msg):
    messagebox.showinfo("Success", msg, parent = edit_profile_screen)
    edit_profile_screen.destroy()

def password_verify():
    if len(old_password.get()) == 0:
        entry("Old Password is empty. Please enter old password.")
    elif len(new_password.get()) == 0:
        entry("New Password is empty. Please enter new password.")
    elif len(confirm_new_password.get()) == 0:
        entry("Confirm Password is empty. Please enter confirm password.")
    elif new_password.get() != confirm_new_password.get():
        entry("New Password and Confirm Password not matched. Please reenter password.")
    else:
        email = guli.GuliVariable("email_add").get()
        dbQuery = """SELECT TOP 1 1 FROM dbo.Users WITH(NOLOCK) 
                     WHERE email = N'"""+email+"""' 
                     AND password_hash = HASHBYTES('SHA2_512', '"""+old_password.get()+"""')"""
        
        result = readFromDb(dbQuery)
        if result == None:
            entry("Wrong old password provided. Please reenter password.")
        else:
            dbQuery1 = """UPDATE dbo.Users
                          SET password_hash = HASHBYTES('SHA2_512', '"""+new_password.get()+"""')
                          WHERE email = N'"""+email+"""'"""
            result1 = insertUpdateDeleteToDb(dbQuery1)
            if result1 == 1:
                change_success("Change Password Successfully")
                return
            
            entry("Change password failed. Please retry.")