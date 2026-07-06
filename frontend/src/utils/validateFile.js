// utils/validateFile.js
import { MAX_FILE_SIZE_BYTES, ALLOWED_FILE_TYPES } from "../constants/APP_CONFIG";

export const validateFile = (file) => {
  if (!ALLOWED_FILE_TYPES.includes(file.type)) {
    return { valid: false, error: "Unsupported file type. Only PDF, TXT, and DOCX are allowed." };
  }
  if (file.size > MAX_FILE_SIZE_BYTES) {
    return { valid: false, error: "File exceeds 10MB limit." };
  }
  return { valid: true };
};
