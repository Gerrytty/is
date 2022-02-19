import os
import re
import pymorphy2


def convert_file_to_array_of_words(path_to_file):
    with open(path_to_file) as file:
        return (" ".join(file.readlines())).split(" ")


def clean(arr):

    clean_words = []

    for word in arr:
        clean_word = re.sub("[^0-9а-яА-Яa-zA-Z]+", "", word).lower()
        if clean_word != "":
            clean_words.append(clean_word)

    return clean_words


def write_to_file(filename, arr):
    with open(f"normal_form_docs/{filename}", "w") as file:
        file.write(" ".join(arr))


def main():

    files = os.listdir("pages")

    for file in files:
        list_of_words = convert_file_to_array_of_words(f"pages/{file}")
        list_of_words = clean(list_of_words)
        normal_form = to_normal_form(list_of_words)
        write_to_file(file, normal_form)


def to_normal_form(arr):
    morph = pymorphy2.MorphAnalyzer(lang='ru')

    normal_form = []

    for word in arr:
        p = morph.parse(word)[0]
        word_in_normal_form = p.normal_form
        normal_form.append(word_in_normal_form)

    return normal_form


if __name__ == "__main__":
    main()