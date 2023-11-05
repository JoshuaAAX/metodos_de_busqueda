#FROM node:18-alpine AS react-builder
#WORKDIR /code
#COPY ./frontend/package*.json ./
#RUN npm install
#COPY ./frontend ./
#RUN npm run build

FROM python:3.11-slim
WORKDIR /code
COPY ./backend/requirements.txt ./
RUN pip install -r requirements.txt
COPY ./backend .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
