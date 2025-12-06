import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from transformers import pipeline

MODEL_NAME = "wonrax/phobert-base-vietnamese-sentiment"

# Cache_resource để tải pipeline model 1 lần duy nhất
@st.cache_resource
def load_model():
    try:
        classifier = pipeline("sentiment-analysis", model=MODEL_NAME)
        return classifier
    except Exception as e:
        st.error(f"Lỗi khi tải model: {e}")
        return None

# Khởi tạo cơ sở dữ liệu SQLite và bảng 'sentiments'.
def init_db():
    conn = sqlite3.connect('sentiment_history.db')
    c = conn.cursor()
    # Tạo bảng nếu chưa tồn tại
    c.execute('''
    CREATE TABLE IF NOT EXISTS sentiments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        sentiment TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Thêm một bản ghi vào database.
def add_sentiment(text, sentiment):
    conn = sqlite3.connect('sentiment_history.db')
    c = conn.cursor()
    timestamp = datetime.now().isoformat(timespec='seconds') # Định dạng YYYY-MM-DD HH:MM:SS

    c.execute("INSERT INTO sentiments (text, sentiment, timestamp) VALUES (?, ?, ?)", 
              (text, sentiment, timestamp))
    
    conn.commit()
    conn.close()

# Lấy 50 kết quả gần nhất từ database.
def get_history():
    conn = sqlite3.connect('sentiment_history.db')
    c = conn.cursor()

    c.execute("SELECT timestamp, text, sentiment FROM sentiments ORDER BY timestamp DESC LIMIT 50")
    
    history_data = c.fetchall()
    conn.close()
    return history_data

# Phân loại cảm xúc của một câu văn.
def analyze_sentiment(classifier, text):
    if not classifier:
        return "Lỗi model"
        
    result = classifier(text)[0]
    # Lấy nhãn và xác suất cao nhất
    label = result['label']
    score = result['score']
    
    print(f"Nhãn: {label}, Xác suất: {score}")
    
    # Nếu xác suất < 0.5, trả về NEUTRAL
    if score < 0.5:
        return "NEUTRAL"
    
    return label.upper()

# Tiền xử lý văn bản
def preprocess_text(text):
    text = text.lower()
    replacement_dict = {
        "rat": "rất",
        "hom": "hôm",
        "wa": "quá",
        "qua": "quá",
        "do": "dở",     
        "bt": "bình thường",
        "cv": "công việc",
        "ko": "không",
        "dc": "được",
        "thik": "thích",
        "lun": "luôn",
        "h": "giờ",
        "nt": "nhắn tin",
        "on": "ổn",
        "buon": "buồn",
        "happy": "vui",
        "met": "mệt",
        "moi": "mỏi",
        "cam on": "cảm ơn",
    }
    
    words = text.split()
    processed_words = []
    
    for word in words:
        # Lấy từ đã thay thế, nếu không có trong từ điển thì dùng lại từ cũ
        processed_words.append(replacement_dict.get(word, word))
        
    text = " ".join(processed_words)
    
    return text

def main():
    st.title("Trợ lý Phân loại Cảm xúc Tiếng Việt")
    init_db()

    # Tải model
    classifier = load_model()

    if classifier:
        st.success("Model đã tải thành công!")
    else:
        st.stop()
        
    st.header("Nhập câu cần phân loại")
    user_input = st.text_area("Nhập văn bản (ví dụ: 'Hôm nay tôi rất vui')", "")

    if st.button("Phân loại cảm xúc"):
        if len(user_input) < 5 or len(user_input) > 50:
            st.error("Lỗi: Câu không hợp lệ, thử lại!")
        else:
            processed_input = preprocess_text(user_input)
            #Gọi pipeline Transformer
            with st.spinner("Đang phân tích..."):
                sentiment = analyze_sentiment(classifier, processed_input)
            print(f"Phân loại: {sentiment}")
            st.subheader("Kết quả phân loại")
            if sentiment == "POS":
                st.success(f"Cảm xúc: TÍCH CỰC (POSITIVE)")
            elif sentiment == "NEG":
                st.error(f"Cảm xúc: TIÊU CỰC (NEGATIVE)")
            else:
                st.info(f"Cảm xúc: TRUNG TÍNH (NEUTRAL)")
            try:
                add_sentiment(user_input, sentiment)
            except Exception as e:
                st.error(f"Lỗi khi lưu vào database: {e}")

    st.header("Lịch sử phân loại (50 mục gần nhất)")
    history = get_history()
    if not history:
        st.info("Chưa có lịch sử nào.")
    else:
        df = pd.DataFrame(history, columns=["Thời gian", "Văn bản đã nhập", "Cảm xúc"])
        st.dataframe(df, width="stretch")
if __name__ == "__main__":
    main()