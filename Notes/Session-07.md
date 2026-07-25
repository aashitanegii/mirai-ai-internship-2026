# 📒 MirAI Internship – Session 7 Notes
## Topic - Git, GitHub, Version Control, Deployment & GitHub Profile Assignment

---

## 1. Introduction & Session Overview — 23:08

The session focused on moving beyond simply writing code toward understanding how software is **managed, versioned, shared, deployed, and presented professionally**.

The broader workflow is:

```text
Write Code
   ↓
Version Control
   ↓
Git
   ↓
GitHub
   ↓
Deployment
   ↓
Cloud / Live Application
   ↓
Developer Portfolio
```

A developer does not only need working code. They also need to manage changes safely, collaborate, deploy applications, and showcase their work professionally.

---

# 2. Understanding Version Control — 28:48

**Version Control** is a system for tracking changes made to source code over time.

Instead of maintaining files such as:

```text
app.py
app_final.py
app_final2.py
app_final_REAL.py
```

version control maintains an organized history of the project.

It allows developers to:

* Track changes in code.
* Restore previous working versions.
* Experiment without destroying stable code.
* Understand who changed what.
* Collaborate with multiple developers.
* Maintain different versions/features simultaneously.

### Core idea shown in the session

The instructor illustrated development as different timelines originating from a stable **base/source of truth**.

```text
BASE / TRUTH
     |
     ├──────── working version
     |
     ├──────── second approach
     |
     └──────── third approach
```

Different approaches can evolve separately and later be combined through **merging**.

---

# 3. Importance of Version Control in Coding — 35:08

Without version control, changing an application directly can create situations like:

```text
Working App
    ↓
make changes
    ↓
something breaks
    ↓
"wrong app crashes / I have to fix everything"
```

The session emphasized maintaining a reliable **base level of code / source of truth**.

Instead of modifying the only working copy, developers can create different development timelines.

For example:

```text
BASE (TRUTH)
      |
      ├── Approach 1
      |
      ├── Approach 2 ✓
      |
      └── Approach 3
```

The successful approach can then be brought back into the main codebase.

### Merging

**Merging** means combining changes from different development histories/branches into another branch.

This allows experimentation while protecting the stable version of the application.

---

# 4. Introduction to Git and Its Creator — 42:43

**Git** is a distributed version-control system used to track changes in source code.

Git allows developers to:

* Create repositories.
* Track modifications.
* Create commits.
* Maintain development history.
* Work with branches.
* Merge changes.
* Revert to earlier versions.
* Collaborate safely.

Git was created by **Linus Torvalds**, who also created the Linux kernel.

### Git vs GitHub

They are related but not identical.

```text
Git
→ Version-control technology
→ Runs locally
→ Tracks code history

GitHub
→ Online platform built around Git
→ Hosts repositories remotely
→ Enables sharing and collaboration
→ Acts as a developer portfolio
```

---

# 5. The Concept of Deployment — 47:42

Writing an application locally does not automatically make it available to users.

**Deployment** is the process of taking an application from the developer's local environment and making it accessible through another environment/server, usually over the internet.

```text
Local Code
     ↓
Repository
     ↓
Deployment Platform / Cloud
     ↓
Live Application
     ↓
Users
```

Development and deployment are therefore different stages.

A program working on:

```text
localhost
```

means it works on your own machine.

A deployed application can be accessed by other users through a public address.

---

# 6. Setting Up Git and GitHub — 59:58

A typical Git workflow begins by installing/configuring Git and connecting your local development environment with GitHub.

Important concepts include:

```text
Repository
Commit
Branch
Remote
Push
Pull
Merge
```

### Basic workflow

```text
Working Directory
      ↓
git add
      ↓
Staging Area
      ↓
git commit
      ↓
Local Git Repository
      ↓
git push
      ↓
GitHub Repository
```

Useful commands:

```bash
git status
git add .
git commit -m "commit message"
git push origin main
```

`git status` checks the current repository state.

`git add` stages changes.

`git commit` creates a recorded snapshot.

`git push` sends local commits to the remote repository.

---

# 7. Deploying Applications to the Cloud — 1:35:42

Cloud deployment makes locally developed applications accessible online.

For applications such as Streamlit projects, the general architecture is:

```text
Local Project
      ↓
Git
      ↓
GitHub Repository
      ↓
Cloud Deployment Service
      ↓
Public Application
```

The repository becomes the source from which the deployment platform obtains the application's code.

Deployment also introduces practical engineering concerns such as:

* Dependencies.
* Environment configuration.
* API keys/secrets.
* Repository structure.
* Entry files.
* Updating deployed applications when code changes.

### Important security principle

API keys and credentials should **not be committed publicly to GitHub**.

Secrets should instead be handled through environment variables or the deployment platform's secret-management system.

---

# 8. Final Adjustments and Updates — 1:52:15

Before considering an application/repository complete, developers should review:

* File organization.
* Dependencies.
* Configuration.
* README/documentation.
* Repository status.
* Git history.
* Deployment configuration.
* Secrets/API keys.
* Whether the live application reflects the newest code.

This represents the transition from simply getting something to work to making the project presentable and maintainable.

---

# 9. Understanding GitHub Basics — 1:55:18

GitHub is more than code storage.

A GitHub profile can demonstrate:

* Projects.
* Technical skills.
* Contributions.
* Commit activity.
* Open-source work.
* Documentation ability.
* Developer identity.

For students, GitHub effectively acts as a **modern technical resume**.

A recruiter or senior engineer visiting a profile should quickly understand:

```text
Who are you?
What technologies do you use?
What are you building?
What have you contributed?
How active are you?
```

This idea leads directly into **Assignment 6**.

---

# 10. Career Guidance & Skills Discussion — 1:58:54

The session connected technical work with career development.

Learning programming alone is not enough; students should also learn how to **demonstrate evidence of their skills**.

GitHub provides proof through:

* Real repositories.
* Commit history.
* Projects.
* Open-source contributions.
* README documentation.
* Deployed applications.
* Technical profile presentation.

The goal is to gradually build a developer identity rather than waiting until placement season to create one.

---

# 11. Session Wrap-Up & Personal Interests — 2:02:16

The session concluded by connecting technical learning with students' own interests and development paths.

Projects and GitHub profiles can reflect personal interests while still remaining technically credible.

A strong developer profile should therefore have both:

```text
Technical competence + Individual personality
```

rather than looking like a generic collection of coursework.

---

# 12. Next Steps & Future Topics — 2:05:19

The next stage is applying the session concepts practically:

```text
Learn Git
→ Maintain repositories
→ Push projects
→ Deploy applications
→ Improve GitHub
→ Build technical credibility
```

Assignment 6 specifically focuses on the **GitHub-profile/portfolio side** of this process.

---

# Assignment 6 — Hacker-Style GitHub Developer Profile

## Objective

Transform the main GitHub profile into a custom developer landing page inspired by terminal/system-fetch tools such as **neofetch**.

The profile should communicate:

* Personality.
* Technical skills.
* Creativity.
* Developer activity.
* Projects/interests.

---

## Task 1 — Unlock the Special GitHub Profile Repository

GitHub has a special profile README feature.

Create a repository whose name is **exactly identical to the GitHub username**.

For example, for username:

```text
aashitanegii
```

create:

```text
aashitanegii/aashitanegii
```

GitHub should recognize it as a special profile repository.

While creating it:

```text
✓ Add a README file
```

The contents of this README automatically appear on the user's main GitHub profile.

---

# Task 2 — Build the Terminal Canvas

Edit `README.md` and remove the default content.

The assignment requires the primary profile design to be placed inside a Markdown monospaced code block:

````markdown
```text
Terminal profile goes here
```
````

Using `text` preserves spacing and gives the profile the terminal-like appearance needed for ASCII layouts.

This is particularly important because ASCII artwork depends on every character occupying consistent horizontal space.

---

# Task 3 — AI-Powered ASCII Art

The profile needs an **ASCII-art portrait/avatar/logo**.

Possible methods:

* Use a headshot with an image-to-ASCII converter.
* Search for an Image-to-ASCII generator.
* Generate a logo/avatar using an AI tool.
* Manually create ASCII artwork.

Example concept:

```text
⠀⠀⣀⣼⠷⠀⠀⠁⢀⣿⠃⠀⠀⢀⣿⣿⣿⣇
⠴⣾⣯⣤⣤⣤⣤⣤⣿⠀⠀⠀⠀⣿⣿⣿⣿⣿
```

Spacing must be preserved carefully.

---

# Task 4 — System Info Bio

Beside the ASCII art, create information formatted like output from a system-fetch utility.

Assignment examples include:

```text
OS: ............ Windows
Uptime: ........ 19 years, X months
Kernel: ........ MirAI B.Tech Student
Languages: ..... Python, JavaScript, C++
Hobbies: ....... AI Engineering, Gaming, Robotics
Contact: ....... your.email@example.com
```

The dots/dashes visually align the fields.

The information should ideally reflect the developer's **real skills and interests**, rather than copying the sample literally.

For your profile, fields could instead represent things such as:

```text
OS
Education
Focus
Languages
Frameworks
AI
Tools
Projects
Interests
Currently Learning
Contact
```

---

# Task 5 — Dynamic GitHub Statistics

The profile must contain live GitHub statistics.

The assignment specifically asks students to research the open-source **GitHub Readme Stats by Anurag Hazra** project.

Unlike the terminal block, the stats card should be placed **outside** the `text` code block because it is rendered as a Markdown image.

The card can dynamically display GitHub activity such as:

* Commits.
* Pull requests/activity where supported by the chosen cards.
* Stars.
* Contributions/statistics.
* Languages/repository information depending on configuration.

Because the card is dynamically generated, the profile can update as GitHub activity changes.

---

# Why Dynamic Stats Matter

Static README:

```text
"I use GitHub."
```

Dynamic developer profile:

```text
Actual GitHub activity
        ↓
Open-source stats service
        ↓
Automatically generated card
        ↓
Displayed on profile
```

It turns developer activity into visible evidence rather than simply claiming experience.

---

# LinkedIn Deliverable

After finishing the README:

1. Open the **main GitHub profile page**.
2. Verify the terminal profile renders correctly.
3. Take a high-quality screenshot.
4. Create a LinkedIn post about customizing the GitHub developer landing page.
5. Discuss using:

   * Markdown
   * ASCII art
   * GitHub profile README functionality
   * Open-source dynamic statistics
6. Include the screenshot.
7. Include the direct GitHub profile link.
8. Tag **MirAI School of Technology**.

Since the internship is still ongoing, the post can frame this as another step in the ongoing AI Builder internship rather than an internship-completion post.

---

# Submission

Unlike Assignment 5, **you are not submitting `app.py` or a recording for this assignment.**

The student portal requires the:

**Live link to your MAIN GitHub profile.**

So the submitted destination should be your profile, not merely the special README repository.

---

# Final Checklist

* [ ] Special repository name exactly matches GitHub username
* [ ] README initialized
* [ ] Main design uses a `text` Markdown code block
* [ ] Terminal/neofetch aesthetic
* [ ] ASCII artwork included
* [ ] System-information bio included
* [ ] Skills/languages included
* [ ] Contact information included
* [ ] Dynamic GitHub Stats integrated
* [ ] Stats render successfully
* [ ] ASCII spacing is intact
* [ ] Profile README appears on main GitHub profile
* [ ] High-quality screenshot taken
* [ ] LinkedIn post drafted/published
* [ ] MirAI School of Technology tagged
* [ ] Main GitHub profile URL submitted
* [ ] Assignment completed before **July 27, 2026, 11:59 PM**

### Biggest takeaway

This session tied together a really important engineering progression:

```text
CODE
 ↓
VERSION CONTROL
 ↓
GIT
 ↓
GITHUB
 ↓
DEPLOYMENT
 ↓
PORTFOLIO
 ↓
CAREER
```

The code is the product, **Git protects its history, GitHub proves the work, deployment lets people use it, and the profile makes that work discoverable.**
