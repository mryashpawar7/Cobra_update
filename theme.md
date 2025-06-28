# Universal Extractor Theme

## Welcome Messages

### Login Prompt
```
🔹 <b>𝐏𝐑𝐎 𝐄𝐗𝐓𝐑𝐀𝐂𝐓𝐎𝐑 🫵</b> 🔹

Send **ID & Password** in this format: <code>ID*Password</code>

Example:
- ID*Pass: <code>6969696969*password123</code>
- Token: <code>eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...</code>
```

### Login Success
```
✅ <b>{app_name} Login Successful</b>

🆔 <b>Credentials:</b> <code>{credentials}</code>

📚 <b>Available Batches</b>

{batch_list}
```

### Batch Format
```
<code>{batch_id}</code> - <b>{batch_name}</b> 💰 ₹{price}
```

## Progress Messages

### Initialization
```
🔄 <b>Processing Large Batch</b>
├─ Subject: {current}/{total}
└─ Current: <code>{topic_name}</code>
```

### Processing Update
```
📦 <b>Large Batch Progress</b>
├─ Completed: {current}/{total} subjects
├─ Total Links: {total_links}
├─ Time: {elapsed_time}
└─ ETA: {estimated_time}
```

### Content Processing
```
🔄 <b>Processing Large Batch</b>
├─ Subject: {current}/{total}
├─ Name: <code>{subject_name}</code>
├─ Topics: {processed}/{total}
├─ Links: {total_links}
├─ Time: {elapsed_time}
└─ ETA: {estimated_time}
```

### Completion
```
✅ <b>Extraction completed successfully!</b>

📊 𝗙𝗶𝗻𝗮𝗹 𝗦𝘁𝗮𝘁𝘂𝘀:
📚 Processed {total} items
📤 File has been uploaded

Thank you for using 𝐏𝐑𝐎 𝐄𝐗𝐓𝐑𝐀𝐂𝐓𝐎𝐑 🫵! 🌟
```

## Document Formatting

### File Caption
```
🎓 <b>COURSE EXTRACTED</b> 🎓

📱 <b>APP:</b> {app_name}
📚 <b>BATCH:</b> {batch_name} (ID: {batch_id})
⏱ <b>EXTRACTION TIME:</b> {duration}
📅 <b>DATE:</b> {date} IST

📊 <b>CONTENT STATS</b>
├─ 📁 Total Links: {total_links}
├─ 🎬 Videos: {video_count}
├─ 📄 PDFs: {pdf_count}
├─ 🖼 Images: {image_count}
├─ 📑 Documents: {doc_count}
├─ 📦 Others: {other_count}
└─ 🔐 Protected: {drm_count}

🚀 <b>Extracted by</b>: @{bot_username}

<code>╾───•𝐏𝐑𝐎 𝐄𝐗𝐓𝐑𝐀𝐂𝐓𝐎𝐑 🫵 •───╼</code>
```

## Error Messages

### Login Failed
```
❌ <b>Login Failed</b>

Error: {error_message}

Please check your credentials and try again.
```

### Extraction Error
```
❌ <b>An error occurred during extraction</b>

Error details: <code>{error_message}</code>

Please try again or contact support.
```

### Invalid Input
```
❌ <b>Invalid format!</b>

Please send ID and password in this format: <code>ID*Password</code>
```

### Progress Updates
```
💾 Creating file with extracted URLs...
📤 Uploading file with extracted links...
``` 
