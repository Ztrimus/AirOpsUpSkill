import React from "react";
import Tree from "react-d3-tree";

function TreeView({ treeData, selectedNode, onNodeClick }) {
  const renderCustomNode = ({ nodeDatum, toggleNode }) => {
    const isSelected = selectedNode === nodeDatum.name;

    return (
      <g>
        {/* Node Circle */}
        <circle
          r={20}
          fill={isSelected ? "orange" : "url(#gradient)"}
          stroke={isSelected ? "gold" : "black"}
          strokeWidth={isSelected ? 4 : 2}
          onClick={() => {
            toggleNode();
            onNodeClick(nodeDatum.name); // Notify parent of node click
          }}
        />
        <defs>
          <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style={{ stopColor: "blue", stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: "cyan", stopOpacity: 1 }} />
          </linearGradient>
        </defs>
        {/* Node Label */}
        <text
          fill="black"
          fontSize="12px"
          textAnchor="middle"
          y="-30"
          style={{ pointerEvents: "none" }}
        >
          {nodeDatum.name}
        </text>
      </g>
    );
  };

  return (
    <div id="treeWrapper" style={{ width: "100%", height: "100%" }}>
      <Tree
        data={treeData}
        orientation="vertical"
        pathFunc="elbow"
        renderCustomNodeElement={renderCustomNode}
      />
    </div>
  );
}

export default TreeView;
