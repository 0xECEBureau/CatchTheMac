FROM alpine:3.18 AS base

RUN echo "Layer 1 setup"

# Add some distractions
RUN echo "COPYING FILES" > /dev/null
RUN echo "LOADING DEPENDENCIES" > /dev/null
RUN echo "INSTALLING PACKAGES" > /dev/null

# Add the flag and remove it
RUN echo "01001101 01000001 01000011 01111011 01001001 01011111 00111100 00110011 01011111 01000100 00110011 01110110 00110000 01110000 01110011 00100001 01111101" > /binary_playload && \
    cat /binary_playload > /dev/null && \
    rm /binary_playload

# Add some more fake layers
RUN echo "FINISHING SETUP" > /etc/motd

WORKDIR /app

COPY . /app/

CMD ["sh"]
