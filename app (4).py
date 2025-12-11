import streamlit as st
from PIL import Image
import cv2
import numpy as np

# ---------------------------------------
# OFFICIAL BLOCKCHAIN HASH (Block 4)
# ---------------------------------------
OFFICIAL_HASH = "0006a93cf74a54a5709f041c460dad2ca82b0d50d93eca11a76efc46fede8fed"

# ---------------------------------------
# SUPPLY-CHAIN BLOCK SUMMARIES
# ---------------------------------------
BLOCKS = [
    {
        "stage": "Harvest",
        "details": {
            "Location": "NFREC, Quincy – Field 7B",
            "Date & Time": "2025-01-05 06:45 AM",
            "Worker ID": "H-203",
        },
    },
    {
        "stage": "Washing & Cleaning",
        "details": {
            "Facility": "Salinas Wash Unit 3",
            "Wash Temperature": "3°C",
            "Date & Time": "2025-01-05 07:20 AM",
            "Supervisor ID": "W-87",
        },
    },
    {
        "stage": "Packaging",
        "details": {
            "Facility": "Zone A Vacuum Pack",
            "Pack Type": "Triple-Wash Ready-to-Eat",
            "Date & Time": "2025-01-05 08:10 AM",
            "Machine ID": "PKG-442",
        },
    },
    {
        "stage": "Cold Chain Transport",
        "details": {
            "Truck ID": "TRK-5562",
            "Dispatch Temperature": "3°C",
            "Route": "Quincy Packaging Center → Tallahassee Distribution Center",
            "Date & Time": "2025-01-05 10:30 AM",
        },
    },
    {
        "stage": "Walmart Store Arrival",
        "details": {
            "Store": "Walmart Supercenter #451, Aisle 3",
            "Received Temperature": "4°C",
            "Date & Time": "2025-01-06 06:10 AM",
            "Staff ID": "RCV-98",
        },
    },
]


# ---------------------------------------
# Helper: decode QR from a PIL image using OpenCV
# ---------------------------------------
def decode_qr_from_pil(pil_image: Image.Image) -> str | None:
    """
    Takes a PIL image, converts it to OpenCV format,
    and tries to decode a QR code using OpenCV's QRCodeDetector.
    Returns the decoded string or None if nothing is found.
    """
    # PIL (RGB) -> NumPy array -> BGR for OpenCV
    np_img = np.array(pil_image.convert("RGB"))
    cv_img = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)

    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(cv_img)

    if points is not None and data:
        return data.strip()
    return None


# ---------------------------------------
# STREAMLIT UI
# ---------------------------------------
st.set_page_config(
    page_title="Lettuce QR Verifier", layout="centered"
)

st.title("Lettuce Blockchain QR Verification")
st.write(
    """
Imagine this app running in the background at a grocery store.

1. The QR code on the bag of lettuce is scanned (you upload a photo here).  
2. The QR contains a hidden hash value.  
3. The system compares it with the **official blockchain hash** for this batch.  
4. If it matches → the lettuce is SAFE and its full journey is shown.  
   If not → the lettuce is flagged as TAMPERED.
"""
)

uploaded_file = st.file_uploader(
    "Upload a photo of the lettuce QR code (PNG/JPG):",
    type=["png", "jpg", "jpeg"],
)

scanned_hash = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded QR code", use_column_width=True)

    scanned_hash = decode_qr_from_pil(image)

    if scanned_hash:
        st.info(f"Scanned value from QR: `{scanned_hash}`")
    else:
        st.error(
            "No QR code could be decoded from this image. "
            "Try a clearer or closer picture of the QR."
        )


# ---------------------------------------
# VERIFICATION LOGIC
# ---------------------------------------
if scanned_hash:
    if scanned_hash == OFFICIAL_HASH:
        # SAFE CASE
        st.success(
            "Your lettuce is SAFE – it matches the official blockchain record."
        )
        st.write("---")
        st.subheader(" Brief Supply-Chain Journey (All Blocks Valid)")

        for block in BLOCKS:
            st.markdown(f"### {block['stage']}")
            for key, value in block["details"].items():
                st.markdown(f"**{key}:** {value}")
            st.write("")

        st.caption(
            "If any block (harvest, washing, packaging, transport, or store arrival) "
            "were secretly changed, the final hash would change and this QR check would fail."
        )
    else:
        # TAMPERED CASE
        st.error(
            " WARNING: Lettuce is TAMPERED – QR hash does not match the official record."
        )
        st.write(
            """
This product does **not** match the blockchain record for batch `LETTUCE001`.  
It may have been altered, repackaged, or come from an unsafe batch.  
Please **do not consume** this lettuce and report it to store staff.
"""
        )
else:
    st.info("Upload a QR code image to verify your lettuce.")
