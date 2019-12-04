# BioPay
## Biometric Based Payment Solution
##### Developed for CMU CS15-122 Term Project (F19)

BioPay is a biometrically (facial recognition) authenticated payment and transaction platform. The intention of this platform is to replace credit card/NFC/cash transactions with ones requiring just your face to complete the purchase. There are two sides to this app. The first is for merchants who will be able to input all of their products into the app, generate a cart for their customers, and actually complete the transaction using the biometric authentication of the customer. This would essensially replace a POS (Point of Sale) system found in most stores. The other side is for consumers. Using the app they will be able to see their transaction history, add/remove payment methods/ and enroll their face which will be used for the facial recognion authentication.

## Requirements
- Python 3.3+
- macOS or Linux
- Windows might work, but not officially supported

## Instalation
To install the program files you must git clone with recursive mode on, in order to fully copy the dlib library. You cannot download the zip file or normally clone the repo, the program will not work.
```
git clone --recurse-submodules https://github.com/prithupareek/BioPay.git
```

You must install these dependencies in order for the program to work:
- face_recognition
- OpenCV
- PyMySQL

##### To install face_recognition
First, build and install the dlib python extensions.
```
$ cd dlib
$ python3 setup.py install
```

Then install the face_recognition dependency
```
$ pip3 install face_recognition
```

##### To install OpenCV
```
$ pip3 install opencv-python==4.1.0.25
```

##### To install PyMySQL
```
$ python3 -m pip install PyMySQL
```

## Executable App
If you would like to simply run an executable version of the program without the need to install any libaries, download the zip archive from the link below.

[Download Link](https://drive.google.com/file/d/1qrrcq-4-W5-I0TNFZ7GIBBw5jMffe4Jq/view?usp=sharing)

To run the app open the file entitled main, inside the main folder.

As of now, this app only works on MacOS.