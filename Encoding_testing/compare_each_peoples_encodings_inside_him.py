import json
import numpy as np


def compare_encodings():
    all_encodings = json.load(open('encodings.json'))

    all_distances = []

    i = 1

    # face_distance = np.linalg.norm(current_user_encoding - compared_user_encoding)

    for user in all_encodings.items():
        current_user_id = user[0]
        current_user_encodings = user[1]

        print(f'Comparing {i}')

        for user_face in current_user_encodings:

            for compared_face in current_user_encodings:

                face_distance = np.linalg.norm(np.array(user_face) - np.array(compared_face))

                if face_distance != 0.0:
                    all_distances.append(face_distance)

        i += 1

    with open("distances.json", "w") as write_file:
        json.dump(all_distances, write_file, indent=4)
    print('Finished')


compare_encodings()
