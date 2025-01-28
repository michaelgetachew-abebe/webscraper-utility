from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import os
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = os.getenv('LOGIN_URL', 'default-url')
USERNAME = os.getenv('USERNAME', '')
PASSWORD = os.getenv('PASSWORD', '')

app = Flask(__name__)

@app.route('/process_msisdns', methods=['POST'])
def process_msisdns():
    msisdns = request.json['msisdns']
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--ignore-ssl-errors=yes")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-urlfetcher-cert-requests')
    options.accept_insecure_certs = True

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(URL)

    login = driver.find_element(By.NAME, 'login')
    password = driver.find_element(By.NAME, 'password')
    connect_btn = driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[3]/input')
    login.clear()
    login.send_keys(USERNAME)
    password.clear()
    password.send_keys(PASSWORD)
    connect_btn.click()

    dm_center_btn = driver.find_element(By.XPATH, '//*[@id="module-list"]/div[1]/a')
    dm_center_btn.click()

    msisdn_dict = {'msisdn': [], 'imei_count': []}
    for msisdn in msisdns:
        msisdn = '+' + msisdn
        msisdn_box = driver.find_element(By.NAME, 'MSISDN')
        msisdn_box.send_keys(msisdn)
        search_btn = driver.find_element(By.NAME, 'filter')
        search_btn.click()
        msisdn_box = driver.find_element(By.NAME, 'MSISDN')
        msisdn_box.clear()

        msisdn_results = driver.find_elements(By.XPATH, '//*[@id="subscribers"]/tbody/tr')
        for i in range(len(msisdn_results)):
            imei_value = driver.find_element(By.XPATH, '//*[@id="subscribers"]/tbody/tr/td[3]').text
            imei_box = driver.find_element(By.NAME, 'IMEI')
            imei_box.send_keys(imei_value)
            search_btn = driver.find_element(By.NAME, 'filter')
            search_btn.click()
            imei_results = driver.find_elements(By.XPATH, '//*[@id="subscribers"]/tbody/tr')
            try:
                num_pages = int((driver.find_element(By.XPATH, '//*[@id="subscribers"]/thead/tr[1]/td/span[1]').text)[-2:])
                page_box = driver.find_element(By.XPATH, '//*[@id="subscribers"]/thead/tr[1]/td/div[1]/form/input[1]')
                page_box.send_keys(num_pages)
                go_btn = driver.find_element(By.XPATH, '//*[@id="subscribers"]/thead/tr[1]/td/div[1]/form/input[2]')
                go_btn.click()
                num_pages = 25 * (num_pages - 1) + len(driver.find_elements(By.XPATH, '//*[@id="subscribers"]/tbody/tr'))
            except Exception as e:
                num_pages = len(imei_results)

            imei_box = driver.find_element(By.NAME, 'IMEI')
            imei_box.clear()

        msisdn_dict['msisdn'].append(msisdn)
        msisdn_dict['imei_count'].append(num_pages)

    driver.quit()

    return jsonify(msisdn_dict)

if __name__ == '__main__':
    app.run()














import openai 
# Set your OpenAI API key 
openai.api_key = 'your-api-key' 

# Function to generate a personalized email 

def generate_outreach_email(customer_data): 
    prompt = f""" You are an AI agent tasked with drafting a professional and personalized outreach email. 
    The email should address the customer's pain points and suggest our solution. 
    Customer Details: - Name: {customer_data['name']} - Industry: {customer_data['industry']} 
    - Pain Points: {customer_data['pain_points']} - Goals: {customer_data['goals']} 
    - Product/Service: {customer_data['product']} Requirements: - Subject: Brief and relevant to the customer's industry. 
    - Email Body: Address the customer's challenges and introduce the product/service as a solution. 
    - Call to Action: Schedule a call or request a reply. Output the email in the following format: 
    Subject: [Your Subject] Body: [Your Email Body] """ 
    
    response = openai.Completion.create( engine="text-davinci-004", prompt=prompt, max_tokens=300, temperature=0.7 ) 
    return response.choices[0].text.strip() 
    

# Example usage 
customer_data = { "name": "Jane Doe", "industry": 
                 "Healthcare", "pain_points": "High administrative costs and slow patient onboarding.", 
                 "goals": "Reduce overhead and improve operational efficiency.", 
                 "product": "AI-powered workflow automation tools" } 
    
email = generate_outreach_email(customer_data) 
print(email)









import requests 
def gather_customer_data(customer_name, company_website): 
    # Simulate gathering data from a CRM or scraping a website 
    crm_data = { "name": customer_name, "industry": "Technology", "pain_points": "Difficulty scaling infrastructure", 
                "goals": "Adopt cloud-based solutions", "preferred_contact_time": "Morning", "contact_email": "example@company.com" } 
    
    # Optionally scrape data from the company website 
    website_info = f"Website overview for {company_website}" 
    
    # Combine and structure the data 
    
    customer_data = { "name": crm_data["name"], "industry": crm_data["industry"], "pain_points": crm_data["pain_points"], 
                     "goals": crm_data["goals"], "preferred_contact_time": crm_data["preferred_contact_time"], 
                     "contact_email": crm_data["contact_email"], "website_info": website_info } 
    
    return customer_data 


# Example usage 
customer_name = "TechCorp Inc." 
company_website = "www.techcorp.com" 
data = gather_customer_data(customer_name, company_website) 
print(data) 


from textblob import TextBlob 

def qa_review(draft_email): 
    # Analyze the draft email 
    analysis = TextBlob(draft_email) 
    sentiment = analysis.sentiment.polarity 
    
    # Review output 
    
    review = { "grammar_check": "Pass" if len(analysis.correct()) == len(draft_email) else "Fail", "tone_check": "Positive" if sentiment > 0 else "Neutral/Negative", "status": "Approved" if sentiment > 0.2 else "Requires Edits" } 
    return review 

# Example usage 
draft_email = """Hi John, We understand your pain points in scaling your infrastructure. 
Our cloud-based solutions are tailored to meet your needs. Let’s schedule a call to discuss this further. 
Best, TechCorp Team """ 

qa_result = qa_review(draft_email) 

print(qa_result)
