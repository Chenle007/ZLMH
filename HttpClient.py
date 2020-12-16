import requests
import os
import json
from enum import Enum

TIME_OUT = 25


class Method(Enum):
    GET = 1
    POST = 2


class HttpClient(object):
    def __init__(self):
        self.session = requests.session()
        self.cookies = None

    def request(self, url, method, cookies=None, postData=None, headers=None, formats="json", encoding=None,jsonData = None,
                timeout=TIME_OUT, allow_redirects=True):
        if headers:
            self.session.headers.update(headers)

        if self.cookies:
            self.session.cookies = self.cookies

        if cookies:
            self.session.cookies = cookies

        try:
            if method == Method.GET:
                response = self.session.get(url, timeout=timeout,allow_redirects=False)
            else:
                response = self.session.post(url, data=postData, timeout=timeout,allow_redirects=allow_redirects,json=jsonData)
            if response.status_code == 200:
                self.session.close()
                if formats == "response":
                    return response
                if formats == "json":
                    return response.json()
                elif formats == "url":
                    return response.url
                elif formats == 'file':
                    return response.content
                else:
                    responseText = ""
                    if encoding:
                        response.encoding = encoding
                        responseText = response.text
                    else:
                        responseText = response.text
                    if formats == "UrlText":
                        return (response.url, responseText)
                    else:
                        return responseText
            elif response.status_code == 302:
                return response
            else:
                self.session.close()
                print("request error status_code:%s", response.status_code)
                return response
        except Exception as e:
            self.session.close()
            print("request error")
            print(e)
            return None

    def download(self, url, dirPath, fileName, headers=None):
        if headers:
            self.session.headers.update(headers)
        try:
            response = self.session.get(url, timeout=TIME_OUT)
            if response.status_code == 200:
                if not os.path.exists(dirPath):
                    os.makedirs(dirPath)
                with open(os.path.join(dirPath, fileName), "wb") as code:
                    code.write(response.content)
                response.close()
                return os.path.join(dirPath, fileName)
            else:
                response.close()
                return None

        except Exception as e:
            self.session.close()
            return None

    def uploadFile(self, url, files, data=None, headers=None):
        print("URL:%s,data%s", url, data)
        if headers:
            self.session.headers.update(headers)
        response = self.session.post(url, files=files, data=data)
        print(response.status_code)
        if response.status_code == 200:
            return 'SUCCESS'
        else:
            return 'FALSE'

    def getCookies(self):
        cookiesDict = {c.name: c.value for c in self.session.cookies}
        return str(cookiesDict)

    def setCookies(self, cookies):
        self.cookies = cookies
        pass


if __name__ == "__main__":
    client = HttpClient()
    result = client.request("http://www.cwl.gov.cn/cwl_admin/kjxx/findKjxx/forIssue?name=ssq&code=2019106", Method.GET, headers={'Accept': 'application/json, text/javascript, */*; q=0.01',
                            'Referer': 'http://www.cwl.gov.cn/kjxx/ssq/',
                            'User-Agent': 'Mozilla/5.0',
                            'X-Requested-With': 'XMLHttpRequest'}, formats="json")
    data = json.dumps(result)
    dict = json.loads(data)
    balls = dict['result'][0]
    print ("red:"+balls['red'])
    print ("blue:"+balls['blue'])
