FROM python:3
ENV PATH="/logger/:${PATH}"
RUN mkdir /logger
COPY logger.py /logger/
COPY start.sh /logger/
#RUN mkdir /var/log/logs-test
#COPY dummie.log /var/log/logs-test/
ENV LOG_FOLDER="/var/log/logs-test/*.log"
WORKDIR /logger
COPY requirements.txt /logger/
RUN pip install -r requirements.txt
#RUN chmod +x logger.py
CMD [ "start.sh" ]


