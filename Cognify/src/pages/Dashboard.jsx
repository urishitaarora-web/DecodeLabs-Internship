import {
  Activity,
  ArrowUpRight,
  Database,
  Gauge,
  TrendingUp
} from "lucide-react";

import { Link } from "react-router-dom";

export default function Dashboard() {
  const metrics = [
    ["Active datasets", "24", Database],
    ["Models trained", "18", Activity],
    ["Predictions", "12,480", TrendingUp],
    ["Best accuracy", "94.82%", Gauge]
  ];

  return (
    <div className="dashboard">

      <div className="page-heading">
        <div>
          <span className="kicker">OVERVIEW</span>

          <h1>Dashboard</h1>

          <p>
            Your machine learning workspace at a glance.
          </p>
        </div>

        <Link
          className="btn btn-primary btn-sm"
          to="/app/datasets"
        >
          + Upload Dataset
        </Link>
      </div>

      <div className="metric-grid">
        {metrics.map(([label, val, Icon], i) => (
          <div
            className={`metric-card ${
              i === 3 ? "metric-dark" : ""
            }`}
            key={label}
          >
            <Icon size={18} />

            <small>{label}</small>

            <b>{val}</b>
          </div>
        ))}
      </div>

      <div className="dashboard-grid">

        <section className="panel chart-panel">
          <div className="panel-head">
            <b>Model Performance</b>
            <small>
              F1 score across recent training runs
            </small>
          </div>

          <div className="line-chart">
            <svg
              viewBox="0 0 700 240"
              preserveAspectRatio="none"
            >
              <path
                d="M0 205 C80 170 100 145 160 130 S260 110 320 90 S440 70 520 50 S620 43 700 28"
                fill="none"
                stroke="currentColor"
                strokeWidth="3"
              />

              <path
                d="M0 210 C80 195 120 180 170 170 S260 150 330 132 S450 105 530 91 S620 80 700 68"
                fill="none"
                stroke="currentColor"
                strokeOpacity=".28"
                strokeDasharray="7 7"
                strokeWidth="2"
              />
            </svg>
          </div>
        </section>

        <section className="panel">
          <div className="panel-head">
            <b>Active Training</b>
            <small>View all</small>
          </div>

          <div className="activity">
            <div>
              <span>●</span>
              <b>Vision_Transformer_v3</b>
              <small>76%</small>
            </div>

            <div>
              <span>●</span>
              <b>NLP_BERT_Large_Tuned</b>
              <small>42%</small>
            </div>

            <div>
              <span>✓</span>
              <b>Audio_Wave2Vec_Base</b>
              <small>100%</small>
            </div>

            <div>
              <span>!</span>
              <b>RL_Agent_Omega</b>
              <small>Failed</small>
            </div>
          </div>
        </section>

        <section className="panel">
          <div className="panel-head">
            <b>Inference Load</b>
            <small>24h</small>
          </div>

          <div className="donut">
            <div>
              <b>12.4K</b>
              <small>Total predictions</small>
            </div>
          </div>
        </section>

        <section className="panel">
          <div className="panel-head">
            <b>Recent Datasets</b>
            <small>View all</small>
          </div>

          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              <tr>
                <td>customer_churn_2023</td>
                <td>Tabular</td>
                <td><em>Ready</em></td>
              </tr>

              <tr>
                <td>imageNet_2024</td>
                <td>Vision</td>
                <td><em>Ready</em></td>
              </tr>

              <tr>
                <td>sensor_logs</td>
                <td>Time Series</td>
                <td><em>Processing</em></td>
              </tr>
            </tbody>
          </table>
        </section>

      </div>
    </div>
  );
}