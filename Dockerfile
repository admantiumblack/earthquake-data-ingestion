FROM python:3.9.18-alpine as build
RUN apk update && apk add binutils
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN pip install pyinstaller
COPY ./ ./
RUN pyinstaller main.py -n ingest_earthquake --onefile

FROM alpine as deploy
COPY --from=build /app/dist/ingest_earthquake ./ingest_earthquake
RUN chmod +x ingest_earthquake
ENV STORAGE_LOCATION=localhost
ENTRYPOINT ["./ingest_earthquake"]
CMD []