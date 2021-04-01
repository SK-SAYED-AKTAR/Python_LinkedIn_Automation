from selenium import webdriver
import time
import mysql.connector as connector
import xlsxwriter
from selenium.webdriver.common.action_chains import ActionChains

companyName = []
jobTitle = []
jobLocation = []


class connectionClass:
    def __init__(self):
        self.con = connector.connect(
                                    host='localhost',
                                    port='3306',
                                    user='<Your User Name>',
                                    password='<Your Password>',
                                    database='<Your Database Name>'
        )
        print(self.con)

    def insertData(self, title, company, city):
        query = "INSERT INTO <Your Table Name>(job_title, company_name, city) VALUES('{}','{}','{}')".format(title, company, city)
        print(query)
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()
        print("Data Insertion Successfull !!!")

def navigate_to_job():
    driver.get("https://www.linkedin.com/jobs/")

    #Filter the JObs
    filter_the_job()

def filter_the_job():
    try:
        #driver.execute_script("window.scrollTo(0, 80)")
        driver.get("https://www.linkedin.com/jobs/search?geoId=102713980&amp;f_WRA=true&amp;origin=JOBS_HOME_REMOTE_JOBS")
        time.sleep(5)
        date_posted_button = driver.find_element_by_class_name("search-reusables__filter-trigger-and-dropdown")
        date_posted_button.click()
        past_month_option = driver.find_elements_by_class_name("search-reusables__value-label")
        for i in past_month_option:
            if i.text == "Past Month":
                print(i.text)
                i.click()
                break
        #For showing the filter Result
        show_result = driver.find_element_by_xpath("//*[@id='ember152']").click()

        # Get the Job Details
        time.sleep(10)
        get_job_details()
    except:
        filter_the_job()

    # #Fetch all the job title
    # job_title = driver.find_elements_by_class_name("job-card-square__title")
    # jobTitle = []
    #
    # for i in job_title:
    #     jobTitle.append(i.text)
    #
    #
    # #Fetch all the job company name
    # job_company_name = driver.find_elements_by_class_name("job-card-container__company-name")
    # jobCompanyName = []
    #
    # for i in job_company_name:
    #     jobCompanyName.append(i.text)
    #
    #
    # #Fetch all the time
    # job_company_name = driver.find_elements_by_tag_name("time")
    # publishedTime = []
    #
    # for i in job_company_name:
    #     publishedTime.append(i.text)
    #
    # with xlsxwriter.Workbook('jobDetails.xlsx') as workbook:
    #     worksheet = workbook.add_worksheet()
    #
    #     for row_num, data in enumerate(jobTitle):
    #         worksheet.write("A" + str(row_num + 1), data)
    #
    #     for row_num, data in enumerate(jobCompanyName):
    #         worksheet.write("B" + str(row_num + 1), data)
    #
    #     for row_num, data in enumerate(publishedTime):
    #         worksheet.write("C" + str(row_num + 1), data)
    #
    # workbook.close()

def get_job_details():
    job_title_cls = driver.find_elements_by_css_selector('a.disabled.ember-view.job-card-container__link.job-card-list__title')
    company_name = driver.find_elements_by_css_selector('a.job-card-container__link.job-card-container__company-name.ember-view')
    job_location = driver.find_elements_by_css_selector('li.job-card-container__metadata-item')


    for i in job_title_cls:
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 100)")
        time.sleep(2)
        jobTitle.append(i.text)

    for j in company_name:
        companyName.append(j.text)

    for k in job_location:
        jobLocation.append(k.text)

    insertIntoDB()

def minimize_pop_box():

    try:
        pop_up_box = driver.find_element_by_xpath("/html/body/div[7]/aside/div[1]/header/section[2]/button[2]")
        pop_up_box.click()
        print("Successfully Destroy the Pop-Box !")
    except:
        print("There is no pop-up box")
    finally:
        # Let's navigate to our jobs feed
        navigate_to_job()

def insertIntoDB():
    obj = connectionClass()

    limit1 = len(companyName)
    limit2 = len(jobTitle)
    limit3 = len(jobLocation)

    limit = min(limit1, limit2, limit3)

    for i in range(limit):
        obj.insertData(jobTitle[i], companyName[i], jobLocation[i])
        print("All data are Inserted")

def login_again():
    userid = input("[*] Enter Your Email ID or Phone Number: ")
    password = input("[*] Enter Your Password: ")
    login(userid=userid, password=password)

def login(userid, password):

    #Navigate to LinkedIn Site
    driver.get("https://www.linkedin.com/")

    #Find the userInput and Send Your credential
    user = driver.find_element_by_xpath("/html/body/main/section[1]/div[2]/form/div[2]/div[1]/input")
    user.send_keys(userid)

    #Find the Password area & send your credential
    passwrd = driver.find_element_by_xpath("/html/body/main/section[1]/div[2]/form/div[2]/div[2]/input")
    passwrd.send_keys(password)

    #Click on Sign In Button
    signIn = driver.find_element_by_xpath("/html/body/main/section[1]/div[2]/form/button")
    signIn.click()

    #Check For Successfully Login
    url = driver.current_url
    time.sleep(1)
    if url != "https://www.linkedin.com/feed/?trk=homepage-basic_signin-form_submit":
        print("Invalid Username or Password")
        driver.implicitly_wait(10)
        login_again()

    else:
        print("Login Successfull !!!")
        driver.implicitly_wait(10)
        # Destroy the Pop_Box
        minimize_pop_box()

if __name__ == "__main__":
    userid = input("[*] Enter Your Email ID or Phone Number: ")
    password = input("[*] Enter Your Password: ")


    driver = webdriver.Chrome("<Your Webdriver Path should be here>")
    driver.maximize_window()

    login(userid=userid, password=password)