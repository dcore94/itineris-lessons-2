FROM harbor.d4science.org/ccp-runtimes/cookie-cutter:1.0.0

COPY requirements.txt /methods/
RUN pip install -r requirements.txt

COPY __main__.py /methods/

RUN mkdir itphones_outputs

CMD ["sh", "-c", "python ."]