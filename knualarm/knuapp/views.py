from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from knuapp.models import dreem_singwan
from knuapp.models import staff_singwan
from knuapp.models import staff_yesan
from knuapp.models import staff_choen
from knuapp.models import Account
from knuapp.models import Announ_kongju
from knuapp.models import Announ_brain
from knuapp.models import Announ_sabum
from knuapp.models import Announ_insa
#from knuapp.models import Announ_natural
from knuapp.models import Announ_indu
from knuapp.models import Announ_cnh
from knuapp.models import Announ_art
from knuapp.models import Announ_control
from knuapp.models import Announ_cse
from knuapp.models import Announ_mech
from knuapp.models import Announ_civil
from knuapp.models import Announ_archi
from knuapp.models import Announ_archeng
from knuapp.models import Announ_ame
from knuapp.models import Announ_ie
from knuapp.models import Announ_optical


import json 
import certifi
import urllib3
import urllib
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time
from time import gmtime, strftime
import datetime
import re

#메세지
welcome = {'type': 'buttons', 'buttons': ['학식보기',"공지사항", "내정보", "!도움!"]}
main = {'message': {'text': '메인으로 돌아갑니다.\n'},  'keyboard': {'type': 'buttons', 'buttons': ['학식보기', '공지사항', "내정보", "!도움!"]} }
sorry = {'message': {'text': '죄송합니다.\n이해하지 못했습니다.\n다시 시도해주세요.'}, 'keyboard': {'type': 'buttons', 'buttons':['메인', "!도움!"]}}
helps = {'message': {'text':'안녕하세요.\n컴퓨터공학부 소프트웨어전공 17학번 문승현입니다.\n이것은 공주대학교 유틸봇입니다.\n업데이트 공지는 홈에서 이루어집니다.\n많은 친구추가와 관심부탁드립니다.\n개발자에게 여자소개시켜주세요.\n버그&아이디어 제보: mhubeen@gmail.com\n감사합니다.'}, "keyboard": { "type": "buttons", "buttons": ["메인","뒤로가기"]}}
haksik = {'message': {'text': '어디 캠퍼스의 학식을 보고 싶으신가요?\n'},  'keyboard': {'type': 'buttons', 'buttons': ['천안캠퍼스', "신관캠퍼스", "예산캠퍼스","메인", "뒤로가기", "!도움!"]} }
call_admin = {'message': {'text': '[ERROR]\n\n알 수 없는 에러가 나타났다!\n\n사용자는 개발자에게 문의를 해주세요!'}, 'keyboard': {'type': 'buttons', 'buttons':['메인', "!도움!"]}}
notfriend = {'message': {'text': '[안내]\n\n공주대학교 봇 서비스를 이용하시려면 먼저 친구추가를 해주세요!!!\n* 만약 친구추가가 되어있어도 안내가 뜬다면 차단하였다가 다시 추가해주세요.'},'keyboard': {'type': 'buttons', 'buttons':['메인', "!도움!"]}}
knucoin_main = {'message': {'text': 'KNUCOIN 서비스에 오신것을 환영합니다.\nKNUCOIN은 하루에 0.1개씩 받을 수 있습니다.\n코인으로 이용할 수  있는 서비스는 이후에 점차 늘려갈 예정입니다.'},'keyboard': {'type': 'buttons', 'buttons':['내코인', "코인 받기", '뒤로가기']}}
mypage = {'message': {'text': '[내정보] \n\n현재는 KNUCOIN 조회만 가능합니다.\n'},'keyboard': {'type': 'buttons', 'buttons':['KNUCOIN', '뒤로가기']}}
notics = {'message': {'text': '공주대학교 공지사항을 쉽게 볼 수 있는 서비스입니다.\n\n최근에 올라온 공지사항을 보여드리며 링크를 직접 들어가셔서 보시면 됩니다.\n많은 이용 바랍니다.\n'},'keyboard': {'type': 'buttons', 'buttons':['학생소식', '공과대학','사범대학', '인문사회과학대학', '산업과학대학', '간호보건대학', '예술대학',  '뒤로가기']}}
notics_value = {'message': {'text': ''},'keyboard': {'type': 'buttons', 'buttons':['메인', '뒤로가기']}}
notics_brain = {'message': {'text': '[공과대학]\n\n공과대학의 공지사항과 공과대학에 소속되있는 학부 및 학과의 공지사항을 조회하실 수 있습니다.\n공지사항을 보시고 싶은 곳을 선택해주세요.\n'},'keyboard': {'type': 'buttons', 'buttons':['공과대학', '컴퓨터공학부', '제어계측공학전공', '기계자동차공학부', '건설환경공학부', '건축학부', '건축공학부', '신소재공학부', '산업시스템공학과', '광공학과', '뒤로가기']}}
#학식 페이지
cheonan = {
    'message': {'text': '[공주대학교 천안캠퍼스]\n\n* 평일\n- 조식: 07:40 ~ 09:00\n- 중식: 11:30 ~ 13:30\n- 석식: 17:40 ~ 19:00\n\n* 주말 및 공휴일\n- 조식: 08:00 ~ 09:00\n- 중식: 12:00 ~ 13:00\n- 석식: 18:00 ~ 19:00\n\n어디 식당의 식단을 보시겠습니까?'},
    'keyboard': {'type': 'buttons', 'buttons': ['생활관 식당', "학생 식당", "직원 식당","메인", "뒤로가기"]}
}
singwan = {
    'message': {'text': '[공주대학교 신관캠퍼스]\n\n* 평일\n- 조식: 07:30 ~ 08:30\n- 중식: 11:30 ~ 13:30\n- 석식: 17:30 ~ 19:00\n\n* 주말 및 공휴일\n- 조식: 07:30 ~ 08:30\n- 중식: 12:00 ~ 13:00\n- 석식: 18:00 ~ 19:00\n\n어디 식당의 식단을 보시겠습니까?'},
    'keyboard': {'type': 'buttons', 'buttons': ['생활관 식당', "학생 식당", "직원 식당","메인", "뒤로가기"]}
}

yesan = { 
    'message': {'text': '[공주대학교 예산캠퍼스]\n\n* 평일\n- 조식: 08:00 ~ 09:00\n- 중식: 11:40 ~ 13:30\n- 석식: 17:40 ~ 19:00\n\n* 주말 및 공휴일\n- 조식: 08:00 ~ 09:00\n- 중식: 12:00 ~ 13:00\n- 석식: 18:00 ~ 19:00\n\n어디 식당의 식단을 보시겠습니까?'},
    'keyboard': {'type': 'buttons', 'buttons': ["학생 식당", "직원 식당", "메인", "뒤로가기"]}
}

singwan_dormi = {'message': {'text': '[공주대학교 신관캠퍼스 기숙사]\n\n어디 기숙사의 식단을 보시겠습니까?'},  'keyboard': {'type': 'buttons', 'buttons': ["은행사/비전", "드림하우스", "메인"]} }

alert = {'message': {'text': "현재 구현이 되지 않은 상태입니다. 죄송합니다. 빠른 시간안에 개발을 마치도록 노력하겠습니다."}, 'keyboard': {'type': 'buttons', 'buttons': ["메인"]}}


week = ['월', '화', '수', '목', '금', '토', '일']

# DB선언
dreem = dreem_singwan
staff_ch = staff_choen
staff_ye = staff_yesan
staff_si = staff_singwan
Account = Account
Announs_kongju = Announ_kongju
Announs_brain = Announ_brain
Announs_sabum = Announ_sabum
Announs_insa = Announ_insa
#Announs_natural = Announ_natural
Announs_indu = Announ_indu
Announs_cnh = Announ_cnh
Announs_art = Announ_art
Announs_control = Announ_control
Announs_cse = Announ_cse
Announs_mech = Announ_mech
Announs_civil = Announ_civil
Announs_archi = Announ_archi
Announs_archeng = Announ_archeng
Announs_ame = Announ_ame
Announs_ie = Announ_ie
Announs_optical = Announ_optical


def db_get(self, days):
    try:
        result = self.objects.filter(day=days)[0].content
        return result
    except:
        return "X"

def db_add_friend(_ids):
    try:
        Account.objects.get(ids=_ids).idx
    except:
        Account(ids=_ids).save()

def db_not_friend(_ids):
    try:
        Account.objects.get(ids=_ids).idx
    except:
        return "X"

def db_get_idx(_ids):
    return Account.objects.get(ids=_ids).idx

def db_update_idx(_ids, _idx):
	try:
		Account.objects.filter(ids=_ids).update(idx=_idx)
	except:
		return "X"
def db_check(self, days):
    try:
        result = self.objects.filter(day=days)[0]
        return result
    except:
        return "X"

def db_insert(self,contents):
	try:
		string = strftime("%y.%m.%d", time.localtime())
		self(day=string, content=contents).save()
	except:
		return "X"

def db_get_Lasted(_ids):
    return Account.objects.get(ids=_ids).lasted

def get_point(_ids):
    return Account.objects.get(ids=_ids).point

def give_point(_ids):
    now = datetime.datetime.now()
    s_Lasted = now.strftime("%y-%m-%d")
    u_Lasted = db_get_Lasted(_ids)
    user_time = datetime.datetime.strptime(u_Lasted, '%y-%m-%d')
    serv_time = datetime.datetime.strptime(s_Lasted, '%y-%m-%d')
    val = serv_time - user_time
    point = Account.objects.get(ids=_ids).point
    gives = (0.1*val.days)
    point += gives
    Account.objects.filter(ids=_ids).update(point=point)
    Account.objects.filter(ids=_ids).update(lasted=s_Lasted)
    if(val.days == 0):
        return "X"
    else:
        return gives

def get_kongju_Announ():
    url = {}
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://www.kongju.ac.kr/lounge/board.jsp?board=student_news&page=0')
    sc =  r.data.decode('cp949', 'ignore')
    cd = BeautifulSoup(sc, "html.parser")
    tb = cd.find("table", class_="content_main_table02").find_all("a", href=True)
    for i, cnt in zip(tb, range(len(tb))):
        if(i['title'] != ""):
            url[cnt] = [i['title'], "http://www.kongju.ac.kr/lounge/"+i['href']]

    return json.dumps(url)

def get_brain_Announ():
    url = {}
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://brain.kongju.ac.kr/brain/cop/bbs/selectBoardList.do?bbsId=BBSMSTR_000000000001')
    sc =  r.data.decode('utf-8')
    cd = BeautifulSoup(sc, "html.parser")
    tb = cd.find("div", class_="courses").find_all("a", href=True)
    for i, cnt in zip(tb, range(len(tb))):
        if(i.text != ""):
            tmp =  i['onclick'].split("fn_egov_inqire_notice(")[1].split(");")[0].replace("'","").replace(" ", "")
            tmp = tmp.split(',')
            url_tmp = "http://brain.kongju.ac.kr/brain/cop/bbs/selectBoardArticle.do?bbsId=" + tmp[1] +"&nttId=" + tmp[0]
            url[cnt] = [i.text , url_tmp]

    return json.dumps(url)

def get_sabum_Announ():
    url = {}
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://sabum.kongju.ac.kr/custo/list.asp?bbs_code=7')
    sc =  r.data.decode('cp949', 'ignore')
    cd = BeautifulSoup(sc, "html.parser")
    tb = cd.find("table", {"id":"bbs_list_tbl"}).find_all("a", href=True)
    for i, cnt in zip(tb, range(len(tb))):
        if(i.text != ""):
            tmp = i['onclick'].split("viewGo(")[1].split(",")[0]
            url_tmp = "http://sabum.kongju.ac.kr/custo/view.asp?idx="+ tmp +"&page=1&bbs_code=7"
            url[cnt] = [i.text , url_tmp]

    return json.dumps(url)

def get_insa_Announ():
    url = {}
    http = urllib3.PoolManager()
    r = http.request('GET', 'https://insa.kongju.ac.kr/main/board/list.action?q=518da08fa3d7eab65226f7de6f82ae4f1be5aadc235d7f9e817ad3dea247a499')
    sc =  r.data.decode('utf-8')
    cd = BeautifulSoup(sc, "html.parser")
    tb = cd.find("table", class_="body-list-board").find_all("a", href=True)
    for i, cnt in zip(tb, range(len(tb))):
        if(i.text != ""):
            url[cnt] = [i.text, "https://insa.kongju.ac.kr" + i['href']]
    return json.dumps(url)

def get_natural_Announ():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    url = {}
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://natural.kongju.ac.kr/news', headers={'User-Agent':'Mozilla/5.0'})
    sc = r.data.decode('utf-8')
    cd = BeautifulSoup(sc, "html.parser")
    tb = cd.find("tbody").find_all("a", href=True)
    for i, cnt in zip(tb, range(len(tb))):
        if(i.text != ""):
            url[cnt] = [i.text, i['href']]
    return url

def get_indu_Announ():
    url = {}
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://indu.kongju.ac.kr/board.do?paramBean.key=65&paramBean.mainGroupKey=1&boardBean.boardMngKey=1')
    sc = r.data.decode('utf-8')
    cd = BeautifulSoup(sc, "html.parser")
    tb = cd.find_all("span")
    for i, cnt in zip(tb, range(len(tb))):
        if(i.text != ""):
            tmp = i['onclick'].split(', ')[1].split(')')[0]
            url_tmp = "http://indu.kongju.ac.kr/board.do?org.apache.struts.taglib.html.TOKEN=17e8cdfe30d15523c996ee4028c725f3&boardBean.boardKey=" + tmp + "&boardBean.boardMngKey=1&paramBean.key=65&paramBean.homepageKey=0&paramBean.mainGroupKey=1&paramBean.page=0&action=view&boardBean.passwd=&paramBean.searchType=subject&paramBean.searchWord="
            url[cnt] = [i.text, url_tmp]
    return json.dumps(url)

def get_cnh_Announ():
    url = {}
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://cnh.kongju.ac.kr/sub03/service_01_list.asp')
    sc = r.data.decode('cp949', 'ignore')
    cd = BeautifulSoup(sc, "html.parser")
    tb = cd.find("div", class_="cont_body").find_all("a", href=True)
    for i, cnt in zip(tb, range(len(tb))):
        if(i.text != ""):
            url[cnt] = [i.text, "http://cnh.kongju.ac.kr/sub03/" + i['href']]
    return json.dumps(url)

def get_art_Announ():
    url = {}
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://art.kongju.ac.kr/sub03/sub01_01.jsp?menuNo=3&subNo=1')
    sc = r.data.decode('utf-8')
    cd = BeautifulSoup(sc, "html.parser")
    tb = cd.find("div", class_="board_list").find_all("a", href=True)
    for i, cnt in zip(tb, range(len(tb))):
        if(i.text != ""):
            url[cnt] = [ i.text, "http://art.kongju.ac.kr/sub03" +i['href'].replace(".","")]

    return json.dumps(url)

def get_control_Announ(): # 제어계측공학전공
    url = {}
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://control.kongju.ac.kr/Service/board/BoardList.aspx?categ=g1')
    sc = r.data.decode('utf-8')
    cd = BeautifulSoup(sc, "html.parser")
    tb = cd.find_all("tr")
    for i, cnt in zip(tb, range(len(tb))):
        tmp = i.find("a", href=True)
        if(tmp != None):
            if(tmp.text != ""):
                url[cnt] = [tmp.text.strip(), "http://control.kongju.ac.kr/Service/board/BoardItem.aspx?categ=g1&page=1&bidx=" + tmp['onclick'].split("goItem('")[1].split("')")[0]]
    return json.dumps(url)

def get_cse_Announ(): # 컴퓨터공학부
    url = {}
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://cse.kongju.ac.kr/community/notice.asp')
    sc = r.data.decode('utf-8')
    cd = BeautifulSoup(sc, "html.parser")
    tb = cd.find("table", class_="lmcGeneralList").find_all("a", href=True)
    for i, cnt in zip(tb, range(len(tb))):
        if(i.text != ""):
            url[cnt] = [i.text.strip(), "http://cse.kongju.ac.kr" + i['href']]
    return json.dumps(url)

def get_mech_Announ(): #기계자동차공학부
    url = {}
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://mech.kongju.ac.kr/community/community01_notice.asp?lmCode=notice')
    sc = r.data.decode('utf-8')
    cd = BeautifulSoup(sc, "html.parser")
    tb = cd.find("table", class_="lmcGeneralList").find_all("a", href=True)
    for i, cnt in zip(tb, range(len(tb))):
        if(i.text != ""):
            url[cnt] = [i.text.strip(), "http://mech.kongju.ac.kr" + i['href']]

    return json.dumps(url)


def get_civil_Announ(): #건설환경공학부
    url = {}
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://civil.kongju.ac.kr/community/community01_notice.asp')
    sc = r.data.decode('utf-8')
    cd = BeautifulSoup(sc, "html.parser")
    tb = cd.find("table", class_="lmcGeneralList").find_all("a", href=True)
    for i, cnt in zip(tb, range(len(tb))):
        if(i.text != ""):
            url[cnt] = [i.text.strip(), "http://civil.kongju.ac.kr" + i['href']]

    return json.dumps(url)

def get_archi_Announ(): #건축학부
    url = {}
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://archi.kongju.ac.kr/notice/list_hi.asp')
    sc = r.data
    cd = BeautifulSoup(sc, "html.parser")
    tb = cd.find("section", {"id":"content"}).find_all("a", href=True)
    for i, cnt in zip(tb, range(len(tb))):
        tmp_href = i['href']
        if(tmp_href.find('download') > 0):
            if(i.text != ""):
                url[cnt] = [i.text.strip(), "http://archi.kongju.ac.kr/notice/view_hi.asp?idx="+ tmp_href.split("view_send('")[1].split("')")[0] +"&search=&find=&gotopage=1&keyword="]
    return json.dumps(url)

def get_archeng_Announ(): #건축공학부
    url = {}
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://archeng.kongju.ac.kr/notice/list_hi.asp')
    sc = r.data
    cd = BeautifulSoup(sc, "html.parser")
    tb = cd.find("table", class_="b_txt").find_all("a", href=True)
    for i, cnt in zip(tb, range(len(tb))):
        tmp_href = i['href']
        if(tmp_href.find('download') > 0):
            if(i.text != ""):
                url[cnt] = [i.text.strip(), "http://archeng.kongju.ac.kr/notice/view_hi.asp?idx=" + tmp_href.split("view_send('")[1].split("')")[0] + "&search=&find=&gotopage=1&keyword="]

    return json.dumps(url)

def get_ame_Announ():
    url = {}
    http = urllib3.PoolManager()
    r = http.request('GET','http://ame.kongju.ac.kr/community/notice.asp')
    sc = r.data
    cd = BeautifulSoup(sc, "html.parser")
    tb = cd.find("table", class_="lmcGeneralList").find_all("a", href=True)
    for i, cnt in zip(tb, range(len(tb))):
        if(i.text != ""):
            url[cnt] = [i.text.strip(), "http://ame.kongju.ac.kr" + i['href']]
    return json.dumps(url)

def get_ie_Announ():
    url = {}
    http = urllib3.PoolManager()
    r = http.request('GET','http://ie.kongju.ac.kr/index.php?mid=board_lhSN77')
    sc = r.data
    cd = BeautifulSoup(sc, "html.parser")
    tb = cd.find("table").find_all("a", href=True)
    for i, cnt in zip(tb, range(len(tb))):
        tmp_href = i['href']
        if(tmp_href.find('document_srl') > 0):
            if(i.text != ""):
                url[cnt] = [i.text.strip(), "http://ie.kongju.ac.kr/" + tmp_href]

    return json.dumps(url)

def get_optical_Announ():
    url = {}
    http = urllib3.PoolManager()
    r = http.request('GET','http://optical.kongju.ac.kr/sub5_4.php')
    sc = r.data
    cd = BeautifulSoup(sc, "html.parser")
    tb = cd.find("table", class_="ezsboard_td").find_all("a", class_="ezsboard", href=True)
    for cnt in  range(1, len(tb), 3):
        url[cnt] = [tb[cnt].text.strip(), "http://optical.kongju.ac.kr" + tb[cnt]['href']]

    return json.dumps(url)

# 학식
def get_staff_si():
    try:
        http = urllib3.PoolManager()
        r = http.request('GET', 'http://www.kongju.ac.kr/service/food_view_w.jsp?code=C001&idx=1')
        sc =  r.data.decode('cp949', 'ignore')
        cd = BeautifulSoup(sc, "html.parser")
        today = cd.find("td", class_="toady")
        for br in today.find_all("br"):
            br.replace_with("\n")
        if(today.getText() == ""):
            today = "\n[중식]\n오늘은 운영하지 않습니다."
        else:
            today = "\n[중식]\n" + today.getText()
    except:
        today = "\n[중식]\n오늘은 운영하지 않습니다."

    return today

def get_staff_ch():
    try:
        http = urllib3.PoolManager()
        r = http.request('GET', 'http://www.kongju.ac.kr/service/food_view_w.jsp?code=C002&idx=1')
        sc =  r.data.decode('cp949', 'ignore')
        cd = BeautifulSoup(sc, "html.parser")
        today = cd.find("td", class_="toady")
        for br in today.find_all("br"):
            br.replace_with("\n")
        if(today.getText() == ""):
            today = "\n[중식]\n오늘은 운영하지 않습니다."
        else:
            today = "\n[중식]\n" + today.getText()
    except:
        today = "\n[중식]\n오늘은 운영하지 않습니다."

    return today

def get_staff_ye():
    try:
        http = urllib3.PoolManager()
        r = http.request('GET', 'http://www.kongju.ac.kr/service/food_view_w.jsp?code=C003&idx=1')
        sc = r.data.decode('cp949', 'ignore')
        cd = BeautifulSoup(sc, "html.parser")
        today = cd.find("td", class_="toady")
        for br in today.find_all("br"):
            br.replace_with("\n")

        if(today.getText() == ""):
            today = "\n[중식]\n오늘은 운영하지 않습니다."
        else:
            today = "\n[중식]\n" + today.getText()
    except:
        today = "\n[중식]\n오늘은 운영하지 않습니다."

    return today

def get_dreem():
    now = time.localtime()
    bobname = ["\n[조식]\n", "\n[중식]\n", "\n[석식]\n"]
    clear = []
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where()
    )
    r = http.request('GET', 'https://dormi.kongju.ac.kr/main/contents/food.php?mid=40&k=2')
    """
    morning = cd.find('div', attrs={'id': 'breakfast'}).find("div")
    morning = morning.getText().replace("(", "").replace(" ", "").split(",")
    lunch = cd.find('div', attrs={'id': 'lunch'}).find("div")
    lunch = lunch.getText().replace("(", "").replace(" ", "").split(",")
    dinner = cd.find('div', attrs={'id': 'diner'}).find("div")
    dinner = dinner.getText().replace("(", "").replace(" ", "").split(",")
    bobs = [morning, lunch, dinner]
    for i in bobs:
        clear.append(i)
        ret = "[드림 하우스]\n"
        
    for i in range(3):
        ret += bobname[i]
        for b in clear[i]:
            ret += b + "\n"
    return ret
    """

@csrf_exempt
def friend_add(request):
    if(request.method == 'POST'):
        ids = json.loads((request.body).decode('utf-8'))
        db_add_friend(ids['user_key'])
    return JsonResponse(call_admin)



def keyboard(request):
	now = time.strftime("%y.%m.%d", time.localtime())
    #dreem_ck = db_check(dreem ,now)
	staff_ch_ck = db_check(staff_ch, now)
	staff_ye_ck = db_check(staff_ye, now)
	staff_si_ck = db_check(staff_si, now)
	Announ_kongju_ck = db_check(Announs_kongju, now)
	Announ_sabum_ck = db_check(Announs_sabum, now)
	Announ_insa_ck = db_check(Announs_insa, now)
	#Announ_natural_ck = db_check(Announs_natural, now)
	Announ_brain_ck = db_check(Announs_brain,now)
	Announ_indu_ck = db_check(Announs_indu, now)
	Announ_cnh_ck = db_check(Announs_cnh, now)
	Announ_art_ck = db_check(Announs_art, now)
    #if (dreem_ck == "X"):
    #    dreem_con = get_dreem()
	
        #db_insert(dreem,dreem_con)
	if (Announ_kongju_ck == "X"):
		Announ_kongju_con = get_kongju_Announ()
		db_insert(Announs_kongju, Announ_kongju_con)
	if (Announ_sabum_ck == "X"):
		Announ_sabum_con = get_sabum_Announ()
		db_insert(Announs_sabum, Announ_sabum_con)
	if (Announ_insa_ck == "X"):
		Announ_insa_con = get_insa_Announ()
		db_insert(Announs_insa, Announ_insa_con)
	if (Announ_brain_ck == "X"):
		Announ_brain_con = get_brain_Announ()
		db_insert(Announs_brain, Announ_brain_con)
	#if (Announ_natural_ck == "X"):
	#	Announ_natural_con = get_natural_Announ()
	#	db_insert(Announs_natural, Announ_natural_con)
	if (Announ_indu_ck == "X"):
		Announ_indu_con = get_indu_Announ()
		db_insert(Announs_indu, Announ_indu_con)
	if (Announ_cnh_ck == "X"):
		Announ_cnh_con = get_cnh_Announ()
		db_insert(Announs_cnh, Announ_cnh_con)
	if (Announ_art_ck == "X"):
		Announ_art_con = get_art_Announ()
		db_insert(Announs_art, Announ_art_con)
	if (staff_ye_ck == "X"):
		staff_ye_con  = get_staff_ye()
		db_insert(staff_ye, staff_ye_con)
	if (staff_ch_ck == "X"):
		staff_ch_con = get_staff_ch()
		db_insert(staff_ch, staff_ch_con)
	if (staff_si_ck == "X"):
		staff_si_con = get_staff_si()
		db_insert(staff_si, staff_si_con)
	return JsonResponse(welcome)

def announToTitle(v):
	ret = []
	js = json.loads(v)
	for i in js:
		ret.append(js[i][0].strip())
	return ret

def announToURL(self, strs):
	now = strftime("%y.%m.%d", time.localtime())
	dic = db_get(self,now)
	js = json.loads(dic)
	for i in js:
		if(js[i][0].strip() == strs):
			return js[i][1]
	return "X"

@csrf_exempt
def message(request):   
	announ_kongju_view = {'message': {'text': '[학생소식]\n\n학생소식을 선택하셨습니다.\n학생소식에 올라온 공지사항을 보여드리겠습니다.'},'keyboard': {'type': 'buttons', 'buttons':[]}}
	announ_brain_view = {'message': {'text': '[공과대학]\n\n공과대학을 선택하셨습니다.\n공과대학에 올라온 공지사항을 보여드리겠습니다.'},'keyboard': {'type': 'buttons',     'buttons':[]}}
	announ_sabum_view = {'message': {'text': '[사범대학]\n\n사범대학을 선택하셨습니다.\n사범대학에 올라온 공지사항을 보여드리겠습니다.'},'keyboard': {'type': 'buttons',     'buttons':[]}}
	announ_insa_view = {'message': {'text': '[인문사회과학대학]\n\n인문사회과학대학을 선택하셨습니다.\n인문사회과학대학에 올라온 공지사항을 보여드리겠습니다.'},'keyboard': {'type': 'buttons',     'buttons':[]}}
	announ_natural_view = {'message': {'text': '[자연과학대학]\n\n자연과학대학을 선택하셨습니다.\n자연과학대학에 올라온 공지사항을 보여드리겠습니다.'},'keyboard': {'type': 'buttons',     'buttons':[]}}
	announ_indu_view = {'message': {'text': '[산업과학대학]\n\n산업과학대학을 선택하셨습니다.\n산업과학대학에 올라온 공지사항을 보여드리겠습니다.'},'keyboard': {'type': 'buttons',     'buttons':[]}}
	announ_cnh_view = {'message': {'text': '[간호보건대학]\n\n간호보건대학을 선택하셨습니다.\n간호보건대학에 올라온 공지사항을 보여드리겠습니다.'},'keyboard': {'type': 'buttons',     'buttons':[]}}
	announ_art_view = {'message': {'text': '[예술대학]\n\n예술대학을 선택하셨습니다.\n예술대학에 올라온 공지사항을 보여드리겠습니다.'},'keyboard': {'type': 'buttons',     'buttons':[]}}

	knucoin_de = {'message': {'text': '[KNUCOIN]\n\n현재 소지하고 있는 갯수는 아래와 같습니다.\n\nKNUCOIN : '},'keyboard': {'type': 'buttons', 'buttons':['메인', '뒤로가기']}}
	knucoin_gi = {'message': {'text': '[KNUCOIN]\n\n코인은 하루에 0.1knc를 지급합니다.\n\n'},'keyboard': {'type': 'buttons', 'buttons':['메인', '뒤로가기']}}
	bob = {'message': {'text': ""}, 'keyboard': {'type': 'buttons', 'buttons': ["메인", "뒤로가기"]}}
	now = strftime("%y.%m.%d", time.localtime())
	message = ((request.body).decode('utf-8'))
	ret_json = json.loads(message)
	strs = ret_json['content']	
	ids = ret_json['user_key']
	types = ret_json['type']
	
	if (strs == "!도움!"):
		db_update_idx(ids, 1)	
		return JsonResponse(helps)

#뒤로가기
	elif (strs == "뒤로가기"):
		if(db_get_idx(ids) == 1):
			db_update_idx(ids, 0)
			return JsonResponse(main)
		if(db_get_idx(ids) == 2):
			db_update_idx(ids, 0)
			return JsonResponse(main)
		if(db_get_idx(ids) == 3):
			db_update_idx(ids, 0)
			return JsonResponse(main)
		if(db_get_idx(ids) == 4):
			db_update_idx(ids, 3)
			return JsonResponse(cheonan)
		if(db_get_idx(ids) == 5):
			db_update_idx(ids, 3)
			return JsonResponse(cheonan)		
		if(db_get_idx(ids) == 6):
			db_update_idx(ids, 3)
			return JsonResponse(cheonan)
		if(db_get_idx(ids) == 7):	
			db_update_idx(ids, 0)
			return JsonResponse(main)		
		if(db_get_idx(ids) == 8):
			db_update_idx(ids, 7)
			return JsonResponse(singwan)
		if(db_get_idx(ids) == 9):
			db_update_idx(ids, 7)		
			return JsonResponse(singwan)
		if(db_get_idx(ids) == 10):
			db_update_idx(ids, 7)
			return JsonResponse(singwan)
		if(db_get_idx(ids) == 11):		
			db_update_idx(ids, 10)
			return JsonResponse(singwan_dormi)
		if(db_get_idx(ids) == 12):
			db_update_idx(ids, 10)
			return JsonResponse(singwan_dormi)
		if(db_get_idx(ids) == 13):
			db_update_idx(ids, 0)
			return JsonResponse(main)
		if(db_get_idx(ids) == 14):
			db_update_idx(ids, 13)
			return JsonResponse(yesan)
		if(db_get_idx(ids) == 15):
			db_update_idx(ids, 13)
			return JsonResponse(yesan)
		if(db_get_idx(ids) == 16):
			db_update_idx(ids, 0)
			return JsonResponse(main)
		if(db_get_idx(ids) == 17):
			db_update_idx(ids, 16)
			return JsonResponse(mypage)
		if(db_get_idx(ids) == 18):
			db_update_idx(ids, 0)
			return JsonResponse(main)
		if(db_get_idx(ids) == 19):
			db_update_idx(ids, 18)
			return JsonResponse(notics)
		if(db_get_idx(ids) == 20):
			db_update_idx(ids, 18)
			return JsonResponse(notics)
		if(db_get_idx(ids) == 21):
			db_update_idx(ids, 18)
			return JsonResponse(notics)
		if(db_get_idx(ids) == 22):
			db_update_idx(ids, 18)
			return JsonResponse(notics)
		if(db_get_idx(ids) == 23):
			db_update_idx(ids, 18)
			return JsonResponse(notics)
		if(db_get_idx(ids) == 24):
			db_update_idx(ids, 18)
			return JsonResponse(notics)
		if(db_get_idx(ids) == 25):
			db_update_idx(ids, 18)
			return JsonResponse(notics)
		if(db_get_idx(ids) == 26):
			db_update_idx(ids, 18)
			return JsonResponse(notics)


	elif(strs == "메인"):
		if(db_get_idx(ids) == 16):
			return JsonResponse(knucoin_main)
		db_update_idx(ids, 0)
		return JsonResponse(main)	
	elif(strs == "내정보"):
		if(db_not_friend(ids) != 'X'):
			db_update_idx(ids, 16)
			return JsonResponse(mypage)
		else:		
			return JsonResponse(notfriend)
	elif(strs == "학식보기"):
		if(db_not_friend(ids) != 'X'):
			db_update_idx(ids, 2)
			return JsonResponse(haksik)
		else:
			return JsonResponse(notfriend)
	elif(strs == "천안캠퍼스"):
		db_update_idx(ids, 3)
		return JsonResponse(cheonan)
	elif(strs == "신관캠퍼스"):
		db_update_idx(ids, 7)
		return JsonResponse(singwan)
	elif(strs == "예산캠퍼스"):
		db_update_idx(ids, 13)
		return JsonResponse(yesan)
	elif(strs == "생활관 식당"):
		if(db_get_idx(ids) == 7):	
			db_update_idx(ids, 10)
			return JsonResponse(singwan_dormi)
		return JsonResponse(alert)
	elif(strs == "직원 식당"):
		if(db_get_idx(ids) == 3):
			db_update_idx(ids, 5)
			bob['message']['text'] = db_get(staff_ch, now)	
			return JsonResponse(bob)	
		if(db_get_idx(ids) == 7):
			db_update_idx(ids, 9)
			bob['message']['text'] = db_get(staff_si, now)
			return JsonResponse(bob)
		if(db_get_idx(ids) == 13):
			db_update_idx(ids, 15)
			bob['message']['text'] = db_get(staff_ye, now)
			return JsonResponse(bob)
	elif(strs == "학생 식당"):
		return JsonResponse(alert)
	elif(strs == "은행사/비전"):
		db_update_idx(ids, 11)
		return JsonResponse(alert)
	elif(strs == "드림하우스"):
		db_update_idx(ids, 12)
        #bob['message']['text'] = db_get(dreem, now)
		return JsonResponse(alert)
	elif(strs == "KNUCOIN"):
		if(db_get_idx(ids) == 16):
			db_update_idx(ids, 17)
			return JsonResponse(knucoin_main)
		return JsonResponse(call_admin)
	elif(strs == "내코인"):
		if(db_get_idx(ids) == 17):
			val = get_point(ids)
			tmps = knucoin_de['message']['text'] + str(val) + "knc\n"
			knucoin_de['message']['text'] = tmps
			return JsonResponse(knucoin_de)
		return JsonResponse(call_admin)	
	elif(strs == "코인 받기"):
		if(db_get_idx(ids) == 17):
			g_val = give_point(ids)
			if(g_val == "X"):
				tmps = knucoin_gi['message']['text'] + "오늘은 받으실 수 없습니다!\n내일 받으시길 바랍니다!"
			else:
				tmps = knucoin_gi['message']['text'] + str(g_val) + "knc를 지급받으셨습니다!!\n"
			knucoin_gi['message']['text'] = tmps
			return JsonResponse(knucoin_gi)
		return JsonResponse(alert)

	elif(strs == "공지사항"):
		db_update_idx(ids, 18)
		return JsonResponse(notics)
	elif(strs == "학생소식"):
		if(db_get_idx(ids) == 18):
			db_update_idx(ids, 19)
			dic = db_get(Announs_kongju,now)
			title = announToTitle(dic)
			announ_kongju_view['keyboard']['buttons'] = title
			return JsonResponse(announ_kongju_view)
		return JsonResponse(call_admin)
	elif(strs == "공과대학"):
		if(db_get_idx(ids) == 18):
			db_update_idx(ids, 20)
			dic = db_get(Announs_brain , now)
			title = announToTitle(dic)
			announ_kongju_view['keyboard']['buttons'] = title
			return JsonResponse(announ_kongju_view)
		return JsonResponse(call_admin)
	elif(strs == "사범대학"):
		if(db_get_idx(ids) == 18):
			db_update_idx(ids,21)
			dic = db_get(Announs_sabum , now)
			title = announToTitle(dic)
			announ_sabum_view['keyboard']['buttons'] = title
			return JsonResponse(announ_sabum_view)
		return JsonResponse(call_admin)
	elif(strs == "인문사회과학대학"):
		if(db_get_idx(ids) == 18):
			db_update_idx(ids,22)
			dic = db_get(Announs_insa , now)
			title = announToTitle(dic)
			announ_insa_view['keyboard']['buttons'] = title
			return JsonResponse(announ_insa_view)
		return JsonResponse(call_admin)
# '학생소식', '공과대학','사범대학', '인문사회과학대학', '자연과학대학', '산업과학대학', '간호보건대학', '예술>    대학'
	#elif(strs == "자연과학대학"):
	#	if(db_get_idx(ids) == 18):
	#		db_update_idx(ids,23)
	#		dic = db_get(Announs_natural , now)
	#		title = announToTitle(dic)
	#		announ_natural_view['keyboard']['buttons'] = title
	#		return JsonResponse(announ_natural_view)
	#	return JsonResponse(call_admin)
	elif(strs == "산업과학대학"):
		if(db_get_idx(ids) == 18):
			db_update_idx(ids,24)
			dic = db_get(Announs_indu , now)
			title = announToTitle(dic)
			announ_indu_view['keyboard']['buttons'] = title
			return JsonResponse(announ_indu_view)
		return JsonResponse(call_admin)
	elif(strs == "간호보건대학"):
		if(db_get_idx(ids) == 18):
			db_update_idx(ids, 25)
			dic = db_get(Announs_cnh , now)
			title = announToTitle(dic)
			announ_cnh_view['keyboard']['buttons'] = title
			return JsonResponse(announ_cnh_view)
		return JsonResponse(call_admin)
	elif(strs == "예술대학"):
		if(db_get_idx(ids) == 18):
			db_update_idx(ids, 26)
			dic = db_get(Announs_art , now)
			title = announToTitle(dic)
			announ_art_view['keyboard']['buttons'] = title
			return JsonResponse(announ_art_view)
		return JsonResponse(call_admin)
	elif(db_get_idx(ids) == 19):
		g_url = announToURL(Announs_kongju,strs)
		if(g_url == "X"):
			return JsonResponse(call_admin)
		else:
			tmp = "[" + strs + "]\n공지사항의 링크는 아래에 적혀있습니다.\nurl : " + g_url 
			notics_value['message']['text'] = tmp
			return JsonResponse(notics_value)
	
	elif(db_get_idx(ids) == 20):
		g_url = announToURL(Announs_brain,strs)
		if(g_url == "X"):
			return JsonResponse(call_admin)
		else:
			tmp = "[" + strs + "]\n공지사항의 링크는 아래에 적혀있습니다.\nurl : " + g_url 
			notics_value['message']['text'] = tmp
			return JsonResponse(notics_value)
	elif(db_get_idx(ids) == 21):
		g_url = announToURL(Announs_sabum,strs)
		if(g_url == "X"):
			return JsonResponse(call_admin)
		else:
			tmp = "[" + strs + "]\n공지사항의 링크는 아래에 적혀있습니다.\nurl : " + g_url 
			notics_value['message']['text'] = tmp
			return JsonResponse(notics_value)
	elif(db_get_idx(ids) == 22):
		g_url = announToURL(Announs_insa,strs)
		if(g_url == "X"):
			return JsonResponse(call_admin)
		else:
			tmp = "[" + strs + "]\n공지사항의 링크는 아래에 적혀있습니다.\nurl : " + g_url 
			notics_value['message']['text'] = tmp
			return JsonResponse(notics_value)
	#elif(db_get_idx(ids) == 23):
	#	g_url = announToURL(Announs_natural,strs)
	#	if(g_url == "X"):
	#		return JsonResponse(call_admin)
	#	else:
	#		tmp = "[" + strs + "]\n공지사항의 링크는 아래에 적혀있습니다.\nurl : " + g_url 
	#		notics_value['message']['text'] = tmp
	#		return JsonResponse(notics_value)
	elif(db_get_idx(ids) == 24):
		g_url = announToURL(Announs_indu,strs)
		if(g_url == "X"):
			return JsonResponse(call_admin)
		else:
			tmp = "[" + strs + "]\n공지사항의 링크는 아래에 적혀있습니다.\nurl : " + g_url 
			notics_value['message']['text'] = tmp
			return JsonResponse(notics_value)

	elif(db_get_idx(ids) == 25):
		g_url = announToURL(Announs_cnh,strs)
		if(g_url == "X"):
			return JsonResponse(call_admin)
		else:
			tmp = "[" + strs + "]\n공지사항의 링크는 아래에 적혀있습니다.\nurl : " + g_url 
			notics_value['message']['text'] = tmp
			return JsonResponse(notics_value)

	elif(db_get_idx(ids) == 26):
		g_url = announToURL(Announs_art,strs)
		if(g_url == "X"):
			return JsonResponse(call_admin)
		else:
			tmp = "[" + strs + "]\n공지사항의 링크는 아래에 적혀있습니다.\nurl : " + g_url 
			notics_value['message']['text'] = tmp
			return JsonResponse(notics_value)
	else:
		return JsonResponse(sorry)
