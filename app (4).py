import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from pyzbar import pyzbar
import cv2
import threading

st.set_page_config(page_title="Lettuce Verification", layout="centered")

st.title(" Lettuce Verification System")
st.write("Scan the QR code on your lettuce to verify authenticity.")

# -------------------------------------------------------
# OFFICIAL HASH + BLOCKCHAIN SUPPLY-CHAIN RECORD
# -------------------------------------------------------
official_hash = "000ab71c09bc7950e9782767cb7a3c3b1e4168cd198224d6ec8491e47d2a1541"

supply_chain_data = {
    "Harvest": {
        "Location": "Yuma, Arizona – Field 7B",
        "DateTime": "2025-01-05 06:45 AM",
        "WorkerID": "H-203"
    },
    "Washing & Cleaning": {
        "Facility": "Salinas Wash Unit 3",
        "WashTemp": "3°C",
        "DateTime": "2025-01-05 07:20 AM",
        "SupervisorID": "W-87"
    },
    "Packaging": {
        "Facility": "Zone A Vacuum Pack",
        "PackType": "Triple-Wash Ready-to-Eat",
        "DateTime": "2025-01-05 08:10 AM",
        "MachineID": "PKG-442"
    },
    "Cold Chain Transport": {
        "TruckID": "TRK-5562",
        "DispatchTemp": "3°C",
        "From": "Salinas Packaging Center",
        "To": "Dallas Distribution Center",
        "DateTime": "2025-01-05 10:30 AM"
    },
    "Walmart Store Arrival": {
        "Store": "Walmart Supercenter #451, Aisle 3",
        "ReceivedTemp": "4°C",
        "DateTime": "2025-01-06 06:10 AM",
        "StaffID": "RCV-98"
    }
}

# -------------------------------------------------------
# QR SCANNER USING WEBCAM
# -------------------------------------------------------
decoded_qr = st.empty()

class QRScanner(VideoTransformerBase):
    def __init__(self):
        self.qr_data = None
        self.lock = threading.Lock()

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        decoded = pyzbar.decode(img)

        with self.lock:
            if decoded:
                self.qr_data = decoded[0].data.decode("utf-8")
                cv2.putText(img, "QR Detected!", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)

        return img


ctx = webrtc_streamer(
    key="example",
    video_transformer_factory=QRScanner,
    media_stream_constraints={"video": True, "audio": False},
)

st.write("Point your lettuce QR code at the camera...")

# -------------------------------------------------------
# VERIFICATION LOGIC
# -------------------------------------------------------
if ctx.video_transformer:
    qr_value = ctx.video_transformer.qr_data

    if qr_value:
        st.success("QR scanned successfully!")
        st.write(f"**Scanned Hash:** `{qr_value}`")

        if qr_value == official_hash:
            # SAFE LETTUCE
            st.success("✔ SAFE – Your lettuce is authentic and untampered.")
            st.markdown("---")
            st.subheader("📦 Full Traceability Record")

            for stage, details in supply_chain_data.items():
                st.markdown(f"### 🟢 {stage}")
                for key, value in details.items():
                    st.markdown(f"**{key}:** {value}")
                st.write("")

        else:
            # TAMPERED LETTUCE
            st.error("❗ TAMPERED – Hash mismatch detected!")
            st.write("""
            This lettuce does **NOT** match the official blockchain record.
            It may have been altered, repackaged, or come from an unsafe batch.  
            Please do **NOT** consume this product.
            """)
