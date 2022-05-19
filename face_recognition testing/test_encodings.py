from pathlib import Path
import face_recognition
import matplotlib.pyplot as plt
import cv2

print("Enter path to images:")
path = input()

encodings = []
encoding = []
master_encoding = []
paths = []

i = 0
detected = 0


def get_face_locations_cv2(photo):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    image = cv2.imread(str(photo))
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        image,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(10, 10)
    )
    return faces


for path in sorted(Path(path).iterdir()):
    if path.is_file():
        i += 1

        if path not in paths:
            current_image = face_recognition.load_image_file(path)
            try:
                #faces = get_face_locations_cv2(path)

                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                cv2_image_instance = cv2.imread(path)
                gray = cv2.cvtColor(cv2_image_instance, cv2.COLOR_BGR2GRAY)
                face_locations_cv2 = face_cascade.detectMultiScale(gray, 1.1, 4)
                for x, y, w, h in face_locations_cv2:
                    face_locations_for_face_recognition = [(y, x + w, y + h, x)]

                encoding = face_recognition.face_encodings(current_image, known_face_locations=face_locations_for_face_recognition)[0]
                detected += 1

            except:
                print(f'Did not detected any face in {path}')
                #raise

            encodings.append(encoding)
            paths.append(path)

print(f'Found {detected} encodings in {i} images')

for master_path in paths:
    if str(master_path).split('/')[-1].split('.')[-1] != 'normal':
        continue
    results_for_plot = [[], []]
    master_image = face_recognition.load_image_file(master_path)
    try:
        master_encoding = face_recognition.face_encodings(master_image)[0]
    except:
        continue
    for current_encoding, current_path in zip(encodings, paths):
        results = face_recognition.compare_faces([master_encoding], current_encoding)

        if current_path == master_path:
            continue

        current_path = str(current_path)
        current_path = current_path.split('/')[-1]
        current_path = current_path.split('.')[0]
        current_path = current_path.split('subject')[-1]

        if results[0] < 0.6:
            if results[0] != 0.0:
                results_for_plot[0].append(results[0])
                results_for_plot[1].append(current_path)

        else:
            results_for_plot[0].append(results[0])
            results_for_plot[1].append(current_path)

    master_path = str(master_path)
    master_path = master_path.split('/')[-1]

    plt.scatter(results_for_plot[1], results_for_plot[0], marker='.')
    plt.xlabel('Subject group')
    plt.ylabel('Euclidean distance')
    plt.title(f'Master image is {master_path}. Faces detected: {detected}/{i}')
    plt.show()
