import os
import random
import urllib.request
import vk_api
from Auth import data as auth_data
#from EraseSubstandardProfiles import sort

USERS_COUNT = 9000
MAX_USERS_PER_QUERY = 1000
DATASET_PATH = "/media/dmitry-koro/Data/Polytech/Diplom/VK_DATASET/"


def auth():
    user = auth_data.get("username")
    password = auth_data.get("password")
    vk_session = vk_api.VkApi(user, password)
    vk_session.auth()
    vk = vk_session.get_api()
    return vk


def get_user_ids(vk):
    ids = []
    if USERS_COUNT > MAX_USERS_PER_QUERY:
        for i in range(int(USERS_COUNT / MAX_USERS_PER_QUERY)):
            keyword = random.choice("абвгдежзиёклмнопрстуфхцчшщэюя")
            response = vk.users.search(q=keyword, sort=0, count=MAX_USERS_PER_QUERY, has_photo=1)
            response_items = response.get("items")
            ids += [d['id'] for d in response_items]
    else:
        response = vk.users.search(sort=0, count=USERS_COUNT, has_photo=1)
        response_items = response.get("items")
        ids += [d['id'] for d in response_items]
    return ids


def download_photos(vk, ids):
    for uid in ids:
        try:
            current_uid_profile_photos = vk.photos.get(owner_id=uid, album_id="profile")

        except vk_api.exceptions.ApiError:
            print(f"User {uid} is private, skip")
            continue

        if len(current_uid_profile_photos["items"]) == 1:
            continue

        current_path = os.path.join(DATASET_PATH, str(uid))
        if not os.path.exists(current_path):
            os.makedirs(current_path)
        else:
            print(f"User {uid} already operated")

        for photo in range(len(current_uid_profile_photos["items"])):
            try:
                url = (str(current_uid_profile_photos["items"][photo]["sizes"]
                           [len(current_uid_profile_photos["items"][photo]["sizes"]) - 1]["url"]))

                urllib.request.urlretrieve(url, current_path + '/' +
                                           str(current_uid_profile_photos["items"][photo]['id']) + '.jpg')

            except urllib.error.HTTPError:
                print("Photo not found, skip")


if __name__ == '__main__':
    vk = auth()
    ids = get_user_ids(vk)
    download_photos(vk, ids)
    #sort()
