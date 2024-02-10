/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    LIFF_ID: process.env.LIFF_ID,
    API_SERVER_URL: process.env.API_SERVER_URL,
    API_SERVER_ACCESS_TOKEN: process.env.API_SERVER_ACCESS_TOKEN,
  },
  images: {
    remotePatterns: [
      {
        hostname: "via.placeholder.com",
      },
    ],
  },
  output: "standalone",
};

export default nextConfig;
