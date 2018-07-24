# coding:utf-8

import cv2
import socket
import sys


def image_sender(host, port):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 420)

    buff = 1024 * 32

    if not cap.isOpened():
        print("Camera Is Not Opened.")
        sys.exit()

    ret, frame = cap.read()

    while ret:
        cv2.imshow("Send", frame)
        img_string = cv2.imencode(".jpg", frame)[1].tostring()
        img_cut_list = [img_string[i:i + buff]
                        for i in range(0, len(img_string), buff)]
        for img_cut_string in img_cut_list:
            udp.sendto(img_cut_string, (host, port))

        if cv2.waitKey(1) == 27:
            break

        ret, frame = cap.read()

    cv2.destroyAllWindows()
    cap.release()
    udp.close()


if __name__ == "__main__":
    image_sender(sys.argv[1], int(sys.argv[2]))
