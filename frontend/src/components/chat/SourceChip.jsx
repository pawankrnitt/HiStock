import React from "react";
import { FileText } from "lucide-react";

const SourceChip = ({ source }) => {
  return (
    <div className="inline-flex items-center px-2 py-1 bg-blue-50 border border-blue-100 rounded text-xs text-blue-700 font-medium">
      <FileText className="w-3 h-3 mr-1" />
      <span>{source.docName || source.id || "Document"}</span>
      {source.page && <span className="ml-1 text-blue-500">p.{source.page}</span>}
    </div>
  );
};

export default SourceChip;
