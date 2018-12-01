FROM python:3.6-alpine3.7
RUN pip install flask bs4 requests pymongo
RUN apk add tzdata
RUN cp /usr/share/zoneinfo/Asia/Taipei /etc/localtime
RUN echo "Asia/Taipei" >  /etc/timezone
RUN apk del tzdata
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["main.py"]
