import os
from app import create_app, GlobalVars

globalV = GlobalVars()
app = create_app(globalV)
# script_dir = os.path.dirname(os.path.realpath(__file__))
# os.chdir(script_dir)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)