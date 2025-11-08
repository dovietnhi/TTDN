FROM rasa/rasa-sdk:3.6.2

# Chạy với quyền root để cài thêm thư viện
USER root

# Copy requirements.txt vào container
COPY requirements.txt /app/requirements.txt
WORKDIR /app
# Cài đặt múi giờ Asia/Ho_Chi_Minh
RUN apt-get update && apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Ho_Chi_Minh /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata
# Cài đặt thư viện với quyền root
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install --no-cache-dir pymongo
# Copy thư mục actions
COPY ./app/actions /app/actions
COPY ./scripts /app/scripts
# Chuyển về user mặc định (không phải root) cho an toàn
USER 1001

# Chạy action server
CMD ["start", "--actions", "actions"]
