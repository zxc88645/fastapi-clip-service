# 使用 Python 官方映像
FROM python:3.12

# 設置工作目錄
WORKDIR /code

# 複製依賴文件
COPY ./requirements.txt /code/requirements.txt

# 安裝依賴
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


# 複製項目文件
COPY ./app /code/app

# 運行服務
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
