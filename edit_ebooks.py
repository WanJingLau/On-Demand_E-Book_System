from tkinter import *
from tkinter.font import BOLD
from tkinter import ttk, messagebox, scrolledtext, filedialog
from PIL import Image, ImageTk
from db_conn import readAllFromDb, readFromDb, insertUpdateDeleteToDb, insertUpdateBookToDb
from helpers import check_single_quote

def edit_ebooks():
    global edit_ebooks_screen
    global editebooks_icon
    global edit_ebooks_image
    global back_icon
    global book_combobox
    global book_category_combobox
    global book_name_entry
    global book_category_entry
    global book_author_entry
    global author
    global summary_scrolledText
    global btn_upload_pdf
    global txt_no_file_chosen
    global lbl_no_file_chosen
    edit_ebooks_screen = Toplevel()
    editebooks_icon = ImageTk.PhotoImage(Image.open("editebooks.png").resize((80, 80), Image.ANTIALIAS))
    edit_ebooks_image = ImageTk.PhotoImage(Image.open("edit_ebooks_image.png").resize((435, 260), Image.ANTIALIAS))
    book_name = StringVar()
    author = StringVar()
    #text variable declaration
    txt_edit_ebooks = "Edit E-Books"
    geometry_size = "1366x768"
    txt_select_book = "Select E-Books to edit"
    txt_book_name = "Book Name:" 
    txt_book_author = "Book Author:"
    txt_book_category = "Book Category:"
    txt_book_summary = "Book Summary:"
    txt_book_content = "Book Content: *(upload only if there is new update on pdf file)"
    txt_file = "Upload File (.pdf)"
    txt_no_file_chosen = "No File Chosen"
    txt_submit = "Submit"
    back_icon = ImageTk.PhotoImage(Image.open("back.png").resize((30, 30), Image.ANTIALIAS))
    Button(edit_ebooks_screen, image = back_icon, cursor="hand2", command = close_page).place(x=15,y=15)
    #screen title, screen size, maximize window
    edit_ebooks_screen.title(txt_edit_ebooks)
    edit_ebooks_screen.state("zoomed")
    edit_ebooks_screen.geometry(geometry_size)
    #page icon, title
    Label(edit_ebooks_screen, image = editebooks_icon).place(x=80, y=40)
    Label(edit_ebooks_screen, image = edit_ebooks_image).place(x=1090, y=205)
    Label(edit_ebooks_screen, text = txt_edit_ebooks, font = ("Helvetica", 14, BOLD)).place(x=180, y = 70)
    #book name selection
    Label(edit_ebooks_screen, text = txt_select_book, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=80,y=140)
    available_book = get_available_book()
    book_combobox = ttk.Combobox(edit_ebooks_screen, values = available_book, state = "readonly", width = 100)
    book_combobox.place(x=80, y= 170)
    book_combobox.bind("<<ComboboxSelected>>", lambda e : get_book_detail())
    #book name display
    Label(edit_ebooks_screen, text = txt_book_name, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=80,y=200)
    book_name_entry = Entry(edit_ebooks_screen, textvariable = book_name, font = "Helvetica 12", state = DISABLED, width=50)
    book_name_entry.place(x=80, y=230)
    #author
    Label(edit_ebooks_screen, text = txt_book_author, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=580,y=200)
    book_author_entry = Entry(edit_ebooks_screen, textvariable = author, font = "Helvetica 12",state = DISABLED, width=50)
    book_author_entry.place(x=580,y=230)
    #book category
    Label(edit_ebooks_screen, text = txt_book_category, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=80,y=270)
    book_category_combobox = ttk.Combobox(edit_ebooks_screen, values=("Action/Adventure", "Horror","Fantasy","Romance"), state = DISABLED)
    book_category_combobox.place(x=80,y=300)
    #upload file
    Label(edit_ebooks_screen, text = txt_book_content, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=580,y=270)
    btn_upload_pdf = Button(edit_ebooks_screen, text= txt_file, font = ("Helvetica", 12, BOLD), state = DISABLED, foreground="black", background="light grey", width=16, cursor="hand2", command = UploadAction)
    btn_upload_pdf.place(x=580,y=300)   
    lbl_no_file_chosen = Label(edit_ebooks_screen, text = txt_no_file_chosen, font = ("Helvetica", 12))
    lbl_no_file_chosen.place(x=760,y=305)
    #summary
    Label(edit_ebooks_screen, text = txt_book_summary, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=80,y=340)
    summary_scrolledText = scrolledtext.ScrolledText(edit_ebooks_screen, state = DISABLED, font = ("Helvetica", 12), width=105, height=10)
    summary_scrolledText.place(x=80,y=370)
    #Submit button
    Button(edit_ebooks_screen, text= txt_submit, font = ("Helvetica", 12, BOLD), foreground="white", background="blue", width=20, height=1, cursor="hand2", command = edit_book_verify).place(x=590,y=620)


def get_available_book():
    available_book_list = []
    dbQuery = "SELECT Name FROM dbo.Books WITH(NOLOCK) WHERE isActive = 1 ORDER BY Id ASC"
    result = readAllFromDb(dbQuery)
    for book in result:
        available_book_list.append(book[0])    
    return available_book_list

def UploadAction():
    filename = filedialog.askopenfilename(parent = edit_ebooks_screen, initialdir = "/", title = "Select file", filetypes = [("PDF files","*.pdf")])
    if filename:
        lbl_no_file_chosen.config(text = filename) #change no file chosen text to file path

def get_book_detail():
    book_name_entry.config(state = NORMAL)
    book_category_combobox.config(state= "readonly")
    book_author_entry.config(state= NORMAL)
    btn_upload_pdf.config(state=NORMAL)
    summary_scrolledText.config(state=NORMAL)
    lbl_no_file_chosen.config(text = txt_no_file_chosen) #change to default
    book_name_entry.delete(0,END)
    book_author_entry.delete(0,END)
    summary_scrolledText.delete(1.0,END)
    global book_name
    book_name = check_single_quote(book_combobox.get())
    dbQuery = """SELECT Category, Author, Summary
                 FROM dbo.Books WITH(NOLOCK) 
                 WHERE Name = N'"""+book_name+"""'
                  AND isActive = 1"""
    result1 = readFromDb(dbQuery)
    book_name_entry.insert(0, book_combobox.get())
    book_name_entry.config(state = DISABLED)
    if result1 != None:
        book_category_combobox.set(result1[0])
        book_author_entry.insert(0, result1[1])
        summary_scrolledText.insert(INSERT, result1[2])

def entry(entry):
   messagebox.showerror("Failed Edit", entry, parent = edit_ebooks_screen)

def edit_book_verify():
    if len(book_combobox.get()) == 0:
        entry("No Book is selected. Please select a Book.")
    elif len(author.get()) == 0 or author.get().isspace():
        entry("Book Author is empty. Please enter Book Author.")
    elif len(summary_scrolledText.get("1.0", "end-1c")) == 0 or summary_scrolledText.get("1.0", "end-1c").isspace():
        entry("Book Summary is empty. Please enter Book Summary.")
    else:
        edit_book()

def close_page():
    edit_ebooks_screen.destroy()

def edit_book():
    global result
    global dbQuery
    new_author = check_single_quote(author.get())
    new_summary = check_single_quote(summary_scrolledText.get("1.0", "end-1c"))
    dbQuery = """UPDATE dbo.Books
                 SET Author = N'"""+new_author+"""',
                     Summary = N'"""+new_summary+"""' """
    
    if lbl_no_file_chosen.cget("text") != txt_no_file_chosen:
        with open(lbl_no_file_chosen.cget("text"), 'rb') as f:
            bindata = f.read()
        dbQuery = dbQuery + ", BookContent = ? WHERE Name = N'"+book_name+"'"
        result = insertUpdateBookToDb(dbQuery, bindata)
    else:
        dbQuery = dbQuery + "WHERE Name = N'"+book_name+"'"
        result = insertUpdateDeleteToDb(dbQuery)
    
    if result == 1:
        messagebox.showinfo("Success", "Book Edit Successfully", parent = edit_ebooks_screen)
        edit_ebooks_screen.destroy()
    else:
        entry("Book Edit Failed. Please try again.")
