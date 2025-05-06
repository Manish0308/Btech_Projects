# import subprocess
# import json

# def extract_metadata(video_path):
#     """
#     Extracts essential metadata from the video using ffprobe.
#     Returns a cleaned metadata dictionary for comparison.
#     """
#     cmd = [
#         "ffprobe",
#         "-v", "quiet",
#         "-print_format", "json",
#         "-show_format",
#         "-show_streams",
#         video_path
#     ]
#     result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     metadata = json.loads(result.stdout)

#     # Only keep essential, stable fields for comparison
#     cleaned_metadata = {
#         "format_name": metadata["format"].get("format_name", ""),
#         "duration": metadata["format"].get("duration", ""),
#         "bit_rate": metadata["format"].get("bit_rate", ""),
#         "nb_streams": metadata["format"].get("nb_streams", ""),
#     }

#     return cleaned_metadata

from pymediainfo import MediaInfo

def extract_metadata(video_path):
    """
    Extracts rich metadata from the video including device information
    using MediaInfo.
    Returns a cleaned metadata dictionary for comparison.
    """
    media_info = MediaInfo.parse(video_path)
    metadata = {}

    for track in media_info.tracks:
        if track.track_type == "General":
            metadata["format"] = track.format
            metadata["duration"] = track.duration
            metadata["file_size"] = track.file_size
            metadata["overall_bit_rate"] = track.overall_bit_rate
            metadata["encoded_date"] = track.encoded_date
            metadata["tagged_date"] = track.tagged_date
            metadata["device_make"] = getattr(track, "com_apple_quicktime_make", None)
            metadata["device_model"] = getattr(track, "com_apple_quicktime_model", None)
            metadata["software"] = getattr(track, "encoded_application", None)

    return metadata

