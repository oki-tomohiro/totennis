# -*- coding: utf-8 -*-
import cv2
import numpy as np
#sx, syは線の始まりの位置
sx, sy = 0, 0
img = cv2.imread("mt_fuji.jpg",cv2.IMREAD_GRAYSCALE)

locate = np.zeros(img.shape) #周波数領域の画像と照らし合わせる.

im1 = np.fft.fft2(img)
im2 = np.fft.fftshift(im1) #フーリエ変換後
im3 = np.abs(im2)
frequency = np.log(im3) #振幅スペクトル
frequency = (frequency-frequency.min()) / (frequency.max()-frequency.min()) #0から1へ正規化している

IM1 = np.zeros(img.shape,dtype=np.complex128) #各点での縞模様.complex型にする
IM2 = np.zeros(img.shape,dtype=np.complex128) #代入用
IMM1 = np.zeros(img.shape,dtype=np.complex128) #合計の縞模様.complex型にする
IMM2 = np.zeros(img.shape,dtype=np.complex128) #代入用
only=np.zeros(img.shape,dtype=np.float64) #float型.その点だけ(only)での空間領域での波形
recon=np.zeros(img.shape,dtype=np.float64) #float型.再構成(reconfigure)した空間領域での画像

h,w = img.shape
#マウスの操作があるとき呼ばれる関数
def callback(event, x, y, flags, param):
    global sx, sy,locate,IM1,IM2,IMM1,IMM2,im2,IMMM1,IMMM2,only,recon,h,w
    #マウスの左ボタンがクリックされたとき
    if event == cv2.EVENT_LBUTTONDOWN:
        IM1[sy,sx] = 0 #その点だけでの空間領域での波形を表示するため,前の波形の要素をなくしている.
        if ((0 <= y and y <= h-1) and (0 <= x and x <= w-1)): #カーソル位置が画面内にあるか
            sy, sx = y, x
            locate[y,x] = 1
            IM1[y,x] = im2[y,x]
            IMM1[y,x] = im2[y,x]
            IM2 = IM1 #コピー
            IMM2 = IMM1 #コピー
            IM2 = np.fft.fftshift(IM2)
            IMM2 = np.fft.fftshift(IMM2)
            IM2 = np.fft.ifft2(IM2)
            IMM2 = np.fft.ifft2(IMM2)
            only=IM2.real
            recon=IMM2.real
            only=(only-only.min()) / (only.max()-only.min()) #正規化
            recon=(recon-recon.min()) / (recon.max()-recon.min()) #正規化
    #マウスの左ボタンがクリックされていて、マウスが動いたとき
    if flags == cv2.EVENT_FLAG_LBUTTON and event == cv2.EVENT_MOUSEMOVE:
        IM1[sy,sx] = 0 #その点だけでの空間領域での波形を表示するため,前の波形の要素をなくしている.
        if ((0 <= y and y <= h-1) and (0 <= x and x <= w-1)): #カーソル位置が画面内にあるか
            sy, sx = y, x
            locate[y,x] = 1
            IM1[y,x] = im2[y,x]
            IMM1[y,x] = im2[y,x]
            IM2 = IM1 #コピー
            IMM2 = IMM1 #コピー
            IM2 = np.fft.fftshift(IM2)
            IMM2 = np.fft.fftshift(IMM2)
            IM2 = np.fft.ifft2(IM2)
            IMM2 = np.fft.ifft2(IMM2)
            only=IM2.real
            recon=IMM2.real
            only=(only-only.min()) / (only.max()-only.min()) #正規化
            recon=(recon-recon.min()) / (recon.max()-recon.min()) #正規化

#ウィンドウの名前を設定
cv2.namedWindow("locate", cv2.WINDOW_NORMAL)
#コールバック関数の設定
cv2.setMouseCallback("locate", callback)
while(1):
    cv2.imshow("img", img)
    cv2.imshow("frequency",frequency)
    cv2.imshow("locate",locate)
    cv2.imshow("only",only)
    cv2.imshow("recon",recon)
    k = cv2.waitKey(1)
     #Escキーを押すと終了
    if k == 27:
        break
     #sを押すと画像を保存
    if k == ord("s"):
        cv2.imwrite("painted.png", img)
        break


cv2.destroyAllWindows()


#今回使うもの
#https://www.tech-tech.xyz/3132153.htmlより