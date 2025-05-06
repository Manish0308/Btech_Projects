# Import the necessary functions
from utils.atom_extractor import FFmpegExtractor, analyze_file
from utils.feature_engineering import generate_pathorder_tags

# Provide the path to your video file
video_path = "dataset/VideoSham/Original/103_unedited.mov"

# Call the analyze_file function
metadata_df, mediainfo_data = analyze_file(video_path)

# Now metadata_df holds the DataFrame with all the extracted metadata
print("Extracted Metadata DataFrame:")
print(metadata_df)

# If you want to save it as a CSV
output_csv_path = "results/output_metadata.csv"  # You can specify a custom path
metadata_df.to_csv(output_csv_path, index=False)
print(f"Metadata saved to: {output_csv_path}")

print(f"pathorder-tag :",generate_pathorder_tags(metadata_df))















# from utils.atom_extractor import analyze_file

# # Path to some small MP4 videos you have
# video_path_1 = "dataset/VideoSham/Original/102_unedited.mp4"
# # video_path_2 = "dataset/VideoSham/Original/101_unedited.mp4"

# # Analyze them
# atoms1, metadata1 = analyze_file(video_path_1)
# # atoms2, metadata2 = analyze_file(video_path_2)

# # Print important info for Video 1
# if 'atom_type' in atoms1.columns:
#     print("\nExtracted Atom Types Video 1:", atoms1['atom_type'].unique())
# else:
#     print("atom_type column not found in atoms1 DataFrame.")

# # Print metadata information for Video 1
# if 'General' in metadata1:
#     print("\nMetadata Video 1:")
#     print(f"Format: {metadata1['General'].get('format', 'Unknown')}")
#     print(f"Duration: {metadata1['General'].get('duration', 'Unknown')}")
#     print(f"File size: {metadata1['General'].get('file_size', 'Unknown')} bytes")
# else:
#     print("General metadata not found for Video 1.")

# Optionally, if you want to analyze and print metadata for the second video:
# if 'atom_type' in atoms2.columns:
#     print("\nExtracted Atom Types Video 2:", atoms2['atom_type'].unique())
# else:
#     print("atom_type column not found in atoms2 DataFrame.")
#
# if 'General' in metadata2:
#     print("\nMetadata Video 2:")
#     print(f"Format: {metadata2['General'].get('format', 'Unknown')}")
#     print(f"Duration: {metadata2['General'].get('duration', 'Unknown')}")
#     print(f"File size: {metadata2['General'].get('file_size', 'Unknown')} bytes")
# else:
#     print("General metadata not found for Video 2.")
