import React, { useEffect, useState } from "react";
import Tree from "react-d3-tree";
import { transformJsonToFlatTree } from "../utils/transformJson";

function GraphView({ rawData, onSelectTask }) {
  const [treeData, setTreeData] = useState(null);

  useEffect(() => {
    if (rawData) {
      const transformedData = transformJsonToFlatTree(rawData);
      console.log("Transformed Flat Tree Data:", transformedData);
      setTreeData(transformedData);
    }
  }, [rawData]);

  const handleNodeClick = (node) => {
    console.log("Node clicked:", node);
    onSelectTask(node.data.attributes);
  };

  if (!treeData) {
    return <p className="text-center">Loading graph...</p>;
  }

  return (
    <div className="h-[600px] w-full bg-white border rounded shadow">
      <Tree
        data={{ name: "Root", children: treeData }} // Wrap flat tree with a root
        orientation="vertical"
        onNodeClick={handleNodeClick}
        translate={{ x: 300, y: 50 }}
      />
    </div>
  );
}

export default GraphView;
