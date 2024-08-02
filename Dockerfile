# 使用 Python 官方映像
FROM python:3.12

# 設置工作目錄
WORKDIR /app

# 複製項目文件
COPY . .

# 安裝依賴
RUN pip install -r requirements.txt

# 暴露服務端口
EXPOSE 8000

# 運行服務
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
