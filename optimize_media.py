import os
from PIL import Image

def optimize_images(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.gif', '.jpg', '.jpeg', '.png')):
                filepath = os.path.join(root, file)
                try:
                    with Image.open(filepath) as img:
                        # Skip small files
                        if os.path.getsize(filepath) < 100 * 1024:
                            continue
                        
                        # Generate new filename
                        base = os.path.splitext(file)[0]
                        new_filename = f"{base}.webp"
                        new_filepath = os.path.join(root, new_filename)
                        
                        print(f"Optimizing {file}...")
                        
                        if file.lower().endswith('.gif'):
                            # Convert animated GIF to animated WebP
                            img.save(new_filepath, format='WEBP', save_all=True, quality=60, method=6)
                        else:
                            # Convert static image to WebP
                            img.save(new_filepath, format='WEBP', quality=75, method=6)
                        
                        print(f"Saved to {new_filename} (Size: {os.path.getsize(new_filepath)})")
                        
                except Exception as e:
                    print(f"Error processing {file}: {e}")

if __name__ == "__main__":
    target_dir = "/Users/ayaosigodfrey/.gemini/antigravity/scratch/helixgade-fresh/assets/img"
    optimize_images(target_dir)
