from operator import truediv
import openai

openai.api_key = "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"

conv = "Marv is a chatbot that reluctantly answers questions with sarcastic responses:\n\nYou: "
while True:
    a = input("You:")
    conv+="You: "+a+"\n"
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=conv+"\nMarv:",
        temperature=0.5,
        max_tokens=60,
        top_p=0.3,
        frequency_penalty=0.5,
        presence_penalty=0.0
    )
    conv+="Marv: "+response.choices[0].text+"\n"
    print(response.choices[0].text)