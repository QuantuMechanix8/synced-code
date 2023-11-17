import sqlite3
import hashlib
import numpy as np

login = sqlite3.connect("Passwords.db")
# login.execute('''CREATE TABLE Passwords
#          (UserID INT PRIMARY KEY  NOT NULL,
#          UserName   TEXT    NOT NULL,
#          Password   INT     NOT NULL,
#          Email TEXT NOT NULL);''')
def last(DBconnect):
	Cursor = DBconnect.cursor()
	Cursor.execute('SELECT * FROM Passwords')
	everything = (Cursor.fetchall())
	count = everything[-1][0]
	return count+1

def addUser(DBconnect):
	while True:
		Username = input("Enter their UserName: ")
		Password = input("Please enter their password: ")
		Email = input("Please enter their Email: ")
		DBconnect.execute("INSERT INTO Passwords (UserID,UserName,Password,Email) VALUES (?,?,?,?)",((last(DBconnect)) ,(Username), (Password), (Email)))
		if (input("any more users to enter? (y/n): ") == "n"):
			False

def outputDB(DBconnect):
	h = DBconnect.execute("SELECT UserID, UserName, Password, Email FROM Passwords")
	for row in h:
		print("UserID = ", row[0])
		print("UserName = ", row[1])
		print("Password = ", row[2])
		print("Email = ", row[3], "\n")

def signIn(DBconnect):
	cursor = DBconnect.cursor()
	Users = cursor.execute('SELECT UserName FROM passwords')
	Usernames = []
	for user in Users:
		Usernames.append(user[0])
	print(Usernames)
	username = str(input("enter your username: "))
	if username in Usernames:
		print("you exist on the database!")
		cursor.execute('SELECT Password FROM Passwords WHERE UserName = ?', (username,))
		password = cursor.fetchall()[0].__repr__()
		password = password[2:-3]
		print(password)
		if str(input("enter your password: ")) == password:
			print("you're in!")

def check(value, field, DBconnect):
	cursor = DBconnect.cursor()
	cursor.execute('SELECT ? FROM passwords WHERE ? = ?', (field, field, value,))
	if cursor.fetchall():
		return True
	return False

# if str(input("sign up? (if not enter something): ")) == (""):
# 	addUser(login)
# else:
# 	signIn(login)

	
