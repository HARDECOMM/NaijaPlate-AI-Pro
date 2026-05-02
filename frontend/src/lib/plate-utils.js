// src/lib/plate-utils.js
export function validateNigerianPlate(text) {
  if (!text) return false;
  // This regex allows optional dashes and spaces between the three parts
  const regex = /^[A-Z]{3}[-\s]?\d{3,4}[-\s]?[A-Z]{2}$/i;
  // Also check for Government/Diplomatic formats if needed
  const govRegex = /^[A-Z]{2}\d{3,5}[A-Z]{1,2}$/i;
  
  return regex.test(text) || govRegex.test(text);
}

// Add this helper to clean plate numbers for display
export function formatPlateForDisplay(text) {
  const clean = text.replace(/[^A-Z0-9]/gi, "").toUpperCase();
  if (clean.length < 8) return clean;
  // Standard formatting: ABC-123DE
  return `${clean.substring(0, 3)}-${clean.substring(3, clean.length - 2)}${clean.substring(clean.length - 2)}`;
}