import glob

def remove_bom_from_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
            
        if content.startswith(b'\xef\xbb\xbf'):
            content = content[3:]
            with open(filepath, 'wb') as f:
                f.write(content)
            print(f"Removed BOM from {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    html_files = glob.glob('*.html')
    for f in html_files:
        remove_bom_from_file(f)
    print("Done removing BOMs.")
