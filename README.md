# gitscrape

## About
This CLI application gets the profile details of any github user, just by entering their username.
A tool for everyone to use on the go, saving you some precious time.

Built using Python's web scraping BeautifulSoup module, it basically shows you the entire profile overview of the user.<br>
What all it fetches:
<ul>
  <li> Full name
  <li> Bio
  <li> Location
  <li> Email
  <li> Number of:
    <ul>
      <li> Repositories
      <li> Stars
      <li> Followers
      <li> Following
    </ul>
  <li> Pinned/Popular repositories
  <li> Avatar (optional)
</ul>

## Setup
**Make sure you have python3 installed on your system. If not, download python3 from [here](https://www.python.org/).**
 1. Clone this repository by `git clone https://github.com/akshgpt7/gitscrape`.
 2. Change directory by `cd gitscrape`.
 3. Install the dependencies by `pip install -r requirements.txt`.
 4. You're good to go! (See usage)
 
## Usage
 1. Change working directory by `cd gitscrape/src`.
 2. To see all features and help, run `python3 gitscrape.py -h`.
 3. To get a user's details, `python3 gitscrape.py <username>`.
 
## Gallery
![output screenshot](https://raw.githubusercontent.com/akshgpt7/gitscrape/master/screenshots/output.png)
 
## Contributing
Any new features, improvements, additions, suggestions or issues are welcome! <br>
Make sure you comply with PEP-8 guidelines for any contribution.
    
    
    
