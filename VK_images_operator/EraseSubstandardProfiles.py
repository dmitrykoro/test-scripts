import os
import shutil
import cv2
from pathlib import Path
from DownloadImages import DATASET_PATH as path


# path = input('Enter path to images: ')

def sort():

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    for path in sorted(Path(path).iterdir()):
        if path.is_dir():
            os.chdir(path)
            total_faces_per_user = 0

            # print(f'Analysing {path}')

            for photo in Path(path).iterdir():
                try:
                    image = cv2.imread(str(photo))
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(
                        gray,
                        scaleFactor=1.2,
                        minNeighbors=5,
                        minSize=(10, 10)
                    )
                    if len(faces) != 1:
                        os.remove(photo)
                        # print(f'Removed {photo}: no faces or to much faces')
                    else:
                        # print(f'[{path}] Detected {len(faces)} faces for image {photo}')
                        total_faces_per_user += len(faces)
                except:
                    continue

            if total_faces_per_user <= 1:
                shutil.rmtree(path)
                print(f'Removed {path}: {total_faces_per_user} faces')


sort()
