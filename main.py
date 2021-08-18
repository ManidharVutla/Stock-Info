from glassdoor_scrapper import glassdoor
from stock_financials import stock_financials
from visualization import visualization

output=dict()

company = input("Enter Company name:")
ticker = input("Enter Company ticker symbol:")

glassdoor_content = input("Do you want provide glassdoor credentials: Y/N:\t")
gd = glassdoor()

if glassdoor_content == "Y":
    url = gd.glassdoor_login_navigate(company)
    output.update(gd.glassdoor_scrapping(url))
else:
    output.update(gd.glassdoor_scrapping("Credentials Not Provided"))

s = stock_financials()
output.update(s.get_stock_financials(ticker))

v = visualization()
v.generate_report(output)





    