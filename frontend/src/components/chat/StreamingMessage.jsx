import React from "react";
import ReactMarkdown from "react-markdown";

const StreamingMessage = ({ text }) => {
  return (
    <div className="relative">
      <ReactMarkdown>{text}</ReactMarkdown>
      <span className="inline-block w-2 h-4 bg-blue-500 animate-pulse ml-1 align-middle" />
    </div>
  );
};

export default StreamingMessage;
