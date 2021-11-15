from tkinter import *
from tkinter import messagebox, ttk
from tkinter.font import BOLD
from db_conn import readFromDb
from PIL import Image, ImageTk
from helpers import check_single_quote
from threading import Thread
import guli, tempfile, os, fitz

def read_ebooks():
    global loading
    global pdf_text
    global read_ebooks_screen
    global read_ebooks_icon
    global back_icon
    read_ebooks_screen = Toplevel()
    read_ebooks_icon = ImageTk.PhotoImage(Image.open("book_reading.png").resize((80, 80), Image.ANTIALIAS))
    back_icon = ImageTk.PhotoImage(Image.open("back.png").resize((30, 30), Image.ANTIALIAS))
    #text declaration
    txt_read_ebooks = "Read E-books"
    geometry_size = "1366x768"
    #screen size, maximize screen
    read_ebooks_screen.title(txt_read_ebooks)
    read_ebooks_screen.state("zoomed")
    read_ebooks_screen.geometry(geometry_size)
    #read_ebooks_screen.overrideredirect(True)
    #read_ebooks_screen.protocol("WM_DELETE_WINDOW", lambda _: disable_event())
    #back button
    Button(read_ebooks_screen, image = back_icon, cursor="hand2", command = close_page).place(x=15,y=15)
    #page title & icon
    Label(read_ebooks_screen, image = read_ebooks_icon).place(x=80, y=40)
    Label(read_ebooks_screen, text = txt_read_ebooks, font = ("Helvetica", 14, BOLD)).place(x=180, y = 70)
    #book title
    Label(read_ebooks_screen, text = "Book Title: " + guli.GuliVariable("read_book").get(), font = ("Helvetica", 12, BOLD)).place(x=80, y=140)
    #get book content
    get_book_content()
    generate_temp()
    #display PDF
    frame = Frame(read_ebooks_screen,width= 78,height= 35,bg="white")
    frame.place(x=80, y=170)
    scroll_y = Scrollbar(frame,orient="vertical")
    scroll_x = Scrollbar(frame,orient="horizontal")
    scroll_x.pack(fill="x",side="bottom")
    scroll_y.pack(fill="y",side="right")
    loading = ttk.Progressbar(frame,orient= HORIZONTAL,length=100,mode='determinate')
    loading.pack(side = TOP,fill=X)
    pdf_text = Text(frame,yscrollcommand=scroll_y.set,xscrollcommand= scroll_x.set,width= 78,height= 35)
    pdf_text.pack(side="left")
    scroll_x.config(command=pdf_text.xview)
    scroll_y.config(command=pdf_text.yview)
    Thread(target = add_to_pdf).start() 

def disable_event():
    pass

def add_to_pdf():
    global image
    image = []
    percentage = 0    

    open_pdf = fitz.open(temp_path)

    for page in open_pdf:
        pix = page.getPixmap()
        pix1 = fitz.Pixmap(pix,0) if pix.alpha else pix
        img = pix1.getImageData("ppm")
        pdf_img = PhotoImage(data = img)
        image.append(pdf_img)
        percentage += 1
        percentage_view = (float(percentage)/float(len(open_pdf))*float(100))
        loading['value'] = percentage_view
    
    loading.pack_forget()

    for i in image:
        pdf_text.image_create(END,image=i)
        pdf_text.insert(END,"\n\n")
    pdf_text.configure(state="disabled")   

def close_page():
    os.remove(temp_path)
    read_ebooks_screen.destroy()

def get_book_content():
    global result
    ebook = check_single_quote(guli.GuliVariable("read_book").get())
    dbQuery = """SELECT BookContent 
                FROM dbo.Books WITH(NOLOCK)
                WHERE Name = N'"""+ebook+"""' AND isActive = 1"""
    result = readFromDb(dbQuery)
    
    if result[0] == None:
        messagebox.showinfo("Failed Read","No PDF file available. Please try again later.", parent = read_ebooks_screen)
        close_page()

def generate_temp():
    global temp_path
    global book
    book = tempfile.NamedTemporaryFile(mode = "w+b", suffix=".pdf", delete=FALSE)
    temp_path = book.name
    book.write(result[0])
    book.close()
