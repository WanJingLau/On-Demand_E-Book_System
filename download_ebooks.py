from tkinter import *
from tkinter import ttk, filedialog, messagebox
from tkinter.font import BOLD
from db_conn import insertUpdateDeleteToDb, readFromDb
from reportlab.pdfgen import canvas
from PIL import Image, ImageTk
from helpers import check_question_mark, check_single_quote, check_spacing
from threading import Thread
import guli, time

def download_ebooks():
    global download_ebooks_screen
    global downloadbooks_icon
    global progress_bar
    global lbl_progress
    global ebook
    global lbl_downloading
    download_ebooks_screen = Toplevel()
    downloadbooks_icon = ImageTk.PhotoImage(Image.open("download_ebooks.png").resize((80, 80), Image.ANTIALIAS))
    #text declaration
    txt_download_ebooks = "Download E-books"
    txt_downloading = "Downloading..."
    geometry_size = "1366x768"
    #screen title, screen size, maximize window
    download_ebooks_screen.title(txt_download_ebooks)
    download_ebooks_screen.state("zoomed")
    download_ebooks_screen.geometry(geometry_size)
    #page icon, title
    Label(download_ebooks_screen, image = downloadbooks_icon).place(x=80, y=40)
    Label(download_ebooks_screen, text=txt_download_ebooks, font=("Helvetica",14,BOLD)).place(x=180, y = 70)
    #downloading
    lbl_downloading = Label(download_ebooks_screen, text=txt_downloading, font=("Helvetica",12,BOLD))
    lbl_downloading.place(x = 80, y = 200)
    #book name
    ebook = guli.GuliVariable("download_book").get()
    Label(download_ebooks_screen, text= "Book Name: " + ebook, font=("Helvetica",12,BOLD)).place(x=80, y=240)
    #Progress
    lbl_progress = Label(download_ebooks_screen, text= "Progress: 20%", font=("Helvetica",12,BOLD))
    lbl_progress.place(x=80, y=280)
    #progress bar
    progress_bar = ttk.Progressbar(download_ebooks_screen, orient = HORIZONTAL, value=20, length = 400, mode = "determinate")
    progress_bar.place(x=80, y= 320)
    download_ebooks_screen.update_idletasks()
    Thread(target = get_pdf).start()

def download_action():
    global filename
    final_book_name = check_spacing(check_question_mark(ebook))
    filename = filedialog.asksaveasfilename(parent = download_ebooks_screen, initialdir = "~/Downloads", title = "Save As", initialfile= final_book_name,defaultextension = ".pdf", filetypes = [("PDF files","*.pdf")])
    if filename:
        progress_bar["value"] += 40
        lbl_progress.config(text= "Progress: 60%")
        download_ebooks_screen.update_idletasks()
        time.sleep(1)
        download_pdf()
    else:
        close_page()

def get_pdf():
    global result
    ebook1 = check_single_quote(ebook)
    dbQuery = """SELECT BookContent 
                FROM dbo.Books WITH(NOLOCK)
                WHERE Name = N'"""+ebook1+"""' AND isActive = 1"""
    result = readFromDb(dbQuery)
    if result[0] != None:
        download_action()
    else:
        messagebox.showinfo("Failed Download","No PDF file available. Please try again later.", parent = download_ebooks_screen)
        close_page()

def download_pdf():
    canvas.Canvas(filename)
    with open(filename, 'wb') as f:
        f.write(result[0])
        f.close()
    progress_bar["value"] += 40
    lbl_progress.config(text= "Progress: 100%")
    download_ebooks_screen.update_idletasks()
    time.sleep(1)
    update_download_quota()
    lbl_downloading.config(text="Download completed.")
    messagebox.showinfo("Download Success", "E-Book has downloaded successfully", parent = download_ebooks_screen)
    redirect()

def redirect():
    txt_redirect = "Redirecting to Favourite E-Books page in "
    txt_seconds = " seconds..."
    x = 3
    lbl_redirect = Label(download_ebooks_screen, text= txt_redirect + str(x) + txt_seconds, font=("Helvetica",12,BOLD))
    lbl_redirect.place(x=80, y=360)
    download_ebooks_screen.update_idletasks()
    for i in range(x-1):
        time.sleep(1)
        x -= 1
        if(x == 1):
            lbl_redirect.place(x=80, y=360)
            txt_second = " second...  "
            lbl_redirect.config(text=txt_redirect+str(x)+txt_second)
        else:
            lbl_redirect.place(x=80, y=360)
            lbl_redirect.config(text=txt_redirect+str(x)+txt_seconds)
        download_ebooks_screen.update_idletasks()   
    time.sleep(1.5)
    close_page()

def close_page():
    download_ebooks_screen.destroy()

def update_download_quota():
    email_address = guli.GuliVariable("email_add").get()

    dbQuery = """UPDATE dbo.UserCheckIn
                 SET DownloadQuota = DownloadQuota - 1
                 WHERE UserId = (
                                    SELECT Id 
                                    FROM dbo.Users WITH(NOLOCK) 
                                    WHERE email = N'"""+email_address+"""'
                                )"""
    insertUpdateDeleteToDb(dbQuery)
    return
