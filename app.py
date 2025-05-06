from flask import Flask, render_template, request, redirect, abort
from jinja2 import TemplateNotFound
import os
from app.converter import SlideConverter

app = Flask(__name__) # this file is a host for flask application
app.config['UPLOAD_FOLDER'] = 'uploads' # This sets a configuration key: where uploaded files will be saved.

@app.route("/")
def home():
    return render_template("home.html")  # homepage

# browser POSTs to /upload and this route gets triggered after submit (no redirect to new html page)
@app.route("/upload", methods=["POST"]) # methods=["POST"] means it only responds when the browser sends data, not just visits.
def upload():
    # request gives access to data from the HTTP request (like uploaded files).
    # This grabs the uploaded file from the form. The key 'pptx_file' must match the name attribute in form
    file = request.files['pptx_file'] # 🟢 This matches the name attribute of input tag in html
    theme = request.form.get('theme', 'dracula')  # 🟢 Get selected theme (defaults to dracula)
    
    if file.filename.endswith(".pptx"): # uploaded file is a PowerPoint file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path) # This builds the full path to save the file and then saves it locally.
        try:
            # Run the converter on the uploaded PPTX and convert it to .html Reveal.js format
            converter = SlideConverter(file_path)
            converter.convert()
            converter.save("slides.html")
        except Exception as e:
            print("❌ Conversion failed:", e)
            return "Conversion failed", 500
        
        # Once slides are ready, redirect the user to /view route to see them.
        return redirect(f"/view?theme={theme}")  # ⬅️ Include selected theme in the URL
    return "Invalid file type", 400 # If the file isn’t a .pptx, send back an error.


# This serves Reveal.js viewer (index.html with the slides.html loaded inside).
@app.route("/view")
def view():
    try:
        theme = request.args.get("theme", "dracula")  # ⬅️ Read the theme from the URL
        return render_template("index.html", theme=theme)  # ← Reveal presentation viewer
    except TemplateNotFound:
        return "<h1>404 — Reveal view not found.</h1>", 404

#########################################################################
"""

 Flask App Entry Point

"""
if __name__ == "__main__":
    app.run(debug=True) # flask work on port 5000 by default
    # debug=True means: 1- Auto-reloads the server on code changes 2- Shows full error logs in browser (for development)