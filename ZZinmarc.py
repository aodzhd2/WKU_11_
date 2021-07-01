import pyzbar.pyzbar as pyzbar
import cv2 # opencv 사용
import time
import sys
import board
import busio as io
import adafruit_mlx90614
from time import sleep
from pyzbar.pyzbar import decode
from gpiozero import LED, Button, Buzzer

cap = cv2.VideoCapture(0) # 카메라 모듈 실시간 영상 받아오기
i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
mlx = adafruit_mlx90614.MLX90614(i2c) # mul90614 센서 사용
ambientTemp = "{:.2f}".format(mlx.ambient_temperature) # 비접족온도센서 측정 값
sleep(1) # 온도 측정 딜레이

used_codes = [] # QR코드 스캔 값 저장 리스트

i = 0

while(cap.isOpened()): # 실시간 화면 프레임 받아오기
    ret,img = cap.read()
    
    if not ret:
        continue
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    decoded = pyzbar.decode(gray)
    
    for d in decoded: # 카메라 모듈로 전송받은 화면에 QR코드 영역 표시 출력
        x,y,w,h = d.rect
        
        
        barcode_data = d.data.decode("utf-8")
        barcode_type = d.type
        
        cv2.rectangle(img, (x,y), (x+w,y+h),(0,0,255),2)
        
        text = '%s (%s)' % (barcode_data,barcode_type)
        cv2.putText(img, text, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,255),2,cv2.LINE_AA)
        
        
    for code in decode(img):
        if code.data.decode("utf-8") not in used_codes :
            f = open ('sorce.txt', 'a') # sorce.txt 파일 생성
            print('Code Data')
            print(code.data.decode('utf-8')) # QR코드 인식 값 출력
            print("체온을 측정해주세요.")
            used_codes.append(code.data.decode('utf-8'))
            for j in range(len(code.data.decode('utf-8'))): # sorce.txt 파일에 QR코드 값 저장
                ll = code.data.decode('utf-8')
                f.write(ll[j])
            f.write('\n')
            time.sleep(3) # QR코드 인식 후 3초 대기
                      
            for o in range(len(ambientTemp)): # sorce.txt 파일에 온도 값 저장
                t = ambientTemp # 비접촉 온도센서로 측정된 온도 값 저장 변수
                f.write(t[o])
                sleep(1)
            f.write('\n')
            f.write('------------------------------------\n')
            f.close() # sorce.txt 파일 종료
                           
        elif code.data.decode('utf-8') in used_codes: # 중복 인식 QR코드 방지
            print('')
        else:
            pass
        
    cv2.imshow('img',img) # 카메라 모듈로 전송받은 화면 출력

    
    key = cv2.waitKey(1)
    if key == ord('q'): # q 입력 시 캠 화면 종료
        break
    elif key == ord('s'):
        i += 1
        cv2.imwrite('c_%03d.jpg' % i, img)
        print("Data:" %i)


        
cap.release()
cv2.destroyALLWindows()