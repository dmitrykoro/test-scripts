import os
import cv2
import face_recognition
from pathlib import Path
import matplotlib.pyplot as plt

plot_data = [[], []]


def get_face_locations_cv2(photo):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    image = cv2.imread(str(photo))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(10, 10)
    )
    return faces


def get_face_encoding_dlib(photo, known_locations):
    image = face_recognition.load_image_file(photo)
    try:
        #encoding = face_recognition.face_encodings(image, known_face_locations=known_locations)[0] #locations by cv2
        encoding = face_recognition.face_encodings(image)[0]  #locations by dlib
    except:
        print(f'No faces in {photo}, pass')
        return [-1]

    return encoding


def calculate_and_compare(photo, main_master_encoding):
    current_face_locations = get_face_locations_cv2(photo)
    current_encoding = get_face_encoding_dlib(photo, current_face_locations)
    if current_encoding[0] == -1:
        return

    compare_result = face_recognition.compare_faces([main_master_encoding], current_encoding)

    photo = str(photo)
    photo = photo.split('/')[-2]

    global plot_data
    plot_data[0].append(compare_result[0])
    plot_data[1].append(photo)
    # print(plot_data)


def test_dataset():
    from DownloadImages import DATASET_PATH as path
    master_dataset_path = input('Enter path to images that will be compared to other: ')

    main_master_is_operated = False
    for photo in Path(master_dataset_path).iterdir():
        if not main_master_is_operated:
            main_master_is_operated = True
            try:
                faces = get_face_locations_cv2(photo)
                main_master_encoding = get_face_encoding_dlib(photo, faces)
            except:
                print(f'Some error occurred, passing current photo {photo}')
        else:
            calculate_and_compare(photo, main_master_encoding)

    i = 0
    for path in sorted(Path(path).iterdir()):
        if i == 1000:
            break

        try:
            if path.is_dir():
                if path == master_dataset_path:
                    continue
                os.chdir(path)
                i += 1
                for photo in Path(path).iterdir():
                    try:
                        calculate_and_compare(photo, main_master_encoding)
                    except:
                        print(f'Some error occurred, passing current photo {photo}')
        # except:

        except:
            continue


def print_plot():
    plt.scatter(plot_data[1], plot_data[0], marker='.')
    plt.xlabel('Subject group')
    plt.ylabel('Euclidean distance')
    #plt.rcParams.update({'font.size': 11})
    plt.xticks(rotation=90)
    plt.show()


test_dataset()
print_plot()
