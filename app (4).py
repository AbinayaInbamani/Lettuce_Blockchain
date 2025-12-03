import streamlit as st
import qrcode
from io import BytesIO

st.set_page_config(page_title="Lettuce Blockchain Verifier", layout="centered")

st.title("Lettuce Blockchain Verification App")
st.write("Verify whether a lettuce batch is SAFE or TAMPERED by comparing hashes.")

# Input for official blockchain hash
official_hash = st.text_input("Enter OFFICIAL Blockchain Hash (from Block 5):")

# Input for scanned QR hash
scanned_hash = st.text_input("Enter SCANNED Hash (from QR Code):")

# Verification logic
if st.button("Verify"):
    if not official_hash or not scanned_hash:
        st.warning("Please enter both hashes.")
    else:
        if official_hash.strip() == scanned_hash.strip():
            st.success("SAFE – Authentic lettuce batch.")
        else:
            st.error("TAMPERED – Hash mismatch detected!")

# Optional: Generate QR code
st.subheader("Generate QR Code for Official Hash")
if st.button("Generate QR Code"):
    if not official_hash:
        st.warning("Enter official hash first!")
    else:
        qr = qrcode.make(official_hash)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="QR Code")
