FROM rasa/rasa-sdk:3.6.2

# Chạy với quyền root để cài thêm thư viện
USER root

WORKDIR /app

<<<<<<< HEAD
# Cài múi giờ
RUN apt-get update && apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Ho_Chi_Minh /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# Cài các thư viện từ requirements nếu có
COPY requirements.txt /app/requirements.txt
=======
# Cài đặt thư viện với quyền root
>>>>>>> parent of 7438095 (6/11)
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy actions
COPY ./actions /app/actions
COPY ./scripts /app/scripts

# Chuyển về user mặc định cho an toàn
USER 1001

# Chạy action server
CMD ["start", "--actions", "actions"]
