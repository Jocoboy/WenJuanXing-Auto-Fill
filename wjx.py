import random
import requests
import re
import time

class WengJuanXing:

    def __init__(self, url, no, exp):
        self.wj_url = url
        self.no = int(no)
        self.exp = exp
        self.post_url = None
        self.header = None
        self.cookie = None

    def get_response(self):
        '''
        Get response from wj_url.
        '''
        response = requests.get(url=self.wj_url, headers=self.header)
        self.cookie = response.cookies
        return response

    def get_ktimes(self):
        ''' 
        Generate arguments[ktimes] (randomly) of post_url.
        '''
        return random.randint(5, 18)

    def get_jqnonce(self, response):
        ''' 
        Generate arguments[jqnonce] (regularly) of post_url.
        '''
        jqnonce = re.search(r'.{8}-.{4}-.{4}-.{4}-.{12}', response.text)
        return jqnonce.group()

    def get_start_time(self, response):
        ''' 
        Generate arguments[starttime] (regularly) of post_url.
        '''
        start_time = re.search(r'\d+?/\d+?/\d+?\s\d+?:\d{2}', response.text)
        return start_time.group()

    def get_rn(self, response):
        ''' 
        Generate arguments[rn] (regularly) of post_url.
        '''
        rn = re.search(r'\d{9,10}\.\d{8}', response.text)
        return rn.group()

    def get_id(self, response):
        ''' 
        Generate arguments[id] (regularly) of post_url.
        '''
        id = re.search(r'\d{8}', response.text)
        return id.group()

    def get_jqsign(self, ktimes, jqnonce):
        '''
        Generate jqsign referring to ktimes and jqsign.
        '''
        result = []
        b = ktimes % 10
        if b == 0:
            b = 1
        for char in list(jqnonce):
            f = ord(char) ^ b
            result.append(chr(f))
        return ''.join(result)

    def set_post_url(self):
        self.set_header()
        response = self.get_response()
        ktimes = self.get_ktimes()
        jqnonce = self.get_jqnonce(response)
        start_time = self.get_start_time(response)
        rn = self.get_rn(response)
        id = self.get_id(response)
        jqsign = self.get_jqsign(ktimes, jqnonce)
        # Generate a time stamp.
        time_stamp = '{}{}'.format(int(time.time()), random.randint(100, 200))
        url = 'https://www.wjx.cn/joinnew/processjq.ashx?submittype=1&curID={}&t={}&starttim' \
              'e={}&ktimes={}&rn={}&jqnonce={}&jqsign={}'.format(
                  id, time_stamp, start_time, ktimes, rn, jqnonce, jqsign)
        self.post_url = url
        print(self.post_url)

    def set_header(self):
        '''
        Set header refer to ip(generated randomly).
        '''
        ip = '{}.{}.{}.{}'.format(112, random.randint(
            64, 68), random.randint(0, 255), random.randint(0, 255))
        self.header = {
            'X-Forwarded-For': ip,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko\
                        ) Chrome/71.0.3578.98 Safari/537.36',
        }

    def set_data(self):
        '''
        Multiple Choice Format: {ProblemId}${OptionId}
        '''
        self.data = {
            'submitdata': self.exp
        }

    def post_data(self):
        self.set_data()
        response = requests.post(
            url=self.post_url, data=self.data, headers=self.header, cookies=self.cookie)
        return response

    def run(self):
        self.set_post_url()
        result = self.post_data()
        print(result.content.decode())

    def mul_run(self):
        for i in range(self.no):
            self.run()



