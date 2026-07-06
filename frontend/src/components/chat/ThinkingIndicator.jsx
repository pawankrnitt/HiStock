import React from "react";
import { useChatStore } from "../../store/chatStore";
import { Bot } from "lucide-react";

const ThinkingIndicator = () => {
  const { thinkingStep } = useChatStore();

  if (!thinkingStep) return null;

  return (
    <div className="flex items-center space-x-3 p-4 text-sm text-gray-500 bg-gray-50 border-t border-gray-100">
      <Bot className="w-5 h-5 text-blue-500 animate-pulse" />
      <span className="font-medium animate-pulse">{thinkingStep}</span>
      <span className="flex space-x-1">
        <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
        <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
        <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
      </span>
    </div>
  );
};

export default ThinkingIndicator;
