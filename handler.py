import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from auth import group_auth, user_auth
import db

group_session = vk_api.VkApi(token=group_auth)
longpoll = VkLongPoll(group_session)


def listener():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            client = event.user_id
            text = event.text.lower()
            return client, text


class GetMatches:
    def __init__(self, user_id):
        self.session = vk_api.VkApi(token=user_auth)
        self.user_id = user_id

    def new_message(self, message, keyboard=None):
        params = {
            'user_id': self.user_id,
            'message': message,
            'random_id': randrange(10 ** 7)
        }
        if keyboard is not None:
            params['keyboard'] = keyboard.get_keyboard()
        else:
            params = params
        group_session.method('messages.send', params)

    def send_photo(self, owner_id, photo_id):
        attachment = f'photo{owner_id}_{photo_id}_{group_auth}'
        send_photo_params = {
            'user_id': self.user_id,
            'attachment': attachment,
            'random_id': randrange(10 ** 7)
        }
        group_session.method('messages.send', {**send_photo_params})

    def get_photos(self, owner_id):
        photos_get_params = {
            'owner_id': owner_id,
            'album_id': 'profile',
            'extended': 1,
            'count': 3
        }
        response = self.session.method('photos.get', {**photos_get_params})
        items = response['items']

        def likes_and_comments_count(item):
            return item['likes']['count'] + item['comments']['count']

        items.sort(key=likes_and_comments_count)
        most_liked_photos = items[-3:]
        self.new_message(f'Ссылка на профиль: vk.com/id{owner_id}')
        for photo in most_liked_photos:
            db.photos_db(photo['owner_id'], photo['sizes'][-1]['url'])
            self.send_photo(photo['owner_id'], photo['id'])

    def search_candidates(self, search_params):
        params = {
            'count': 10,
            'fields': 'screen_name',
            'has_photo': 1
        }
        response = self.session.method('users.search', {**search_params, **params})
        items = [item for item in response['items'] if not item['is_closed']]
        for candidate_id in items:
            db.candidate_db(candidate_id['id'], candidate_id['first_name'], candidate_id['last_name'])
            db.user_to_candidates(self.user_id, candidate_id['id'])
            self.get_photos(candidate_id['id'])
