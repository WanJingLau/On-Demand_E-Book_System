from tkinter import *
from tkinter import ttk
from tkinter.font import BOLD
from PIL import Image, ImageTk
from db_conn import readAllFromDb
from bookdetails import bookdetails
import guli

def book_lists():
    global book_lists_screen
    global back_icon
    global action_adventure_icon
    global horror_icon
    global fantasy_icon
    global romance_icon
    global search_icon
    global lbl_image
    global book_lists_title
    global scroll_canvas
    global scroll_frame2
    global home_icon
    book_lists_screen = Toplevel()
    action_adventure_icon = ImageTk.PhotoImage(Image.open("action_adventure_small.png").resize((80, 80), Image.ANTIALIAS))
    romance_icon = ImageTk.PhotoImage(Image.open("romance_small.png").resize((80, 80), Image.ANTIALIAS))
    fantasy_icon = ImageTk.PhotoImage(Image.open("fantasy_small.png").resize((80, 80), Image.ANTIALIAS))
    horror_icon = ImageTk.PhotoImage(Image.open("horror_small.png").resize((80, 80), Image.ANTIALIAS))
    search_icon = ImageTk.PhotoImage(Image.open("search_small.png").resize((80, 80), Image.ANTIALIAS))   
    back_icon = ImageTk.PhotoImage(Image.open("back.png").resize((30, 30), Image.ANTIALIAS))
 
    #text declaration
    geometry_size = "1366x768"
    book_lists_title = guli.GuliVariable("book_category").get()
    #screen title, size, maximize window
    book_lists_screen.title(book_lists_title)
    book_lists_screen.state("zoomed")
    book_lists_screen.geometry(geometry_size)
    #page title, icon
    lbl_image = Label(book_lists_screen)
    lbl_image.place(x=80, y=40)
    get_page_icon()
    Label(book_lists_screen, text = book_lists_title, font = ("Helvetica", 14, BOLD)).place(x=180, y =70)
    #back button
    Button(book_lists_screen, image = back_icon, cursor="hand2", command = close_page).place(x=15,y=15)
    #Frame 
    scroll_frame = Frame(book_lists_screen, height=475, width=1200, borderwidth = 1, relief=SOLID)
    scroll_frame.place(x=80, y = 180)
    #canvas with scroll bar
    scroll_canvas = Canvas(scroll_frame, width=1200, height=475)
    scroll_canvas.pack(side=LEFT, fill=BOTH, expand=1)
    canvas_scrollbar = ttk.Scrollbar(scroll_frame, orient = VERTICAL, command=scroll_canvas.yview)
    canvas_scrollbar.pack(side=RIGHT,fill=Y)
    scroll_canvas.configure(yscrollcommand=canvas_scrollbar.set)
    book_lists_screen.bind("<MouseWheel>", lambda e: scroll(e))
    scroll_frame.bind("<Configure>", lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox(ALL)))
    #2nd frame
    scroll_frame2 = Frame(scroll_canvas)
    scroll_canvas.create_window((0,0), window=scroll_frame2, anchor=NW)
    #display book list
    display_book_list()

def scroll(event):
    scroll_canvas.yview_scroll(int(-1*(event.delta/120)), UNITS)

def display_book_list():
    global row_frame
    txt_view_details = "View Details"   
    book_list = get_books()
    
    if book_list != []:
        y = 0
        for name in book_list:
            row_frame = Frame(scroll_frame2, height=50, width=1165, borderwidth = 1, relief = SOLID, background = "light grey", highlightcolor="light grey")
            row_frame.grid(row=y, column=0, padx=20, pady=15)
            Label(row_frame, text = name[0], background = "light grey",font = ("Helvetica", 12, BOLD)).place(x=20, y=12)
            Button(row_frame, text= txt_view_details, font = ("Helvetica", 12), width=20, height=1, cursor="hand2", command = lambda name=name: view_book(name[0])).place(x=800, y=7.5)
            y += 1

def get_books():
    global dbQuery
    if book_lists_title == "Search":
        dbQuery = """SELECT Name FROM dbo.Books WITH(NOLOCK)
                     WHERE isActive = 1
                     AND Name LIKE '%'+'"""+guli.GuliVariable("search_book").get()+"""'+'%'
                     ORDER BY Id ASC"""
    else:
        dbQuery = """SELECT Name
                    FROM dbo.Books WITH(NOLOCK)
                    WHERE isActive = 1
                    AND Category = '"""+guli.GuliVariable("book_category").get()+"""'
                    ORDER BY Id ASC"""
    result = readAllFromDb(dbQuery)
    return result

def view_book(book_name):
    guli.GuliVariable("book_name").setValue(book_name)
    bookdetails()

def get_page_icon():
    if book_lists_title == "Action/Adventure":
        lbl_image.config(image=action_adventure_icon)
    elif book_lists_title == "Horror":
        lbl_image.config(image=horror_icon)
    elif book_lists_title == "Fantasy":
        lbl_image.config(image=fantasy_icon)
    elif book_lists_title == "Romance":
        lbl_image.config(image=romance_icon)
    elif book_lists_title == "Search":
        lbl_image.config(image=search_icon)

def close_page():
    book_lists_screen.destroy()
