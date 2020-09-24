from bs4 import BeautifulSoup
import pandas as pd
import requests

nop_apis = {}
api_no = 0
url = 'https://www.programmableweb.com/category/all/apis'
while True:

    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')

    apis = soup.find_all('tr', {'class': 'even'})
    for api in apis:
        title_tag = api.find('td', {"class": "views-field-pw-version-title"})
        title = title_tag.find('a', {'href': True}).text
        api_url = title_tag.find('a', {'href': True}).get('href')
        link = "https://www.programmableweb.com" + api_url
        api_response = requests.get(link)
        api_data = api_response.text
        category_tag = api.find('td', {"class": "views-field-field-article-primary-category"})
        category = category_tag.find('a', {'href': True}).text

        api_soup = BeautifulSoup(api_data, "html.parser")
        description = api_soup.find('div', {"class": "api_description"}).text

        api_no += 1
        nop_apis[api_no] = [title, category, link, description]
        print(api_no)
        print("title : ", title, "//", "Category :", category, "//", "link : ", link, "description: ", description,
              "\n")
    url_tag = soup.find('a', {'title': 'Go to next page'})
    if url_tag.get('href'):
        break
    else:
        break

print("Total apis: ", api_no)
nop_apis_df = pd.DataFrame.from_dict(nop_apis, orient="index",
                                     columns=['Api Title', 'category', 'Link', 'Discription'])
nop_apis_df.to_csv('npo_apis.csv')
