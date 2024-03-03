import subprocess
import sys
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict
from Database.dbConnection import dbConnection


def should_install(requirement):
    flag = False
    try:
        pkg_resources.require(requirement)
    except (DistributionNotFound, VersionConflict):
        flag = True
    return flag

def install_packages(requirement_list):
    try:
        requirements = [
            requirement
            for requirement in requirement_list
            if should_install(requirement)
        ]
        if len(requirements) > 0:
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', *requirements])
            subprocess.run(
                [sys.executable, '-m', 'pip3', 'install', *requirements])
        else:
            print("Requirements already satisfied.")
    except Exception as e:
        print(e)

def start_package_installation():
    requirements = []
    with open('./requirements.txt') as f:
        lines = f.readlines()
        for l in lines:
            if l != '':
                requirements.append(l.strip())
    install_packages(requirements)

# Connect to database
def connect_to_db():
    db = dbConnection()
    connection = db.connect()
    print("Connected to db")
    return connection