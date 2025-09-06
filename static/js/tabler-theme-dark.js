/*!
 * Tabler v1.4.0
 * Default dark theme with toggle support
 */

(function () {
  "use strict";

  // Default dark theme settings
  const defaults = {
    theme: "dark",
    "theme-base": "gray",
    "theme-font": "sans-serif",
    "theme-primary": "blue",
    "theme-radius": "1"
  };

  // Immediately apply dark mode to prevent FOUC
  // Use stored value if user previously toggled
  const savedTheme = localStorage.getItem("tabler-theme") || defaults.theme;
  document.documentElement.setAttribute("data-bs-theme", savedTheme);

  // Apply other defaults immediately (non-blocking)
  for (const key of Object.keys(defaults)) {
    if (key === "theme") continue; // already set
    const saved = localStorage.getItem("tabler-" + key) || defaults[key];
    document.documentElement.setAttribute("data-bs-" + key, saved);
  }

  // After DOM loads, save current settings in localStorage
  document.addEventListener("DOMContentLoaded", () => {
    localStorage.setItem("tabler-theme", savedTheme);
    for (const key of Object.keys(defaults)) {
      if (key === "theme") continue;
      const value = document.documentElement.getAttribute("data-bs-" + key);
      localStorage.setItem("tabler-" + key, value);
    }
  });

})();
