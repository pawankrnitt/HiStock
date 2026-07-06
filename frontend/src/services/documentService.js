// services/documentService.js
import axios from "axios";
import apiClient from "./apiClient";
import { API_ROUTES } from "../constants/API_ROUTES";

const getPresignUrl = async (fileName, contentType) => {
  const response = await apiClient.post(API_ROUTES.DOCUMENTS.PRESIGN, { fileName, contentType });
  return response.data;   // { presignUrl, docId, s3Key }
};

const uploadToS3 = async (presignUrl, file, onProgress) => {
  // Upload DIRECTLY to S3 — backend not involved in file bytes transfer
  await axios.put(presignUrl, file, {
    headers: { "Content-Type": file.type },
    onUploadProgress: (event) => {
      const percent = Math.round((event.loaded / event.total) * 100);
      onProgress(percent);
    },
  });
};

const getDocuments = async () => {
  const response = await apiClient.get(API_ROUTES.DOCUMENTS.BASE);
  return response.data;
};

const deleteDocument = async (docId) => {
  await apiClient.delete(API_ROUTES.DOCUMENTS.BY_ID(docId));
};

export { getPresignUrl, uploadToS3, getDocuments, deleteDocument };
