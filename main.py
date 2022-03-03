import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from auth import group_auth
import handler
import re
import time

vk_session = vk_api.VkApi(token=group_auth)
longpoll = VkLongPoll(vk_session)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if re.match(r'[А-Яа-яA-Za-z]', event.text):
            handler.text_msg(event.user_id,
                             """Вас приветствует VKinder - лучший сервис для знакомств!
                                Начни поиск прямо сейчас! """)
            time.sleep(0.8)
            handler.text_msg(event.user_id, 'Для начала введи диапазон возраста (пример: от 18 до 20):')

            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                    if re.findall(r'\d\d', event.text):
                        age_from = int(re.findall(r'\d\d', event.text)[0])
                        age_to = int(re.findall(r'\d\d', event.text)[1])
                        time.sleep(0.5)
                        handler.text_msg(event.user_id, 'Теперь укажи пол (1-ж, 2-м, 0-любой):')

                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                                if re.findall(r'\d', event.text):
                                    sex = int(re.findall(r'\d', event.text)[0])
                                    time.sleep(0.5)
                                    handler.text_msg(event.user_id, f'Укажи город, в котором ведешь поиск')

                                    for event in longpoll.listen():
                                        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                                            if re.findall(r'[А-Яа-яA-Za-z]', event.text):
                                                hometown = str(re.findall(r'[А-Яа-яA-Za-z]', event.text)[0])
                                                time.sleep(0.5)
                                                handler.text_msg(event.user_id, f'Мы начинаем поиск!')
                                                time.sleep(1)
                                                handler.text_msg(event.user_id, f'Вот кого нам удалось найти для тебя:')
                                                handler.search_candidates(event.user_id, age_from,
                                                                          age_to, sex, hometown)
    continue
