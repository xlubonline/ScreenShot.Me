from flask import Flask, request, send_file, jsonify
import undetected_chromedriver as uc
import time
import os

app = Flask(__name__)

@app.route("/ss")
def screenshot():
    url = request.args.get("q")
    if not url:
        return jsonify({"error": "Missing ?q= URL param"}), 400

    try:
        options = uc.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1280,720")
        options.add_argument("--disable-dev-shm-usage")

        driver = uc.Chrome(options=options)
        driver.get(url)
        time.sleep(2)

        screenshot_path = "/tmp/screenshot.png"
        driver.save_screenshot(screenshot_path)
        driver.quit()

        return send_file(screenshot_path, mimetype="image/png")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
