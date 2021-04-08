import requests
import json
import uuid
import os
from fill import fillForm
from login import login
from encrypt import desEncrypt


def queryCollectorProcessingList(headers, cookies):
    payload = {"pageNumber": 1, "pageSize": 20}
    url = "https://ahnu.campusphere.net/wec-counselor-collector-apps/stu/collector/queryCollectorProcessingList"

    # 获取问卷wid
    res = requests.post(url=url, headers=headers, cookies=cookies,
                        data=json.dumps(payload))
    data = res.json()
    # 判断问卷提交状态
    if data['datas']['totalSize'] == 0:
        exit('无待提交的问卷')
    if data['datas']['rows'][0]['isHandled'] == 1:
        exit('今日问卷已提交')
    if data['datas']['rows'][0]['isHandled'] == 0:
        wid = data['datas']['rows'][0]['wid']
        return wid


def queryCollectorHistoryList(headers, cookies):
    payload = {"pageNumber": 1, "pageSize": 20}
    url = "https://ahnu.campusphere.net/wec-counselor-collector-apps/stu/collector/queryCollectorHistoryList"
    # 获取历史问卷wid
    res = requests.post(url=url, headers=headers, cookies=cookies,
                        data=json.dumps(payload))
    data = res.json()
    wid = data['datas']['rows'][8]['wid']
    return wid


def detailCollector(wid, headers, cookies):
    payload = {"collectorWid": wid}
    url = "https://ahnu.campusphere.net/wec-counselor-collector-apps/stu/collector/detailCollector"
    res = requests.post(url=url, headers=headers, cookies=cookies,
                        data=json.dumps(payload))
    data = res.json()

    formWid = data['datas']['collector']['formWid']
    schoolTaskWid = data['datas']['collector']['schoolTaskWid']

    return (formWid, schoolTaskWid)

def getFormFields(formWid, collectorWid, headers, cookies):
    payload = {"pageNumber": 1, "pageSize": 20,
               "formWid": formWid, "collectorWid": collectorWid}
    url = "https://ahnu.campusphere.net/wec-counselor-collector-apps/stu/collector/getFormFields"
    res = requests.post(url=url, headers=headers, cookies=cookies,
                        data=json.dumps(payload))
    data = res.json()
    rows = data['datas']['rows']
    

    return rows


def submitForm(username, form, cookies, wid, formWid, schoolTaskWid):
    extension = {
        "systemName": "android",
        "systemVersion": "10",
        "model": "GM1910",
        "deviceId": str(uuid.uuid1()),
        "appVersion": "8.2.18",
        "lon": 4.9E-324,
        "lat": 4.9E-324,
        "userId": username
        }
    headers = {
        "tenantId": "ahnu",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; GM1910 Build/QKQ1.190716.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.152 Mobile Safari/537.36 okhttp/3.12.4",
        "CpdailyStandAlone": "0",
        "extension": "1",
        "Cpdaily-Extension": desEncrypt(json.dumps(extension),'b3L26XNL','\x01\x02\x03\x04\x05\x06\x07\x08'),
        "Content-Type": "application/json; charset=utf-8",
        "Host": "ahnu.campusphere.net",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }
    url = "https://ahnu.campusphere.net/wec-counselor-collector-apps/stu/collector/submitForm"
    payload = {}
    payload['formWid'] = formWid
    payload['address'] = ""
    payload['collectWid'] = wid
    payload['schoolTaskWid'] = schoolTaskWid
    payload['form'] = form
    payload['uaIsCpadaily'] = True
    payload['latitude'] = ""
    payload['longitude'] = ""
    res = requests.post(url=url, headers=headers,
                        cookies=cookies, data=json.dumps(payload))
    data = res.json()
    if data['code'] == "0":
        print('成功提交')
    else:
        print('提交失败')


def main(username, password):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; GM1910 Build/QKQ1.190716.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.152 Mobile Safari/537.36  cpdaily/8.2.18 wisedu/8.2.18",
        "Content-Type": "application/json;charset=UTF-8"
    }
    cookies = login(username, password)

    processingWid = queryCollectorProcessingList(headers, cookies)
    processingFormWid, processingSchoolTaskWid = detailCollector(
        processingWid, headers, cookies)
    r1 = getFormFields(processingFormWid, processingWid, headers, cookies)

    historyWid = queryCollectorHistoryList(headers, cookies)
    historyFormWid, historySchoolTaskWid = detailCollector(
        historyWid, headers, cookies)
    r2 = getFormFields(historyFormWid, historyWid, headers, cookies)

    form = fillForm(r1, r2)

    submitForm(username,form, cookies, processingWid,
               processingFormWid, processingSchoolTaskWid)


if __name__ == '__main__':
    username = os.environ["username"]
    password = os.environ["password"]
    main(username,password)
