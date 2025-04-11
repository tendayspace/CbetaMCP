# 使用轻量 Python 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 拷贝依赖清单并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 拷贝全部代码（含.env）
COPY . .

# 显式暴露端口（方便 Dockerfile 文档化）
EXPOSE 8000

# 使用 uvicorn 启动，并加载环境变量（自动识别 .env）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000","--reload"]
