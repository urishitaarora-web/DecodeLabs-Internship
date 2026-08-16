import React, {
  useEffect,
  useMemo,
  useState,
} from "react";
import { useAuth } from "@clerk/react";
import {
  BarChart3,
  CheckCircle2,
  Database,
  AlertTriangle,
  Loader2,
  RefreshCw,
  PieChart as PieChartIcon,
  Activity,
} from "lucide-react";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ZAxis,
  CartesianGrid,
  Tooltip,
  ScatterChart,
  Scatter,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";

export default function AnalysisPage() {
  const { getToken, isLoaded, userId } = useAuth();

  const apiUrl = import.meta.env.VITE_API_URL;

  const [datasets, setDatasets] = useState([]);
  const [selectedDatasetId, setSelectedDatasetId] = useState("");

  const [analysis, setAnalysis] = useState(null);

  const [loadingDatasets, setLoadingDatasets] = useState(true);
  const [loadingAnalysis, setLoadingAnalysis] = useState(false);

  const [error, setError] = useState("");

  const [eda, setEda] = useState(null);
  const [edaLoading, setEdaLoading] = useState(false);
  const [edaError, setEdaError] = useState("");
  const [selectedNumericColumn, setSelectedNumericColumn] = useState("");

  /* =====================================================
     FETCH DATASETS
  ===================================================== */

  const fetchDatasets = async () => {
    if (!isLoaded || !userId) return;

    setLoadingDatasets(true);
    setError("");

    try {
      const token = await getToken();

      const response = await fetch(`${apiUrl}/datasets/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to load datasets."
        );
      }

      const availableDatasets = data.datasets || [];

      setDatasets(availableDatasets);

      if (
        availableDatasets.length > 0 &&
        !selectedDatasetId
      ) {
        setSelectedDatasetId(availableDatasets[0].id);
      }
    } catch (err) {
      console.error("Dataset loading error:", err);

      setError(
        err.message || "Unable to load datasets."
      );
    } finally {
      setLoadingDatasets(false);
    }
  };

  /* =====================================================
     FETCH MAIN ANALYSIS
  ===================================================== */

  const runAnalysis = async (
    datasetId = selectedDatasetId
  ) => {
    if (!datasetId) {
      setError("Select a dataset first.");
      return;
    }

    if (!isLoaded) {
      setError("Authentication is still loading.");
      return;
    }

    if (!userId) {
      setError(
        "Please sign in before analyzing a dataset."
      );
      return;
    }

    setLoadingAnalysis(true);
    setError("");

    try {
      const token = await getToken();

      const response = await fetch(
        `${apiUrl}/analysis/dataset/${datasetId}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();
      console.log("FULL ANALYSIS RESPONSE:", data);
console.log("FIRST COLUMN:", data?.columns?.[0]);
console.log("ALL COLUMNS:", data?.columns);
      console.log(
  "RUNS COLUMN:",
  data?.columns?.find(
    (column) => column.name === "runs"
  )
);

console.log(
  "RUNS VARIANCE:",
  data?.columns?.find(
    (column) => column.name === "runs"
  )?.statistics?.variance
);

      if (!response.ok) {
        throw new Error(
          data.detail || "Dataset analysis failed."
        );
      }

      setAnalysis(data);
    } catch (err) {
      console.error("Analysis error:", err);

      setAnalysis(null);

      setError(
        err.message ||
          "Unable to analyze dataset."
      );
    } finally {
      setLoadingAnalysis(false);
    }
  };

  /* =====================================================
     FETCH EDA
  ===================================================== */

  const fetchEDA = async (datasetId) => {
    if (!datasetId || !isLoaded || !userId) return;

    setEdaLoading(true);
    setEdaError("");

    try {
      const token = await getToken();

      const response = await fetch(
        `${apiUrl}/datasets/${datasetId}/eda`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to load EDA data."
        );
      }

      setEda(data);
      if (
        data?.numeric_distributions?.length > 0
      ) {
        setSelectedNumericColumn(
          data.numeric_distributions[0].column
        );
      } else {
         setSelectedNumericColumn("");
      }
    } catch (err) {
      console.error("EDA fetch error:", err);

      setEda(null);

      setEdaError(
        err.message ||
          "Unable to load exploratory analysis."
      );
    } finally {
      setEdaLoading(false);
    }
  };

  /* =====================================================
     INITIAL DATASET LOAD
  ===================================================== */

  useEffect(() => {
    if (isLoaded && userId) {
      fetchDatasets();
    }
  }, [isLoaded, userId]);

  /* =====================================================
     RUN ANALYSIS WHEN DATASET CHANGES
  ===================================================== */

  useEffect(() => {
    if (selectedDatasetId) {
      runAnalysis(selectedDatasetId);
      fetchEDA(selectedDatasetId);
    }
  }, [selectedDatasetId]);

  /* =====================================================
     SELECTED DATASET
  ===================================================== */

  const selectedDataset = useMemo(
    () =>
      datasets.find(
        (dataset) =>
          dataset.id === selectedDatasetId
      ),
    [datasets, selectedDatasetId]
  );

  /* =====================================================
     CATEGORICAL DATA
  ===================================================== */

  const categoricalChartData = useMemo(() => {
    if (
      !eda?.categorical_distributions ||
      eda.categorical_distributions.length === 0
    ) {
      return null;
    }

    return (
      eda.categorical_distributions
        .filter(
          (item) =>
            item?.unique <= 50 &&
            item?.distribution?.length > 0
        )
        .sort(
          (a, b) =>
            a.unique - b.unique
        )[0] || null
    );
  }, [eda]);

  /* =====================================================
     MISSING VALUE CHART DATA
  ===================================================== */

  const missingChartData = useMemo(() => {
    if (!eda?.missing_values) return [];

    return eda.missing_values
      .filter((item) => item.missing > 0)
      .sort(
        (a, b) =>
          b.missing - a.missing
      )
      .slice(0, 10);
  }, [eda]);

  /* =====================================================
     COMPOSITION CHART
  ===================================================== */

  const compositionChartData = useMemo(() => {
    if (!eda?.summary) return [];

    return [
      {
        name: "Numeric",
        value: eda.summary.numeric_columns || 0,
      },
      {
        name: "Categorical",
        value:
          eda.summary.categorical_columns || 0,
      },
      {
        name: "Datetime",
        value:
          eda.summary.datetime_columns || 0,
      },
    ].filter((item) => item.value > 0);
  }, [eda]);

  const chartColors = [
    "#6366f1",
    "#14b8a6",
    "#f59e0b",
    "#ec4899",
    "#8b5cf6",
    "#06b6d4",
    "#f97316",
    "#22c55e",
  ];

  /* =====================================================
     RETURN
  ===================================================== */

  return (
    <div className="workspace-page analysis-page">

      {/* =================================================
          HEADER
      ================================================= */}

      <div className="page-heading">
        <div>
          <span className="kicker">
            COGNIFY WORKSPACE
          </span>

          <h1>Dataset Analysis</h1>

          <p>
            Explore dataset structure, quality,
            missing values, distributions,
            and relationships.
          </p>
        </div>
      </div>

      {/* =================================================
          DATASET SELECTOR
      ================================================= */}

      <section className="dataset-section dataset-selector-section">

        <div className="dataset-section-heading">
          <h2>Select Dataset</h2>

          <p>
            Choose a saved dataset to inspect
            with Cognify's analysis engine.
          </p>
        </div>

        <div className="dataset-selector-row">

          <select
            value={selectedDatasetId}
            onChange={(event) =>
              setSelectedDatasetId(
                event.target.value
              )
            }
            disabled={
              loadingDatasets ||
              datasets.length === 0
            }
          >
            <option value="">
              {loadingDatasets
                ? "Loading datasets..."
                : datasets.length === 0
                ? "No saved datasets"
                : "Select a dataset"}
            </option>

            {datasets.map((dataset) => (
              <option
                key={dataset.id}
                value={dataset.id}
              >
                {dataset.filename}
              </option>
            ))}
          </select>

          <button
            type="button"
            className="btn btn-primary btn-sm"
            onClick={() =>
              runAnalysis()
            }
            disabled={
              loadingAnalysis ||
              edaLoading ||
              !selectedDatasetId
            }
          >
            {loadingAnalysis ? (
              <Loader2
                size={15}
                className="spin"
              />
            ) : (
              <RefreshCw size={15} />
            )}

            {loadingAnalysis
              ? "Analyzing..."
              : "Refresh Analysis"}
          </button>

        </div>

        {selectedDataset && (
          <div className="selected-dataset">
            Selected:
            <strong>
              {selectedDataset.filename}
            </strong>
          </div>
        )}

      </section>

      {/* =================================================
          MAIN ERROR
      ================================================= */}

      {error && (
        <div className="upload-error">
          <AlertTriangle size={17} />
          {error}
        </div>
      )}

      {/* =================================================
          EMPTY STATE
      ================================================= */}

      {!loadingAnalysis &&
        !analysis &&
        !error &&
        datasets.length === 0 && (
          <section className="panel empty-workflow">

            <div className="empty-icon">
              <Database size={24} />
            </div>

            <h2>
              No datasets available
            </h2>

            <p>
              Upload and analyze a dataset
              from the Datasets page first.
            </p>

          </section>
        )}

      {/* =================================================
          ANALYSIS LOADING
      ================================================= */}

      {loadingAnalysis && (
        <section className="analysis-loading-card">

          <div className="loading-spinner-wrap">
            <Loader2
              size={26}
              className="spin"
            />
          </div>

          <div>
            <strong>
              Cognify is analyzing your dataset
            </strong>

            <p>
              Inspecting structure, quality,
              missing values and statistics...
            </p>
          </div>

        </section>
      )}

      {/* =================================================
          EDA LOADING
      ================================================= */}

      {edaLoading && !loadingAnalysis && (
        <section className="eda-loading-card">

          <div className="eda-loading-animation">
            <Activity size={23} />
          </div>

          <div className="eda-loading-content">

            <strong>
              Generating exploratory analysis
            </strong>

            <p>
              Cognify is preparing charts,
              distributions and dataset insights...
            </p>

            <div className="eda-loading-bar">
              <div className="eda-loading-progress" />
            </div>

          </div>

        </section>
      )}

      {/* =================================================
          EDA ERROR
      ================================================= */}

      {edaError && !edaLoading && (
        <div className="eda-error-card">
          <AlertTriangle size={18} />

          <div>
            <strong>
              Exploratory analysis unavailable
            </strong>

            <p>{edaError}</p>
          </div>
        </div>
      )}

      {/* =================================================
          ANALYSIS CONTENT
      ================================================= */}

      {analysis && !loadingAnalysis && (
        <>

          {/* =================================================
              DATASET OVERVIEW
          ================================================= */}

          <section className="dataset-section">

            <div className="dataset-section-heading">
              <h2>Dataset Overview</h2>

              <p>
                Analysis results for{" "}
                <strong>
                  {analysis.dataset.filename}
                </strong>
              </p>
            </div>

            <div className="metric-grid">

              <div className="metric-card metric-purple">
                <Database size={18} />

                <small>Total Rows</small>

                <b>
                  {analysis.dataset.rows.toLocaleString()}
                </b>
              </div>

              <div className="metric-card metric-blue">
                <BarChart3 size={18} />

                <small>Total Columns</small>

                <b>
                  {analysis.dataset.columns}
                </b>
              </div>

              <div className="metric-card metric-orange">
                <AlertTriangle size={18} />

                <small>Missing Values</small>

                <b>
                  {analysis.dataset.missing_values.toLocaleString()}
                </b>

                <span>
                  {analysis.dataset.missing_percentage}%
                </span>
              </div>

              <div className="metric-card metric-green">
                <CheckCircle2 size={18} />

                <small>Data Quality</small>

                <b>
                  {analysis.dataset.data_quality ?? "—"}%
                </b>
              </div>

            </div>
          </section>

          {/* =================================================
              DATASET HEALTH
          ================================================= */}

          {eda?.dataset && eda?.summary && (
            <section className="eda-section">

              <div className="eda-section-header">
                <div>
                  <span className="eda-kicker">
                    DATASET HEALTH
                  </span>

                  <h2>Dataset Health</h2>

                  <p>
                    Overview of the dataset
                    structure and quality.
                  </p>
                </div>
              </div>

              <div className="health-grid">

                <div className="health-card health-purple">
                  <div className="health-card-label">
                    Total Rows
                  </div>

                  <div className="health-card-value">
                    {eda.dataset.rows.toLocaleString()}
                  </div>

                  <div className="health-card-sub">
                    Records analyzed
                  </div>
                </div>

                <div className="health-card health-blue">
                  <div className="health-card-label">
                    Total Columns
                  </div>

                  <div className="health-card-value">
                    {eda.dataset.columns}
                  </div>

                  <div className="health-card-sub">
                    Features detected
                  </div>
                </div>

                <div className="health-card health-orange">
                  <div className="health-card-label">
                    Missing Cells
                  </div>

                  <div className="health-card-value">
                    {eda.summary.missing_cells.toLocaleString()}
                  </div>

                  <div className="health-card-sub">
                    Across all columns
                  </div>
                </div>

                <div className="health-card health-pink">
                  <div className="health-card-label">
                    Duplicate Rows
                  </div>

                  <div className="health-card-value">
                    {eda.summary.duplicate_rows.toLocaleString()}
                  </div>

                  <div className="health-card-sub">
                    Exact duplicates
                  </div>
                </div>

                <div className="health-card health-teal">
                  <div className="health-card-label">
                    Numeric Columns
                  </div>

                  <div className="health-card-value">
                    {eda.summary.numeric_columns}
                  </div>

                  <div className="health-card-sub">
                    Quantitative features
                  </div>
                </div>

                <div className="health-card health-indigo">
                  <div className="health-card-label">
                    Categorical Columns
                  </div>

                  <div className="health-card-value">
                    {eda.summary.categorical_columns}
                  </div>

                  <div className="health-card-sub">
                    Categorical features
                  </div>
                </div>

                <div className="health-card health-cyan">
                  <div className="health-card-label">
                    Datetime Columns
                  </div>

                  <div className="health-card-value">
                    {eda.summary.datetime_columns}
                  </div>

                  <div className="health-card-sub">
                    Temporal features
                  </div>
                </div>

              </div>
            </section>
          )}

          {/* ================================
                AI / COGNIFY RECOMMENDATIONS
          ================================ */}

{eda?.recommendations?.length > 0 && (
  <section className="eda-section ai-recommendations">

    <div className="eda-section-header">
      <div>
        <span className="eda-kicker">
          COGNIFY AI
        </span>

        <h2>
          AI Recommendations
        </h2>

        <p>
          Intelligent preprocessing recommendations
          generated from your dataset.
        </p>
      </div>
    </div>

    <div className="insights-grid">

      {eda.recommendations.map(
        (recommendation, index) => (

          <div
            className="insight-card"
            key={`${recommendation.title}-${index}`}
          >

            <div className="insight-icon">
              {recommendation.type === "success"
                ? "✓"
                : recommendation.type === "warning"
                ? "!"
                : "◆"}
            </div>

            <div>

              <strong>
                {recommendation.title}
              </strong>

              <p>
                {recommendation.message}
              </p>

            </div>

          </div>

        )
      )}

    </div>

  </section>
)}
          {/* =================================================
              INSIGHTS
          ================================================= */}

          {eda?.summary && (
            <section className="eda-section">

              <div className="eda-section-header">
                <div>
                  <span className="eda-kicker">
                    COGNIFY INSIGHTS
                  </span>

                  <h2>
                    Data Quality Insights
                  </h2>

                  <p>
                    Automatically generated
                    observations from the dataset.
                  </p>
                </div>
              </div>

              <div className="insights-grid">

                <div className="insight-card">
                  <div className="insight-icon insight-success">
                    {eda.summary.missing_cells === 0
                      ? "✓"
                      : "!"}
                  </div>

                  <div>
                    <strong>
                      {eda.summary.missing_cells === 0
                        ? "Complete dataset"
                        : "Missing data detected"}
                    </strong>

                    <p>
                      {eda.summary.missing_cells === 0
                        ? "No missing cells were found across the dataset."
                        : `${eda.summary.missing_cells.toLocaleString()} missing cells require attention.`}
                    </p>
                  </div>
                </div>

                <div className="insight-card">
                  <div className="insight-icon insight-info">
                    {eda.summary.duplicate_rows === 0
                      ? "✓"
                      : "!"}
                  </div>

                  <div>
                    <strong>
                      {eda.summary.duplicate_rows === 0
                        ? "No duplicate rows"
                        : "Duplicate records detected"}
                    </strong>

                    <p>
                      {eda.summary.duplicate_rows === 0
                        ? "The dataset contains no exact duplicate records."
                        : `${eda.summary.duplicate_rows.toLocaleString()} duplicate rows were detected.`}
                    </p>
                  </div>
                </div>

                <div className="insight-card">
                  <div className="insight-icon insight-purple">
                    ◈
                  </div>

                  <div>
                    <strong>
                      Mixed feature types
                    </strong>

                    <p>
                      The dataset contains{" "}
                      {eda.summary.numeric_columns} numeric,{" "}
                      {eda.summary.categorical_columns} categorical
                      and{" "}
                      {eda.summary.datetime_columns} datetime columns.
                    </p>
                  </div>
                </div>

                <div className="insight-card">
                  <div className="insight-icon insight-orange">
                    ◆
                  </div>

                  <div>
                    <strong>
                      Dataset scale
                    </strong>

                    <p>
                      Cognify analyzed{" "}
                      {eda.dataset.rows.toLocaleString()} records
                      across {eda.dataset.columns} columns.
                    </p>
                  </div>
                </div>

              </div>
            </section>
          )}

          {/* =================================================
              CHARTS
          ================================================= */}

          {eda && (
            <section className="eda-section">

              <div className="eda-section-header">
                <div>
                  <span className="eda-kicker">
                    VISUAL ANALYTICS
                  </span>

                  <h2>
                    Dataset Visualizations
                  </h2>

                  <p>
                    Visual breakdown of important
                    dataset characteristics.
                  </p>
                </div>
              </div>

              <div className="chart-grid">

                {/* COMPOSITION */}

                {compositionChartData.length > 0 && (
                  <div className="chart-card">

                    <div className="chart-card-header">
                      <div className="chart-icon chart-icon-purple">
                        <PieChartIcon size={18} />
                      </div>

                      <div>
                        <strong>
                          Column Composition
                        </strong>

                        <span>
                          Distribution of feature types
                        </span>
                      </div>
                    </div>

                    <div className="chart-container chart-pie">
                      <ResponsiveContainer
                        width="100%"
                        height={330}
                      >
                        <PieChart>

                          <Pie
                            data={compositionChartData}
                            dataKey="value"
                            nameKey="name"
                            cx="50%"
                            cy="50%"
                            outerRadius={105}
                            innerRadius={55}
                            paddingAngle={4}
                          >
                            {compositionChartData.map(
                              (_, index) => (
                                <Cell
                                  key={index}
                                  fill={
                                    chartColors[index %
                                      chartColors.length]
                                  }
                                />
                              )
                            )}
                          </Pie>

                          <Tooltip />

                          <Legend
                            verticalAlign="bottom"
                            height={36}
                          />

                        </PieChart>
                      </ResponsiveContainer>
                    </div>

                  </div>
                )}

                {/* CATEGORICAL */}

                {categoricalChartData && (
                  <div className="chart-card">

                    <div className="chart-card-header">
                      <div className="chart-icon chart-icon-blue">
                        <BarChart3 size={18} />
                      </div>

                      <div>
                        <strong>
                          {categoricalChartData.column} Distribution
                        </strong>

                        <span>
                          Most frequent categories
                        </span>
                      </div>
                    </div>

                    <div className="chart-container">
                      <ResponsiveContainer
                        width="100%"
                        height={350}
                      >
                        <BarChart
                          data={
                            categoricalChartData.distribution
                          }
                          layout="vertical"
                          margin={{
                            top: 10,
                            right: 25,
                            left: 20,
                            bottom: 10,
                          }}
                        >

                          <CartesianGrid
                            strokeDasharray="3 3"
                            opacity={0.25}
                          />

                          <XAxis
                            type="number"
                          />

                          <YAxis
                            type="category"
                            dataKey="category"
                            width={100}
                          />

                          <Tooltip />

                          <Bar
                            dataKey="count"
                            name="Records"
                            radius={[
                              0,
                              8,
                              8,
                              0,
                            ]}
                            fill="#6366f1"
                          >
                            {categoricalChartData.distribution.map(
                              (_, index) => (
                                <Cell
                                  key={index}
                                  fill={
                                    chartColors[index %
                                      chartColors.length]
                                  }
                                />
                              )
                            )}
                          </Bar>

                        </BarChart>
                      </ResponsiveContainer>
                    </div>

                  </div>
                )}


              </div>
            </section>
          )}

          {/* =================================================
              MISSING VALUES TABLE
          ================================================= */}

          {eda?.missing_values && (
            <section className="eda-section">

              <div className="eda-section-header">
                <div>
                  <span className="eda-kicker">
                    DATA QUALITY
                  </span>

                  <h2>Missing Values</h2>

                  <p>
                    Columns containing missing
                    data that may require preprocessing.
                  </p>
                </div>
              </div>

              <div className="eda-table-card">

                {eda.missing_values.filter(
                  (item) =>
                    item.missing > 0
                ).length === 0 ? (

                  <div className="empty-eda-state">

                    <div className="empty-eda-icon">
                      <CheckCircle2 size={22} />
                    </div>

                    <div>
                      <strong>
                        No missing values detected
                      </strong>

                      <p>
                        All columns in this
                        dataset are complete.
                      </p>
                    </div>

                  </div>

                 ) : (

                  <div className="eda-table-wrapper">

                    <table className="eda-table">

                      <thead>
                        <tr>
                          <th>Column</th>
                          <th>Missing Values</th>
                          <th>Missing %</th>
                          <th>Severity</th>
                        </tr>
                      </thead>

                      <tbody>

                        {eda.missing_values
                          .filter(
                            (item) =>
                              item.missing > 0
                          )
                          .map((item) => {

                            const severity =
                              item.percentage >= 50
                                ? "High"
                                : item.percentage >= 10
                                ? "Medium"
                                : "Low";

                            return (
                              <tr
                                key={item.column}
                              >

                                <td>
                                  <strong>
                                    {item.column}
                                  </strong>
                                </td>

                                <td>
                                  {item.missing.toLocaleString()}
                                </td>

                                <td>
                                  {item.percentage.toFixed(
                                    2
                                  )}
                                  %
                                </td>

                                <td>
                                  <span
                                    className={`missing-badge missing-${severity.toLowerCase()}`}
                                  >
                                    {severity}
                                  </span>
                                </td>

                              </tr>
                            );
                          })}

                      </tbody>

                    </table>

                  </div>
                )}

              </div>
            </section>
          )}

          {/* ================================
            DATASET PREVIEW
           ================================ */}

        {eda?.preview?.length > 0 && (
          <section className="eda-section">

          <div className="eda-section-header">
            <div>
             <span className="eda-kicker">
                  DATASET EXPLORER
             </span>

             <h2>
                  Dataset Preview
             </h2>

             <p>
                Preview of the first 10 rows of the selected dataset.
             </p>
          </div>
        </div>

    <div className="eda-table-card">

      <div className="eda-table-wrapper">

        <table className="eda-table">

          <thead>
            <tr>
              {Object.keys(eda.preview[0]).map(
                (column) => (
                  <th key={column}>
                    {column}
                  </th>
                )
              )}
            </tr>
          </thead>

          <tbody>

            {eda.preview.map(
              (row, rowIndex) => (

                <tr key={rowIndex}>

                  {Object.keys(eda.preview[0]).map(
                    (column) => (

                      <td key={column}>
                        {row[column] === null ||
                        row[column] === undefined
                          ? "—"
                          : String(row[column])}
                      </td>

                    )
                  )}

                </tr>

              )
            )}

          </tbody>

        </table>

      </div>

    </div>

  </section>
)}

          {/* ================================
                  CORRELATION HEATMAP
          ================================ */}

{eda?.correlation?.columns?.length >= 2 && (
  <section className="eda-section">

    <div className="eda-section-header">
      <div>
        <span className="eda-kicker">
          RELATIONSHIPS
        </span>

        <h2>
          Correlation Heatmap
        </h2>

        <p>
          Explore relationships between numeric
          features in the dataset.
        </p>
      </div>
    </div>

    <div className="eda-heatmap-card">

      <div
        className="eda-heatmap"
        style={{
          gridTemplateColumns: `120px repeat(${eda.correlation.columns.length}, minmax(70px, 1fr))`,
        }}
      >

        {/* Empty top-left cell */}
        <div className="heatmap-corner" />

        {/* Column headers */}
        {eda.correlation.columns.map(
          (column) => (
            <div
              key={`header-${column}`}
              className="heatmap-label heatmap-column-label"
              title={column}
            >
              {column}
            </div>
          )
        )}

        {/* Matrix */}
        {eda.correlation.matrix.map(
          (row) => (
            <React.Fragment key={row.column}>

              <div
                className="heatmap-label heatmap-row-label"
                title={row.column}
              >
                {row.column}
              </div>

              {eda.correlation.columns.map(
                (column) => {

                  const value = Number(
                    row[column]
                  );

                  const intensity =
                    Math.min(
                      Math.abs(value),
                      1
                    );

                  return (
                    <div
                      key={`${row.column}-${column}`}
                      className="heatmap-cell"
                      style={{
                        background:
                          value >= 0
                            ? `rgba(59, 130, 246, ${0.12 + intensity * 0.78})`
                            : `rgba(236, 72, 153, ${0.12 + intensity * 0.78})`,
                      }}
                      title={`${row.column} vs ${column}: ${value.toFixed(3)}`}
                    >
                      {value.toFixed(2)}
                    </div>
                  );
                }
              )}

            </React.Fragment>
          )
        )}

      </div>

      <div className="heatmap-legend">

        <span>
          Negative
        </span>

        <div className="heatmap-gradient" />

        <span>
          Positive
        </span>

      </div>

    </div>

  </section>
)}

          {/* =========================================================
    NUMERIC DISTRIBUTION
========================================================= */}

{eda?.numeric_distributions?.length > 0 && (
  <section className="eda-section">

    <div className="eda-section-header">
      <div>
        <span className="eda-kicker">
          NUMERIC ANALYSIS
        </span>

        <h2>Numeric Distribution</h2>

        <p>
          Explore the distribution of individual numeric columns.
        </p>
      </div>
    </div>

    {/* COLUMN SELECTOR */}

    <div className="numeric-selector">

      <label htmlFor="numeric-column">
        Select Numeric Column
      </label>

      <select
        id="numeric-column"
        value={selectedNumericColumn}
        onChange={(event) =>
          setSelectedNumericColumn(
            event.target.value
          )
        }
      >

        {eda.numeric_distributions.map(
          (item) => (
            <option
              key={item.column}
              value={item.column}
            >
              {item.column}
            </option>
          )
        )}

      </select>

    </div>

    {/* SELECTED COLUMN */}

    {(() => {

      const selectedNumericData =
        eda.numeric_distributions.find(
          (item) =>
            item.column ===
            selectedNumericColumn
        );

      if (!selectedNumericData) {
        return null;
      }

      return (
        <div className="numeric-analysis-grid">

          {/* Histogram */}

          <div className="panel eda-chart-panel">

            <div className="panel-head">

              <div>

                <b>
                  {selectedNumericData.column}
                </b>

                <small>
                  Numeric distribution
                </small>

              </div>

            </div>

            <div className="eda-chart">

              <ResponsiveContainer
                width="100%"
                height={400}
              >

                <BarChart
                  data={
                    selectedNumericData.histogram
                  }
                  margin={{
                    top: 20,
                    right: 30,
                    left: 20,
                    bottom: 60,
                  }}
                >

                  <CartesianGrid
                    strokeDasharray="3 3"
                  />

                  <XAxis
                    dataKey="bin"
                    angle={-35}
                    textAnchor="end"
                    interval={0}
                  />

                  <YAxis />

                  <Tooltip />

                  <Bar
                    dataKey="count"
                    name="Records"
                    radius={[
                      0,
                      6,
                      6,
                      0,
                    ]}
                    >
  {eda.numeric_distributions[0].histogram.map(
    (entry, index) => (
      <Cell
        key={`cell-${index}`}
        fill={
          [
            "#6366F1",
            "#8B5CF6",
            "#A855F7",
            "#EC4899",
            "#F97316",
            "#F59E0B",
            "#10B981",
            "#06B6D4",
          ][index % 8]
        }
      />
    )
  )}
</Bar>
                </BarChart>

              </ResponsiveContainer>

            </div>

          </div>

          {/* Statistics */}

          <div className="numeric-stats-card">

            <span className="eda-kicker">
              STATISTICS
            </span>

            <h3>
              {selectedNumericData.column}
            </h3>

            <div className="numeric-stats-grid">

              <div>
                <span>Count</span>
                <strong>
                  {selectedNumericData.count}
                </strong>
              </div>

              <div>
                <span>Sum</span>
                <strong>
                  {selectedNumericData.sum?.toLocaleString()}
                </strong>
              </div>

              <div>
                <span>Mean</span>
                <strong>
                  {selectedNumericData.mean}
                </strong>
              </div>

              <div>
                <span>Median</span>
                <strong>
                  {selectedNumericData.median}
                </strong>
              </div>

              <div>
                <span>Minimum</span>
                <strong>
                  {selectedNumericData.min}
                </strong>
              </div>

              <div>
                <span>Maximum</span>
                <strong>
                  {selectedNumericData.max}
                </strong>
              </div>

              <div>
                <span>Variance</span>
                <strong>
                    {selectedNumericData.variance}
                </strong>
              </div>
              <div>
                <span>Std. Deviation</span>
                <strong>
                  {selectedNumericData.std}
                </strong>
              </div>

            </div>

          </div>

        </div>
      );

    })()}

  </section>
)}

          {/* ================================
    OUTLIER DETECTION + BOX PLOT
================================ */}

{eda?.outliers?.length > 0 && (
  <section className="eda-section">

    <div className="eda-section-header">
      <div>
        <span className="eda-kicker">
          ANOMALY ANALYSIS
        </span>

        <h2>
          Outlier Detection
        </h2>

        <p>
          Identify unusual values using the
          interquartile range (IQR) method.
        </p>
      </div>
    </div>

    <div className="outlier-grid">

      {eda.outliers.map((item) => {

        const min = Number(item.min);
        const q1 = Number(item.q1);
        const median = Number(item.median);
        const q3 = Number(item.q3);
        const max = Number(item.max);

        const range = max - min || 1;

        const q1Position =
          ((q1 - min) / range) * 100;

        const medianPosition =
          ((median - min) / range) * 100;

        const q3Position =
          ((q3 - min) / range) * 100;

        const severity =
          item.percentage >= 10
            ? "high"
            : item.percentage >= 5
            ? "medium"
            : "low";

        return (
          <article
            className="outlier-card"
            key={item.column}
          >

            <div className="outlier-card-header">

              <div>
                <strong>
                  {item.column}
                </strong>

                <span>
                  {item.count.toLocaleString()} outliers
                </span>
              </div>

              <span
                className={`outlier-badge outlier-${severity}`}
              >
                {severity.toUpperCase()}
              </span>

            </div>

            {/* BOX PLOT */}

            <div className="boxplot-wrapper">

              <div className="boxplot-values">

                <span>
                  Min: {item.min ?? "—"}
                </span>

                <span>
                  Q1: {item.q1 ?? "—"}
                </span>

                <span>
                  Median: {item.median ?? "—"}
                </span>

                <span>
                  Q3: {item.q3 ?? "—"}
                </span>

                <span>
                  Max: {item.max ?? "—"}
                </span>

              </div>

              <div className="boxplot">

                {/* WHISKER LINE */}

                <div
                  className="boxplot-whisker"
                  style={{
                    left: "0%",
                    right: "0%",
                  }}
                />

                {/* MIN WHISKER */}

                <div
                  className="boxplot-cap"
                  style={{
                    left: "0%",
                  }}
                />

                {/* MAX WHISKER */}

                <div
                  className="boxplot-cap"
                  style={{
                    left: "100%",
                  }}
                />

                {/* BOX */}

                <div
                  className="boxplot-box"
                  style={{
                    left: `${q1Position}%`,
                    width: `${Math.max(
                      q3Position - q1Position,
                      1
                    )}%`,
                  }}
                />

                {/* MEDIAN */}

                <div
                  className="boxplot-median"
                  style={{
                    left: `${medianPosition}%`,
                  }}
                />

              </div>

            </div>

            {/* OUTLIER INFO */}

            <div className="outlier-stats">

              <div>
                <span>
                  Outliers
                </span>

                <strong>
                  {item.count.toLocaleString()}
                </strong>
              </div>

              <div>
                <span>
                  Percentage
                </span>

                <strong>
                  {item.percentage}%
                </strong>
              </div>

              <div>
                <span>
                  Lower Bound
                </span>

                <strong>
                  {item.lower_bound ?? "—"}
                </strong>
              </div>

              <div>
                <span>
                  Upper Bound
                </span>

                <strong>
                  {item.upper_bound ?? "—"}
                </strong>
              </div>

            </div>

          </article>
        );
      })}

    </div>

  </section>
)}
          {/* =================================================
              COLUMN INTELLIGENCE
          ================================================= */}

          <section className="dataset-section">

            <div className="dataset-section-heading">

              <h2>
                Column Intelligence
              </h2>

              <p>
                Detailed statistics for every
                detected column.
              </p>

            </div>

            <div className="panel column-intelligence-panel">

              <div className="table-scroll">

                <table className="eda-table intelligence-table">

                  <thead>
                    <tr>
                      <th>Column</th>
                      <th>Type</th>
                      <th>Missing</th>
                      <th>Unique</th>
                      <th>Sum</th>
                      <th>Mean</th>
                      <th>Median</th>
                      <th>Variance</th>
                      <th>Std. Deviation</th>
                      <th>Min</th>
                      <th>Max</th>
                    </tr>
                  </thead>

                  <tbody>

                    {analysis.columns.map(
                      (column, index) => (
                        <tr
                          key={`${column.name}-${index}`}
                        >

                          <td>
                            <strong>
                              {column.name}
                            </strong>
                          </td>

                          <td>
                            <span className="dtype-badge">
                              {column.dtype}
                            </span>
                          </td>

                          <td>
                            {column.missing}
                            {" "}
                            ({column.missing_percentage}%)
                          </td>

                          <td>
                            {column.unique}
                          </td>

                          <td>
                            {column.statistics?.sum != null
                              ? column.statistics.sum.toLocaleString()
                            : "—"}
                          </td>

                          <td>
                            {column.statistics?.mean ??
                              "—"}
                          </td>

                          <td>
                            {column.statistics?.median ??
                              "—"}
                          </td>

                          <td>
                            {column.statistics?.variance ?? "—"}
                          </td>

                          <td>
                            {column.statistics?.std ?? "—"}
                          </td>
                          
                          <td>
                            {column.statistics?.min ??
                              "—"}
                          </td>

                          <td>
                            {column.statistics?.max ??
                              "—"}
                          </td>

                        </tr>
                      )
                    )}

                  </tbody>

                </table>

              </div>

            </div>

          </section>

        </>
      )}
    </div>
  );
}