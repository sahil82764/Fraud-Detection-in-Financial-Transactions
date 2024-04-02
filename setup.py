from setuptools import setup
from typing import List

projectName =  "fraudTransaction-predictor"
versionInstance = "0.0.1"
authorName = "UNEMPLOYED TECH BROs"
projectDescription = "/////////"
packageName = ["fraudTransaction"]
requirementFile = "requirements.txt"

def get_requirements()->List[str]:
    """
    Description: This function is going to return the list of requirements mentioned in requirements.txt file.

    Returns: This function is going to return a list which contain name of libraries mentioned in requirements.txt file.
    """
    with open(requirementFile) as requirement_file:
        return requirement_file.readlines()
    


setup(
    name = projectName,
    version = versionInstance,
    author = authorName,
    description = projectDescription,
    packages = packageName,
    install_requires = get_requirements()

)