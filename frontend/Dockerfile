# Stage 1: Build Angular app
FROM node:20-alpine AS build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build the app (será executado em dev mode com hot reload)
# Em produção, descomente a linha abaixo:
# RUN npm run build

# Stage 2: Development (com hot reload)
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install -g @angular/cli@17
RUN npm install

# Copy source code
COPY . .

# Expose port
EXPOSE 4200

# Start development server with hot reload
CMD ["npm", "start"]
