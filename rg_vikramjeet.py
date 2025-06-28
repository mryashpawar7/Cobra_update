import requests
import json
import cloudscraper
from pyrogram import filters
from Extractor import app
import os
import asyncio
import aiohttp
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode
from bs4 import BeautifulSoup
from config import CHANNEL_ID

log_channel = CHANNEL_ID

def decrypt(enc):
    enc = b64decode(enc.split(':')[0])
    key = '638udh3829162018'.encode('utf-8')
    iv = 'fedcba9876543210'.encode('utf-8')
    if len(enc) == 0:
        return ""

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(enc), AES.block_size)
    return plaintext.decode('utf-8')

def decode_base64(encoded_str):
    try:
        decoded_bytes = base64.b64decode(encoded_str)
        decoded_str = decoded_bytes.decode('utf-8')
        return decoded_str
    except Exception as e:
        return f"Error decoding string: {e}"

async def fetch(session, api, course_id, item, headers, f):
    fi = item.get("id")
    t = item.get("Title")
    async with session.get(f"https://{api}/get/fetchVideoDetailsById?course_id={course_id}&folder_wise_course=1&ytflag=0&video_id={fi}", headers=headers) as response:
        r4 = await response.json()
        vt = r4["data"].get("Title", "")
        vl = r4["data"].get("download_link", "")
        if vl:
            dvl = decrypt(vl)
            print(f"{vt}:{dvl}")
            f.write(f"{vt}:{dvl}\n")
        else:
            encrypted_links = r4["data"].get("encrypted_links", [])
            for link in encrypted_links:
                a = link.get("path")
                k = link.get("key")
                if a and k:
                    k1 = decrypt(k)
                    k2 = decode_base64(k1)
                    da = decrypt(a)
                    print(f"{vt}:{da}*{k2}")
                    f.write(f"{vt}:{da}*{k2}\n")
                    break
        if "material_type" in r4["data"]:
            mt = r4["data"]["material_type"]
            if mt == "VIDEO":
                p1 = r4["data"].get("pdf_link", "")
                p2 = r4["data"].get("pdf_link2", "")
                if p1:
                    dp1 = decrypt(p1)
                    print(f"{vt}:{dp1}")
                    f.write(f"{vt}:{dp1}\n")
                if p2:
                    dp2 = decrypt(p2)
                    print(f"{vt}:{dp2}")
                    f.write(f"{vt}:{dp2}\n")

async def fetch_folder_contents(session, api, course_id, folder_id, headers, f):
    async with session.get(f"https://{api}/get/folder_contentsv2?course_id={course_id}&parent_id={folder_id}", headers=headers) as response:
        j = await response.json()
        tasks = []
        if "data" in j:
            for item in j["data"]:
                mt = item.get("material_type")
                tasks.append(fetch_item_details(session, api, course_id, item, headers, f))
                if mt == "FOLDER":
                    tasks.append(fetch_folder_contents(session, api, course_id, item["id"], headers, f))
        await asyncio.gather(*tasks)

async def rgvikram_txt(app, message, api, name):
    api_base = api if api.startswith(("http://", "https://")) else f"https://{api}"
    
    editable11 = await app.send_message(message.chat.id, "Send Id*password or Token")
    input1 = await app.listen(editable11.chat.id)
    raw_text = input1.text
    await input1.delete(True)
    await editable11.delete(True)
    
    if '*' in raw_text:

        raw_url = f"{api_base}/post/userLogin"
        hdr = {
            "Auth-Key": "appxapi",
            "User-Id": "-2",
            "Authorization": "",
            "User_app_category": "",
            "Language": "en",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "okhttp/4.9.1"
        }
        info = {"email": raw_text.split("*")[0], "password": raw_text.split("*")[1]}
        print(info)
        
        try:
            response = requests.post(raw_url, data=info, headers=hdr).json()
            userid = response["data"]["userid"]
            token = response["data"]["token"]
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return await message.reply_text("Please try again later. Maybe Password Wrong")

        hdr1 = {
            "Client-Service": "Appx",
            "source": "website",
            "Auth-Key": "appxapi",
            "Authorization": token,
            "User-ID": userid
        }
        await message.reply_text("**Login Successful✅**")
    else:
        # Login using token
        token = raw_text
        hdr1 = {
            "Client-Service": "Appx",
            "source": "website",
            "Auth-Key": "appxapi",
            "Authorization": token,
            "User-ID": ""
        }
        await message.reply_text("**Login with Token Successful✅**")
    
    try:
        mc1 = requests.get(f"{api_base}/get/get_all_purchases?userid={hdr1['User-ID']}&item_type=10", headers=hdr1).json()
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        return await message.reply_text("Error decoding response from server. Please try again later.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return await message.reply_text("An error occurred while fetching your courses. Please try again later.")
    
    FFF = "𝗕𝗔𝗧𝗖𝗛 𝗜𝗗 ➤ 𝗕𝗔𝗧𝗖𝗛 𝗡𝗔𝗠𝗘\n\n"
    
    if "data" in mc1 and mc1["data"]:
        for i in mc1["data"]:
            for ct in i["coursedt"]:
                ci = ct.get("id")
                cn = ct.get("course_name")
                FFF += f"**`{ci}`   -   `{cn}`**\n\n"
    else:
        try:
            mc2 = requests.get(f"{api_base}/get/mycourseweb?userid={hdr1['User-ID']}", headers=hdr1).json()
            if "data" in mc2 and mc2["data"]:
                for i in mc2["data"]:
                    ci = i.get("id")
                    cn = i.get("course_name")
                    FFF += f"**`{ci}`   -   `{cn}`**\n\n"
            else:
                await message.reply_text("No course found in ID")
                return
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {str(e)}")
            return await message.reply_text("Error decoding response from server. Please try again later.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return await message.reply_text("An error occurred while fetching your courses. Please try again later.")

    editable1 = await message.reply_text(f"𝗔𝗽𝗽𝘅 𝗟𝗼𝗴𝗶𝗻 𝗦𝘂𝗰𝗲𝘀𝘀✅\n\n`{token}`\n{FFF}")
    
    editable2 = await app.send_message(message.chat.id, "**Now send the Course ID to Download**")
    input2 = await app.listen(editable2.chat.id)
    raw_text2 = input2.text
    await editable1.delete(True)
    await editable2.delete(True)
    await input2.delete(True)
    
    try:
        r = requests.get(f"{api_base}/get/course_by_id?id={raw_text2}", headers=hdr1).json()
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        return await message.reply_text("Error decoding response from server. Please try again later.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return await message.reply_text("An error occurred while fetching the course details. Please try again later.")

    for i in r.get("data", []):
        txtn = i.get("course_name")
        filename = f"{raw_text2}_{txtn.replace(':', '_').replace('/', '_')}.txt"

        if '/' in filename:
            filename1 = filename.replace("/", "").replace(" ", "_")
        else:
            filename1 = filename

        async with aiohttp.ClientSession() as session:
            with open(filename1, 'w') as f:
                try:
                    r1 = await fetch(session, f"{api_base}/get/allsubjectfrmlivecourseclass?courseid={raw_text2}&start=-1", hdr1)
                    tasks = []
                    for i in r1.get("data", []):
                        si = i.get("subjectid")
                        sn = i.get("subject_name")
                        r2 = await fetch(session, f"{api_base}/get/alltopicfrmlivecourseclass?courseid={raw_text2}&subjectid={si}&start=-1", hdr1)
                        for i in r2.get("data", []):
                            ti = i.get("topicid")
                            tn = i.get("topic_name")
                            tasks.append(handle_course(session, api_base, raw_text2, si, ti, hdr1, f))
                    await asyncio.gather(*tasks)
                except Exception as e:
                    print(f"An error occurred while processing the course: {str(e)}")
                    return await message.reply_text("An error occurred while processing the course. Please try again later.")
        
        try:
            await app.send_document(message.chat.id, filename1)
            await app.send_document(log_channel,   filename1=f"{selected_course_name}.txt",)
        except Exception as e:
            print(f"An error occurred while sending the document: {str(e)}")
            await message.reply_text("An error occurred while sending the document. Please try again later.")
        finally:
            if os.path.exists(filename1):
                os.remove(filename1)
                
