import requests
from Colour import bcolors
import sys
from pathlib import Path
CURRENT_VERSION = 1.0

def write_gray(str):
    print("\033[90m" + str + '\033[0m')

def check_for_update():
    response = requests.get('http://api.github.com/repos/batburger/PseudoCode/releases/latest')
    if response.status_code == 403:
        return {} # We properly just hit the rate limit - no need to alert the user.

    if response.status_code != 200:
        write_gray("No connection to github - can't check for updates.")
        return {}

    response = response.json()
    try:
        version_available = float(response["tag_name"])
    except ValueError:
        write_gray("There was an error processing the server's response.")
        return {}

    if version_available > CURRENT_VERSION:
        write_gray("An update to version " + response["tag_name"] + " is available, run with -u option to auto update!")

    return response

def auto_update(top_level_response):
    if top_level_response == {}:
        raise requests.ConnectionError

    try:
        version_available = float(top_level_response["tag_name"])
    except KeyError:
        print(bcolors.FAIL + "There was an error processing the server's response." + bcolors.ENDC)
        sys.exit(1)
    except ValueError:
        print(bcolors.FAIL + "There was an error processing the server's response." + bcolors.ENDC)
        sys.exit(1)

    if version_available == CURRENT_VERSION:
        print(bcolors.FAIL + "Already on the newest version "+ str(version_available) + " - no need to update." + bcolors.ENDC)
        sys.exit(1)

    print(bcolors.HEADER + "Upgrading to version " + str(version_available) + bcolors.ENDC)

    if "assets_url" not in top_level_response:
        print(bcolors.FAIL + "Github's response is malformed" + bcolors.ENDC)
        sys.exit(1)

    response  = requests.get(top_level_response["assets_url"])
    if response.status_code != 200:
        print(bcolors.FAIL + "Can't get new asset" + bcolors.ENDC)
        sys.exit(1)

    response = response.json()
    if len(response) < 1 or "browser_download_url" not in response[0]:
        print(bcolors.FAIL + "Github's response is malformed" + bcolors.ENDC)
        sys.exit(1)

    print("Downloading new application ... ", end="")

    response = requests.get(response[0]["browser_download_url"])
    if response.status_code != 200:
        print(bcolors.FAIL + "[FAIL]" + bcolors.ENDC)
        sys.exit(1)

    print(bcolors.OKGREEN + "[SUCCESS]" + bcolors.ENDC)

    print("Writing to '~/AInterpreter' ... ", end="")

    home = str(Path.home())
    FILE_PATH = home + '/AInterpreter'

    try:
        f = open(FILE_PATH, 'wb')
    except IOError:
        print(bcolors.FAIL + "[FAIL]" + bcolors.ENDC)
        sys.exit(1)
    with f:
        f.write(response.content)
        f.close()

    print(bcolors.OKGREEN + "[SUCCESS]" + bcolors.ENDC)

    print("")
    print(bcolors.BOLD + "Congratulation you upgraded to version " + str(version_available) + bcolors.ENDC)
    sys.exit(0)
