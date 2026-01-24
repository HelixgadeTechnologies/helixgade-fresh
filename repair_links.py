import os
import re

def repair_links(directory):
    # Get all media files and their extensions
    media_files = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.gif', '.jpg', '.jpeg', '.png', '.webp')):
                base = os.path.splitext(file)[0]
                rel_path = os.path.relpath(os.path.join(root, file), directory)
                if base not in media_files:
                    media_files[base] = []
                media_files[base].append(file)

    # Process HTML files
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()

                # Find all .webp references
                webp_refs = re.findall(r'src="([^"]+\.webp)"', content)
                new_content = content
                for ref in webp_refs:
                    base = os.path.splitext(os.path.basename(ref))[0]
                    # Check if the .webp file actually exists
                    full_ref_path = os.path.join(os.path.dirname(filepath), ref)
                    if not os.path.exists(full_ref_path):
                        # Try to find a fallback
                        potential_matches = media_files.get(base, [])
                        original = next((m for m in potential_matches if not m.endswith('.webp')), None)
                        if original:
                            new_ref = ref.replace('.webp', os.path.splitext(original)[1])
                            new_content = new_content.replace(ref, new_ref)
                            print(f"Repaired {ref} -> {new_ref} in {file}")

                if new_content != content:
                    with open(filepath, 'w') as f:
                        f.write(new_content)

if __name__ == "__main__":
    target_dir = "/Users/ayaosigodfrey/.gemini/antigravity/scratch/helixgade-fresh"
    repair_links(target_dir)
