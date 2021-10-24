import base64
import pickle
import random

import cv2
import face_recognition
import string


def image2vector(image):
    print(image)
    if validate_face(image):
        print("face_detected")
        loaded_image = face_recognition.load_image_file(image)
        loaded_image_encoding = face_recognition.face_encodings(loaded_image)[0]
        return loaded_image_encoding
    return None


def image2vector_list(image):
    if validate_face(image):
        print("face_detected")
        loaded_image = face_recognition.load_image_file(image)
        loaded_image_encoding = face_recognition.face_encodings(loaded_image)[0]
        return list(loaded_image_encoding)
    return []


def compare_images(known_face_encodings, unknown_face_encoding):
    result = face_recognition.compare_faces(known_face_encodings, unknown_face_encoding)
    print(result)
    return result


def vector2bytes(vector):
    np_bytes = pickle.dumps(vector)
    np_base64 = base64.b64encode(np_bytes)
    return np_base64


def bytes2vector(bytes2convert):
    np_bytes = base64.b64decode(bytes2convert)
    np_array = pickle.loads(np_bytes)
    return np_array


def validate_face(image):
    cascade_path = "haar_cascades/haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)
    img = cv2.imread(str(image))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
    )

    return len(faces) == 1


def generate_file_name():
    sym_array = string.ascii_lowercase + string.ascii_uppercase
    return ''.join([random.choice(sym_array) for i in range(0, 15)])
