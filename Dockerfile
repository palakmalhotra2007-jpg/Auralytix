# Multi-stage Dockerfile for Auralytix React SPA Frontend + Nginx Reverse Proxy
# Stage 1: Build the React SPA
FROM node:20-alpine AS build

WORKDIR /app

# Copy package manifests and install dependencies
COPY package*.json ./
RUN npm install

# Copy source code and build production distribution
COPY . .
RUN npm run build

# Stage 2: Serve with Nginx and proxy to FastAPI backend
FROM nginx:alpine

# Copy built frontend assets
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom Nginx reverse proxy configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
