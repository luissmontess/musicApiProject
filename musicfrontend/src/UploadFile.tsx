import React, { useState } from "react";
import axios from "axios";

const UploadFile: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string>("");

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setFile(event.target.files[0]);
    }
  };

  const handleFileUpload = async () => {
    if (!file) {
      setUploadStatus("No file selected.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://127.0.0.1:8000/effect/reverb_effect", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        responseType: "blob",
      });

      const blob = new Blob([response.data], { type: "audio/wav" });
      const downloadUrl = window.URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = downloadUrl;
      link.download = "processed-output.wav"; // File name for download
      document.body.appendChild(link);
      link.click();
      link.remove();

      setUploadStatus(`File uploaded successfully: ${response.data.message}`);
    } catch (error) {
      setUploadStatus("Error uploading file.");
    }
  };

  return (
    <div className="upload-container">
      <h1>Upload a .wav File</h1>
      <input
        type="file"
        accept=".wav"
        onChange={handleFileChange}
      />
      <button
        onClick={handleFileUpload}
        disabled={!file}
      >
        Upload File
      </button>
      {uploadStatus && <p>{uploadStatus}</p>}
    </div>
  );
};

export default UploadFile;
