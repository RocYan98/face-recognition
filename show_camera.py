import cv2
import face_recognition
import time
import copy


def start(username):
    # 读取目标图片
    localtion = "dataset/" + username + ".png"
    target = cv2.imread(localtion)
    # 目标encoding
    target_encoding = face_recognition.face_encodings(target)[0]

    # 将目标放入人脸库
    know_encodings = [target_encoding]
    know_names = [username]

    # 打开摄像头
    vc = cv2.VideoCapture(0)

    # 目标是否已经出现
    target_has_appeared = False
    # 目标实际最后一次出现到时间
    last_time = 0
    # 目标出现的总时间
    total_time = 0
    # 记录中目标上一次出现的时间
    appear_time = 0
    # 存放时间
    time_dict = dict()
    time_list = []

    while True:
        # 获取摄像头中的一帧，reg表示是否获取到
        ret, img = vc.read()
        if not ret:
            print("没有获取到视频")
            break

        # 获取图片中人脸到位置
        locations = face_recognition.face_locations(img)
        # 获取图片中所有人脸到encoding
        unknow_encodings = face_recognition.face_encodings(img, locations)

        # 这一帧中目标是否出现
        target_appear = False
        for (top, right, bottom, left), face_encoding in zip(locations, unknow_encodings):
            # 将图片中人脸框起来
            cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 1)
            # 将图片中到人脸与人脸库中进行对比
            matchs = face_recognition.compare_faces(know_encodings, face_encoding)
            name = "unknow"
            for match, know_name in zip(matchs, know_names):
                if match:
                    name = know_name

            if name == username:
                target_appear = True

            # 将寻找到的人脸旁写上相应的姓名
            cv2.putText(img, name, (right, top - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)

        # 如果目标出现，更新最后一次出现的时间
        if target_appear:
            last_time = time.time()

        # 如果目标从消失到出现 或 目标从出现到消失且间隔时间长达5秒以上（防止卡顿或短暂未获取到人脸而重复记录）则记录时间
        if target_has_appeared != target_appear and (target_appear or time.time() - last_time > 5):
            target_has_appeared = target_appear
            last_time = time.time()
            if target_appear:
                print("出现时间:")
                appear_time = time.time()
                time_dict["appear"] = get_time()
            else:
                print("消失时间:")
                total_time += time.time() - appear_time
                time_dict["disappear"] = get_time()
                time_dict["last"] = time.time() - appear_time
                deepcopy = copy.deepcopy(time_dict)
                time_list.append(deepcopy)

            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

        # 显示这一帧的图片
        cv2.imshow("video", img)

        if cv2.waitKey(1) == 27:
            # 释放资源
            vc.release()
            cv2.destroyAllWindows()

            if target_has_appeared:
                print("消失时间:\n" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                total_time += time.time() - appear_time
                time_dict["disappear"] = get_time()
                time_dict["last"] = time.time() - appear_time
                deepcopy = copy.deepcopy(time_dict)
                time_list.append(deepcopy)

            print("本次在线总时长:%d秒" % int(total_time))
            return time_list, int(total_time)


def get_time():
    year = time.localtime().tm_year
    month = time.localtime().tm_mon
    day = time.localtime().tm_mday
    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min
    second = time.localtime().tm_sec

    return str(year) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2) + " " + str(hour).zfill(2) + ":" + str(
        minute).zfill(2) + ":" + str(second).zfill(2)
