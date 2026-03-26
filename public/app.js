const LOCAL_HOSTS = new Set(["", "localhost", "127.0.0.1"]);

const API_BASE_URL = (() => {
  const configuredBaseUrl = document
    .querySelector('meta[name="api-base-url"]')
    ?.getAttribute("content")
    ?.trim();

  if (configuredBaseUrl) {
    return configuredBaseUrl.replace(/\/+$/, "");
  }

  const { hostname, origin, protocol } = window.location;
  if (LOCAL_HOSTS.has(hostname)) {
    const localHostname = hostname || "127.0.0.1";
    const localProtocol = protocol === "file:" ? "http:" : protocol;
    return `${localProtocol}//${localHostname}:8000`;
  }

  return origin.replace(/\/+$/, "");
})();

const FEATURE_LABELS = {
  years_experience: "Years of experience",
  skills_match_score: "Skills match score",
  education_level: "Education level",
  project_count: "Project count",
  resume_length: "Resume length",
  github_activity: "GitHub activity",
};

const form = document.getElementById("analyze-form");
const resultDiv = document.getElementById("result");
const submitButton = document.getElementById("submit-button");
const jobDescriptionInput = document.getElementById("job_description");
const resumeInput = document.getElementById("resume");
const fileMeta = document.getElementById("file-meta");

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function showResult(html, isError = false) {
  resultDiv.classList.remove("hidden");
  resultDiv.classList.toggle("error", isError);
  resultDiv.innerHTML = html;
  requestAnimationFrame(() => {
    resultDiv.scrollIntoView({ behavior: "smooth", block: "start" });
  });
}

function formatNumber(value, digits = 2) {
  const numeric = Number(value);
  if (Number.isNaN(numeric)) {
    return escapeHtml(value);
  }
  return numeric.toFixed(digits);
}

function clampPercent(value, max = 100) {
  return Math.max(0, Math.min(Number(value) || 0, max));
}

function getErrorMessage(error, fallback = "Request failed") {
  return error instanceof Error && error.message ? error.message : fallback;
}

async function readJson(response) {
  const text = await response.text();
  if (!text) {
    return {};
  }

  try {
    return JSON.parse(text);
  } catch (error) {
    throw new Error(text);
  }
}

function renderKeywords(items, emptyLabel, tone) {
  if (!items || items.length === 0) {
    return `<p class="empty-copy">${escapeHtml(emptyLabel)}</p>`;
  }

  return `
    <div class="tag-list">
      ${items.map((item) => `<span class="tag ${tone}">${escapeHtml(item)}</span>`).join("")}
    </div>
  `;
}

function renderFeatureList(features) {
  const entries = Object.entries(features || {});
  if (entries.length === 0) {
    return `<p class="empty-copy">No extracted features available.</p>`;
  }

  return `
    <div class="feature-list">
      ${entries
        .map(([key, value]) => {
          const label = FEATURE_LABELS[key] || key.replaceAll("_", " ");
          return `
            <div class="feature-row">
              <span>${escapeHtml(label)}</span>
              <strong>${escapeHtml(formatNumber(value, 2))}</strong>
            </div>
          `;
        })
        .join("")}
    </div>
  `;
}

function renderMetricCard(label, value, accentWidth, hint, toneClass) {
  return `
    <article class="metric-card ${toneClass}">
      <p class="metric-label">${escapeHtml(label)}</p>
      <p class="metric-value">${escapeHtml(value)}</p>
      <div class="metric-bar">
        <span style="width: ${clampPercent(accentWidth)}%"></span>
      </div>
      <p class="metric-hint">${escapeHtml(hint)}</p>
    </article>
  `;
}

function updateFileMeta() {
  const file = resumeInput.files[0];
  if (!file) {
    fileMeta.textContent = "No file selected yet.";
    return;
  }

  const sizeInKb = Math.max(1, Math.round(file.size / 1024));
  fileMeta.textContent = `${file.name} - ${sizeInKb} KB`;
}

resumeInput.addEventListener("change", updateFileMeta);

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const resumeFile = resumeInput.files[0];
  const jobDescription = jobDescriptionInput.value.trim();

  if (!resumeFile) {
    showResult("Please upload a resume file before starting the analysis.", true);
    return;
  }

  if (!jobDescription) {
    showResult("Please paste a job description to compare against the resume.", true);
    return;
  }

  const body = new FormData();
  body.append("resume", resumeFile);
  body.append("job_description", jobDescription);

  submitButton.disabled = true;
  submitButton.textContent = "Analyzing...";

  showResult(`
    <div class="loading-state">
      <div class="loading-stack">
        <div class="loading-orb"></div>
        <div class="loading-bar"></div>
      </div>
      <div>
        <p class="section-kicker">Processing</p>
        <h2>Building the screening summary</h2>
        <p class="loading-copy">Parsing the resume, matching skills, measuring semantic alignment, and preparing the final recommendation.</p>
      </div>
    </div>
  `);

  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: "POST",
      body,
    });

    const data = await readJson(response);

    if (!response.ok) {
      showResult(`Error: ${escapeHtml(data.detail || "Request failed")}`, true);
      return;
    }

    const decisionClass = data.decision === "shortlist" ? "outcome-shortlist" : "outcome-reject";
    const decisionLabel = data.decision === "shortlist" ? "Shortlisted" : "Needs Improvement";
    const decisionMessage = data.decision === "shortlist"
      ? "This profile aligns well with the target role and clears the current screening threshold."
      : "The profile shows some strengths, but the current role description still has gaps or lower alignment.";

    showResult(`
      <div class="result-banner ${decisionClass}">
        <div class="result-copy">
          <p class="section-kicker">Screening Result</p>
          <h2>${escapeHtml(decisionLabel)}</h2>
          <p class="banner-copy">${escapeHtml(decisionMessage)}</p>
        </div>

        <div class="summary-grid">
          <article class="summary-token">
            <span>Prediction ID</span>
            <strong>${escapeHtml(data.prediction_id)}</strong>
          </article>
          <article class="summary-token">
            <span>Confidence</span>
            <strong>${escapeHtml(formatNumber(data.probability, 4))}</strong>
          </article>
          <article class="summary-token">
            <span>Threshold</span>
            <strong>${escapeHtml(formatNumber(data.threshold, 2))}</strong>
          </article>
        </div>
      </div>

      <div class="metric-grid">
        ${renderMetricCard("ATS-Style Score", formatNumber(data.ats_score, 2), data.ats_score, "Heuristic keyword coverage and section quality", "tone-ats")}
        ${renderMetricCard("Semantic Score", formatNumber(data.semantic_score, 4), Number(data.semantic_score) * 100, "Meaning-level similarity with the role", "tone-semantic")}
        ${renderMetricCard("Final Score", formatNumber(data.final_score, 2), data.final_score, "Overall screening fit", "tone-final")}
      </div>

      <div class="insight-grid">
        <article class="insight-card">
          <h3>Matched Strengths</h3>
          ${renderKeywords(data.matched_keywords, "No strong keyword matches were detected.", "tag-good")}
        </article>

        <article class="insight-card">
          <h3>Missing Requirements</h3>
          ${renderKeywords(data.missing_keywords, "No tracked gaps found for this role description.", "tag-warn")}
        </article>

        <article class="insight-card">
          <h3>Extracted Features</h3>
          ${renderFeatureList(data.extracted_features)}
        </article>
      </div>

      <article class="explanation-panel">
        <p class="section-kicker">Why This Result Appeared</p>
        <h3>Screening Summary</h3>
        <p>${escapeHtml(data.explanation || "")}</p>
        <p class="support-copy">Use this as a heuristic screening aid rather than a final hiring decision.</p>
      </article>

      <article class="feedback-panel">
        <p class="section-kicker">Help Us Improve</p>
        <h3>Was this recommendation accurate?</h3>
        <p class="feedback-intro">Your feedback helps us retrain and improve the screening model over time.</p>

        <form id="feedback-form" class="feedback-form">
          <div class="feedback-buttons">
            <button type="button" class="feedback-btn feedback-correct" data-label="1">
              <span class="feedback-icon">&#10003;</span>
              <span class="feedback-text">Correct</span>
              <span class="feedback-subtext">The recommendation was accurate</span>
            </button>
            <button type="button" class="feedback-btn feedback-incorrect" data-label="0">
              <span class="feedback-icon">&#10007;</span>
              <span class="feedback-text">Incorrect</span>
              <span class="feedback-subtext">The recommendation was wrong</span>
            </button>
          </div>

          <label class="feedback-note-field">
            <span class="field-label">Optional: Add a note</span>
            <textarea id="feedback-note" class="feedback-note" placeholder="Why do you think this was correct or incorrect? (optional)" rows="3"></textarea>
          </label>

          <button type="submit" id="feedback-submit-button" class="feedback-submit-button" disabled>
            Submit Feedback
          </button>

          <div id="feedback-status" class="feedback-status hidden"></div>
        </form>
      </article>
    `);

    const feedbackForm = document.getElementById("feedback-form");
    const feedbackButtons = feedbackForm.querySelectorAll(".feedback-btn");
    const feedbackSubmitButton = document.getElementById("feedback-submit-button");
    const feedbackStatus = document.getElementById("feedback-status");
    let selectedLabel = null;

    feedbackButtons.forEach((button) => {
      button.addEventListener("click", (clickEvent) => {
        clickEvent.preventDefault();
        selectedLabel = button.dataset.label;
        feedbackButtons.forEach((feedbackButton) => feedbackButton.classList.remove("selected"));
        button.classList.add("selected");
        feedbackSubmitButton.disabled = false;
      });
    });

    feedbackForm.addEventListener("submit", async (submitEvent) => {
      submitEvent.preventDefault();

      if (selectedLabel === null) {
        feedbackStatus.classList.remove("hidden");
        feedbackStatus.classList.remove("success");
        feedbackStatus.classList.add("error");
        feedbackStatus.textContent = "Please select 'Correct' or 'Incorrect' before submitting.";
        return;
      }

      const feedbackNote = document.getElementById("feedback-note").value.trim();
      let submissionSucceeded = false;

      feedbackSubmitButton.disabled = true;
      feedbackSubmitButton.textContent = "Submitting...";
      feedbackStatus.classList.add("hidden");
      feedbackStatus.classList.remove("error", "success");

      try {
        const feedbackResponse = await fetch(`${API_BASE_URL}/feedback/${data.prediction_id}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            reviewed_label: parseInt(selectedLabel, 10),
            feedback_note: feedbackNote || null,
          }),
        });

        if (!feedbackResponse.ok) {
          const errorBody = await readJson(feedbackResponse);
          throw new Error(errorBody.detail || "Failed to submit feedback");
        }

        const feedbackResult = await readJson(feedbackResponse);
        submissionSucceeded = true;
        const hasProgressInfo = Number.isInteger(feedbackResult.labeled_feedback_count)
          && Number.isInteger(feedbackResult.minimum_required);
        const progressMessage = hasProgressInfo
          ? `<p>${escapeHtml(feedbackResult.labeled_feedback_count)} reviewed samples saved out of ${escapeHtml(feedbackResult.minimum_required)} needed for retraining.</p>`
          : "";

        feedbackStatus.classList.remove("hidden");
        feedbackStatus.classList.remove("error");
        feedbackStatus.classList.add("success");
        feedbackStatus.innerHTML = `
          <p><strong>&#10003; Feedback received!</strong></p>
          <p>Thank you for helping improve our screening model.</p>
          ${progressMessage}
          ${feedbackResult.retrain_available ? '<p class="retrain-notice">Enough feedback is available to retrain the model.</p>' : ""}
        `;

        feedbackButtons.forEach((feedbackButton) => {
          feedbackButton.disabled = true;
        });
        feedbackForm.style.opacity = "0.6";
        feedbackSubmitButton.textContent = "Feedback Submitted";
      } catch (error) {
        feedbackStatus.classList.remove("hidden");
        feedbackStatus.classList.remove("success");
        feedbackStatus.classList.add("error");
        feedbackStatus.textContent = `Error: ${escapeHtml(getErrorMessage(error))}`;
        feedbackSubmitButton.disabled = false;
        feedbackSubmitButton.textContent = "Submit Feedback";
      } finally {
        if (submissionSucceeded) {
          feedbackSubmitButton.disabled = true;
        }
      }
    });
  } catch (error) {
    showResult(`Error: ${escapeHtml(getErrorMessage(error))}`, true);
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Analyze Resume";
  }
});
