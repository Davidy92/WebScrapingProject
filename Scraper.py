from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time 


# Initializing WebDriver and Addings incognito (Need to add_extension Adblocker)
option = webdriver.ChromeOptions()
option.add_argument("--incognito")

# create new instance of chrome in incognito mode
browser = webdriver.Chrome(executable_path='C:\Selenium\chromedriver', chrome_options=option)

# go to website
browser.get("http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=California+State+University%2C+Northridge&schoolID=163&queryoption=TEACHER")

timeout = 10
try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mainContent"]/div[1]/div/div[3]/div/div/input')))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()

browser.maximize_window()

#List of majors to cycle from
majorList = ("Accounting", "Accounting & Info Systems","African-American Studies", 
             "Agriculture", "American Indian Studies", "Anthropology", "Architecture", 
             "Art", "Asian American Studies", "Astronomy", "Biology", "Business", 
             "Business Law", "Central American Studies", "Chemistry", "Chicano Studies", 
             "Child Development", "Cinema & Television Arts", "Classics", "Communication", 
             "Communication Disorders", "Computer Information Systems", "Computer Science", 
             "Counseling", "Criminal Justice", "Culinary Arts", "Deaf Studies", "Design", 
             "Economics", "Education", "Engineering", "English", "Environ. & Occupational Health", 
             "Environmental Public Health", "Ethnic Studies", "Extended Studies", "Family & Consumer Science", 
             "Finance", "Fine Arts", "Freshman Seminar", "Geography", "Geology", "Graphic Arts", 
             "Health Science", "Hispanic Studies", "History", "Hospitality", "Humanities", 
             "Information Systems", "International Studies", "Japanese", "Journalism", "Judaic Studies", 
             "Kinesiology", "Languages", "Latin American Studies", "Law", "Linguistics & Language Dev.", 
             "Literature", "Management", "Manufacturing System Engineering & Management", "Manufacturing Technology", 
             "Marketing", "Math Stats & Physics", "Mathematics", "Mechanical Engineering", "Medicine", "Music", 
             "Nursing", "Pan African Studies", "Philosophy", "Physical Education", "Physics", "Physics & Astronomy", 
             "Political Science", "Psychology", "Recreation & Tourism Mgmt", "Religion", "Religious Studies", "Science", 
             "Sign Language", "Social Science", "Social Work", "Sociology", "Spanish", "Theater", "Urban Planning", "Women's Studies", "Writing")

#Selecting drop-down boxes
majorList = browser.find_element_by_xpath('//*[@id="mainContent"]/div[1]/div/div[3]/div/div/input')
majorList.send_keys('Accounting')
majorList.send_keys('\ue007')

#Close advertisement  (Will delete after learning how to add adblocker extension)
exit_button = browser.find_element_by_xpath('//*[@id="cookie_notice"]/a[2]')
WebDriverWait(browser, timeout).until(EC.visibility_of(exit_button))
ActionChains(browser).move_to_element(exit_button).click().perform()

#Click load More button
def load_more(browser):
    time.sleep(1)
    try:
        display = browser.execute_script("return document.getElementsByClassName('progressbtnwrap')[0].style.display")
        if display == 'none':
            return False
        elem = browser.find_element_by_xpath('//div[contains(@class, "progressbtnwrap")]/div[contains(@class, "content")]')
        browser.execute_script("arguments[0].click();", elem)
        return True
    except Exception as e:
        print("Error")
        print(e)
    return False

while load_more(browser):
    print("scrolling further")

#Initialize sleep-time to allow professors to update
time.sleep(1)

#Scrap Professor names, ratings, number of ratings
titles = []
titles_element = browser.find_elements_by_xpath('//*[@id="mainContent"]/div[1]/div/div[5]/ul')
for x in titles_element:
    titles.append(x.text)


#Scrap Professor unique IDS
ids = []
resultSet = browser.find_element_by_xpath('//*[@id="mainContent"]/div[1]/div/div[5]/ul')
ids = resultSet.find_elements_by_tag_name('li')
final = []

#Converting Web elements into strings (Prep for storing into text file)
for id in ids:
    str(final.append(id.get_attribute('id')))

#Storing the professor names, amount of ratings, and rating into an individual element
delimiter = '$'

mylist = ' '.join(titles)
mylist = mylist.replace('\n', '$')

temp1 = mylist.split(delimiter)
print(temp1)

#Sorting all the names, ratings, and amount of ratings into individual lists
pro_rating = []
pro_name = []
pro_amount_rating = []
ids = []

counter = 0
for index in temp1:
    if counter == 1:
        pro_name.append(index)
    if counter == 2:
        pro_amount_rating.append(index)
    if counter == 3:
        pro_rating.append(index)
        counter = 0
    counter += 1

print("All Professor ratings: ", pro_rating)    
print("All professor names: ", pro_name)
print("Amount of times professor rated: ", pro_amount_rating)

# all id's formatted
for i in final:
    ids.append(i[13:])
    
print("Professor ids: ", ids)

#Writting all the information into a text file.
with open('Professor_List.txt', 'w') as filehandle:  
    filehandle.write("Professor IDS: ")
    for listitem in ids:
        filehandle.write('%s, ' % listitem)
    filehandle.write('\n')
    filehandle.write("Professor Names: ")
    for listitem in pro_name:
        filehandle.write('%s, ' % listitem)
    filehandle.write('\n')
    filehandle.write("Professor Ratings: ")
    for listitem in pro_rating:
        filehandle.write('%s, ' % listitem)
    filehandle.write('\n')
    filehandle.write("Professor Amount of Ratings: ")
    for listitem in pro_amount_rating:
        filehandle.write('%s, ' % listitem)
