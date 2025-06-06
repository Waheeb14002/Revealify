# Revealify Project Report

### 🎯 Project Goal
Revealify is a Python-based tool that converts PowerPoint (`.pptx`) presentations into fully functional, web-based slides using the Reveal.js framework. The final product aims to let users upload `.pptx` files and view them as modern, animated, interactive slideshows, without needing PowerPoint or downloading any software.

Reveal.js is a popular HTML presentation framework that supports transitions, themes, and dynamic content rendering. By combining it with Python and Flask, Revealify will allow users to interact with their presentations directly in the browser.

---

## 🟢 Features

| Feature                                                               | Status         |
|-----------------------------------------------------------------------|----------------|
| 🟢 Full web application (Flask)                                        | ✅ Implemented |
| 🟢 Modern Flask web UI with Theme selector (Reveal.js)                 | ✅ Implemented |
| 🟢 Upload and convert `.pptx`                                          | ✅ Implemented |
| 🟢 Fragments (click-to-reveal)                                         | ✅ Implemented |
| 🟢 Slide titles & text parsing                                         | ✅ Implemented |
| 🟢 Bullet points + nesting                                             | ✅ Implemented |
| 🟢 Table content support (text only)                                   | ✅ Implemented |
| 🟢 Styled inline text (bold, italic, underline, strikethrough, hyperlinks) | ✅ Implemented |
| 🟢 Images/Pictures extraction                                          | ✅ Implemented |




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

**Hours Logged:** ~15 hours

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

**Hours Logged:** ~15 hours

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

**Hours Logged:** ~15 hours

> **Apr 21:** Heavy frontend debugging and refinement (~ 6+ hours)

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

### Week 5 — 📊 Table Support & Final Reveal.js Styling (Apr 21–Apr 28)

**Hours Logged:** ~15 hours

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

> **Heavy UI trial-and-error and testing** contributed to ~15 hours of focused work across multiple debugging sessions.
---

### Week 6 — ✨ Rich Text Styling & Table Dimension Precision (Apr 29–May 5)

**Hours Logged:** ~8 hours

- Added support for **precise table positioning and dimensions**, including `x`, `y`, `width`, and `height` in percentage of slide size  
- Extracted and applied **column widths** from `<a:tblGrid>` for more faithful Reveal.js table rendering  
- Enhanced the `XmlParser` to output detailed table shape geometry using EMUs-to-percent conversion logic  
- Introduced support for **styled inline text** inside paragraphs and bullets by parsing `<a:r>` and `<a:rPr>`  
- Supported rich formatting: **bold**, *italic*, <u>underline</u>, and <span style="text-decoration:line-through;">strikethrough</span> using HTML equivalents (`<strong>`, `<em>`, `<u>`, `<span>`)  
- Updated `ParagraphContent` and `BulletNode` to render styled `runs` inline without breaking text flow  
- Ensured full compatibility with existing bullet nesting and paragraph grouping logic  
- Cleaned up item dispatching logic in `converter.py` to only process `"text"` and `"table"` types, skipping unhandled shapes safely  

---

### Week 7 — 🔄 Switched to python-pptx & Rich Text Table Cells (May 6–May 12)

**Hours Logged:** ~12 hours

- Started over, transitioning from manual XML parsing to using the `python-pptx` library, with modifications for advanced extraction when needed  
- Added robust support for text shape extraction and absolute positioning, including precise `x`, `y`, `width`, and `height` as percentages of slide dimensions  
- After implementing exact positioning, I encountered a bug where shapes were overlapping and collapsing for some reason. Spent many hours trying to figure out what was causing shapes to overlap; eventually I resolved it. 
- Extended rich text styling to table cells, supporting bold, italic, underline, and strikethrough within table content  
- Developed and integrated JavaScript font fitting logic to dynamically shrink text within text shapes until it fits the bounding box  
- Encountered a bug where `.scrollHeight` remained constant despite font shrinking, causing text to hit the minimum font-size rather than fit naturally; this issue remains unresolved  
- Enhanced overall code structure for future extensibility and easier handling of Reveal.js HTML rendering  

---


## 📅 Daily Breakdown Summary (Mar 24–May 12)

> Estimated average: ~4-5 hours/day, increasing toward the later stages

- Early days focused on XML parsing and debugging, PowerPoint structure, and content classification (~4–5 hours/day)  
- Mid-phase included refactoring into OOP, edge case handling and debugging , and fragment logic in Reveal.js  
- Recent days (Week 4) were heavier due to Flask integration, UI design, and extensive debugging of styling and rendering logic  
- Progress has been consistently iterative, with code improvements, testing cycles, and user experience polish across both backend and frontend sides
- Heavy trial-and-error and debugging accompanied nearly every new conversion feature, with multiple sessions often requiring several focused hours each to resolve edge cases and ensure reliable results.
...makes it clear that not all hours were “pure coding”—lots went into thoughtful debugging and quality.

Total time logged so far: **100 hours / 150 hours**



---
 
## 🔁 Next Steps
- Add drag-and-drop upload, invalid file type alert, and loading spinner  

---

