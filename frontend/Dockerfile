FROM node:26-slim

WORKDIR /app

COPY package.json package-lock.json nuxt.config.ts ./
RUN npm ci

COPY . .

EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
