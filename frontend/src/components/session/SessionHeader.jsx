import React from "react";
import { Users, Share2, FileDown } from "lucide-react";
import { triggerReport } from "../../services/reportService";
import toast from "react-hot-toast";

const SessionHeader = ({ session }) => {
  const handleShare = () => {
    const url = `${window.location.origin}/session/${session.sessionId}`;
    navigator.clipboard.writeText(url);
    toast.success("Session link copied to clipboard!");
  };

  const handleReport = async () => {
    try {
      const res = await triggerReport(session.sessionId);
      toast.success(res.message);
    } catch {
      toast.error("Failed to trigger report.");
    }
  };

  return (
    <div className="flex justify-between items-center p-4 bg-white border-b border-gray-200">
      <div>
        <h2 className="text-lg font-semibold text-gray-900">{session.name}</h2>
        <div className="flex items-center text-xs text-gray-500 mt-1 space-x-3">
          <span className="flex items-center">
            <Users className="w-3 h-3 mr-1" />
            {session.members?.length || 1} members
          </span>
          <span className="text-gray-300">•</span>
          <span>ID: {session.sessionId.split("_")[1]}</span>
        </div>
      </div>
      <div className="flex space-x-2">
        <button
          onClick={handleShare}
          className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors tooltip-trigger"
          title="Share Session"
        >
          <Share2 className="w-5 h-5" />
        </button>
        <button
          onClick={handleReport}
          className="flex items-center px-3 py-2 bg-blue-50 text-blue-700 hover:bg-blue-100 rounded-lg text-sm font-medium transition-colors"
        >
          <FileDown className="w-4 h-4 mr-2" />
          Report
        </button>
      </div>
    </div>
  );
};

export default SessionHeader;
