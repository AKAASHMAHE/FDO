import { useEffect, useState } from "react";

const API_URL = "http://127.0.0.1:8000";

/* =========================================================
   UI Helpers
   ========================================================= */

function StatusBadge({ status }) {
  const normalized = (status || "UNKNOWN").toLowerCase();

  return (
    <span className={`status-badge ${normalized}`}>
      {status}
    </span>
  );
}

function MetricCard({ value, label, type }) {
  return (
    <div className={`metric-card ${type || ""}`}>
      <div className="metric-value">{value}</div>
      <div className="metric-label">{label}</div>
    </div>
  );
}

/* =========================================================
   Semantic Resource Formatting
   ========================================================= */

function formatSemanticResource(value) {
  if (value === null || value === undefined) {
    return "Unknown";
  }

  const text = String(value).trim();

  if (!text) {
    return "Unknown";
  }

  // FUNCTION URI
  const functionMatch = text.match(
    /\/resource\/function\/(.+)$/
  );

  if (functionMatch) {
    return formatFunctionName(functionMatch[1]);
  }

  // EXPECTED DATA URI
  const expectedDataMatch = text.match(
    /\/resource\/expected-data\/(.+)$/
  );

  if (expectedDataMatch) {
    return expectedDataMatch[1];
  }

  // DECLARED DATA URI
  const declaredDataMatch = text.match(
    /\/resource\/declared-data\/(.+)$/
  );

  if (declaredDataMatch) {
    return declaredDataMatch[1];
  }

  // If it is not an ontology URI, return it normally.
  return text;
}

function formatFunctionName(value) {
  if (!value) {
    return "Unknown Function";
  }

  let name = String(value).trim();

  // Example:
  // NAV-01:FUNC.NAV.SEARCH
  // becomes:
  // FUNC.NAV.SEARCH
  if (name.includes(":")) {
    name = name.split(":").pop();
  }

  // Remove FUNC.
  name = name.replace(/^FUNC\./i, "");

  const replacements = {
    NAV: "Navigation",
    SEARCH: "Search",
    MAP: "Map",
    LOCATION: "Location",
    COMM: "Communication",
    CALL: "Calling",
    MESSAGE: "Messaging",
    PAYMENT: "Payment",
    FITNESS: "Fitness",
    EDUCATION: "Education",
  };

  return name
    .split(/[._-]+/)
    .filter(Boolean)
    .map(
      (word) =>
        replacements[word.toUpperCase()] ||
        word.charAt(0).toUpperCase() +
          word.slice(1).toLowerCase()
    )
    .join(" ");
}
/* =========================================================
   Semantic Result Card
   ========================================================= */

function SemanticResultCard({ item }) {
  const confidence =
    item.confidence !== null &&
    item.confidence !== undefined
      ? Math.round(item.confidence * 100)
      : null;

  const status = item.fdo_status || "AMBIGUOUS";

  const statusLabel =
    status === "FDO"
      ? "FDO DETECTED"
      : status === "NOT_FDO"
      ? "NOT FDO"
      : "AMBIGUOUS";

  const functionName = formatSemanticResource(
    item.function
  );

  const expectedData = formatSemanticResource(
    item.expected_data
  );

  const declaredData = formatSemanticResource(
    item.declared_data
  );

  return (
    <article className="semantic-card">
      {/* Function */}
      <div className="semantic-card-header">
        <div>
          <span className="section-label">
            FUNCTION
          </span>

          <h4>{functionName}</h4>
        </div>

        <StatusBadge status={status} />
      </div>

      {/* Semantic Decision */}
      <div
        className={`semantic-decision ${status.toLowerCase()}`}
      >
        <div>
          <span className="section-label">
            SEMANTIC DECISION
          </span>

          <strong>{statusLabel}</strong>
        </div>

        {confidence !== null && (
          <div className="decision-confidence">
            <span>Confidence</span>
            <strong>{confidence}%</strong>
          </div>
        )}
      </div>

      {/* Expected vs Declared */}
      <div className="comparison-grid">
        <div className="comparison-column">
          <span className="column-title expected">
            EXPECTED
          </span>

          <div className="data-row">
            <span>Data</span>
            <strong>{expectedData}</strong>
          </div>

          <div className="data-row">
            <span>Type</span>
            <strong>
              {item.expected_type || "Unknown"}
            </strong>
          </div>

          <div className="data-row">
            <span>Purpose</span>
            <strong>
              {item.expected_purpose || "Unknown"}
            </strong>
          </div>
        </div>

        <div className="comparison-column">
          <span className="column-title declared">
            DECLARED
          </span>

          <div className="data-row">
            <span>Data</span>
            <strong>{declaredData}</strong>
          </div>

          <div className="data-row">
            <span>Type</span>
            <strong>
              {item.declared_type || "Unknown"}
            </strong>
          </div>

          <div className="data-row">
            <span>Purpose</span>
            <strong>
              {item.declared_purpose || "Unknown"}
            </strong>
          </div>
        </div>
      </div>

      {/* Confidence */}
      <div className="decision-section">
        <div className="confidence-row">
          <span>Decision Confidence</span>

          <strong>
            {confidence !== null
              ? `${confidence}%`
              : "N/A"}
          </strong>
        </div>

        {confidence !== null && (
          <div className="confidence-track">
            <div
              className="confidence-fill"
              style={{
                width: `${confidence}%`,
              }}
            />
          </div>
        )}
      </div>

      {/* Explanation */}
      <div className="explanation-box">
        <span className="section-label">
          WHY THIS DECISION?
        </span>

        <p>
          {item.reason ||
            "The available semantic evidence was insufficient to determine a definitive result."}
        </p>
      </div>

      {/* Reasoning Chain */}
      <div className="reasoning-section">
        <span className="section-label">
          SEMANTIC REASONING CHAIN
        </span>

        <div className="reasoning-chain">
          <div className="reasoning-step">
            <span className="reasoning-number">
              1
            </span>

            <div>
              <strong>Function</strong>
              <span>{functionName}</span>
            </div>
          </div>

          <span className="reasoning-arrow">
            ↓
          </span>

          <div className="reasoning-step">
            <span className="reasoning-number">
              2
            </span>

            <div>
              <strong>Expected Data</strong>
              <span>{expectedData}</span>
            </div>
          </div>

          <span className="reasoning-arrow">
            ↓
          </span>

          <div className="reasoning-step">
            <span className="reasoning-number">
              3
            </span>

            <div>
              <strong>Declared Data</strong>
              <span>{declaredData}</span>
            </div>
          </div>

          <span className="reasoning-arrow">
            ↓
          </span>

          <div className="reasoning-step">
            <span className="reasoning-number">
              4
            </span>

            <div>
              <strong>Purpose Comparison</strong>
              <span>
                Expected vs Declared Purpose
              </span>
            </div>
          </div>

          <span className="reasoning-arrow">
            ↓
          </span>

          <div className="reasoning-step final-step">
            <span className="reasoning-number">
              5
            </span>

            <div>
              <strong>FDO Decision</strong>
              <span>{statusLabel}</span>
            </div>
          </div>
        </div>
      </div>
    </article>
  );
}

/* =========================================================
   History Card
   ========================================================= */

function HistoryCard({ item, onView }) {
  const createdAt = item.created_at
    ? new Date(item.created_at).toLocaleString()
    : "Unknown date";

  return (
    <article className="history-card">
      <div className="history-card-main">
        <div>
          <span className="section-label">
            APPLICATION
          </span>

          <h4>{item.application_name}</h4>

          <span className="history-application-id">
            {item.application_id} · {item.category}
          </span>
        </div>

        <StatusBadge status={item.analysis_status} />
      </div>

      <div className="history-meta">
        <div>
          <span>Analysis ID</span>
          <strong>{item.analysis_id}</strong>
        </div>

        <div>
          <span>Created</span>
          <strong>{createdAt}</strong>
        </div>
      </div>

      <div className="history-metrics">
        <div>
          <strong>{item.total_mappings}</strong>
          <span>Mappings</span>
        </div>

        <div>
          <strong>{item.fdo_count}</strong>
          <span>FDO</span>
        </div>

        <div>
          <strong>{item.not_fdo_count}</strong>
          <span>Not FDO</span>
        </div>

        <div>
          <strong>{item.ambiguous_count}</strong>
          <span>Ambiguous</span>
        </div>
      </div>

      <button
        className="history-view-button"
        onClick={() =>
          onView(item.analysis_id)
        }
      >
        View Analysis →
      </button>
    </article>
  );
}

/* =========================================================
   Main App
   ========================================================= */

function App() {
  const [applicationName, setApplicationName] =
    useState("");

  const [category, setCategory] =
    useState("");

  const [policyText, setPolicyText] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [historyLoading, setHistoryLoading] =
    useState(false);

  const [historyError, setHistoryError] =
    useState("");

  const [error, setError] =
    useState("");

  const [result, setResult] =
    useState(null);

  const [history, setHistory] =
    useState([]);

  const [showHistory, setShowHistory] =
    useState(false);

  /* =======================================================
     Load History
     ======================================================= */

  const loadHistory = async () => {
    setHistoryLoading(true);
    setHistoryError("");

    try {
      const response = await fetch(
        `${API_URL}/api/v1/analyses`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Unable to load analysis history."
        );
      }

      setHistory(data);
    } catch (err) {
      setHistoryError(
        err.message ||
          "Unable to connect to the analysis server."
      );
    } finally {
      setHistoryLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  /* =======================================================
     Analyze Policy
     ======================================================= */

  const handleAnalyze = async (event) => {
    event.preventDefault();

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        `${API_URL}/api/v1/analyze`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            application_name:
              applicationName,
            category,
            policy_text: policyText,
            policy_source: "frontend",
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Analysis failed."
        );
      }

      setResult(data);

      // Refresh history after successful analysis.
      await loadHistory();
    } catch (err) {
      setError(
        err.message ||
          "Unable to connect to the analysis server."
      );
    } finally {
      setLoading(false);
    }
  };

  /* =======================================================
     Load Previous Analysis
     ======================================================= */

  const loadAnalysis = async (analysisId) => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/api/v1/analyses/${analysisId}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Unable to load analysis."
        );
      }

      setResult(data);

      const selected = history.find(
        (item) =>
          item.analysis_id === analysisId
      );

      if (selected) {
        setApplicationName(
          selected.application_name
        );

        setCategory(
          selected.category
        );
      }

      setShowHistory(false);
    } catch (err) {
      setError(
        err.message ||
          "Unable to load the selected analysis."
      );
    } finally {
      setLoading(false);
    }
  };

  /* =======================================================
     Reset
     ======================================================= */

  const resetAnalysis = () => {
    setResult(null);
    setError("");
    setApplicationName("");
    setCategory("");
    setPolicyText("");
  };

  /* =======================================================
     History Toggle
     ======================================================= */

  const toggleHistory = () => {
    if (!showHistory) {
      loadHistory();
    }

    setShowHistory(
      (current) => !current
    );
  };

  /* =======================================================
     Render
     ======================================================= */

  return (
    <div className="app">

      {/* Header */}
      <header className="header">
        <div className="brand">
          <div className="brand-mark">
            F
          </div>

          <div>
            <h1>FDO Privacy</h1>

            <p>
              Explainable Functional Data
              Ontology Framework
            </p>
          </div>
        </div>

        <div className="header-actions">
          <button
            className="history-button"
            onClick={toggleHistory}
          >
            {showHistory
              ? "← Hide History"
              : "Analysis History"}
          </button>

          <div className="header-badge">
            SEMANTIC PRIVACY ANALYSIS
          </div>
        </div>
      </header>

      {/* Main */}
      <main className="main">

        {/* =================================================
            Home / Analysis Form
            ================================================= */}

        {!result && !showHistory && (
          <>
            <section className="hero">
              <span className="hero-label">
                FUNCTIONAL DATA OVERREACH DETECTION
              </span>

              <h2>
                Analyze privacy policies through
                <br />
                semantic reasoning.
              </h2>

              <p>
                Compare the data required for an
                application's functionality with
                the data declared in its privacy
                policy using FDO ontology and
                semantic analysis.
              </p>
            </section>

            <form onSubmit={handleAnalyze}>
              <section className="card analysis-form">
                <div className="card-heading">
                  <div>
                    <span className="section-label">
                      STEP 01
                    </span>

                    <h3>
                      Application Information
                    </h3>
                  </div>
                </div>

                <div className="form-grid">

                  <div>
                    <label>
                      Application Name
                    </label>

                    <input
                      type="text"
                      placeholder="e.g. WhatsApp"
                      value={applicationName}
                      onChange={(event) =>
                        setApplicationName(
                          event.target.value
                        )
                      }
                      required
                    />
                  </div>

                  <div>
                    <label>
                      Category
                    </label>

                    <select
                      value={category}
                      onChange={(event) =>
                        setCategory(
                          event.target.value
                        )
                      }
                      required
                    >
                      <option value="">
                        Select category
                      </option>

                      <option value="Social Media">
                        Social Media
                      </option>

                      <option value="Communication">
                        Communication
                      </option>

                      <option value="Navigation">
                        Navigation
                      </option>

                      <option value="Banking">
                        Banking / Finance
                      </option>

                      <option value="Other">
                        Other
                      </option>
                    </select>
                  </div>

                </div>

                <label>
                  Privacy Policy
                </label>

                <textarea
                  className="policy-input"
                  placeholder="Paste the privacy policy text here..."
                  value={policyText}
                  onChange={(event) =>
                    setPolicyText(
                      event.target.value
                    )
                  }
                  required
                />

                <div className="form-footer">
                  <span>
                    The policy will be processed
                    through the FDO semantic
                    analysis pipeline.
                  </span>

                  <button
                    type="submit"
                    disabled={loading}
                  >
                    {loading
                      ? "Analyzing..."
                      : "Analyze Policy →"}
                  </button>
                </div>
              </section>
            </form>
          </>
        )}

        {/* =================================================
            Analysis History
            ================================================= */}

        {showHistory && !result && (
          <section className="history-page">

            <div className="results-header">
              <div>
                <span className="hero-label">
                  SAVED ANALYSES
                </span>

                <h2>
                  Analysis History
                </h2>

                <p>
                  Review previous privacy
                  policy analyses stored in
                  the FDO system.
                </p>
              </div>

              <button
                className="secondary-button"
                onClick={() =>
                  setShowHistory(false)
                }
              >
                ← Back to Analysis
              </button>
            </div>

            {historyError && (
              <section className="card error-card">
                <div className="error-title">
                  History Error
                </div>

                <p>{historyError}</p>
              </section>
            )}

            {historyLoading ? (
              <section className="card empty-state">
                <h3>
                  Loading analysis history...
                </h3>

                <p>
                  Fetching saved analyses
                  from the backend.
                </p>
              </section>
            ) : history.length > 0 ? (
              <div className="history-list">
                {history
                  .slice(0, 10)
                  .map((item) => (
                    <HistoryCard
                      key={item.analysis_id}
                      item={item}
                      onView={loadAnalysis}
                    />
                  ))}
              </div>
            ) : (
              <section className="card empty-state">
                <h3>
                  No previous analyses
                </h3>

                <p>
                  Run your first privacy
                  policy analysis and it
                  will appear here.
                </p>
              </section>
            )}

          </section>
        )}

        {/* =================================================
            Error
            ================================================= */}

        {error && (
          <section className="card error-card">
            <div className="error-title">
              Analysis Error
            </div>

            <p>{error}</p>
          </section>
        )}

        {/* =================================================
            Results
            ================================================= */}

        {result && (
          <section className="results-page">

            <div className="results-header">
              <div>
                <span className="hero-label">
                  ANALYSIS COMPLETE
                </span>

                <h2>
                  {applicationName}
                </h2>

                <p>
                  {category ||
                    "Saved analysis"}{" "}
                  · Semantic privacy analysis
                </p>
              </div>

              <button
                className="secondary-button"
                onClick={resetAnalysis}
              >
                ← New Analysis
              </button>
            </div>

            {/* Metrics */}
            <div className="metric-grid">

              <MetricCard
                value={
                  result.total_mappings
                }
                label="Total Mappings"
                type="total"
              />

              <MetricCard
                value={result.fdo_count}
                label="FDO Detected"
                type="fdo"
              />

              <MetricCard
                value={result.not_fdo_count}
                label="Not FDO"
                type="not-fdo"
              />

              <MetricCard
                value={
                  result.ambiguous_count
                }
                label="Ambiguous"
                type="ambiguous"
              />

            </div>

            {/* Analysis Metadata */}
            <div className="analysis-meta card">

              <div>
                <span>
                  ANALYSIS ID
                </span>

                <strong>
                  {result.analysis_id}
                </strong>
              </div>

              <div>
                <span>
                  STATUS
                </span>

                <strong>
                  {result.analysis_status}
                </strong>
              </div>

            </div>

            {/* Semantic Results */}
            {result.semantic_results?.length >
            0 ? (
              <section>

                <div className="section-heading">
                  <div>
                    <span className="section-label">
                      SEMANTIC LAYER
                    </span>

                    <h3>
                      FDO Analysis Results
                    </h3>
                  </div>

                  <span className="result-count">
                    {
                      result.semantic_results
                        .length
                    }{" "}
                    result
                    {result.semantic_results
                      .length !== 1
                      ? "s"
                      : ""}
                  </span>
                </div>

                <div className="semantic-results">
                  {result.semantic_results.map(
                    (item) => (
                      <SemanticResultCard
                        key={
                          item.semantic_result_id
                        }
                        item={item}
                      />
                    )
                  )}
                </div>

              </section>
            ) : (
              <section className="card empty-state">
                <h3>
                  No semantic findings
                </h3>

                <p>
                  The analysis completed
                  without semantic FDO
                  findings.
                </p>
              </section>
            )}

          </section>
        )}

      </main>

      {/* Footer */}
      <footer className="footer">
        <span>
          FDO Privacy Project
        </span>

        <span>
          OWL · RDF · SPARQL · Apache Jena
          Fuseki
        </span>
      </footer>

    </div>
  );
}

export default App;