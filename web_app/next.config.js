/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    API_GATEWAY: process.env.API_GATEWAY,
    AUTH_SECRET: process.env.AUTH_SECRET,
  },
  output: "standalone",
};

module.exports = nextConfig;
