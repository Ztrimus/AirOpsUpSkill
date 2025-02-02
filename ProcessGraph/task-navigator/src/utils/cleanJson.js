export const cleanJsonSteps = (json) => {
  const cleanedJson = { ...json };

  for (const key in cleanedJson) {
    if (cleanedJson[key].Step) {
      cleanedJson[key].Step = cleanedJson[key].Step.replace(/^\d+\.\s*/, ""); // Remove leading numbers
    }
  }

  return cleanedJson;
};
