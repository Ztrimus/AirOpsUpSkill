// src/InteractiveList.js

import React, { useState } from "react";
import {
  FaChevronDown,
  FaChevronRight,
  FaCheckCircle,
  FaCircle,
} from "react-icons/fa";

/**
 * InteractiveList Component
 * Renders a hierarchical interactive list with enhanced UI features.
 */
function InteractiveList({ treeData, onSelectNode }) {
  const [expandedNodes, setExpandedNodes] = useState(new Set()); // Track expanded nodes
  const [selectedNode, setSelectedNode] = useState(null); // Track selected node
  const [completedNodes, setCompletedNodes] = useState({}); // Track completed nodes

  const toggleNode = (nodeName) => {
    setExpandedNodes((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(nodeName)) {
        newSet.delete(nodeName);
      } else {
        newSet.add(nodeName);
      }
      return newSet;
    });
  };

  const handleNodeClick = (node) => {
    setSelectedNode(node.name); // Update selected node
    onSelectNode(node.name); // Notify parent
    toggleNode(node.name); // Toggle expanded state
  };

  const handleCompletionToggle = (nodeName) => {
    setCompletedNodes((prev) => ({
      ...prev,
      [nodeName]: !prev[nodeName],
    }));
  };

  const renderList = (node) => {
    const isIDListValid = node.attributes && Array.isArray(node.attributes.IDList);

    return (
      <li key={node.name} className="mb-4">
        <div
          className={`flex items-center justify-between p-4 rounded-lg shadow-md cursor-pointer transform transition duration-200 hover:scale-105
            ${
              selectedNode === node.name
                ? "bg-blue-500 text-white"
                : "bg-white border border-gray-300 text-gray-700 hover:bg-gray-100"
            }`}
          onClick={() => handleNodeClick(node)}
          aria-label={`Task ${node.name}`}
          role="button"
          tabIndex={0}
          onKeyPress={(e) => {
            if (e.key === "Enter") {
              handleNodeClick(node);
            }
          }}
        >
          <div className="flex items-center">
            {/* Expand/Collapse Icon */}
            {node.children && node.children.length > 0 && (
              <span className="mr-3 text-gray-500">
                {expandedNodes.has(node.name) ? <FaChevronDown /> : <FaChevronRight />}
              </span>
            )}

            {/* Task Name */}
            <span
              className={`font-medium ${
                completedNodes[node.name] ? "line-through text-gray-400" : ""
              }`}
            >
              {node.name}
            </span>
          </div>

          {/* Completion Toggle */}
          <span
            className="text-green-500 cursor-pointer"
            onClick={(e) => {
              e.stopPropagation(); // Prevent triggering the parent click
              handleCompletionToggle(node.name);
            }}
            aria-label={completedNodes[node.name] ? "Mark as incomplete" : "Mark as complete"}
            role="button"
            tabIndex={0}
            onKeyPress={(e) => {
              if (e.key === "Enter") {
                handleCompletionToggle(node.name);
              }
            }}
          >
            {completedNodes[node.name] ? <FaCheckCircle /> : <FaCircle />}
          </span>
        </div>

        {/* Additional Task Details */}
        <div className="ml-6 mt-2 text-sm text-gray-500">
          <p>
            <strong>Tree Level:</strong> {node.attributes?.TreeLevel ?? "N/A"}
          </p>
          <p>
            <strong>IDList:</strong>{" "}
            {isIDListValid ? node.attributes.IDList.join(", ") : "N/A"}
          </p>
        </div>

        {/* Nested Children */}
        {expandedNodes.has(node.name) && node.children && node.children.length > 0 && (
          <ul className="ml-6 mt-2 border-l-2 border-gray-300 pl-4">
            {node.children.map((child) => renderList(child))}
          </ul>
        )}
      </li>
    );
  };

  const isValidTreeData = (data) => {
    if (!data || typeof data !== "object") return false;
    if (!data.name || typeof data.name !== "string") return false;
    if (!data.attributes || typeof data.attributes !== "object") return false;
    if (!Array.isArray(data.attributes.IDList)) return false;
    if (!("TreeLevel" in data.attributes)) return false;
    if (data.children && !Array.isArray(data.children)) return false;
    return true;
  };

  if (!isValidTreeData(treeData)) {
    console.error("Invalid treeData provided to InteractiveList:", treeData);
    return <div className="text-red-500">Invalid task data.</div>;
  }

  return (
    <div className="max-w-2xl mx-auto p-6 bg-gradient-to-r from-green-50 to-blue-50 dark:from-gray-800 dark:to-gray-900 rounded-xl shadow-lg">

      <ul className="list-none">{renderList(treeData)}</ul>
    </div>
  );
}

export default InteractiveList;
