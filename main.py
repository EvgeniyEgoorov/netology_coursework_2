from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import re
from auth import group_auth
from handler import Handler


class User:
    def __init__(self):
        self.search_params = {}

    def prinnt(self):
        print(self.search_params)

    def token_param(self, user_id, session):
        session.new_message(user_id, """
            И самое главное - чтобы запустить поиск, нам нужен твой персональный токен! 
            """)
        text = session.listener()[1]
        if re.match(r'[a-z0-9]*', text):
            token = re.match(r'[a-z0-9]*', text)
            user_auth = token[0]
            session.new_message(user_id, """
                        Начинаем поиск! 
                        """)
            session.search_candidates(user_id, user_auth, self.search_params)
            # self.prinnt()

    def city_param(self, user_id, session):
        session.new_message(user_id, """
            А в каком городе мы ведем поиск?
            """)
        text = session.listener()[1]
        if re.match(r'[a-zа-я]*', text):
            home_town = re.match(r'[a-zа-я]*', text)
            self.search_params['home_town'] = home_town[0]
            self.token_param(user_id, session)

    def age_param(self, user_id, session):
        session.new_message(user_id, """
            Прекрасный выбор! Давай сузим круг поиска, укажи возраст в формате "от" и "до"
            """)
        text = session.listener()[1]
        if re.findall(r'(?<!\d)\d{2}(?!\d)', text):
            age_from = int(re.findall(r'(?<!\d)\d{2}(?!\d)', text)[0])
            age_to = int(re.findall(r'(?<!\d)\d{2}(?!\d)', text)[1])
            self.search_params['age_from'] = age_from
            self.search_params['age_to'] = age_to
            self.city_param(user_id, session)

    def sex_param(self, user_id, session):
        text = session.listener()[1]
        if text == 'старт!':
            session.new_message(user_id, """
                Супер! Сначала определимся кого мы ищем - для этого:
                нажми 1, если ищешь девушку, 2 - если парня, и 0 - если это неважно
                """)
            text = session.listener()[1]
            if re.findall(r'(?<!\d)\d(?!\d)', text):
                self.search_params['sex'] = text
                self.age_param(user_id, session)

    def get_started(self):
        session = Handler(group_auth)
        user_id = session.listener()[0]
        session.new_message(user_id, "Привет! Это VKinder - лучший сервис для знакомств!")
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("Старт!", VkKeyboardColor.PRIMARY)
        session.new_message(user_id, 'Нажми Старт!, чтобы начать поиск!', keyboard)
        self.sex_param(user_id, session)


if __name__ == '__main__':
    user = User()
    user.get_started()
