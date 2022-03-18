import os
import pymorphy2

l = ["AND", "OR", "NOT"]


def to_normal_form(arr):
    morph = pymorphy2.MorphAnalyzer(lang='ru')

    normal_form = []

    for i, word in enumerate(arr):
        if word not in l:
            p = morph.parse(word)[0]
            word_in_normal_form = p.normal_form
            normal_form.append(word_in_normal_form)
        else:
            normal_form.append(word)

    return normal_form


def create_index(path_to_files):
    files = [f"{i}.txt" for i in range(100)]

    word_map_to_document = dict()

    for i, filename in enumerate(files):
        with open(f"{path_to_files}/{filename}", "r") as file:
            words = file.readline().split()
            for word in words:
                if word not in word_map_to_document:
                    word_map_to_document[word] = {i}
                else:
                    word_map_to_document.get(word).add(i)

    return word_map_to_document


def func_by_token(token, set_to_operate, set_to_insert):
    if token == "NOT":
        set_to_operate.difference_update(set_to_insert)

    if token == "AND":
        set_to_operate.intersection_update(set_to_insert)

    if token == "OR":
        set_to_operate.update(set_to_insert)

    return set_to_operate


def parse(list_of_tokens, dict_of_words):

    list_of_tokens = to_normal_form(list_of_tokens)

    print(list_of_tokens)

    if list_of_tokens[0] != "NOT":
        set_of_all_docs = set(dict_of_words[list_of_tokens[0]])
        i = 1
    else:
        set_of_all_docs = set(range(0, 100))
        set_of_all_docs.difference_update(dict_of_words[list_of_tokens[1]])
        i = 2

    while i < len(list_of_tokens) - 1:

        token = list_of_tokens[i]
        next_token = list_of_tokens[i + 1]
        print(f"{i} {token} {next_token}")

        if next_token != "NOT":
            func_by_token(token, set_of_all_docs, dict_of_words[next_token])
            i += 2

        else:
            set_of_docs_without_next_token = set(range(0, 100)).difference(dict_of_words[list_of_tokens[i + 2]])
            func_by_token(token, set_of_all_docs, set_of_docs_without_next_token)
            i += 3

    return set_of_all_docs


def main():
    dict_of_words = create_index("normal_form_docs")
    print(dict_of_words)
    search1 = "научный AND библиотека AND NOT медик"
    set1 = parse(search1.split(" "), dict_of_words)

    print(set1)


def simple_demo(search):
    dict_of_words = {"день": [0, 1, 2, 3],
                     "ночь": [1, 2, 4, 5],
                     "солнце": [2, 3, 4],
                     "море": [4]}

    list_of_tokens = "NOT день AND ночь AND солнце".split(" ")
    list_of_tokens = search.split(" ")

    s = parse(list_of_tokens, dict_of_words)

    print(s)


if __name__ == "__main__":
    print(create_index("normal_form_docs"))