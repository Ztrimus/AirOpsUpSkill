import React, {
    forwardRef,
    useImperativeHandle,
    useState,
    useEffect,
    useRef,
  } from "react";
  import Tree from "react-d3-tree";
  
  const TreeView = forwardRef(({ treeData, selectedNode, onNodeClick }, ref) => {
    const treeContainerRef = useRef(null);
    const [translate, setTranslate] = useState({
      x: window.innerWidth / 2,
      y: window.innerHeight / 4,
    });
    const [zoom, setZoom] = useState(1);
  
    // Adjust translate position on window resize
    useEffect(() => {
      const handleResize = () => {
        if (treeContainerRef.current) {
          const dimensions = treeContainerRef.current.getBoundingClientRect();
          setTranslate({
            x: dimensions.width / 2,
            y: dimensions.height / 4,
          });
        }
      };
      window.addEventListener("resize", handleResize);
      handleResize();
      return () => window.removeEventListener("resize", handleResize);
    }, []);
  
    // Expose zoomToNode method to the parent
    useImperativeHandle(ref, () => ({
      zoomToNode: (nodeName) => {
        console.warn("zoomToNode functionality removed.");
      },
    }));
  
    const renderCustomNode = ({ nodeDatum, toggleNode }) => {
      const isSelected = selectedNode === nodeDatum.name;
  
      return (
        <g
          onClick={() => {
            toggleNode();
            onNodeClick(nodeDatum.name);
          }}
        >
          <circle
            r={40}
            fill={isSelected ? "orange" : "#63b3ed"}
            stroke={isSelected ? "#ff9800" : "#333"}
            strokeWidth={3}
            style={{ cursor: "pointer" }}
          />
          <text
            fill={isSelected ? "#000" : "#555"}
            fontSize="12px"
            textAnchor="middle"
            y={5}
          >
            {nodeDatum.name}
          </text>
        </g>
      );
    };
  
    return (
      <div
        id="treeWrapper"
        ref={treeContainerRef}
        style={{
          width: "100%",
          height: "100vh",
          background: "linear-gradient(to bottom, #f0f4f8, #e2eaf0)",
          borderRadius: "12px",
          boxShadow: "0 8px 20px rgba(0, 0, 0, 0.15)",
          overflow: "hidden",
        }}
      >
        <Tree
          data={treeData}
          orientation="vertical"
          translate={translate}
          zoom={zoom}
          renderCustomNodeElement={renderCustomNode}
          zoomable
          enableLegacyTransitions
          transitionDuration={500}
          nodeSize={{ x: 200, y: 200 }}
          styles={{
            links: {
              stroke: "#ccc",
              strokeWidth: 2,
            },
          }}
        />
      </div>
    );
  });
  
  export default TreeView;
  