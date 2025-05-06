# import os
# import pandas as pd
# from hachoir.parser import createParser
# from hachoir.field import MissingField
# from pymediainfo import MediaInfo
# from collections import defaultdict

# class AtomExtractor:
#     def __init__(self, filepath):
#         """Initialize with the path to the media file."""
#         self.filepath = filepath
#         self.parser = createParser(filepath)
#         self.atoms = []
#         self.mediainfo = MediaInfo.parse(filepath)
        
#     def extract_atoms(self):
#         """Extract atom/box structure from the container format."""
#         if not self.parser:
#             raise ValueError(f"Cannot parse file: {self.filepath}")
        
#         # Process the root and recursively extract atoms
#         self._process_fields(self.parser.root, depth=0, parent=None)
#         return self.atoms
    
#     def _process_fields(self, field, depth=0, parent=None):
#         """Recursively process fields/atoms in the container."""
#         try:
#             for subfield in field:
#                 atom_info = {
#                     'atom_type': subfield.name,
#                     'size': getattr(subfield, 'size', 0) // 8,  # Convert from bits to bytes
#                     'offset': getattr(subfield, 'address', 0) // 8,  # Convert from bits to bytes
#                     'depth': depth,
#                     'parent': parent,
#                     'order': len(self.atoms) + 1
#                 }
                
#                 # Extract any available value
#                 try:
#                     if hasattr(subfield, 'value') and not isinstance(subfield.value, MissingField):
#                         atom_info['value'] = str(subfield.value)
#                     else:
#                         atom_info['value'] = None
#                 except Exception:
#                     atom_info['value'] = None
                
#                 self.atoms.append(atom_info)
                
#                 # Recursively process children
#                 if subfield.is_field_set:
#                     self._process_fields(subfield, depth+1, subfield.name)
#         except Exception as e:
#             print(f"Error processing field: {e}")
    
#     def get_mediainfo_data(self):
#         """Extract structured data from MediaInfo."""
#         result = defaultdict(dict)
        
#         for track in self.mediainfo.tracks:
#             track_type = track.track_type
            
#             for key, value in track.__dict__.items():
#                 if key.startswith('_'):
#                     continue
#                 if value:
#                     result[track_type][key] = value
                    
#         return dict(result)
    
#     def to_dataframe(self):
#         """Convert atom data to pandas DataFrame."""
#         atoms = self.extract_atoms()
#         return pd.DataFrame(atoms)
    
#     def save_to_csv(self, output_path=None):
#         """Save atom structure to CSV file."""
#         if output_path is None:
#             base = os.path.splitext(os.path.basename(self.filepath))[0]
#             output_path = f"{base}_atoms.csv"
            
#         df = self.to_dataframe()
#         df.to_csv(output_path, index=False)
#         return output_path

#     def check_tampering(self, reference_atoms_df):
#         """Compare the atom structure of this video with a reference to detect tampering."""
#         current_atoms_df = self.to_dataframe()
        
#         # Compare atom counts, types, or structure (basic comparison)
#         if current_atoms_df.equals(reference_atoms_df):
#             return "Video is original."
#         else:
#             # Detailed tampering check (based on metadata differences)
#             changes = current_atoms_df.merge(reference_atoms_df, indicator=True, how='outer')
#             tampered_atoms = changes[changes['_merge'] != 'both']
#             if not tampered_atoms.empty:
#                 return "Video is tampered or altered."
#             return "Video is original."

# def analyze_file(filepath):
#     """Analyze a media file and print summary information."""
#     extractor = AtomExtractor(filepath)
    
#     # Extract atoms
#     atoms_df = extractor.to_dataframe()
    
#     # Get MediaInfo data
#     mediainfo_data = extractor.get_mediainfo_data()
    
#     # Save atom structure to CSV
#     csv_path = extractor.save_to_csv()
    
#     print(f"Analyzed file: {filepath}")
#     print(f"Total atoms extracted: {len(atoms_df)}")
#     print(f"Top-level atoms: {', '.join(atoms_df[atoms_df['depth'] == 0]['atom_type'].unique())}")
#     print(f"Atom structure saved to: {csv_path}")
    
#     # Print some MediaInfo data
#     if 'General' in mediainfo_data:
#         print("\nGeneral Info:")
#         general = mediainfo_data['General']
#         print(f"Format: {general.get('format', 'Unknown')}")
#         print(f"Duration: {general.get('duration', 'Unknown')}")
#         print(f"File size: {general.get('file_size', 'Unknown')} bytes")
    
#     if 'Video' in mediainfo_data:
#         print("\nVideo Info:")
#         video = mediainfo_data['Video']
#         print(f"Codec: {video.get('codec', 'Unknown')}")
#         print(f"Resolution: {video.get('width', '?')}x{video.get('height', '?')}")
    
#     return atoms_df, mediainfo_data

# def upload_and_analyze_video(filepath, reference_filepath=None):
#     """Handle video file upload and analysis for tampering."""
#     atoms_df, _ = analyze_file(filepath)
    
#     if reference_filepath:
#         reference_extractor = AtomExtractor(reference_filepath)
#         reference_atoms_df = reference_extractor.to_dataframe()
        
#         tampering_status = AtomExtractor(filepath).check_tampering(reference_atoms_df)
#         print(f"Tampering status: {tampering_status}")
    
#     return atoms_df

# # Example usage
# # video_file_path = "path_to_video.mp4"
# # upload_and_analyze_video(video_file_path, reference_filepath="reference_video.mp4")








import os
import pandas as pd
import subprocess
from collections import defaultdict
from pymediainfo import MediaInfo

class FFmpegExtractor:
    def __init__(self, filepath):
        """Initialize with the path to the media file."""
        self.filepath = filepath
        self.mediainfo = MediaInfo.parse(filepath)
        
    def get_ffmpeg_metadata(self):
        """Extract video metadata using ffmpeg."""
        # Use ffmpeg to get detailed metadata information about the video
        command = [
            'ffmpeg', 
            '-i', self.filepath, 
            '-hide_banner'
        ]
        
        # Run the ffmpeg command and capture the output
        result = subprocess.run(command, stderr=subprocess.PIPE, text=True)
        metadata = result.stderr
        
        return metadata
    
    def extract_media_info(self):
        """Extract structured data from MediaInfo."""
        result = defaultdict(dict)
        
        for track in self.mediainfo.tracks:
            track_type = track.track_type
            
            for key, value in track.__dict__.items():
                if key.startswith('_'):
                    continue
                if value:
                    result[track_type][key] = value
                    
        return dict(result)
    
    # def to_dataframe(self):
    #     """Convert metadata data to pandas DataFrame."""
    #     # Convert the extracted metadata to DataFrame format
    #     metadata = self.get_ffmpeg_metadata()
    #     metadata_lines = metadata.split("\n")
        
    #     metadata_info = []
    #     for line in metadata_lines:
    #         if line.strip():  # Skip empty lines
    #             metadata_info.append(line.strip())
        
    #     return pd.DataFrame(metadata_info, columns=["Metadata"])

    def to_dataframe(self):
        """Convert metadata data to pandas DataFrame."""
        # Convert the extracted metadata to DataFrame format
        metadata = self.get_ffmpeg_metadata()
        metadata_lines = metadata.split("\n")
        
        metadata_info = []
        for idx, line in enumerate(metadata_lines):
            if line.strip():  # Skip empty lines
                # Capture metadata structure in columns
                metadata_info.append({
                    'Index': idx,
                    'Metadata': line.strip(),
                })
        
        # Create DataFrame with extracted metadata
        df = pd.DataFrame(metadata_info)
        
        # Add additional structured metadata (General, Video, etc.)
        mediainfo_data = self.extract_media_info()
        for section, section_data in mediainfo_data.items():
            for key, value in section_data.items():
                df.loc[len(df)] = {
                    'Index': len(df),
                    'Metadata': f"{section} - {key}: {value}",
                }
        
        return df
    def save_to_csv(self, output_path=None):
        """Save metadata to CSV file in the 'results' directory."""
        # Ensure the 'results' directory exists
        results_dir = 'results'
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        # Set default output file name
        if output_path is None:
            base = os.path.splitext(os.path.basename(self.filepath))[0]
            output_path = os.path.join(results_dir, f"{base}_metadata.csv")
        
        # Save metadata to CSV in the 'results' directory
        df = self.to_dataframe()
        df.to_csv(output_path, index=False)
        return output_path

    def check_tampering(self, reference_metadata_df):
        """Compare the metadata of this video with a reference to detect tampering."""
        current_metadata_df = self.to_dataframe()
        
        # Compare metadata changes (basic comparison)
        if current_metadata_df.equals(reference_metadata_df):
            return "Video is original."
        else:
            # Detailed tampering check (based on metadata differences)
            changes = current_metadata_df.merge(reference_metadata_df, indicator=True, how='outer')
            tampered_metadata = changes[changes['_merge'] != 'both']
            if not tampered_metadata.empty:
                return "Video is tampered or altered."
            return "Video is original."

def analyze_file(filepath):
    """Analyze a media file and print summary information."""
    extractor = FFmpegExtractor(filepath)
    
    # Extract metadata
    metadata_df = extractor.to_dataframe()
    
    # Get MediaInfo data
    mediainfo_data = extractor.extract_media_info()
    
    # Save metadata structure to CSV
    csv_path = extractor.save_to_csv()
    
    print(f"Analyzed file: {filepath}")
    print(f"Total metadata lines extracted: {len(metadata_df)}")
    print(f"Metadata saved to: {csv_path}")
    
    # Print some MediaInfo data
    if 'General' in mediainfo_data:
        print("\nGeneral Info:")
        general = mediainfo_data['General']
        print(f"Format: {general.get('format', 'Unknown')}")
        print(f"Duration: {general.get('duration', 'Unknown')}")
        print(f"File size: {general.get('file_size', 'Unknown')} bytes")
    
    if 'Video' in mediainfo_data:
        print("\nVideo Info:")
        video = mediainfo_data['Video']
        print(f"Codec: {video.get('codec', 'Unknown')}")
        print(f"Resolution: {video.get('width', '?')}x{video.get('height', '?')}")
    
    return metadata_df, mediainfo_data

def upload_and_analyze_video(filepath, reference_filepath=None):
    """Handle video file upload and analysis for tampering."""
    metadata_df, _ = analyze_file(filepath)
    
    if reference_filepath:
        reference_extractor = FFmpegExtractor(reference_filepath)
        reference_metadata_df = reference_extractor.to_dataframe()
        
        tampering_status = FFmpegExtractor(filepath).check_tampering(reference_metadata_df)
        print(f"Tampering status: {tampering_status}")
    
    return metadata_df

# Example usage
# video_file_path = "path_to_video.mp4"
# upload_and_analyze_video(video_file_path, reference_filepath="reference_video.mp4")
