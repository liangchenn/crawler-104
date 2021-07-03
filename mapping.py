import re             # for regular expression (regex)
import json           # for saving data
import requests       # for obtaining response

from tqdm import tqdm # for progress bar

def get_city_area_code():

    '''obtain area code for each district in Taiwan on 104 website.'''

    # generate city string
    cities = '''台北市, 新北市, 宜蘭縣, 基隆市, 桃園市, 新竹縣, 苗栗縣, 台中市, 彰化縣, 南投縣, 雲林縣, 嘉義縣, 台南市, 高雄市, 屏東縣, 台東縣, 花蓮縣, 澎湖縣, 金門縣, 連江縣'''
    # number of subdivisions of each city
    subdivisions = [12, 29, 12, 7, 13, 14, 18, 29, 26, 13, 20, 19, 37, 38, 33, 16, 13, 6, 6, 4]
    # city code on 104 website, slightly different from the numerical order (e.g. 9, 17 are missing)
    codes  = [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 16, 18, 19, 20, 21, 22, 23]

    # create city list of dict with list comprehension
    city_list = [{'city' : city, 'code' : f"{i:02d}", 'num' : num} for city, i, num in zip(cities.split(', '), codes, subdivisions)]

    # create mapping list for (area_name, area_code) mapping
    mapping = []

    # for each city
    for city in tqdm(city_list):

        # for each subdivisions in the city
        for sub in range(city['num']):

            # crawl down corresponding page, and get the information in response

            # the structured data would be saved in url with list before query params
            url = f"https://www.104.com.tw/jobs/search/list?area=60010{city['code']}{sub+1:03d}"
            # will need referer in the header to obtain the correct response
            referer = f"https://www.104.com.tw/jobs/search/?area=60010{city['code']}{sub+1:03d}"
            # response
            res = requests.get(url, headers={"Referer" : referer})

            try:
                # the area code and area name are saved in data --> filterDesc --> area
                data = json.loads(res.text)['data']['filterDesc']['area']
                # append to list
                mapping += data
            except:
                # abnormal case
                print((city, sub+1))

    # result list
    # use regex to parse for city, district name
    # use list comprehension to 
    res = [{
        "area_name" : p['des'], 
        "area_code" : p['no'], 
        "city" : re.search('(.*?)[縣市]', p['des']).group(0), 
        "district" : re.search("[縣市]((.*?)[鄉鎮市區])", p['des']).group(1) if len(p['des']) > 3 else "",
        } for p in mapping]

    return res


if __name__ == '__main__':
    
    res = get_city_area_code()
    with open('mapping.json', 'w') as f:
        json.dump(res, f)





