from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from knu.models import dreem_singwan
from knu.models import staff_singwan
from knu.models import staff_yesan
from knu.models import staff_choen
from knu.models import Account

import json 
import urllib
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time
from time import gmtime, strftime
import re

#메세지
welcome = {'type': 'buttons', 'buttons': ['학식보기', "!도움!"]}
main = {'message': {'text': '메인으로 돌아갑니다.\n'},  'keyboard': {'type': 'buttons', 'buttons': ['학식보기', "!도움!"]} }
sorry = {'message': {'text': '죄송합니다.\n이해하지 못했습니다.\n다시 시도해주세요.'}, 'keyboard': {'type': 'buttons', 'buttons':['메인', "!도움!"]}}
helps = {'message': {'text':'안녕하세요.\n컴퓨터공학부 소프트웨어전공 17학번 문승현입니다.\n이것은 공주대학교 유틸봇입니다.\n업데이트 공지는 홈에서 이루어집니다.\n많은 친구추가와 관심부탁드립니다.\n개발자에게 여자소개시켜주세요.\n버그&아이디어 제보: mhubeen@gmail.com\n감사합니다.'}, "keyboard": { "type": "buttons", "buttons": ["메인","뒤로가기"]}}
haksik = {'message': {'text': '어디 캠퍼스의 학식을 보고 싶으신가요?\n'},  'keyboard': {'type': 'buttons', 'buttons': ['천안캠퍼스', "신관캠퍼스", "예산캠퍼스","메인", "뒤로가기", "!도움!"]} }
call_admin = {'message': {'text': '[ERROR]\n\n알 수 없는 에러가 나타났다!\n\n사용자는 개발자에게 문의를 해주세요!'}, 'keyboard': {'type': 'buttons', 'buttons':['메인', "!도움!"]}}
notfriend = {'message': {'text': '[안내]\n\n공주대학교 봇 서비스를 이용하시려면 먼저 친구추가를 해주세요!!!\n* 만약 친구추가가 되어있어도 안내가 뜬다면 차단하였다가 다시 추가해주세요.'},'keyboard': {'type': 'buttons', 'buttons':['메인', "!도움!"]}}



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

bob = {'message': {'text': ""}, 'keyboard': {'type': 'buttons', 'buttons': ["메인", "뒤로가기"]}}

week = ['월', '화', '수', '목', '금', '토', '일']

dreem = dreem_singwan
staff_ch = staff_choen
staff_ye = staff_yesan
staff_si = staff_singwan

def DisplayMyPage(request):
    return render(request, 'html/index.html')

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

def get_staff_si():
    try:
        lnk1 = urllib.request.Request("http://www.kongju.ac.kr/service/food_view_w.jsp?code=C001&idx=1")
        frame = urllib.request.urlopen(lnk1)
        sc = frame.read().decode('cp949', 'ignore')
        frame.close()
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
        lnk1 = urllib.request.Request("http://www.kongju.ac.kr/service/food_view_w.jsp?code=C002&idx=21")
        frame = urllib.request.urlopen(lnk1)
        sc = frame.read().decode('cp949', 'ignore')
        frame.close()
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
        lnk1 = urllib.request.Request("http://www.kongju.ac.kr/service/food_view_w.jsp?code=C003&idx=22")
        frame = urllib.request.urlopen(lnk1)
        sc = frame.read().decode('cp949', 'ignore')
        frame.close()
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
    data = urllib.parse.urlencode({'year': now.tm_year, 'month': now.tm_mon, 'day': now.tm_mday, 'x':'20', 'y':'20'})
    lnk1 = urllib.request.Request("https://dormi.kongju.ac.kr/main/contents/food.php?mid=40&k=2", data=data.encode("utf-8"))
    frame = urllib.request.urlopen(lnk1)
    sc = frame.read().decode("utf-8")
    frame.close()
    cd = BeautifulSoup(sc, "html.parser")
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

@csrf_exempt
def friend_add(request):
    if(request.method == 'POST'):
        ids = json.loads((request.body).decode('utf-8'))
        db_add_friend(ids['user_key'])
    return JsonResponse(call_admin)

def keyboard(request):
    now = time.strftime("%y.%m.%d", time.localtime())
    dreem_ck = db_check(dreem ,now)
    staff_ch_ck = db_check(staff_ch, now)
    staff_ye_ck = db_check(staff_ye, now)
    staff_si_ck = db_check(staff_si, now)
    if (dreem_ck == "X"):
    	dreem_con = get_dreem()
    	db_insert(dreem,dreem_con)
    if (staff_ch_ck == "X"):
        staff_ch_con = get_staff_ch()
        db_insert(staff_ch, staff_ch_con)
    if (staff_ye_ck == "X"):
        staff_ye_con  = get_staff_ye()
        db_insert(staff_ye, staff_ye_con)
    if (staff_si_ck == "X"):
        staff_si_con = get_staff_si()
        db_insert(staff_si, staff_si_con)

    return JsonResponse(welcome)

@csrf_exempt
def message(request):
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
    elif(strs == "메인"):
        db_update_idx(ids, 0)
        return JsonResponse(main)
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
        bob['message']['text'] = db_get(dreem, now)
        return JsonResponse(bob)

