# coding:utf-8
import cv2
import numpy as np
import socket
import sys


def image_receiver(host, port):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.settimeout(10)
    udp.bind((host, port))

    buff = 1024 * 32

    while True:
        img_string = b""

        img_cut_string, addr = udp.recvfrom(buff)
        img_string += img_cut_string
        while len(img_cut_string) == buff:
            img_cut_string, addr = udp.recvfrom(buff)
            img_string += img_cut_string

        img_narray = np.fromstring(img_string, np.uint8)
        img = cv2.imdecode(img_narray, 1)

        try:
            cv2.imshow("Receive", img)
        except cv2.error:
            pass

        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()
    udp.close()


if __name__ == "__main__":
    image_receiver(sys.argv[1], int(sys.argv[2]))
