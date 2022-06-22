import os

import face_recognition
import json

from pathlib import Path


def compute_encodings():
    dirname = input('Enter the full dir path:')

    all_encodings = {

    }

    i = 0
    for user_folder in Path(dirname).iterdir():
        print(f'Operating on user {user_folder}')

        current_user_encodings = []

        for user_image in user_folder.iterdir():


            current_image = face_recognition.load_image_file(user_image)
            try:
                user_encoding = face_recognition.face_encodings(current_image)[0]
            except:
                break

            current_user_encodings.append(user_encoding.tolist())

            user_id = str(user_folder).split('/')[-1]

        all_encodings[f'{user_id}'] = current_user_encodings

        i += 1

    with open("encodings.json", "w") as write_file:
        json.dump(all_encodings, write_file, indent=4)


compute_encodings()
