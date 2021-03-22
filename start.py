from vk_api.tools import VkTools
from vk_api import ApiError
import vk_api
import re
import time
import sqlite3
import threading

conn = sqlite3.connect("qw1.db")
cursor = conn.cursor()

api_token = ""
vk = vk_api.VkApi(token=api_token)
vk_api = vk.get_api()
tools = VkTools(vk)


def start(group_id, timeObyazSlowa, timeWarnSlowa, times):
    wall = tools.get_all('wall.get', 100, {'owner_id': -group_id, 'filter': 'suggests'})
    print(wall)
    for post in wall['items']:
        if any([re.search(weat, str(post['text']).lower()) for weat in timeObyazSlowa]) and not any(
                [re.search(weat, str(post['text']).lower()) for weat in timeWarnSlowa]):
            print('id post: ' + str(post['id']) + " text: " + str(post['text']))
            if any([re.search(weat, str(post['text']).lower()) for weat in permcode]):
                permid.append(str(post['id']))
            else:
                posts.append(str(post['id']))

    for addPermPost in wall['items']:
        if any([re.search(weat, str(addPermPost['id'])) for weat in permid]):
            photos = ''
            if 'attachments' in addPermPost:
                for attach in addPermPost['attachments']:
                    photos = photos + 'photo-' + str(group_id) + '_' + str(
                        attach[attach['type']]['id']) + ","
                for code in permcode:
                    s = str(addPermPost['text']).replace(code, "")
                vk.method('wall.post',
                          {'owner_id': -group_id, 'post_id': int(addPermPost['id']), 'from_group': 0,
                           'signed': 1, 'message': s, 'attachments': photos})
            else:
                for code in permcode:
                    s = str(addPermPost['text']).replace(code, "")
                vk.method('wall.post',
                          {'owner_id': -group_id, 'post_id': int(addPermPost['id']), 'from_group': 0,
                           'signed': 1, 'message': s})
            time.sleep(int(times))
    for addPost in wall['items']:
        if any([re.search(weat, str(addPost['id'])) for weat in posts]):
            photos = ""
            if 'attachments' in addPost:
                for attach in addPost['attachments']:
                    photos = photos + 'photo-' + str(group_id) + '_' + str(attach['photo']['id']) + ","
                vk.method('wall.post',
                          {'owner_id': -group_id, 'post_id': int(addPost['id']), 'from_group': 0,
                           'signed': 1, 'attachments': photos})
            else:
                vk.method('wall.post',
                          {'owner_id': -group_id, 'post_id': int(addPost['id']), 'from_group': 0,
                           'signed': 1})
            time.sleep(int(times))
    timeObyazSlowa.clear()
    timeWarnSlowa.clear()
    print("Процесс завершен")



while True:
    try:
        attachments = []
        group_id = ""
        api_token = ""
        tokens = []
        ids = []
        warnSlowa = []
        obyazSlowa = []
        truepost = []
        minTimePostSec = []
        permcode = ["dit12"]
        permid = []
        posts = []

        select_ids = "SELECT id FROM vktb1"
        select_warnSlowa = "SELECT warnSlowa FROM vktb1"
        select_obyazSlowa = "SELECT obyazSlowa FROM vktb1"
        select_minTimePostSec = "SELECT minTimePostSec FROM vktb1"
        cursor.execute(select_ids)
        result = cursor.fetchall()
        for row in result:
            row = str(row)
            row = row.replace('(', '')
            row = row.replace(',)', '')
            ids.append(row.lower())
        cursor.execute(select_warnSlowa)
        result = cursor.fetchall()
        for row in result:
            row = str(row)
            row = row.replace('(\'', '')
            row = row.replace('\',)', '')
            warnSlowa.append(row.lower())
        cursor.execute(select_obyazSlowa)
        result = cursor.fetchall()
        for row in result:
            row = str(row)
            row = row.replace('(\'', '')
            row = row.replace('\',)', '')
            obyazSlowa.append(row.lower())
        cursor.execute(select_minTimePostSec)
        result = cursor.fetchall()
        for row in result:
            row = str(row)
            row = row.replace('(', '')
            row = row.replace(',)', '')
            minTimePostSec.append(row.lower())

        for count in range(len(ids)):
            group_id = int(ids[count])
            if minTimePostSec[count] == '' or minTimePostSec[count] == '0':
                times = 0
            else:
                times = int(minTimePostSec[count])
            timeWarnSlowa = warnSlowa[count].lower().split()
            timeObyazSlowa = obyazSlowa[count].lower().split()
            t = threading.Thread(target=start, args=(group_id, timeObyazSlowa, timeWarnSlowa, times,))
            t.start()

        warnSlowa.clear()
        obyazSlowa.clear()
        ids.clear()
        minTimePostSec.clear()
    except ApiError as e:
        print(e)
    except EOFError as e:
        print(e)
    except OSError as e:
        print(e)
    time.sleep(3600)
    print("Новый цикл")
