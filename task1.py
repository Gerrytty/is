import requests
from bs4 import BeautifulSoup


def parse(search_string, storage, pos):

    if len(storage) >= 100:
        return

    response = requests.get(search_string)
    soup = BeautifulSoup(response.text, 'html.parser')

    for a in soup.find_all('a', href=True):
        link = a['href']

        if link.startswith("https://kpfu.ru") and link not in storage and "de" not in link and "fr" not in link and "en" not in link and "cn" not in link and "es" not in link:
            storage.append(a['href'])
            print("Found the URL:", a['href'])

        if len(storage) >= 100:
            return

    parse(storage[pos], storage, pos + 1)


def clean(text):
    filtered = list(filter(lambda x: x != '', text.split("\n")))

    out = []
    for word in filtered:
        l = list(filter(lambda x: x != '', word.split(" ")))
        if l:
            out.append(" ".join(l))

    return " ".join(out)


def get_text_by_links_arr(storage):
    for i, link in enumerate(storage):
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        text = clean(text)
        print(f"{i}\n")
        with open(f"pages/{i}.txt", "w") as f:
            f.write(text)


def create_index_file(storage):
    with open("index.txt", "w") as f:
        for i, link in enumerate(storage):
            f.write(f"pages/{i} {link}\n")


def main():
    all_links = []
    pos = 0
    parse("https://kpfu.ru", all_links, pos)
    get_text_by_links_arr(all_links)
    create_index_file(all_links)


if __name__ == "__main__":
    main()