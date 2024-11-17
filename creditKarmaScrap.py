from bs4 import BeautifulSoup
import requests
import csv

# Open the URL
URL = "https://www.creditkarma.com/credit-cards"
response = requests.get(URL)
credit_karma = response.text

# Parse the HTML
soup = BeautifulSoup(credit_karma, 'html.parser')

# Find all elements with the target class
cards = soup.find_all(
    class_='jsx-3424950016 flex flex-column flex-row-ns items-stretch justify-between-l pt2 pt3-ns offer')

# Initialize empty lists to store the data
card_names = []
ratings = []
annual_fees = []
APRs = []
credit_scores = []

# Iterate through the cards and extract the necessary information
for card in cards:
    # Extract Card Name
    cardName = card.find(class_='lh-copy mv0 f4 f3-ns')
    card_names.append(cardName.get_text().strip())

    # Extract Rating
    rating = card.find('div', class_='flex-shrink-0 mr2')
    ratings.append(rating.get('aria-label') if rating else "Not available")

    # Extract Annual Fee
    annual_fee = card.find('div', class_='normal ck-black-60 f5 mt3 mb2', string="Annual fee")
    if annual_fee:
        fee_value = annual_fee.find_next('p', class_='ma0')
        annual_fees.append(fee_value.text.strip())
    else:
        annual_fees.append("Not available")

    # Extract APR
    A_pr = card.find('div', class_='normal ck-black-60 f5 mt3 mb2', string="Regular purchase APR")
    if A_pr:
        A_pr_value = A_pr.find_next('p', class_='ma0')
        APRs.append(A_pr_value.text.strip())
    else:
        APRs.append("Not available")

    # Extract Recommended Credit Scores
    credit_scores.append("Credit Karma does not support.")

filename = "credit_karma_credit_cards.txt"

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

print("Data has been written to 'credit_karma_credit_cards.txt'")
