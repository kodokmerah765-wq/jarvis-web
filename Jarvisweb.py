import streamlit as st
from groq import Groq
from gtts import gTTS
import os
import base64

# 1. KONFIGURASI HALAMAN WEB
st.set_page_config(page_title="Jarvis AI Web", page_icon="🤖", layout="centered")

# Modifikasi CSS agar tampilan gelap dan futuristik ala Iron Man
# Modifikasi tampilan (CSS) agar gelap dan futuristik ala Iron Man
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #ffffff; }
    h1 { color: #58a6ff; text-align: center; }
    .stTextInput i { color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)  # <-- Bagian ini sudah diperbaiki memakai unsafe_allow_html
st.title("🤖 JARVIS INTERACTIVE WEB")
st.write("Selamat datang kembali, **Tony**. Ketik perintah atau pertanyaan Anda di bawah.")

# 2. KONFIGURASI API GROQ
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

SYSTEM_INSTRUCTION = (
    "Anda adalah Jarvis, asisten AI pribadi yang sangat cerdas, loyal, dan efisien seperti di film Iron Man. "
    "Panggil pengguna dengan sebutan 'Tony'. Jawablah dengan singkat, padat, jelas, dan sedikit berwibawa "
    "namun tetap ramah dan membantu. Gunakan bahasa Indonesia."
)

# Inisialisasi riwayat obrolan di web browser
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}]

# 3. FUNGSI UNTUK MEMUTAR SUARA DI WEB BROWSER
def putar_suara_di_web(teks):
    tts = gTTS(text=teks, lang='id', slow=False)
    filename = "respon_jarvis.mp3"
    tts.save(filename)
    
    # Mengubah audio menjadi format yang bisa dibaca browser secara otomatis
    with open(filename, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)
    os.remove(filename)

# 4. TAMPILAN ANTARMUKA CHAT
user_input = st.chat_input("Ketik sesuatu atau berikan perintah pada Jarvis...")

if user_input:
    # Tampilkan chat user di layar web
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
        
    # Kirim ke otak Groq AI
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Jarvis sedang berpikir..."):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=1000
            )
            jawaban = completion.choices[0].message.content
            st.write(jawaban)
            
    # Masukkan ke riwayat dan bunyikan suaranya di browser Tony
    st.session_state.messages.append({"role": "assistant", "content": jawaban})
    putar_suara_di_web(jawaban)

# Menampilkan riwayat chat sebelumnya di layar agar keren
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else None):
            st.write(msg["content"])