from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

# Set up the WebDriver (adjust path if needed)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

# Open the URL
URL = "https://www.nerdwallet.com/l/compare-financial-products-2g?bucket_id=sem-homepage-google+version&ds_rl=1246084&gad_source=1&gclid=Cj0KCQjwj4K5BhDYARIsAD1Ly2pdOFLeNpP_m3aBU4NiIKuj9lf_o1moKngVUXkgXMjpez1cLm2rUPoaAgz7EALw_wcB&gclsrc=aw.ds&mktg_body=1678&mktg_hline=11649&mktg_place=kwd-40958987563&model_execution_id=5D260DE2-7EC0-45CA-8CD3-7EF8E5A9EA01&nw_campaign_id=150238270218585900&utm_campaign=cc_mktg_paid_060716_brand_exact&utm_content=ta&utm_medium=cpc&utm_source=goog&utm_term=nerdwallet"

driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)

# Wait for the content to load
time.sleep(5)  # Adjust if necessary

# Use BeautifulSoup to parse the dynamically loaded HTML
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find the card class in general
cards = soup.find_all(class_='_2y0rmn')

# Initialize empty lists to store data
card_names = []
ratings = []
annual_fees = []
APRs = []
credit_scores = []

# Extract data for each card
for card in cards:
    # Extract Card Name
    cardName = card.find(class_='_2VV_pT zeCuXk _3VmbAf _28z5Fp uaOakE _3fSL8e')
    # Extract Rating
    rating = card.find(class_='_21c6Cw _3XU-cR')
    # Extract Annual Fee
    annual_fee = card.find('div', class_='_3bILC5 _23q5GU', string="Annual fee")
    # Extract APR
    A_pr = card.find('div', class_='_3bILC5 _23q5GU', string="Regular APR")
    # Extract Recommended Credit Score
    credit = card.find('div', class_='_3bILC5 _23q5GU', string="Recommended Credit Score")

    # Only include cards with a name, rating, and annual fee
    if cardName and rating and annual_fee:
        card_names.append(cardName.get_text().strip())
        ratings.append(rating.get_text().strip())

        fee_value = annual_fee.find_next('p', class_='_28z5Fp _2QGW4B')
        annual_fees.append(fee_value.text.strip() if fee_value else "Not available")

        if A_pr:
            A_pr_value = A_pr.find_next('p', class_='_28z5Fp _2QGW4B')
            APRs.append(A_pr_value.text.strip())
        else:
            APRs.append("Not available")

        if credit:
            credit_score = credit.find_next('div', class_='KssUqC')
            credit_scores.append(credit_score.text.strip())
        else:
            credit_scores.append("Not available")

filename = "nerdwallet_credit_cards.txt"

# Open the file for writing (will create the file if it doesn't exist)
with open(filename, mode="w", encoding="utf-8") as file:
    # Iterate through the data and write each card's details in the desired format
    for i in range(len(card_names)):
        file.write(f"Credit Card Name: {card_names[i]}\n")
        file.write(f"Ratings: {ratings[i]}\n")
        file.write(f"Annual Fees: {annual_fees[i]}\n")
        file.write(f"APR: {APRs[i]}\n")
        file.write(f"Recommended Credit Scores: {credit_scores[i]}\n")
        file.write("-"*40 + "\n")  # Line separator between cards for readability

print("Data has been written to the text file.")
# Close the WebDriver
driver.quit()

print("Data has been written to 'nerdwallet_credit_cards.txt'")
