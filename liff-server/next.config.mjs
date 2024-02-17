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
        protocol: "https",
        hostname: "via.placeholder.com",
      },
      {
        protocol: "https",
        hostname: "storage.googleapis.com",
        pathname: "/timelink-assets/**",
      },
    ],
  },
  output: "standalone",
};

export default nextConfig;
