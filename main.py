"""
Program Name: Ivorian-curses scrapper
Author: https://www.github.com/LuckyKanny
Description: This is a python program for scrap the ivorian home-school website in searching and downloading curses in.
Copyright: © 2023 @oskhane. All rights reserved.

This program is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
You should have received a copy of the license along with this program.
If not, see <https://creativecommons.org/licenses/by-nc-nd/4.0/>.
"""

from time import time
from requests import get
from bs4 import BeautifulSoup
from pathlib import Path

# High School
h_school_path = Path.cwd() / "data" / "lycee"
h_school_path.mkdir(exist_ok=True, parents=True)
second = "https://lycee-ci.online/course/index.php?categoryid=2"
first = "https://lycee-ci.online/course/index.php?categoryid=5"
last = "https://lycee-ci.online/course/index.php?categoryid=8"
h_school = [h_school_path, second, first, last]
# College
college_path = Path.cwd() / "data" / "college"
college_path.mkdir(exist_ok=True, parents=True)
sixth = "https://college-ci.online/course/index.php?categoryid=29"
fifth = "https://college-ci.online/course/index.php?categoryid=28"
fourth = "https://college-ci.online/course/index.php?categoryid=4"
third = "https://college-ci.online/course/index.php?categoryid=3"
college = [college_path, sixth, fifth, fourth, third]


def subjects_catching(url, subject_path):
    """Subjects searching and listing

    :param url: The url of class level to catch available subjects.
    :param subject_path: The subject directory path to next downloading.
    :return: A dictionary in this template : {subject_url: [Subject_name, subject_path]}.

    """
    r = get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    subject_path = (subject_path / soup.find_all(class_="nocourse")[0].text.split()[0])
    subject_path.mkdir(parents=True, exist_ok=True)
    print(subject_path)
    categorynames = soup.find_all(class_="categoryname")
    return {
        str(categoryname)
        .split('"')[3]: [str(categoryname)
        .split('"')[-1]
        .split(">")[1]
        .split("<")[0], subject_path / str(categoryname)
        .split('"')[-1]
        .split(">")[1]
        .split("<")[0]]
        for categoryname in categorynames
    }


def curses_catching(url, subject_path):
    """Curses searching and listing

    :param url: Subject's url to catch.
    :param subject_path: The subject directory path to next downloading.
    :return: If "coursename" is not empty, returns a dictionary in this template : {curse_url: curse_title}. \
            Else, do a subjects_catching() alternative and returns a dictionary in this template \
            {sub_subject_title: {subject_url: [Subject_name, subject_path]}}.

    """
    Path(subject_path).mkdir(parents=True, exist_ok=True)
    print(subject_path)
    r = get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    coursenames=soup.find_all(class_="coursename")
    if len(coursenames) != 0:
        return {
            str(coursename)
            .split('"')[5]: str(coursename)
            .split('"')[-1]
            .split(">")[1]
            .split("<")[0]
            for coursename in coursenames
        }
    sub_subjects = soup.find_all(class_="categoryname")
    sub_subjects_list = {
        str(sub_subject)
        .split('"')[3]: str(sub_subject)
        .split('"')[4]
        .split(">")[1]
        .split("<")[0]
        for sub_subject in sub_subjects
    }
    return {
        sub_subjects_list[sub_subject]:
        curses_catching(sub_subject, f"{subject_path}{sub_subjects_list.get(sub_subject)}")
        for sub_subject in sub_subjects_list
    }


def link_click(url, file_path):
    """File downloading

    :param url: Final curse url where we click.
    :param file_path: File path where we save the downloaded file.
    :return: None.

    """
    print(file_path)
    r = get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    final = soup.find(class_="autolink")
    download(str(final).split('"')[3], file_path)


def download(url, file_path):
    r = get(url)
    with open(file_path, "wb") as f:
        f.write(r.content)


def main(url, subject_path):
    subjects = subjects_catching(url, subject_path)
    for subject in subjects:
        curses = curses_catching(subject, str(subjects.get(subject)[1]))
        if curses is not None:
            for c in curses:
                link_click(c, Path(subjects[subject][1]) / f"{curses[c]}.pdf")


def high_school():
    pass


if __name__ == "__main__":
    start = time()
    for link in college[1:]:
        main(link, college[0])
        print("\n")

    end = time()
    print(f"Time elapsed : {end - start} seconds")
