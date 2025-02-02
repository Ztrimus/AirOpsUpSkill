import React, { useState } from "react";

function TaskListView({ hierarchy }) {
  const renderTaskTree = (task) => {
    const [isExpanded, setIsExpanded] = useState(false);
    const [isCompleted, setIsCompleted] = useState(false);

    return (
      <div className="ml-4 mb-2" key={task.id}>
        <div className="flex items-center">
          <input
            type="checkbox"
            className="mr-2"
            checked={isCompleted}
            onChange={() => setIsCompleted(!isCompleted)}
          />
          <span
            className={`font-semibold cursor-pointer ${
              isCompleted ? "line-through text-gray-500" : ""
            }`}
            onClick={() => setIsExpanded(!isExpanded)}
          >
            {task.name}
          </span>
          {task.children.length > 0 && (
            <button
              className="ml-auto text-blue-500 hover:underline"
              onClick={() => setIsExpanded(!isExpanded)}
            >
              {isExpanded ? "Collapse" : "Expand"}
            </button>
          )}
        </div>

        <div className="ml-4 text-sm text-gray-600">
          <p><strong>Tree Level:</strong> {task.attributes.TreeLevel}</p>
          <p><strong>IDList:</strong> {task.attributes.IDList.join(", ")}</p>
        </div>

        {isExpanded && task.children.length > 0 && (
          <div className="ml-4 border-l border-gray-300 pl-4">
            {task.children.map((child) => renderTaskTree(child))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="bg-white rounded shadow p-4">
      <h2 className="text-xl font-bold mb-4">To-Do Tree List</h2>
      {renderTaskTree(hierarchy)}
    </div>
  );
}

export default TaskListView;
