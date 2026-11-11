# NodeJS 26.12.0 Alpine 3.24 (dev)
FROM ghcr.io/pnpm/pnpm:12-alpine AS build
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
COPY . .
RUN apk add libatomic
RUN pnpm ci
RUN pnpm run build


# NGinx 1.31.8 Debian 13
FROM dhi.io/nginx@sha256:bd653042e33ea48fde85d24dac4ff840eb152a2db12e86790851babcfbd10b80

COPY --from=build /app/dist /www/dist