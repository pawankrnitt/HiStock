import React, { useEffect, useRef } from "react";
import { useChatStore } from "../../store/chatStore";
import MessageBubble from "./MessageBubble";
import StreamingMessage from "./StreamingMessage";

const MessageList = () => {
  const { messages } = useChatStore();
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex flex-col p-4 space-y-6">
      {messages.map((msg) => (
        <div key={msg.messageId} className="flex flex-col space-y-2">
          {/* User Question */}
          <div className="self-end max-w-[80%]">
            <div className="bg-blue-600 text-white px-4 py-2 rounded-2xl rounded-br-sm text-sm shadow-sm">
              <p className="whitespace-pre-wrap">{msg.question}</p>
            </div>
            <span className="text-xs text-gray-400 mt-1 block text-right">
              {msg.askedBy}
            </span>
          </div>

          {/* AI Answer */}
          <div className="self-start max-w-[90%]">
            <div className="bg-white border border-gray-200 px-4 py-3 rounded-2xl rounded-bl-sm text-sm text-gray-800 shadow-sm prose prose-sm max-w-none">
              {msg.isStreaming ? (
                <StreamingMessage text={msg.answer} />
              ) : (
                <MessageBubble message={msg} />
              )}
            </div>
          </div>
        </div>
      ))}
      <div ref={bottomRef} />
    </div>
  );
};

export default MessageList;
