print("\n"*10000)

from msvcrt import getch
from getpass import getpass
import os, math, sys, time, random

function = type(lambda: None)


chars = {"letters": ("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
					 "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"),
		 "numbers": ("0","1","2","3","4","5","6","7","8","9"),
		 "symbols": ("`","-","=","[","]","#",";","'",".","/","\\","¬","!",'"',"£","$",
					 "%","^","&","*","(",")","_","+","{","}","~",":","@","<",">","?"),
		 "spacers": (" ")}
		 
meth_path = [None]

answer_messages = ("Incorrect :(", "Correct!")

try:
 	sys.stdout.mode
except:
	print("Please open this program in console.")
	time.sleep(1)
	quit()

	
class Option_Menu:

	def __init__(self, vars, title, *options):
		self.data = [title, *[option for option in options]]
		self.vars = vars


	def __getitem__(self, item):
		return self.__dict__[item];


	def __setitem__(self, item, value):
		self.__dict__[item] = value


	def display(self):
		global meth_path
		position = 0
		length = 0
		for i in range(len(self.data)):
			if len(self.data[i][0].format(**self.vars)) > length:
				length = len(self.data[i][0].format(**self.vars))
		boundary = round(length / 2)

		while True:
			
			for i in range(len(self.data)):
				
				display = self.data[i][0].format(**self.vars)
				
				spacing = boundary - math.floor(len(display)/2)

				if position + 1 == i:
					print(" -> " +
						  " "*spacing + display +
						  " "*spacing + (" ","")[len(display) % 2] +
						  " <- ")
				else:
					print(" "*(spacing+4) + display)
					if i == 0:
						print(" "*(spacing+4) + "-"*len(display))

			print("\n" + self.data[position+1][0] +
				  "\n" + "-"*len(self.data[position+1][0]) +
				  "\n" + self.data[position+1][2].format(**self.vars))
		
			key_input = ord(getch())
			clear_console()
			
			if key_input in (72,119):
				
				if position > 0:
					position -= 1
				else:
					position = len(self.data)-2
					
			elif key_input in (80,115):
				
				if position < len(self.data)-2:
					position += 1
				else:
					position = 0
					
			elif key_input in (13,32):
				
				destination_str = self.data[position+1][1][0]
				if destination_str:
				
					destination = globals()[destination_str]
				
					if isinstance(destination, Input_Menu):
						clear_console()
						var,locations = destination.display(self.data[position+1][1][1])
						print("variable:", var, "location:", locations)
						for location in locations:
							self.vars[location] = var
						clear_console()
						
					elif isinstance(destination, Option_Menu):
						clear_console()
						locations = self.data[position+1][1][1]
						if locations:
							for location in locations:
								var = self.vars[location]
								destination.vars[location] = var
						if self != quiz_results:
							meth_path.append(self)
						destination.display()
						
					elif isinstance(destination, Info_Menu):
						clear_console()
						meth_path.append(self)
						destination.display()
						
						
					elif isinstance(destination, function):
						locations = self.data[position+1][1][1]
						parameters = dict()
						if locations:
							if destination in (go_back,set_var):
								parameters = locations
							else:
								for location in locations:
									parameters[location] = self.vars[location]
						if destination != go_back:
							meth_path.append(self)
						destination(parameters)
						break;
					
			'''
			^ = 72
			w = 119
			v = 80
			s = 115
			< = 13
			  = 32
			'''



class Input_Menu:
	
	def __init__(self, prompt, data_type=str, item_type=None, list_split=" ", data_range=None, charray=None, len_range=None, hidden=False):
		parameters = {"data_type":  data_type,
					  "item_type":  item_type,
					  "list split": list_split,
					  "data_range": data_range,
					  "charray":    charray,
					  "len_range":  len_range,
					  "hidden":     hidden}
		self.data = [prompt, parameters]


	def __getitem__(self, item):
		return self.__dict__[item];


	def __setitem__(self, item, value):
		self.__dict__[item] = value


	def display(self, return_var):
		if not self.data[1]["hidden"]:
			data = input(str(self.data[0]) + " ")
		else:
			data = getpass(str(self.data[0]) + " (will not be echoed to console) ")

		try:
			if self.data[1]["data_type"] in (list,tuple):
				data = self.data[1]["data_type"]([self.data[2]["item_type"](x) for x in data.split(self.data[1]["list_split"])])
			else:
				data = self.data[1]["data_type"](data)

			valid_specs = True
			
			if self.data[1]["data_type"] == int and self.data[1]["data_range"] != None:
				if data < list(self.data[1]["data_range"])[0] or data > list(self.data[2]["data_range"])[-1]:
					valid_specs = False
				
			if self.data[1]["data_type"] in (list,str) and self.data[1]["charray"] != None:
				if False in [char in self.data[1]["charray"] for char in data]:
					valid_specs = False
				
			if self.data[1]["data_type"] in (list,str) and self.data[1]["len_range"] != None:
				if len(data) < list(self.data[1]["len_range"])[0] or len(data) > list(self.data[1]["len_range"])[-1]:
					valid_specs = False

			if valid_specs:
				return data, return_var;
			if not valid_specs:
				print("Please do it right. (Please fit with specifications)")
				time.sleep(3)
				return "Not yet set", return_var;
		
		except:
			print("Please do it right. (Incorrect data type)")
			time.sleep(3)
			return "Not yet set", return_var;



class Info_Menu:

	def __init__(self, title, info, key=13):
		self.data = [title,info,key]


	def __getitem__(self, item):
		return self.__dict__[item];


	def __setitem__(self, item, value):
		self.__dict__[item] = value


	def display(self):
		print(self.data[0], "\n" + "-"*len(self.data[0]), "\n" + self.data[1])
		print("Press getch key", self.data[2], "to continue...")
		key = None
		while key != self.data[2]:
			key = ord(getch())
		
		
		go_back(1)
		


def test_program():
	clear_console()
	test_option_1.display()

def start_program():
	clear_console()
	main.display()



def run_quiz(vars):
	global meth_path
	questions = read_from_file(0)[vars["topic"]][vars["difficulty"]]
	question_order = list(range(len(questions)))
	random.shuffle(question_order)
	
	for question_number,question in enumerate(question_order[:5]):
		answer_random = [(i,answer) for i,answer in enumerate(questions[question][1:])]
		random.shuffle(answer_random)
									
		question_menu = Option_Menu({"question_number": question_number+1},
									("Question {question_number}: " + questions[question][0], None, None),
									*[(str(i+1)+": " + answer_random[i][1],("set_var", [None, "q"+str(question_number+1), 
									answer_messages[answer_random[i][0]==0], "quiz_results"]), "") for i in range(4)])
									
		question_menu.display()
	meth_path = meth_path[:-2]
	quiz_results.vars["topic"],quiz_results.vars["difficulty"] = vars["topic"],vars["difficulty"]
	quiz_results.vars["total"] = sum([1 for n in range(5) if quiz_results.vars["q"+str(n+1)] == globals()["answer_messages"][1]])
	quiz_results.display()

def set_var(details):
	globals()[details[3]].vars[details[1]] = details[2]
	if details[0]:
		globals()[details[0]].display()



def confirm_user(user_info):
	users = read_from_file(1)
	if any([user_info["username"] == user[0][0][0] and user_info["password"] == user[0][1][0] for user in users]):
		print("Correct username and password! Logging in...")
		time.sleep(2)
		clear_console()
		user_main.vars["user"] = user_info["username"]
		user_main.display()
	else:
		print("Incorrect username-password combination, please try again...")
		time.sleep(2)
		clear_console()
		go_back(1)

def new_user(user_info):
	users = read_from_file(1)
	
	if any([user_info["username"] in (user[0][0][0],"Not yet set") for user in users]):
		print("Username is taken or not set.")
		time.sleep(2)
		clear_console()
		go_back(1)
	else:
		print("Creating your account...!")
		time.sleep(2)
		clear_console()
		append_to_file([[[user_info["username"]],[user_info["password"]]],[""]])
		user_main.vars["user"] = user_info["username"]
		user_main.display()



def view_scores(user_info):
	database = read_from_file(1)
	username = user_main.vars["user"]
	user = [user for user in database if user[0][0][0] == username][0]
	scores = Info_Menu("Your Scores:", "\n".join(["Topic: {} Difficulty: {}\nScore: {}/5\n".format(("Maths","Spelling")[int(test[1])],
																								   ("Easy","Medium","Hard")[int(test[2])],
																								   test[0]) for test in user[1]]))
	scores.display()


def new_score(user_info):
	database = read_from_file(1)
	username = user_main.vars["user"]
	user = [(user,i) for i,user in enumerate(database) if user[0][0][0] == username][0]
	
	if user[0][1][0][0] == "":
		user[0][1][0] = [str(user_info["total"]),str(user_info["topic"]),str(user_info["difficulty"])]
	else:
		user[0][1].append([str(user_info["total"]),str(user_info["topic"]),str(user_info["difficulty"])])
		
	database[user[1]] = user[0]
	write_to_file(database)



def read_from_file(file):
	input_str,output_list = open("database.txt", "r").read().split("#\n")[file],list()
	
	if file == 0:
		split_sequence = ("\n\n", "\n", " ~~~ ", "|")
	elif file == 1:
		split_sequence = ("\n", " ~~~ ", "|", ",")
	
	for i,a in enumerate(input_str.split(split_sequence[0])):
		output_list.append(list())
		
		for j,b in enumerate(a.split(split_sequence[1])):
			output_list[i].append(list())
			
			for k,c in enumerate(b.split(split_sequence[2])):
				output_list[i][j].append(list())
								
				for d in c.split(split_sequence[3]):
					output_list[i][j][k].append(d)
	
	return output_list

def append_to_file(user):

	for j,section in enumerate(user):
		for k,test in enumerate(user[j]):
			user[j][k] = ",".join(user[j][k])
		user[j] = "|".join(user[j])
	user = " ~~~ ".join(user)
	
	open("database.txt", "a").write("\n"+user)
	
def write_to_file(users):

	for i,user in enumerate(users):
		for j,section in enumerate(users[i]):
			for k,test in enumerate(users[i][j]):
				users[i][j][k] = ",".join(users[i][j][k])
			users[i][j] = "|".join(users[i][j])
		users[i] = " ~~~ ".join(users[i])
	users = "\n".join(users)
	
	questions = open("database.txt", "r").read().split("#\n")[0]
	open("database.txt", "w").write(questions+"#\n"+users)



def go_back(location):
	global meth_path

	if len(meth_path) == 1: #empty path
		exit_program(location)
	elif type(location) == int:
		destination = meth_path[-1 * location]
		meth_path = meth_path[:-1 * location]
	elif type(location) == type(Option_Menu):
		i = meth_path.index(location)
		destination = meth_path[i]
	
	clear_console()
	
	destination.display()

def clear_console():
	print("\n"*100)
	
def test():
	print("test")

def exit_program(redundancy):
	quit()



get_username   = Input_Menu("Please enter your username:", data_type=str, len_range=range(4,16), charray=(*chars["letters"],*chars["numbers"]))
get_password   = Input_Menu("Please enter your password:", data_type=str, len_range=range(8,32), charray=(*chars["letters"],*chars["numbers"],*chars["symbols"]), hidden=True)
get_sort_order = Input_Menu("Please enter a sort priority:", data_type=list, item_type=str, len_range=5)

basic_info = Info_Menu("Info:", 
					   "Quizzimodo is a wondrous quizzing app for you and your buddies to make learning fun! You can compare scores and meme with your friends! Create an account to get started!", 
					   key=32)

main      = Option_Menu({},
					    ("Welcome to Quizzimodo!", None, None),
					    ("Log in", ("login", None), "Already have an account? Just log in to get quizzing now!"),
					    ("Sign up", ("signup", None), "Don't have an account? Create one here!"),
					    ("Info", ("basic_info", None), "Information on what Quizzimodo is and how to use it."),
					    ("Quit", ("exit_program", None), "Quit the application and come back another time."))

login     = Option_Menu({"username": "Not yet set","password": "Not yet set"},
					    ("Log in to your account and you can quiz!", None, None),
					    ("Username", ("get_username", ["username"]), "Current username = {username}"),
					    ("Password", ("get_password", ["password"]), "Current password = {password}"),
					    ("Confirm", ("confirm_user", ["username", "password"]), "Ready to log in?"),
					    ("Back", ("go_back", 1), "Return to the main menu."))

signup    = Option_Menu({"username": "Not yet set","password": "Not yet set"},
					    ("Create an account and you can quiz!", None, None),
					    ("Username", ("get_username", ["username"]), "Current username = {username}"),
					    ("Password", ("get_password", ["password"]), "Current password = {password}"),
					    ("Confirm", ("new_user", ["username", "password"]), "Are you sure you want this username and password? You wont be able to change them later!"),
					    ("Back", ("go_back", 1), "Return to the main menu."))

user_main = Option_Menu({"user": "none"},
					    ("Welcome {user}!", None, None),
					    ("Take a quiz", ("quiz_topic", None), "Try out your quizzing skills with our wide range of quizzes and quiz things!! 0w0"),
					    ("View your results", ("view_scores", ["user"]), "Manage your past successes and see your high scores!"),
					    ("Log out", ("main", None), "Had enough quizzing for today? That's okay! Come back any time! ;)"))

quiz_topic      = Option_Menu({"topic": "maths"},
							  ("What topic do you want?", None, None),
							  ("Maths", ("set_var", ["quiz_difficulty", "topic", 0, "quiz_ready"]), "Questions on mathematics!"),
							  ("Spelling", ("set_var", ["quiz_difficulty", "topic", 1, "quiz_ready"]), "Questions on spelling!"),
							  ("Go back...", ("go_back", 1), "Go back to the difficulty choice."))

quiz_difficulty = Option_Menu({"difficulty": "0"},
							  ("What difficulty do you want?", None, None),
							  ("Easy", ("set_var", ["quiz_ready", "difficulty", 0, "quiz_ready"]), "2 answer choices per question!"),
							  ("Medium", ("set_var", ["quiz_ready", "difficulty", 1, "quiz_ready"]), "3 answer choices per question!"),
							  ("Hard", ("set_var", ["quiz_ready", "difficulty", 2, "quiz_ready"]), "4 answer choices per question!"),
							  ("Go back...", ("go_back", 1), "Go back to the difficulty choice."))

quiz_ready      = Option_Menu({},
							  ("Are you ready to begin the quiz?", None, None),
							  ("Lets go!", ("run_quiz", ["topic", "difficulty"]), "Begin the quiz!"),
							  ("Nope...", ("go_back", 1), "Go back to the difficulty choice."))

quiz_results    = Option_Menu({"q1": None, "q2": None, "q3": None, "q4": None, "q5": None, "total": None},
							  ("Your results!", None, None),
							  ("Go back to the menu.", ("new_score", ["total", "topic", "difficulty"]), 
							  "You got:\nQuestion 1: {q1}\nQuestion 2: {q2}\nQuestion 3: {q3}\nQuestion 4: {q4}\nQuestion 5: {q5}\nTotal score: {total}/5\nPress enter to go back!"))


start_program()

#==========================================================================================================================================================================================================

test_info = Info_Menu("Info Test", "This is the information test menu", key=13)

test_input_1 = Input_Menu("input_prompt_1")
test_input_2 = Input_Menu("input_prompt_2")

test_option_5 = Option_Menu({},
							("This is the fourth test menu, hi!", None, None),
							("quit_again", ("exit_program", None), "quits2"),
							("back_again", ("go_back", 1), "goes back down path"))

test_option_4 = Option_Menu({},
							("This is the fourth test menu, hi!", None, None),
							("option_1_goto", ("test_option_1", None), "option_1_info"),
							("quit_again", ("exit_program", None), "quits2"),
							("back_again", ("go_back", 1), "goes back down path"))

test_option_3 = Option_Menu({},
							("This is the third test menu, hi!", None, None),
							("info_goto", ("test_info", None), "displays some info"),
							("quit_function", ("exit_program", None), "quits1"),
							("back_function", ("go_back", 1), "goes back down path"))

test_option_2 = Option_Menu({},
							("This is the second test menu, hi!", None, None),
							("option_3_goto", ("test_option_3", None), "option_3_info {inputted_var}"),
							("option_4_goto", ("test_option_4", None), "option_4_info"),
							("input_2_goto", ("test_input_2", None), "input_2_info"),
							("back_function", ("go_back", 1), "goes back down path"))

test_option_1 = Option_Menu({"inputted_var": "default"},
							("This is the first test menu, hi!", None, None),
							("option_2_goto", ("test_option_2", ["inputted_var"]), "option_2_info"),
							("input_1_goto", ("test_input_1", ["inputted_var"]), "input_1_info {inputted_var}"),
							("quit_function", ("exit_program", None), "quit_info"),
							("back_function", ("go_back", 1), "goes back down path"))

							
test_program()
