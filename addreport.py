import streamlit as st
import urllib.parse

st.title("Customization Report by Request")
st.divider()

st.subheader("Hi... ! 😊")
st.write("Jika ada kebutuhan untuk mengolah report sesuai dengan kebutuhan anda, just let me know ya . .  👇")

# WhatsApp contact information
phone_number = "6285156215055"  # Your WhatsApp number in international format
default_message = "Saya mau request custom report dong"  # Default message

# Create the WhatsApp URL with pre-filled message
whatsapp_url = f"https://wa.me/{phone_number}?text={urllib.parse.quote(default_message)}"

# WhatsApp contact button
st.link_button("Contact WhatsApp", whatsapp_url)

# Optional: Add a text area for custom message
custom_message = st.text_area("Sampaikan pesan-mu sekaligus !")
custom_whatsapp_url = f"https://wa.me/{phone_number}?text={urllib.parse.quote(custom_message)}"
st.link_button("Send via WhatsApp", custom_whatsapp_url)