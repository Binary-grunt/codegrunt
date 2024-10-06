# import sys
from openai import OpenAI


client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write will create a exercice with the provided subject and make a exercice simple to create variable in programming, just the code without markdown and ``` return pur code exercice"
        }
    ]
)

# print(completion.choices[0].message.content)


def create_file(lang: str):
    match lang:
        case "JavaScript":
            x = open("myfile.js", "w")
            x.write(completion.choices[0].message.content)
            x.close()
            print("Javascript files generated.")
        case "PHP":
            open("myfile.php", "w")
            print("PHP files generated.")
        case "Python":
            open("myfile.py", "w")
            print("Python files generated.")
        case _:
            print("Select correct language. Try again")


if __name__ == '__main__':
    print("Please select the language -\n"
          "1. PHP\n"
          "2. JavaScript\n"
          "3. Python\n"
          )
    lang = input("What's the programming language you want to learn? ")
    create_file(lang)
    # print(f"Arguments count: {len(sys.argv)}")
    # for i, arg in enumerate(sys.argv):
    #     print(f"Argument {i:>6}: {arg}")
