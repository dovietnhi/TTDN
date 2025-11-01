# 🤖 Chatbot Rasa Demo

Chatbot được xây dựng bằng **Rasa Open Source**, hỗ trợ triển khai qua **Docker**.  
Mục tiêu: xây dựng bot trả lời tự động trên web.

---

## 🧱 Cấu trúc dự án

chatbot-app/
├── actions/ # Các custom action (Python)
│ └── actions.py
├── data/ # Dữ liệu huấn luyện
│ ├── nlu.yml
│ ├── rules.yml
│ └── stories.yml
├── models/ # Model sau khi train
├── domain.yml # Khai báo intent, entity, responses
├── config.yml # Cấu hình pipeline & policies
├── credentials.yml # Kết nối với webchat (REST, socketio)
├── endpoints.yml # Định nghĩa endpoint cho action server
├── requirements.txt # Thư viện cần thiết
├── Dockerfile # Dùng để build image Rasa
├── docker-compose.yml # Dùng để chạy Rasa + Action Server
├── index.html # Webchat UI
└── README.md # File hướng dẫn

---

## 🚀 Cách chạy chatbot

### 1️⃣ Cài đặt môi trường (nếu chạy local)

```bash
    Build image Docker

Mở PowerShell tại thư mục D:\chatbot-app, rồi chạy:

docker build -t chatbot-demo .
pip install -r requirements.txt
Huấn luyện mô hình:
docker compose run rasa train
docker compose up --build

docker run -it -v "D:\chatbot-app:/app" chatbot-demo train
docker run -it -v "$(pwd):/app" rasa-core train


Chạy chatbot:

Restart lại Rasa server

Nếu bạn đang dùng Docker Compose, hãy dừng và khởi động lại:

docker-compose down
docker-compose up

Mở index.html trên trình duyệt để trò chuyện.

2️⃣ Chạy bằng Docker
Bước 1: Build image
docker build -t rasa-chatbot .

Bước 2: Chạy container
docker run -d -p 5005:5005 rasa-chatbot

(Tùy chọn) Dùng Docker Compose
docker-compose up --build

💬 Kết nối với Webchat

Trong credentials.yml, bật SocketIO:

rest:
socketio:
  user_message_evt: user_uttered
  bot_message_evt: bot_uttered
  session_persistence: true


Và trong index.html:

<script src="https://cdn.jsdelivr.net/npm/rasa-webchat/lib/index.js"></script>
<div id="webchat"></div>
<script>
  WebChat.default({
    initPayload: '/greet',
    socketUrl: 'http://localhost:5005',
    socketPath: '/socket.io/',
    title: 'Rasa Chatbot',
    subtitle: 'Xin chào!',
  }, null);
</script>

🛠️ Khắc phục lỗi phổ biến
Lỗi	Nguyên nhân	Cách xử lý
attempt to write a readonly database	SQLite trong Docker không ghi được	Thêm sqlalchemy<2.0 trong requirements.txt
xhr poll error / 404 socket.io	Rasa chưa bật SocketIO	Thêm block socketio: trong credentials.yml
ModuleNotFoundError	Thiếu thư viện	Kiểm tra và cài bằng pip install -r requirements.txt
👨‍💻 Liên hệ

Tác giả: Tên bạn
Email: [your_email@example.com
]
GitHub: [github.com/yourusername]


---

Nếu bạn muốn mình viết luôn thêm:
- ✅ `Dockerfile`
- ✅ `docker-compose.yml`
- ✅ `index.html`  
đồng bộ với 2 file này (`requirements.txt` + `README.md`)

thì mình có thể tạo trọn bộ deploy sẵn cho bạn (chạy 1 lệnh là lên web).  
Bạn muốn mình tạo giúp luôn không?
## Xuất dữ liệu
docker compose exec action_server python /app/scripts/export_chat_data.py
## Coppy file trong container ra ngoài
docker compose cp action_server:/app/chat_data.json ./chat_data.json
