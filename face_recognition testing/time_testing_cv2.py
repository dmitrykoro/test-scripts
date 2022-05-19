import cv2
from pathlib import Path
import face_recognition
import matplotlib.pyplot as plt
import time
from PIL import Image

print("Enter path to images:")
path = input()

stats = [[], [], []]

for path in sorted(Path(path).iterdir()):
    if path.is_file():
        im = Image.open(path)
        width, height = im.size
        resolution = f'{width}x{height}'
        stats[0].append(resolution)

        current_image = face_recognition.load_image_file(path)
        face_locations = face_recognition.face_locations(current_image, model="hog")

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


        start = time.time()
        image = cv2.imread(str(path), 1)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(10, 10)
        )
        end = time.time()
        localisation_time = end - start
        stats[1].append(localisation_time)

        start = time.time()
        encodings = face_recognition.face_encodings(current_image, known_face_locations=face_locations)
        end = time.time()
        encoding_time = end - start
        stats[2].append(encoding_time)



plt.plot(stats[0], stats[1])
#plt.legend('Localisation time')

plt.plot(stats[0], stats[2])
plt.legend(['Localisation time', 'Encoding time'])

plt.xlabel('Resolution')
plt.ylabel('Time')
plt.title(f'Localisation: CV2, encoding: Dlib')
plt.show()