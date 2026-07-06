// hooks/useDocumentUpload.js
import { useState, useCallback } from "react";
import { getPresignUrl, uploadToS3 } from "../services/documentService";
import toast from "react-hot-toast";

const useDocumentUpload = () => {
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadStatus, setUploadStatus]     = useState(null);  // null | "uploading" | "processing" | "error"

  const handleUploadFile = useCallback(async (file) => {
    setUploadStatus("uploading");
    setUploadProgress(0);

    try {
      // Step 1: Get pre-signed URL from backend
      const { presignUrl } = await getPresignUrl(file.name, file.type);

      // Step 2: Upload directly to S3 (never touches backend server)
      await uploadToS3(presignUrl, file, setUploadProgress);

      // Step 3: Wait for "document_processed" socket event (handled in useSocket.js)
      // Status will be updated to "ready" when the backend Lambda completes (Phase 6)
      setUploadStatus("processing");
      toast.success("Upload complete — processing your document...");

    } catch (error) {
      setUploadStatus("error");
      toast.error("Upload failed. Please try again.");
      console.error("[upload error]", error);
    }
  }, []);

  const resetUpload = useCallback(() => {
    setUploadProgress(0);
    setUploadStatus(null);
  }, []);

  return { uploadProgress, uploadStatus, handleUploadFile, resetUpload };
};

export default useDocumentUpload;
