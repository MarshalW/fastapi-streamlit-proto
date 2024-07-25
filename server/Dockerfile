FROM  python:3.12-alpine

# 设置时区环境变量
ENV TZ=Asia/Shanghai

# 设置时区和pip镜像
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && pip config --user set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 设置工作目录
WORKDIR /app

# 安装项目依赖
RUN pip install --no-cache-dir fastapi uvicorn

RUN pip install sse-starlette

RUN pip install openai

RUN pip install llama-index \
                llama-index-llms-openai-like \
                llama-index-embeddings-ollama


# 复制项目文件到容器中
COPY ./src /app

# 为容器指定要运行的命令
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "7777"]

# 暴露端口80，让容器外的请求可以访问到应用
EXPOSE 7777