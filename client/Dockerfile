FROM ubuntu:22.04

RUN sed -i s@/archive.ubuntu.com/@/mirrors.tuna.tsinghua.edu.cn/@g /etc/apt/sources.list
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install \
        iputils-ping \
        nano \
        curl \
        python3 \
        pip \
        -y

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install \
    streamlit \
    streamlit-option-menu \
    streamlit-local-storage \
    httpx \
    sseclient-py

WORKDIR /app
CMD [ "streamlit","run", "--client.showSidebarNavigation=False", "./app.py" ]