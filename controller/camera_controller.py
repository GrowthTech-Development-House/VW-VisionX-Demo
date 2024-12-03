import cv2, os, datetime, threading,time
from app.controller.inspection_controller import run_inspection


def get_feed_cam1(type, capture, globalV):
    try:
        if globalV.cap_1.camera_status():
            while True:
                globalV.cam1_frame = globalV.cap_1.get_frame()
                frame = globalV.cam1_frame
                inspected_frame = run_inspection(frame, globalV)
                if frame is None:
                    break
                success, buffer = cv2.imencode('.jpg', inspected_frame)
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        else:
            print(f'Reconnecting..')
            globalV.cap_1.reconnect('Cam1')
    except Exception as e:
        print(f'Error: {e} occured')
        log(f"An error occurred: {e}", "./camera_log")


def log(message, folder_path):
    current_datetime = datetime.datetime.now()
    formatted_date = current_datetime.strftime("%Y-%m-%d")
    folder_path = './system_log'
    error_file_name = f'error_{formatted_date}.txt'
    error_file_path = os.path.join(folder_path, error_file_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(error_file_path, 'a') as f:
        f.write(f'{current_datetime}: {message}\n')


class Camera:
    def __init__(self, cam_index, save_folder, reconnect_delay=1):
        self.cam_index = cam_index
        self.save_folder = save_folder
        self.reconnect_delay = reconnect_delay
        self.cap = cv2.VideoCapture(self.cam_index, cv2.CAP_ANY)
        if self.cap.isOpened():
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        self.Frame = None
        self.isstop = False
        self.thread = threading.Thread(target=self.queryframe, daemon=True)

    def camera_status(self):
        return self.cap.isOpened()

    def connect(self, camera_angle):
        log(f'Connecting to {camera_angle} with index: {self.cam_index}', './camera_log')
        if not self.cap.isOpened():
            self.cap.open(self.cam_index, cv2.CAP_ANY)
            if self.cap.isOpened():
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            if not self.cap.isOpened():
                message = f'Camera {camera_angle} with index: {self.cam_index} failed to connect'
                log(message, "./camera_log")
                # log(message, "./system_log")
                return False
            return True

    def check_connection(self):
        """
        Checks if the camera is properly connected and streaming.
        Returns:
            bool: True if the camera is connected and streaming, False otherwise.
        """
        if not self.cap.isOpened():
            log(f'Camera {self.cam_index} is not connected.', './camera_log')
            return False
        # Try to grab a frame to ensure the camera is streaming correctly.
        success, _ = self.cap.read()
        if not success:
            log(f'Camera {self.cam_index} is not streaming properly.', './camera_log')
            return False
        return True

    def reconnect(self, camera_angle):
        log(f'Reconnecting to {camera_angle} with index: {self.cam_index}', './camera_log')
        self.cap.release()
        time.sleep(self.reconnect_delay)

        connected = False
        while not connected:
            connected = self.connect(camera_angle)

        return connected

    def start(self):
        self.thread.start()

    def stop(self):
        self.isstop = True
        self.thread.join()
        print('Camera stopped!')

    def queryframe(self):
        while not self.isstop:
            if not self.cap.isOpened():
                self.connect("camera")
            try:
                success, frame = self.cap.read()
                if not success:
                    log('Failed to read frame from camera', './camera_log')
                    self.reconnect("camera")
                    continue
                self.Frame = frame
            except cv2.error as ex:
                print(f'cv2 Exception during read: {ex}')
                self.cap.release()
                self.connect("camera")
            except Exception as e:
                print(f'Exception during read: {e}')
                self.cap.release()
                self.connect("camera")
        self.cap.release()

    def get_frame(self):
        return self.Frame

    def save_frame(self, frame, file_name, cam, globalV):
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)

        folder_path = f'{self.save_folder}/{file_name}'

        if cam == 1:
            globalV.global_im_path_cam1 = folder_path
        else:
            globalV.global_im_path_cam2 = folder_path

        cv2.imwrite(folder_path, frame)
        print(f"Frame saved to {folder_path}.")