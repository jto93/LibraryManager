#Create a library management system 
#Use Tkinter for GUI
from tabnanny import check
from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry

from isbnLookup import getBookInfo

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
        check_patrons_sql = """SELECT EXISTS (
                                SELECT 
                                    name
                                FROM 
                                    sqlite_schema 
                                WHERE 
                                    type='table' AND 
                                    name='patrons'
                            );"""
        try: 
            cur.execute(check_patrons_sql)
        except:
            print('Check failure')
        
        res = cur.fetchone()
        res = res[0]
        if res == 1: 
            print('The tables already exist.')
            return

        fkey_command = "PRAGMA foreign_keys = ON"
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
                        id integer PRIMARY KEY,
                        title text,
                        pages integer,
                        summary text,
                        isCheckedOut bool, 
                        author_id integer NOT NULL,
                        FOREIGN KEY (author_id) 
                                REFERENCES authors (id)                      
                        ) """
        #Check out records database
        records_sql = """CREATE TABLE if not exists records (
                          id integer PRIMARY KEY, 
                          checkOut date,
                          expectedReturnDate date,
                          actualReturnDate date,
                          book_id integer,
                          patron_id integer,
                          FOREIGN KEY (patron_id) 
                                REFERENCES patrons (id),
                          FOREIGN KEY (book_id) 
                                REFERENCES books (id)
                          ) """
        #SQL execution and error handling
        try: 
            cur.execute(fkey_command)
            print('Fkey command ran. ')
        except Exception as e: 
            print(e)
            print('Error during Foreign Key enable')

        try: 
            cur.execute(patron_sql)
            print('Patron Table Created')

        except Exception as e: 
            print(e) 
            print('Error creating Patron Table')

        try: 
            cur.execute(author_sql)
            print('Author Table Created')
        except Exception as e: 
            print(e)
            print('Error creating Author Table')

        try:
            cur.execute(books_sql)
            print('Book Table created')
        except Exception as e: 
            print(e) 
            print('Error creating Book Table')
        
        try:
            cur.execute(records_sql)
            print('Record Table Created')

        except Exception as e: 
            print(e) 
            print('Error creating Record Table')
                
#SQL Database Functions
def add_book(isbn): 

    title, authors, pages, summary = getBookInfo(isbn)
    with connection:
        author = authors[0].split(' ')
        author_first = str(author[0])
        author_last = str(author[1])
        print("title: " + title)
        print("author first: " + author_first)
        print("author last: " + author_last)
        print("pages: " + str(pages))
        print("summary: " + summary)
#
        #Look up author in author table
        author_query_sql = """SELECT id from authors 
                                WHERE first IS '%s' AND last IS '%s'""" %(author_first,author_last)
        cur.execute(author_query_sql)

        author_id = cur.fetchone()
        
        if author_id != None:
           author_id = author_id[0]
        
        #If Author is not in table, add them to the list of authors
        if author_id is None:
            author_add_sql = """INSERT INTO authors (first,last)
                                    VALUES ('%s','%s')""" %(author_first,author_last)
            cur.execute(author_add_sql)
            cur.execute(author_query_sql)
            author_id = cur.fetchone()
            author_id = author_id[0]

        #Check if Book is already in collection
        book_query_sql = """SELECT * from books
                               WHERE title IS '%s' AND author_id is '%i'""" %(title,author_id)
        cur.execute(book_query_sql)
        book_id = cur.fetchone()

        #if Book is not in table, add to table
        if book_id is None: 
            book_add_sql = """INSERT INTO books (title,pages,summary, isCheckedOut,author_id)
                                VALUES ('%s','%i','%s','False','%i')"""%(title,pages,summary, author_id)
            cur.execute(book_add_sql)
            cur.execute(book_query_sql)
            book_id = cur.fetchone()
            print(book_id) 
        
        else: 
            print('Book is already part of collection!')

    #add_book_sql = """INSERT INTO books_sql (%s,%s,%i)"""

def get_books(): 
    with connection: 
        get_list_of_books_sql = """SELECT * FROM books"""
        cur.execute(get_list_of_books_sql)
        global book_list
        book_list = cur.fetchall()

def main():

#Database Creation Section
    global connection
    connection = sqlite3.connect('library.db')
    #Create a cursor to start running SQL commands 
    global cur
    cur = connection.cursor()
    #Create tables if they do not exist
    create_tables(cur)

#Tkinter GUI Section 
    #View a Window
    window = Tk()
    #Set Window Size
    window.minsize(height=200, width=400)
    window.title("Library Manager")
    window.iconbitmap('C:/Users/j_t_o/Desktop/Python Projects/Library/images/book.ico')

    #Home Page > Root page
    def home(): 

        def add_book_page():
            title_label.grid_remove()
            add_book_page_button.grid_remove()
            add_patron_page_button.grid_remove()
            view_library_books_button.grid_remove()
            view_patron_list_button.grid_remove()
            add_book_label = Label(window, text="Add a Book", font=("Times_New_Roman"))
            add_book_label.grid(row=0,column=0,columnspan=4)

            #Book Entry
            book_title = Label(window, text="Book: ", font=("Times_New_Roman"))
            book_title.grid(row=1,column=0)
            book_entry = Entry(window, width=30)
            book_entry.grid(row=1,column=1)

            #Author Input
            author_entry = Label(window, text="Author", font=("Times_New_Roman",12,"bold"))
            author_entry.grid(row=2,column=0,columnspan=3)
            author_first_title = Label(window, text="First: ", font=("Times_New_Roman"))
            author_first_title.grid(row=3,column=0)
            author_first_entry = Entry(window, width=30)
            author_first_entry.grid(row=3,column=1)
            author_last_title = Label(window, text="Last: ", font=("Times_New_Roman"))
            author_last_title.grid(row=4,column=0)
            author_last_entry = Entry(window, width=30)
            author_last_entry.grid(row=4,column=1)

            #ISBN Input
            isbn_title = Label(window, text="ISBN Entry: ", font=("Times_New_Roman"))
            isbn_title.grid(row=5,column=0)
            isbn_entry = Entry(window, width=30)
            isbn_entry.grid(row=5,column=1)

            def back(): 
                add_book_label.grid_remove()
                book_title.grid_remove()
                book_entry.grid_remove()
                author_entry.grid_remove()
                author_first_title.grid_remove()
                author_first_entry.grid_remove()
                author_last_title.grid_remove()
                author_last_entry.grid_remove()
                isbn_title.grid_remove()
                isbn_entry.grid_remove()
                add_book_button.grid_remove()
                back_button.grid_remove()
                home()

            add_book_button = Button(window, text="Add Book", font=("Times_New_Roman"), bg="Grey",fg="Black",command=lambda:add_book(isbn_entry.get()))
            add_book_button.grid(row=6,column=0,padx=20,pady=20)
            back_button = Button(window, text="Back", font=("Times_New_Roman"), bg="Grey",fg="Black", command=back)
            back_button.grid(row=6,column=1)
           
        def add_patron_page(): 
            title_label.grid_remove()
            add_book_page_button.grid_remove()
            add_patron_page_button.grid_remove()
            view_library_books_button.grid_remove()
            view_patron_list_button.grid_remove()
            title3_label = Label(window, text="Add a Patron", font=("Times_New_Roman"))
            title3_label.grid(row=0,column=0)

            #First Name Entry
            name_title = Label(window, text="First: ", font=("Times_New_Roman"))
            name_title.grid(row=1,column=0)
            name_entry = Entry(window, width=30)
            name_entry.grid(row=1,column=1)

            #Last Name Entry
            last_name_title = Label(window, text="Last: ", font=("Times_New_Roman"))
            last_name_title.grid(row=2,column=0)
            last_name_entry = Entry(window, width=30)
            last_name_entry.grid(row=2,column=1)

            def back(): 
                title3_label.grid_remove()
                name_title.grid_remove()
                name_entry.grid_remove()
                last_name_title.grid_remove()
                last_name_entry.grid_remove()  
                add_patron_button.grid_remove()
                back_button.grid_remove()
                
                home()

            add_patron_button = Button(window, text="Add Patron", font=("Times_New_Roman"), bg="Grey",fg="Black")
            add_patron_button.grid(row=3,column=0)
            back_button = Button(window, text="Back", font=("Times_New_Roman"), bg="Grey",fg="Black", command=back)
            back_button.grid(row=3,column=1)

        def view_library_books():
            title_label.grid_remove()
            add_book_page_button.grid_remove()
            add_patron_page_button.grid_remove()
            view_library_books_button.grid_remove()
            view_patron_list_button.grid_remove()
            view_books_label = Label(window, text="View Books", font=("Times_New_Roman"))
            view_books_label.grid(row=0,column=0)
            get_books()

            count = 0
            for i in book_list: 
                book_title_label = Label(window,text=i[1])
                book_title_label.grid(row=count+1,column=0)
                count += 1
                 

            def back(): 
                view_books_label.grid_remove()
                back_button.grid_remove()
                home()

            count += 1
            back_button = Button(window, text="Back", font=("Times_New_Roman"), bg="Grey",fg="Black", command=back)
            back_button.grid(row=count,column=0)

        def view_patron_list():
            title_label.grid_remove()
            add_book_page_button.grid_remove()
            add_patron_page_button.grid_remove()
            view_library_books_button.grid_remove()
            view_patron_list_button.grid_remove()
            view_patrons_label = Label(window, text="View Patrons", font=("Times_New_Roman"))
            view_patrons_label.grid(row=0,column=0)

            def back(): 
                view_patrons_label.grid_remove()
                back_button.grid_remove()
                home()

            
            back_button = Button(window, text="Back", font=("Times_New_Roman"), bg="Grey",fg="Black", command=back)
            last = 1
            back_button.grid(row=last,column=0)

        title_label = Label(window, text="Library Manager", font=("Times_New_Roman"))
        title_label.grid(row=0,column=0) 
        add_book_page_button = Button(window, text="Add Book", font=("Times_New_Roman"), command=add_book_page)
        add_book_page_button.grid(row=1,column=0)
        add_patron_page_button = Button(window, text="Add New Patron", font=("Times_New_Roman"), command=add_patron_page)
        add_patron_page_button.grid(row=2,column=0)
        view_library_books_button = Button(window, text="View Books", font=("Times_New_Roman"), command=view_library_books)
        view_library_books_button.grid(row=3,column=0)
        view_patron_list_button = Button(window, text="View Patrons", font=("Times_New_Roman"), command=view_patron_list)
        view_patron_list_button.grid(row=4,column=0)
        
    home()
    window.mainloop()
main()