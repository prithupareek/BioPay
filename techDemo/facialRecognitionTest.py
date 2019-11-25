import face_recognition
import os
import numpy as np

# From https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html
def removeTempFiles(path, suffix='.DS_Store'):
    if path.endswith(suffix):
        print(f'Removing file: {path}')
        os.remove(path)
    elif os.path.isdir(path):
        for filename in os.listdir(path):
            removeTempFiles(path + '/' + filename, suffix)

# sets the picture to compare everything else to
picture_of_me = face_recognition.load_image_file("known-faces/Prithu.jpg")
my_face_encoding_1 = face_recognition.face_encodings(picture_of_me)[0]
# my_face_encoding = ast.literal_eval(my_face_encoding_string)
my_face_encoding_string = my_face_encoding_1.tostring()
print(my_face_encoding_1)
my_face_encoding = np.fromstring(my_face_encoding_string, dtype=float)

directory = "unknown-faces"

# removes DS_Store files
removeTempFiles(directory)

# loops through the test pictures
for file in os.listdir(directory):
    print(file)

    unknownFace = face_recognition.load_image_file(directory + '/' + file)
    unknownFaceEncoding = face_recognition.face_encodings(unknownFace)[0]
    # print(unknownFaceEncoding)

    results = face_recognition.compare_faces([my_face_encoding], unknownFaceEncoding)


    if results[0] == True:
        print("It is a picture of me!")
    else:
        print("It is not a picture of me!")





