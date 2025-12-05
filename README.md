# TRỢ LÝ PHÂN LOẠI CẢM XÚC TIẾNG VIỆT (Vietnamese Sentiment Assistant)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![AI Model](https://img.shields.io/badge/Model-PhoBERT-green)

## Giới thiệu
Đây là ứng dụng Web đơn giản giúp tự động nhận diện cảm xúc của câu văn Tiếng Việt (Tích cực, Tiêu cực, Trung tính). Dự án sử dụng mô hình **Transformer (PhoBERT)** thông qua thư viện Hugging Face và giao diện tương tác **Streamlit**.

### Tính năng chính
* **Nhập liệu tự do:** Hỗ trợ nhập văn bản tiếng Việt có dấu/không dấu.
* **Xử lý thông minh:** Tự động phân loại cảm xúc.
* **Lịch sử:** Lưu trữ và hiển thị 50 lần phân tích gần nhất.
* **Giao diện:** Thân thiện, dễ sử dụng, chạy trên nền tảng Web.

---

## Yêu cầu cài đặt
Để chạy được ứng dụng, máy tính cần cài đặt:
1.  **Python:** Phiên bản 3.8 trở lên (Project đang sử dụng là bản 3.12).
2.  **Project:** Download File Zip và giải nén hoặc Clone về thiết bị.
3.  **Thư viện:** Các thư viện liệt kê trong `requirements.txt` của dự án.

---

## Hướng dẫn Cài đặt & Chạy

### Bước 1: Thiết lập môi trường ảo (Virual Enviroment)
Mở Terminal tại thư mục dự án và chạy lệnh sau để cài đặt các thư viện cần thiết:
```bash
python -m venv .venv (Để cài đặt môi trường ảo)
.\.venv\Scripts\Activate (Để mở môi trường ảo)
```
### Bước 2: Chuẩn bị thư viện
```bash
python -m pip install --upgrade pip (Update Pip lên bản mới nhất)
pip install -r requirements.txt (Cài đặt các thư viên trong file requirements.txt)
```
### Bước 3: Chạy ứng dụng 
```bash
streamlit run app.py
```

## Tài liệu tham khảo
1. Hugging Face Transformers
2. PhoBERT
3. Streamlit Documentation