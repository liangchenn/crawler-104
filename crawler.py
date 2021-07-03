import requests
import re
import json 

from datetime import datetime
from tqdm import tqdm
import pandas as pd 


class JobCrawler(object):

    # prefix for 104 website
    PRE_LINK = "https://www.104.com.tw/jobs/search/"
    # area-area_code mapping file path
    MAP_PATH = "./mapping.json"

    def __init__(self):

        self.page_source_code = None
        self.url = None
        self.mapping = None


    def get(self, url):
        '''get response.'''

        res = requests.get(url)
        if res.status_code == 200:
            self.page_source_code = res.text

        return 


    def _parse_all_count(self):
        '''parse page source code and return counts of jobs of different types.'''

        # Found counts of job on the page 
        text = re.search(r'initFilter =({(.*?)});', self.page_source_code).group(1)
        values = json.loads(text)['count'][:5]
        keys = ['all', 'fulltime', 'parttime', 'highend', 'temp']
        res = dict([(k, v) for k, v in zip(keys, values)])

        return res

    def _get_area_mapping(self):
        '''obtain area mapping from preprocessing work.'''

        with open(self.MAP_PATH, 'r') as fin:
            self.mapping = json.load(fin)

        return 


    def crawl(self):
        '''
        Main crawler function.
        - compose urls for different areas and job experience criteria
        - get the number of counts of each job type  
        - save results to data directory
        '''

        # get area code
        self._get_area_mapping()

        # final results list
        result = []

        # for each area
        for area in tqdm(self.mapping):
            # for each job experience criteria
            for exp in [1, 3, 5, 10, 99]:
                # compose url with area and experience condition
                url = f"https://www.104.com.tw/jobs/search/?area={area['area_code']}&jobexp={exp}&isnew=0"
                
                # obtain response and parse the number of counts
                self.get(url)
                counts = self._parse_all_count()

                # compose subset result 
                res = {
                    "area_name" : area['area_name'],
                    "area_code" : area['area_code'],
                    "job_exp" : exp
                }

                # add counts of job under different types to res
                res.update(counts)
                # append subset result to list for all results
                result.append(res)

        # prepare output file destination, add time information
        outputfile = "data/result-" + datetime.today().strftime('%Y-%m-%d') + '.csv'
        # convert into csv format with pandas modules
        df = pd.DataFrame(result)
        # write csv file
        df.to_csv(outputfile)

        return


if __name__ == "__main__":

    from datetime import datetime
    timestamp = datetime.today().strftime("%Y-%m-%d %H:%M:%S")


    try:
        # initialize job and start crawling
        job = JobCrawler()
        job.crawl()
        print(f'Finish crawling job @ {timestamp}')

        # keep working record to work.log
        with open('work.log', 'a') as f:
            f.write(f"[{timestamp}] Crawler job successfully done.\n")

    except KeyboardInterrupt:
        raise
    except Exception as e:
        # handle exception and keep error msg to exception.log
        with open('exception.log', 'a') as f:
            f.write(f"[{timestamp}] Error occurred \t {e}\n")
