import RPi.GPIO as GPIO
import time

# 핀 번호 설정
DIR_td = 20   # 방향 핀 (Top-Down)
STEP_td = 16  # 스텝 핀 (Top-Down)
DIR_lr = 3    # 방향 핀 (Left-Right)
STEP_lr = 2   # 스텝 핀 (Left-Right)
DIR_foodplate = 27   # 방향 핀
STEP_foodplate = 17  # 스텝 핀

CW = 1        # 시계 방향
CCW = 0       # 반시계 방향

# 칸별 모터 이동 파라미터 설정
steps = {
    2: (1740, 15),  # 1번 칸: td steps, lr steps
    4: (1740, 90),  # 2번 칸: td steps, lr steps
    1: (4753, 15),  # 3번 칸: td steps, lr steps
    3: (4753, 90)   # 4번 칸: td steps, lr steps
}

step_count_foodplate = 63
delay_foodplate = 0.1


def to_blank(q):
    # 사용 가능한 첫 번째 칸을 찾기
    blank_info = q.get()
    prob_updated = []
    for i, prob in enumerate(blank_info, start=1):
        if prob < 10:
            for j, prob in enumerate(blank_info, start=1):
                if j==i:
                    prob_updated.append(100)
                else:
                    prob_updated.append(prob)
            
            q.put(prob_updated)
            
            print(f"Moving to slot {i}")
            td_steps, lr_steps = steps[i]
            
            # 상 모터 작동 (Top-Down)
            GPIO.output(DIR_td, CCW)
            for _ in range(td_steps):
                GPIO.output(STEP_td, GPIO.HIGH)
                time.sleep(0.001)
                GPIO.output(STEP_td, GPIO.LOW)
                time.sleep(0.001)
            
            # 우 모터 작동 (Left-Right)
            GPIO.output(DIR_lr, CW)
            for _ in range(lr_steps):
                GPIO.output(STEP_lr, GPIO.HIGH)
                time.sleep(0.03)
                GPIO.output(STEP_lr, GPIO.LOW)
                time.sleep(0.03)
                
            for x in range(step_count_foodplate):
                GPIO.output(DIR_foodplate, CW)
                GPIO.output(STEP_foodplate, GPIO.HIGH)
                time.sleep(delay_foodplate)
                GPIO.output(STEP_foodplate, GPIO.LOW)
                time.sleep(delay_foodplate)
                #뒤로
            for x in range(step_count_foodplate):
                GPIO.output(DIR_foodplate, CCW)
                GPIO.output(STEP_foodplate, GPIO.HIGH)
                time.sleep(delay_foodplate)
                GPIO.output(STEP_foodplate, GPIO.LOW)
                time.sleep(delay_foodplate)
                
            print(f":) Moving finished, returning to original position")
            
            # 좌 모터 되돌리기
            GPIO.output(DIR_lr, CCW)
            for _ in range(lr_steps):
                GPIO.output(STEP_lr, GPIO.HIGH)
                time.sleep(0.03)
                GPIO.output(STEP_lr, GPIO.LOW)
                time.sleep(0.03)
                
            # 하 모터 되돌리기
            GPIO.output(DIR_td, CW)
            for _ in range(td_steps):
                GPIO.output(STEP_td, GPIO.HIGH)
                time.sleep(0.001)
                GPIO.output(STEP_td, GPIO.LOW)
                time.sleep(0.001)
            print("Returned to original position")
            
            break
            
        elif i==4:
            print("No empty place")
            break
            
        
