import random
from tkinter import *
from tkinter import messagebox
from tkinter.font import BOLD
from PIL import Image, ImageTk
from threading import Thread
from datetime import date, timedelta
import guli
from db_conn import readAllFromDb, readFromDb, insertUpdateDeleteToDb

def check_in_days():
    global check_in_days_screen
    global check_in_days_icon
    global check_in_days_image
    global back_icon
    global btn_check_in
    global frame_day
    global txt_check_in1
    global txt_download_quota
    global checked
    global lbl_word
    global lbl_download_quota
    #variable declaration
    checked = IntVar(value=1)
    check_in_days_screen = Toplevel()
    check_in_days_icon = ImageTk.PhotoImage(Image.open("checkin.png").resize((80, 80), Image.ANTIALIAS))
    check_in_days_image = ImageTk.PhotoImage(Image.open("check_in_days_image.png").resize((340, 250), Image.ANTIALIAS))
    back_icon = ImageTk.PhotoImage(Image.open("back.png").resize((30, 30), Image.ANTIALIAS))
    #text variable declaration
    txt_check_in_days = "Check In Days"
    geometry_size = "1366x768"
    txt_download_quota = " download quota"
    txt_check_in1 = "Check in to get "
    txt_check_in = txt_check_in1+str(1)+txt_download_quota
    #screen title,size, maximize windows
    check_in_days_screen.title(txt_check_in_days)
    check_in_days_screen.geometry(geometry_size)
    check_in_days_screen.state("zoomed")
    #back button
    Button(check_in_days_screen, image = back_icon, cursor="hand2", command = close_page).place(x=15,y=15)
    #page title
    Label(check_in_days_screen, image = check_in_days_icon).place(x=80, y=40)
    Label(check_in_days_screen, image = check_in_days_image).place(x=1000, y=90)
    Label(check_in_days_screen, text = txt_check_in_days, font = ("Helvetica", 14, BOLD)).place(x=180, y = 70)
    #display day
    frame_day = Frame(check_in_days_screen)
    frame_day.place(x=100, y = 200)
    checkButton_day()
    #encourage words
    frame_word = Frame(check_in_days_screen, height=100, width=850, borderwidth = 1, relief = SOLID)
    frame_word.place(x=100, y = 300)
    lbl_word = Label(frame_word, font = ("Helvetica", 12, BOLD))
    lbl_word.place(x=20, y=35)
    #total download quota
    Label(check_in_days_screen, text="Total Download Quota: ", font = ("Helvetica", 12, BOLD)).place(x=100, y = 430)
    lbl_download_quota = Label(check_in_days_screen, text = 0, font = ("Helvetica", 12, BOLD))
    lbl_download_quota.place(x=290, y=430)
    #check in button
    btn_check_in = Button(check_in_days_screen, text= txt_check_in, font = ("Helvetica", 12, BOLD), foreground="white", background = "blue", width=40, height=1, cursor="hand2", command = check_in)
    btn_check_in.place(x=500,y=500)
    get_word()
    Thread(target=get_check_in).start()

def checkButton_day():
    global checkbutton1, checkbutton2, checkbutton3, checkbutton4, checkbutton5, checkbutton6, checkbutton7
    global lbl_day1, lbl_day2, lbl_day3, lbl_day4, lbl_day5, lbl_day6, lbl_day7
    #day1
    checkbutton1 = Checkbutton(frame_day, width=4, state = DISABLED)
    checkbutton1.grid(row = 0, column=0,ipadx=20)
    lbl_day1 = Label(frame_day, text="Day 1", font=("Helvetica",12,BOLD))
    lbl_day1.grid(row=1, column=0,ipadx=20)
    #day2
    checkbutton2 = Checkbutton(frame_day, width=4, state = DISABLED)
    checkbutton2.grid(row = 0, column=1,ipadx=20)
    lbl_day2 = Label(frame_day, text="Day 2", font=("Helvetica",12,BOLD))
    lbl_day2.grid(row=1, column=1,ipadx=20)
    #day3
    checkbutton3 = Checkbutton(frame_day, width=4, state = DISABLED)
    checkbutton3.grid(row = 0, column=2,ipadx=20)
    lbl_day3 = Label(frame_day, text="Day 3", font=("Helvetica",12,BOLD))
    lbl_day3.grid(row=1, column=2,ipadx=20)
    #day4
    checkbutton4 = Checkbutton(frame_day, width=4, state = DISABLED)
    checkbutton4.grid(row = 0, column=3,ipadx=20)
    lbl_day4 = Label(frame_day, text="Day 4", font=("Helvetica",12,BOLD))
    lbl_day4.grid(row=1, column=3,ipadx=20)
    #day5
    checkbutton5 = Checkbutton(frame_day, width=4, state = DISABLED)
    checkbutton5.grid(row = 0, column=4,ipadx=20)
    lbl_day5 = Label(frame_day, text="Day 5", font=("Helvetica",12,BOLD))
    lbl_day5.grid(row=1, column=4,ipadx=20)
    #day6
    checkbutton6 = Checkbutton(frame_day, width=4, state = DISABLED)
    checkbutton6.grid(row = 0, column=5,ipadx=20)
    lbl_day6 = Label(frame_day, text="Day 6", font=("Helvetica",12,BOLD))
    lbl_day6.grid(row=1, column=5,ipadx=20)
    #day7
    checkbutton7 = Checkbutton(frame_day, width=4, state = DISABLED)
    checkbutton7.grid(row = 0, column=6,ipadx=20)
    lbl_day7 = Label(frame_day, text="Day 7", font=("Helvetica",12,BOLD))
    lbl_day7.grid(row=1, column=6,ipadx=20)

def get_check_in():
    global email_address
    global txt_today
    global result
    txt_today = "Today"
    email_address = guli.GuliVariable("email_add").get()
    dbQuery = """SELECT LastCheckInDate, CumulativeDay, DownloadQuota
                 FROM dbo.UserCheckIn WITH(NOLOCK)
                 WHERE UserId = (
                                    SELECT Id 
                                    FROM dbo.Users WITH(NOLOCK) 
                                    WHERE email = N'"""+email_address+"""'
                                )"""
    result = readFromDb(dbQuery)
    if result == None:
        lbl_day1.config(text=txt_today)
        guli.GuliVariable("new_check_in").setValue(1)
    else:
        lbl_download_quota.config(text=result[2])
        guli.GuliVariable("new_check_in").setValue(0)
        if result[0] == date.today() - timedelta(days = 1):
            check_cumulative_day_diff()
        elif result[0] == date.today():
            check_cumulative_day_same()
        else:
            lbl_day1.config(text=txt_today)

def check_cumulative_day_diff():
    global amount
    if result[1] == 1:
        checkbutton1.config(variable=checked)
        lbl_day2.config(text=txt_today)
    elif result[1] == 2:
        checkbutton1.config(variable=checked)
        checkbutton2.config(variable=checked)
        lbl_day3.config(text=txt_today)
    elif result[1] == 3:
        checkbutton1.config(variable=checked)
        checkbutton2.config(variable=checked)
        checkbutton3.config(variable=checked)        
        lbl_day4.config(text=txt_today)
    elif result[1] == 4:
        checkbutton1.config(variable=checked)
        checkbutton2.config(variable=checked)
        checkbutton3.config(variable=checked)
        checkbutton4.config(variable=checked)        
        lbl_day5.config(text=txt_today)
    elif result[1] == 5:
        checkbutton1.config(variable=checked)
        checkbutton2.config(variable=checked)
        checkbutton3.config(variable=checked)
        checkbutton4.config(variable=checked)
        checkbutton5.config(variable=checked)           
        lbl_day6.config(text=txt_today)
    elif result[1] == 6:
        checkbutton1.config(variable=checked)
        checkbutton2.config(variable=checked)
        checkbutton3.config(variable=checked)
        checkbutton4.config(variable=checked)
        checkbutton5.config(variable=checked)
        checkbutton6.config(variable=checked)        
        lbl_day7.config(text=txt_today)
    elif result[1] == 7:
        lbl_day1.config(text=txt_today)
    if result[1] != 7:
        amount = result[1] + 1
    else:
        amount = 1  
    btn_check_in.config(text= txt_check_in1+str(amount)+txt_download_quota)

def check_cumulative_day_same():
    if result[1] == 1:
        checkbutton1.config(variable=checked)
        lbl_day1.config(text=txt_today)
    elif result[1] == 2:
        checkbutton1.config(variable=checked)
        checkbutton2.config(variable=checked)
        lbl_day2.config(text=txt_today)
    elif result[1] == 3:
        checkbutton1.config(variable=checked)
        checkbutton2.config(variable=checked)
        checkbutton3.config(variable=checked)        
        lbl_day3.config(text=txt_today)
    elif result[1] == 4:
        checkbutton1.config(variable=checked)
        checkbutton2.config(variable=checked)
        checkbutton3.config(variable=checked)
        checkbutton4.config(variable=checked)        
        lbl_day4.config(text=txt_today)
    elif result[1] == 5:
        checkbutton1.config(variable=checked)
        checkbutton2.config(variable=checked)
        checkbutton3.config(variable=checked)
        checkbutton4.config(variable=checked)
        checkbutton5.config(variable=checked)           
        lbl_day5.config(text=txt_today)
    elif result[1] == 6:
        checkbutton1.config(variable=checked)
        checkbutton2.config(variable=checked)
        checkbutton3.config(variable=checked)
        checkbutton4.config(variable=checked)
        checkbutton5.config(variable=checked)
        checkbutton6.config(variable=checked)        
        lbl_day6.config(text=txt_today)
    elif result[1] == 7:
        checkbutton1.config(variable=checked)
        checkbutton2.config(variable=checked)
        checkbutton3.config(variable=checked)
        checkbutton4.config(variable=checked)
        checkbutton5.config(variable=checked)
        checkbutton6.config(variable=checked)
        checkbutton7.config(variable=checked)
        lbl_day7.config(text=txt_today)
    if result[1] != 7:
        amount = result[1] + 1
    else:
        amount = 1   
    btn_check_in.config(text= "Come back tomorrow to get "+str(amount)+txt_download_quota, state=DISABLED, background="white")

def check_in():
    global result1
    global amount
    if guli.GuliVariable("new_check_in").get() == 1:
        dbQuery_new = """INSERT INTO [dbo].[UserCheckIn] ([UserId],[LastCheckInDate],[CumulativeDay],[DownloadQuota])
                    SELECT Id,'"""+str(date.today())+"""', 1, 1
                    FROM dbo.Users WITH(NOLOCK)
                    WHERE email = N'"""+email_address+"""'"""
        result1 = insertUpdateDeleteToDb(dbQuery_new)
    else:
        if result[0] != date.today() - timedelta(days = 1):
            amount = 1

        dbQuery_existing = """UPDATE dbo.UserCheckIn
                              SET LastCheckInDate = '"""+str(date.today())+"""',
                                  CumulativeDay = CASE 
                                                    WHEN CumulativeDay = 7 OR LastCheckInDate != '"""+str(date.today() - timedelta(days = 1))+"""' THEN 1
                                                    ELSE CumulativeDay + 1
                                                  END,
                                  DownloadQuota = DownloadQuota + """+str(amount)+"""
                              WHERE UserId = (
                                                SELECT Id FROM dbo.Users WITH(NOLOCK)
                                                WHERE email = N'"""+email_address+"""'
                                             )"""
        result1 = insertUpdateDeleteToDb(dbQuery_existing)
    
    if result1 == 1:
        get_check_in()
    else:
        messagebox.showerror("Failed Check In", "Check In Failed. Please try again.", parent = check_in_days_screen)

def close_page():
    check_in_days_screen.destroy()

def get_word():
    digit = "0123456789"
    
    dbQuery = """SELECT Word 
                 FROM dbo.CheckInWords WITH(NOLOCK)
                 ORDER BY Id ASC
                 OFFSET """+random.choice(digit)+""" ROWS
                 FETCH NEXT 1 ROWS ONLY"""
    
    result = readAllFromDb(dbQuery)
    if result != None:
        for word in result:
            lbl_word.config(text=word[0])
