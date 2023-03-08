import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from dotenv import load_dotenv
import time

# laoding the environment variables from a file .env in the same root path
load_dotenv('./.env')
passwd = os.environ.get("PASSWD")
usernm = os.environ.get("USERNM")

fullPath = ""

fetchedData = dict()
def onStartDirMaker(codeExtractionDir):
    # Creating a new directory for further file storage logic inside of it
    print("Currently in: ", os.getcwd(), " Directory.")
    global fullpath
    fullpath = os.path.join(os.getcwd(), codeExtractionDir)
    if os.path.exists(fullpath):
        print(f"Directory ./{codeExtractionDir} already exists : Skipped")
        return fullpath
    else:
        try:
            os.mkdir(codeExtractionDir)
            print(f"Directory ./{codeExtractionDir} creation: Success")
        except Exception as e:
            print(f"Error Occured while creating DIR {codeExtractionDir} : Failed")
        return fullpath


def humanLikeTyping(element, text):
    for character in text:
        element.send_keys(character)
        # duration is perfect for simulating actual human intervention on the machine input fields
        time.sleep(0.01)


def fileCreationWizard(heading, content):
    print("Inside the file creation wizard fucntion")
    print(fullPath)
    filename = f"{heading.text}.py"
    actualDestinationPath = os.path.join(fullPath,filename)
    with open(actualDestinationPath, 'w') as file:
        for sloc in content.text:
            file.write(sloc)


# for instantiating the browser driver api with required neccesities
# kindly replace the below exceutable path with the latest geckodriver from the https://github.com/mozilla/geckodriver/releases/
service = Service(r"./geckodriver.exe")
options = webdriver.FirefoxOptions()
options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
driver = webdriver.Firefox(service=service, options=options)

# For visiting/opening the page using the above code
driver.get("https://www.mycompiler.io/")
element = driver.find_element(By.LINK_TEXT, 'Login')
element.click()


# Main function for extracting the data from the webpage
def dataExtractor(startOnValue, EndOnvalue):
    # setting up the limit of results of the page
    for page_no in range(startOnValue, EndOnvalue):
        # Heading of the file can be given by Heading placeholder
        # Given By X-PATH:   /html/body/div/div[2]/div[1]/div/div[2]/div[0]/div[1]/h2/a
        #   Value needs to be updated over here only  ------------------ ^
        headingXpathValue = "/html/body/div/div[2]/div[1]/div/div[2]/div[{}]/div[1]/h2/a".format(str(page_no))
        heading = driver.find_element(By.XPATH, headingXpathValue)
        print(heading.text)
        heading.click()
        content = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[3]/div[1]/pre/div[2]/div")
        print(content.text)

        driver.implicitly_wait(2)

        # Returing back the previous page
        driver.back()
        fileCreationWizard(heading, content)
        print()


# For providing the user input
username = driver.find_element(By.NAME, 'username_or_email')
passfield = driver.find_element(By.NAME, "password")
humanLikeTyping(username, usernm)
humanLikeTyping(passfield, passwd)
driver.find_element(By.ID, "login-button").click()

# Going to myprograms page link
driver.get("https://www.mycompiler.io/my-programs")

startCount = 1
endcount = 21
codeExtractionDir = "CodeFromSeleniumCrawler"

# call to run the main logic as arguments startDivtagnumber, endDivTagnumber per page
fullPath = onStartDirMaker(codeExtractionDir)
dataExtractor(startCount, endcount)

driver.find_element(By.XPATH, "/html/body/div/div[2]/div[2]/div/nav/a[2]").click()
dataExtractor(startCount, endcount)
driver.quit()
