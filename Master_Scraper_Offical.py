from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time 


#Adding adblocker
option = webdriver.ChromeOptions()
option.add_extension(r"C:\Users\David\Documents\Extensions\uBlock-Origin_v1.16.18.crx")


# create new instance of chrome in incognito mode
browser = webdriver.Chrome(executable_path='C:\Selenium\chromedriver', chrome_options=option)

# go to website of interest
browser.get("http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=California+State+University%2C+Northridge&schoolID=163&queryoption=TEACHER")

timeout = 10
try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mainContent"]/div[1]/div/div[3]/div/div/input')))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()

browser.maximize_window()

#Close advertisement
exit_button = browser.find_element_by_xpath('//*[@id="cookie_notice"]/a[2]')
WebDriverWait(browser, timeout).until(EC.visibility_of(exit_button))
ActionChains(browser).move_to_element(exit_button).click().perform()

#List of majors
major_List = ("Accounting", "Accounting ","African-American Studies", 
             "Agriculture", "American Indian Studies", "Anthropology", "Architecture", 
             "Art", "Asian American Studies", "Astronomy", "Biology", "Business", 
             "Business Law", "Central American Studies", "Chemistry", "Chicano Studies", 
             "Child Development", "Cinema ", "Classics", "Communication", 
             "Communication Disorders", "Computer Information Systems", "Computer Science", 
             "Counseling", "Criminal Justice", "Culinary Arts", "Deaf Studies", "Design", 
             "Economics", "Education", "Engineering", "English", "Environ. ", 
             "Environmental Public Health", "Ethnic Studies", "Extended Studies", "Family ", 
             "Finance", "Fine Arts", "Freshman Seminar", "Geography", "Geology", "Graphic Arts", 
             "Health Science", "Hispanic Studies", "History", "Hospitality", "Humanities", 
             "Information Systems", "International Studies", "Japanese", "Journalism", "Judaic Studies", 
             "Kinesiology", "Languages", "Latin American Studies", "Law", "Linguistics ", 
             "Literature", "Management", "Manufacturing System Engineering ", "Manufacturing Technology", 
             "Marketing", "Math Stats ", "Mathematics", "Mechanical Engineering", "Medicine", "Music", 
             "Nursing", "Pan African Studies", "Philosophy", "Physical Education", "Physics", "Physics ", 
             "Political Science", "Psychology", "Recreation ", "Religion", "Religious Studies", "Science", 
             "Sign Language", "Social Science", "Social Work", "Sociology", "Spanish", "Theater", "Urban Planning", "Women's Studies", "Writing")

#Initializing File
masterFile = open("Master_Database.txt", 'w+')
masterFile.write("{}\t{}\t\t{}\t{}".format("Professor IDS", "Professor Names", "Professor Ratings", "Number of Ratings\n"))
masterFile.write("{}\t{}\t\t{}\t{}".format("-------------", "---------------", "-----------------", "-----------------\n"))


#Selecting drop-down boxes
for major in major_List:
    majorList = browser.find_element_by_xpath('//*[@id="mainContent"]/div[1]/div/div[3]/div/div/input')
    majorList.send_keys(major)
    time.sleep(1)
    majorList.send_keys('\ue007')
        
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
    
    # get professor name + rating
    titles = []
    titles_element = browser.find_elements_by_xpath('//*[@id="mainContent"]/div[1]/div/div[5]/ul')
    for x in titles_element:
        titles.append(x.text)
    
    
    #Professor ID storing
    ids = []
    resultSet = browser.find_element_by_xpath('//*[@id="mainContent"]/div[1]/div/div[5]/ul')
    ids = resultSet.find_elements_by_tag_name('li')
    final = []
    
    #Converting Web element into strings
    for id in ids:
        str(final.append(id.get_attribute('id')))
    
    #Storing the professor names, amount of ratings, and rating into an individual element
    delimiter = '$'
    mylist = ' '.join(titles)
    mylist = mylist.replace('\n', '$')
    temp1 = mylist.split(delimiter)
    
    #Sorting all the names, ratings, and amount of ratings into individual lists
    pro_rating = []
    pro_name = []
    pro_amount_rating = []
    ids = []
    
    counter = 0
    for i, index in enumerate(temp1):
        if counter % 3 == 1:
            pro_name.append(index)
        if counter % 3 == 2:
            pro_amount_rating.append(index)
        if counter % 3 == 0:
            pro_rating.append(index)
        counter += 1
    
    # all id's formatted
    for i in final:
        ids.append(i[13:])

    counter = 0
    #Writting all the information into a text file.
    
    masterFile.write("Major: (" + major + ")\n")
    for items in ids:
        masterFile.write("{}\t\t{}\t\t\t\t\t{}\t\t\t{}".format(items,pro_name[counter],pro_rating[counter],pro_amount_rating[counter]) + "\n")
        counter += 1
    
    #Clear search box
    exit_search = browser.find_element_by_xpath('//*[@id="mainContent"]/div[1]/div/div[3]/div/div/span/span[2]')
    WebDriverWait(browser, timeout).until(EC.visibility_of(exit_search))
    ActionChains(browser).move_to_element(exit_search).click().perform()
        
masterFile.close()
