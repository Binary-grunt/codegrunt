from openai import OpenAI

client = OpenAI()

# TODO: ADD option gpt, like model etc

def write_file_ai(subject: str, eof: str, generated_text: str) -> str:
    file_name = f"{subject}.{eof}"
    with open(file_name, "w") as generated_file:
        generated_file.write(generated_text)
    print(f"File '{file_name}' generated successfully.")


def generated_exercice(subject: str, language_provided: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are an teacher in programming,
                    and computer science""",
            },
            {
                "role": "user",
                "content": f"""Write will create a exercice on the next
                subject {subject} on the language {language_provided}
                and make a exercice simple to create variable in programming,
                just the code without markdown and ``` return pur code
                exercice. Just the instruction inside commentary
                and the prototype code starter,
                like leetcode."""
            }
        ]
    )
    return completion.choices[0].message.content


def analyze_code(file_content: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are an AI code evaluator. You will analyze
                code provided by the user, assess if it meets the requirements
                described, and return either 'Result: True' if the code fully
                meets the requirements, or 'Result: False' if it doesn't.
                Be strict in your evaluation, as if you were running unit tests.
                Do not explain your answer."""
            },
            {
                "role": "user",
                "content": f"""
                The following is a {language} coding exercise. Analyze the provided code to determine if it correctly follows the given instructions.
                The code must:
                1. Strictly follow the provided instructions.
                2. Handle typical and edge cases effectively.
                3. Be syntactically correct and execute as expected.
                4. Implement the required logic accurately.
                5. Return correct results for all input cases, similar to a
                real-world unit test.
                If the code passes these criteria, return 'Result: True'.
                Otherwise, return 'Result: False'.
                Here is the code:

                {file_content}
                Do not explain your reasoning or generate any text beyond
                'Result: True' or 'Result: False'.
                """
            }
        ]
    )
    return completion.choices[0].message.content