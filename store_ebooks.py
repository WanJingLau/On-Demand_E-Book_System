from tkinter import *
from tkinter import ttk, messagebox
from tkinter.font import BOLD
from PIL import Image, ImageTk
from download_ebooks import download_ebooks
from read_ebooks import read_ebooks
from review_ebooks import review_ebooks
from db_conn import readAllFromDb, insertUpdateDeleteToDb, readFromDb
from helpers import check_single_quote
import guli

#favourite books
def store_ebooks():
    global store_ebooks_screen
    global store_ebooks_icon
    global favorite_book_image
    global back_icon
    global scroll_frame2
    global scroll_canvas
    store_ebooks_screen = Toplevel()
    store_ebooks_icon = ImageTk.PhotoImage(Image.open("storebooks.png").resize((80, 80), Image.ANTIALIAS))
    favorite_book_image = ImageTk.PhotoImage(Image.open("favorite_book_image.png").resize((170, 160), Image.ANTIALIAS))
    back_icon = ImageTk.PhotoImage(Image.open("back.png").resize((30, 30), Image.ANTIALIAS))
    #text declaration
    txt_store_ebooks = "Favourite E-books"
    txt_display_ebooks = "Here is your favourite books and you can add more than 20 e-books."
    geometry_size = "1366x768"
    #screen size, maximize screen
    store_ebooks_screen.title(txt_store_ebooks)
    store_ebooks_screen.state("zoomed")
    store_ebooks_screen.geometry(geometry_size)
    #back button
    Button(store_ebooks_screen, image = back_icon, cursor="hand2", command = close_page).place(x=15,y=15)
    #page title & icon
    Label(store_ebooks_screen, image = store_ebooks_icon).place(x=80, y=40)
    Label(store_ebooks_screen, image = favorite_book_image).place(x=1170, y=35)
    Label(store_ebooks_screen, text = txt_store_ebooks, font = ("Helvetica", 14, BOLD)).place(x=180, y = 70)
    #display 20books
    Label(store_ebooks_screen, text = txt_display_ebooks, font = ("Helvetica", 12, BOLD)).place(x=80, y = 140)
    #Frame 
    scroll_frame = Frame(store_ebooks_screen, height=475, width=1200, borderwidth = 1, relief=SOLID)
    scroll_frame.place(x=80, y = 190)
    #canvas with scroll bar
    scroll_canvas = Canvas(scroll_frame, width=1200, height=475)
    scroll_canvas.pack(side=LEFT, fill=BOTH, expand=1)
    canvas_scrollbar = ttk.Scrollbar(scroll_frame, orient = VERTICAL, command=scroll_canvas.yview)
    canvas_scrollbar.pack(side=RIGHT,fill=Y)
    scroll_canvas.configure(yscrollcommand=canvas_scrollbar.set)
    store_ebooks_screen.bind("<MouseWheel>", lambda e: scroll(e))
    scroll_frame.bind("<Configure>", lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox(ALL)))
    #2nd frame
    scroll_frame2 = Frame(scroll_canvas)
    scroll_canvas.create_window((0,0), window=scroll_frame2, anchor=NW)
    #display favourite book
    display_favourite_book()

def scroll(event):
    scroll_canvas.yview_scroll(int(-1*(event.delta/120)), UNITS)

def close_page():
    store_ebooks_screen.destroy()

def display_favourite_book():
    global row_frame
    txt_no_favourite_book = "No favourite book found"
    txt_read = "Read"
    txt_download = "Download"
    txt_delete = "Delete"
    txt_review = "Review"
    #get favourite book
    favourite_book = get_favourite_book()
    if favourite_book != []:
        y = 0
        for name in favourite_book:
            row_frame = Frame(scroll_frame2, height=50, width=1165, borderwidth = 1, relief = SOLID, background = "light grey", highlightcolor="light grey")
            row_frame.grid(row=y, column=0, padx=20, pady=15)
            Label(row_frame, text = name[0], background = "light grey",font = ("Helvetica", 12, BOLD)).place(x=20, y=12)
            Button(row_frame, text= txt_read, font = ("Helvetica", 12), width=10, height=1, cursor="hand2", command = lambda name=name: read_book(name[0])).place(x=730, y=7.5)
            Button(row_frame, text= txt_download, font = ("Helvetica", 12), width=10, height=1, cursor="hand2", command = lambda name=name: download_book(name[0])).place(x=835, y=7.5)
            Button(row_frame, text= txt_delete, font = ("Helvetica", 12), width=10, height=1, cursor="hand2", command = lambda name=name: delete_favourite_book(name[0])).place(x=940, y=7.5)
            Button(row_frame, text= txt_review, font = ("Helvetica", 12), width=10, height=1, cursor="hand2", command = lambda name=name: review_book(name[0])).place(x=1045, y=7.5)
            y += 1
    else:
        Label(scroll_frame2, text = txt_no_favourite_book, font = ("Helvetica", 12, BOLD), foreground="grey").grid(padx=500, pady=225)

def get_favourite_book():
    global email_address
    email_address = guli.GuliVariable("email_add").get()
    dbQuery = """SELECT B.Name
                 FROM dbo.UserBookStore UBS WITH(NOLOCK)
                 INNER JOIN dbo.Books B WITH(NOLOCK) ON B.Id = UBS.BookId AND B.isActive = 1
                 WHERE UBS.UserId = (
                                        SELECT Id FROM dbo.Users WITH(NOLOCK) WHERE email = N'"""+email_address+"""'
                                    )
                 AND UBS.isActive = 1
                 ORDER BY UBS.Id ASC"""
    result = readAllFromDb(dbQuery)
    return result

def read_book(book_name):
    guli.GuliVariable("read_book").setValue(book_name)
    read_ebooks()

def download_book(book_name):
    dbQuery = """SELECT DownloadQuota
                 FROM dbo.UserCheckIn WITH(NOLOCK)
                 WHERE UserId = (
                                    SELECT Id 
                                    FROM dbo.Users WITH(NOLOCK) 
                                    WHERE email = N'"""+email_address+"""'
                                )"""
    result = readFromDb(dbQuery)
    if result != None and result[0] != 0:
        guli.GuliVariable("download_book").setValue(book_name)
        download_ebooks()
    else:
        messagebox.showwarning("Failed Download", "Unable to download. You have 0 download quota.", parent = store_ebooks_screen)

def delete_favourite_book(book_name):
    delete = messagebox.askyesno("Delete E-Books","Are you sure you want to delete this e-book from favourite?", parent = store_ebooks_screen)
    if delete:
        bookname = check_single_quote(book_name)
        dbQuery = """UPDATE dbo.UserBookStore 
                     SET isActive = 0 
                     WHERE BookId = (
                                        SELECT Id FROM dbo.Books WITH(NOLOCK) WHERE Name = N'"""+bookname+"""'
                                    )
                     AND UserId = (
                                    SELECT Id FROM dbo.Users WITH(NOLOCK) WHERE email = N'"""+email_address+"""'
                                  )
                     AND isActive = 1"""
        result = insertUpdateDeleteToDb(dbQuery)
        if result == 1:
            messagebox.showinfo("Success", "E-Book Delete From Favourite Successfully", parent = store_ebooks_screen)
            refresh_list()
        else:
            messagebox.showerror("Failed Delete", "E-Book Delete Failed. Please try again.", parent = store_ebooks_screen)

def review_book(book_name):
    book_name1 = check_single_quote(book_name)
    dbQuery = """SELECT 1 
                 FROM dbo.UserBookRating WITH(NOLOCK)
                 WHERE UserId = (
                                    SELECT Id FROM dbo.Users WITH(NOLOCK) WHERE email = N'"""+email_address+"""'
                                )
                 AND BookId = (
                                    SELECT Id FROM dbo.Books WITH(NOLOCK) WHERE Name = N'"""+book_name1+"""' AND isActive = 1
                              )"""
    result = readFromDb(dbQuery)
    if result == None:
        guli.GuliVariable("review_book").setValue(book_name)
        review_ebooks()
    else:
        messagebox.showinfo("Review Failed", "You have reviewed this book before. Please select another book. Thanks.", parent = store_ebooks_screen)

def refresh_list():
    for widget in scroll_frame2.winfo_children():
        widget.destroy()
    display_favourite_book()