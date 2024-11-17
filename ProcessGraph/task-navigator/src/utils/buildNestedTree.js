// utils/buildTree.js

/**
 * Transforms flat tree data into a nested tree structure.
 * @param {Object} flatData - The flat tree data with UUID keys.
 * @param {string} rootUuid - The UUID of the root node.
 * @returns {Object|null} - The nested tree structure or null if root not found.
 */
export function buildNestedTree(flatData, rootUuid) {
    if (!flatData || typeof flatData !== "object" || !flatData[rootUuid]) {
      console.error("Invalid flatData or rootUuid provided to buildNestedTree.");
      return null;
    }
  
    const traverse = (uuid) => {
      const node = flatData[uuid];
      if (!node) {
        console.warn(`Node with UUID "${uuid}" not found.`);
        return null;
      }
  
      const { Step, TreeLevel, IDList, ChildNodeUUID } = node;
  
      return {
        name: Step || "Unnamed Step",
        attributes: {
          TreeLevel: TreeLevel || 0,
          IDList: Array.isArray(IDList) ? IDList : [],
        },
        children: Array.isArray(ChildNodeUUID)
          ? ChildNodeUUID
              .map((childUuid) => traverse(childUuid))
              .filter((child) => child !== null)
          : [],
      };
    };
  
    return traverse(rootUuid);
  }
  