# coding:utf-8

import cv2
import io
import picamera
import socket
import sys


def image_sender(host, port):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    stream = io.BytesIO()

    with picamera.PiCamera() as cap:

        buff = 1024 * 32

        cap.resolution = (320, 240)

    while True:
        cap.capture(stream, format='jpeg')
        img_cut_list = [stream[i:i + buff]
                        for i in range(0, len(stream), buff)]
        for img_cut_string in img_cut_list:
            udp.sendto(img_cut_string, (host, port))

        if cv2.waitKey(1) == 27:
            break

    udp.close()

if __name__ == "__main__":
    image_sender(sys.argv[1], int(sys.argv[2]))
