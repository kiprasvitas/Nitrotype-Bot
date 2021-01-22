from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

driver = webdriver.Chrome("C:\\MEGA\\Python\\Tiktok\\chromedriver.exe") #Replace with your own directory

#Variables
min_speed = 73 #WPM
max_speed = 95 #WPM
number_of_races = 50
missing_chance = 9
password = "password"
username = "username"

#Lower
speed=random.randint(min_speed, max_speed)
print("My speed is: " + str(speed))
cnt = 0
n=number_of_races #number of times to race
sleeptime=60/(speed*16)

def Opening_Browser():
    driver.get('https://www.nitrotype.com/') #URL of the website
    sleep(3) #Depending on your internet speed you can adjust it
    login(password, username)

def getError(min, max, lettervalue):
    rand = random.randint(min, max)
    texterr = ["#", lettervalue, lettervalue, lettervalue, lettervalue, lettervalue, lettervalue, lettervalue, lettervalue, lettervalue, lettervalue]
    error = texterr[rand]
    return error

#Racing

def Race(driver, inputdelay, cnt, n):
    try:
        driver.find_element_by_xpath('//*[text()="Start Qualifying Race"]').click()
    except:
        pass
    try:
        element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.dash-copy')))
    except:
        print("Something went wrong \nQuiting Program")
        Opening_Browser()
    typingtab=driver.find_element_by_css_selector('.dash-copy')

    try:
        driver.find_element_by_css_selector('.dash-copy-input').click() #clicks on the input tab
    except:
        driver.find_element_by_xpath('//*[@id="raceContainer"]/div[1]/div[1]/div/div/div/div[2]/button').click() #click continue connection

    inputtab=driver.find_element_by_css_selector('.dash-copy-input')
    words=typingtab.find_elements_by_css_selector('.dash-word')

    for word in words:
        errorcnt=0
        while True:
            try:
                letterval=word.find_element_by_css_selector('.is-waiting').text
                letter=getError(0, missing_chance, letterval)
                inputtab.send_keys(letter)
                sleep(inputdelay)
                errorcnt=0
            except:
                try:
                    letter=word.find_element_by_css_selector('.is-incorrect').text
                    inputtab.send_keys(letter)
                    sleep(inputdelay)
                except:
                    errorcnt+=1
                    if errorcnt==5:
                        break

    print("Race has successfully ended.")
    cnt += 1
    print("You're on race: " + str(cnt) + "  Out of: " + str(n))
    if (cnt!=n):
        speed=random.randint(min_speed, max_speed)
        sleeptime=60/(speed*16)
        print("My speed is: " + str(speed))
        RaceAgain(driver)
        Race(driver, sleeptime, cnt, n)


def login(password, username):
    driver.find_element_by_xpath('//*[@id="root"]/div/header/div/div[2]/div[3]/div/div[1]/a').click() #button
    sleep(1.24)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="username"]').send_keys(username)
    sleep(0.75)
    driver.find_element_by_xpath('//*[@id="root"]/div/div/main/div/section/div[2]/div/div[3]/form/button').click() #Login button
    sleep(2.25)
    RaceAsGuest(driver)
    Race(driver, sleeptime, cnt, n)

def RaceAsGuest(driver):
    driver.find_element_by_xpath('//*[@id="root"]/div/header/div/div[3]/div[1]/a').click() #Start race button
    sleep(3)


def RaceAgain(driver):
    sleep(3.25)
    try:
        driver.find_element_by_css_selector('.modal-close').click()
    except:
        try:
            driver.find_element_by_xpath('//*[text()="Next"]').click() #clicks next button for reward popup
            sleep(1.75)
            driver.find_element_by_xpath('//*[@id="root"]/div[1]/div[2]/div[3]/div/div[1]/button').click()
            print("Closed Pop-up Banner")
        except:
            print("Didn't close popup.")
            pass
    sleep(random.randint(1, 2))
    driver.find_element_by_xpath('//*[@id="raceContainer"]/div[1]/div[2]/div[3]/div/div[2]/button').click()#clicks on the Race Again button

Opening_Browser()
    

print("The program has successfully ended.")

command = "taskkill /F /IM chromedriver.exe /T"