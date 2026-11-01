# Birthday Surprise Website — Backend Media Version

## Important: no upload controls on the webpage
This version does NOT ask visitors to upload photos or videos. Media is read from the `photos/` and `videos/` folders included in this project.

## Where to add photos
1. Extract the ZIP file.
2. Open the extracted project folder.
3. Open the `photos` folder.
4. Copy your five photos into it (JPG, JPEG, PNG, or WEBP).
5. Name them in the order you want, for example:
   - `01_photo.jpg`
   - `02_photo.jpg`
   - `03_photo.jpg`
   - `04_photo.jpg`
   - `05_photo.jpg`

The app sorts filenames alphabetically and uses the first five photos. Each photo appears on its own slide.

## Where to add videos
1. Open the `videos` folder.
2. Copy your five videos into it (MP4, WEBM, or MOV).
3. Name them in the order you want, for example:
   - `01_video.mp4`
   - `02_video.mp4`
   - `03_video.mp4`
   - `04_video.mp4`
   - `05_video.mp4`

Each video appears on its own slide, autoplays muted, loops continuously, and has no visible play/pause controls. H.264 MP4 is recommended.

## How to write the memory captions
Open `birthday_data.json` in VS Code or Notepad.

- Edit `photo_captions` for the five photo slide descriptions.
- Edit `video_captions` for the five video slide descriptions.

Keep the order of the captions aligned with the alphabetically sorted filenames in each folder.

## Run the website
Open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Other customisation
You can edit `name`, `sender`, `letter_greeting`, `letter_text`, `letter_signoff`, and `balloon_words` in `birthday_data.json`.

## Notes
- If fewer than five files are present, the remaining slides show placeholders.
- Media stays in the project folders; no need to upload again when opening the website.
- Large videos increase the project size and can take longer to load.
