from setuptools import setup,find_packages
from typing import List

PROJECT_NAME='Housing-Predictor'
VERSION='0.0.1'
AUTHOR='Tamil Selvan'
DESCRIPTION='This is a Housing Machine Learning Project'

REQUIREMENT_FILE_NAME='requirements.txt'

HYPHEN_E_DOT='-e .'


def get_requirements_list() -> List[str]:
    '''
    Description: This Function will return the name of libraries present in the 
    "requirements.txt" file as a list.
    '''
    with open(file=REQUIREMENT_FILE_NAME, mode='r') as requirement_file:
        requirement_list = requirement_file.readlines()
        requirement_list = [requirement_name.replace('\n', '') for requirement_name in requirement_list]
        if HYPHEN_E_DOT in requirement_list:
            requirement_list.remove(HYPHEN_E_DOT)
    return requirement_list






setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    packages=find_packages(), # A list of folder name which has __init__.py file.
    install_requires=get_requirements_list()

)