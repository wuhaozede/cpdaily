import requests
import re
from encrypt import wiseduAES


def login(username, password):
    # 登陆地址
    url = 'https://ids.ahnu.edu.cn/authserver/login?service=https%3A%2F%2Fahnu.campusphere.net%2Fportal%2Flogin'
    
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74'
    }
    
    # 获取cookies
    res = requests.get(url=url, headers=headers)
    cookies = requests.utils.dict_from_cookiejar(res.cookies)

    # 获取隐藏字段
    payload = dict(re.findall(
        r'<input type="hidden" name="(.*?)" value="(.*?)"', res.text))
    salt = dict(re.findall(
        r'<input type="hidden" id="(.*?)" value="(.*?)"', res.text))

    # 填写表单
    payload['username'] = username
    payload['password'] = (wiseduAES(password, salt['pwdDefaultEncryptSalt']))
    res = requests.post(url=url, headers=headers, cookies=cookies,
                        data=payload, allow_redirects=False)
    # 获取重定向地址
    try:
        url = res.headers['Location']
    except KeyError:
        exit('用户名或密码错误')

    # 获取cookies
    res = requests.get(url=url, headers=headers, allow_redirects=False)
    cookies = requests.utils.dict_from_cookiejar(res.cookies)
    
    return cookies


