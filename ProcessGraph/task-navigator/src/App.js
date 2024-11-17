import React, { useState } from "react";
import FileUploader from "./components/FileUploader";
import TreeView from "./components/TreeView";
import InteractiveList from "./components/InteractiveList";
import { transformJsonToTree } from "./utils/transformJson";
import { cleanJsonSteps } from "./utils/cleanJson";

function App() {
  const [treeData, setTreeData] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null); // Centralized state for selected node

  const handleFileUpload = (data) => {
    const cleanedData = cleanJsonSteps(data); // Clean the JSON
    const transformedTree = transformJsonToTree(cleanedData, "root_uuid");
    setTreeData(transformedTree);
  };

  const handleNodeSelection = (nodeName) => {
    setSelectedNode(nodeName); // Update selected node state
  };

  return (
    <div className="min-h-screen bg-gray-100 text-gray-800">
      <header className="p-4 bg-blue-600 text-white flex justify-between items-center">
        <h1 className="text-2xl font-bold">To-Do Tree</h1>
        <FileUploader onUpload={handleFileUpload} />
      </header>

      <main className="flex h-screen p-4">
        {/* Left Panel: Tree Graph */}
        <div className="w-1/2 pr-2">
          <div className="bg-white shadow-lg rounded-lg h-full overflow-hidden">
            <div className="p-4 bg-gray-200 border-b border-gray-300">
              <h2 className="text-lg font-semibold">Tree Graph</h2>
            </div>
            <div className="h-full overflow-y-auto p-4">
              {treeData ? (
                <TreeView
                  treeData={treeData}
                  selectedNode={selectedNode} // Pass selected node
                  onNodeClick={handleNodeSelection} // Handle node clicks
                />
              ) : (
                <p className="text-center text-gray-500">Upload a JSON file to get started.</p>
              )}
            </div>
          </div>
        </div>

        {/* Right Panel: Interactive List */}
        <div className="w-1/2 pl-2">
          <div className="bg-white shadow-lg rounded-lg h-full overflow-hidden">
            <div className="p-4 bg-gray-200 border-b border-gray-300">
              <h2 className="text-lg font-semibold">Interactive List</h2>
            </div>
            <div className="h-full overflow-y-auto p-4">
              {treeData ? (
                <InteractiveList
                  treeData={treeData}
                  onSelectNode={handleNodeSelection} // Handle list selection
                />
              ) : (
                <p className="text-center text-gray-500">The list will appear here.</p>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
