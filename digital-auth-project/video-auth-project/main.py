import os
import json
import argparse
from utils.metadata_util import extract_metadata
from utils.hash_utils import compute_hash
from utils.watermark_util import embed_watermark, verify_watermark

BASELINE_DIR = "baselines"
ORIGINAL_DIR = "dataset/VideoSham/original"
VERIFY_DIR = "dataset/VideoSham/tampered"  # Can be changed to any test directory
BASELINE_FILE = os.path.join(BASELINE_DIR, "baseline_data.json")
WATERMARK_TEXT_TEMPLATE = "auth:manish|id:{id}|ts:20250424"

os.makedirs(BASELINE_DIR, exist_ok=True)

def store_video_baseline_data():
    baseline_data = {}

    for filename in os.listdir(ORIGINAL_DIR):
        if filename.endswith("_unedited.mp4"):
            video_id = filename.split("_")[0].zfill(4)
            video_path = os.path.join(ORIGINAL_DIR, filename)

            print(f"Storing data for: {filename}")

            metadata = extract_metadata(video_path)
            video_hash = compute_hash(video_path)
            watermark_text = WATERMARK_TEXT_TEMPLATE.format(id=video_id)

            wm_output_path = os.path.join(BASELINE_DIR, f"wm_{filename}")
            embed_watermark(video_path, wm_output_path, watermark_text)

            baseline_data[filename] = {
                "hash": video_hash,
                "metadata": metadata,
                "watermark_text": watermark_text
            }

    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline_data, f, indent=2)
    
    print("✅ Baseline data stored in:", BASELINE_FILE)


def analyze_video_against_baseline():
    if not os.path.exists(BASELINE_FILE):
        print("❌ Baseline data not found.")
        return

    with open(BASELINE_FILE, "r") as f:
        baseline_data = json.load(f)

    results = {}

    for filename in os.listdir(VERIFY_DIR):
        if filename.endswith(".mp4"):
            original_name = filename.replace("processed", "unedited")
            original_baseline = baseline_data.get(original_name)

            if not original_baseline:
                print(f"⚠️ No baseline for {original_name}")
                continue

            test_path = os.path.join(VERIFY_DIR, filename)
            print(f"Verifying: {filename}")

            test_hash = compute_hash(test_path)
            test_metadata = extract_metadata(test_path)
            watermark_valid = verify_watermark(test_path, original_baseline["watermark_text"])

            results[filename] = {
                "hash_match": test_hash == original_baseline["hash"],
                "metadata_match": test_metadata == original_baseline["metadata"],
                "watermark_valid": watermark_valid
            }

    with open("results/verification_report.json", "w") as f:
        json.dump(results, f, indent=2)

    print("✅ Verification complete. Report saved to results/verification_report.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video Authentication System")
    parser.add_argument("mode", choices=["store", "verify"], help="Choose mode: 'store' or 'verify'")
    args = parser.parse_args()

    if args.mode == "store":
        store_video_baseline_data()
    elif args.mode == "verify":
        analyze_video_against_baseline()
