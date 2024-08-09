import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

# blank_finder 모듈을 가정합니다. 이 모듈에는 blank_finder 함수가 정의되어 있어야 합니다.
import blank_finder

class ImageHandler(FileSystemEventHandler):
    def __init__(self, directory, queue):
        self.directory = directory
        self.queue = queue
    def on_created(self, event):
        # 파일이 생성될 때 호출되는 이벤트 핸들러
        if event.is_directory:
            return
        elif event.src_path.endswith('.jpg'):
            print(f"New image detected: {event.src_path}")
            # 새 이미지가 감지되면 blank_finder 함수를 호출합니다.
            probabilities = blank_finder.blank_finder(event.src_path, self.queue)
            print(f"Probabilities: {probabilities}")

def start_monitoring(path, q):
    event_handler = ImageHandler(path, q)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# if __name__ == "__main__":
#     image_directory = "../locking/"
#     start_monitoring(image_directory)
