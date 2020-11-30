import re, string
import shelve
import sys, os
from gensim.parsing.preprocessing import remove_stopwords, preprocess_string, strip_punctuation


def parse_file(file_path, db):
    """
    :param file_path:
    :param db:
    :return:
    """
    with open(file_path) as file:
        for line in file:
            abs_id, abstract = parse_line(line)
            db[abs_id] = abstract
    return db


def parse_line(line):
    """

    :param line:
    :return:
    """
    # get id and abstract through regex
    match = re.search(r"^(\d+)\s(.*)", line)
    abs_id = match.group(1)
    abstract = match.group(2)
    abstract = preprocess_abs(abstract)
    return abs_id, abstract


def preprocess_abs(abstract: str):
    """

    :param abstract:
    :return:
    """
    # remove quotation if it exists
    abstract = abstract.rstrip('"')
    abstract = abstract.lstrip('"')

    # remove stopword
    abstract = remove_stopwords(abstract)

    # fast way to strip punctuation
    abstract = abstract.translate(str.maketrans('', '', string.punctuation))
    return abstract


def main():
    args = sys.argv[:]
    if not args:
        raise SystemExit("No file to clean provided.")

    elif not os.path.isfile(args[1]):
        raise SystemExit(f"Not a file: {args[1]}. Please provide a file to preprocess.")
    else:
        with shelve.open("adb") as adb:
            db = parse_file(args[1], adb)
            for r in db:
                print(f"{r} {db[r]}")


if __name__ == "__main__":
    main()
