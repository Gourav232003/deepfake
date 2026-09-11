/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      // Tokens taken directly from Design.md — keep the two files in sync.
      colors: {
        graphite: {
          900: "#14161a",
          700: "#2a2e35",
          500: "#5b6270",
          300: "#a8adb8",
          100: "#eceef1",
        },
        surface: {
          light: "#faf9f7",
          dark: "#1b1e23",
        },
        state: {
          real: "#3f7a54",       // muted forest green
          fake: "#a4453d",       // desaturated red
          synthetic: "#6a5a8c",  // violet-gray
          tampered: "#b8862f",   // amber
          invalid: "#7a2e2e",    // dark red
          nowatermark: "#6b7280", // neutral gray
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["'JetBrains Mono'", "ui-monospace", "monospace"],
      },
      spacing: {
        18: "4.5rem",
      },
      maxWidth: {
        content: "1200px",
        prose: "760px",
      },
    },
  },
  plugins: [],
};
