import random
import requests
import re
import time


class WenJuanXing:

    def __init__(self, url, no, subdata):
        self.wj_url = url
        self.no = int(no)
        self.subdata = subdata
        self.post_url = None
        self.header = None
        self.cookie = None

    def get_response(self):
        '''
        Access the wj_url and get the inner html.
        :return: response from the get request
        '''
        response = requests.get(url=self.wj_url, headers=self.header)
        self.cookie = response.cookies
        return response

    def get_ktimes(self):
        ''' 
        Generate an integer as arguments[ktimes] to construct the post_url.
        :return: ktimes - an integer
        '''
        return random.randint(15, 50)

    def get_jqnonce(self, response):
        ''' 
        Search for the arguments[jqnonce] from the response text through regular expression to construct the post_url.
        :param response: response from the get request
        :return: jqnonce - matched group
        '''
        jqnonce = re.search(r'.{8}-.{4}-.{4}-.{4}-.{12}', response.text)
        return jqnonce.group()
        # try:
        #     return jqnonce.group()
        # except AttributeError:
        #     return None

    def get_start_time(self, response):
        ''' 
        Search for the arguments[start_time] from the response text through regular expression to construct the post_url.
        :param response: response from the get request
        :return: start_time - matched group
        '''
        start_time = re.search(r'\d+?/\d+?/\d+?\s\d+?:\d{2}', response.text)
        return start_time.group()

    def get_rn(self, response):
        ''' 
        Search for the arguments[rn] from the response text through regular expression to construct the post_url.
        :param response: response from the get request
        :return: rn - matched group
        '''
        rn = re.search(r'\d{9,10}\.\d{8}', response.text)
        return rn.group()

    def get_id(self, response):
        ''' 
        Search for the arguments[id] from the response text through regular expression to construct the post_url.
        :param response: response from the get request
        :return: id - matched group
        '''
        id = re.search(r'\d{8}', response.text)
        return id.group()

    def get_jqsign(self, ktimes, jqnonce):
        '''
        Encrypt arguments[jqsign] with arguments[ktimes] and arguments[jqnonce] to construct the post_url.
        :param ktimes: ktimes - an integer
        :param jqnonce: jqnonce - matched group
        :return: jqnonce - a string
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
        '''
        The main function to construct the post_url.
        '''
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
        Generate ip randomly, segmented control needed.
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
        One-choice Format: [ProblemId]$[OptionId]

        Multiple-choice Format: [ProblemId]$[OptionId|OptionId...]

        Fill-in-the-blanks Format: [ProblemId]$[ContentText]

        use '{' as separators
        '''
        self.data = {
            'submitdata': self.subdata
        }

    def post_data(self):
        '''
        Send datas to the server.
        :return: result from the server
        '''
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
