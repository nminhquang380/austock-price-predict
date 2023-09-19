FROM amazonlinux:2

RUN amazon-linux-extras enable python3.8
RUN yum clean metadata
RUN yum -y install python3.8
RUN python3.8 -m ensurepip
RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install virtualenv

RUN python3.8 -m virtualenv lambda-env
RUN source lambda-env/bin/activate

RUN python3.8 -m pip install yfinance psycopg2-binary numpy urllib3==1.26.5 -t python

RUN python3.8 -m pip install -U scikit-learn

# Install zip utility
RUN yum -y install zip

CMD zip -r9 lambda-layer.zip ./python