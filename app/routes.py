from app.controller.camera_controller import get_feed_cam1
from flask import render_template, Response, session, request, jsonify

from app.controller.general_helper import countedBOM


def register_routes(app, globalV):
    @app.route("/", methods=['GET', 'POST'])
    def dashboard():
        if request.method == "POST":
            globalV.inspection_mode = request.form.get("mode")
            print(f'Inspection action: {globalV.inspection_mode}')

        return render_template("dashboard.html", current_user=0)

    @app.route("/video_feed_cam1")
    def video_feed_cam1():
        return Response(get_feed_cam1('videofeed', 0, globalV), mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route("/logout")
    def logout():
        if 'token' in session:
            # Remove the token key from the session
            session.pop('token')

        return render_template("admin.html", current_user=0)

    @app.route('/getBOM')
    def getBOM():
        return jsonify(globalV.BOM)
