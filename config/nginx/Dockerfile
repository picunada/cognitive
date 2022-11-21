# Stage 1 - build frontend app
FROM node:18-alpine as frontend

# Creating folders, and files for a project
WORKDIR /app
COPY frontend /app
COPY .env /app/.env

# Project initialization
RUN npm install
RUN npm rebuild node-sass
RUN npm run build

# Stage 2 - nginx & frontend dist
FROM nginx:alpine

# copy files and settings
COPY --from=frontend /app/dist/ /vue

# run nginx
CMD ["nginx", "-g", "daemon off;"]
