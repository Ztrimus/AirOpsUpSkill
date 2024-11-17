import React, { useState } from "react";

function TaskListView({ hierarchy }) {
  const renderTaskList = (taskList) => {
    return taskList.map((task) => <TaskItem key={task.id} task={task} />);
  };

  return (
    <div className="bg-white rounded shadow p-4">
      <h2 className="text-xl font-bold mb-4">To-Do Task List</h2>
      {renderTaskList([hierarchy])}
    </div>
  );
}

function TaskItem({ task }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);

  const handleToggle = () => setIsExpanded(!isExpanded);

  return (
    <div className="ml-4 mb-2">
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
          onClick={handleToggle}
        >
          {task.name}
        </span>
        {task.children.length > 0 && (
          <button
            className="ml-auto text-blue-500 hover:underline"
            onClick={handleToggle}
          >
            {isExpanded ? "Collapse" : "Expand"}
          </button>
        )}
      </div>

      <div className="ml-4 text-sm text-gray-600">
        <p><strong>Tree Level:</strong> {task.attributes.TreeLevel}</p>
        <p><strong>IDList:</strong> {task.attributes.IDList.join(", ")}</p>
      </div>

      {isExpanded && (
        <div className="ml-4 border-l border-gray-300 pl-4">
          {task.children.map((child) => (
            <TaskItem key={child.id} task={child} />
          ))}
        </div>
      )}
    </div>
  );
}

export default TaskListView;
