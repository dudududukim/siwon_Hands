import RPi.GPIO as GPIO
import time

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)

# 핀 번호 설정
DIR_tdl = 20   # 방향 핀
STEP_tdl = 16  # 스텝 핀
DIR_tdr = 27   # 방향 핀
STEP_tdr = 17  # 스텝 핀

DIR_lr = 3   # 방향 핀
STEP_lr = 2

CW = 1     # 시계 방향
CCW = 0    # 반시계 방향
SPR = 200  # 스테퍼 모터의 스텝 수 (예: 200 스텝/회전)

# 상하좌우 button pin number 설정
# [하, 우, 좌, 상]
pins = [6, 13, 19, 26]

# GPIO 핀 설정
GPIO.setup(DIR_tdl, GPIO.OUT)
GPIO.setup(DIR_tdr, GPIO.OUT)
GPIO.setup(DIR_lr, GPIO.OUT)
GPIO.setup(STEP_tdl, GPIO.OUT)
GPIO.setup(STEP_tdr, GPIO.OUT)
GPIO.setup(STEP_lr, GPIO.OUT)

for pin in pins:
    GPIO.setup(pin, GPIO.IN)

# 모터 제어 파라미터
step_count = SPR 
delay = 0.001
delay_small = 0.03
try:
    while True:
        # button input check
        values = [GPIO.input(pin) for pin in pins]
        
        # [하, 우, 좌, 상]
        if values == [1, 1, 1, 1]:
            continue
        
        if not values[0]:  # 하 버튼 눌렸을 때
            # print("하")
            GPIO.output(DIR_tdl, CW)
            GPIO.output(DIR_tdr, CW)
            
            # 모터 한 스텝 움직임
            GPIO.output(STEP_tdl, GPIO.HIGH)
            GPIO.output(STEP_tdr, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(STEP_tdl, GPIO.LOW)
            GPIO.output(STEP_tdr, GPIO.LOW)
            time.sleep(delay)
            
        elif not values[3]:  # 상 버튼 눌렸을 때
            # print("상")
            GPIO.output(DIR_tdl, CCW)
            GPIO.output(DIR_tdr, CCW)
            # 모터 한 스텝 움직임
            GPIO.output(STEP_tdl, GPIO.HIGH)
            GPIO.output(STEP_tdr, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(STEP_tdl, GPIO.LOW)
            GPIO.output(STEP_tdr, GPIO.LOW)
            time.sleep(delay)

        elif not values[2]: # 좌
            # print("좌")
            GPIO.output(DIR_lr, CCW)
            GPIO.output(STEP_lr, GPIO.HIGH)
            time.sleep(delay_small)
            GPIO.output(STEP_lr, GPIO.LOW)
            time.sleep(delay_small)
            
        elif not values[1]: # 우
            # print("우")
            GPIO.output(DIR_lr, CW)
            GPIO.output(STEP_lr, GPIO.HIGH)
            time.sleep(delay_small)
            GPIO.output(STEP_lr, GPIO.LOW)
            time.sleep(delay_small)
            
            
        else:
            continue

except KeyboardInterrupt:
    # CTRL+C를 누를 경우 GPIO 설정 해제
    GPIO.cleanup()
