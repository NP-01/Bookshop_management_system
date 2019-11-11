import time
import random, math
import re
import pickle
import os
import getpass
import smtplib
import colorama
import sys
from colorama import Fore, Style
#----------------------------------------OTP_VALIDATION---------------------------------------------------------

def Get_OTP():
	digits = "0123456789"
	OTP = ""
	for i in range(6) : 
		OTP += digits[math.floor(random.random() * 10)] 
	return OTP

def Send_OTP():
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls()
	ID = input("Enter customer id:  ")
	C = Customer(0)
	with open('customers.txt', 'rb') as file:
		while C.id != ID:
			C = pickle.load(file)
	otp = Get_OTP()
	s.login("iiitn.bookshop@gmail.com", "lsx7P%jD14OtgrNr73eG")
	message = otp
	s.sendmail("iiitn.bookshop@gmail.com", C.email_id, message)
	s.quit()
	return otp

def Send_ID(cust_id, email_id):
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls()
	s.login("iiitn.bookshop@gmail.com", "lsx7P%jD14OtgrNr73eG")
	message = cust_id
	s.sendmail("iiitn.bookshop@gmail.com", email_id, message)
	s.quit()
#----------------------------------------BOOK---------------------------------------------------------

class Book:
	def __init__(self,a):
		random.seed(time.time())
		self.status = a
		self.id = "BID00000"
		if(a==1):
			self.status = a
			self.id = "BID" + str(int((random.random()*(10**6))))
			
			self.name = input("\nName:  ")
			regex_name = re.compile(r'^([a-z]+)( [a-z]+)*( [a-z]+)*( [0-9])*$', re.IGNORECASE) 
			while (bool(regex_name.search(self.name)) == False):
				print("Invalid Book Name!\nEnter the book name again: ")
				self.name = input()
				
			self.author =(input("\nAuthor:  "))
			regex_author = re.compile(r'^([a-z]+)(.+)*( +)*([a-z]+)*(.+)( )*([a-z]+)*$', re.IGNORECASE)
			#regex_author = re.compile(r'^([a-z]+)*(.+)*( +)*([a-z]+)*(.+)*( +)*([a-z]+)*$', re.IGNORECASE)
			while (bool(regex_author.search(self.author)) == False):
				print("Invalid Name!\nEnter author again: ",end=" ")
				self.author = input()

			while True:
				try:
					self.price= int(input("\nPrice:  "))
					self.number_of_pages = int(input("\nNo. of Pages:  "))
					break
				except ValueError:
					print("Invalid Price or No. of Pages! Enter again.\n")
			
			self.stock = 1

	# Operator Overloading
	def __add__(self,n):
		self.stock = self.stock + 1
	def __sub__(self,n):
		self.stock = self.stock - 1

	# Function Overwriting
	def __str__(self):
		if(self.status==1):
			return "%s\t%s\t\t%s" % (self.id,self.author,self.name)
		else:
			return "\n\nEND OF FILE"
	def showdata(self):
		print("The details of desired book are as follows: ")
		print("ID = ",self.id)
		print("Name = ",self.name)
		print("Author = ",self.author)
		print("Price = ",self.price)
		print("No. of Pages = ",self.number_of_pages)
		print("No. of Copies = ",self.stock)

def Display_All_Book():
		os.system("clear")
		print("Book List")
		print("\n-----------------------------------------------------------------------------------------------------------------------------------")
		print("-----------------------------------------------------------------------------------------------------------------------------------")
		print("Sr.no\t  ID\t\tAuthor Name\t\t\tName")
		print("-----------------------------------------------------------------------------------------------------------------------------------")
		print("-----------------------------------------------------------------------------------------------------------------------------------")
		l = 1
		with open('book.txt','rb') as file:
			while True:
				try:
					B = pickle.load(file)
					if B.stock >= 1:
						print(l,"\t",B,Fore.YELLOW + "IN STOCK")
						print(Style.RESET_ALL)
					else:
						print(l,"\t",B,Fore.BLUE + "OUT OF STOCK")
						print(Style.RESET_ALL) 
					l = l + 1

				except EOFError:
					print("\n\nFile finished.......")
					break

def Create_Book():
	os.system("clear")
	B = Book(1) 
	with open('book.txt', 'rb+') as file:
		while True:
			try:
				B1 = pickle.load(file)
				if(B1.name == B.name):
					print("Book already exists !")
					print("Number of copies: ",B1.stock,"\nDo you wish to increment the stock ?...(y/n)")
					ch = input()
					if ch == 'y':
						books = []

						with open('book.txt','rb') as file:
							while True:
								try:
									books.append(pickle.load(file))
								except EOFError:
									break

						for i in range(0,len(books)) :
							if books[i].id == B1.id :
								break

						B1 = books[i]
						B1+1
						os.system("rm book.txt")
						os.system("touch book.txt")

						for book in books:
							with open('book.txt','ab') as file:
								pickle.dump(book,file)

						break
					else:
						break
			except EOFError:
				with open('book.txt','ab') as file:
					pickle.dump(B,file)
				break
	print("\n\nCreating Book Record. Please Wait...........")
	time.sleep(3)
	print("\nBook Record Created...")

def Display_Book(book_id):
	os.system("clear")
	B = Book(0)
	with open('book.txt','rb') as file:
		while(book_id != B.id):
			B = pickle.load(file)

	B.showdata()
	if B.stock >= 1:
		print("Book is in stock\n")
	else:
		print("Book is out of stock\n")

def Modify_Book(book_id):
	os.system("clear")
	books = []

	with open('book.txt','rb') as file:
		while True:
			try:
				books.append(pickle.load(file))
			except EOFError:
				break

	for i in range(0,len(books)) :
		if books[i].id == book_id :
			break

	B = books[i]
	
	print("Choose the parameter to modify:\n\n[1]Name\n\n[2]Author\n\n[3]Price\n\n[4]Number of Pages\n\n[5]Update the stock")
	p = int(input())
		
		
	if(p==1):
		B.name = input("Enter the new data:  ")
	
	elif(p==2):
		B.author = input("Enter the new data:  ")
		
	elif(p==3):
		B.price = int(input("Enter the new data:  "))
	
	elif(p==4):
		B.number_of_pages = int(input("Enter the new data:  "))

	elif(p==5):
		n = int(input("Enter [1] to increment the stock else enter [2] to decrement the stock:  "))

		if n==1:
			B+1
		if n==2:
			B-1
		else:
			print("\n\nInvalid!\n\n")
		
	else:
		print("Invalid Option!")
	
	os.system("rm book.txt")
	os.system("touch book.txt")

	for book in books:
		with open('book.txt','ab') as file:
			pickle.dump(book,file)

	if p==1 or p==2 or p==3 or p==4 or p==5:
		print("\nModifying Book Record........Please Wait")
		time.sleep(3)
		print("Book Record Modified")

def Delete_Book(book_id):
	os.system("clear")
	books = []

	with open('book.txt','rb') as file:
		while True:
			try:
				books.append(pickle.load(file))
			except EOFError:
				break

	for i in range(0,len(books)) :
		if books[i].id == book_id :
			break

	del books[i]

	os.system("rm book.txt")
	os.system("touch book.txt")

	for book in books:
		with open('book.txt','ab') as file:
			pickle.dump(book,file)

	print("\nDeleting Books Record........Please Wait")
	time.sleep(3)
	print("Book Record Deleted")

#----------------------------------------/BOOK--------------------------------------------------------

#----------------------------------------Customer-----------------------------------------------------
#This is the regular expression format for validating email-id
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

# Mobile no. and email-id validator
def isValid(s,n):
	if n==1:
		Pattern = re.compile("(0/91)?[7-9][0-9]{9}") 
		return Pattern.match(s)
	elif n==2:
		return re.search(regex,s)

class Customer:
	def __init__(self,a):
		random.seed(time.time())
		self.status = a
		self.id = "UID00000"
		if(a==1):
			self.status = a
			self.id = "UID" + str(int((random.random()*(10**6))))
			
			self.name = input("\nName:  ")
			while (bool(re.fullmatch('[A-Za-z]{2,25}( [A-Za-z]{2,25})?', self.name)) == False):
				print("Invalid Name!\nEnter your name again: ",end=" ")
				self.name = input()
			
			while True:
				try:
					self.age = int(input("\nAge:  "))
					break
				except ValueError:
					print("Invalid Age!\nEnter your age again.\n")

			self.mobile_no = int(input("\nMobile No.:  "))
			while ((isValid(str(self.mobile_no),1))==False):
				self.mobile_no = int(input("\nInvalid mobile no!\nEnter mobile no. again:  "))
			
			self.occupation = input("\nOccupation:  ")
			
			self.email_id = input("\nEmail-id:  ")
			while ((isValid(self.email_id,2))==False):
				self.email_id = input("\nInvalid email id!\nEnter email-id again:  ")
			self.purchased = 0

	def __add__(self,n):
		self.purchased = self.purchased + n

# The default function is overwritten
	def __str__(self):
		if(self.status==1):
			return "%s\t%s %s %s" % (self.id,self.name,Fore.GREEN + str(self.mobile_no),Fore.BLUE + self.email_id)
		else:
			return "\n\nEND OF FILE"

	def showdata(self):
		print("The details of desired customer are as follows: ")
		print("ID = ",self.id)
		print("Name = ",self.name)
		print("Age = ",self.age)
		print("Mobile no. = ",self.mobile_no)
		print("Occupation = ",self.occupation)
		print("Email-id = ",self.email_id)
		print("Purchased = ",self.purchased)

def Create_New_Customer():
	os.system("clear")
	C = Customer(1) 

	with open('customers.txt', 'rb') as file:
		while True:
			try:
				C1 = pickle.load(file)
				if(C1.mobile_no == C.mobile_no):
					print("Customer already exists !")
					break

			except EOFError:
				with open('customers.txt','ab') as file:
					pickle.dump(C,file)
				print("\n\nCreating Customer Record. Please Wait...........")
				time.sleep(3)
				print("\nCustomer Record Created...")
				Send_ID(C.id,C.email_id)
				break

def Display_All_Records():		
	os.system("clear")
	print("CUSTOMER LIST")
	print("\n-----------------------------------------------------------------------------------------------------------------------------------")
	print("-----------------------------------------------------------------------------------------------------------------------------------")
	print("Sr.no\t  ID\t\tName--->Mobile No--->Email")
	print("-----------------------------------------------------------------------------------------------------------------------------------")
	print("-----------------------------------------------------------------------------------------------------------------------------------")
	m = 1
	with open('customers.txt','rb') as file:
		while True:
			try:
				C = pickle.load(file)
				print(m,"\t",C)
				print(Style.RESET_ALL)
				m = m + 1
			except EOFError:
				print("\n\nFile finished.......")
				break

def Display_Record(cust_id):
	os.system("clear")
	C = Customer(0)
	with open('customers.txt','rb') as file:
		while(cust_id != C.id):
			C = pickle.load(file)

	C.showdata()

def Modify_Record(cust_id):
	
	os.system("clear")
	customers = []

	with open('customers.txt','rb') as file:
		while True:
			try:
				customers.append(pickle.load(file))
			except EOFError:
				break

	for i in range(0,len(customers)) :
		if customers[i].id == cust_id :
			break

	C = customers[i]

	print("Choose the parameter to modify:\n\n[1]Name\n\n[2]Mobile number\n\n[3]Email-id")
	p = int(input())
			
	if(p==1):
		C.name = input("Enter the new data:  ")
		
	elif(p==2):
		C.mobile_no = int(input("Enter the new data:  "))
		while ((isValid(str(C.mobile_no),1))==False):
			C.mobile_no = int(input("\nInvalid mobile no!\nEnter mobile no. again:  "))
		
	elif(p==3):
		C.email_id = input("Enter the new data:  ")
		while ((isValid(C.email_id,2))==False):
			C.email_id = input("\nInvalid email id!\nEnter email-id again:  ")
		
	else:
		print("Invalid Option!")
	
	os.system("rm customers.txt")
	os.system("touch customers.txt")

	for customer in customers:
		with open('customers.txt','ab') as file:
			pickle.dump(customer,file)
	
	if p==1 or p==2 or p==3:
		print("\nModifying Customer Record........Please Wait")
		time.sleep(3)
		print("Customer Record Modified")

def Delete_Record(cust_id):
	os.system("clear")
	customers = []

	with open('customers.txt','rb') as file:
		while True:
			try:
				customers.append(pickle.load(file))
			except EOFError:
				break

	for i in range(0,len(customers)) :
		if customers[i].id == cust_id :
			break

	del customers[i]

	os.system("rm customers.txt")
	os.system("touch customers.txt")

	for customer in customers:
		with open('customers.txt','ab') as file:
			pickle.dump(customer,file)

	print("\nDeleting Customer Record........Please Wait")
	time.sleep(3)
	print("Customer Record Deleted")
#------------------------------------------------------/Customer----------------------------------------
def Book_Purchase():
	os.system("clear")
	books = []
	print("Welcome To Book Purchase Portal")
	print("Please Enter Mode of Search")
	n=int(input("[1] By Name\n[2] By Author\t"))

	data = 1
	found = 0
	if(n==1):
		name=str(input("Enter Book Name:  "))
		with open('book.txt','rb') as file:
			try:
				B = pickle.load(file)
				if(name == B.name):
					books.append(B)
				while(name != B.name):
					try:
						B = pickle.load(file)
						books.append(B)
					except EOFError:
						print("The Book \"",name,"\" is not available !")
						break
			except EOFError:
				print("\n\nNO DATA !!!")
				data = 0
	if(n==2):
		auth=str(input("Enter Author Name:  "))
		with open('book.txt','rb') as file:
			try:
				B = pickle.load(file)
				if(auth == B.author):
					books.append(B)
				while(auth == B.author):
					try:
						B = pickle.load(file)
						books.append(B)
					except EOFError:
						print("The Author \"",auth,"\"is not available !")
						break
			except EOFError:
				print("\n\nNO DATA !!!")
				data = 0
	
	if data !=0:
		l = 1

		for book in books:
			print("\n",l,"\b.\n")
			book.showdata()
			print("\n\n")
			l = l + 1

		N = int(input("Enter the serial number of the book to buy:  "))

		B = books[N-1]

		if B.stock >=1 :
			print("\n\nThe total price to be paid: ",B.price,"\n\n")
			pwd = getpass.getpass("Enter the admin password: ")
			v = 3
			while v!=0:
				if pwd == 'iiitn' :
					otp = Send_OTP()
					OTP = input("Enter the otp:  ")
					if(OTP == otp):
						print("Book purchase successful")
						
						books = []

						with open('book.txt','rb') as file:
							while True:
								try:
									books.append(pickle.load(file))
								except EOFError:
									break

						for i in range(0,len(books)) :
							if books[i].id == B.id :
								break

						B = books[i]
						B-1
						os.system("rm book.txt")
						os.system("touch book.txt")

						for book in books:
							with open('book.txt','ab') as file:
								pickle.dump(book,file)

						cid = input("Enter customer id:  ")
						customers = []

						with open('customers.txt','rb') as file:
							while True:
								try:
									customers.append(pickle.load(file))
								except EOFError:
									break

						for i in range(0,len(customers)) :
							if customers[i].id == cid :
								found = 1
								break

						if found==0:
							print("\nCustomer does not exist !\n")
							time.sleep(1)
							Main_Menu()
						
						C = customers[i]
						C+1
						os.system("rm customers.txt")
						os.system("touch customers.txt")

						for customer in customers:
							with open('customers.txt','ab') as file:
								pickle.dump(customer,file)

						break

					else:
						os.system("clear")
						print(Fore.RED + "\n\n\t\tWrong OTP!")
						time.sleep(2)
						print("\n\nThank You For Your Visit To Our Bookshop.\nPlease Do Visit Again\n")
						time.sleep(1)
						exit(0)
						os.system("clear")
						sys.exit()
						end()

				else:
					v = v - 1;
					print("Number of chances left = %d\n" % v)
					pwd = getpass.getpass("Enter the admin password: ")

		else :
			print("Book is out of stock !")
	
	time.sleep(1)
	Main_Menu()


def Book_Donate():
		os.system("clear")
		print("Book Donate Portal")
		print("Thanks To Donate To Our Franchise")
		print("Please Enter Book Details")
		dh1 = 'y'
		while dh1=='y' or dh1=='Y':
			Create_Book()
			print("\nBook donation successful")
			dh1 = 'N'
			dh1 = input("\nDo you want to Donate more book...(y/N)?")
#---------------------------------------------------AdminMenu--------------------------------------------------

def Admin_Menu():
	os.system("clear")
	user = getpass.getuser()
	print("User Name:",user)
	pwd = getpass.getpass("Enter the admin password: ") 
	
	if pwd == 'iiitn': 
		ch0 = 'y'
		while ch0=='y' or ch0=='Y':
			os.system("clear")
			print("\n\n****************************")
			print("     ADMINISTRATOR MENU     ")
			print("****************************\n\n")
			print("\n1. CREATE CUSTOMER RECORD")
			print("\n2. DISPLAY ALL CUSTOMER RECORDS")
			print("\n3. DISPLAY SPECIFIC CUSTOMER RECORD")
			print("\n4. MODIFY CUSTOMER RECORD")
			print("\n5. DELETE CUSTOMER RECORD")
			print("\n6. CREATE BOOK")
			print("\n7. DISPLAY ALL BOOKS")
			print("\n8. DISPLAY SPECIFIC BOOK")
			print("\n9. MODIFY BOOK")
			print("\n10. DELETE BOOK")
			print("\n11. BACK TO MAIN MENU")
			n = int(input("\nPlease Enter Your Choice (1-11)"))

			if n==1:
				ch1 = 'y'
				while ch1=='y' or ch1=='Y':
					Create_New_Customer()
					ch1 = 'N'
					ch1 = input("\nDo you want to add more record...(y/N)?")	

			if n==2:
				Display_All_Records()

			if n==3:
				ch3 = 'y'
				while ch3=='y' or ch3=='Y' :
					print("Enter the ID of the customer:  ",end=" ")
					cust_id = input()
					Display_Record(cust_id)
					ch3 = 'N'
					ch3 = input("\n\nDo you want to print details of another customer...(y/N)?  ")
				
			if n==4:
				ch4 = 'y'
				while ch4=='y' or ch4=='Y':
					print("Enter the ID of the customer:  ",end=" ")
					cust_id = input()
					Modify_Record(cust_id)
					ch4 = 'N'
					ch4 = input("\n\nDo you want modify another customer record...(y/N)? ")

			if n==5:
				ch5 = 'y'
				while ch5=='y' or ch5=='Y':
					cust_id = input("Enter the customer ID:  ")
					Delete_Record(cust_id)
					ch5 = 'N'
					ch5 = input("\n\nDo you want delete another customer record...(y/N)? ")
			
			if n==6:
				bh1 = 'y'
				while bh1=='y' or bh1=='Y':
					Create_Book()
					bh1 = 'N'
					bh1 = input("\nDo you want to add more book...(y/N)?")
				
			if n==7:
				Display_All_Book()
			
			if n==8:
				bh3 = 'y'
				while bh3=='y' or bh3=='Y' :
					print("Enter the ID of the Book:  ",end=" ")
					book_id = input()
					Display_Book(book_id)
					bh3 = 'N'
					bh3 = input("\n\nDo you want to print details of another book...(y/N)?  ")		
			if n==9:
				bh4 = 'y'
				while bh4=='y' or bh4=='Y':
					print("Enter the ID of the Book:  ",end=" ")
					book_id = input()
					Modify_Book(book_id)
					bh4 = 'N'
					bh4 = input("\n\nDo you want modify another book record...(y/N)? ")
			
			if n==10:
				book_id = input("Enter the Book ID:  ")
				bh5 = 'y'
				while bh5=='y' or bh5=='Y':
					Delete_Book(book_id)
					bh5 = 'N'
					bh5 = input("\n\nDo you want delete another book record...(y/N)? ")

			if n==11:
				Main_Menu()

			ch0 = 'N'
			ch0 = input("\n\nDo you want to choose another option from the ADMINISTRATOR MENU....(y/N)?  ")
	else: 
		print("\nINCORRECT PASSWORD!\n")
		time.sleep(1)
	
	Main_Menu()

#---------------------------------------------------MainMenu--------------------------------------------------

def Main_Menu():
	os.system("clear")
	print("                          		---------------------------------------------------------------------------------------------------------------------------")
	print("                          		---------------------------------------------------------------------------------------------------------------------------")
	print("                             		                                            WELCOME TO IIIT NAGPUR BOOKSHOP                                                ")
	print("                          		---------------------------------------------------------------------------------------------------------------------------")
	print("                          		---------------------------------------------------------------------------------------------------------------------------")

	print("\n\n*******************")
	print("     MAIN MENU     ")
	print("*******************\n\n")
	print("\n1. BOOK PURCHASE")
	print("\n2. BOOK DONATE")
	print("\n3. ADMINISTRATOR MENU")
	print("\n4. EXIT")
	n = int(input("\nPlease Select Your Option (1-4)  "))

	if(n==1):
		Book_Purchase()
	
	elif(n==2):
		Book_Donate()

	elif(n==3):
		Admin_Menu()

	else:
		print("\n\nThank You Visitng Our Bookshop.\nPlease Do Visit Again\n")
		time.sleep(1)
		exit(0)

Main_Menu()
