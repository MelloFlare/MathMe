from MathMe import *
import webbrowser

global_question_steps = []  #ChatGPT step by step solution in array 
global_total_steps = 0 #lenght of global_question_steps or total steps to solve
global_student_num = 0 #Total number of student
global_question = "" #Teachers Question to ChatGPT
global_steps_correct = [] #Shows which step was correct 

class Node: # This hold the Student name, The loops it took for each step, and next pointer to Student
    def __init__(self, data, name): # constructor for the Node
        self.data = data
        self.name = name
        self.next = None

    def insertAtBegin(self, data, name): #Sets the head
        new_node = Node(data, name)
        if self.head is None:
            self.head = new_node
            return
        else:
            new_node.next = self.head
            self.head = new_node

    def inserAtEnd(self, data, name): #Adds new student to the end 
        new_node = Node(data, name)
        if self.head is None:
            self.head = new_node
            return
 
        current_node = self.head
        while(current_node.next):
            current_node = current_node.next
 
        current_node.next = new_node

    def updateNode(self, val, index): # Allows you to update node with custom data(total loops)
        current_node = self.head
        position = 0
        if position == index:
            current_node.data = val
        else:
            while(current_node != None and position != index):
                position = position+1
                current_node = current_node.next
 
            if current_node != None:
                current_node.data = val
            else:
                print("Index not present")
def create_nodes(num_people): #Create the classroom of Students (Creats Each NODE)    -------THIS doesnt work properly, can you try and fix it----------
    head = None
    print("WOW")
    for _ in range(num_people):
        print("Enter Names of Student One by ONe")
        name = input("Enter one of the Students name: ")        
        data = [1] * global_total_steps  # Assuming data is empty for each student
        if head is None:
            head = Node(data, name)
        else:
            current_node = head
            while current_node.next:
                current_node = current_node.next
            current_node.next = Node(data, name)
    return head

def superPipeline():   # entirety of the pipeline, calls instructorInput once, then pipeline for as many students as instructur inputs
    instructorInput()  #instructorInput is called
    print("this happends")
    head = create_nodes(global_student_num) #Creates Stduent NODES
    print("waht")
    traverse_students(head) #Goes through the Classroom 

def traverse_students(head): #Goes through each student one by one, ask them the question 
    current_node = head
    while current_node is not None:
        print(current_node.name)
        student_question = [str(global_question) + "  Find the Question in this, DONT SOLVE OR DONT GIVE HINTS"] #The Summary of Teachers question to ChatGPT
        messages = generate_message(student_question) 
        response = ask_question(messages, model)
        print(print_response(response)) #Shows the Student what question they need to solve
        print("\n Type your answer(Show all work)")
        full_answer = input("Convert your Work into Txt(and input it here surrounded by parenthese): ") #Student puts the answer here

        testing =  [str(global_question_steps) + " Do the steps in this match up with " + str(full_answer) + r", if a step is correct mark it with True else False if incorrect, write the result in []"]
        messages = generate_message(testing)
        response = ask_question(messages, model)
        global_steps_correct = print_response(response) #top 3 lines Check for which Step the Student got wrong
        pipeline(current_node) # Goes though the Each steps and check how well they did

        current_node = current_node.next #goes the next student and repeats until no Student nodes left


def pipeline(current_node): #runs through the correctness of each step the student did, takes in that Stduents node
    curr = current_node # keep track of the Current Student
    index = 0
    while index < len(global_steps_correct) and global_steps_correct[index]: #Finds the first False in Step_correct
        index += 1

    if index < len(global_steps_correct):   # Check if a False value was found
        inputLoop(index, False, curr) #Sents it to be Fixed
    else:
        print("Good Job!! This is correct") # They got everything correct




def instructorInput(): # asks instructor for input, returns multi-line string with the question, wanted number of steps, specific steps wanted, max numer of mistakes per step, and number of students
    print()
    print("Question Setpup!")
    global_question = input("Enter the question: ")
    global_question = global_question + ", Keep each step in one line, number each step, and DONT ADD spaces between steps "
    print() #Asked the Teach to write a Question 
    messages = generate_message(global_question)
    response = ask_question(messages, model)
    t = print_response(response) #Store the ChatGpt response in t

    x = t.splitlines() #turn steps in t into a array in x
    global_question_steps = each_step(x) #Adds number to the beginning
    global_total_steps = len(global_question_steps) #gets the total steps

    global_student_num = int(input("How many students are answering this question: ")) # how many students are there


#does one loop of student answering and recieving feedback and returns if the student was correct
def inputLoop(index, bol, curr):
    current_node = curr # keep tracks of the current Student
    index = index #Index of what step is worng 
    repeat = bol # Are they Repeating for the thrid time
    current_step = global_question_steps[index] #get the correct step answer from GPT
    print("Looks like you got Step: " + str(index) + " wrong. Use this Hint to help you solve this Step") #Tells the student this step is wrong
    questions_to_ask = [str(current_step) + " ask a question that lead to this"] #Give a Hint as a question
    message = generate_message(questions_to_ask)        
    response = ask_question(message, model)       
    question = print_response(response)
    print(print_response(question)) 
    print()

    if(repeat == True): # THIS IS THE THrid time they are attempting this
        ytLink = [""]
        print("Please watch this Video careful about your topic and after watching")
        while(repeat != False):
            #ADD the video link here  -------------------------------------------PRINT THE LINK_________________________________________________________
            print("\n Type your answer(Show all work)")
            step_answer = input("Convert your Work into Txt(and input it here surrounded by parenthese): ") #gets student new answer

            testing =  [str(current_step) + " Does this step match up with " + str(step_answer) + r", if a step is correct say True or if its incorrect say False"]
            messages = generate_message(testing)
            response = ask_question(messages, model)
            correctness = print_response(response) #Checks and see if its true or false
            if(correctness): #if true They got it correct, updates the loop, and exits 
                print("Congrats!! You got this step correct")
                counter(current_node, index)
                global_steps_correct[index] = True #Turns the false answer to True
                repeat = False
            else: #They got it wrong, goes back to start of while, updates loop(data)
                print("Please, relook at Video")
                counter(current_node, index)
                
        pipeline(current_node) #Goes back and checks again 
        
    else:  #THIS IS THE SECOND attempt
        print("\n Type your answer(Show all work)")
        step_answer = input("Convert your Work into Txt(and input it here surrounded by parenthese): ") #gets the new answer from student for that Step

        testing =  [str(current_step) + " Does this step match up with " + str(step_answer) + r", if a step is correct say True or if its incorrect say False"]
        messages = generate_message(testing)
        response = ask_question(messages, model)
        correctness = print_response(response) #Checks if the answer is True or False
        if(correctness): #If True they Got it correct, updates the loop, and exits
            counter(current_node, index)
            print("Congrats!! You got this step correct")
            global_steps_correct[index] = True
            pipeline(current_node) #goes back and checks agin
        else: # They got it wrong updates the loop, resends the index, turn Result = True, adn current_node
            print("This is incorrect, Please try again")
            counter(current_node, index)
            inputLoop(index, True, current_node)


def counter(curr, index): #Helper function to update the loop for a certin index
    current_node = curr
    current_node.data[index] += 1