from flask import Flask, request
import json
import numpy as np

app = Flask(__name__)

f = open('individual_encodings.json')
known_encodings = json.load(f)


@app.route('/', methods=['POST'])
def check_whois():
    min_distance = 1.0

    received_encoding = json.loads(request.get_data())
    received_encoding = [float(s) for s in received_encoding.split() if s != ' ']
    received_encoding = np.array(received_encoding)

    for candidate_person in known_encodings.items():
        candidate_encoding = np.array(candidate_person[1][0])

        face_distance = np.linalg.norm(candidate_encoding - received_encoding)

        print(f'Face distance with {candidate_person[0]} is {face_distance}')

        if face_distance < min_distance:
            person_name = candidate_person[0].split('.')[0]
            min_distance = face_distance

    print(f'This is {person_name}')

    return {'result': 'ok'}


if __name__ == '__main__':
    app.run()
