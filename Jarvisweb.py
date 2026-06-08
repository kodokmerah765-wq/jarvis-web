import streamlit as st
from groq import Groq
from gtts import gTTS
import base64
from io import BytesIO

# 1. KONFIGURASI HALAMAN WEB
st.set_page_config(page_title="Jarvis AI Web", page_icon="🤖", layout="centered")

# Modifikasi CSS agar tampilan gelap dan futuristik ala Iron Man
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #ffffff; }
    h1 { color: #58a6ff; text-align: center; }
    .stTextInput i { color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)
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

# Inisialisasi riwayat obrolan di web browser jika belum ada
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tempat penampung audio terisolasi agar tidak mengganggu rendering teks
audio_placeholder = st.empty()

# 3. FUNGSI UNTUK MEMUTAR SUARA LANGSUNG DARI MEMORI RAM
def putar_suara_di_web(teks):
    tts = gTTS(text=teks, lang='id', slow=False)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    
    data = fp.read()
    b64 = base64.b64encode(data).decode()
    md = f"""
        <audio autoplay="true">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
    audio_placeholder.markdown(md, unsafe_allow_html=True)

# === TAMPILKAN RIWAYAT CHAT SEBELUMNYA ===
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else None):
        st.write(msg["content"])

# 4. TAMPILAN ANTARMUKA CHAT
user_input = st.chat_input("Ketik sesuatu atau berikan perintah pada Jarvis...")

if user_input:
    # Ambil input dan tampilkan di UI secara langsung
    with st.chat_message("user"):
        st.write(user_input)
    
    # Masukkan input user ke dalam state
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Buat format pesan untuk dikirim ke Groq Cloud
    messages_payload = [{"role": "system", "content": SYSTEM_INSTRUCTION}] + [
        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
    ]
        
    # Minta balasan dari Groq AI
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Jarvis sedang berpikir..."):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages_payload,
                temperature=0.7,
                max_tokens=1000
            )
            jawaban = completion.choices[0].message.content
            st.write(jawaban)
            
    # Masukkan balasan asisten ke dalam state
    st.session_state.messages.append({"role": "assistant", "content": jawaban})
    
    # Putar suaranya tanpa melakukan st.rerun()
    putar_suara_di_web(jawaban)
