from operator import truediv
import openai

openai.api_key = "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"
nom = "Marc"
conv = nom+" est chat.\n"
while True:
    try:
        a = input("Vous:")
    except:
        print("------------------------------------------")
        print(conv)
        break
    conv+="Vous: "+a+"\n"
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=conv+nom+": ",
        temperature=0.5,
        max_tokens=200,
        top_p=0.3,
        frequency_penalty=0.5,
        presence_penalty=0.0
    )
    conv+=nom+": "+response.choices[0].text+"\n"
    #print(response.choices[0])
    print(response.choices[0].text)