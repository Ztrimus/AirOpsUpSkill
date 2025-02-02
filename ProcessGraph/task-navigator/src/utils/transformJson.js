// export const transformJsonToTree = (json, rootUUID) => {
//   const buildTree = (nodeId) => {
//     const node = json[nodeId];
//     if (!node) return null;

//     return {
//       name: node.Step,
//       attributes: {
//         TreeLevel: node.TreeLevel,
//         IDList: node.IDList.join(", "),
//       },
//       children: (node.ChildNodeUUID || []).map(buildTree).filter(Boolean),
//     };
//   };

//   return buildTree(rootUUID);
// };

export const transformJsonToTree = (json, rootUUID) => {
  const buildTree = (nodeId) => {
    const node = json[nodeId];
    if (!node) return null;

    return {
      name: node.Step,
      attributes: {
        TreeLevel: node?.TreeLevel,
        IDList: node.IDList.join(", "),
      },
      children: (node.ChildNodeUUID || []).map(buildTree).filter(Boolean),
    };
  };

  const tree = buildTree(rootUUID);
  console.log("Transformed Tree:", tree);
  return tree;
};

export const transformJsonToAntdTree = (json, rootUUID) => {
  const buildTree = (nodeId) => {
    const node = json[nodeId];
    if (!node) return null;

    return {
      title: node.Step,
      key: node.UUID,
      children: (node.ChildNodeUUID || []).map(buildTree).filter(Boolean),
    };
  };

  return [buildTree(rootUUID)];
};
