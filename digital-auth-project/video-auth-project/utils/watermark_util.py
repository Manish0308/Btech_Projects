import cv2
import numpy as np

def text_to_bits(text):
    return ''.join([format(ord(c), '08b') for c in text])

def embed_watermark(video_path, output_path, watermark_text):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    wm_bits = text_to_bits(watermark_text)
    wm_len = len(wm_bits)

    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        return

    # 🛠 Safely flatten and copy frame
    flat = frame.reshape(-1).copy()

    if wm_len > len(flat):
        print("Error: Watermark too long for frame size.")
        return

    for i in range(wm_len):
        flat[i] = (int(flat[i]) & ~1) | int(wm_bits[i])  # Safely handle uint8

    watermarked_frame = flat.reshape(frame.shape)
    out.write(watermarked_frame)

    # Write rest of the video unmodified
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()
    print(f"✅ Watermark embedded in: {output_path}")




def bits_to_text(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join([chr(int(b, 2)) for b in chars if len(b) == 8])
def verify_watermark(video_path, watermark_text):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return False

    wm_bits = text_to_bits(watermark_text)
    wm_len = len(wm_bits)

    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        return False

    # 🛠 Flatten and copy frame for safe bit manipulation
    flat = frame.reshape(-1).copy()

    extracted_bits = []

    # Ensure the watermark length matches the frame size (safe extraction)
    if wm_len > len(flat):
        print("Error: Watermark length exceeds frame size.")
        return False

    # Extract the bits from the LSBs of pixels
    for i in range(wm_len):
        extracted_bits.append(str(flat[i] & 1))

    # Combine extracted bits to form a string
    extracted_watermark = ''.join(extracted_bits)
    
    # Convert extracted bits to text (ensure it matches the original watermark)
    extracted_text = ''.join([chr(int(extracted_watermark[i:i+8], 2)) for i in range(0, len(extracted_watermark), 8)])

    if extracted_text == watermark_text:
        print("✅ Valid watermark found.")
        return True
    else:
        print("❌ No valid watermark found.")
        return False

def extract_watermark(video_path, max_length=256):
    """
    Extracts watermark text from the first frame of a video.
    Assumes watermark was embedded using LSB on the first frame.
    max_length defines the maximum number of characters to extract.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return ""

    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        return ""

    flat = frame.reshape(-1)
    extracted_bits = []

    # 1 char = 8 bits → max bits = max_length * 8
    for i in range(max_length * 8):
        extracted_bits.append(str(flat[i] & 1))

    bits = ''.join(extracted_bits)
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    extracted_text = ''.join([chr(int(c, 2)) for c in chars if len(c) == 8])

    # Trim trailing garbage (nulls or invalids)
    extracted_text = extracted_text.strip("\x00").strip()

    print(f"🔍 Extracted watermark: {extracted_text}")
    return extracted_text

# import cv2
# import numpy as np

# def text_to_bits(text):
#     """Convert text to binary string with length prefix"""
#     length = format(len(text), '032b')  # 32-bit length prefix
#     bits = ''.join([format(ord(c), '08b') for c in text])
#     return length + bits

# def bits_to_text(bits):
#     """Convert binary string back to text"""
#     if len(bits) < 32:
#         return ""
#     length = int(bits[:32], 2)
#     chars = [bits[32+i*8:32+(i+1)*8] for i in range(length)]
#     return ''.join([chr(int(b, 2)) for b in chars if len(b) == 8])

# def embed_watermark(video_path, output_path, watermark_text):
#     cap = cv2.VideoCapture(video_path)
#     if not cap.isOpened():
#         print("Error: Could not open video.")
#         return False

#     # Get video properties
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
#     # Use lossless codec for testing (change to 'mp4v' for production)
#     fourcc = cv2.VideoWriter_fourcc(*'FFV1')  # Lossless codec
#     out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=True)

#     wm_bits = text_to_bits(watermark_text)
#     wm_len = len(wm_bits)
    
#     frame_count = 0
#     watermark_embedded = False

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
            
#         # Only embed in first frame for this example
#         if not watermark_embedded:
#             # Use blue channel only (channel 0) to minimize visual impact
#             channel = 0  
#             flat = frame[:,:,channel].reshape(-1)
            
#             if wm_len > len(flat):
#                 print(f"Error: Need {wm_len} pixels but frame has {len(flat)}")
#                 return False
                
#             # Embed watermark in LSBs
#             for i in range(wm_len):
#                 flat[i] = (flat[i] & 0xFE) | int(wm_bits[i])
                
#             frame[:,:,channel] = flat.reshape(frame.shape[:2])
#             watermark_embedded = True
            
#         out.write(frame)
#         frame_count += 1

#     cap.release()
#     out.release()
#     print(f"✅ Watermark embedded in {frame_count} frames: {output_path}")
#     return True

# def verify_watermark(video_path, expected_text=None):
#     cap = cv2.VideoCapture(video_path)
#     if not cap.isOpened():
#         print("Error: Could not open video.")
#         return False

#     ret, frame = cap.read()
#     if not ret:
#         print("Error: Could not read frame.")
#         return False

#     # Extract from blue channel (channel 0)
#     channel = 0
#     flat = frame[:,:,channel].reshape(-1)
    
#     # First read the length prefix (32 bits)
#     length_bits = ''.join([str(flat[i] & 1) for i in range(32)])
#     if not length_bits:
#         print("❌ No length prefix found")
#         return False
        
#     length = int(length_bits, 2)
#     total_bits = 32 + length * 8
    
#     if total_bits > len(flat):
#         print(f"❌ Watermark too long: {total_bits} > {len(flat)}")
#         return False
        
#     # Extract all bits
#     extracted_bits = ''.join([str(flat[i] & 1) for i in range(total_bits)])
#     extracted_text = bits_to_text(extracted_bits)
    
#     if expected_text:
#         if extracted_text == expected_text:
#             print(f"✅ Valid watermark found: '{extracted_text}'")
#             return True
#         else:
#             print(f"❌ Watermark mismatch. Expected '{expected_text}', got '{extracted_text}'")
#             return False
#     else:
#         print(f"ℹ️ Extracted watermark: '{extracted_text}'")
#         return extracted_text

