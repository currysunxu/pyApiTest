FROM python:3.7-slim
ADD ./hostfile ./hostfile

WORKDIR /app
COPY /etc/hosts /tmp/hosts.bak
RUN cp hostfile /tmp/hosts

 # hosts 於外部
RUN cp /etc/hosts .
#RUN cp /etc/hosts /tmp/hosts #路径长度最好保持一致
RUN mkdir -p -- /lib-override && cp /lib/x86_64-linux-gnu/libnss_files.so.2 /lib-override
RUN sed -i 's:/etc/hosts:/tmp/hosts:g' /lib-override/libnss_files.so.2
ENV LD_LIBRARY_PATH /lib-override

ENV PATH=/opt/java/bin:$PATH
CMD cat /tmp/hosts >> /etc/hosts; java -Djava.security.egd=file:/dev/./urandom -jar /app.jar; cat /etc/hosts
