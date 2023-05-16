FROM python:3.8.10
ARG CACHEBUST=1 
LABEL writer noob.hy
WORKDIR /opt/suggestion
#ENV https_proxy "https://free.shecan.ir/dns-query"
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf
RUN apt-get update
COPY . .
RUN apt-get install -y python3-pip
RUN pip install -r requirement.txt
EXPOSE 5000
CMD flask run

