FROM rasa/rasa-sdk:3.6.2

# Chạy với quyền root để cài thêm thư viện
USER root

# Copy requirements.txt vào container
COPY requirements.txt /app/requirements.txt
WORKDIR /app

# Cài đặt thư viện với quyền root
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install --no-cache-dir pymongo
# Copy thư mục actions
COPY ./actions /app/actions
COPY ./scripts /app/scripts
# Chuyển về user mặc định (không phải root) cho an toàn
USER 1001

# Chạy action server
CMD ["start", "--actions", "actions"]
