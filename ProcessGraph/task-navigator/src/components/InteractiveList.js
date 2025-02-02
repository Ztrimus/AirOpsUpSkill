import React from "react";

function InteractiveList({ treeData, onSelectNode }) {
  const renderList = (node) => (
    <li key={node.name} className="mb-2">
      <div
        className="p-2 border border-gray-300 rounded-lg hover:bg-gray-100 cursor-pointer"
        onClick={() => onSelectNode(node.name)} // Notify parent of selection
      >
        <span className="font-semibold">{node.name}</span>
      </div>
      {node.children && (
        <ul className="ml-4 mt-2">
          {node.children.map((child) => renderList(child))}
        </ul>
      )}
    </li>
  );

  return (
    <div>
      <ul className="list-none">{renderList(treeData)}</ul>
    </div>
  );
}

export default InteractiveList;
