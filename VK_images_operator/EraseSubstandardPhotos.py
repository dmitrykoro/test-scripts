import os
import shutil
import cv2
import face_recognition
from pathlib import Path


def erase_photos():
    from DownloadImages import DATASET_PATH as path

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    for path in sorted(Path(path).iterdir()):
        try:
            if path.is_dir():
                os.chdir(path)
                master_image_flag = True

                print(f'Working on {path}')

                for photo in Path(path).iterdir():
                    try:
                        '''image = cv2.imread(str(photo))
                        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        faces = face_cascade.detectMultiScale(
                            gray,
                            scaleFactor=1.2,
                            minNeighbors=5,
                            minSize=(10, 10)
                        )'''

                        # print(faces)
                        current_image = face_recognition.load_image_file(photo)
                        if master_image_flag:
                            #master_encoding = face_recognition.face_encodings(current_image, known_face_locations=faces)[0]
                            master_encoding = face_recognition.face_encodings(current_image)[0]
                            master_image_flag = False
                        else:
                            #encoding = face_recognition.face_encodings(current_image, known_face_locations=faces)[0]
                            encoding = face_recognition.face_encodings(current_image)[0]
                            # encodings.append(encoding)
                            match = face_recognition.compare_faces([master_encoding], encoding)
                            # print(results)
                            res = match[0]
                            if res > 0.6:
                                os.remove(photo)
                                print(f'Removed {photo}')
                    except:
                        continue
        except:
            continue


erase_photos()
