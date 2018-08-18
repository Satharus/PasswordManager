#Importing the needed libraries
import gspread #Used to access google sheets
from oauth2client.service_account import ServiceAccountCredentials #Used to authenticate
																#the user to google sheets
import os #Used for some Linux specific terminal commands such as "clear"
######

#Initialising authentication and account information
scope = ['https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('PasswordManagerAuth.json', scope)
client = gspread.authorize(creds)
######

#Opening the sheet and creating a PrettyPrinter variable
sheet = client.open("PasswordManagerProject").sheet1
gInsert = 0 #Global variable used to count the number of actions
			#done in the runtime
gServices = ["Service", "Dummy"] #Global variable used to store the services
masterPassword = sheet.cell(1,4).value
masterPasswordHint = sheet.cell(1,5).value
######
print("The master password is: ", end='')
print(masterPassword)
#Fuction definitions
def initialiseServices():
	#Adds all the services to the gServices array
	global gServices
	gServices = ["Service", "Dummy"]
	i = len(gServices)
	while sheet.cell(i,1).value!='': #It should only break when it reaches
									#the end of the list, i.e. empty cell
		gServices.append(sheet.cell(i,1).value)
		i = i + 1

def listServices():
	#Lists all of the services to the user
	global gServices
	print("Services available:")
	i = 2
	while sheet.cell(i,1).value!='':
		print(i - 1, end='-')
		print(gServices[i])
		i = i + 1

def checkService(s):
	#Checks if the service exists before accessing the spreadsheet, to prevent
	#value or runtime errors.
	global gServices
	try:
		if gServices.index(s) < len(gServices) and gServices.index(s) > 0:
			return 1
	except ValueError:
			return 0

def editData(row, col):
	data = input()
	sheet.update_cell(row, col, data)

def insertNewEntry():
	#Inserts a new service, username, and password to the user
	global gInsert
	while 1:
		x = 0
		while x < 3:
			tempPassword = input("Master Password: ") #Input the password
			if tempPassword == masterPassword:
				service = input("Service name: ")
				service = service.lower()
				service = service.lstrip()
				service = service.rstrip()
				if checkService(service) == 0: #Checks if the sevice exists or not
					username = input("Username: ")
					password = input("Password: ")
					row = [service,username,password]
					nAccount = sheet.row_count +  gInsert
					sheet.insert_row(row,nAccount)
					sheet.resize(nAccount + 1, 5) #Resizes the google sheet to make sure
												#that it is always in the correct size
					gInsert = gInsert + 1 #Adds one to the insertion to make sure that the
										#sheet doesn't delete any of the current services
					break
				else: #If the service exists, it prompts the user more options
					print("Service already exists! Please choose one of the following options:")
					print("1-List all saved services")
					print("2-Enter another service")
					print("3-Modify the service")
					print("0-Exit")
					choice = int(input(">"))
					if choice == 1: #Listing all services
						os.system("clear")
						listServices()
					elif choice == 2: #Entering another service, continues the while loop
						os.system("clear")
						continue
					elif choice == 3: #Overwriting the service's values
						temp = sheet.find(service)
						print("What would you like to change? ")
						print("1.Username", end='\t')
						print("2.Password", end='\t')
						print("3.Both")
						choice = int(input(">"))
						if choice == 1:
							print("Current Username: ", end='')
							print(sheet.cell(temp.row, temp.col+1).value)
							print("Enter a new username: ", end='')
							editData(temp.row, temp.col+1)
							break
						elif choice == 2:
							print("Enter a new password: ", end='')
							editData(temp.row, temp.col+2)
							break
						elif choice == 3:
							print("Current Username: ", end='')
							print(sheet.cell(temp.row, temp.col+1).value)
							print("Enter a new username: ", end='')
							editData(temp.row, temp.col+1)
							print("Enter a new password: ", end='')
							editData(temp.row, temp.col+2)
							break
					elif choice == 0:
						break
					else:
						print("Invalid input!")
						os.system("sleep 1")
						os.system("clear")
						break
			else:
				print("Wrong password!")
				if x < 2:
					print("Hint: ", end='')
					print(masterPasswordHint)
				x = x + 1
		break

def deleteEntry():
	while 1:
		service = input("Service name: ")
		service = service.lower()
		service = service.lstrip()
		service = service.rstrip()
		if checkService(service) == 1:
			temp = sheet.find(service)
			x = 0
			while x < 3:
				tempPassword = input("Master Password: ")
				if tempPassword == masterPassword:
					sheet.delete_row(temp.row)
					nAccount = sheet.row_count
					break
				else:
					print("Wrong password!")
					if x < 2:
						print("Hint: ", end='')
						print(masterPasswordHint)
					x = x + 1
		else:
			print("Service not found! Please choose one of the following options:")
			print("1-List all available services")
			print("2-Re-enter the service name")
			print("0-Exit")
			choice = int(input(">"))
			if choice == 1:
				os.system("clear")
				listServices()
			elif choice == 2:
				os.system("clear")
				continue
			elif choice == 0:
				break
			else:
				print("Invalid input!")
				os.system("sleep 1")
				os.system("clear")
				break
		break

def getInfo():
	while 1:
		service = input("Service name: ")
		service = service.lower()
		service = service.lstrip()
		service = service.rstrip()
		if checkService(service) == 1:
			temp = sheet.find(service)
			x = 0
			while x < 3:
				tempPassword = input("Master Password: ")
				if tempPassword == masterPassword:
					print("Service: ", end='')
					print(sheet.cell(temp.row, temp.col).value)
					print("Username: ", end='')
					print(sheet.cell(temp.row, temp.col+1).value)
					print("Password: ", end='')
					print(sheet.cell(temp.row, temp.col+2).value)
					break
				else:
					print("Wrong password!")
					if x < 2:
						print("Hint: ", end='')
						print(masterPasswordHint)
					x = x + 1
		else:
			print("Service not found! Please choose one of the following options:")
			print("1-List all available services")
			print("2-Re-enter the service name")
			print("0-Exit")
			choice = int(input(">"))
			if choice == 1:
				os.system("clear")
				listServices()
			elif choice == 2:
				os.system("clear")
				continue
			elif choice == 0:
				break;
			else:
				print("Invalid input!")
				os.system("sleep 1")
				os.system("clear")
				break
		break

def changeEntry():
	while 1:
		service = input("Service name: ")
		service = service.lower()
		service = service.lstrip()
		service = service.rstrip()
		if checkService(service) == 1:
			temp = sheet.find(service)
			print("What would you like to change? ")
			print("1.Username", end='\t')
			print("2.Password", end='\t')
			print("3.Both")
			choice = int(input(">"))
			if choice == 1:
				x = 0
				while x < 3:
					print("Current Username: ", end='')
					print(sheet.cell(temp.row, temp.col+1).value)
					tempPassword = input("Master Password: ")
					if tempPassword == masterPassword:
						print("Enter a new username: ", end='')
						editData(temp.row, temp.col+1)
						break
					else:
						print("Wrong password!")
						if x < 2:
							print("Hint: ", end='')
							print(masterPasswordHint)
						x = x + 1
			elif choice == 2:
				x = 0
				while x < 3:
					tempPassword = input("Master Password: ")
					if tempPassword == masterPassword:
						print("Enter a new password: ", end='')
						editData(temp.row, temp.col+2)
						break
					else:
						print("Wrong password!")
						if x < 2:
							print("Hint: ", end='')
							print(masterPasswordHint)
						x = x + 1
			elif choice == 3:
				x = 0
				while x < 3:
					print("Current Username: ", end='')
					print(sheet.cell(temp.row, temp.col+1).value)
					tempPassword = input("Master Password: ")
					if tempPassword == masterPassword:
						print("Enter a new username: ", end='')
						editData(temp.row, temp.col+1)
						print("Enter a new password: ", end='')
						editData(temp.row, temp.col+2)
						break
					else:
						print("Wrong password!")
						if x < 2:
							print("Hint: ", end='')
							print(masterPasswordHint)
						x = x + 1
			break
		else:
			print("Service not found! Please choose one of the following options:")
			print("1-List all available services")
			print("2-Re-enter the service name")
			print("0-Exit")
			choice = int(input(">"))
			if choice == 1:
				os.system("clear")
				listServices()
			elif choice == 2:
				os.system("clear")
				continue
			elif choice == 0:
				break
			else:
				print("Invalid input!")
				os.system("sleep 1")
				os.system("clear")
				break

def main():
	print("\t\t\t  Welcome to Password Manager")
	print("What would you like to do?")
	print("1.View an account's entry")
	print("2.Enter a new account/service")
	print("3.Modify an account's data")
	print("4.Delete an account's entry")
	print("0.Exit")
	choice = int(input(">"))
	if choice == 0:
		exit()
	elif choice == 1:
		os.system("clear")
		print("\t\t\t  Viewing an account's entry")
		getInfo()
	elif choice == 2:
		os.system("clear")
		print("\t\t\t  Entering an account/service")
		insertNewEntry()
	elif choice == 3:
		os.system("clear")
		print("\t\t\t  Modifying an account's data")
		changeEntry()
	elif choice == 4:
		os.system("clear")
		print("\t\t\t  Deleting an account's entry")
		deleteEntry()
######

#Main Program
initialiseServices()
while 1:
	main()
	target = input("Continue using the program(y/n): ")
	if target == 'y':
		print("Going back to main menu")
		initialiseServices()
		os.system("clear")
	else:
		exit()
######
