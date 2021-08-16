import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from datetime import datetime
import pathlib

class visualization():

    def generate_report(self, output):

        soup = BeautifulSoup(open("misc/template.html"), 'html.parser')

        # Company Info
        name = soup.find("h3", {"id": "NAME"})
        name.string = output['Name']

        sector = soup.find("h3", {"id": "SECTOR"})
        sector.string = output['Sector']

        country = soup.find("h3", {"id": "COUNTRY"})
        country.string = output['Country']

        # Glassdoor Info
        ratings = soup.find("h3", {"id": "RATINGS"})
        ratings.string = output['rating']

        approval = soup.find("h3", {"id": "APPROVAL"})
        approval.string = output['ceo_approval']

        friend = soup.find("h3", {"id": "FRIEND"})
        friend.string = output['recommend_to_friend']

        # Financials
        eps = soup.find("h2", {"id": "EPS"})
        eps.string = f"{output['Trailing EPS']}"

        pe = soup.find("h2", {"id": "P/E"})
        pe.string = f"{output['Trailing P/E']}"

        beta = soup.find("h2", {"id": "BETA"})
        beta.string = f"{output['Beta']}"

        dividend = soup.find("h2", {"id": "DIVIDEND"})
        dividend.string = f"{output['Annual Dividend Rate']}"

        market_cap = soup.find("h2", {"id": "MARKETCAPITALIZATION"})
        market_cap.string = f"{output['Market Capitalization']}"

        enterprise_val = soup.find("h2", {"id": "ENTERPRISEVALUE"})
        enterprise_val.string = f"{output['Enterprise Value']}"

        roe = soup.find("h2", {"id": "ROE"})
        roe.string = f"{output['Return on Equity']}"

        yoy = soup.find("h2", {"id": "YOY"})
        yoy.string = f"{output['Quarterly Revenue Growth']}"

        # Graph
        self.generate_graph(output)
        attributes = {'class': 'mt-5'}
        div = soup.find("div", {"id": "IMAGE"})
        path = f"misc/{output['Name']}.png"
        img = soup.new_tag('img', src=path, **attributes)
        div.append(img)

        # Recommendations
        tbody = soup.find("tbody", {"id": "RECOMMENDATIONS"})
        p_attributes = {'class' : 'mb-1 text-dark font-weight-medium'}
        td_attributes = {'class': 'font-weight-medium'}

        # Report Generate Date
        date = soup.find("h2", {"id": "DATE"})
        date.string = datetime.today().strftime("%Y-%m-%d")

        for k,v in output['recent_recommendations'].items():
            tr = soup.new_tag('tr')
            td_1 = soup.new_tag('td')
            p = soup.new_tag('p', **p_attributes)
            p.string = k
            td_1.append(p)
            tr.append(td_1)
            td_2 = soup.new_tag('td', **td_attributes)
            td_2.string = v
            tr.append(td_2)
            tbody.append(tr)


        self.create_html(soup, output['Name'])

    
    def create_html(self, soup, name):
        with open(f"{name}.html", "wb") as f_output:
            f_output.write(soup.prettify("utf-8")) 
        print(f"Your Report is ready at {pathlib.Path().resolve()}/{name}.html. Happy Investing!")


    def generate_graph(self, output):
        plt.close("all")

        # Cash and Debt 
        cash = dict(reversed(list(output['Cash'].items())))
        long_term_debt = dict(reversed(list(output['Long Term Debt'].items())))
       
        plt.plot(cash.keys(), cash.values(), label = 'Cash', color='green', marker='o')
        plt.plot(long_term_debt.keys(), long_term_debt.values(), label = 'Long Term Debt', color='red', marker='o')
        plt.xticks(list(long_term_debt.keys()))
        plt.ylabel('Amount in Billions')
        plt.legend()
        
        plt.savefig(f"misc/{output['Name']}.png")
        
  

