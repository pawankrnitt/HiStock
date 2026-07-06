import React from "react";
import { usePresenceStore } from "../../store/presenceStore";

const MemberList = () => {
  const { onlineMembers } = usePresenceStore();

  return (
    <div>
      <h3 className="text-sm font-semibold text-gray-700 mb-3">Online Members</h3>
      {onlineMembers.length === 0 ? (
        <p className="text-sm text-gray-500">Only you</p>
      ) : (
        <div className="flex flex-wrap gap-2">
          {onlineMembers.map((member) => (
            <div
              key={member.userId}
              className="relative w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 font-medium text-xs border border-blue-200"
              title={member.name}
            >
              {member.name.charAt(0).toUpperCase()}
              <span className="absolute bottom-0 right-0 w-2.5 h-2.5 bg-green-500 border-2 border-white rounded-full"></span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MemberList;
