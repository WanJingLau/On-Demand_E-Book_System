from tkinter import *
from tkinter import ttk, filedialog, scrolledtext, messagebox
from tkinter.font import BOLD
from PIL import Image, ImageTk
from db_conn import insertUpdateBookToDb, readFromDb
from helpers import check_front_end_space, check_single_quote

def upload_ebooks():
    global upload_ebooks_screen
    global uploadbooks_icon
    global upload_ebooks_image
    global search_combobox
    global book_name_entry
    global author_entry
    global summary_scrolledText
    global book_name
    global author
    global filename
    global bindata
    global lbl_no_file_chosen
    global txt_no_file_chosen
    global back_icon
    #variable declaration
    upload_ebooks_screen = Toplevel()
    uploadbooks_icon = ImageTk.PhotoImage(Image.open("uploadbooks.png").resize((80, 80), Image.ANTIALIAS))
    upload_ebooks_image = ImageTk.PhotoImage(Image.open("upload_ebooks_image.png").resize((360, 245), Image.ANTIALIAS))
    book_name = StringVar()
    author = StringVar()
    #text variable declaration
    txt_upload_ebooks = "Upload / Add E-books"
    geometry_size = "1366x768"
    txt_book_category = "Select Book Category"
    txt_book_name = "Enter Book Name"
    txt_author = "Enter Author"
    txt_summary = "Enter Book Summary"
    txt_content = "Book Content"
    txt_file = "Upload File (.pdf)"
    txt_submit = "Submit"  
    txt_no_file_chosen = "No File Chosen"
    #screen title,size, maximize windows
    upload_ebooks_screen.title(txt_upload_ebooks)
    upload_ebooks_screen.geometry(geometry_size)
    upload_ebooks_screen.state("zoomed")
    #back_button
    back_icon = ImageTk.PhotoImage(Image.open("back.png").resize((30, 30), Image.ANTIALIAS))
    Button(upload_ebooks_screen, image = back_icon, cursor="hand2", command = close_page).place(x=15,y=15)
    #page title
    Label(upload_ebooks_screen, image = uploadbooks_icon).place(x=80, y=40)
    Label(upload_ebooks_screen, image = upload_ebooks_image).place(x=1150, y=110)
    Label(upload_ebooks_screen, text = txt_upload_ebooks, font = ("Helvetica", 14, BOLD)).place(x=180, y = 70)
    #book_name
    Label(upload_ebooks_screen, text = txt_book_name, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=80,y=140)
    book_name_entry = Entry(upload_ebooks_screen, textvariable = book_name, font = "Helvetica 12", width=50)
    book_name_entry.place(x=80,y=170)
    book_name_entry.focus_set()
    #author
    Label(upload_ebooks_screen, text = txt_author, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=580,y=140)
    author_entry = Entry(upload_ebooks_screen, textvariable = author, font = "Helvetica 12", width=50)
    author_entry.place(x=580,y=170)
    #book category
    Label(upload_ebooks_screen, text = txt_book_category, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=80,y=210)
    search_combobox = ttk.Combobox(upload_ebooks_screen, values=("Action/Adventure", "Horror","Fantasy","Romance"), state = "readonly") 
    search_combobox.place(x=80,y=240)
    #upload file
    Label(upload_ebooks_screen, text = txt_content, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=580,y=210)
    Button(upload_ebooks_screen, text= txt_file, font = ("Helvetica", 12, BOLD), foreground="black", background="light grey", width=16, cursor="hand2", command = UploadAction).place(x=580,y=240)   
    lbl_no_file_chosen = Label(upload_ebooks_screen, text = txt_no_file_chosen, font = ("Helvetica", 12))
    lbl_no_file_chosen.place(x=760,y=245)
    #summary
    Label(upload_ebooks_screen, text = txt_summary, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=80,y=280)
    summary_scrolledText = scrolledtext.ScrolledText(upload_ebooks_screen, font = ("Helvetica", 12), width=105, height=10)
    summary_scrolledText.place(x=80,y=310)
    #Submit button
    Button(upload_ebooks_screen, text= txt_submit, font = ("Helvetica", 12, BOLD), foreground="white", background="blue", width=20, height=1, cursor="hand2", command = book_verify).place(x=590,y=550)

def UploadAction():
    filename = filedialog.askopenfilename(parent = upload_ebooks_screen, initialdir = "/", title = "Select file", filetypes = [("PDF files","*.pdf")])
    if filename:
        lbl_no_file_chosen.config(text = filename) #change no file chosen text to file path

def entry(entry):
   messagebox.showerror("Failed Upload", entry, parent = upload_ebooks_screen)

def book_verify():
    if len(book_name.get()) == 0 or book_name.get().isspace():
        entry("Book Name is empty. Please enter Book Name.")
    elif len(author.get()) == 0 or author.get().isspace():
        entry("Book Author is empty. Please enter Book Author.")
    elif len(search_combobox.get()) == 0:
        entry("No Book Category is selected. Please select Book Category.")
    elif lbl_no_file_chosen.cget("text") == txt_no_file_chosen:
        entry(txt_no_file_chosen + ". Please select a PDF file to upload.")
    elif len(summary_scrolledText.get("1.0", "end-1c")) == 0 or summary_scrolledText.get("1.0", "end-1c").isspace():
        entry("Book Summary is empty. Please enter Book Summary.")
    else:
        book_exist = check_book_exist()
        if book_exist != None:
            entry("Similar Book Name already added. Please add other new book.")
        else:
            add_book()

def check_book_exist():
    global new_book_name
    new_book_name = check_single_quote(check_front_end_space(book_name.get()))
    dbQuery = "SELECT TOP 1 1 FROM dbo.Books WITH(NOLOCK) WHERE Name = N'"+new_book_name+"' AND isActive = 1"
    result = readFromDb(dbQuery)
    return result

def add_book():
    with open(lbl_no_file_chosen.cget("text"), 'rb') as f:
        bindata = f.read()
    new_book_author = check_single_quote(author.get())
    new_book_summary = check_single_quote(summary_scrolledText.get("1.0", "end-1c"))
    dbQuery = """INSERT INTO dbo.Books (Name, Category, Author, Summary, BookContent, isActive)
                 VALUES(N'"""+new_book_name+"""',
                        N'"""+search_combobox.get()+"""',
                        N'"""+new_book_author+"""',
                        N'"""+new_book_summary+"""',
                        ?,1)"""
    result = insertUpdateBookToDb(dbQuery, bindata)
    if result == 1:
        messagebox.showinfo("Success", "New Book Upload Successfully", parent = upload_ebooks_screen)
        upload_ebooks_screen.destroy()
    else:
        entry("New Book Upload Failed. Please try again.")

def close_page():
    upload_ebooks_screen.destroy()