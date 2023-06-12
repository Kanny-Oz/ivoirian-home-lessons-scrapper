from requests import get, request
from bs4 import BeautifulSoup
from pathlib import Path

link = "https://lycee-ci.online/course/index.php?categoryid=90"



# Charging after classroom's level
def catching(url):
    r = get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    categorynames = soup.find_all(class_="categoryname")
    matters_link_list = []
    for categoryname in categorynames:
        links_list = str(categoryname).split('"')
        matters_link_list.append(links_list[3])
    i = 0
    while i < len(matters_link_list):
        _matter_catching(matters_link_list[i])
        i += 1


def _matter_catching(url):
    r = get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    coursenames = soup.find_all(class_="coursename")
    lessons_link_list = []
    for coursename in coursenames:
        links_list = str(coursename).split('"')
        lessons_link_list.append(links_list[5])
    i = 0
    while i < len(lessons_link_list):
        _curse_catching(lessons_link_list[i])
        i += 1


def _curse_catching(url):
    r = get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    pdf_link = str(soup.find(class_="autolink")).split('"')[3]
    _resume_catching(pdf_link)


def _resume_catching(url):
    _download(url)


def _download(url):
    url = get(url).url
    print(url)
    file_link_split = str(url).split("/")
    filename = file_link_split[-1].replace("%20", "_")
    (Path.cwd() / "data").mkdir(exist_ok=True)
    filepath = Path.cwd() / "data" / filename
    print(filepath)
    r = get(url)
    with open(filepath, "wb") as f:
        f.write(r.content)


if __name__ == "__main__":
    catching(link)
