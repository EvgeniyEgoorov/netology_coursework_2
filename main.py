from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import re
from handler import GetMatches, listener
import db


class User:
    def __init__(self):
        self.search_params = {}

    def city_param(self, handler):
        handler.new_message("""
            А в каком городе мы ведем поиск?
            """)
        text = listener()[1]
        if re.match(r'[a-zа-я]*', text):
            hometown = re.match(r'[a-zа-я]*', text)
            self.search_params['hometown'] = hometown[0]
            handler.new_message("Начинаем поиск!")
            handler.search_candidates(self.search_params)
        else:
            handler.new_message('Некорректный ввод!')

    def age_param(self, handler):
        handler.new_message("""
            Прекрасный выбор! Давай сузим круг поиска, укажи возраст в формате "от" и "до"
            """)
        text = listener()[1]
        if re.findall(r'(?<!\d)\d{2}(?!\d)', text):
            age_from = int(re.findall(r'(?<!\d)\d{2}(?!\d)', text)[0])
            age_to = int(re.findall(r'(?<!\d)\d{2}(?!\d)', text)[1])
            self.search_params['age_from'] = age_from
            self.search_params['age_to'] = age_to
            self.city_param(handler)
        else:
            handler.new_message("Некорректный ввод! Укажи возраст в формате 'от' и 'до'")

    def sex_param(self, handler):
        text = listener()[1]
        if text == 'старт!':
            handler.new_message("""
                Супер! Сначала определимся кого мы ищем - для этого:
                нажми 1, если ищешь девушку, 2 - если парня, и 0 - если это неважно
                """)
            text = listener()[1]
            if re.findall(r'(?<!\d)\d(?!\d)', text):
                self.search_params['sex'] = text
                self.age_param(handler)
            else:
                handler.new_message('Некорректный ввод! Укажи соответствующий номер')

    def get_started(self):
        user_id = listener()[0]
        handler = GetMatches(user_id)
        handler.new_message('Привет! Это VKinder - лучший сервис для знакомств!')
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('Старт!', VkKeyboardColor.PRIMARY)
        handler.new_message('Нажми Старт!, чтобы начать поиск!', keyboard)
        db.db()
        db.user_db(user_id)
        self.sex_param(handler)


if __name__ == '__main__':
    user = User()
    user.get_started()
