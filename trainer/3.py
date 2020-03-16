
import urllib
from bs4 import BeautifulSoup
url='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential'
data={'appid':'wxecb727e7e5aede73',
      'secret':'a85dfba90937ffb57d20a783888b55f9'}

data=urllib.urlencode(data)
html=urllib.urlopen(url,data)

html=html.read()

html = bytes.decode(html)
content = eval(content)

access_token=html['access_token']
print access_token

