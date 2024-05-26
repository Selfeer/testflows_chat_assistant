import os
import subprocess
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openai import OpenAI

from testflows.core import *
from tests.correct_answers import *


@TestStep(Given)
def retrieve_an_answer(self, key, questions_answers):
    """Retrieve an answer using the question_retriever.py script."""

    process = subprocess.Popen(
        ["python3", "../question_retriever.py", "--key", key],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    with By("sending a question to the question_retriever script"):
        process.stdin.write(questions_answers[0] + "\n")
        process.stdin.flush()
        process.stdin.close()

    with And("retrieving the answer"):
        output = ""
        for line in process.stdout:
            if line.strip() == "Ask a question:":
                break
            output += line

        process.wait()

    return output


@TestStep(When)
def compare_answers(self, key, expected, actual):
    """Compare the correct and actual answers provided by the test program."""

    with By("Initializing the OpenAI client"):
        client = OpenAI(api_key=key)

    with And("sending the API request to OpenAI to compare the answers"):
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "I will provide you with two sets of text - I need you to determine weather these two sets of text are similar to each other or not. Only respond with the word 'Similar' if they are similar and 'Not Similar' if they are not.",
                },
                {
                    "role": "user",
                    "content": f"""1. {expected} \n 2. {actual}""",
                },
            ],
        )

    return completion.choices[0].message.content


@TestOutline
def validate_answer(self, key, question_answer):
    """Validate the answer to a question."""
    with Given("I ask a question and retrieve an answer"):
        actual_answer = retrieve_an_answer(
            key=key,
            questions_answers=question_answer,
        )
    with When("I compare the actual and expected answers"):
        result = compare_answers(
            key=key,
            expected=question_answer[1],
            actual=actual_answer,
        )
    with Then("I check that the answer is consistent"):
        assert (
            result == "Similar"
        ), f"The answer is not consistent. \n Expected: \n {question_answer[1]} \n but got: \n {actual_answer}."


@TestScenario
def question_1(self, key):
    """Validate the answer to the question 'What is the TestFlows?'."""
    validate_answer(key=key, question_answer=question_and_answer[0])


@TestScenario
def question_2(self, key):
    """Validate the answer to the question 'How do I run the TestFlows tests in parallel?'."""
    validate_answer(key=key, question_answer=question_and_answer[1])


@TestFeature
@Name("answer consistency")
def feature(self):
    key = Secret("key")(os.environ["OPENAI_API_KEY"])

    for scenario in loads(current_module(), Scenario):
        Scenario(test=scenario)(key=key.value)


feature()
