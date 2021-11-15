from tkinter import *
from tkinter.font import BOLD
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from db_conn import readAllFromDb, readFromDb, insertUpdateDeleteToDb
from helpers import check_single_quote

def delete_ebooks():
    global delete_ebooks_screen
    global deleteebooks_icon
    global delete_ebooks_image
    global book_combobox
    global book_name_entry
    global book_category_entry
    global book_author_entry
    global back_icon
    delete_ebooks_screen = Toplevel()
    deleteebooks_icon = ImageTk.PhotoImage(Image.open("deleteebooks.png").resize((80, 80), Image.ANTIALIAS))
    delete_ebooks_image = ImageTk.PhotoImage(Image.open("delete_ebooks_image.png").resize((340, 260), Image.ANTIALIAS))
    back_icon = ImageTk.PhotoImage(Image.open("back.png").resize((30, 30), Image.ANTIALIAS))
    Button(delete_ebooks_screen, image = back_icon, cursor="hand2", command = close_page).place(x=15,y=15)
    #text variable declaration
    txt_delete_ebooks = "Delete E-Books"
    txt_select_book = "Select E-Books to delete"
    txt_delete = "Delete"
    geometry_size = "1366x768"
    txt_book_name = "Book Name:" 
    txt_book_author = "Book Author:"
    txt_book_category = "Book Category:"  
    #screen title, screen size, maximize window
    delete_ebooks_screen.title(txt_delete_ebooks)
    delete_ebooks_screen.state("zoomed")
    delete_ebooks_screen.geometry(geometry_size)
    #page icon, title
    Label(delete_ebooks_screen, image = deleteebooks_icon).place(x=80, y=40)
    Label(delete_ebooks_screen, image = delete_ebooks_image).place(x=990, y=65)
    Label(delete_ebooks_screen, text = txt_delete_ebooks, font = ("Helvetica", 14, BOLD)).place(x=180, y = 70)
    #book name selection
    Label(delete_ebooks_screen, text = txt_select_book, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=80,y=140)
    available_book = get_available_book()
    book_combobox = ttk.Combobox(delete_ebooks_screen, values = available_book, state = "readonly", width = 100)
    book_combobox.place(x=80, y= 170)
    book_combobox.bind("<<ComboboxSelected>>", lambda e : get_book_detail())
    #book name display
    Label(delete_ebooks_screen, text = txt_book_name, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=80,y=250)
    book_name_entry = Entry(delete_ebooks_screen, font = "Helvetica 12", state = DISABLED, width=80)
    book_name_entry.place(x=80, y=280)
    #book category display
    Label(delete_ebooks_screen, text = txt_book_category, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=80,y=320)
    book_category_entry = Entry(delete_ebooks_screen, font = "Helvetica 12", state = DISABLED, width=80)
    book_category_entry.place(x=80, y=350)
    #book author display
    Label(delete_ebooks_screen, text = txt_book_author, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=80,y=390)
    book_author_entry = Entry(delete_ebooks_screen, font = "Helvetica 12", state = DISABLED, width=80)
    book_author_entry.place(x=80, y=420)
    #delete button
    Button(delete_ebooks_screen, text= txt_delete, font = ("Helvetica", 12, BOLD), foreground="white", background="blue", width=20, height=1, cursor="hand2", command = delete_verify).place(x=590,y=500)

def get_available_book():
    available_book_list = []
    dbQuery = "SELECT Name FROM dbo.Books WITH(NOLOCK) WHERE isActive = 1 ORDER BY Id ASC"
    result = readAllFromDb(dbQuery)
    for book in result:
        available_book_list.append(book[0])    
    return available_book_list

def get_book_detail():
    book_name_entry.config(state = NORMAL)
    book_category_entry.config(state= NORMAL)
    book_author_entry.config(state= NORMAL)
    book_name_entry.delete(0,END)
    book_category_entry.delete(0,END)
    book_author_entry.delete(0,END)
    global book_name
    book_name = check_single_quote(book_combobox.get())
    dbQuery = """SELECT Category, Author
                 FROM dbo.Books WITH(NOLOCK) 
                 WHERE Name = N'"""+book_name+"""'
                  AND isActive = 1"""
    result1 = readFromDb(dbQuery)
    book_name_entry.insert(0, book_combobox.get())
    if result1 != None:
        book_category_entry.insert(0,result1[0])
        book_author_entry.insert(0, result1[1])
    book_name_entry.config(state = DISABLED)
    book_category_entry.config(state= DISABLED)
    book_author_entry.config(state= DISABLED)

def delete_verify():
    if len(book_combobox.get()) == 0:
        messagebox.showerror("Failed Delete", "No book selected. Please select a book to delete.", parent = delete_ebooks_screen)
    else:
        delete = messagebox.askyesno("Delete E-Books","Are you sure you want to delete this e-book?", parent = delete_ebooks_screen)
        if delete:
            dbQuery = "UPDATE dbo.Books SET isActive = 0 WHERE Name = N'"+book_name+"'"
            result = insertUpdateDeleteToDb(dbQuery)
            if result == 1:
                messagebox.showinfo("Success", "E-Book Delete Successfully", parent = delete_ebooks_screen)
                delete_ebooks_screen.destroy()
            else:
                messagebox.showerror("Failed Delete", "E-Book Delete Failed. Please try again.", parent = delete_ebooks_screen)

def close_page():
    delete_ebooks_screen.destroy()