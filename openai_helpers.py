from openai import OpenAI

client = OpenAI()

# TODO: ADD option gpt, like model etc

contentCharacter = "You are an teacher in programming, and computer science"


def generated_exercice(subject: str, language_provided: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": contentCharacter,
            },
            {
                "role": "user",
                "content": f"Write will create a exercice on the next subject {subject} on the language {language_provided} and make a exercice simple to create variable in programming, just the code without markdown and ``` return pur code exercice. Just the instruction inside commentary and the prototype code starter, like leetcode. "
            }
        ]
    )
    return completion.choices[0].message.content


def analyze_code(file: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": contentCharacter,
            },
            {
                "role": "user",
                "content": f"Analyze the provided files here {file}, it's a exercice like a Leetocde with instruction. The code exercice should fit perfectly to the instruction. You wont explain and generate text, just return Result: True, or Result: False if it's correct or not"
            }
        ]
    )
    return completion.choices[0].message.content
