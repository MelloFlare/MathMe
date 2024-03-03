import MathMe

# entirety of the pipeline, calls instructorInput once, then pipeline for as many students as instructur inputs
def superPipeline():
    inInput = instructorInput().splitlines()
    if(int(inInput[1]) < 0):
        students = [int(inInput[3])][int(inInput[1])]
        for i in range(0, int(inInput[3])):
            students[i] = pipeline(inInput)
        return students
    else: 
        return

#runs through the pipeline for one student, called in superpipeline using returned value from instructorInput as parameters
def pipeline(inInput):
    
    return

# asks instructor for input, returns multi-line string with the question, wanted number of steps, specific steps wanted, max numer of mistakes per step, and number of students
def instructorInput():
    print("----------------------------------------------------------------------------------------------------")
    print("Instructor Input:")
    question = input("Enter a math problem: ")
    numSteps = input("Enter the number of steps the problem should take, enter 0 to leave it up to chatGPT: ")
    specificSteps = input("List specific steps you want students to take in order in a comma separated list: ")
    maxIncorrect = input("Enter the number of times a student can incorreclty answer a step: ")
    print("----------------------------------------------------------------------------------------------------")
    returnString = question + "\n" + numSteps + "\n" + specificSteps + "\n" + maxIncorrect
    return returnString

#does one loop of student answering and recieving feedback and returns if the student was correct
def inputLoop():
    return