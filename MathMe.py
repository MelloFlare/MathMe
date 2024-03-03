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
    return content


def each_step(array):
    newA = []
    for elemets in array:
        if elemets != '':
            if "Step" in elemets:
                newA.append(elemets)
    return newA


def ask_step(steps):
    all_step = steps
    
    for element in all_step:
        questions = [str(element + " ask a question that lead to this")]
        message = generate_message(questions)
        response = ask_question(message, model)
        print_response(response)