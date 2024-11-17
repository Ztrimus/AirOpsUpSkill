import React, { useState } from "react";
import { FaUpload, FaSpinner, FaCheckCircle, FaExclamationCircle } from "react-icons/fa";

function FileUploader({ onUpload }) {
  const [uploadStatus, setUploadStatus] = useState(null); // Tracks upload status (loading, success, error)
  const [fileName, setFileName] = useState(""); // Tracks the uploaded file name

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      setUploadStatus("loading"); // Show loading indicator
      setFileName(file.name); // Set file name for display

      reader.onload = (event) => {
        try {
          const jsonData = JSON.parse(event.target.result);
          console.log("Parsed JSON:", jsonData); // Log the parsed JSON
          onUpload(jsonData); // Pass the JSON data to the parent component
          setUploadStatus("success"); // Set success status
        } catch (error) {
          setUploadStatus("error"); // Set error status
          alert("Invalid JSON file. Please upload a valid JSON.");
        }
      };

      reader.readAsText(file);
    }
  };

  return (
    <div className="flex flex-col items-center space-y-4">
      {/* File Upload Button */}
      <label className="relative cursor-pointer bg-blue-600 text-white px-4 py-2 rounded-lg shadow hover:bg-blue-700 focus:outline-none focus:ring focus:ring-blue-300 transition">
        <div className="flex items-center space-x-2">
          <FaUpload />
          <span>{uploadStatus === "loading" ? "Uploading..." : "Upload JSON"}</span>
        </div>
        <input
          type="file"
          accept=".json"
          onChange={handleFileChange}
          className="hidden"
        />
      </label>

      {/* Status and Feedback */}
      {uploadStatus && (
        <div
          className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm ${
            uploadStatus === "success"
              ? "bg-green-100 text-green-700"
              : uploadStatus === "error"
              ? "bg-red-100 text-red-700"
              : "bg-blue-100 text-blue-700"
          }`}
        >
          {uploadStatus === "loading" && <FaSpinner className="animate-spin" />}
          {uploadStatus === "success" && <FaCheckCircle />}
          {uploadStatus === "error" && <FaExclamationCircle />}
          <span>
            {uploadStatus === "success"
              ? `Successfully uploaded: ${fileName}`
              : uploadStatus === "error"
              ? "Failed to upload. Please try again."
              : ""}
          </span>
        </div>
      )}

      {/* File Name Display */}
      {fileName && uploadStatus !== "success" && (
        <p className="text-gray-600 text-sm italic">{fileName}</p>
      )}
    </div>
  );
}

export default FileUploader;
