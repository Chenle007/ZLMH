import HttpClient
import json
import re
import requests

version = "0.0.2"
URL = "http://app.91fuyun.com:8787/service/rest"

#⚠️特殊处理漫画Id⚠️下方SpecialComicObj中填入漫画ID对应总页数估算值
SpecialComicId = ["4867"]
#⚠️特殊处理漫画页数（可以估算个大概值）
SpecialComicObj = {"4867":64}

class ReadComicData(object):
    # 转换Json对象
    def toJsonObj(self, resObj):
        jsonStr = json.dumps(resObj)
        resData = json.loads(jsonStr)
        return resData

    #网络请求
    def requestWithBody(self, data):
        result = client.request(URL, HttpClient.Method.POST, headers={"Host": "app.91fuyun.com:8787",
                                                                      "Content-Type": "application/x-www-form-urlencoded",
                                                                      "Connection": "keep-alive", "Accept": "*/*",
                                                                      "User-Agent": "ComicReader/1.2 (iPhone; iOS 13.3.1; Scale/3.00)",
                                                                      "Accept-Language": "zh-Hans-CN;q=1, en-CN;q=0.9, zh-Hans;q=0.8, en;q=0.7",
                                                                      "Content-Length": str(len(data)),
                                                                      "Accept-Encoding": "gzip, deflate"},
                                postData=data)
        return self.toJsonObj(result)

    #查询列表
    def checkComicListWithName(self, name):
        body = {"api":"cartoon.search","apiVersion":"v1","app_version":"6","app_version_name":"1.2","appname":"%E5%AE%85%E6%A8%82%E6%BC%AB%E7%95%AB","channel":"tg1","deviceId":"appVersionName%3D2.4.7%26mobileModel%3DiPhone4%2C1%26osVersionCode%3D13.3.1","game":"cartoon","lchannel":"2","os":"ios","package":"com.zhaile.mh","params[keyword]":name,"params[supports_pay]":"1","params[token]":"2667179a7e9e165b0374ee98e992e6786783","params[username]":"sado123","since":"0"}
        result = self.requestWithBody(body)
        return result

    #查看漫画目录
    def checkCmoicDetailListWithComicId(self, comicId):
        body = {"api":"cartoon.getcartoon","apiVersion":"v1","app_version":"6","app_version_name":"1.2","appname":"%E5%AE%85%E6%A8%82%E6%BC%AB%E7%95%AB","channel":"tg1","deviceId":"appVersionName%3D2.4.7%26mobileModel%3DiPhone4%2C1%26osVersionCode%3D13.3.1","game":"cartoon","lchannel":"2","os":"ios","package":"com.zhaile.mh","params[cartoon_id]":str(comicId),"params[supports_pay]":"1","params[token]":"2667179a7e9e165b0374ee98e992e6786783","params[username]":"sado123","since":"0"}
        result = self.requestWithBody(body)
        return result

    #查看漫画详情
    def readCmoicWithPageNo(self, comicId, pageNo):
        body = {"api":"cartoon.getcartoonchapter","apiVersion":"v1","app_version":"6","app_version_name":"1.2","appname":"%E5%AE%85%E6%A8%82%E6%BC%AB%E7%95%AB","channel":"tg1","deviceId":"appVersionName%3D2.4.7%26mobileModel%3DiPhone4%2C1%26osVersionCode%3D13.3.1","game":"cartoon","lchannel":"2","os":"ios","package":"com.zhaile.mh","params[cartoon_id]":str(comicId),"params[chapter_no]":str(pageNo),"params[supports_pay]":"1","params[token]":"2667179a7e9e165b0374ee98e992e6786783","params[username]":"sado123","since":"0"}
        result = self.requestWithBody(body)
        return result

if __name__ == "__main__":
    global client
    global comic
    client = HttpClient.HttpClient()
    comic = ReadComicData()
    print("初始化成功 v" + version )
    while (1):
        keyWorld = input("请输入搜索关键字(输入exit退出程序):").encode("UTF-8")
        if (keyWorld == "exit".encode("UTF-8")):
            print("---- 退出程序 ----")
            exit(0)
        keyWorldRes = comic.checkComicListWithName(keyWorld)
        # print(keyWorldRes)
        if (str(keyWorldRes["code"]) == "200" ):
            print("🎉🎉查询成功🎉🎉")
            for line in keyWorldRes["data"]:
                print("ID:"+ line['id'] + " " + line["title"] + " 评分：" + line['score'])
            targetId = input("请选择漫画ID:")
            comicDetailListRes = comic.checkCmoicDetailListWithComicId(targetId)
            if (str(comicDetailListRes["code"]) == "200"):
                print("🎉🎉检索成功🎉🎉")
                detailLine = comicDetailListRes["data"]
                listCount = len(detailLine["detail"])
                print("该漫画总章数为：" + str(listCount))
                # for datailLineMsg in detailLine["detail"]:
                #     print(datailLineMsg)
                readRes = comic.readCmoicWithPageNo(comicId=targetId, pageNo=0)
                if (str(readRes["code"]) == "200"):
                    print("🎉🎉第一章免费，可以爬取🎉🎉")
                    totalNum = (len(readRes["data"]["content"]) * listCount )
                    for specialId in SpecialComicId:
                        if (specialId == str(targetId)):
                            totalNum = int(SpecialComicObj[specialId])
                    print("该漫画总图数约为： " + str(totalNum) + " 张")
                    canDownload = input("是否允许下载? (YES or NO)：")
                    if (canDownload == "y" or canDownload == "yes" or canDownload == "YES"):
                        canDownload = None
                    else:
                        print("退出程序")
                        exit(0)
                    dir = input("请输入存放文件夹(如：/xxx/Desktop/demo/)")
                    if (dir == ""):
                        print("输入内容为空")
                        exit(0)
                    firstPic = readRes["data"]["content"][0]
                    locArray = firstPic.split("/")
                    sig = locArray[(len(locArray) - 1)]
                    origURL = firstPic.replace(sig,"")
                    sigArray = sig.split(".")
                    num = re.findall("\d+",sigArray[0])[0]
                    origTag = sigArray[0].replace(str(num), "")
                    upNum = int(num)
                    while(1):
                        requestURL = ""
                        countNumStr = ""
                        if (upNum < 10):
                            countNumStr = "0" + str(upNum)
                        else:
                            countNumStr = str(upNum)
                        requestURL = origURL + origTag + countNumStr + ".zip"
                        pic = requests.get(requestURL)
                        print("已完成 " + dir + origTag + countNumStr + ".jpg")
                        with open(dir + origTag + countNumStr + ".jpg", "wb") as file:
                            file.write(pic.content)
                        file.close()
                        if (upNum > totalNum):
                            print("🎉🎉下载完毕🎉🎉\n⚠️⚠️下载总数存在误差，如发现少页，请在SpecialComicId中添加漫画ID⚠️⚠️")
                            exit(0)
                        upNum = upNum + 1;
                elif (str(readRes["code"]) == "721"):
                    print("付费章节，可以破解，下个版本添加破解逻辑")
                else:
                    print(readRes)

            else:
                print("查询失败")

    else:
        print("查询失败")


