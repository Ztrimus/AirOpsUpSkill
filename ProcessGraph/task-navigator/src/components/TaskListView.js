import React, { useState } from "react";
import { FaChevronDown, FaChevronRight, FaCheckCircle, FaCircle } from "react-icons/fa";

/**
 * TaskListView Component
 * Renders a hierarchical task list with enhanced UI features.
 */
function TaskListView({ hierarchy }) {
  const renderTaskList = (taskList) => {
    return taskList.map((task) => <TaskItem key={task.id} task={task} />);
  };

  return (
    <div className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded shadow p-6">
      <h2 className="text-2xl font-bold mb-6 text-white">To-Do Task List</h2>
      {renderTaskList([hierarchy])}
    </div>
  );
}

/**
 * TaskItem Component
 * Represents an individual task with interactive features.
 */
function TaskItem({ task }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);

  const handleToggle = () => setIsExpanded(!isExpanded);
  const handleCompletionToggle = () => setIsCompleted(!isCompleted);

  return (
    <div className="ml-6 mb-4">
      <div
        className={`flex items-center p-2 rounded-md transition transform hover:scale-105 ${
          isCompleted ? "bg-green-100" : "bg-white"
        } shadow-sm`}
      >
        <button
          onClick={handleCompletionToggle}
          className="text-green-500 focus:outline-none"
          aria-label={isCompleted ? "Mark as incomplete" : "Mark as complete"}
        >
          {isCompleted ? <FaCheckCircle size={20} /> : <FaCircle size={20} />}
        </button>
        <span
          className={`ml-3 flex-1 font-semibold cursor-pointer ${
            isCompleted ? "line-through text-gray-500" : "text-gray-800"
          } transition-colors duration-200`}
          onClick={handleToggle}
        >
          {task.name}
        </span>
        {task.children && task.children.length > 0 && (
          <button
            className="text-indigo-500 hover:text-indigo-700 focus:outline-none"
            onClick={handleToggle}
            aria-label={isExpanded ? "Collapse task" : "Expand task"}
          >
            {isExpanded ? <FaChevronDown size={16} /> : <FaChevronRight size={16} />}
          </button>
        )}
      </div>

      <div className="ml-8 mt-2 text-sm text-gray-600">
        <p><strong>Tree Level:</strong> {task.attributes.TreeLevel}</p>
        <p><strong>IDList:</strong> {task.attributes.IDList.join(", ")}</p>
      </div>

      {isExpanded && task.children && task.children.length > 0 && (
        <div className="ml-8 border-l border-gray-300 pl-4 mt-2">
          {task.children.map((child) => (
            <TaskItem key={child.id} task={child} />
          ))}
        </div>
      )}
    </div>
  );
}

export default TaskListView;
