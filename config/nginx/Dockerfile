FROM node:18-alpine as build-stage

WORKDIR /app
RUN corepack enable

COPY .npmrc package.json pnpm-lock.yaml ./
RUN --mount=type=cache,id=pnpm-store,target=/root/.pnpm-store \
    pnpm install --frozen-lockfile
from project.apps.payment.models import Payment
COPY frontend /app
COPY .env /app/.env
RUN pnpm build

FROM nginx:stable-alpine as production-stage

COPY --from=build-stage /app/dist /vue
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

