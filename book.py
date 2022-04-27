#Class Book
import datetime

class Book: 
    totalNumber = 0
    numIn = 0
    numOut = 0
    checkOutWindow = datetime.timedelta(days=14)
    
#Methods

    def __init__(self, title, author, ISBN):
        Book.add_Book()
        self.title = title
        self.author = author
        self.ISBN = ISBN
        self.pages = 0
        self.isCheckedOut = False
        self.checkOutDate = ""
        self.returnDate = ""
        self.curPatron = ""

#Class Methods
    @classmethod
    def number_of_books(cls):
        return cls.totalNumber
    
    @classmethod
    def number_of_books_in(cls):
        return cls.numIn

    @classmethod
    def number_of_books_out(cls):
        return cls.numOut

    @classmethod
    def add_Book(cls):
        cls.totalNumber += 1
        cls.numIn += 1

    @classmethod
    def remove_Book(cls):
        cls.totalNumber -= 1
        cls.numIn -= 1

    @classmethod
    def checkBookOut(cls):
        cls.numIn -= 1
        cls.numOut += 1

    @classmethod
    def checkBookIn(cls):
        cls.numIn += 1
        cls.numOut -= 1
    @classmethod 
    def getCheckOutWindow(cls):
        return cls.checkOutWindow

#Get
    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_ISBN(self):
        return self.ISBN
    
    def get_pages(self):
        return self.pages

    def getCheckedOut(self):
        return self.isCheckedOut

    def getCheckOutDate(self):
        return self.checkOutDate

    def getReturnDate(self):
        return self.returnDate

    def getCurrentPatron(self):
        return self.curPatron

    def getPast(self):
        return self.past

#Set 
    def set_title(self, newTitle):
        self.title = newTitle

    def set_author(self, newAuthor):
        self.author = newAuthor

    def set_ISBN(self, newISBN):
        self.ISBN = newISBN

    def set_pages(self, pages):
        self.pages = pages

    def checkOut(self, Patron):
        Book.checkBookOut()
        self.isCheckedOut = True
        self.checkOutDate = datetime.date.today()
        self.setReturnDate()
        self.curPatron = Patron
        print('Thanks %s, %s has been checked out. Your return date is %s.' %(self.curPatron, self.title, self.returnDate))

    def setReturnDate(self): 
        td = datetime.date.today()
        self.returnDate = td + Book.getCheckOutWindow()

    def checkIn(self): 
        Book.checkBookIn()
        tDate = datetime.date.today()
        x = tDate - self.returnDate
        if x.days > 0: 
            fee = x.days * .25
            print('%s was returned %i days late. You owe the library $%i' %(self.title, x.days, fee ))
        else: 
            x = x.days * -1
            print('Thanks for returning your book %s days early.' %(x))

        self.past.append([self.curPatron,self.checkOutDate,self.returnDate])
        self.isCheckedOut = False
        self.checkOutDate = 0
        self.returnDate = 0
        self.curPatron = 0