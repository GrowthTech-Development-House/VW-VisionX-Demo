import sys
import datetime as datetime
from collections import Counter

def run_inspection(frame, globalV):
    try:
        if globalV.inspection_mode == 'Counting':
            result = globalV.model_1.predict(frame, stream=True, verbose=False)
            res = next(result, None)
            box = res.boxes
            classes = box.cls
            class_names = res.names
            items = []
            for cls in classes:
                item = class_names[int(cls)]
                items.append(item)
            globalV.BOM = Counter(items)
            return res.plot()
        elif globalV.inspection_mode == 'Defect Detection':
            result = globalV.model_1.predict(frame, stream=True)
            return next(result, None).plot()
        elif globalV.inspection_mode == 'Positioning':
            result = globalV.model_1.predict(frame, stream=True)
            return next(result, None).plot()
        elif globalV.inspection_mode == 'Assembly':
            result = globalV.model_1.predict(frame, stream=True)
            return next(result, None).plot()
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

