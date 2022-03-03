from auth import user_auth, group_auth
import vk_api
from random import randrange


user_session = vk_api.VkApi(token=user_auth)
group_session = vk_api.VkApi(token=group_auth)


def search_candidates(user_id, age_from, age_to, sex, hometown):
    search_params = {
        'count': 20,
        'hometown': hometown,
        'sex': sex,
        'age_from': age_from,
        'age_to': age_to,
        'fields': 'screen_name',
        'has_photo': 1
    }
    response = user_session.method('users.search', {**search_params})
    items = [item for item in response['items'] if not item['is_closed']]
    for candidate_id in items:
        photos_get(user_id, (candidate_id['id']))


def photos_get(user_id, owner_id):
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
        send_photo(user_id, photo['owner_id'], photo['id'])


def text_msg(user_id, message):
    text_message_params = {
        'user_id': user_id,
        'message': message,
        'random_id': randrange(10 ** 7)
    }
    group_session.method('messages.send', {**text_message_params})


def send_photo(user_id, owner_id, photo_id):
    attachment = f'photo{owner_id}_{photo_id}_{group_auth}'
    send_photo_params = {
        'user_id': user_id,
        'attachment': attachment,
        'random_id': randrange(10 ** 7)
    }
    group_session.method('messages.send', {**send_photo_params})

