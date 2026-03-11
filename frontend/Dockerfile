# ---------- Build Stage ----------
    FROM node:18-alpine AS build

    WORKDIR /app
    
    # Install dependencies
    COPY package*.json ./
    RUN npm install
    
    # Copy source code
    COPY . .
    
    # Build app
    RUN npm run build
    
    
    # ---------- Production Stage ----------
    FROM nginx:alpine
    
    # Upgrade packages to patch any vulnerabilities in the base image (e.g., zlib CVE-2026-22184)
    RUN apk upgrade --no-cache
    
    # Remove default nginx config
    RUN rm -rf /usr/share/nginx/html/*
    
    # Copy build files
    COPY --from=build /app/dist /usr/share/nginx/html
    
    # Expose port
    EXPOSE 80
    
    CMD ["nginx", "-g", "daemon off;"]
    