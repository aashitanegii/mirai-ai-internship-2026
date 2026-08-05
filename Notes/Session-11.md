# 📒 MirAI Internship – Session 11 Notes

**Session:** Interactive Web Development with DOM & APIs

---

# 1. Session Overview

This session introduced **frontend web development** using HTML, CSS, JavaScript, the DOM, and APIs. Unlike previous Streamlit-based sessions, the focus shifted to building interactive browser applications that communicate with backend AI services.

The main project discussed was an **AI Resume Builder**, where users upload a resume and provide a job description to generate an optimized resume.

---

# 2. AI Resume Builder Project

The primary project demonstrated during the session was an **AI Resume Builder**.

### Features

* Upload Resume (PDF)
* Paste Job Description
* Generate AI-optimized Resume
* Edit generated resume
* Tailor resume for a specific job

### Workflow

```text
Resume Upload
      ↓
Job Description
      ↓
AI Processing
      ↓
Resume Optimization
      ↓
Editable Resume
```

---

# 3. HTML Basics

HTML (HyperText Markup Language) is used to structure webpages.

Common elements introduced:

```html
<html>
<head>
<body>

<h1>
<p>
<div>
<input>
<button>
<form>
```

HTML provides the content and layout of a webpage.

---

# 4. Document Object Model (DOM)

The DOM (Document Object Model) represents an HTML page as a tree of objects that JavaScript can access and modify.

Example:

```text
Document
   │
 html
 ├── head
 └── body
      ├── h1
      ├── input
      ├── button
      └── div
```

Using the DOM, JavaScript can:

* Read page elements
* Update text
* Change styles
* Add/remove elements
* Respond to user actions

---

# 5. Selecting DOM Elements

JavaScript can access HTML elements using methods like:

```javascript
document.getElementById()

document.querySelector()

document.querySelectorAll()
```

Example:

```javascript
const button = document.getElementById("generateBtn");
```

---

# 6. DOM Manipulation

Once an element is selected, JavaScript can modify it.

Examples:

```javascript
element.innerHTML

element.textContent

element.style

element.value
```

Example:

```javascript
title.textContent = "Resume Generated";
```

This allows webpages to update dynamically without reloading.

---

# 7. Event Handling

Events allow webpages to respond to user interactions.

Common events:

* Click
* Input
* Change
* Submit

Example:

```javascript
button.addEventListener("click", generateResume);
```

When the button is clicked, the associated function executes.

---

# 8. Forms and User Input

Forms collect user information.

Typical fields:

* Resume Upload
* Job Description
* Text Inputs
* Buttons

Example:

```html
<input type="file">

<textarea>

<button>
```

JavaScript retrieves the entered values and processes them.

---

# 9. APIs and Client–Server Architecture

An API connects the frontend with backend services.

Architecture:

```text
Browser (Client)
        ↓
HTTP Request
        ↓
API Server
        ↓
AI Processing
        ↓
Response
        ↓
Browser
```

The frontend sends user data to the backend and displays the returned result.

---

# 10. Resume Generation Workflow

The AI Resume Builder follows this process:

```text
Upload Resume
        ↓
Read Resume Content
        ↓
Paste Job Description
        ↓
Send Data to AI API
        ↓
Generate Optimized Resume
        ↓
Display Editable Result
```

---

# 11. Weather API Project

Another project discussed was a Weather Application.

Workflow:

```text
Enter City
      ↓
Weather API
      ↓
Current Weather Data
      ↓
Display Temperature
Humidity
Wind Speed
Conditions
```

Purpose:

* Learn API integration
* Handle JSON responses
* Display dynamic data

---

# 12. Client–Server Communication

Frontend:

* HTML
* CSS
* JavaScript

Backend/API:

* AI model
* Database
* Business logic

Communication occurs through HTTP requests and responses.

---

# 13. Startup & YC Insights

The session also included career guidance inspired by startup thinking.

Key ideas:

* Solve real-world problems.
* Build useful products instead of tutorials.
* Validate ideas with users.
* Focus on execution and iteration.
* Ship projects consistently.

---

# 14. Personal Information Protection

Basic security practices discussed:

* Never expose API keys.
* Store secrets securely (e.g., `.env`).
* Do not commit sensitive information to GitHub.
* Protect personal and user data.

---

# 15. Session 11 Key Takeaways

During this session, you learned how modern web applications work by combining **HTML, CSS, JavaScript, the DOM, event handling, and APIs**. You explored how an **AI Resume Builder** collects user input, communicates with an AI service, and displays optimized results. The session also introduced **client–server architecture**, API-based applications through a Weather API example, startup product thinking, and best practices for protecting sensitive information such as API keys.

---

# 💡 Concepts Learned

* HTML page structure
* Forms and input elements
* DOM (Document Object Model)
* Selecting DOM elements
* DOM manipulation
* JavaScript event handling
* Client–server architecture
* REST API integration
* Resume Builder workflow
* Weather API integration
* HTTP requests and responses
* Dynamic webpage updates
* Secure API key management
* Startup product mindset
* Building interactive frontend applications
