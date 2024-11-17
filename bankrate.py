from bs4 import BeautifulSoup
import requests
import csv

# ----------------------------------------- BANKRATE WEBSCRAPING --------------------------------------------- #

url = ('https://www.bankrate.com/finance/credit-cards/todays-best-credit-cards-pm-gp/')

response = requests.get(url)
points_guy_webpage = response.text

soup = BeautifulSoup(points_guy_webpage, "html.parser")

# --------------------------------------------- Finding card names ------------------------------------------------ #
card_name_elements = soup.find_all(class_='text-lg md:text-2xl display-inline-block leading-6 md:leading-7 type-heading'
                                          '-three text-black js-product-box__title m-0 hover:underline hover:text-blue')

card_names = [card.get_text().replace('\n', '').strip() for card in card_name_elements]

# --------------------------------------------- Finding the ratings ------------------------------------------------ #
ratings_elements = soup.find_all(class_='text-sm type-heading-four')
ratings = [rates.get_text() for rates in ratings_elements][::2]

# --------------------------------------------- Finding the annual fees ----------------------------------------- #
annual_fees_elements = soup.find_all(class_='mb-0 text-black font-circular-bold type-body-two text-lg')

a_fees = [fees.get_text() for fees in annual_fees_elements]

filtered_fees = [
    fee.strip()
    for fee in a_fees
    if '$' in fee and 'Cash' not in fee and 'cash' not in fee and 'Earn' not in fee and '$200' not in fee
]

# --------------------------------------------- Finding the APR's ------------------------------------------------ #
APR_elements = soup.find_all(class_='mb-0 text-black font-circular-bold type-body-two text-lg')

uf = [elements.get_text() for elements in APR_elements]
APRs = [
    APR.replace("(Variable)", "").replace("Variable", "").strip()
    for APR in uf
    if 'Variable' in APR
]

# ------------------------------------ Finding the recommended credit scores -------------------------------- #
scores_elements = soup.find_all(class_='mr-1 text-slate text-sm')

credit_scores = [
    credits.get_text().replace('Recommended credit score: ', '').strip()
    for credits in scores_elements
    if 'Recommended credit score: ' in credits.get_text()
]

# ------------------------------------- Writing to CSV files ------------------------------------------- #

# Define the filename
# Define the filename
# Define the filename
filename = "bankrate_credit_cards.txt"

# Open the file for writing (will create the file if it doesn't exist)
with open(filename, mode="w", encoding="utf-8") as file:
    # Iterate through the data and write each card's details in the desired format
    for i in range(len(card_names)):
        file.write(f"Credit Card Name: {card_names[i]}\n")
        file.write(f"Ratings: {ratings[i]}\n")
        file.write(f"Annual Fees: {filtered_fees[i]}\n")
        file.write(f"APR: {APRs[i]}\n")
        file.write(f"Recommended Credit Scores: {credit_scores[i]}\n")
        file.write("-"*40 + "\n")  # Line separator between cards for readability

print("Data has been written to the text file.")


# # Open the file for writing
# with open(filename, mode="w", newline='', encoding="utf-8") as file:
#     writer = csv.writer(file)

#     # Write the header row
#     writer.writerow(["Credit Card Name", "Rating", "Annual Fees", "APR", "Recommended Credit Scores"])

#     # Iterate through the data and write rows
#     for i in range(len(card_names)):
#         row = [
#             card_names[i] if i < len(card_names) else "N/A",
#             ratings[i] if i < len(ratings) else "N/A",
#             filtered_fees[i] if i < len(filtered_fees) else "N/A",
#             APRs[i] if i < len(APRs) else "N/A",
#             credit_scores[i] if i < len(credit_scores) else "N/A"
#         ]
#         writer.writerow(row)

print(f"Data successfully written to {filename}!")


