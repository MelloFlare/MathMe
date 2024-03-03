from openai import OpenAI
import secrets_1

client = OpenAI(api_key=secrets_1.api_key)
model = "gpt-4"


def ask_question(messages, model):

    """
    Function That Asks GPT 4 A Question
    """

    # set up the question here
    # ask gpt-3.5 the question
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    # return the answer
    return response


def generate_message(questions):
    messages = []
    for question in questions:
        message = {
            "role":"user",
            "content":question
        }

        messages.append(message)

    return messages

def print_response(response):
    content = response.choices[0].message.content
    print(content)
    return content


def each_step(array):
    oldA = array
    newA = []
    for elemets in oldA:
        if( elemets != ' ' and elemets[1] == "." or elemets[2] == '.'):
            newA.append(elemets)

    return newA


def ask_step(steps):
    all_step = steps
    
    for element in all_step:
        questions = [str(element + " ask a question that lead to this")]
        message = generate_message(questions)
        response = ask_question(message, model)
        print_response(response)


#Setup = ["Use Step by Step format to answer future questions]
questions = ["Say hi", """Solve the integral of 1/sin(x), and give me in steps, first substitute x = 2u , 
             dx = 2du, then sin(2u) = 2sinucosu, then use the identity of 1 = sin(x)^2+cos(x)^2, , so that the integral become (sin(u)^2 + cos(u)^2 )/ sinu cosu, then reduced into two integrals, sinu/cosu and cosu/sinu, then let m = sinu , dm = cosu, and n = cosu , dn = -sinu, , the two integrals become 1/m and 1/n. then solve the integral to ln(m) - ln(n) +c , then use the identity of ln(m) - ln(n) = ln(m/n) +c. Then recall m = sinu, n = cosu, the equation become ln(sinu/cosu)+c which is lm(tanu)+c. Then recall x = 2u, so the final solution is ln(tan(x/2))+c Stay only on this approach, Keep each step in one line and number each step"""]
#questions = ["what is (1 + 1)* 2 - 3 show each step"]
messages = generate_message(questions)
response = ask_question(messages, model)
t = print_response(response)

#questions = ["what math knowledge should the solver now for each step at that level?"]
#message2 = generate_message(questions)
#response2 = ask_question(message2, model)
#print_response(response2)

x = t.splitlines()
print(x)
y = each_step(x)
test = "test"
print(y)

ask_step(y)