import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange


class Handler:
    def __init__(self, group_auth):
        self.group_session = vk_api.VkApi(token=group_auth)
        self.longpoll = VkLongPoll(self.group_session)

    def listener(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                client = event.user_id
                text = event.text.lower()
                return client, text

    def new_message(self, user_id, message, keyboard=None):
        params = {
            'user_id': user_id,
            'message': message,
            'random_id': randrange(10 ** 7)
        }
        if keyboard is not None:
            params['keyboard'] = keyboard.get_keyboard()
        else:
            params = params
        self.group_session.method('messages.send', params)

    def search_candidates(self, user_id, user_auth, search_params):
        user_session = vk_api.VkApi(token=user_auth)
        params = {
            'count': 20,
            'fields': 'screen_name',
            'has_photo': 1
        }
        response = user_session.method('users.search', {**search_params, **params})
        items = [item for item in response['items'] if not item['is_closed']]
        for candidate_id in items:
            self.photos_get(user_id, (candidate_id['id']), user_session, user_auth)

    def photos_get(self, user_id, owner_id, user_session, user_auth):
        photos_get_params = {
            'owner_id': owner_id,
            'album_id': 'profile',
            'extended': 1,
            'count': 3
        }
        response = user_session.method('photos.get', {**photos_get_params})
        items = response['items']

        def likes_and_comments_count(item):
            return item['likes']['count'] + item['comments']['count']

        items.sort(key=likes_and_comments_count)
        most_liked_photos = items[-3:]
        for photo in most_liked_photos:
            self.send_photo(user_id, photo['owner_id'], photo['id'], user_auth, user_session)

    def send_photo(self, user_id, owner_id, photo_id, user_auth, user_session):
        attachment = f'photo{owner_id}_{photo_id}_{user_auth}'
        send_photo_params = {
            'user_id': user_id,
            'attachment': attachment,
            'random_id': randrange(10 ** 7)
        }
        user_session.method('messages.send', {**send_photo_params})

