from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from knuapp.models import dreem_singwan
from knuapp.models import staff_singwan
from knuapp.models import staff_yesan
from knuapp.models import staff_choen
from knuapp.models import Account
from knuapp.models import Announ

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
welcome = {'type': 'buttons', 'buttons': ['학식보기', "KNUCOIN", "!도움!"]}
main = {'message': {'text': '메인으로 돌아갑니다.\n'},  'keyboard': {'type': 'buttons', 'buttons': ['학식보기', 'KNUCOIN', "!도움!"]} }
sorry = {'message': {'text': '죄송합니다.\n이해하지 못했습니다.\n다시 시도해주세요.'}, 'keyboard': {'type': 'buttons', 'buttons':['메인', "!도움!"]}}
helps = {'message': {'text':'안녕하세요.\n컴퓨터공학부 소프트웨어전공 17학번 문승현입니다.\n이것은 공주대학교 유틸봇입니다.\n업데이트 공지는 홈에서 이루어집니다.\n많은 친구추가와 관심부탁드립니다.\n개발자에게 여자소개시켜주세요.\n버그&아이디어 제보: mhubeen@gmail.com\n감사합니다.'}, "keyboard": { "type": "buttons", "buttons": ["메인","뒤로가기"]}}
haksik = {'message': {'text': '어디 캠퍼스의 학식을 보고 싶으신가요?\n'},  'keyboard': {'type': 'buttons', 'buttons': ['천안캠퍼스', "신관캠퍼스", "예산캠퍼스","메인", "뒤로가기", "!도움!"]} }
call_admin = {'message': {'text': '[ERROR]\n\n알 수 없는 에러가 나타났다!\n\n사용자는 개발자에게 문의를 해주세요!'}, 'keyboard': {'type': 'buttons', 'buttons':['메인', "!도움!"]}}
notfriend = {'message': {'text': '[안내]\n\n공주대학교 봇 서비스를 이용하시려면 먼저 친구추가를 해주세요!!!\n* 만약 친구추가가 되어있어도 안내가 뜬다면 차단하였다가 다시 추가해주세요.'},'keyboard': {'type': 'buttons', 'buttons':['메인', "!도움!"]}}
knucoin_main = {'message': {'text': 'KNUCOIN 서비스에 오신것을 환영합니다.\nKNUCOIN은 하루에 0.1개씩 받을 수 있습니다.\n코인으로 이용할 수  있는 서비스는 이후에 점차 늘려갈 예정입니다.'},'keyboard': {'type': 'buttons', 'buttons':['내코인', "코인 받기", '뒤로가기']}}


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

dreem = dreem_singwan
staff_ch = staff_choen
staff_ye = staff_yesan
staff_si = staff_singwan
Account = Account
Announs = Announ


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
    Account.objects.filter(ids=_ids).update(idx=_idx)

def db_check(self, days):
    try:
        result = self.objects.filter(day=days)[0]
        return result
    except:
        return "X"

def db_insert(self,contents):
    string = strftime("%y.%m.%d", time.localtime())
    self(day=string, content=contents).save()

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

def get_Announ():
        url = {}
        lnk1 = urllib.request.Request("http://www.kongju.ac.kr/lounge/board.jsp?board=student_news&page=0")
        frame = urllib.request.urlopen(lnk1)
        sc = frame.read()
        frame.close()
        cd = BeautifulSoup(sc, "html.parser")
        tb = cd.find("table", class_="content_main_table02").find_all("a", href=True)
        for i, cnt in zip(tb, range(len(tb))):
             url[cnt] = [i['title'], "http://www.kongju.ac.kr/lounge/"+i['href']]
        return json.dump(url)

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
    print("YEEEE")
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where()
    )
    r = http.request('GET', 'https://dormi.kongju.ac.kr/main/contents/food.php?mid=40&k=2')
    print(r)
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
    Announ_ck = db_check(Announs, now)
    #if (dreem_ck == "X"):
    #    dreem_con = get_dreem()
        #db_insert(dreem,dreem_con)
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

@csrf_exempt
def message(request):   
    knucoin_de = {'message': {'text': '[KNUCOIN]\n\n현재 소지하고 있는 갯수는 아래와 같습니다.\n\nKNUCOIN : '},'keyboard': {'type': 'buttons', 'buttons':['메인', '뒤로가기']}}
    knucoin_gi = {'message': {'text': '[KNUCOIN]\n\n코인은 하루에 0.1knc를 지급합니다.\n\n'},'keyboard': {'type': 'buttons', 'buttons':['메인', '뒤로가기']}}
    bob = {'message': {'text': ""}, 'keyboard': {'type': 'buttons', 'buttons': ["메인", "뒤로가기"]}}
    now = strftime("%y.%m.%d", time.localtime())
    message = ((request.body).decode('utf-8'))
    ret_json = json.loads(message)
    strs = ret_json['content']
    ids = ret_json['user_key']

    if (strs == "!도움!"):
        db_update_idx(ids, 1)
        return JsonResponse(helps)
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

    elif(strs == "메인"):
        if(db_get_idx(ids) == 16):
            return JsonResponse(knucoin_main)
        db_update_idx(ids, 0)
        return JsonResponse(main)
    elif(strs == "KNUCOIN"):
        if(db_not_friend(ids) != 'X'):
            db_update_idx(ids, 16)
            return JsonResponse(knucoin_main)
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
    elif(strs == "내코인"):
        val = get_point(ids)
        print(val)
        tmps = knucoin_de['message']['text'] + str(val) + "knc\n"
        knucoin_de['message']['text'] = tmps
        return JsonResponse(knucoin_de)
    elif(strs == "코인 받기"):
        g_val = give_point(ids)
        if(g_val == "X"):
            tmps = knucoin_gi['message']['text'] + "오늘은 받으실 수 없습니다!\n내일 받으시길 바랍니다!"
        else:
            tmps = knucoin_gi['message']['text'] + str(g_val) + "knc를 지급받으셨습니다!!\n"
        knucoin_gi['message']['text'] = tmps
        return JsonResponse(knucoin_gi)


