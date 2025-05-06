# Revealify Project Report

### 🎯 Project Goal
Revealify is a Python-based tool that converts PowerPoint (`.pptx`) presentations into fully functional, web-based slides using the Reveal.js framework. The final product aims to let users upload `.pptx` files and view them as modern, animated, interactive slideshows, without needing PowerPoint or downloading any software.

Reveal.js is a popular HTML presentation framework that supports transitions, themes, and dynamic content rendering. By combining it with Python and Flask, Revealify will allow users to interact with their presentations directly in the browser.

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


## 🗓 Project Timeline & Progress Log

> 📆 **Start Date:** March 24, 2025  
> 🕒 **Target:** 150 hours of work

---

### Week 1 — ✨ Discovery Phase (Mar 24–Mar 30) 

**Hours Logged:** ~20 hours

- Began with just the project idea: converting PowerPoint presentations into Reveal.js slides — had no clear implementation path at first.
- Explored how web-based presentation frameworks work and why Reveal.js was a suitable choice.
- Studied the Reveal.js documentation to understand its slide structure, themes, transitions, and JavaScript-based navigation system.
- Realized that Reveal.js is not a standalone renderer and would require integration through Node.js and HTML templating.
- Set up a basic Reveal.js test project and experimented with local servers (`npx http-server`) to preview slides.
- In parallel, researched `.pptx` parsing in Python and experimented with the `python-pptx` library.
- Tested content extraction from slides and studied how titles, paragraphs, and textboxes are represented internally.
- Gradually formed the project pipeline: `.pptx` → parsed structured data → HTML slide sections → Reveal.js rendering.

---

### Week 2 — ⚙️ Environment Setup & Minimum Viable Product (MVP) Script (Mar 31–Apr 7)

**Hours Logged:** ~32 hours

- Set up the full development environment: Python `venv`, `requirements.txt`, `.gitignore`, and folder layout  
- Created a basic script to extract text from `.pptx` using `python-pptx`  
- Structured extracted content into Reveal.js-friendly HTML sections  
- Generated `slides.html` and created a test `index.html` scaffold  
- Integrated Reveal.js into the project using `npm install`, connecting it to the pipeline  
- Linked the converter output to the Reveal frontend via `fetch("slides.html")`  
- Tested local Reveal.js preview using `npx http-server`  
- Explored Reveal fragments and how to apply `class="fragment"` to bullets  
- Resolved issues related to file linking, test data setup, and folder paths  

---

### Week 3 — 📄 Refactoring to OOP & Project Structure (Apr 8–Apr 14)

**Hours Logged:** ~28 hours

- Refactored procedural script into a modular object-oriented design
- Introduced `SlideConverter`, `HTMLSlide`, and `SlideContent` classes
- Organized logic into an `app/` folder and clarified code responsibilities
- Learned Python module importing strategies and use of `__init__.py`
- Built and tested methods for accurate slide ordering and type detection
- Integrated bullet-level detection and added Reveal fragment handling
- Enhanced the project’s layout for future Flask or web-based extensions
- Cleaned and commented the code, tested edge cases across different `.pptx` files

---

### Week 4 — 🌐 Flask Web App & UI Development (Apr 15–Apr 21)

**Hours Logged:** ~40 hours

> **Apr 21:** Heavy frontend debugging and refinement (~12 hours)

- Learned Flask fundamentals: routing, templates, static file handling, and `render_template` usage  
- Explored Flask project structure conventions and set up a scalable layout  
- Studied HTML, CSS, and JavaScript essentials to support frontend development  
- Designed and implemented a fully working Flask web app with:  
  - Upload form supporting `.pptx` file validation  
  - Clean routing with `/`, `/upload`, and `/view`  
  - Reveal.js preview integration using the converted `slides.html`  
- Built a stylish, modern UI with:  
  - Upload feedback using JavaScript  
  - Cancel upload functionality with styled feedback container  
  - Dynamic file detection and display  
  - Color and interaction design consistent with dark-themed Reveal.js  
- Debugged Reveal.js and static asset serving issues, ensuring smooth client-side loading  
- Iteratively refined layout, buttons, icons, hover effects, and user flow for a responsive feel  

---

### Week 4 — 📊 Table Support & Final Reveal.js Styling (Apr 21–Apr 28)

**Hours Logged:** ~20 hours (so far up to Apr 27)

- Extended the XML parser to support tables using `graphicFrame` + `<a:tbl>`  
- Maintained slide content ordering to include both paragraphs and tables without breaking sequence  
- Implemented a new `TableContent` class inheriting from `SlideContent` to generate responsive HTML `<table>` output  
- Integrated table blocks into Reveal.js slides while maintaining support for fragments and titles  
- Debugged complex rendering issues with table width, scrolling, and overflow behavior  
- Refined table HTML with `r-stretch`, `overflow-x/overflow-y: auto`, and wrapping strategies for wide layouts  
- Investigated Reveal.js limitations around scroll plugins and proposed pure-CSS fallback solutions  
- Rewrote and tested responsive CSS rules to preserve Reveal’s native style while allowing fit-to-slide tables  
- Improved `view.css` table layout, borders, wrapping, vertical alignment, and font balance  
- Maintained modularity and readability in `slide.py`, `converter.py`, and `xml_parser.py` despite expanding functionality
- Added a new **theme selector dropdown** to the homepage for choosing a Reveal.js theme before upload with over than 10 reveal themes, styled with emojis and modern dark UI 
- Finalized the user experience: a clean, modern “Choose a Reveal.js Theme” interaction above the upload button  
- Introduced <div class="r-fit-text"> wrapping for better dynamic fitting of text contents inside slides
- Refined scrolling behavior for wide tables with overflow-x/overflow-y: auto inside slides

> **Heavy UI trial-and-error and testing** contributed to ~20 hours of focused work across multiple debugging sessions.


---

## 📅 Daily Breakdown Summary (Mar 24–Apr 28)

> Estimated average: ~5-6 hours/day, increasing toward the later stages

- Early days focused on XML parsing and debugging, PowerPoint structure, and content classification (~4–5 hours/day)  
- Mid-phase included refactoring into OOP, edge case handling and debugging , and fragment logic in Reveal.js  
- Recent days (Week 4) were heavier (~7–12 hours/day) due to Flask integration, UI design, and extensive debugging of styling and rendering logic  
- Progress has been consistently iterative, with code improvements, testing cycles, and user experience polish across both backend and frontend sides

Total time logged so far: **140 hours / 150 hours**

---
 
## 🔁 Next Steps
- Add drag-and-drop upload, invalid file type alert, and loading spinner  

---

