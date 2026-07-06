import React from "react";
import { usePresenceStore } from "../../store/presenceStore";

const TypingIndicator = () => {
  const { typingUsers } = usePresenceStore();

  if (typingUsers.length === 0) return null;

  const text = typingUsers.length === 1
    ? `${typingUsers[0].name} is typing...`
    : `${typingUsers.length} people are typing...`;

  return (
    <div className="px-4 py-2 text-xs text-gray-500 italic bg-white border-t border-gray-100">
      {text}
    </div>
  );
};

export default TypingIndicator;
