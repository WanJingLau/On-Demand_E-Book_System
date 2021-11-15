from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter.font import BOLD
from PIL import Image, ImageTk
from db_conn import insertUpdateDeleteToDb
from helpers import check_single_quote
import guli

def review_ebooks():
    global review_screen
    global review_image
    global review_icon
    global back_icon
    global rating_spinbox
    global comment_scrolledText
    global review_book_name
    review_screen = Toplevel()
    book_name = StringVar()
    review_image = ImageTk.PhotoImage(Image.open("review_image.png").resize((580, 350), Image.ANTIALIAS))
    review_icon = ImageTk.PhotoImage(Image.open("review.png").resize((80, 80), Image.ANTIALIAS))

    #text declaration
    txt_review = "Review E-Book"
    geometry_size = "1366x768"
    txt_comments = "Comments:"
    txt_rating = "Rating (Please select star amount):"
    txt_submit = "Submit"
    txt_book_title = "Book Title:"
    #screen size, maximize windows
    review_screen.title(txt_review)
    review_screen.state("zoomed")
    review_screen.geometry(geometry_size)
    #back button
    back_icon = ImageTk.PhotoImage(Image.open("back.png").resize((30, 30), Image.ANTIALIAS))
    Button(review_screen, image = back_icon, cursor="hand2", command = close_page).place(x=15,y=15)
    #review image
    Label(review_screen, image = review_image).place(x=750, y=140)
    #page title, icon
    Label(review_screen, image=review_icon).place(x=80, y=40)
    Label(review_screen, text = txt_review, font = ("Helvetica", 14, BOLD)).place(x=180, y = 70)
    #book title
    Label(review_screen, text=txt_book_title, font = ("Helvetica", 12, BOLD), foreground="blue").place(x=80,y=140)
    book_name_entry = Entry(review_screen, textvariable = book_name, font = "Helvetica 12", width=68)
    book_name_entry.place(x=80, y=170)
    review_book_name = guli.GuliVariable("review_book").get()
    book_name_entry.insert(0, review_book_name)
    book_name_entry.config(state=DISABLED)
    #rating
    Label(review_screen, text = txt_rating, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=80, y=210)
    rating_spinbox = Spinbox(review_screen, from_= 1, to = 5, state="readonly", justify=CENTER, font=("Helvetica", 12, BOLD))
    rating_spinbox.place(x=80, y = 240)
    #comment
    Label(review_screen, text = txt_comments, font = ("Helvetica", 12, BOLD), foreground = "blue").place(x=80, y=280)
    comment_scrolledText = scrolledtext.ScrolledText(review_screen, font = ("Helvetica", 12), width=50, height=5)
    comment_scrolledText.place(x=80,y=310)
    comment_scrolledText.focus_set()
    #Submit button
    Button(review_screen, text= txt_submit, font = ("Helvetica", 12, BOLD), foreground="white", background="blue", width=20, height=1, cursor="hand2", command = review_verify).place(x=590,y=500)

def review_verify():
    email_address = guli.GuliVariable("email_add").get()
    new_review_book = check_single_quote(review_book_name)
    new_comment = check_single_quote(comment_scrolledText.get("1.0", "end-1c"))
    dbQuery = """INSERT INTO [dbo].[UserBookRating] ([UserId],[BookId],[Rating],[Comment])
                 SELECT U.Id, B.Id,"""+ rating_spinbox.get() +""",N'"""+new_comment+"""'
                 FROM dbo.Users U WITH(NOLOCK)
                 INNER JOIN dbo.Books B WITH(NOLOCK) ON B.Name = N'"""+new_review_book+"""' AND B.isActive = 1
                 WHERE U.email = N'"""+email_address+"""'"""
    result = insertUpdateDeleteToDb(dbQuery)
    if result == 1:
        messagebox.showinfo("Success Review", "E-Book Reviewed Successfully.", parent = review_screen)
        close_page()
    else:
        messagebox.showerror("Failed Review", "E-Book Review Failed. Please try again.", parent = review_screen)                

def close_page():
    review_screen.destroy()
