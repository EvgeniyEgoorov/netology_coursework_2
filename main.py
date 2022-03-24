from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import re
from handler import GetMatches, new_message, listener
import db


class User:
    def __init__(self):
        self.search_params = {}

    def token_param(self, user_id):
        new_message(user_id, """
            И самое главное - чтобы запустить поиск, нам нужен твой персональный токен! 
            """)
        text = listener()[1]
        if re.match(r'[a-z0-9]*', text):
            token = re.match(r'[a-z0-9]*', text)
            user_auth = token[0]
            new_message(user_id, """
                        Начинаем поиск! 
                        """)
            seeker = GetMatches(user_auth)
            seeker.search_candidates(user_id, self.search_params)
        else:
            new_message(user_id, "Некорректный ввод!")

    def city_param(self, user_id):
        new_message(user_id, """
            А в каком городе мы ведем поиск?
            """)
        text = listener()[1]
        if re.match(r'[a-zа-я]*', text):
            home_town = re.match(r'[a-zа-я]*', text)
            self.search_params['home_town'] = home_town[0]
            self.token_param(user_id)
        else:
            new_message(user_id, "Некорректный ввод!")

    def age_param(self, user_id):
        new_message(user_id, """
            Прекрасный выбор! Давай сузим круг поиска, укажи возраст в формате "от" и "до"
            """)
        text = listener()[1]
        if re.findall(r'(?<!\d)\d{2}(?!\d)', text):
            age_from = int(re.findall(r'(?<!\d)\d{2}(?!\d)', text)[0])
            age_to = int(re.findall(r'(?<!\d)\d{2}(?!\d)', text)[1])
            self.search_params['age_from'] = age_from
            self.search_params['age_to'] = age_to
            self.city_param(user_id)
        else:
            new_message(user_id, "Некорректный ввод! Укажи возраст в формате 'от' и 'до'")

    def sex_param(self, user_id):
        text = listener()[1]
        if text == 'старт!':
            new_message(user_id, """
                Супер! Сначала определимся кого мы ищем - для этого:
                нажми 1, если ищешь девушку, 2 - если парня, и 0 - если это неважно
                """)
            text = listener()[1]
            if re.findall(r'(?<!\d)\d(?!\d)', text):
                self.search_params['sex'] = text
                self.age_param(user_id)
            else:
                new_message(user_id, "Некорректный ввод! Укажи соответствующий номер")

    def get_started(self):
        user_id = listener()[0]
        new_message(user_id, "Привет! Это VKinder - лучший сервис для знакомств!")
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("Старт!", VkKeyboardColor.PRIMARY)
        new_message(user_id, 'Нажми Старт!, чтобы начать поиск!', keyboard)
        db.db()
        db.user_db(user_id)
        self.sex_param(user_id)


if __name__ == '__main__':
    user = User()
    user.get_started()
