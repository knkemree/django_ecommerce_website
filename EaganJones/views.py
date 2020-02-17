from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
import requests
import urllib.request
from bs4 import BeautifulSoup
from fuzzywuzzy import process
import pandas as pd
from django.shortcuts import render
# import json to load json data to python dictionary
import json
# urllib.request to make a request to api
import urllib.request

# Create your views here.
from EaganJones.models import Companies


def company_list(request):

    ## initializing the UserAgent object
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
    # creating our own def to parse urls
    def make_soup(url):
        ## getting the reponse from the page using get method of requests module
        page = requests.get(url, headers=headers)

        ## storing the content of the page in a variable
        html = page.content

        ## creating BeautifulSoup object
        soup = BeautifulSoup(html, "html.parser")

        return soup

    data_list = []
    url_collection = []
    html_table = []
    excel_link = []
    indexlink = []
    company_inf =[]

    if request.method == 'POST':

        try:
            ticker = request.POST['test']
        except:

            csv_file1 = request.FILES["csv_file1"]


            c = csv_file1.read().decode("utf-8")

            ticker = c.replace('\r', ",", (c.count('\r')-1)).replace('\n', "").replace("\r", "")



        url = urllib.request.urlopen('https://datafied.api.edgar-online.com/v2/companies?primarysymbols=' + ticker + '&appkey=a76c61e85f9225192ce5cbbd0b22fb52').read()
        print(url)

        # converting JSON data to a dictionary
        list_of_data = json.loads(url)
        print(list_of_data)
        y = int(list_of_data['result']['totalrows'])

        if y == 0:
            messages.success(request, "Unmatched Ticker Symbol or No Available Financial Data.")
            return redirect('EaganJones:company_list')
        # data for variable list_of_data
        for i in range(0, y):
                    data = {
                    "cik": str(list_of_data['result']['rows'][i]['values'][0]['value']),
                    "companyname": str(list_of_data['result']['rows'][i]['values'][1]['value']),
                    "entityid": str(list_of_data['result']['rows'][i]['values'][2]['value']),
                    "primaryexchange": str(list_of_data['result']['rows'][i]['values'][3]['value']),
                    "marketoperator": str(list_of_data['result']['rows'][i]['values'][4]['value']),
                    "markettier": str(list_of_data['result']['rows'][i]['values'][5]['value']),
                    "primarysymbol": str(list_of_data['result']['rows'][i]['values'][6]['value']),
                    "siccode": str(list_of_data['result']['rows'][i]['values'][7]['value']),
                    "sicdescription": str(list_of_data['result']['rows'][i]['values'][8]['value']),

                        }

                    companyname = list_of_data['result']['rows'][i]['values'][1]['value']
                    cik = list_of_data['result']['rows'][i]['values'][0]['value']
                    primarysymbol = list_of_data['result']['rows'][i]['values'][6]['value']
                    markettier = list_of_data['result']['rows'][i]['values'][5]['value']
                    sicdescription = list_of_data['result']['rows'][i]['values'][8]['value']

                    data_list.append(data)




        x = ticker.split(",")

        for i in x:
            url2 = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=' + i + '&type=10-k&dateb=&owner=exclude&count=40'
            url_collection.append(url2)

        print(url_collection)


        for c in url_collection:

            souped_link = make_soup(c)
            table = souped_link.find("table", {"class": "tableFile2"})

            indexlink_list = []

            for row in table.find_all("tr"):
                cells = row.findAll("td")
                print(len(cells))
                if len(cells) == 5:

                    if cells[0].text.strip() == '10-K':

                        link = cells[1].find("a", {"id": "documentsbutton"})['href']
                        url = "https://www.sec.gov" + link
                        indexlink_list.append(url)
                        indexlink = indexlink_list[0]  # get latest 10=k filing link

            souped_button = make_soup(indexlink)
            table2 = souped_button.find("div", {"id": "seriesDiv"})
            tables_page = "https://www.sec.gov" + table2.find("a")["href"]

            souped_excel_button = make_soup(tables_page)
            excel_button = souped_excel_button.find("td").find_all("a")[1]['href']
            excel_link = "https://www.sec.gov" + excel_button
            print(excel_link)

            a = pd.ExcelFile(excel_link).sheet_names

            print(a)
            c = process.extractOne("CASH FLOWS STATEMENTS", a)
            d = process.extractOne("CONSOLIDATED STATEMENTS OF CASH", a)
            if d[1] > c[1]:
                cash_flows_sheet = d[0]
            else:
                cash_flows_sheet = c[0]
            print(c)
            print(d)

            df = pd.read_excel(excel_link, sheet_name=cash_flows_sheet, na_filter=False)
            print(df)

            a = pd.DataFrame(df)

            html_table = a.to_html(index=False)
            json_table = a.to_json()

            Companies.objects.get_or_create(cik=cik,
                                     primarysymbol=primarysymbol,
                                     companyname=companyname,
                                     jsonnn=json_table,
                                     table=html_table,
                                     markettier=markettier,
                                     sicdescription = sicdescription)
            print(json_table)

            company_inf = Companies.objects.order_by('-created_at')



    context = {
            'data_list': data_list,
            'excel_link':excel_link,
            'html_table': html_table,
            'company_inf': company_inf

            }
    return render(request, "company_list.html", context)

def company_detail(request, id, primarysymbol):
    company = get_object_or_404(Companies, id=id, primarysymbol=primarysymbol)
    companies = Companies.objects.all()
    context = {'company': company,
               'companies': companies,
               }
    return render(request, 'company_detail.html', context)

