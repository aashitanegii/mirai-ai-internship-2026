# 📒 MirAI Internship – Session 12 Notes

**Session:** Build the Frontend of an AI Resume Optimizer and Connect It to an LLM API

---

# 1. Session Overview

This session focused on building a **frontend AI Resume Optimizer** and integrating it with an LLM API. The discussion covered API usage, frontend development, client-server communication, handling API limitations, image generation APIs, and troubleshooting real-world development issues.

The main project was an **AI Resume Optimizer** that uploads a resume, accepts a job description, sends data to an AI model, and displays an optimized resume.

---

# 2. AI Resume Optimizer Project

The capstone project discussed was an AI Resume Optimizer.

### Features

* Upload Resume (PDF)
* Enter Job Description
* Connect to an LLM API
* Analyze Resume
* Generate optimized resume suggestions
* Display AI-generated output

### Workflow

```text
Upload Resume
      ↓
Extract Resume Text
      ↓
Paste Job Description
      ↓
Send Request to LLM API
      ↓
AI Analysis
      ↓
Optimized Resume
```

---

# 3. Technical Setup

Before connecting AI models, the frontend application must be configured properly.

Typical setup includes:

* HTML
* CSS
* JavaScript
* API configuration
* Environment variables
* API keys

The frontend is responsible for collecting user input and sending requests to the backend or AI service.

---

# 4. Gemini API Rate Limits

The session discussed one common challenge while building AI applications—**API rate limits**.

Key points:

* Free APIs have request limits.
* Too many requests may return errors.
* Developers should handle failures gracefully.
* Consider alternative providers if limits are reached.

---

# 5. Google Maps & Uber Case Study

A real-world case study explained how applications communicate with external APIs.

Example workflow:

```text
User Location
      ↓
Google Maps API
      ↓
Route Calculation
      ↓
Distance & ETA
      ↓
Uber App Display
```

The purpose was to understand how modern applications combine multiple APIs.

---

# 6. Client–Server Architecture

The communication between frontend and backend follows a client-server model.

```text
Client (Browser)
        ↓
HTTP Request
        ↓
Server / AI API
        ↓
Processing
        ↓
HTTP Response
        ↓
Client Display
```

The frontend should never directly expose sensitive credentials.

---

# 7. Endpoints

An endpoint is a specific URL used to access an API.

Example:

```text
Frontend
      ↓
API Endpoint
      ↓
AI Model
```

Different endpoints perform different tasks such as generating text or creating images.

---

# 8. API Keys

API keys authenticate requests to external services.

Best practices:

* Store keys securely.
* Use `.env` files.
* Never upload API keys to GitHub.
* Keep credentials private.

---

# 9. OpenRouter

The session introduced **OpenRouter** as an alternative platform for accessing multiple AI models.

Benefits:

* Access to various LLMs.
* Free model options.
* Single API interface.
* Useful when another provider reaches its limits.

---

# 10. Hugging Face APIs

The session demonstrated Hugging Face APIs for AI tasks.

Possible use cases:

* Image generation
* NLP models
* Open-source AI models
* Model inference

These APIs can be integrated similarly to Gemini.

---

# 11. Resume Optimizer Planning

Before coding, the application's requirements were planned.

Main requirements:

* Resume upload
* Job description input
* Resume analysis
* AI-generated suggestions
* Editable output
* Clean user interface

Planning before implementation helps organize development.

---

# 12. Initial Web Page Development

The frontend structure was created using:

* HTML
* CSS
* JavaScript

The interface included:

* File upload
* Text area
* Generate button
* Output section

---

# 13. Resume Analyzer Requirements

The AI Resume Optimizer should evaluate:

* Skills
* Keywords
* Resume sections
* Job-description relevance
* ATS compatibility
* Overall resume quality

---

# 14. HTML, CSS & JavaScript Files

The project was divided into separate files.

Typical structure:

```text
index.html
style.css
script.js
```

Each file has a different responsibility:

* HTML → Structure
* CSS → Styling
* JavaScript → Functionality

---

# 15. API Integration

The frontend sends collected data to the AI model.

Workflow:

```text
User Input
      ↓
JavaScript
      ↓
API Request
      ↓
LLM
      ↓
AI Response
      ↓
Display Result
```

---

# 16. Testing API Integration

The session emphasized testing API requests.

Common checks:

* Correct endpoint
* Valid API key
* Proper request format
* Successful response
* Error handling

---

# 17. Troubleshooting API Errors

Developers should be prepared for issues such as:

* Invalid API keys
* Rate limits
* Missing request data
* Incorrect endpoints
* Model unavailable
* Network failures

Applications should display helpful error messages instead of crashing.

---

# 18. Displaying AI Responses

After receiving a successful response:

```text
API Response
      ↓
Parse JSON
      ↓
Extract Generated Text
      ↓
Update HTML
```

The webpage dynamically displays AI-generated content without reloading.

---

# 19. Hugging Face Image Generation

Besides text generation, Hugging Face APIs can also generate images.

Workflow:

```text
Prompt
      ↓
Image Generation API
      ↓
Generated Image
      ↓
Display on Webpage
```

---

# 20. Career & Industry Insights

The instructor also shared advice on:

* Learning by building projects.
* Understanding system design instead of only syntax.
* Working with APIs and AI tools.
* Developing practical software engineering skills.
* Staying adaptable as AI technologies evolve.

---

# 21. Session 12 Key Takeaways

This session demonstrated how to connect a frontend web application with an LLM API to create an **AI Resume Optimizer**. You learned about **API integration, client-server communication, endpoints, API keys, OpenRouter, Hugging Face APIs, frontend development with HTML/CSS/JavaScript, testing, debugging, and handling real-world API issues**. The session also highlighted planning applications before coding and emphasized practical engineering skills for AI-powered software development.

---

# 💡 Concepts Learned

* AI Resume Optimizer architecture
* Frontend development (HTML, CSS, JavaScript)
* Client–server architecture
* API endpoints
* HTTP requests & responses
* API key management
* Gemini API limitations
* OpenRouter for multiple AI models
* Hugging Face APIs
* Image generation APIs
* Resume analysis workflow
* Frontend project structure
* API integration & testing
* Error handling and debugging
* JSON response processing
* Building production-ready AI applications
