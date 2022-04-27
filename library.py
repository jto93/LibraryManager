#Create a library management system 
#Use Tkinter for GUI
from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry

#Book class
from book import Book
#Patron class
from patron import Patron
#SQLite Database
import sqlite3

#Creates the SQLite Tables if they do not already exist
def create_tables(cur):
    #Saves me from having to commit each executed change
    with connection: 

        #Patron Database
        patron_sql = """CREATE TABLE if not exists patrons (
                        id integer PRIMARY KEY, 
                        first text,
                        last text
                        ) """
        #Author Database
        author_sql = """CREATE TABLE if not exists authors (
                        id integer PRIMARY KEY, 
                        first text, 
                        last text,
                        birth date, 
                        death date,
                        country text
                        ) """
        #Book Database
        books_sql = """CREATE TABLE if not exists books (
                        ISBN integer PRIMARY KEY,
                        title text,
                        FOREIGN KEY (author_id) REFERENCES authors (id),
                        pages integer,
                        isCheckedOut bool                        
                        ) """
        #Check out records
        records_sql = """CREATE TABLE if not exists records (
                          id integer PRIMARY KEY, 
                          checkOut date,
                          expectedReturnDate date,
                          actualReturnDate date,
                          FOREIGN KEY (book_id) REFERENCES books (iSBN),
                          FOREIGN KEY (Patron_id) REFERENCES patrons (id)
                          ) """

        cur.execute(patron_sql)
        cur.execute(author_sql)
        cur.execute(books_sql)
        cur.execute(records_sql)
                
def main():

#Database Creation Section
    #global connection
    #connection = sqlite3.connect(':memory:')
    #Create a cursor to start running SQL commands 
    #global cur
    #cur = connection.cursor()
    #Create tables if it does not exist
    #create_tables(cur)

#Tkinter GUI Section 
    #View a Window
    window = Tk()
    #Set Window Size
    window.minsize(height=500, width=900)
    window.title("Library Manager")

    def home(): 

        def add_employee_page():
            title_label.destroy()
            add_book_page_button.destroy()
            add_patron_page_button.destroy()
            view_library_books_button.destroy()
            view_patron_list_button.destroy()
            add_book_label = Label(window, text="Add a Book", font=("Times_New_Roman"))
            add_book_label.pack()

            #Book Entry
            book_title = Label(window, text="Book: ", font=("Times_New_Roman"))
            book_title.pack()
            book_title.place(x=10, y=20)
            book_entry = Entry(window, width=30)
            book_entry.pack()
            book_entry.place(x=60, y=20)

            #Author Input
            author_title = Label(window, text="Author: ")
            author_title.pack()
            author_title.place(x=10, y=90)
            author_entry = Entry(window, width=30)
            author_entry.place(x=60, y=50)

            #ISBN Input
            isbn_title = Label(window, text="ISBN Entry: ")
            isbn_title.pack()
            isbn_title.place(x=10, y=50)
            isbn_entry = Entry(window, width=30)
            isbn_entry.place(x=80, y=90)

            def back(): 
                add_book_label.destroy()
                book_title.destroy()
                book_entry.destroy()
                author_title.destroy()
                author_entry.destroy()
                isbn_title.destroy()
                isbn_entry.destroy()
                add_book_button.destroy()
                back_button.destroy()
                home()

            add_book_button = Button(window, text="Add Book", font=("Times_New_Roman"), bg="Grey",fg="Black")
            add_book_button.pack()
            add_book_button.place(x=10,y=160)
            back_button = Button(window, text="Back to Main", font=("Times_New_Roman"), bg="Grey",fg="Black", command=back)
            back_button.pack()
            back_button.place(x=120,y=160)
           
        def add_patron_page(): 
            title_label.destroy()
            add_book_page_button.destroy()
            add_patron_page_button.destroy()
            view_library_books_button.destroy()
            view_patron_list_button.destroy()
            title3_label = Label(window, text="Add a Patron", font=("Times_New_Roman"))
            title3_label.pack()

            #First Name Entry
            name_title = Label(window, text="First: ", font=("Times_New_Roman"))
            name_title.pack()
            name_title.place(x=10, y=20)
            name_entry = Entry(window, width=30)
            name_entry.pack()
            name_entry.place(x=60, y=20) 

            #Last Name Entry
            last_name_title = Label(window, text="Last: ", font=("Times_New_Roman"))
            last_name_title.pack()
            last_name_title.place(x=10, y=90)
            last_name_entry = Entry(window, width=30)
            last_name_entry.pack()
            last_name_entry.place(x=60, y=90)  

            def back(): 
                title3_label.destroy()
                name_title.destroy()
                name_entry.destroy()
                last_name_title.destroy()
                last_name_entry.destroy()  
                add_patron_button.destroy()
                back_button.destroy()
                home()

            add_patron_button = Button(window, text="Add Patron", font=("Times_New_Roman"), bg="Grey",fg="Black")
            add_patron_button.pack()
            add_patron_button.place(x=10,y=160)
            back_button = Button(window, text="Back to Main", font=("Times_New_Roman"), bg="Grey",fg="Black", command=back)
            back_button.pack()
            back_button.place(x=120,y=160)

        def view_library_books():
            title_label.destroy()
            add_book_page_button.destroy()
            add_patron_page_button.destroy()
            view_library_books_button.destroy()
            view_patron_list_button.destroy()
            view_books_label = Label(window, text="View Books", font=("Times_New_Roman"))
            view_books_label.pack()

            def back(): 
                view_books_label.destroy()
                back_button.destroy()
                home()

            
            back_button = Button(window, text="Back to Main", font=("Times_New_Roman"), bg="Grey",fg="Black", command=back)
            back_button.pack()
            back_button.place(x=120,y=160)

        def view_patron_list():
            title_label.destroy()
            add_book_page_button.destroy()
            add_patron_page_button.destroy()
            view_library_books_button.destroy()
            view_patron_list_button.destroy()
            view_patrons_label = Label(window, text="View Patrons", font=("Times_New_Roman"))
            view_patrons_label.pack()

            def back(): 
                view_patrons_label.destroy()
                back_button.destroy()
                home()

            
            back_button = Button(window, text="Back to Main", font=("Times_New_Roman"), bg="Grey",fg="Black", command=back)
            back_button.pack()
            back_button.place(x=120,y=160)

        title_label = Label(window, text="Library Manager", font=("Times_New_Roman"))
        title_label.pack() 
        add_book_page_button = Button(window, text="Add Book", font=("Times_New_Roman"), command=add_employee_page)
        add_book_page_button.pack()
        add_patron_page_button = Button(window, text="Add New Patron", font=("Times_New_Roman"), command=add_patron_page)
        add_patron_page_button.pack()
        view_library_books_button = Button(window, text="View Books", font=("Times_New_Roman"), command=view_library_books)
        view_library_books_button.pack()
        view_patron_list_button = Button(window, text="View Patrons", font=("Times_New_Roman"), command=view_patron_list)
        view_patron_list_button.pack()

    home()
    window.mainloop()
main()