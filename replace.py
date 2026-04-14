import os
import sys

# Common text/code file extensions
TEXT_EXTENSIONS = {
    ".txt", ".html", ".htm", ".css", ".js", ".json", ".xml",
    ".md", ".py", ".java", ".c", ".cpp", ".h", ".hpp",
    ".cs", ".php", ".rb", ".go", ".rs", ".sh", ".bat",
    ".yml", ".yaml", ".ini", ".cfg", ".conf"
}

def log(msg):
    print(msg)

def is_text_file(filepath):
    _, ext = os.path.splitext(filepath)
    if ext.lower() in TEXT_EXTENSIONS:
        return True

    # Fallback: check for binary content
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(1024)
            if b"\x00" in chunk:
                return False
    except:
        return False

    return True

def process_file(filepath, target, replacement):
    if not is_text_file(filepath):
        log(f"[SKIP TYPE] {filepath}")
        return False

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except:
        log(f"[SKIP READ] {filepath}")
        return False

    if target in content:
        new_content = content.replace(target, replacement)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            log(f"[WRITE] Replaced in: {filepath}")
            return True
        except:
            log(f"[ERROR WRITE] {filepath}")
            return False
    else:
        log(f"[NO MATCH] {filepath}")
        return False

def collect_files(directory):
    file_list = []
    log("[SCAN] Walking directory tree (skipping hidden folders)...")
    
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        log(f"[DIR] {root} ({len(files)} files)")
        
        for file in files:
            file_list.append(os.path.join(root, file))

    return file_list

def print_progress(current, total):
    percent = (current / total) * 100 if total else 100
    bar_length = 30
    filled = int(bar_length * current // total) if total else bar_length
    bar = "#" * filled + "-" * (bar_length - filled)
    sys.stdout.write(f"\r[PROGRESS] |{bar}| {current}/{total} ({percent:.1f}%)")
    sys.stdout.flush()

if __name__ == "__main__":
    print("=== Insta Replace (Safe Text Mode) ===\n")

    target = input("What text do you want to replace? ").strip()
    replacement = input("Replace it with what? ").strip()

    if not target:
        print("Error: You must enter text to replace.")
        exit()

    current_dir = os.getcwd()
    log(f"\n[START] Directory: {current_dir}")

    files = collect_files(current_dir)
    total_files = len(files)

    log(f"[INFO] Total files found: {total_files}\n")

    replaced_count = 0

    for i, filepath in enumerate(files, start=1):
        print_progress(i, total_files)
        if process_file(filepath, target, replacement):
            replaced_count += 1

    print()
    log("\n=== Summary ===")
    log(f"Files scanned: {total_files}")
    log(f"Files modified: {replaced_count}")
    log("Done.")