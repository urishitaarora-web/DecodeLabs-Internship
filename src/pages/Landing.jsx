import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ArrowRight,
  Play,
  Moon,
  Sun,
  FileSpreadsheet,
  BarChart3,
  SlidersHorizontal,
  BrainCircuit,
  Activity,
  GitCompareArrows,
  Target,
  Lightbulb,
  Check,
  Database,
  Sparkles,
} from "lucide-react";

const workflowSteps = [
  {
    id: 1,
    title: "Raw Data",
    short: "UPLOAD",
    description: "Upload your CSV, Excel, or JSON files",
    icon: FileSpreadsheet,
    position: "step-1",
  },
  {
    id: 2,
    title: "Analysis",
    short: "ANALYZE",
    description: "Explore quality, patterns and insights",
    icon: BarChart3,
    position: "step-2",
  },
  {
    id: 3,
    title: "Preprocessing",
    short: "CLEAN",
    description: "Clean, encode and transform your data",
    icon: SlidersHorizontal,
    position: "step-3",
  },
  {
    id: 4,
    title: "Model Training",
    short: "TRAIN",
    description: "Train multiple machine learning algorithms",
    icon: BrainCircuit,
    position: "step-4",
  },
  {
    id: 5,
    title: "Evaluation",
    short: "MEASURE",
    description: "Evaluate model performance and metrics",
    icon: Activity,
    position: "step-5",
  },
  {
    id: 6,
    title: "Comparison",
    short: "COMPARE",
    description: "Compare models and choose the best one",
    icon: GitCompareArrows,
    position: "step-6",
  },
  {
    id: 7,
    title: "Prediction",
    short: "PREDICT",
    description: "Generate predictions from trained models",
    icon: Target,
    position: "step-7",
  },
  {
    id: 8,
    title: "Insights",
    short: "EXPLAIN",
    description: "Understand results and actionable insights",
    icon: Lightbulb,
    position: "step-8",
  },
];

function WorkflowCard({ step, index }) {
  const Icon = step.icon;

  return (
    <motion.div
      className={`workflow-card ${step.position}`}
      initial={{ opacity: 0, scale: 0.85 }}
      animate={{
        opacity: 1,
        scale: 1,
      }}
      transition={{
        delay: 0.3 + index * 0.08,
        duration: 0.5,
        ease: "easeOut",
      }}
    >
      <div className="workflow-number">{step.id}</div>

      <div className="workflow-icon">
        <Icon size={18} strokeWidth={1.8} />
      </div>

      <div className="workflow-card-content">
        <span>{step.short}</span>
        <strong>{step.title}</strong>
      </div>
    </motion.div>
  );
}

function CentralAI() {
  return (
    <motion.div
      className="central-ai"
      animate={{
        y: [0, -8, 0],
      }}
      transition={{
        duration: 4,
        repeat: Infinity,
        ease: "easeInOut",
      }}
    >
      <div className="ai-glow"></div>

      <div className="ai-platform">
        <motion.div
          className="cube cube-one"
          animate={{
            y: [0, -8, 0],
            rotate: [0, 6, 0],
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />

        <motion.div
          className="cube cube-two"
          animate={{
            y: [0, 10, 0],
            rotate: [0, -7, 0],
          }}
          transition={{
            duration: 3.5,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />

        <motion.div
          className="cube cube-three"
          animate={{
            y: [0, -5, 0],
            rotate: [0, 5, 0],
          }}
          transition={{
            duration: 2.8,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />

        <div className="ai-core">
          <BrainCircuit size={34} strokeWidth={1.4} />
        </div>
      </div>

      <div className="ai-label">
        <Sparkles size={12} />
        <span>COGNIFY AI ENGINE</span>
      </div>
    </motion.div>
  );
}

export default function Landing({ theme = "light", toggleTheme }) {
  const isDark = theme === "dark";

  const scrollToWorkflow = () => {
    document
      .getElementById("workflow")
      ?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="landing-page">
      {/* ================= NAVBAR ================= */}

      <header className="landing-navbar">
        <div className="navbar-inner">
          <Link to="/" className="brand">
            <div className="brand-mark">
              <span></span>
              <span></span>
              <span></span>
            </div>

            <span className="brand-name">Cognify</span>
          </Link>

          <nav className="desktop-nav">
            <a href="#product">Product</a>
            <a href="#features">Features</a>
            <a href="#workflow">Workflow</a>
            <a href="#solutions">Solutions</a>
            <a href="#resources">Resources</a>
            <a href="#pricing">Pricing</a>
          </nav>

          <div className="navbar-actions">
            <button
              className="theme-button"
              onClick={toggleTheme}
              aria-label="Toggle theme"
            >
              {isDark ? (
                <Sun size={17} />
              ) : (
                <Moon size={17} />
              )}
            </button>

            <Link to="/app" className="login-link">
              Log in
            </Link>

            <Link to="/app" className="nav-cta">
              Get Started
              <ArrowRight size={15} />
            </Link>
          </div>
        </div>
      </header>

      {/* ================= HERO ================= */}

      <main>
        <section className="hero-section" id="product">
          <div className="hero-container">

            {/* LEFT */}

            <div className="hero-copy">
              <motion.div
                className="hero-badge"
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                <span className="badge-dot"></span>
                AI-POWERED MACHINE LEARNING PLATFORM
              </motion.div>

              <motion.h1
                initial={{ opacity: 0, y: 25 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{
                  duration: 0.7,
                  delay: 0.1,
                }}
              >
                Transform Data
                <br />
                into{" "}
                <span className="gradient-text">
                  Intelligence
                </span>
              </motion.h1>

              <motion.p
                className="hero-description"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{
                  duration: 0.6,
                  delay: 0.25,
                }}
              >
                Cognify helps you upload, analyze, preprocess
                and train machine learning models with ease.
                Get accurate predictions and explainable insights
                — all in one platform.
              </motion.p>

              <motion.div
                className="hero-actions"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{
                  duration: 0.5,
                  delay: 0.35,
                }}
              >
                <Link to="/app" className="primary-cta">
                  Start Building
                  <ArrowRight size={17} />
                </Link>

                <button
                  className="secondary-cta"
                  onClick={scrollToWorkflow}
                >
                  Explore Workflow
                  <Play size={14} fill="currentColor" />
                </button>
              </motion.div>

              <motion.div
                className="hero-trust"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.55 }}
              >
                <span className="trust-label">
                  Trusted by data teams worldwide
                </span>

                <div className="trust-logos">
                  <span className="google-logo">Google</span>
                  <span className="microsoft-logo">
                    Microsoft
                  </span>
                  <span className="nvidia-logo">
                    NVIDIA
                  </span>
                  <span className="aws-logo">aws</span>
                  <span className="ibm-logo">IBM</span>
                </div>
              </motion.div>
            </div>

            
            {/* RIGHT WORKFLOW VIDEO */}
          <div className="hero-visual">
            <div className="workflow-video-glow"></div>

            <video
              className="workflow-video"
              autoPlay
              loop
              muted
              playsInline
              preload="auto"
              aria-label="Cognify machine learning workflow animation"
            >
             <source
              src="/assets/cognify_workflow.mp4"
              type="video/mp4"
            />
            Your browser does not support the video element.
          </video>
        </div>
      </div>
    </section>

        {/* ================= WORKFLOW SECTION ================= */}

        <section
          className="workflow-section"
          id="workflow"
        >
          <div className="section-container">

            <div className="section-heading">
              <span className="section-eyebrow">
                THE COGNIFY WORKFLOW
              </span>

              <h2>
                From raw data to
                <span> intelligent decisions.</span>
              </h2>

              <p>
                Every stage of your machine learning journey,
                connected in one transparent workflow.
              </p>
            </div>

            <div className="workflow-timeline">
              {workflowSteps.map((step, index) => {
                const Icon = step.icon;

                return (
                  <motion.div
                    className="timeline-step"
                    key={step.id}
                    initial={{
                      opacity: 0,
                      y: 20,
                    }}
                    whileInView={{
                      opacity: 1,
                      y: 0,
                    }}
                    viewport={{
                      once: true,
                      amount: 0.2,
                    }}
                    transition={{
                      delay: index * 0.08,
                    }}
                  >
                    <div className="timeline-icon">
                      <Icon size={20} />
                    </div>

                    <span className="timeline-number">
                      0{step.id}
                    </span>

                    <h3>{step.title}</h3>

                    <p>{step.description}</p>

                    {index !== workflowSteps.length - 1 && (
                      <div className="timeline-arrow">
                        <ArrowRight size={16} />
                      </div>
                    )}
                  </motion.div>
                );
              })}
            </div>
          </div>
        </section>

        {/* ================= FEATURES ================= */}

        <section
          className="features-section"
          id="features"
        >
          <div className="section-container">

            <div className="section-heading">
              <span className="section-eyebrow">
                ONE PLATFORM
              </span>

              <h2>
                Everything you need to
                <span> build intelligent models.</span>
              </h2>

              <p>
                Cognify brings the complete machine learning
                lifecycle into one intuitive workspace.
              </p>
            </div>

            <div className="feature-grid">

              <FeatureCard
                icon={<Database size={22} />}
                title="Smart Data Upload"
                text="Upload CSV, Excel or JSON datasets with automatic validation and schema detection."
              />

              <FeatureCard
                icon={<BarChart3 size={22} />}
                title="Automated Analysis"
                text="Instantly discover missing values, duplicates, outliers, distributions and correlations."
              />

              <FeatureCard
                icon={<SlidersHorizontal size={22} />}
                title="Data Preprocessing"
                text="Clean, encode, scale and transform your dataset through an intuitive pipeline."
              />

              <FeatureCard
                icon={<BrainCircuit size={22} />}
                title="Model Training"
                text="Train multiple machine learning algorithms and monitor their performance."
              />

              <FeatureCard
                icon={<GitCompareArrows size={22} />}
                title="Model Comparison"
                text="Compare accuracy, precision, recall, F1-score and other evaluation metrics."
              />

              <FeatureCard
                icon={<Lightbulb size={22} />}
                title="Explainable AI"
                text="Understand why your model made a prediction using transparent AI insights."
              />

            </div>
          </div>
        </section>

        {/* ================= CTA ================= */}

        <section className="final-cta" id="solutions">
          <div className="cta-card">

            <div className="cta-decoration"></div>

            <div className="cta-content">
              <span className="section-eyebrow">
                BUILD WITH COGNIFY
              </span>

              <h2>
                Turn your data into
                <span> intelligence.</span>
              </h2>

              <p>
                Explore the complete machine learning workflow
                without the complexity.
              </p>

              <Link to="/app" className="primary-cta">
                Start Building
                <ArrowRight size={17} />
              </Link>
            </div>
          </div>
        </section>
      </main>

      {/* ================= FOOTER ================= */}

      <footer className="landing-footer">
        <div className="footer-inner">
          <div className="footer-brand">
            <div className="brand-mark small">
              <span></span>
              <span></span>
              <span></span>
            </div>

            <strong>Cognify</strong>
          </div>

          <p>
            Transform Data into Intelligence.
          </p>

          <span>
            © 2026 Cognify. All rights reserved.
          </span>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({ icon, title, text }) {
  return (
    <motion.div
      className="feature-card"
      whileHover={{
        y: -5,
      }}
      transition={{
        duration: 0.2,
      }}
    >
      <div className="feature-icon">
        {icon}
      </div>

      <div>
        <h3>{title}</h3>
        <p>{text}</p>
      </div>

      <div className="feature-arrow">
        <ArrowRight size={17} />
      </div>
    </motion.div>
  );
}