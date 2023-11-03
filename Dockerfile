FROM node:18-alpine AS react-builder
WORKDIR /code
COPY ./frontend/package*.json ./
RUN npm install
COPY ./frontend ./
RUN npm run build

FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY ./backend/requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY --from=react-builder /code/dist ./frontend/dist
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
