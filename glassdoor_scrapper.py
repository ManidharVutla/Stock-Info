import json
import getpass
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

#SLEEP TIME - in sec
SLEEP = 3

class glassdoor():

    def glassdoor_login_navigate(self, company):
        
        email_id, password = self.get_email_passkey()

        if len(email_id) == 0 or len(password) == 0:
            return "Credentials Not Provided"
        
        browser = webdriver.Safari()

        login_url = "https://www.glassdoor.com/profile/login_input.htm?userOriginHook=HEADER_SIGNIN_LINK"

        browser.maximize_window()
        browser.get(login_url) 

        email = browser.find_element_by_xpath('//*[@id="userEmail"]')
        passkey = browser.find_element_by_xpath('//*[@id="userPassword"]')


        email.send_keys(email_id)
        passkey.send_keys(password)

        sign_in = browser.find_element_by_xpath('//*[@id="InlineLoginModule"]/div/div/div/div[1]/div[3]/form/div[3]/div[1]/button')
        sign_in.click()

        time.sleep(3)
        search_bar = browser.find_element_by_xpath('//*[@id="sc.keyword"]')
        search_bar.click()
        search_bar.send_keys(f'{company} Reviews')
        time.sleep(3)
        search_bar.send_keys(f"{Keys.ARROW_DOWN}{Keys.ARROW_DOWN}{Keys.ENTER}")

        time.sleep(20)
        source  = browser.page_source

        browser.quit()
        
        return source
       
    

    def glassdoor_scrapping(self, page_source):

        data = {}
        if page_source=="Credentials Not Provided":
            data['rating'] = 'N/A'
            data['recommend_to_friend'] = 'N/A'
            data['ceo_approval'] = 'N/A'
        
        else:
            soup = BeautifulSoup(page_source, 'html.parser')

            rating = soup.find("div", {"class": "v2__EIReviewsRatingsStylesV2__ratingNum v2__EIReviewsRatingsStylesV2__large"}).get_text(strip=True)
            data ['rating'] = rating

            company_ratings = soup.find_all("tspan", {"class": "donut__DonutStyle__donutchart_text_val"})
            
            data['recommend_to_friend'] = f'{company_ratings[0].get_text(strip=True)}%'
            data['ceo_approval'] = f'{company_ratings[1].get_text(strip=True)}%'
            
        return data


    def get_email_passkey(self):
        try:
            with open('./secret.json', 'r') as file:
                creds = json.load(file)

            email_id = creds['email_id']
            password = creds['password']

        except FileNotFoundError:
            glassdoor_content = input("Glassdoor credentials not found, Do you want provide glassdoor credentials: Y/N:\t")
            email_id, password = "", ""
            if glassdoor_content.lower() == "y":
                email_id = input('Enter your username:\n')
                password = getpass.getpass('Enter your password:\n')

                payload = {
                    'email_id': email_id,
                    'password': password
                }

                with open('./secret.json', 'w') as file:
                    file.write(json.dumps(payload))

        return email_id, password

