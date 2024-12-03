import os, time
from flask import Flask
from app.global_vars import GlobalVars
from app.routes import register_routes
from app.config import ProductionConfig, DevelopmentConfig

globalV = GlobalVars()

def create_app(globalV):
    app = Flask(__name__)
    flask_env = os.environ.get('APP_ENV', 'Prod')
    if flask_env == 'Prod':
        app.config.from_object(ProductionConfig)
    elif flask_env == 'Dev':
        app.config.from_object(DevelopmentConfig)

    # init db
    t1 = time.time()
    print(f'DB connect time: {time.time()-t1}s')

    # init default config
    t1 = time.time()
    globalV.setDefaultConfig(app)
    print(f'Default config init time: {time.time()-t1}')

    with app.app_context():
        start_time = time.time()
        register_routes(app, globalV)
        print(f'App started')

    return app
