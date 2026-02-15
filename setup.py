from setuptools import find_packages, setup


hypen_e_dot = "-e ."
def get_requirements(file_path)-> list:
    """this function will return the list of requirements"""
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        if hypen_e_dot in requirements:
            requirements.remove(hypen_e_dot)
    return requirements




setup(
    name="mlproject"
    ,version="0.1",
    author="mohamed",
    packahges=find_packages(),
    install_requires=get_requirements("requirements.txt")
    


)