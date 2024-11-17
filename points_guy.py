from bs4 import BeautifulSoup
import requests
import csv

# ----------------------------------------- THE POINTS GUY WEBSCRAPING --------------------------------------------- #

url = ('https://thepointsguy.com/credit-cards/best-pm-c3/?utm_source=google&utm_medium=cpc&utm_campaign=BRD1-Other-the%'
       '20points%20guy-650673813725&utm_term=the%20points%20guy&utm_cmpid=21787678739&utm_adgid=172258207807&utm_tgtid='
       'kwd-50590404027&utm_mt=e&utm_adid=650673813725&utm_dvc=c&utm_ntwk=g&utm_adpos=&utm_plcmnt=&utm_locphysid=102660'
       '7&utm_locintid=&utm_feeditemid=&utm_devicemdl=&utm_plcmnttgt=&utm_misc=&utm_ltpcid=Cj0KCQjwj4K5BhDYARIsAD1Ly2pu'
       'M6TIdWeD5zm4Sdr0JehPTrEkTFPIF2m1tM8-aQV5xLF9cE7v9Q4aAmfsEALw_wcB&gad_source=1&gclid=Cj0KCQjwj4K5BhDYARIsAD1Ly2p'
       'uM6TIdWeD5zm4Sdr0JehPTrEkTFPIF2m1tM8-aQV5xLF9cE7v9Q4aAmfsEALw_wcB')

response = requests.get(url)
points_guy_webpage = response.text

soup = BeautifulSoup(points_guy_webpage, "html.parser")

# --------------------------------------------- Finding card names ------------------------------------------------ #
card_name_elements = soup.find_all(class_='jsx-1331445845 cardName-title')
card_names = [card.get_text() for card in card_name_elements]

# --------------------------------------------- Finding annual fees --------------------------------------------- #
annual_fee_elements = soup.find_all(class_='jsx-1770111297')
uf_list = [fees.get_text() for fees in annual_fee_elements][2::3]
annual_fees = uf_list[:13]

# --------------------------------------------- Finding card ratings --------------------------------------------- #
rating_elements = soup.find_all(class_='jsx-eb71e6eaa52b9727 jsx-1439345612 numeric')
website_ratings = [rates.get_text() for rates in rating_elements]

# --------------------------------------------- Finding the APR's ------------------------------------------------ #
APR_elements = soup.find_all(class_='jsx-3616297574')
APR_list = [APR.get_text() for APR in APR_elements][::4]
APR_list = [APR.replace('Regular APR', '').replace('Variable', '').replace('(Variable)', '').replace('()', '').strip() for APR in APR_list]

# -------------------------------- Finding the recommended credit scores ------------------------------------------- #
scores_elements = soup.find_all(class_='jsx-854763532 range')
credit_scores = [scores.get_text() for scores in scores_elements]

# ------------------------------------- Writing to CSV files ------------------------------------------- #

filename = "the_points_guy.txt"

# Open the file for writing (will create the file if it doesn't exist)
with open(filename, mode="w", encoding="utf-8") as file:
    # Iterate through the data and write each card's details in the desired format
    for i in range(len(card_names)):
        file.write(f"Credit Card Name: {card_names[i]}\n")
        file.write(f"Ratings: {website_ratings[i]}\n")
        file.write(f"Annual Fees: {annual_fees[i]}\n")
        file.write(f"APR: {APR_list[i]}\n")
        file.write(f"Recommended Credit Scores: {credit_scores[i]}\n")
        file.write("-"*40 + "\n")  # Line separator between cards for readability

print("Data has been written to the text file.")

print(f"Data successfully written to {filename}!")