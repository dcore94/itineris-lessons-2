FROM harbor.d4science.org/ccp-runtimes/cookie-cutter:1.0.0

COPY requirements.txt DejaVuSans.ttf train.sh train.py predict.sh predict.py /methods/
RUN pip install -r requirements.txt
RUN chmod 755 train.sh predict.sh