import sys, cv2
import datetime as datetime
from collections import Counter
from tabnanny import verbose

colors = {2: (0,0,0), 1: (255,255,255), 0: (255,0,0), 3: (0,255,0), 4: (0,0,255), 5: (255,255,0), 6: (0,255,255), 7: (255,0,255) }

def run_inspection(frame, globalV):
    try:
        if globalV.inspection_mode == 'Counting':
            result = globalV.model_1.predict(frame, stream=True, verbose=False, iou=0.5)
            res = next(result, None)
            box = res.boxes
            boxes = box.xyxy
            classes = box.cls
            class_names = res.names
            items = []
            for cls, bx in zip(classes, boxes):
                # Add detected item to list by class
                item = class_names[int(cls)]
                items.append(item)
                annotate_image(item, cls, bx, frame)
            globalV.BOM = Counter(items)
            return frame
        elif globalV.inspection_mode == 'Defect Detection':
            result = globalV.model_2.predict(frame, stream=True, verbose=False, iou=0.5)
            res = next(result, None)
            box = res.boxes
            boxes = box.xyxy
            classes = box.cls
            class_names = res.names
            for cls, bx in zip(classes, boxes):
                # Add detected item to list by class
                item = class_names[int(cls)]
                annotate_image(item, cls, bx, frame)
            return frame
        elif globalV.inspection_mode == 'Positioning':
            # result = globalV.model_3.predict(frame, stream=True, verbose=False)
            # return next(result, None).plot()
            return frame
        elif globalV.inspection_mode == 'Assembly':
            # result = globalV.model_1.predict(frame, stream=True)
            # return next(result, None).plot()
            return frame
        else:
            return frame

    except Exception as e:
        # Print the error message along with the file name and line number where the error occurred
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        print("An error occurred in file:", file_name)
        print("Line number:", line_number)
        print("Error message:", e)

        # Get the current date and time
        current_datetime = datetime.datetime.now()

        # Extract the date part from the datetime object
        current_date = current_datetime.date()
        formatted_date = current_date.strftime("%Y-%m-%d")

        # Open a file in write mode ('w') inside a folder
        folder_path = './system_log'

        error_file_name = f'error_{formatted_date}.txt'
        error_file_path = folder_path + '/' + error_file_name

        with open(error_file_path, 'a') as f:
            # Write some content to the file
            f.write(f'{datetime.datetime.now()}: {e} - Line Number: {line_number} - File: {file_name}\n')


def itemize(arr, names):
    counted = []
    for name in arr:
        if name not in counted:
            counted[name] = 0
        counted[name] += 1
    print(f'Counted: {counted}')
    return counted

def annotate_image(item, cls, bx, frame):
    # Generate custom bounding boxes and put text on image
    x1, y1, x2, y2 = bx
    text = f'{item}'
    font = cv2.FONT_HERSHEY_SIMPLEX
    if int(cls) < colors.__len__():
        color = colors.get(int(cls))
    else:
        color = (192, 192, 192)
    cv2.rectangle(
        img=frame,
        pt1=(int(x1), int(y1)),
        pt2=(int(x2), int(y2)),
        color=color,
        thickness=2
    )
    cv2.putText(
        frame,
        text,
        (int(x1), int(y1) - 5),
        font,
        0.7,
        (0, 0, 0),
        1,
        cv2.LINE_AA)

