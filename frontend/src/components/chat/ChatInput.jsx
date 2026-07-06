import React from "react";
import useChat from "../../hooks/useChat";
import { Send } from "lucide-react";

const ChatInput = () => {
  const { inputValue, handleInputChange, handleSendMessage, isStreaming } = useChat();

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="p-4 bg-white border-t border-gray-200">
      <div className="relative flex items-end">
        <textarea
          value={inputValue}
          onChange={(e) => handleInputChange(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about NVDA or TSLA..."
          className="w-full bg-gray-50 border border-gray-300 rounded-2xl py-3 pl-4 pr-12 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none min-h-[50px] max-h-[150px]"
          rows={1}
        />
        <button
          onClick={handleSendMessage}
          disabled={!inputValue.trim() || isStreaming}
          className="absolute right-2 bottom-2 p-2 rounded-full bg-blue-600 text-white hover:bg-blue-700 disabled:bg-gray-300 disabled:text-gray-500 transition-colors"
        >
          <Send className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};

export default ChatInput;
