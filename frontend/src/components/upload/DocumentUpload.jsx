import React from "react";
import { useDropzone } from "react-dropzone";
import useDocumentUpload from "../../hooks/useDocumentUpload";
import { UploadCloud, CheckCircle, XCircle, Loader2 } from "lucide-react";
import { ALLOWED_FILE_TYPES } from "../../constants/APP_CONFIG";

const DocumentUpload = () => {
  const { uploadProgress, uploadStatus, handleUploadFile, resetUpload } = useDocumentUpload();

  const onDrop = (acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      handleUploadFile(acceptedFiles[0]);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: ALLOWED_FILE_TYPES.reduce((acc, type) => ({ ...acc, [type]: [] }), {}),
    maxFiles: 1,
    multiple: false,
  });

  return (
    <div>
      <h3 className="text-sm font-semibold text-gray-700 mb-3">Upload Context</h3>
      
      {!uploadStatus && (
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-colors ${
            isDragActive ? "border-blue-500 bg-blue-50" : "border-gray-300 hover:border-blue-400 hover:bg-gray-50"
          }`}
        >
          <input {...getInputProps()} />
          <UploadCloud className="w-8 h-8 text-gray-400 mx-auto mb-2" />
          <p className="text-sm text-gray-600 font-medium">Drag & drop a file here</p>
          <p className="text-xs text-gray-400 mt-1">PDF, TXT, DOCX up to 10MB</p>
        </div>
      )}

      {uploadStatus === "uploading" && (
        <div className="bg-gray-50 p-4 rounded-xl border border-gray-200 text-center">
          <p className="text-sm font-medium text-gray-700 mb-2">Uploading to S3...</p>
          <div className="w-full bg-gray-200 rounded-full h-2 mb-1">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${uploadProgress}%` }}
            ></div>
          </div>
          <p className="text-xs text-gray-500">{uploadProgress}%</p>
        </div>
      )}

      {uploadStatus === "processing" && (
        <div className="bg-blue-50 p-4 rounded-xl border border-blue-100 flex items-center justify-between">
          <div className="flex items-center text-blue-700 text-sm font-medium">
            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
            Processing in Lambda...
          </div>
        </div>
      )}

      {uploadStatus === "error" && (
        <div className="bg-red-50 p-4 rounded-xl border border-red-100 flex justify-between items-center text-red-700 text-sm">
          <div className="flex items-center font-medium">
            <XCircle className="w-4 h-4 mr-2" />
            Upload failed
          </div>
          <button onClick={resetUpload} className="text-xs underline">Retry</button>
        </div>
      )}
    </div>
  );
};

export default DocumentUpload;
