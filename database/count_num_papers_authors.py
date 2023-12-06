import json

num_papers_authors = {}
tot = 2370685


def count_author(data: dict) -> None:
    """
    Count the number of papers of each author
    :param data: metadata of the paper
    :return: None
    """
    authors_parsed = data['authors_parsed']
    authors = [' '.join(author[::-1]).strip() for author in authors_parsed]
    for author in authors:
        author = fetch_name(author)
        if author in num_papers_authors:
            num_papers_authors[author] += 1
        else:
            num_papers_authors[author] = 1


def fetch_name(author: str) -> str:
    """
    Remove the institute name and "and" string from the author's name
    :param author: author's name with institute name
    :return: author's name
    """
    author = author.split('  ')[-1]
    if len(author) > 4 and author[:4] == 'and ':
        author = author[4:]
    if author[0].islower():
        author = author[0].upper() + author[1:]
    return author


def save_json(data: dict) -> None:
    """
    Save the result to json file
    :param data: dict
    :return: None
    """
    with open('num_papers_authors.json', 'w') as f:
        json.dump(data, f, indent=4)
    print("Successfully save the result to json file")


if __name__ == '__main__':
    with open('arxiv.json') as f:
        for index, line in enumerate(f):
            data = json.loads(line)
            count_author(data)
            print(f'[{index+1}/{tot}] have been counted.')
    save_json(num_papers_authors)