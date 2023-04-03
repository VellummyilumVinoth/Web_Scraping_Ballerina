import requests
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from bs4 import BeautifulSoup
import csv
from github import Github

# Set up GitHub credentials
ACCESS_TOKEN = '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'
g = Github(ACCESS_TOKEN)

# Set up repository information
REPO_OWNER = 'VellummyilumVinoth'
REPO_NAME = 'Ballerina_Examples_By_Web_Scrapping'

url = 'https://ballerina.io/learn/by-example'
url1 = 'https://ballerina.io'
# Retrieve the HTML content of the URL
response = requests.get(url, verify=False)
html_content = response.content

# Parse the HTML content and extract all the <a> tags
soup = BeautifulSoup(html_content, 'html.parser')
a_tags = soup.find_all('a')

# Iterate through each <a> tag and extract the code from the linked page
for a_tag in a_tags:
    href = a_tag.get('href')
    if href is not None:
        # Construct the absolute URL of the linked page
        if not href.startswith('http'):
            href = url1 + href
            #print(href)
        # Retrieve the HTML content of the linked page
        response = requests.get(href,verify=False)
        # Extract the code from the JavaScript variable
        pattern = r'"codes":\["(.*?)"\]'
        match = re.search(pattern, response.text)
        if match:
            code = match.group(1)
            code_lines = code.split('\\n')
    
            code = ''.join(code_lines)
            pattern = re.compile(r'<.*?>')
            code = pattern.sub('', code)
            code = bytes(code, "utf-8").decode("unicode_escape")
    
            soup = BeautifulSoup(code, 'html.parser')

            code_elements = soup.find_all('span', {'class': 'line'})

            extracted_codes = ''.join([element.get_text() for element in code_elements])
   
            # Save the codes to a file
            filename = f"{href.split('/')[-1]}.bal"
            with open(filename, 'w') as f:
               f.write(extracted_codes)
            print(f"The codes have been saved to {filename}")
            
            # Push the file to GitHub
            repo = g.get_user(REPO_OWNER).get_repo(REPO_NAME)
            with open(filename, 'r') as f:
                content = f.read()
            repo.create_file(filename, f"Add {filename}", content)
            print(f"{filename} has been pushed to {REPO_OWNER}/{REPO_NAME}")
            
        else:
            print('Code not found')
