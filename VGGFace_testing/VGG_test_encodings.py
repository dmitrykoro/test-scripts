from pathlib import Path
from matplotlib import pyplot
from PIL import Image
from numpy import asarray
from scipy.spatial.distance import cosine
from mtcnn.mtcnn import MTCNN
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input



print("Enter path to images:")
path = input()


encodings = []
encoding = []
master_encoding = []
paths = []


def extract_face(path, required_size=(224, 224)):
    # load image from file
    pixels = pyplot.imread(path)
    # create the detector, using default weights
    detector = MTCNN()
    # detect faces in the image
    results = detector.detect_faces(pixels)
    # extract the bounding box from the first face
    x1, y1, width, height = results[0]['box']
    x2, y2 = x1 + width, y1 + height
    # extract the face
    face = pixels[y1:y2, x1:x2]
    # resize pixels to the model size
    image = Image.fromarray(face)
    image = image.resize(required_size)
    face_array = asarray(image)
    #print(f'Finished detecting. Embedding for {path} is:')
    #print(face_array)
    face = face_array

    model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')
    encoding = model.predict(face)
    print(f'Finished detecting. Encoding for {path} is:')
    print(encoding)
    return encoding


i = -1
for path in sorted(Path(path).iterdir()):
    if path.is_file():
        i += 1
        if i == 0:
            print(f'Master image is: {path}')
            #master_image = face_recognition.load_image_file(path)
            #master_encoding = face_recognition.face_encodings(master_image)[0]
            master_encoding = extract_face(path)
            continue

        #current_image = face_recognition.load_image_file(path)
        #encoding = face_recognition.face_encodings(current_image)[0]
        current_encoding = extract_face(path)
        encodings.append(encoding)

        paths.append(path)


print(f'Found {len(encodings)} encodings in {i} images')


for current_encoding, current_path in zip(encodings, paths):
    results = cosine(master_encoding, current_encoding)

    current_path = str(current_path)
    current_path = current_path.split('/')[-1]

    if results[0] <= 0.5:
        print(f'{results} -- OK    ({current_path})')
    else:
        print(f'{results} -- FAIL    ({current_path})')