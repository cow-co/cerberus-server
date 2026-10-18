# NodeJS 26.12.0 Alpine 3.24 (dev)
FROM dhi.io/node@sha256:ba2ebc56e9558265f3fe2a6da3d0450c525d5b0ed49e46efe59588e5d69a1631 as build
RUN npx get-pnpm
RUN pnpm build


# NGinx 1.31.7 Debian 13
FROM dhi.io/nginx@sha256:00708c837b500b2b3f97a9fed6aef060011217874325c27bdf9f899f38e30dcb