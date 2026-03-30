# Individual Contribution Writeups

Use these drafts in the same structure as the screenshot you shared. Replace the placeholder roll numbers for members other than Shubh before final submission.

## 1. Shubh Agnihotri

**ADAPTIVE RESUME SCREENER**  
**SHUBH AGNIHOTRI**  
Roll No. 2305336

**Abstract:** This report presents the Adaptive Resume Screener, an end-to-end prototype that combines explainable resume analysis with a lightweight PyTorch machine learning model. The system accepts a resume and a target job description, computes ATS-style and semantic matching signals, produces a shortlist recommendation, stores the result in SQLite, and supports feedback collection for future adaptive retraining.

**Individual contribution and findings:** Shubh took primary responsibility as the Project Lead and also handled the system integration role while sharing ownership of the machine learning and feature engineering components. He coordinated the overall project structure, aligned the work of different modules, connected the frontend, backend, machine learning pipeline, and database flow into one complete working system, and prepared the high-level architecture narrative used across the report and viva. On the technical side, he contributed to the model-oriented parts of the project by covering the six-feature screening logic, the `ResumeNet` inference flow, threshold-based decision making, evaluation understanding, and the adaptive retraining pipeline in `feedback_loop/`. His findings emphasized that a hybrid approach combining heuristic scoring with a compact interpretable model gave better academic value than a purely black-box system.

**Individual contribution to project report preparation:** Contributed to the project overview, system architecture, machine learning workflow, and limitations or future work sections. Helped prepare architecture explanations, flow descriptions, and the final technical positioning of the project as an explainable academic prototype.

**Individual contribution for project presentation and demonstration:** Presented the problem statement, motivation, high-level architecture, and end-to-end system flow. Supported the explanation of feature engineering, model logic, retraining readiness, and the concluding discussion during the project viva.

Full Signature of Supervisor: ____________________________

Full Signature of Student: ______________________________

---

## 2. Aditya

**ADAPTIVE RESUME SCREENER**  
**ADITYA**  
Roll No. 2305678

**Abstract:** This report presents the Adaptive Resume Screener, a complete prototype for resume shortlisting that integrates frontend interaction, backend processing, machine learning inference, and result persistence. The system is designed to produce readable, explainable screening output through score interpretation, extracted feature display, and feedback-driven improvement support.

**Individual contribution and findings:** Aditya handled the system integration part and also co-owned the frontend and demo flow. He focused on keeping the system understandable from a user and presentation perspective by linking the project overview with the live workflow used in demonstration. His contribution covered the integration of user interaction with backend processing, including how the browser submits resume and job description data, how the backend is invoked, how the different modules work together in sequence, and how the final output is shown as a smooth demo sequence. His findings highlighted that strong integration and presentation continuity were essential for turning multiple technical components into a coherent end-to-end product.

**Individual contribution to project report preparation:** Contributed to the problem statement, objectives, integration workflow, and user-facing system explanation. Helped write the sections that connect frontend interaction with backend processing and supported the demo-oriented narrative used in the report.

**Individual contribution for project presentation and demonstration:** Presented the integrated system story, explained the transition from architecture to live demo, and supported the walkthrough of the web-based analysis flow. Helped ensure that the presentation moved clearly from concept to working implementation.

Full Signature of Supervisor: ____________________________

Full Signature of Student: ______________________________

---

## 3. Mrinalendu

**ADAPTIVE RESUME SCREENER**  
**MRINALENDU**  
Roll No. 2305139

**Abstract:** This report presents the Adaptive Resume Screener, a practical web-based screening prototype that allows a user to upload a resume, provide a job description, and receive a transparent recommendation with supporting metrics. The system also stores predictions and feedback for later analysis and improvement.

**Individual contribution and findings:** Mrinalendu shared ownership of the frontend and demo flow and also handled database, testing, and deployment support responsibilities. He focused on the user-facing experience by covering how the interface accepts inputs, displays scores and keyword insights, and captures feedback from the website. In addition, he supported the operational side of the project by understanding where results are stored, how the application is run for demonstration, and how deployment and test readiness improve presentation confidence. His findings showed that a clean interface and reliable demo setup are just as important as the model itself when presenting an applied software project.

**Individual contribution to project report preparation:** Contributed to the frontend design, UI workflow, screenshot-based explanation, feedback interaction, and deployment-oriented report sections. Supported documentation related to the user journey from file upload to result display and feedback submission.

**Individual contribution for project presentation and demonstration:** Demonstrated the web interface, including resume upload, job description entry, result rendering, and feedback submission. Also supported explanation of database visibility, deployment basics, and demo readiness during the project presentation.

Full Signature of Supervisor: ____________________________

Full Signature of Student: ______________________________

---

## 4. Harshit

**ADAPTIVE RESUME SCREENER**  
**HARSHIT**  
Roll No. 2305702

**Abstract:** This report presents the Adaptive Resume Screener, a full-stack prototype built with FastAPI, SQLite, and a PyTorch screening model to demonstrate an explainable resume evaluation workflow. The project includes API design, file validation, structured JSON responses, persistence, testing, and Docker-based execution support.

**Individual contribution and findings:** Harshit shared responsibility for the backend and API implementation as well as database, testing, and deployment preparation. His contribution centered on understanding and presenting how the FastAPI backend accepts input, validates requests, parses resumes, triggers analysis and prediction services, and stores both screening output and user feedback in SQLite. He also contributed to the database and operational reliability side by covering schema understanding, test coverage, and how Docker can be used to start the full stack for demonstration. His findings emphasized that modular route, schema, and service separation made the backend easier to explain, test, and troubleshoot.

**Individual contribution to project report preparation:** Contributed to the backend design, API endpoint explanation, database operation flow, validation logic, and testing sections of the report. Also supported the documentation of deployment steps and persistence behavior.

**Individual contribution for project presentation and demonstration:** Presented the FastAPI request flow, endpoint responsibilities, validation logic, and database write path. Supported the viva discussion on how predictions and feedback are stored, how tests improve confidence, and how the application can be run reliably during a live demo.

Full Signature of Supervisor: ____________________________

Full Signature of Student: ______________________________

---

## 5. Ritik

**ADAPTIVE RESUME SCREENER**  
**RITIK**  
Roll No. 2305320

**Abstract:** This report presents the Adaptive Resume Screener, an explainable machine learning driven prototype for resume-job matching. The system combines heuristic keyword and semantic analysis with a lightweight neural network model to generate a readable shortlist recommendation and support future improvement through a feedback loop.

**Individual contribution and findings:** Ritik shared ownership of the backend and API layer and also handled machine learning and feature engineering responsibilities. His contribution focused on the technical connection between resume analysis and model inference, including the six engineered input features, heuristic score generation, threshold-based decision logic, and the way backend services pass structured data into the PyTorch screening model. He also contributed to understanding the evaluation metrics and adaptive retraining readiness pipeline so that the project could be explained as an end-to-end learning system rather than only a static predictor. His findings showed that interpretable feature engineering helped keep the model understandable, fast, and suitable for an academic prototype.

**Individual contribution to project report preparation:** Contributed to the machine learning pipeline, feature engineering, scoring logic, evaluation metrics, and adaptive retraining sections of the report. Also supported the explanation of backend-to-model integration and the logic behind the final recommendation.

**Individual contribution for project presentation and demonstration:** Presented the six input features, model decision logic, threshold reasoning, performance metrics, and retraining readiness mechanism. Supported the explanation of how backend services and model inference work together to generate the final shortlist or reject decision.

Full Signature of Supervisor: ____________________________

Full Signature of Student: ______________________________
