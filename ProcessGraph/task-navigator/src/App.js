import React, { useState } from "react";
import FileUploader from "./components/FileUploader";
import TreeView from "./components/TreeView";
import InteractiveList from "./components/InteractiveList";
import { buildNestedTree } from "./utils/buildNestedTree";
import { cleanJsonSteps } from "./utils/cleanJson";

function App() {
  const [treeData, setTreeData] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileUpload = async (data) => {
    try {
      setLoading(true);
      const cleanedData = cleanJsonSteps(data); // Clean the JSON
      const transformedTree = buildNestedTree(cleanedData, "root_uuid"); // Transform the data into a tree
      setTreeData(transformedTree);
      setError(null);
    } catch (err) {
      setError("Failed to process the uploaded file. Please check the file format.");
    } finally {
      setLoading(false);
    }
  };

  const handleNodeSelection = (nodeName) => {
    setSelectedNode(nodeName); // Update selected node state
  };

  return (
    <div className="min-h-screen bg-gray-100 text-gray-800 flex flex-col items-center justify-center">
      {!treeData ? (
        <div className="p-6 bg-white rounded-lg shadow-lg max-w-lg w-full">
          <h1 className="text-2xl font-bold text-center mb-4 text-blue-600">Upload Your JSON File</h1>
          {error && <p className="text-red-500 text-center mb-4">{error}</p>}
          <FileUploader onUpload={handleFileUpload} />
          {loading && <p className="text-center text-blue-500 mt-4">Processing...</p>}
        </div>
      ) : (
        <main className="flex flex-col md:flex-row w-full h-screen p-4">
          {/* Left Panel: Tree Graph */}
          <div className="w-full md:w-1/2 pr-2 mb-4 md:mb-0">
            <div className="bg-white shadow-lg rounded-lg h-full overflow-hidden">
              <div className="p-4 bg-gray-200 border-b border-gray-300">
                <h2 className="text-lg font-semibold">Tree Graph</h2>
              </div>
              <div className="h-full overflow-y-auto p-4">
                <TreeView
                  treeData={treeData}
                  selectedNode={selectedNode}
                  onNodeClick={handleNodeSelection}
                />
              </div>
            </div>
          </div>

          {/* Right Panel: Interactive List */}
          <div className="w-full md:w-1/2 pl-2">
            <div className="p-4 bg-gray-200 border-b border-gray-300">
              <h2 className="text-lg font-semibold">Interactive List</h2>
            </div>
            <div className="h-full overflow-y-auto p-4">
              <InteractiveList
                treeData={treeData}
                onSelectNode={handleNodeSelection}
              />
            </div>
          </div>
        </main>
      )}
    </div>
  );
}

export default App;
