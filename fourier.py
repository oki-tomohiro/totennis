# -*- coding: utf-8 -*-
import cv2
import numpy as np
#sx, sy�͐��̎n�܂�̈ʒu
sx, sy = 0, 0
img = cv2.imread("mt_fuji.jpg",cv2.IMREAD_GRAYSCALE)

locate = np.zeros(img.shape) #���g���̈�̉摜�ƏƂ炵���킹��.

im1 = np.fft.fft2(img)
im2 = np.fft.fftshift(im1) #�t�[���G�ϊ���
im3 = np.abs(im2)
frequency = np.log(im3) #�U���X�y�N�g��
frequency = (frequency-frequency.min()) / (frequency.max()-frequency.min()) #0����1�֐��K�����Ă���

IM1 = np.zeros(img.shape,dtype=np.complex128) #�e�_�ł̎Ȗ͗l.complex�^�ɂ���
IM2 = np.zeros(img.shape,dtype=np.complex128) #����p
IMM1 = np.zeros(img.shape,dtype=np.complex128) #���v�̎Ȗ͗l.complex�^�ɂ���
IMM2 = np.zeros(img.shape,dtype=np.complex128) #����p
only=np.zeros(img.shape,dtype=np.float64) #float�^.���̓_����(only)�ł̋�ԗ̈�ł̔g�`
recon=np.zeros(img.shape,dtype=np.float64) #float�^.�č\��(reconfigure)������ԗ̈�ł̉摜

h,w = img.shape
#�}�E�X�̑��삪����Ƃ��Ă΂��֐�
def callback(event, x, y, flags, param):
    global sx, sy,locate,IM1,IM2,IMM1,IMM2,im2,IMMM1,IMMM2,only,recon,h,w
    #�}�E�X�̍��{�^�����N���b�N���ꂽ�Ƃ�
    if event == cv2.EVENT_LBUTTONDOWN:
        IM1[sy,sx] = 0 #���̓_�����ł̋�ԗ̈�ł̔g�`��\�����邽��,�O�̔g�`�̗v�f���Ȃ����Ă���.
        if ((0 <= y and y <= h-1) and (0 <= x and x <= w-1)): #�J�[�\���ʒu����ʓ��ɂ��邩
            sy, sx = y, x
            locate[y,x] = 1
            IM1[y,x] = im2[y,x]
            IMM1[y,x] = im2[y,x]
            IM2 = IM1 #�R�s�[
            IMM2 = IMM1 #�R�s�[
            IM2 = np.fft.fftshift(IM2)
            IMM2 = np.fft.fftshift(IMM2)
            IM2 = np.fft.ifft2(IM2)
            IMM2 = np.fft.ifft2(IMM2)
            only=IM2.real
            recon=IMM2.real
            only=(only-only.min()) / (only.max()-only.min()) #���K��
            recon=(recon-recon.min()) / (recon.max()-recon.min()) #���K��
    #�}�E�X�̍��{�^�����N���b�N����Ă��āA�}�E�X���������Ƃ�
    if flags == cv2.EVENT_FLAG_LBUTTON and event == cv2.EVENT_MOUSEMOVE:
        IM1[sy,sx] = 0 #���̓_�����ł̋�ԗ̈�ł̔g�`��\�����邽��,�O�̔g�`�̗v�f���Ȃ����Ă���.
        if ((0 <= y and y <= h-1) and (0 <= x and x <= w-1)): #�J�[�\���ʒu����ʓ��ɂ��邩
            sy, sx = y, x
            locate[y,x] = 1
            IM1[y,x] = im2[y,x]
            IMM1[y,x] = im2[y,x]
            IM2 = IM1 #�R�s�[
            IMM2 = IMM1 #�R�s�[
            IM2 = np.fft.fftshift(IM2)
            IMM2 = np.fft.fftshift(IMM2)
            IM2 = np.fft.ifft2(IM2)
            IMM2 = np.fft.ifft2(IMM2)
            only=IM2.real
            recon=IMM2.real
            only=(only-only.min()) / (only.max()-only.min()) #���K��
            recon=(recon-recon.min()) / (recon.max()-recon.min()) #���K��

#�E�B���h�E�̖��O��ݒ�
cv2.namedWindow("locate", cv2.WINDOW_NORMAL)
#�R�[���o�b�N�֐��̐ݒ�
cv2.setMouseCallback("locate", callback)
while(1):
    cv2.imshow("img", img)
    cv2.imshow("frequency",frequency)
    cv2.imshow("locate",locate)
    cv2.imshow("only",only)
    cv2.imshow("recon",recon)
    k = cv2.waitKey(1)
     #Esc�L�[�������ƏI��
    if k == 27:
        break
     #s�������Ɖ摜��ۑ�
    if k == ord("s"):
        cv2.imwrite("painted.png", img)
        break


cv2.destroyAllWindows()


#����g������
#https://www.tech-tech.xyz/3132153.html���