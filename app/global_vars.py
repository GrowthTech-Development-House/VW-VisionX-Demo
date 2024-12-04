import torch
from ultralytics import YOLO
from datetime import datetime

from app.controller.camera_controller import Camera


class GlobalVars:
    def __init__(self):
        self.name = ''

        self.cap_1 = None
        self.cam1_index = 0
        self.cam1_frame = None

        self.model_1 = None
        self.model_2 = None
        self.model_3 = None
        self.model_4 = None

        self.inspection_mode = None
        self.BOM = None

    def setDefaultConfig(self, app):
        self.name = 'Demo_Web_App'

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        torch.cuda.set_device(0)
        print(f'Cuda device: {device}')

        self.cap_1 = Camera(self.cam1_index, save_folder=f'./images/camera1/{datetime.now().strftime("%Y-%m-%d")}')
        self.cap_1.start()

        # self.model_1 = YOLO("./model/label_line_model_1280_28112024.pt")
        # self.model_1.to(device=device)
        self.model_1 = YOLO("models/BOM_v1.pt")
        self.model_2 = YOLO("models/Defect_v1.pt")
        self.model_3 = YOLO("models/Position_v1.pt")
        print('models loaded')

        self.inspection_mode = 'Counting'
        self.BOM = []


