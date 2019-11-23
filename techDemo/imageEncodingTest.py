import base64

with open("filename.jpg", "rb") as imageFile:
    text = base64.b64encode(imageFile.read())
    print(len(text))
    print(text)

fh = open("imageToSave.png", "wb")
fh.write(base64.decodebytes(text))
fh.close()