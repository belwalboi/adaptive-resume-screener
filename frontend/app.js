const API_BASE_URL = window.location.hostname === "localhost"
  ? "http://localhost:8000"
  : "http://backend:8000";

const form = document.getElementById("analyze-form");
const resultDiv = document.getElementById("result");

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
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const resumeFile = document.getElementById("resume").files[0];
  const jobDescription = document.getElementById("job_description").value.trim();

  if (!resumeFile) {
    showResult("Please upload a resume file.", true);
    return;
  }

  if (!jobDescription) {
    showResult("Job description is required.", true);
    return;
  }

  const body = new FormData();
  body.append("resume", resumeFile);
  body.append("job_description", jobDescription);

  const button = form.querySelector("button");
  button.disabled = true;
  button.textContent = "Analyzing...";

  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: "POST",
      body,
    });

    const data = await response.json();

    if (!response.ok) {
      showResult(`Error: ${escapeHtml(data.detail || "Request failed")}`, true);
      return;
    }

    const matched = (data.matched_keywords || []).slice(0, 12).join(", ");
    const missing = (data.missing_keywords || []).slice(0, 12).join(", ");

    showResult(`
      <h3>Screening Result</h3>
      <p><strong>Prediction ID:</strong> ${escapeHtml(data.prediction_id)}</p>
      <p><strong>Decision:</strong> ${escapeHtml(data.decision)} (${escapeHtml(data.probability)})</p>
      <p><strong>ATS Score:</strong> ${escapeHtml(data.ats_score)}</p>
      <p><strong>Semantic Score:</strong> ${escapeHtml(data.semantic_score)}</p>
      <p><strong>Final Score:</strong> ${escapeHtml(data.final_score)}</p>
      <p><strong>Matched Keywords:</strong> ${escapeHtml(matched || "None")}</p>
      <p><strong>Missing Keywords:</strong> ${escapeHtml(missing || "None")}</p>
      <p><strong>Explanation:</strong> ${escapeHtml(data.explanation || "")}</p>
    `);
  } catch (error) {
    showResult(`Error: ${escapeHtml(error.message)}`, true);
  } finally {
    button.disabled = false;
    button.textContent = "Analyze Resume";
  }
});
