"""
Program Name: Ivorian-curses scrapper
Author: https://www.github.com/LuckyKanny
Description: This is a python program for scrap the ivorian home-school website in searching and downloading curses in.
Copyright: © 2023 @oskhane. All rights reserved.

This program is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
You should have received a copy of the license along with this program.
If not, see <https://creativecommons.org/licenses/by-nc-nd/4.0/>.
"""

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


def catching(url, school_type):
    r1 = get(url)
    soup = BeautifulSoup(r1.content, "html.parser")

    categorynames = soup.find_all(class_="categoryname")
    titles = soup.find_all(class_="nocourse")
    categorynames_text = [categoryname.text for categoryname in categorynames]
    dico = {}
    dir_path = ""
    split = ""
    for categoryname in categorynames:
        for categoryname_text in categorynames_text:
            if categoryname.text == categoryname_text:
                split = str(categoryname).split('"')[3]
                dico.update({split: categoryname_text})
                if school_type is h_school_path:
                    dir_path = f"{school_type / dico[split]}"
                    Path(dir_path).mkdir(exist_ok=True, parents=True)
                elif school_type is college_path:
                    dir_path = f"{school_type / str(titles).split()[4] / dico[split]}"
                    Path(dir_path).mkdir(exist_ok=True, parents=True)
                else:
                    print("?")

    # catching(url)
    r2 = get(split)
    print(f"Catching {split}")
    soup = BeautifulSoup(r2.content, "html.parser")
    coursenames = soup.find_all(class_="coursename")
    link_curse = {}
    for coursename in coursenames:
        links_list = str(coursename).split('"')
        print(links_list)
        link_curse.update({links_list[5]: str(links_list[6]).split(">")[1].split("<")[0]})
    print(f"before append {link_curse}")
    i = 0
        # _curse_catching(url)
    for unit in link_curse:
        print(unit)
        r3 = get(unit)
        print(f"_curse_catching {r3.url}")
        soup = BeautifulSoup(r3.content, "html.parser")
        pdf_link = str(soup.find(class_="autolink")).split('"')[3]

        # download
        url = get(pdf_link).url
        print(f"download {pdf_link}")
        print(dir_path)
        file_link_split = str(url).split("/")
        filename = file_link_split[-1].replace("%20", "_")
        (Path.cwd() / dir_path).mkdir(exist_ok=True, parents=True)
        filepath = Path(dir_path) / filename
        print(filepath)
        r = get(pdf_link)
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


"""
@todo: The multi-page system
"""