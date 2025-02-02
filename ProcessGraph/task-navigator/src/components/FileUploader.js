import React from "react";

function FileUploader({ onUpload }) {
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        try {
          const jsonData = JSON.parse(event.target.result);
          console.log("Parsed JSON:", jsonData); // Log the parsed JSON
          onUpload(jsonData); // Pass the JSON data to the parent component
        } catch (error) {
          alert("Invalid JSON file.");
        }
      };
      reader.readAsText(file);
    }
  };

  return (
    <label className="cursor-pointer bg-blue-500 text-white px-4 py-2 rounded">
      Upload JSON
      <input
        type="file"
        accept=".json"
        onChange={handleFileChange}
        className="hidden"
      />
    </label>
  );
}

export default FileUploader;
