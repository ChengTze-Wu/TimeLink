import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
          primary: {
            green: "#44ad53",
            white: "#e7e7e7",
          },
          secondary: {
            blue: "#272c33",
            gray: "#414a58",
          },
        },
      },
    },
  plugins: [],
}
export default config
