import threading
import lock_check
import queue
import new_image_checker
import food_in_checker
import RPi.GPIO as GPIO

def setup_gpio():
    GPIO.setmode(GPIO.BCM)  # 전역적으로 한 번만 설정
    
    # 핀 번호 설정
    DIR_td = 20   # 방향 핀 (Top-Down)
    STEP_td = 16  # 스텝 핀 (Top-Down)
    DIR_lr = 3    # 방향 핀 (Left-Right)
    STEP_lr = 2   # 스텝 핀 (Left-Right)
    DIR_foodplate = 27   # 방향 핀
    STEP_foodplate = 17  # 스텝 핀  
    
    # GPIO 핀 설정
    GPIO.setup(DIR_td, GPIO.OUT)
    GPIO.setup(STEP_td, GPIO.OUT)
    GPIO.setup(DIR_lr, GPIO.OUT)
    GPIO.setup(STEP_lr, GPIO.OUT)
    
    GPIO.setup(DIR_foodplate, GPIO.OUT)
    GPIO.setup(STEP_foodplate, GPIO.OUT)
    

def main():
    setup_gpio()
    
    # Queue 생성
    q = queue.LifoQueue()

    # image_in_checker 모듈에서 디렉토리 모니터링을 시작하는 스레드 설정
    image_directory = "./refridge_images/"
    monitoring_thread = threading.Thread(target=new_image_checker.start_monitoring, args=(image_directory, q))

    # receive_message 모듈에서 시리얼 통신을 시작하는 스레드 설정
    serial_thread = threading.Thread(target=lock_check.receive_message)
    
    # food_in_checker 모듈에서 음식 감지를 시작하는 스레드 설정
    food_thread = threading.Thread(target=food_in_checker.food_detected, args=(q,))

    # 스레드 시작
    monitoring_thread.start()
    serial_thread.start()
    food_thread.start()

    try:
        monitoring_thread.join()
        serial_thread.join()
        food_thread.join()
    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        GPIO.cleanup()  # Cleanup GPIO only once here
    # 메인 스레드에서 스레드가 종료될 때까지 기다림
    
if __name__ == "__main__":
    main()
