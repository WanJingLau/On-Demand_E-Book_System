from db_conn import readFromDb
from tkinter.font import BOLD
from book_lists import book_lists
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from db_conn import readFromDb
import guli
from helpers import check_single_quote

def bookcategories():
    global book_categories_screen
    global book_categories_icon
    global book_categories_image
    global search_entry
    global action_adventure_icon
    global horror_icon
    global fantasy_icon
    global romance_icon
    global back_icon
    global search
    book_categories_screen = Toplevel()
    book_categories_icon = ImageTk.PhotoImage(Image.open("bookcategories.png").resize((80, 80), Image.ANTIALIAS))
    book_categories_image = ImageTk.PhotoImage(Image.open("book_categories_image.png").resize((230, 210), Image.ANTIALIAS))
    action_adventure_icon = ImageTk.PhotoImage(Image.open("action_adventure.png").resize((110, 120), Image.ANTIALIAS))
    horror_icon = ImageTk.PhotoImage(Image.open("horror.png").resize((110, 120), Image.ANTIALIAS))
    fantasy_icon = ImageTk.PhotoImage(Image.open("fantasy.png").resize((110, 120), Image.ANTIALIAS))
    romance_icon = ImageTk.PhotoImage(Image.open("romance.png").resize((110, 120), Image.ANTIALIAS))
    back_icon = ImageTk.PhotoImage(Image.open("back.png").resize((30, 30), Image.ANTIALIAS))
    search = StringVar()
    #text declaration
    txt_book_categories = "Book Categories"
    txt_search = "Search"
    geometry_size = "1366x768"
    txt_action_Adventure = "Action/Adventure"
    txt_horror = "Horror"
    txt_fantasy = "Fantasy"
    txt_romance = "Romance"
    #screen title, size, maximize windows
    book_categories_screen.title(txt_book_categories)
    book_categories_screen.state("zoomed")
    book_categories_screen.geometry(geometry_size)
    #page title, icon
    Label(book_categories_screen, image = book_categories_icon).place(x=80, y=40)
    Label(book_categories_screen, text = txt_book_categories, font = ("Helvetica", 14, BOLD)).place(x=180, y =70)
    Label(book_categories_screen, image = book_categories_image).place(x=1200, y=100)
    #back
    Button(book_categories_screen, image = back_icon, cursor="hand2", command = close_page).place(x=15,y=15)
    #search entry & button
    search_entry = Entry(book_categories_screen, font = "Helvetica 12", textvariable = search, width=80)
    search_entry.place(x=80,y=140) 
    Button(book_categories_screen, text=txt_search, font = ("Helvetica", 12, BOLD), foreground="white", background="blue", width=10, height=1, cursor="hand2", command = redirect_search_book_list).place(x=850,y=135)
    #action/adventure
    Label(book_categories_screen, image = action_adventure_icon).place(x=350, y=220)
    Button(book_categories_screen, text= txt_action_Adventure, font = ("Helvetica", 12, BOLD), width=16, height=1, cursor="hand2", command = lambda txt_action_Adventure=txt_action_Adventure: redirect_book_list(txt_action_Adventure)).place(x=320,y=360)
    #horror
    Label(book_categories_screen, image = horror_icon).place(x=900, y=220)
    Button(book_categories_screen, text = txt_horror, font = ("Helvetica", 12, BOLD), width=16, height=1, cursor="hand2", command = lambda txt_horror=txt_horror: redirect_book_list(txt_horror)).place(x=872.5,y=360)
    #fantasy
    Label(book_categories_screen, image = fantasy_icon).place(x=350, y=440)
    Button(book_categories_screen, text = txt_fantasy, font = ("Helvetica", 12, BOLD), width=16, height=1, cursor="hand2", command = lambda txt_fantasy=txt_fantasy: redirect_book_list(txt_fantasy)).place(x=320,y=580)
    #romance
    Label(book_categories_screen, image = romance_icon).place(x=900, y=440)
    Button(book_categories_screen, text = txt_romance, font = ("Helvetica", 12, BOLD), width=16, height=1, cursor="hand2", command = lambda txt_romance=txt_romance: redirect_book_list(txt_romance)).place(x=872.5,y=580)

def redirect_book_list(category):
    guli.GuliVariable("book_category").setValue(category)
    book_lists()

def redirect_search_book_list():
    if len(search.get()) == 0 or search.get().isspace():
        messagebox.showerror("Failed Search", "Search empty. Please enter a book name to search.", parent = book_categories_screen)
    else:
        book_name = check_single_quote(search_entry.get())
        dbQuery = """SELECT 1 FROM dbo.Books WITH(NOLOCK)
                     WHERE isActive = 1
                     AND Name LIKE '%'+'"""+book_name+"""'+'%'"""
        result = readFromDb(dbQuery)
        if result == None:
            messagebox.showinfo("Done Search", "No E-Book found. Please try another e-book name.", parent = book_categories_screen)
        else:
            guli.GuliVariable("book_category").setValue("Search")
            guli.GuliVariable("search_book").setValue(book_name)
            search_entry.delete(0, END)
            book_lists()

def close_page():
    book_categories_screen.destroy()