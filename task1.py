import os
import requests
from bs4 import BeautifulSoup


def ok_link(link, all_links):
    return link.startswith("https://kpfu.ru") and link not in all_links \
                and "de" not in link and "fr" not in link \
                and "en" not in link and "cn" not in link and "es" not in link \
                and "pdf" not in link and "mp4" not in link and "mov" not in link


def find_links(search_string, all_links, ok_links, pos, max_len=100):

    if len(ok_links) >= max_len:
        return

    response = requests.get(search_string)
    soup = BeautifulSoup(response.text, 'html.parser')

    for a in soup.find_all('a', href=True):
        link = a['href']

        if ok_link(link, all_links):

            all_links.append(link)
            print("Found the URL:", a['href'])
            text_by_link = get_text(link)

            if len(text_by_link) >= 1000:

                print(f"Link {link} have >= 1000 words")

                ok_links.append(link)
                curr_index = len(ok_links) - 1
                save_link(text_by_link, curr_index)
                write_index(link, curr_index)

        if len(ok_links) >= max_len:
            return

    find_links(all_links[pos], all_links, ok_links, pos + 1)


def clean(text):
    filtered = list(filter(lambda x: x != '', text.split("\n")))

    out = []
    for word in filtered:
        import re
        clean_word = re.sub("[^0-9а-яА-Яa-zA-Z \\\]+", " ", word)
        l = list(filter(lambda x: x != '', clean_word.replace("\\", " ").split(" ")))
        if l:
            out.append(" ".join(l))

    return " ".join(out).split(" ")


def get_text(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    text = clean(text)
    return text


def write_index(link, index):
    with open(f"index.txt", "a") as f:
        f.write(f"{index} {link}\n")


def save_link(words, index, dir_to_save="pages"):
    with open(f"{dir_to_save}/{index}.txt", "w") as f:
        f.write(" ".join(words))
    print(f"Saved file {index}")


def main():

    os.remove("index.txt")

    all_links = []
    ok_links = []
    pos = 0
    find_links("https://kpfu.ru", all_links, ok_links, pos)


if __name__ == "__main__":
    main()