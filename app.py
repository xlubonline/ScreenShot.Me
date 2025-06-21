from flask import Flask, request, send_file, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

app = Flask(__name__)

@app.route("/ss")
def screenshot():
    url = request.args.get("q")
    if not url:
        return jsonify({"error": "Missing 'q' parameter"}), 400

    # Headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1280,720")

    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        time.sleep(2)  # Allow the page to load

        screenshot_path = "/tmp/screenshot.png"
        driver.save_screenshot(screenshot_path)

        return send_file(screenshot_path, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        driver.quit()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
