/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    API_GATEWAY: process.env.API_GATEWAY,
    AUTH_SECRET: process.env.AUTH_SECRET,
    GCS_BUCKET_NAME: process.env.GCS_BUCKET_NAME,
    GCS_CLIENT_EMAIL: process.env.GCS_CLIENT_EMAIL,
    GCS_PRIVATE_KEY: process.env.GCS_PRIVATE_KEY,
  },
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "storage.googleapis.com",
        pathname: "/timelink-assets/**",
      },
    ],
  },
  experimental: {
    // Issue `TypeError: Expected signal to be an instanceof AbortSignal` when
    // using `@google-cloud/storage` for uploading files, we need to add this config
    // see: https://github.com/vercel/next.js/issues/59432#issuecomment-1876846798 and
    // https://nextjs.org/docs/app/api-reference/next-config-js/serverComponentsExternalPackages
    serverComponentsExternalPackages: ["@google-cloud/storage"],
  },
  output: "standalone",
};

module.exports = nextConfig;
