FROM python:3.10
USER root
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN chmod 777 start.sh
ENTRYPOINT [ "/bin/sh" ]
CMD ["start.sh"]
