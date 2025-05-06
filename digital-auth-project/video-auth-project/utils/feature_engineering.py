import pandas as pd

def generate_pathorder_tags(atom_df):
    """
    Generate PathOrder-Tag feature list from extracted atom DataFrame.
    Args:
        atom_df (pd.DataFrame): DataFrame containing extracted atoms.
    Returns:
        List[str]: List of PathOrder-Tag strings.
    """
    pathorder_tags = []

    for idx, row in atom_df.iterrows():
        depth = row.get('depth', 0)
        atom_type = row.get('atom_type', 'unknown')
        parent = row.get('parent', 'Root') or 'Root'  # In case parent is None
        order = row.get('order', idx + 1)  # If no explicit order, use DataFrame index + 1
        
        # 🛠 Build the path
        if depth == 0:
            path = f"Root/{atom_type}"  # Top level atoms
        else:
            path = f"{parent}/{atom_type}"
        
        # Combine path and order
        pathorder_tag = f"{path}@{order}"
        pathorder_tags.append(pathorder_tag)

    return pathorder_tags
