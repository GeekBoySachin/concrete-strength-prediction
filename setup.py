from setuptools import find_packages,setup
from typing import List

HYPHEN_E_DOT = "-e ."
REQUIREMENTS_FILE = "requirements.txt"

def get_requirements()->List[str]:
    with open(REQUIREMENTS_FILE) as file:
        requirements_list = file.readlines()
    requirements_list = [package.replace("\n","") for package in requirements_list]
    if HYPHEN_E_DOT in requirements_list:
        requirements_list.remove(HYPHEN_E_DOT)
    return requirements_list


setup(name="Concrete Strength Predictor",
    version="0.0.1",
    author="sachin",
    author_email="sachinv1004@gmail.com",
    install_requires=get_requirements(),
    packages=find_packages(),
    )
