import { useParams } from "react-router-dom";
import { pageMeta } from "../data/pages";
import {
  ArrowRight,
  BarChart3,
  CheckCircle2,
  Database,
  FileSpreadsheet,
  GitCompare,
  UploadCloud,
  WandSparkles,
  X,
  FileText,
} from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { useAuth } from "@clerk/react";

const samples = {
  analysis: {
    icon: BarChart3,
    action: "Analyze Dataset",
    cards: [
      ["Data Quality", "88%", "Excellent"],
      ["Missing Values", "2.4%", "Review"],
      ["Exact Duplicates", "843", "Detected"],
      ["Anomalous Outliers", "1,204", "Detected"],
    ],
  },

  preprocessing: {
    icon: WandSparkles,
    action: "Create Pipeline",
    cards: [
      ["Missing Value Imputation", "customer_income", "Pending"],
      ["Drop Duplicates", "1,204 rows", "Applied"],
      ["Standard Scaling", "transaction_amount", "Applied"],
      ["Feature Engineering", "loyalty_score", "Ready"],
    ],
  },

  training: {
    icon: WandSparkles,
    action: "Start Training",
    cards: [
      ["XGBoost Classifier", "Gradient boosting", "Ready"],
      ["Random Forest", "Ensemble method", "Ready"],
      ["Support Vector Machine", "Linear/non-linear", "Ready"],
      ["Deep Neural Network", "Multi-layer perceptron", "Ready"],
    ],
  },

  evaluation: {
    icon: CheckCircle2,
    action: "Run Evaluation",
    cards: [
      ["Accuracy", "94.2%", "Excellent"],
      ["Precision", "92.8%", "Strong"],
      ["Recall", "91.6%", "Strong"],
      ["F1 Score", "92.2%", "Strong"],
    ],
  },

  comparison: {
    icon: GitCompare,
    action: "Compare Models",
    cards: [
      ["Churn_Pred_v3", "Random Forest", "92.4%"],
      ["Churn_Pred_v2", "XGBoost", "91.8%"],
      ["Churn_Pred_v1", "SVM", "88.6%"],
      ["Baseline", "Logistic Regression", "84.1%"],
    ],
  },

  prediction: {
    icon: ArrowRight,
    action: "Generate Prediction",
    cards: [
      ["Prediction", "High churn risk", "94.8% confidence"],
      ["Input", "Customer #10428", "Validated"],
      ["Model", "Churn_Pred_v3", "Production candidate"],
      ["Latency", "42 ms", "Healthy"],
    ],
  },

  explainable: {
    icon: WandSparkles,
    action: "Explain Prediction",
    cards: [
      ["Contract length", "+42%", "High impact"],
      ["Monthly charges", "+27%", "Medium impact"],
      ["Tenure", "-18%", "Protective"],
      ["Support calls", "+13%", "Medium impact"],
    ],
  },

  reports: {
    icon: FileSpreadsheet,
    action: "Create Report",
    cards: [
      ["Dataset report", "Data quality & schema", "Ready"],
      ["EDA report", "Charts & statistics", "Ready"],
      ["Model report", "Training & evaluation", "Ready"],
      ["Prediction report", "Inputs & explanations", "Ready"],
    ],
  },

  history: {
    icon: Database,
    action: "View Activity",
    cards: [
      ["Training run", "Churn_Pred_v3", "Completed"],
      ["Preprocessing", "Pipeline v8", "Updated"],
      ["Dataset", "customer_churn_2023", "Analyzed"],
      ["Prediction batch", "Batch #1042", "Generated"],
    ],
  },
};

function DatasetPage() {
  const { userId, isLoaded, getToken } = useAuth();
  const inputRef = useRef(null);
  const [file, setFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState("");

  const [analysis, setAnalysis] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [savedDatasets, setSavedDatasets] = useState([]);
  const [loadingDatasets, setLoadingDatasets] = useState(true);
  const allowedTypes = [".csv", ".xlsx", ".json"];
  const fetchDatasets = async () => {
  if (!isLoaded || !userId) {
    return;
  }
  const token = await getToken();
  console.log("Fetching datasets...");
  console.log("Clerk loaded:", isLoaded);
  console.log("Clerk userId:", userId);

  setLoadingDatasets(true);

  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/datasets/`,
       {
        headers: {
         Authorization: `Bearer ${token}`,
        },
      }
    );

    const result = await response.json();

    if (!response.ok) {
      throw new Error(
        result.detail || "Unable to fetch datasets."
      );
    }

    console.log(
      "Datasets from backend:",
      result.datasets
    );

    setSavedDatasets(result.datasets || []);

  } catch (err) {
    console.error("Dataset fetch error:", err);

    setSavedDatasets([]);

    setError(
      err.message || "Unable to load datasets."
    );

  } finally {
    setLoadingDatasets(false);
  }
};
useEffect(() => {
  if (isLoaded && userId) {
    fetchDatasets();
  }
}, [isLoaded, userId]);
  const analyzeDataset = async () => {
    if (!file) return;
    console.log("Clerk auth:", {
      isLoaded,
      userId,
    });
    if (!isLoaded) {
      throw new Error("Authentication is still loading.");
    }
    if (!userId) {
      throw new Error("You must be logged in to save the dataset.");
    }

    setAnalyzing(true);
    setError("");
    setAnalysis(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const token = await getToken();

      const response = await fetch(
       `${import.meta.env.VITE_API_URL}/analyze-dataset`,
         {
         method: "POST",
          headers: {
           Authorization: `Bearer ${token}`,
          },
          body: formData,
        }
      );
      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Dataset analysis failed."
        );
      }

      setAnalysis(data);

const saveResponse = await fetch(
  `${import.meta.env.VITE_API_URL}/save-dataset`,
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      filename: data.filename,
      file_size: file.size,

      rows: data.dataset.rows,
      columns: data.dataset.columns,

      missing_values: data.dataset.missing_values,
      missing_percentage: data.dataset.missing_percentage,

      duplicates: data.dataset.duplicates,
      data_quality: data.dataset.data_quality,

      column_types: data.column_types,
      columns_info: data.columns,

      status: "Analyzed",
    }),
  }
);

const saveData = await saveResponse.json();

if (!saveResponse.ok) {
  throw new Error(
    saveData.detail || "Could not save dataset."
  );
}
await fetchDatasets();
    } catch (err) {

      setError(
        err.message ||
        "Could not connect to Cognify backend."
      );

    } finally {

      setAnalyzing(false);
    }
  };
  const validateFile = (selectedFile) => {
    if (!selectedFile) return;

    const extension =
      "." + selectedFile.name.split(".").pop().toLowerCase();

    if (!allowedTypes.includes(extension)) {
      setError("Unsupported file type. Please upload CSV, Excel, or JSON.");
      setFile(null);
      return;
    }

    setError("");
    setFile(selectedFile);
  };

  const handleFileChange = (e) => {
    validateFile(e.target.files[0]);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);

    const droppedFile = e.dataTransfer.files[0];
    validateFile(droppedFile);
  };

  const removeFile = () => {
    setFile(null);
    setError("");

    if (inputRef.current) {
      inputRef.current.value = "";
    }
  };

  return (
    <div className="workspace-page">
      <div className="page-heading">
        <div>
          <span className="kicker">COGNIFY WORKSPACE</span>
          <h1>Dataset Management</h1>
          <p>
            Upload, structure, validate, and manage the datasets used
            across your ML workflow.
          </p>
        </div>
      </div>

      <section className="dataset-section">
        <div className="dataset-section-heading">
          <h2>Upload Dataset</h2>
          <p>
            Start your machine learning workflow by uploading a dataset.
          </p>
        </div>

        {!file ? (
          <div
            className={`upload-dropzone ${
              dragActive ? "upload-dropzone-active" : ""
            }`}
            onClick={() => inputRef.current?.click()}
            onDragOver={(e) => {
              e.preventDefault();
              setDragActive(true);
            }}
            onDragLeave={() => setDragActive(false)}
            onDrop={handleDrop}
          >
            <div className="upload-icon">
              <UploadCloud size={28} />
            </div>

            <h3>Drop your dataset here</h3>

            <p>
              Drag & drop your file or <span>browse files</span>
            </p>

            <small>
              Supported formats: CSV, XLSX, JSON
            </small>

            <input
              ref={inputRef}
              type="file"
              accept=".csv,.xlsx,.json"
              hidden
              onChange={handleFileChange}
            />
          </div>
        ) : (
          <div className="uploaded-file-card">
            <div className="uploaded-file-icon">
              <FileText size={22} />
            </div>

            <div className="uploaded-file-info">
              <strong>{file.name}</strong>

              <span>
                {(file.size / 1024 / 1024).toFixed(2)} MB
              </span>
            </div>

            <div className="upload-success">
              <CheckCircle2 size={16} />
              Ready
            </div>

            <button
              className="remove-file-btn"
              onClick={removeFile}
              title="Remove file"
            >
              <X size={17} />
            </button>
          </div>
        )}

        {error && (
          <div className="upload-error">
            <span>⚠</span>
            {error}
          </div>
        )}

        {file && (
          <div className="dataset-ready">
            <div className="dataset-ready-icon">
              <Database size={20} />
            </div>

            <div>
              <strong>Dataset ready for analysis</strong>
              <p>
                Your dataset has been successfully selected and is ready for ML analysis.
              </p>
            </div>

            <button
              className="btn btn-primary btn-sm"
              onClick={analyzeDataset}
              disabled={analyzing}
            >
              {analyzing ? "Analyzing..." : "Analyze Dataset"}
            </button>
          </div>
        )}
        {analysis && (
  <section className="dataset-analysis">

    <div className="dataset-section-heading">
      <h2>Dataset Analysis</h2>

      <p>
        Cognify analyzed{" "}
        <strong>{analysis.filename}</strong>
        {" "}using the ML analysis engine.
      </p>
    </div>

    <div className="metric-grid">

      <div className="metric-card">
        <Database size={18} />
        <small>Total Rows</small>
        <b>
          {analysis.dataset.rows.toLocaleString()}
        </b>
      </div>

      <div className="metric-card">
        <Database size={18} />
        <small>Total Columns</small>
        <b>
          {analysis.dataset.columns}
        </b>
      </div>

      <div className="metric-card">
        <Database size={18} />
        <small>Missing Values</small>
        <b>
          {analysis.dataset.missing_values.toLocaleString()}
        </b>
      </div>

      <div className="metric-card metric-dark">
        <CheckCircle2 size={18} />
        <small>Data Quality</small>
        <b>
          {analysis.dataset.data_quality}%
        </b>
      </div>

    </div>

    <div className="panel">

      <div className="panel-head">
        <b>Column Information</b>

        <small>
          {analysis.columns.length} columns detected
        </small>
      </div>

      <table>

        <thead>
          <tr>
            <th>Column</th>
            <th>Data Type</th>
            <th>Missing</th>
            <th>Unique</th>
          </tr>
        </thead>

        <tbody>

          {analysis.columns.map((column) => (

            <tr key={column.name}>

              <td>{column.name}</td>

              <td>{column.type}</td>

              <td>{column.missing}</td>

              <td>{column.unique}</td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>

  </section>
)}
        
      </section>

      <section className="dataset-library">
  <div className="panel-head">
    <div>
      <b>Dataset Library</b>

      <div className="dataset-count">
        {loadingDatasets
          ? "Loading datasets..."
          : `${savedDatasets.length} dataset${
              savedDatasets.length === 1 ? "" : "s"
            } available`}
      </div>
    </div>
  </div>

  {loadingDatasets ? (
    <div className="panel">
      <p>Loading your datasets...</p>
    </div>
  ) : savedDatasets.length === 0 ? (
    <div className="panel">
      <p>
        No datasets uploaded yet. Upload your first dataset
        to get started.
      </p>
    </div>
  ) : (
    <div className="workspace-cards">
      {savedDatasets.map((dataset) => (
        <article
          className="info-card"
          key={dataset.id}
        >
          <div className="feature-icon">
            <Database size={18} />
          </div>

          <small>
            {dataset.filename}
          </small>

          <b>
            {dataset.rows?.toLocaleString() || 0} rows ·{" "}
            {dataset.columns || 0} columns
          </b>

          <span>
            {dataset.status || "Analyzed"}
          </span>
        </article>
      ))}
    </div>
  )}
</section>
    </div>
  );
}

export default function WorkspacePage() {
  const { page } = useParams();

  if (page === "datasets") {
    return <DatasetPage />;
  }

  const meta = pageMeta[page] || pageMeta.datasets;
  const data = samples[page] || samples.analysis;
  const Icon = data.icon;

  return (
    <div className="workspace-page">
      <div className="page-heading">
        <div>
          <span className="kicker">COGNIFY WORKSPACE</span>
          <h1>{meta.title}</h1>
          <p>{meta.subtitle}</p>
        </div>

        <button className="btn btn-primary btn-sm">
          <Icon size={15} />
          {data.action}
        </button>
      </div>

      <div className="workspace-banner">
        <div>
          <b>Current workflow: {meta.title}</b>
          <p>
            This Phase 1 screen is a functional UI scaffold;
            backend execution is intentionally not connected yet.
          </p>
        </div>

        <UploadCloud size={30} />
      </div>

      <div className="workspace-cards">
        {data.cards.map(([a, b, c]) => (
          <article className="info-card" key={a}>
            <div className="feature-icon">
              <Icon size={18} />
            </div>

            <small>{a}</small>
            <b>{b}</b>
            <span>{c}</span>
          </article>
        ))}
      </div>

      <div className="panel empty-workflow">
        <div className="empty-icon">
          <Icon size={24} />
        </div>

        <h2>Interactive {meta.title} workspace</h2>

        <p>
          The UI foundation is ready. In Phase 2 we will connect
          real dataset ingestion and the Python/AI backend to this screen.
        </p>

        <div className="steps-mini">
          <span>UI ✓</span>
          <span>Routing ✓</span>
          <span>Theme ✓</span>
          <span>API → Phase 2</span>
        </div>
      </div>
    </div>
  );
}