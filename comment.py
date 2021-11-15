from tkinter import *
from tkinter import ttk
from tkinter.font import BOLD
from PIL import Image, ImageTk
import guli
from helpers import check_single_quote
from db_conn import readAllFromDb

def comment():
    global comment_screen
    global comment_image
    global comment_icon
    global back_icon
    global scroll_canvas
    global scroll_frame2
    comment_screen = Toplevel()
    back_icon = ImageTk.PhotoImage(Image.open("back.png").resize((30, 30), Image.ANTIALIAS))
    comment_icon = ImageTk.PhotoImage(Image.open("comment_icon.png").resize((80, 80), Image.ANTIALIAS))
    comment_image = ImageTk.PhotoImage(Image.open("comment_image.png").resize((230, 170), Image.ANTIALIAS))
    
    #text declaration
    txt_comment = "Comments"
    geometry_size = "1366x768"
    #screen title, size, maximise windows
    comment_screen.title(txt_comment)
    comment_screen.state("zoomed")
    comment_screen.geometry(geometry_size)
    #back button
    Button(comment_screen, image = back_icon, cursor="hand2", command = close_page).place(x=15,y=15)
    #page title, icon
    Label(comment_screen, image=comment_icon).place(x=80, y=40)
    Label(comment_screen, text = txt_comment, font = ("Helvetica", 14, BOLD)).place(x=180, y=70)
    Label(comment_screen, image = comment_image).place(x=1090, y=18)
    #Frame 
    scroll_frame = Frame(comment_screen, height=475, width=1200, borderwidth = 1, relief=SOLID)
    scroll_frame.place(x=80, y = 180)
    #canvas with scroll bar
    scroll_canvas = Canvas(scroll_frame, width=1200, height=475)
    scroll_canvas.pack(side=LEFT, fill=BOTH, expand=1)
    canvas_scrollbar = ttk.Scrollbar(scroll_frame, orient = VERTICAL, command=scroll_canvas.yview)
    canvas_scrollbar.pack(side=RIGHT,fill=Y)
    scroll_canvas.configure(yscrollcommand=canvas_scrollbar.set)
    comment_screen.bind("<MouseWheel>", lambda e: scroll(e))
    scroll_frame.bind("<Configure>", lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox(ALL)))
    #2nd frame
    scroll_frame2 = Frame(scroll_canvas)
    scroll_canvas.create_window((0,0), window=scroll_frame2, anchor=NW)
    #display favourite book
    display_comment()

def scroll(event):
    scroll_canvas.yview_scroll(int(-1*(event.delta/120)), UNITS)

def display_comment():
    global row_frame
    txt_no_comments = "No comments"
    txt_username = "Username:"
    #get book comment
    book_comments = get_book_comments()
    if book_comments != []:
        y = 0
        for comment in book_comments:
            row_frame = Frame(scroll_frame2, height=80, width=1165, borderwidth = 1, relief = SOLID, background = "light grey", highlightcolor="light grey")
            row_frame.grid(row=y, column=0, padx=20, pady=15)
            Label(row_frame, text = txt_username, background = "light grey",font = ("Helvetica", 12, BOLD)).place(x=20, y=12)
            Label(row_frame, text = comment[0], background = "light grey",font = ("Helvetica", 12, BOLD)).place(x=110, y=12)
            Label(row_frame, text = comment[1], background = "light grey",font = ("Helvetica", 12, BOLD)).place(x=20, y=42)
            y += 1
    else:
        Label(scroll_frame2, text = txt_no_comments, font = ("Helvetica", 12, BOLD), foreground="grey").grid(padx=500, pady=225)

def get_book_comments():
    book_name = check_single_quote(guli.GuliVariable("book_name").get())
    dbQuery = """SELECT U.username, UBR.Comment
                 FROM dbo.UserBookRating UBR WITH(NOLOCK)
                 INNER JOIN dbo.Users U WITH(NOLOCK) ON U.Id = UBR.UserId
                 WHERE UBR.BookId = (
                                        SELECT Id FROM dbo.Books WITH(NOLOCK) WHERE Name = N'"""+book_name+"""'
                                    )
                 AND UBR.Comment != ''
                 ORDER BY UBR.Id DESC"""
    result = readAllFromDb(dbQuery)
    return result

def close_page():
    comment_screen.destroy()