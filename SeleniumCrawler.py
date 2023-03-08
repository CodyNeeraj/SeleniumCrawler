import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from dotenv import load_dotenv
import time

# laoding the environment variables from a file .env in the same root path
load_dotenv('./.env')
passwd =  os.environ.get("PASSWD")
usernm = os.environ.get("USERNM")

# Creating  a new directory for further file storage logic inside of it
base_dir = os.getcwd()

def humanLikeTyping(element, text):
   for character in text:
      element.send_keys(character)
      # duration is perfect for simulating actual human intervention on the machine input fields
      time.sleep(0.15)


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


# For providing the user input
username = driver.find_element(By.NAME, 'username_or_email')
passfield = driver.find_element(By.NAME,"password")
humanLikeTyping(username,usernm)
humanLikeTyping(passfield, passwd)
driver.find_element(By.ID,"login-button").click()


driver.get("https://www.mycompiler.io/my-programs")


# Actual code for extracting the data from the webpage

# setting up the limit of results of the page
for page_no in range(0,21):
    # Heading of the file can be given by Heading placeholder
    # Given By X-PATH:   /html/body/div/div[2]/div[1]/div/div[2]/div[0]/div[1]/h2/a
    #   Value needs to be updated over here only  ------------------ ^
    headingXpathValue = "/html/body/div/div[2]/div[1]/div/div[2]/div[{}]/div[1]/h2/a".format(page_no)
    heading = driver.find_element(By.XPATH, headingXpathValue)

    # Code content of  the file can be given by above placeholder
    # Given By X-PATH: /html/body/div/div[2]/div[1]/div/div[2]/div[{}]/div[3]/pre/div[2]/div

    ContentXpathValue  = "/html/body/div/div[2]/div[1]/div/div[2]/div[{}]/div[3]/pre/div[2]/div".format(page_no)
    try:
        content = driver.find_element(By.XPATH,ContentXpathValue)
    except Exception as ex:
        print(ex)
        content = driver.find_element(By.XPATH,"/html/body/div/div[2]/div[1]/div/div[2]/div[{}]/div[2]/pre/div[2]/div")






