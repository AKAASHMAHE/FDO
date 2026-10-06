import { useEffect, useState } from "react";

const API_URL = "http://127.0.0.1:8000";

function getErrorDetail(data, fallback) {
  const detail = data?.detail;

  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        const location = Array.isArray(item?.loc)
          ? item.loc.join(".")
          : "";
        const message =
          item?.msg || JSON.stringify(item);

        return location
          ? `${location}: ${message}`
          : message;
      })
      .join("; ");
  }

  if (typeof detail === "string") {
    return detail;
  }

  if (detail) {
    return JSON.stringify(detail);
  }

  return fallback;
}

async function parseJsonResponse(response) {
  try {
    return await response.json();
  } catch {
    return null;
  }
}

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

function safeText(value, fallback = "Unknown") {
  if (value === null || value === undefined) {
    return fallback;
  }

  const text = String(value).trim();
  return text || fallback;
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
    return formatIdentifierLabel(expectedDataMatch[1]);
  }

  // DECLARED DATA URI
  const declaredDataMatch = text.match(
    /\/resource\/declared-data\/(.+)$/
  );

  if (declaredDataMatch) {
    return formatIdentifierLabel(declaredDataMatch[1]);
  }

  // If it is not an ontology URI, return it normally.
  return text;
}

function formatIdentifierLabel(value) {
  if (!value) {
    return "Unknown";
  }

  let label = String(value).trim();

  if (label.includes(":")) {
    label = label.split(":").pop();
  }

  label = label
    .replace(/^EXP[-_.]*/i, "")
    .replace(/^AI[-_.]*/i, "")
    .replace(/^DATA[._-]/i, "")
    .replace(/^FUNC[._-]/i, "");

  const words = label
    .split(/[._-]+/)
    .filter(Boolean);

  if (
    words.length > 1 &&
    words[0].toUpperCase() === "MEDIA"
  ) {
    words.shift();
  }

  if (!words.length) {
    return String(value).trim();
  }

  const replacements = {
    NAV: "Navigation",
    COM: "Communication",
    COMM: "Communication",
    VIDEO: "Video",
    CALL: "Call",
    MEDIA: "Media",
    CAMERA: "Camera",
    MICROPHONE: "Microphone",
    LOCATION: "Location",
    PRECISE: "Precise",
    APPROXIMATE: "Approximate",
    CONTACTS: "Contacts",
    DEVICE: "Device",
    ACCOUNT: "Account",
    FINANCIAL: "Financial",
    HEALTH: "Health",
    USAGE: "Usage",
    OTHER: "Other / Unclear Data",
  };

  return words
    .map(
      (word) =>
        replacements[word.toUpperCase()] ||
        word.charAt(0).toUpperCase() +
          word.slice(1).toLowerCase()
    )
    .join(" ");
}

function formatDataLabel(resource, type) {
  const typeLabel = formatIdentifierLabel(type);

  if (
    typeLabel &&
    typeLabel !== "Unknown" &&
    typeLabel !== "Other"
  ) {
    return typeLabel;
  }

  return formatSemanticResource(resource);
}

function formatPurposeLabel(value) {
  return formatIdentifierLabel(value);
}

function normalizePurposes(item) {
  if (Array.isArray(item.declared_purposes)) {
    return item.declared_purposes
      .map((purpose) => String(purpose).trim())
      .filter(Boolean);
  }

  const value = item.declared_purpose;

  if (!value) {
    return [];
  }

  try {
    const parsed = JSON.parse(value);

    if (Array.isArray(parsed)) {
      return parsed
        .map((purpose) => String(purpose).trim())
        .filter(Boolean);
    }
  } catch {
    // Fall back to the original single-purpose response shape.
  }

  return [String(value).trim()].filter(Boolean);
}

function PurposeList({ purposes }) {
  const purposeItems = Array.isArray(purposes)
    ? purposes
    : [];
  const safePurposes = purposeItems.length
    ? purposeItems
    : ["Unknown"];

  return (
    <ul className="purpose-list">
      {safePurposes.map((purpose, index) => (
        <li key={`${purpose}-${index}`}>
          {formatPurposeLabel(purpose)}
        </li>
      ))}
    </ul>
  );
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
   Semantic Grouping & Cards
   ========================================================= */

function groupSemanticResultsByFunction(items) {
  if (!Array.isArray(items) || items.length === 0) {
    return [];
  }

  const groupsMap = new Map();

  for (const item of items) {
    const rawKey =
      item.function ||
      item.function_label ||
      "Unknown Function";
    const key = String(rawKey).trim().toLowerCase();

    if (!groupsMap.has(key)) {
      const displayName =
        item.function_label ||
        formatSemanticResource(item.function);

      groupsMap.set(key, {
        functionKey: rawKey,
        functionName: displayName,
        items: [],
      });
    }

    groupsMap.get(key).items.push(item);
  }

  return Array.from(groupsMap.values());
}

function GroupedSemanticCard({ group }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const { functionName, items } = group;

  // 1. Status analysis
  const statuses = items.map(
    (i) => i.fdo_status || "AMBIGUOUS"
  );
  const uniqueStatuses = Array.from(new Set(statuses));
  const isUniformStatus = uniqueStatuses.length === 1;
  const uniformStatus = uniqueStatuses[0];

  const fdoCount = items.filter(
    (i) => (i.fdo_status || "") === "FDO"
  ).length;
  const notFdoCount = items.filter(
    (i) => (i.fdo_status || "") === "NOT_FDO"
  ).length;
  const ambiguousCount = items.filter(
    (i) =>
      (i.fdo_status || "") !== "FDO" &&
      (i.fdo_status || "") !== "NOT_FDO"
  ).length;

  // 2. Confidence analysis
  const confidences = items
    .map((i) =>
      i.confidence !== null && i.confidence !== undefined
        ? Math.round(i.confidence * 100)
        : null
    )
    .filter((c) => c !== null);

  const uniqueConfidences = Array.from(new Set(confidences));
  const isUniformConfidence = uniqueConfidences.length === 1;
  const displayConfidence = isUniformConfidence
    ? `${uniqueConfidences[0]}%`
    : confidences.length > 0
    ? "Multiple confidence values"
    : "N/A";

  // 3. Expected data & purpose uniformity
  const expectedDatas = Array.from(
    new Set(
      items.map(
        (i) =>
          i.expected_data_label ||
          formatDataLabel(i.expected_data, i.expected_type)
      )
    )
  );
  const expectedPurposes = Array.from(
    new Set(
      items.map((i) => formatPurposeLabel(i.expected_purpose))
    )
  );

  const isUniformExpectedData = expectedDatas.length === 1;
  const isUniformExpectedPurpose = expectedPurposes.length === 1;

  // 4. Policy Declared Data Chips
  const declaredDataItemsMap = new Map();
  for (const item of items) {
    const label =
      item.declared_data_label ||
      formatDataLabel(item.declared_data, item.declared_type);

    if (label && !declaredDataItemsMap.has(label)) {
      declaredDataItemsMap.set(label, {
        label,
        type: formatIdentifierLabel(item.declared_type),
      });
    }
  }
  const uniqueDeclaredData = Array.from(
    declaredDataItemsMap.values()
  );

  return (
    <article className="semantic-card grouped-semantic-card">
      {/* Header: Function & Decision Status */}
      <div className="semantic-card-header">
        <div>
          <span className="section-label">FUNCTION</span>
          <h4>{functionName}</h4>
        </div>

        {isUniformStatus ? (
          <StatusBadge status={uniformStatus} />
        ) : (
          <div className="status-breakdown-badges">
            {fdoCount > 0 && (
              <span className="status-badge fdo">
                FDO: {fdoCount}
              </span>
            )}
            {notFdoCount > 0 && (
              <span className="status-badge not_fdo">
                NOT FDO: {notFdoCount}
              </span>
            )}
            {ambiguousCount > 0 && (
              <span className="status-badge ambiguous">
                AMBIGUOUS: {ambiguousCount}
              </span>
            )}
          </div>
        )}
      </div>

      {/* Semantic Decision Banner */}
      <div
        className={`semantic-decision ${
          isUniformStatus
            ? uniformStatus.toLowerCase()
            : "mixed"
        }`}
      >
        <div>
          <span className="section-label">
            SEMANTIC DECISION
          </span>
          <strong>
            {isUniformStatus
              ? uniformStatus === "FDO"
                ? "FDO DETECTED"
                : uniformStatus === "NOT_FDO"
                ? "NOT FDO"
                : "AMBIGUOUS"
              : `MIXED DECISIONS (${items.length} COMPARISONS)`}
          </strong>
        </div>

        <div className="decision-confidence">
          <span>Confidence</span>
          <strong>{displayConfidence}</strong>
        </div>
      </div>

      {/* Summary Grid: Expected vs Policy Declared */}
      <div className="comparison-grid">
        {/* EXPECTED COLUMN */}
        <div className="comparison-column">
          <span className="column-title expected">
            EXPECTED FUNCTIONAL BASELINE
          </span>

          {isUniformExpectedData && isUniformExpectedPurpose ? (
            <>
              <div className="data-row">
                <span>Data</span>
                <strong>{expectedDatas[0]}</strong>
              </div>
              <div className="data-row">
                <span>Type</span>
                <strong>{expectedDatas[0]}</strong>
              </div>
              <div className="data-row">
                <span>Expected Purpose</span>
                <strong>{expectedPurposes[0]}</strong>
              </div>
            </>
          ) : (
            <div className="multiple-expectations-notice">
              <strong>Multiple semantic expectations</strong>
              <span>
                This function has {expectedDatas.length} data type(s) evaluated. Expand reasoning below for details.
              </span>
            </div>
          )}
        </div>

        {/* POLICY DECLARED COLUMN */}
        <div className="comparison-column">
          <div className="column-title-row">
            <span className="column-title declared">
              POLICY DECLARED DATA
            </span>
            <span className="declared-count-badge">
              {uniqueDeclaredData.length} data type
              {uniqueDeclaredData.length !== 1 ? "s" : ""}
            </span>
          </div>

          <div className="declared-chips-container">
            {uniqueDeclaredData.map((d) => (
              <span className="declared-chip" key={d.label}>
                {d.label}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Comparisons Count Footer */}
      <div className="group-summary-footer">
        <span className="comparisons-count-label">
          {items.length} semantic comparison
          {items.length !== 1 ? "s" : ""} evaluated
        </span>
      </div>

      {/* View Reasoning Toggle Button */}
      <button
        type="button"
        className="view-reasoning-toggle"
        onClick={() => setIsExpanded(!isExpanded)}
        aria-expanded={isExpanded}
      >
        <span>{isExpanded ? "Hide reasoning" : "View reasoning"}</span>
        <svg
          className={`chevron-icon ${isExpanded ? "expanded" : ""}`}
          width="16"
          height="16"
          viewBox="0 0 16 16"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M4 6L8 10L12 6"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </button>

      {/* Expanded Reasoning Panel */}
      {isExpanded && (
        <div className="expanded-reasoning-panel">
          <div className="reasoning-panel-title">
            <h5>DETAILED COMPARISONS & REASONING</h5>
          </div>

          <div className="comparisons-subcards-list">
            {items.map((item, idx) => {
              const itemConfidence =
                item.confidence !== null &&
                item.confidence !== undefined
                  ? `${Math.round(item.confidence * 100)}%`
                  : "N/A";

              const expectedD =
                item.expected_data_label ||
                formatDataLabel(
                  item.expected_data,
                  item.expected_type
                );
              const declaredD =
                item.declared_data_label ||
                formatDataLabel(
                  item.declared_data,
                  item.declared_type
                );
              const expectedP = formatPurposeLabel(
                item.expected_purpose
              );
              const declaredPs = normalizePurposes(item);

              const isMatch =
                expectedD.toLowerCase() ===
                declaredD.toLowerCase();

              return (
                <div
                  className="comparison-subcard"
                  key={item.semantic_result_id || idx}
                >
                  <div className="subcard-header">
                    <span className="subcard-index">
                      COMPARISON {idx + 1} OF {items.length}
                    </span>
                    <StatusBadge status={item.fdo_status} />
                  </div>

                  <div className="subcard-grid">
                    {/* Expected */}
                    <div className="subcard-col expected-col">
                      <span className="subcard-col-label">
                        EXPECTED
                      </span>
                      <div className="subcard-data-row">
                        <span>Data & Type:</span>
                        <strong>{expectedD}</strong>
                      </div>
                      <div className="subcard-data-row">
                        <span>Purpose:</span>
                        <strong>{expectedP}</strong>
                      </div>
                    </div>

                    {/* Declared */}
                    <div className="subcard-col declared-col">
                      <span className="subcard-col-label">
                        DECLARED
                      </span>
                      <div className="subcard-data-row">
                        <span>Data & Type:</span>
                        <strong>{declaredD}</strong>
                      </div>
                      <div className="subcard-data-row">
                        <span>Purposes:</span>
                        <PurposeList
                          purposes={declaredPs}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Semantic Check Metrics */}
                  <div className="subcard-checks-bar">
                    <div className="check-metric">
                      <span>Data Match:</span>
                      <strong
                        className={
                          isMatch ? "match-yes" : "match-no"
                        }
                      >
                        {isMatch
                          ? "EXACT MATCH"
                          : "DATA TYPE MISMATCH"}
                      </strong>
                    </div>
                    <div className="check-metric">
                      <span>Confidence:</span>
                      <strong>{itemConfidence}</strong>
                    </div>
                  </div>

                  {/* Why this decision */}
                  <div className="subcard-explanation">
                    <span className="explanation-title">
                      WHY THIS DECISION
                    </span>
                    <p>
                      {item.reason ||
                        "The available semantic evidence was insufficient to determine a definitive result."}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </article>
  );
}

function PolicyAnalysisCard({ finding }) {
  const confidence =
    finding.confidence !== null &&
    finding.confidence !== undefined
      ? Math.round(finding.confidence * 100)
      : null;

  const evidence = Array.isArray(finding.evidence)
    ? finding.evidence.slice(0, 2)
    : [];

  return (
    <article className="policy-analysis-card">
      <div className="policy-analysis-card-header">
        <div>
          <span className="section-label">
            POLICY-DECLARED DATA
          </span>

          <h4>
            {finding.data_label ||
              formatIdentifierLabel(
                finding.data_type
              )}
          </h4>
        </div>

        {confidence !== null && (
          <span className="policy-confidence">
            {confidence}% confidence
          </span>
        )}
      </div>

      <div className="data-row">
        <span>Function / Processing Context</span>
        <strong>
          {formatPurposeLabel(
            finding.function ||
              "Policy-declared processing"
          )}
        </strong>
      </div>

      <div className="data-row">
        <span>Purposes</span>
        <PurposeList
          purposes={finding.purposes || []}
        />
      </div>

      {evidence.length > 0 && (
        <details className="policy-evidence">
          <summary>View evidence</summary>

          <ul>
            {evidence.map((item, index) => (
              <li key={`${item}-${index}`}>
                {item}
              </li>
            ))}
          </ul>
        </details>
      )}
    </article>
  );
}

function FunctionalBaselineSection({ result }) {
  const items = Array.isArray(result?.functional_baseline)
    ? result.functional_baseline
    : [];

  if (!items.length) {
    return null;
  }

  const source = result.baseline_source || "CURATED";
  const status = result.baseline_status || "AVAILABLE";
  const isAiDerived = source === "AI_DERIVED";
  const confidence =
    result.baseline_confidence !== null &&
    result.baseline_confidence !== undefined
      ? Math.round(result.baseline_confidence * 100)
      : null;

  const grouped = items.reduce((acc, item) => {
    const key = item.function_name || "Unknown Function";

    if (!acc[key]) {
      acc[key] = [];
    }

    acc[key].push(item);
    return acc;
  }, {});

  return (
    <section className="functional-baseline-section">
      <div className="section-heading">
        <div>
          <span className="section-label">
            FUNCTIONAL BASELINE
          </span>

          <h3>
            {isAiDerived
              ? "AI-derived functional baseline"
              : "Curated functional baseline"}
          </h3>

          {isAiDerived && (
            <p className="section-note">
              This baseline is provisional and
              generated from application
              functionality, not from the privacy
              policy.
            </p>
          )}
        </div>

        <span className="baseline-source-badge">
          {status} / {source}
          {confidence !== null
            ? ` / ${confidence}%`
            : ""}
        </span>
      </div>

      <div className="functional-baseline-grid">
        {Object.entries(grouped).map(
          ([functionName, mappings]) => (
            <article
              className="functional-baseline-card"
              key={functionName}
            >
              <span className="section-label">
                FUNCTION
              </span>

              <h4>{functionName}</h4>

              <div className="baseline-data-list">
                {mappings.map((item) => (
                  <div
                    className="baseline-data-item"
                    key={item.expected_id}
                  >
                    <strong>
                      {formatIdentifierLabel(
                        item.expected_data_type
                      )}
                    </strong>

                    <span>{item.necessity}</span>

                    <p>{item.expected_purpose}</p>

                    {item.baseline_justification && (
                      <p className="baseline-justification">
                        {item.baseline_justification}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </article>
          )
        )}
      </div>
    </section>
  );
}

function BaselineUnavailableSection({ result }) {
  const policyAvailable =
    result?.policy_analysis?.available === true;

  return (
    <section className="card info-card">
      <span className="section-label">
        FDO COMPARISON
      </span>

      <h3>Functional Baseline Unavailable</h3>

      <p>
        {policyAvailable
          ? "Policy analysis is available, but FDO determination requires a functional baseline."
          : "A definitive FDO determination cannot be made because no reliable functional baseline is available."}
      </p>
    </section>
  );
}

function getPolicyFindings(result) {
  const findings = result?.policy_analysis?.findings;

  return Array.isArray(findings) ? findings : [];
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

          <h4>{safeText(item.application_name)}</h4>

          <span className="history-application-id">
            {safeText(item.application_id)} / {safeText(item.category)}
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
        View Analysis
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

  const [description, setDescription] =
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

  const [manualPolicyMode, setManualPolicyMode] =
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

      const data = await parseJsonResponse(response);

      if (!response.ok) {
        throw new Error(
          getErrorDetail(
            data,
            "Unable to load analysis history."
          )
        );
      }

      setHistory(Array.isArray(data) ? data : []);
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
    const timer = window.setTimeout(() => {
      loadHistory();
    }, 0);

    return () => {
      window.clearTimeout(timer);
    };
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
            category: category || "Other",
            description: description.trim()
              ? description
              : undefined,
            policy_text: policyText.trim()
              ? policyText
              : undefined,
            policy_source: policyText.trim()
              ? "frontend"
              : undefined,
          }),
        }
      );

      const data = await parseJsonResponse(response);

      if (!response.ok) {
        const fallback =
          response.status === 422
            ? "Invalid analysis request."
            : response.status >= 500
            ? "Server error while running analysis."
            : "Analysis failed.";

        throw new Error(
          `HTTP ${response.status}: ${getErrorDetail(
            data,
            fallback
          )}`
        );
      }

      setResult(data);

      // Refresh history after successful analysis.
      await loadHistory();
    } catch (err) {
      const message =
        err.message ||
        "Unable to connect to the analysis server.";

      setError(`Analysis failed: ${message}`);

      if (
        message
          .toLowerCase()
          .includes("paste the policy manually")
      ) {
        setManualPolicyMode(true);
      }
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
      let response = await fetch(
        `${API_URL}/api/v1/analyses/${analysisId}`
      );

      let data = await parseJsonResponse(response);

      if (response.status === 404) {
        response = await fetch(
          `${API_URL}/api/v1/analysis/${analysisId}`
        );
        data = await parseJsonResponse(response);
      }

      if (!response.ok) {
        throw new Error(
          getErrorDetail(
            data,
            "Unable to load analysis."
          )
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

        setDescription("");
      }

      setShowHistory(false);
    } catch (err) {
      setError(
        `Analysis failed: ${
          err.message ||
          "Unable to load the selected analysis."
        }`
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
    setDescription("");
    setPolicyText("");
    setManualPolicyMode(false);
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
              ? "Hide History"
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

                <div className="form-single">
                  <label>
                    Application Description
                  </label>

                  <input
                    type="text"
                    placeholder="Optional: primary features or functional context"
                    value={description}
                    onChange={(event) =>
                      setDescription(
                        event.target.value
                      )
                    }
                  />
                </div>

                <label>
                  Privacy Policy
                </label>

                {!manualPolicyMode && (
                  <p className="field-help">
                    Leave this empty to let the system
                    attempt official privacy policy discovery.
                  </p>
                )}

                <textarea
                  className="policy-input"
                  placeholder={
                    manualPolicyMode
                      ? "Paste the privacy policy text here to continue."
                      : "Optional fallback: paste policy text here, or leave blank for automatic discovery."
                  }
                  value={policyText}
                  onChange={(event) =>
                    setPolicyText(
                      event.target.value
                    )
                  }
                />

                <div className="form-footer">
                  <span>
                    {policyText.trim()
                      ? "The supplied policy text will be processed through the FDO semantic analysis pipeline."
                      : "The system will try to discover an official privacy policy first. If discovery fails, paste the policy manually."}
                  </span>

                  <button
                    type="submit"
                    disabled={loading}
                  >
                    {loading
                      ? "Analyzing..."
                      : policyText.trim()
                      ? "Analyze Policy"
                      : "Find & Analyze Policy"}
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
                Back to Analysis
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
                  {safeText(
                    applicationName || result.application_id,
                    "Analysis Result"
                  )}
                </h2>

                <p>
                  {safeText(category, "Saved analysis")}{" "}
                  / Semantic privacy analysis
                </p>
              </div>

              <button
                className="secondary-button"
                onClick={resetAnalysis}
              >
                New Analysis
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

            <FunctionalBaselineSection
              result={result}
            />

            {result.policy_analysis?.available && (
              <section className="policy-analysis-section">
                <div className="section-heading">
                  <div>
                    <span className="section-label">
                      POLICY ANALYSIS
                    </span>

                    <h3>
                      Policy-Declared Findings
                    </h3>

                    {result.policy_analysis
                      .policy_source && (
                      <p className="section-note">
                        Source:{" "}
                        {
                          result.policy_analysis
                            .policy_source
                        }
                      </p>
                    )}
                  </div>

                  <span className="result-count">
                    {getPolicyFindings(result).length}{" "}
                    finding
                    {getPolicyFindings(result)
                      .length !== 1
                      ? "s"
                      : ""}
                  </span>
                </div>

                <div className="policy-analysis-grid">
                  {getPolicyFindings(result).map(
                    (finding, index) => (
                      <PolicyAnalysisCard
                        key={`${finding.data_type}-${finding.function}-${index}`}
                        finding={finding}
                      />
                    )
                  )}
                </div>
              </section>
            )}

            {!result.has_expected_baseline && (
              <BaselineUnavailableSection
                result={result}
              />
            )}

            {/* Semantic Results */}
            {result.has_expected_baseline &&
            result.semantic_results?.length > 0 ? (() => {
              const groupedResults = groupSemanticResultsByFunction(
                result.semantic_results
              );

              return (
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
                      {groupedResults.length} function group
                      {groupedResults.length !== 1 ? "s" : ""}{" "}
                      ({result.semantic_results.length} total comparison
                      {result.semantic_results.length !== 1 ? "s" : ""})
                    </span>
                  </div>

                  <div className="semantic-results">
                    {groupedResults.map((group) => (
                      <GroupedSemanticCard
                        key={group.functionKey}
                        group={group}
                      />
                    ))}
                  </div>
                </section>
              );
            })() : result.has_expected_baseline ? (
              <section className="card empty-state">
                <h3>
                  No semantic findings
                </h3>

                <p>
                  Expected functional data mapping is
                  not available for this application,
                  or no trustworthy policy-declared
                  data evidence was found, so a
                  definitive FDO comparison cannot be
                  made.
                </p>
              </section>
            ) : null}

          </section>
        )}

      </main>

      {/* Footer */}
      <footer className="footer">
        <span>
          FDO Privacy Project
        </span>

        <span>
          OWL / RDF / SPARQL / Apache Jena
          Fuseki
        </span>
      </footer>

    </div>
  );
}

export default App;
