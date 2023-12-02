/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./web/templates/**/*.html", "./web/static/js/*.js"],
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
};
