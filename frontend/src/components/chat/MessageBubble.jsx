import React from "react";
import ReactMarkdown from "react-markdown";
import SourceChip from "./SourceChip";

const MessageBubble = ({ message }) => {
  return (
    <div className="flex flex-col space-y-3">
      <ReactMarkdown>{message.answer}</ReactMarkdown>
      {message.sources && message.sources.length > 0 && (
        <div className="flex flex-wrap gap-2 mt-2 pt-2 border-t border-gray-100">
          {message.sources.map((src, i) => (
            <SourceChip key={i} source={src} />
          ))}
        </div>
      )}
    </div>
  );
};

export default MessageBubble;
