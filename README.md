# 🖼️ Revealify - PowerPoint to Reveal.js Converter

This project converts `.pptx` PowerPoint slides into [Reveal.js](https://revealjs.com/) web-based slides — preserving structure, titles, nested bullets, and fragment animations — and presents them via a modern Flask web app.

---

## ✅ Features

| Feature                                | Status       |
|----------------------------------------|--------------|
| ✅ Full web application (Flask)         | Implemented  |
| ✅ Modern Flask web UI                 | Implemented  |
| ✅ Slide titles & text parsing         | Implemented  |
| ✅ Bullet points + nesting             | Implemented  |
| ✅ Fragments (click-to-reveal)          | Implemented  |
| ✅ Table content support (text only)    | Implemented  |
| ✅ Upload and convert `.pptx`           | Implemented  |
| ✅ Theme selector (Reveal.js)           | Implemented  |


## 📂 Example PowerPoint File

A sample PowerPoint file `example.pptx` is provided inside the project.  
You can use it to test the Revealify conversion process immediately.

---

## 🔧 Getting Started

### 🌀 Clone the Repository

To clone this project and run it locally:

```bash
git clone https://github.com/Waheeb14002/Revealify.git
```
```bash
cd Revealify
```

Then follow the steps below to install and run.

---

## ⚙️ Set Up Your Environment

Before running Revealify in either mode, make sure to set up the necessary environment:

### 🐍 Python (for Flask mode and script-based conversion)

#### 1. Create a virtual environment:

```bash
python -m venv venv
```

#### 2. Activate the virtual environment:

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

#### 3. Install required Python dependencies:

```bash
pip install -r requirements.txt
```

---

### 🟪 Node.js (for Standalone mode)

If you'd like to run Revealify without Flask, you need [Node.js](https://nodejs.org) installed.  
This provides the `npx` command used to start a lightweight server.

After installation, verify Node.js and npm:

```bash
node -v
npm -v
```

✅ If both show version numbers, you're ready to run standalone mode.

---

### 🚀 How to Run This Project

You can run Revealify in one of two modes:

- **[Standalone Mode](#-standalone-mode-run-without-flask)**
- **[Flask Web App Mode](#-running-as-a-flask-web-app)**

Choose your preferred option below.

---

## ⚡Standalone Mode: Run Without Flask 

You can also run Revealify without using Flask at all:

> ⚠️ This method requires [Node.js](https://nodejs.org/) to be installed.  
> It provides the `npx` command used to launch a simple web server.

1. Open a terminal in your project root.

2. Run the converter manually to generate `slides.html`:

```bash
python run.py
```

3. Start a simple HTTP server:

```bash
npx http-server 
```

4. Then open your browser and navigate to:

```
http://localhost:8081
```

✔️ This method **directly previews** the generated `slides.html` inside the Reveal.js player.  
✔️ Useful for testing or showing your presentations without running a Python server.

---

## 🌐 Running as a Flask Web App

If you'd like to use Revealify as a full web application with upload, theming, and dynamic slide conversion, follow the steps below.

This is the recommended method for users who want an interactive UI and full control from the browser.


### 📤 Upload and Convert a `.pptx` File

Start the Flask app:

```bash
python app.py
```

Then open your browser and go to:

```
http://localhost:5000
```

- Upload a `.pptx` PowerPoint file
- Click **Convert**
- You'll be redirected to `/view` where your Reveal.js presentation is displayed

---


## Note: 📁 No `npm install` Required

All Reveal.js files are already included under:

```
/static/reveal.js/
```

✔️ You do **not** need to run `npm install`  
✔️ You do **not** need `node_modules/`, `package.json`, or `package-lock.json`  
✔️ This works fully with Flask — no Node.js required

---


## 🔄 Want to Upgrade Reveal.js?

⚠️ *This is optional and only needed if you want the latest Reveal.js version.*

1. You’ll need [Node.js](https://nodejs.org/) installed.

2. In your project root, run:
   ```bash
   npm install reveal.js
   ```

3. Copy the entire folder:
   ```bash
   # Instead of picking parts, copy it all
   mv node_modules/reveal.js static/reveal.js
   ```

4. You may delete the `node_modules/` folder and `package.json` files if you no longer need them.

---

## 📝 Developer Notes

- `slides.html` is never committed — it is generated fresh per upload
- Your .gitignore already excludes: slides.html, .pptx, venv/, and node_modules/
- Reveal.js was copied from `node_modules/reveal.js/` into `static/reveal.js/` for browser use
- No need to use `npm install` — this is not a Node-based app
- VS Code users: Python virtual environment auto-activates via `.vscode/settings.json`:

  ```json
  {
    "python.terminal.activateEnvironment": true
  }
  ```

  ✅ So No need to run `venv\Scripts\activate` manually every time in the integrated terminal.

---

## 📂 Project Structure (Simplified)

```
project/
├── app/                    # Conversion logic (Python classes)
├── static/
│   └── reveal.js/          # Reveal.js static assets (copied)
│   └── styles/             # Custom CSS for web UI
├── templates/
│   ├── home.html           # Upload UI
│   └── index.html          # Reveal.js player
├── uploads/                # Temporary uploaded .pptx files
├── app.py                  # Flask entry point
├── requirements.txt
└── README.md
```

---
