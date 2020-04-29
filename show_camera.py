import cv2
import face_recognition

yqp = cv2.imread("dataset/yqp.JPG")
yqp_encoding = face_recognition.face_encodings(yqp)[0]
wrf = cv2.imread("dataset/wrf.jpg")
wrf_encoding = face_recognition.face_encodings(wrf)[0]

know_encodings = [yqp_encoding, wrf_encoding]
names = ["yqp", "wrf"]

vc = cv2.VideoCapture(0)
while True:
    ret, img = vc.read()
    if not ret:
        print("没有获取到视频")
        break

    locations = face_recognition.face_locations(img)
    unknow_encodings = face_recognition.face_encodings(img, locations)

    for (top, right, bottom, left), face_encoding in zip(locations, unknow_encodings):
        cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 1)
        matchs = face_recognition.compare_faces(know_encodings, face_encoding)
        name = "unknow"
        for match, know_name in zip(matchs, names):
            if match:
                name = know_name
        cv2.putText(img, name, (right, top - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)

    cv2.imshow("me", img)

    if cv2.waitKey(1) != -1:
        vc.release()
        cv2.destroyAllWindows()
        break