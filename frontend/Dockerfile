FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN apk add --no-cache zlib=1.3.2-r0
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:1.27-alpine
RUN apk add --no-cache zlib=1.3.2-r0
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
