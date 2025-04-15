FROM python:3.10.13-alpine

# Path: /app
WORKDIR /app

# 阶段1：安装构建依赖
RUN apk update && \
    apk add --no-cache --virtual .build-deps \
    gcc \
    g++ \
    musl-dev \
    openblas-dev \
    python3-dev \
    py3-pip \
    build-base

# 配置清华镜像源
RUN pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# 复制项目文件到容器中
COPY . .

# 安装项目的依赖
RUN pip install --no-cache-dir -r requirements.txt && pip cache purge

# 阶段2：清理构建依赖
RUN rm -rf /var/cache/apk/*

# 最终运行命令
CMD ["python", "main.py"]
