import sys
import argparse
import webbrowser
from spinner import SpinnerThread

# COLORS
ORANGE = '\033[33m'
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
CYAN = '\033[36m'
WHITE = '\033[1;37m'
YELLOW = '\033[93m'

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print(RED, 'Error importing modules.')


class gitscrape(argparse.Action):
    """Action class for username feature"""

    def __call__(self, parser, namespace, values, option_string=None):
        # Spinner
        self.spinner = SpinnerThread()
        self.spinner.start()

        self.user = values
        self.url = requests.get("https://github.com/" + self.user)
        if self.url.status_code != requests.codes.ok:
            print(RED, '\n', "Unable to find username. Please enter"
                       " valid username and try again.")
            self.spinner.stop()
            sys.exit()

        self.full_name = self.location = "No Information Provided"

        self.soup = BeautifulSoup(self.url.text, features="lxml")
        try:
            self.full_name = self.soup.select('.vcard-fullname')[0].get_text()
            self.username = self.soup.select('.vcard-username')[0].get_text()

            self.bio = self.soup.select('.user-profile-bio')[0].get_text()
            if self.bio == "":
                self.bio = "<No bio>"

            self.location = self.soup.select('.p-label')[0].get_text()

        except IndexError:
            pass

        self.repo_list = []
        rep = self.soup.select('a[class="text-bold flex-auto min-width-0"]')
        for i in rep:
            self.repo_list.append(i.get('href').lstrip('/'))

        self.email = self.get_email()

        self.repositories = self.soup.select('.Counter')[0].get_text()
        self.info_links = self.soup.select('span[class="text-bold text-gray-dark"]')
        self.followers = self.info_links[0].get_text().strip()
        self.following = self.info_links[1].get_text().strip()
        self.stars = self.info_links[2].get_text().strip()

        user_id = self.soup.select(
            'form[class="js-site-search-form"]')[0].get('data-scope-id')
        self.avatar_url = str("https://avatars2.githubusercontent"
                              ".com/u/{}?s=400&v=4".format(user_id))

        self.display()

    def get_email(self):
        try:
            repo = self.soup.select('span[class="repo"]')[0].get_text()
            email = get_latest_commit(repo, self.username)
        except IndexError:
            email = "Not enough information."
        return email

    def display(self):
        self.spinner.stop()
        print(GREEN, '\n', "-" * 78, '\n')
        print(BLUE, self.full_name, " ({})".format(self.username))
        print(WHITE, self.bio, '\n')
        print(YELLOW, "Location :: ", self.location)
        print(" Email :: ", self.email, '\n')
        print(CYAN, "Repositories : {} \t Stars : {} \t Followers : {} "
                    "\t Following : {} \n".format(self.repositories,
                                                  self.stars,
                                                  self.followers,
                                                  self.following))
        print(ORANGE, "Pinned/Popular Repositories")
        for rep in self.repo_list:
            print(GREEN, rep)

        if '-a' in sys.argv or '--avatar' in sys.argv:
            webbrowser.open_new(self.avatar_url)

        print(GREEN, '\n', "-" * 78, '\n')


def get_latest_commit(repo_name, username):
    """Function returning email
    (Since you don't have permission to directly
     scrape email from github profile.)"""

    email = ""
    commit_data = requests.get(
        "https://github.com"
        "/{}/{}/commits?author={}".format(
            username,
            repo_name,
            username)).text
    soup = BeautifulSoup(commit_data, "lxml")
    a_tags = soup.findAll("a")
    for a_tag in a_tags:
        URL = a_tag.get("href")
        if URL.startswith("/{}/{}/commit/".format(username, repo_name)):
            label = str(a_tag.get("aria-label"))
            if "Merge" not in label and label != "None":
                patch_data = requests.get("https://github.com{}{}".format(
                    URL, ".patch")).text
                try:
                    start = patch_data.index("<")
                    stop = patch_data.index(">")
                    email = patch_data[start + 1: stop]
                except ValueError:
                    return "Cannot fetch email"
                break
    if (email != "") and (".noreply." not in email):
        return email
    else:
        return "Cannot fetch email"


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(RED, "ENTER A USERNAME!")
        print(BLUE, "Run 'python3 gitscrape.py -h' for help")
        sys.exit()

    parser = argparse.ArgumentParser(description="Get the profile details"
                                                 " of any github user, just"
                                                 " by entering their"
                                                 " username.")

    parser.add_argument('username', type=str,
                        help="Username of the user to fetch details.",
                        action=gitscrape)
    parser.add_argument('-a', '--avatar', action='store_true',
                        help="Display avatar of user.")
    args = parser.parse_args()
