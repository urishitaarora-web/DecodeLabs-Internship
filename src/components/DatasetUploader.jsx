import { useRef, useState } from "react";
import {
  UploadCloud,
  FileSpreadsheet,
  CheckCircle2,
  AlertCircle,
  X,
} from "lucide-react";

export default function DatasetUploader({ onDatasetLoaded }) {
  const inputRef = useRef(null);

  const [dragging, setDragging] = useState(false);
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");

  const supportedTypes = [
    "text/csv",
    "application/json",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  ];

  const processFile = (selectedFile) => {
    setError("");

    if (!selectedFile) return;

    const extension = selectedFile.name
      .split(".")
      .pop()
      .toLowerCase();

    const allowedExtensions = ["csv", "json", "xls", "xlsx"];

    if (!allowedExtensions.includes(extension)) {
      setError("Unsupported file type. Please upload CSV, Excel, or JSON.");
      return;
    }

    setFile(selectedFile);

    if (onDatasetLoaded) {
      onDatasetLoaded(selectedFile);
    }
  };

  const handleInputChange = (event) => {
    processFile(event.target.files?.[0]);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setDragging(false);

    const droppedFile = event.dataTransfer.files?.[0];

    processFile(droppedFile);
  };

  const removeFile = () => {
    setFile(null);
    setError("");

    if (inputRef.current) {
      inputRef.current.value = "";
    }

    if (onDatasetLoaded) {
      onDatasetLoaded(null);
    }
  };

  return (
    <div className="dataset-uploader">

      {!file ? (
        <>
          <div
            className={`upload-dropzone ${
              dragging ? "upload-dropzone-active" : ""
            }`}
            onDragOver={(event) => {
              event.preventDefault();
              setDragging(true);
            }}
            onDragLeave={() => setDragging(false)}
            onDrop={handleDrop}
            onClick={() => inputRef.current?.click()}
          >
            <input
              ref={inputRef}
              type="file"
              accept=".csv,.json,.xls,.xlsx"
              onChange={handleInputChange}
              hidden
            />

            <div className="upload-icon">
              <UploadCloud size={30} />
            </div>

            <h3>Upload your dataset</h3>

            <p>
              Drag & drop your file here or{" "}
              <span>browse from your computer</span>
            </p>

            <small>
              Supported formats: CSV, XLSX, XLS, JSON
            </small>
          </div>

          {error && (
            <div className="upload-error">
              <AlertCircle size={16} />
              {error}
            </div>
          )}
        </>
      ) : (
        <div className="uploaded-file-card">

          <div className="uploaded-file-icon">
            <FileSpreadsheet size={24} />
          </div>

          <div className="uploaded-file-info">
            <strong>{file.name}</strong>

            <span>
              {(file.size / (1024 * 1024)).toFixed(2)} MB
            </span>
          </div>

          <div className="upload-success">
            <CheckCircle2 size={18} />
            <span>File loaded</span>
          </div>

          <button
            className="remove-file-btn"
            onClick={removeFile}
            aria-label="Remove file"
          >
            <X size={17} />
          </button>

        </div>
      )}

    </div>
  );
}