import requests
from bs4 import BeautifulSoup
from google import genai
from google.genai import types


def indian():
    url = "https://indian-tv.cz/recenze"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    # latest review
    review: BeautifulSoup = soup.find("h1", "articlebox__heading")
    game_name = review.find("a").get_text(strip=True)
    href = review.find("a").get("href")

    # check if is same as last
    with open("href.txt", "r") as file:
        if file.read().strip() == href:
            print("Stejná recenze jako naposled!")
            with open("review.txt", "r") as rev_file:
                print(rev_file.read())
            return

    with open("href.txt", "w") as file:
        file.write(href)

    # working with review
    r = requests.get(href, headers=headers)
    soup:BeautifulSoup = BeautifulSoup(r.text,'html.parser')
    text = soup.find("section", "article-body").get_text()


    # AI summary

    client = genai.Client(api_key='--')
    task = "Shrň mi to to nejdůležitější do pár vět a na konci mi dej cca bodové hodnocení, které si vyvodil z recenze. Toto je ta recenze:"

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents={'text': task + text},
        config={
            'temperature': 0,
            'top_p': 0.95,
            'top_k': 20,
        },
    )

    client.close()

    with open("review.txt", "w") as file:
        file.write(game_name + "\n" + response.text)
    print(game_name)
    print(response.text)
    print("Více na:" + href)



if __name__ == "__main__":
    indian()