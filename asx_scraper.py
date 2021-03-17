from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

def scrape_option_chain(code, expiry_month, expiry_year , option_type = 'B'):

    # URL parameters
    expiry = {'month' : expiry_month ,'year' : expiry_year}

    base_url="https://www.asx.com.au/asx/markets/optionPrices.do?by=underlyingCode&underlyingCode=CBA&expiryDate=Sep+2020&optionType=B"
    base_url_start = "https://www.asx.com.au/asx/markets/optionPrices.do?by=underlyingCode"
    base_url_code = "underlyingCode=" + code
    base_url_expiry = "expiryDate=" + expiry['month'] + "+" + expiry['year']
    base_url_type = "optionType=" + option_type

    url = base_url_start + "&" + base_url_code + "&" + base_url_expiry + "&" + base_url_type

    print(url)

    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text

    # Parse the html content
    soup = BeautifulSoup(html_content, "lxml")
    #print(soup.prettify()) # print the parsed data of html

    # Find table elements
    option_table = soup.find("table", attrs={"class": "datatable options", "id": "optionstable"})
    option_table_data = option_table.tbody.find_all("tr")  # contains 2 rows

    # Get table column headings
    headings = []
    for th in option_table_data[0].find_all("th"):
        headings.append(th.attrs['class'][0])


    # Adjust header lists ahead of table parse
    option_table_data.pop(0) # remove header row

    code_column = headings[0] # code column represented as <th> element
    headings.pop(0)

    # Parse table
    table_data = []
    for tr in option_table_data :
        t_row = {}

        # set code column first
        t_row[code_column] =  tr.th.a.text

        # find all td's(3) in tr and zip it with t_header
        for td, th in zip(tr.find_all("td"), headings):
            t_row[th] = td.text
        table_data.append(t_row)

    # Convert to dataframe
    option_table_df = pd.DataFrame(table_data)

    return option_table_df

# option_table_df.to_csv(code + "-option_chain-20200818.csv")


