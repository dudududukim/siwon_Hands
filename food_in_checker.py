import RPi.GPIO as GPIO
import motor
import time
from queue import Queue, Empty  # 큐가 비어있을 때 발생하는 예외를 처리하기 위해 추가

SWITCH_PIN = 24  # Ensure this is correctly set as per BCM or BOARD

def setup():
    GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Setup without setting the mode

def food_detected(q):
    setup()
    last_pressed = 0
    debounce_time = 0.1  # 디바운스 시간 조정

    while True:
        try:
            input_state = GPIO.input(SWITCH_PIN)
            if input_state == GPIO.HIGH and (time.time() - last_pressed) > debounce_time:
                last_pressed = time.time()  # 마지막 트리거 시간 업데이트
                time.sleep(0.1)  # 짧은 지연 시간 추가
                if GPIO.input(SWITCH_PIN) == GPIO.HIGH:  # 재확인
                    if not q.empty():
                        print("Food detected! Activating motor...")
                        motor.to_blank(q)
                        time.sleep(5)  # 재트리거 방지
                    else:
                        # print("No Queue exists")  # 큐가 비었을 경우 출력
                        continue
        except KeyboardInterrupt:
            print("Interrupted by the user")
            break
        except Empty:
            print("Queue is empty, skipping...")
            time.sleep(1)  # 큐가 비어 있는 경우, 다시 확인하기 전에 잠시 대기

    # No cleanup here, as it's handled in the main module after threads end
