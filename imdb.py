from bs4 import BeautifulSoup
import json
import re
import requests
while True:
    try:
        #retreviing the url of imdb page
        URL = input("Please enter the url of your film or show\n")
        url = requests.get(URL).text

    except:
        print("error.")
    else:

        #parse through the page and extract the json data of the page
        soup_url = BeautifulSoup(url, 'html.parser')
        url_info1 = soup_url.find("script",type="application/ld+json").string.strip()
        json_url= json.loads(url_info1)

        #parse through the page and extract the non-json data of the page
        data = []
        subtext = soup_url.find("div", {'class': 'subtext'})

        for i in subtext.contents:
            data.append(i.string)
        year,country = data[-2].split('(')
        country=country[:-2]


        #validates whether the data is present or not
        def check_valid(x,y=None):
            try:
                if y is None:
                    return json_url[x]
                else:
                    if type(json_url[x]) is list:
                        return [i[y] for i in json_url[x] if i["@type"] == 'Person']
                    else:
                        return json_url[x][y]
            except:
                return None


        #prints the results retrieved
        print(f'''
\n\n\n\n
Name: {check_valid("name")}
Type: {check_valid('@type')}
Genre: {check_valid('genre')}
Released Date: {year}
Country: {country}
Top actors/actresses: {check_valid('actor','name')}
Parent rating: {check_valid('contentRating')}
Director: {check_valid('director','name')}
Writers: {check_valid('creator', 'name')}
Average Score: {check_valid('aggregateRating','ratingValue')}
Plot: {check_valid('description')} 


        ''')

        print("Would you like to save this information in a file? (y/n)\n")

        #write the data to a text file
        while True:
            a=input()
            if a=='y'or 'Y':
                with open(f'filmshow/{check_valid("name")}.text', 'w') as f:
                    f.write(f'''Name: {check_valid("name")}
Type: {check_valid('@type')}
Genre: {check_valid('genre')}
Released Date: {year}
Country: {country}
Top actors/actresses: {check_valid('actor','name')}
Parent rating: {check_valid('contentRating')}
Director: {check_valid('director','name')}
Writers: {check_valid('creator', 'name')}
Average Score: {check_valid('aggregateRating','ratingValue')}
Plot: {check_valid('description')} ''')
                break
            elif a=='n' or 'N':
                print("Thank you")
                break
            else:
                print('Please type "y" or "n"')
        break

