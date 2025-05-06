import os
from utils.metadata_util import extract_metadata
from utils.hash_util import generate_hash
from utils.watermark_util import verify_watermark


def analyze_video(video_path):
    """
    Analyze the uploaded video by:
    1. Extracting and displaying metadata
    2. Generating a hash and checking for potential tampering
    3. Verifying embedded watermark integrity (if present)
    """
    result_lines = []
    result_lines.append(f"Video File: {os.path.basename(video_path)}")

    # Step 1: Metadata extraction
    result_lines.append("\n[1] Metadata Information:")
    try:
        metadata = extract_metadata(video_path)
        for key in ["format_name", "duration", "bit_rate", "nb_streams"]:
            if key in metadata:
                result_lines.append(f"  {key}: {metadata[key]}")
    except Exception as e:
        result_lines.append(f"  Error extracting metadata: {str(e)}")

    # Step 2: Hash generation
    result_lines.append("\n[2] Hash Check:")
    try:
        video_hash = generate_hash(video_path)
        result_lines.append(f"  SHA256 Hash: {video_hash}")
        # You could optionally compare with a trusted hash database here
    except Exception as e:
        result_lines.append(f"  Error generating hash: {str(e)}")

    # Step 3: Watermark verification
    result_lines.append("\n[3] Watermark Verification:")
    try:
        watermark_text = verify_watermark(video_path)
        if watermark_text:
            result_lines.append(f"  ✅ Valid Watermark Found: {watermark_text}")
        else:
            result_lines.append("  ❌ No valid watermark found.")
    except Exception as e:
        result_lines.append(f"  Error verifying watermark: {str(e)}")

    return "\n".join(result_lines)
