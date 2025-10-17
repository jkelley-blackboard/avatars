
# 📦 Avatar Packaging Scripts

These scripts automate the creation of `.zip` packages containing avatar images for upload, using a list of user identifiers. Each avatar is placed in a uniquely named folder and added to a zip archive. Batches are created to keep zip file sizes manageable.

---

## 📁 Input File Format

The input file must be named `list.csv` and use a **pipe (`|`) delimiter** with the following structure:

```
PK1|username
_123_1|jdoe
_456_1|asmith
...
```

- **PK1**: Unique identifier used to name the folder (e.g., `_123_1`)
- **username**: Used to name the image file (e.g., `jdoe.jpg`)

---

## 🐍 Python Script (`avatar_packager.py`)

### ✅ Requirements
- Python 3.6+
- Standard libraries only (`os`, `csv`, `shutil`, `zipfile`)

### 🔧 Configuration
- `data_file`: Path to the input CSV file (`list.csv`)
- `image_dir`: Path to the source image directory (currently unused; uses `sample.jpg`)
- `ext`: Image file extension (default `.jpg`)
- `batch_size`: Number of avatars per zip file

### 🚀 How It Works
1. Reads `list.csv` line by line.
2. Creates a folder named `user<PK1>`.
3. Copies a placeholder image (`sample.jpg`) into the folder, named `<username>.jpg`.
4. Adds the folder to a zip archive (`avatars.zip`).
5. After every `batch_size` entries, renames the zip to `avatars_batch_<n>.zip` and starts a new one.
6. Finalizes the last batch after the loop ends.

### 🏁 Run It
```bash
python avatar_packager.py
```

---

## 💻 PowerShell Script (`avatar_packager.ps1`)

### ✅ Requirements
- Windows PowerShell 5.0+
- `Compress-Archive` cmdlet (built-in)

### 🔧 Configuration
- `$dataFile`: Path to the input CSV file (`list.csv`)
- `$imageDir`: Path to the source image directory (currently unused; uses `sample.jpg`)
- `$ext`: Image file extension (default `.jpg`)
- `$batchsize`: Number of avatars per zip file

### 🚀 How It Works
1. Imports `list.csv` using `|` delimiter.
2. Creates a folder named `user<PK1>`.
3. Copies a placeholder image (`sample.jpg`) into the folder, named `<username>.jpg`.
4. Adds the folder to a zip archive (`avatars.zip`) using `Compress-Archive -Update`.
5. After every `$batchsize` entries, renames the zip to `avatars_batch_<n>.zip` and starts a new one.
6. Finalizes the last batch after the loop ends.

### 🏁 Run It
```powershell
.vatar_packager.ps1
```

---

## 📌 Notes
- Both scripts use a placeholder image (`sample.jpg`). Replace this with actual image logic if needed.
- Ensure `sample.jpg` exists in the working directory or update the path accordingly.
- Output zip files will be named `avatars_batch_1.zip`, `avatars_batch_2.zip`, etc.
