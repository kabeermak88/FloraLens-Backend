# from flask import Flask, render_template, request
# import os
# from utils.predict import predict_flower

# app = Flask(__name__)

# UPLOAD_FOLDER = "static/uploads"
# MODEL_PATH = "model/flower_model.h5"

# # Ensure upload folder exists
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         file = request.files["file"]
#         if file:
#             filepath = os.path.join(UPLOAD_FOLDER, file.filename)
#             file.save(filepath)

#             label, confidence = predict_flower(MODEL_PATH, filepath)
#             return render_template(
#                 "index.html",
#                 uploaded_image=filepath,
#                 label=label,
#                 confidence=f"{confidence*100:.2f}%"
#             )
#     return render_template("index.html", uploaded_image=None)

# if __name__ == "__main__":
#     app.run(debug=True)

# from flask import Flask, render_template, request, jsonify, make_response
# import os
# from utils.predict import predict_flower

# app = Flask(__name__)

# UPLOAD_FOLDER = "static/uploads"
# MODEL_PATH = "model/flower_model.h5"

# # Ensure upload folder exists
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # ✅ CORS headers manually added
# @app.after_request
# def add_cors_headers(response):
#     response.headers["Access-Control-Allow-Origin"] = "*"
#     response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
#     response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
#     return response


# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         file = request.files["file"]
#         if file:
#             filepath = os.path.join(UPLOAD_FOLDER, file.filename)
#             file.save(filepath)

#             label, confidence = predict_flower(MODEL_PATH, filepath)
#             return render_template(
#                 "index.html",
#                 uploaded_image=filepath,
#                 label=label,
#                 confidence=f"{confidence*100:.2f}%"
#             )
#     return render_template("index.html", uploaded_image=None)


# # ✅ Mobile API route (for React Native app)
# @app.route("/predict", methods=["POST", "OPTIONS"])
# def predict_api():
#     if request.method == "OPTIONS":
#         # Handle preflight request
#         response = make_response()
#         response.headers["Access-Control-Allow-Origin"] = "*"
#         response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
#         response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
#         return response

#     try:
#         file = request.files["file"]
#         filepath = os.path.join(UPLOAD_FOLDER, file.filename)
#         file.save(filepath)

#         label, confidence = predict_flower(MODEL_PATH, filepath)

#         return jsonify({
#             "prediction": label,
#             "confidence": round(confidence * 100, 2)
#         })
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# if __name__ == "__main__":
#     # ✅ Make sure it's accessible to your phone on Wi-Fi
#     app.run(host="0.0.0.0", port=5000, debug=True)
from flask import Flask, request, jsonify, make_response
import os
from utils.predict import predict_flower

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
MODEL_PATH = "model/flower_model.h5"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ Manual CORS headers (no flask_cors required)
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response

@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    if request.method == "OPTIONS":
        # CORS preflight response
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
        return response

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Predict flower
    label, confidence = predict_flower(MODEL_PATH, filepath)

    return jsonify({
        "prediction": label,
        "confidence": f"{confidence*100:.2f}%"
    })


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask Flower Identifier API running!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
