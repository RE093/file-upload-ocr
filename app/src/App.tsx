import { useState } from "react";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";

import "./App.css";
import "react-toastify/dist/ReactToastify.css";

function App() {
  const [error, setError] = useState<string | null>(null);
  const [files, setFiles] = useState<File | null>(null);
  const [uploadingFiles, setUploadingFiles] = useState<any[]>([]);
  const [uploadedFiles, setUploadedFiles] = useState<any[]>([]);

  function handleFileChange(event: any) {
    setError(null);
    event.preventDefault();
    const files = event.target.files;
    console.log(files);
    console.log(event);
    if (!files) {
      setError("Please select a file");
      return;
    }
    setFiles(files);
  }

  async function handleFileUpload(event: any) {
    event.preventDefault();
    if (!files) {
      setError("Please select a file");
      return;
    }

    const { data } = await axios.post(
      "http://localhost:8000/upload",
      {
        files: files,
      },
      {
        headers: {
          "Content-Type": "multipart/form-data",
          Accept: "application/json",
        },
      }
    );

    console.log(data);

    const { files: uploading_files } = data;
    setUploadingFiles(uploading_files);
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>File Upload OCR</h1>
      </header>
      <main>
        {uploadingFiles?.length ? (
          uploadingFiles.map((file) => {
            return (
              <div className="uploading-file__item" key={file.uploadId}>
                <p>{file.title}</p>
                <div className="uploading-file__item--right">
                  <p>{file.status}</p>
                  <img src={file.file} alt={file.title} />
                </div>
              </div>
            );
          })
        ) : (
          <form onSubmit={handleFileUpload}>
            <input onChange={handleFileChange} type="file" multiple />
            <button type="submit">Upload</button>
          </form>
        )}
        <p>{error}</p>
        <h2>Uploaded Files:</h2>
        {uploadedFiles?.length
          ? uploadedFiles.map((file) => {
              return (
                <div className="uploaded-file__item" key={file.uploadId}>
                  <p>{file.originalName}</p>
                  <img src={file.file} alt={file.originalName} />
                </div>
              );
            })
          : null}
      </main>
      <ToastContainer />
    </div>
  );
}

export default App;
