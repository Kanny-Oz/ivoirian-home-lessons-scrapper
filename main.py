import inspect
from requests import get
from bs4 import BeautifulSoup
from pathlib import Path

# High School
h_school_path = (Path.cwd() / "data" / "lycee")
h_school_path.mkdir(exist_ok=True, parents=True)
second = "https://lycee-ci.online/course/index.php?categoryid=2"
first = "https://lycee-ci.online/course/index.php?categoryid=5"
last = "https://lycee-ci.online/course/index.php?categoryid=8"
h_school = [h_school_path, second, first, last]
# College
college_path = (Path.cwd() / "data" / "college")
college_path.mkdir(exist_ok=True, parents=True)
sixth = "https://college-ci.online/course/index.php?categoryid=29"
fifth = "https://college-ci.online/course/index.php?categoryid=28"
fourth = "https://college-ci.online/course/index.php?categoryid=4"
third = "https://college-ci.online/course/index.php?categoryid=3"
college = [college_path, sixth, fifth, fourth, third]


def _matter_dir_create(soup, school_type):
    categorynames = soup.find_all(class_="categoryname")
    titles = soup.find_all(class_="nocourse")
    categorynames_text = [categoryname.text for categoryname in categorynames]
    dico = {}
    dir_path = ""
    for categoryname in categorynames:
        for categoryname_text in categorynames_text:
            if categoryname.text == categoryname_text:
                split = str(categoryname).split('"')[3]
                dico.update({split: categoryname_text})
                if school_type is h_school_path:
                    dir_path = f"{school_type / dico[split]}"
# dir_path.mkdir(exist_ok=True, parents=True)
                elif school_type is college_path:
                    dir_path = f"{school_type / str(titles).split()[4] / dico[split]}"
# dir_path.mkdir(exist_ok=True, parents=True)
                else:
                    print("?")
    return dir_path


def catching(url, school_type):
    r = get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    dir_path = _matter_dir_create(soup, school_type)
    _matter_catching(url)
    return dir_path


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


def _download(url, dir_path):
    url = get(url).url
    print(url)
    file_link_split = str(url).split("/")
    filename = file_link_split[-1].replace("%20", "_")
    (Path.cwd() / dir_path).mkdir(exist_ok=True, parents=True)
    filepath = _matter_dir_create / filename
    print(filepath)
    r = get(url)
    with open(filepath, "wb") as f:
        f.write(r.content)


def get_variable_name(var):
    frame = inspect.currentframe()
    variables = frame.f_back.f_locals.items()
    for name, value in variables:
        if value is var:
            return name
    return None


if __name__ == "__main__":
    for link in college[1:]:
        catching(link, college[0])

    for link in h_school[1:]:
        catching(link, h_school[0])
