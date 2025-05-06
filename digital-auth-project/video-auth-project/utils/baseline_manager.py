import os
import re
import json
from utils.hash_util import generate_hash
from utils.metadata_util import extract_metadata
from utils.watermark_util import embed_watermark
from utils.watermark_util import extract_watermark



BASELINE_FILE = "baseline_data.json"

def store_video_baseline_data(video_path):
    filename = os.path.basename(video_path)

    id_match = re.search(r'\d+', filename)
    if not id_match:
        return "❌ Could not extract ID from filename."
    
    video_id = id_match.group(0).zfill(3)  # Always 3 digits, like '061'

    print(f"Processing original video: {filename} (ID: {video_id})")

    # 1. Generate hash
    video_hash = generate_hash(video_path)

    # 2. Extract metadata
    metadata = extract_metadata(video_path)

    # 3. Embed watermark and store watermark text
    watermark_text = f"VIDWM_{filename}"
    watermarked_path = f"results/wm_{filename}"
    embed_watermark(video_path, watermarked_path, watermark_text)

    # 4. Load existing baseline data safely
    data = {}
    if os.path.exists(BASELINE_FILE):
        try:
            with open(BASELINE_FILE, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Warning: baseline_data.json was empty or corrupted. Resetting...")

    # 5. Add or update this video's data using only ID as key
    data[video_id] = {
        "hash": video_hash,
        "metadata": metadata,
        "watermark": watermark_text
    }

    # 6. Save updated data back safely
    with open(BASELINE_FILE, "w") as f:
        json.dump(data, f, indent=4)

    return f"✅ Successfully stored/updated baseline data for Video ID: {video_id}"


# BASELINE_FILE = "baseline_data.json"

# import re

# import os
# import json
# import re
# from utils.hash_utils import generate_hash
# from utils.metadata_util import extract_metadata
# from utils.watermark_util import extract_watermark

BASELINE_FILE = "baseline_data.json"

# def analyze_video_against_baseline(video_path):
#     filename = os.path.basename(video_path)

#     if not os.path.exists(BASELINE_FILE):
#         return "❌ No baseline data found. Please store baseline for original videos first."

#     with open(BASELINE_FILE, "r") as f:
#         data = json.load(f)

#     # 🛠 Extract ID like '061' or '123'
#     id_match = re.search(r'\d+', filename)
#     if not id_match:
#         return "❌ Invalid filename format. Could not extract video ID."

#     video_id = id_match.group(0).zfill(3)  # Always 3-digit string

#     if video_id not in data:
#         return f"❌ No baseline found for video ID {video_id}. Please store the original version first."

#     # Fetch baseline data using clean ID
#     stored_hash = data[video_id]["hash"]
#     stored_metadata = data[video_id]["metadata"]
#     stored_watermark = data[video_id]["watermark"]

#     # Compute current video data
#     current_hash = generate_hash(video_path)
#     current_metadata = extract_metadata(video_path)
#     extracted_watermark = extract_watermark(video_path)

#     # Compare results
#     hash_match = stored_hash == current_hash
#     metadata_match = stored_metadata == current_metadata
#     watermark_match = stored_watermark == extracted_watermark

#     result = f"🔍 Analyzing {filename} against baseline ID {video_id}...\n"
#     result += f"\nHash Match: {'✅' if hash_match else '❌'}"
#     result += f"\nMetadata Match: {'✅' if metadata_match else '❌'}"
#     result += f"\nWatermark Match: {'✅' if watermark_match else '❌'}"

#     if hash_match and metadata_match and watermark_match:
#         result += "\n\n🟢 Result: Video is AUTHENTIC (No tampering detected)"
#     else:
#         result += "\n\n🔴 Result: Video may be TAMPERED (Differences detected)"

#     return result


BASELINE_FILE = "baseline_data.json"

def analyze_video_against_baseline(video_path):
    filename = os.path.basename(video_path)

    if not os.path.exists(BASELINE_FILE):
        return "❌ No baseline data found. Please store baseline for original videos first."

    with open(BASELINE_FILE, "r") as f:
        data = json.load(f)

    # 🛠 Extract ID like '061' or '123'
    id_match = re.search(r'\d+', filename)
    if not id_match:
        return "❌ Invalid filename format. Could not extract video ID."

    video_id = id_match.group(0).zfill(3)  # Always 3-digit string

    if video_id not in data:
        return f"❌ No baseline found for video ID {video_id}. Please store the original version first."

    # Fetch baseline data using clean ID
    stored_hash = data[video_id]["hash"]
    stored_metadata = data[video_id]["metadata"]
    stored_watermark = data[video_id]["watermark"]

    # Compute current video data
    current_hash = generate_hash(video_path)
    current_metadata = extract_metadata(video_path)
    extracted_watermark = extract_watermark(video_path)

    # Compare results
    hash_match = stored_hash == current_hash
    metadata_match = stored_metadata == current_metadata
    watermark_match = stored_watermark == extracted_watermark

    # 🎯 Additional device mismatch check
    device_mismatch = False
    if (stored_metadata.get("device_make") and current_metadata.get("device_make")) and \
       (stored_metadata.get("device_make") != current_metadata.get("device_make")):
        device_mismatch = True
    if (stored_metadata.get("device_model") and current_metadata.get("device_model")) and \
       (stored_metadata.get("device_model") != current_metadata.get("device_model")):
        device_mismatch = True

    # Build result
    result = f"🔍 Analyzing {filename} against baseline ID {video_id}...\n"
    result += f"\nHash Match: {'✅' if hash_match else '❌'}"
    result += f"\nMetadata Match: {'✅' if metadata_match else '❌'}"
    result += f"\nWatermark Match: {'✅' if watermark_match else '❌'}"

    if device_mismatch:
        result += "\nDevice Match: ❌ (Device mismatch detected!)"
    else:
        result += "\nDevice Match: ✅ (Device matches)"

    if hash_match and metadata_match and watermark_match and not device_mismatch:
        result += "\n\n🟢 Result: Video is AUTHENTIC (No tampering detected)"
    else:
        result += "\n\n🔴 Result: Video may be TAMPERED (Differences detected)"

    return result
