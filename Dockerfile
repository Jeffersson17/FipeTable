FROM node:14

WORKDIR /app

COPY ./frontend/package*.json ./

RUN npm install

COPY ./frontend .

RUN npm run build

EXPOSE 8080

CMD ["npm", "run", "serve"]
