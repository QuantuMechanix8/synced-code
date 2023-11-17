import datetime
class book:
  def __init__(self, title, author, price, loan_period, rating):
    self.title, self.author, self.price, self.loan_period, self.rating, self.borrowed = title, author, price, loan_period, rating, False


class person:
  def __init__(self, name, age):
    self.name, self.age, self.owes = name, age, []
  
  def borrow(self, book):
    book.borrowed = True
    now = datetime.datetime.now()
    today = datetime.datetime.strptime(now, "%d/%m/%y")
    due_date = today + datetime.timedelta(book.loan_period)
    self.owes.append((book.title, due_date))

class minor(person):
  def __init__(self, name, age):
    person.__init__(self, name, age)
  
  def borrow(self, book):
    if book.rating == "U":
      book.borrowed = True
      today = datetime.datetime.now().strftime("%Y-%m-%d")
      due_date = today + (datetime.timedelta(book.loan_period)*2)
      self.owes.append((book.name, book.price, due_date))
    else:
      print("Age inappropriate book, cannot borrow")

class member(person):
  def __init__(self, name, age):
    person.__init__(self, name, age)

  def borrow(self, book):
    book.borrowed = True
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    due_date = today + (datetime.timedelta(book.loan_period)*2)
    self.owes.append((book.name, (book.price/2), due_date))



LOTR = book("Lord of the Rings", "J.R.R Tolkein", 10, 28, "U")
HP = book("Harry Potter", "J.K Rowling", 10, 35, "U")
SoG = book("50 Shades of Grey", "?", 15, 21, "R")
Colin = minor("Colin", 12)
James = member("James", 27)
Isadora = person("Isadora", 68)
Isadora.borrow(SoG)
print(Isadora.owes)

