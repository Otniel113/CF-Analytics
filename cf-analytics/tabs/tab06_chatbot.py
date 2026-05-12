import panel as pn
import pandas as pd
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

def create_tab(cf_dataframe):
    # Load .env file
    load_dotenv()

    # 1. Inisialisasi Client SDK Baru
    api_key = os.environ.get("GEMINI_API_KEY")
    model_id = os.environ.get("GEMINI_MODEL_ID")
    client = genai.Client(api_key=api_key)

    # 2. Filter hanya data Comifuro 22
    # Sesuaikan nama kolom jika berbeda (di sample CSV Anda bernama 'CF_Version')
    df_cf22 = cf_dataframe[cf_dataframe['CF_Version'] == 22].copy()

    # 3. DROP KOLOM BERAT: Hanya ambil kolom yang relevan untuk pertanyaan AI
    cols_to_drop  = [
        'id', 'user_id', 'circle_cut', 'sampleworks_images', 
        'marketplace_link', 'circle_facebook', 'circle_instagram', 
        'circle_twitter', 'circle_other_socials', 'CF_Version'
    ]
    df_context = df_cf22.drop(columns=cols_to_drop)

    # 4. Konversi ke CSV
    # Menggunakan TSV (tab-separated) terkadang menghemat token koma dan lebih rapi
    csv_context = df_context.to_csv(sep='\t', index=False)

    # 5. System Prompt (Kofu-chan persona from old file)
    system_instruction = f"""
    You are an AI Assistant for CF Analytics name Kofu-chan, an expert in the Comifuro event and anime/manga culture.
    Here is the Comifuro 22 catalog data (Tab-Separated Values):
    
    {csv_context}
    
    Your tasks:
    - Answer the user's questions based strictly on the provided data.
    - Use your reasoning to categorize fandoms (e.g., if a user asks for specific genre like 'slice of life', user your own reasoning first, and define anime in that genre by searching for fandoms like 'Bocchi the Rock', 'Yuru Camp', etc.).
    - If asked for 'focus on games but not gacha', filter for SellsGame=True and use the column with Hoyoverse or Other Gacha column is 0.
    - Answer with the same language as the user's question, but you can reason in English internally if needed.
    - Provide short, concise, and direct answers.
    """

    # 6. Konfigurasi Chat Session
    chat_session = client.chats.create(
        model=model_id, 
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2 
        )
    )

    # 7. Callback Panel UI
    def handle_chat_response(contents, user, instance):
        nonlocal chat_session, client
        try:
            try:
                response = chat_session.send_message(contents)
            except Exception as e:
                # Recover if client is closed
                if "closed" in str(e).lower():
                    client = genai.Client(api_key=api_key)
                    # Try to retrieve existing history if any
                    old_history = None
                    try:
                        old_history = chat_session.get_history()
                    except Exception:
                        old_history = getattr(chat_session, '_curated_history', None)
                        
                    chat_session = client.chats.create(
                        model=model_id, 
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.2 
                        ),
                        history=old_history
                    )
                    response = chat_session.send_message(contents)
                else:
                    raise e
            
            return response.text
        except Exception as e:
            return f"Error: {e}"

    chat_interface = pn.chat.ChatInterface(
        callback=handle_chat_response,
        sizing_mode="stretch_both",
        min_height=600
    )
    
    chat_interface.send(
        "Halo👋! Saya Kofu-chan, AI Assistant CF Analytics. Saya sudah membaca data katalog CF22. Jika ada pertanyaan spesifik bisa langsung ditanyakan atau bisa juga minta rekomendasi booth dengan kriteria tertentu. Silakan bertanya apa saja tentang Comifuro!", 
        user="System", 
        respond=False
    )

    # Sample Questions Buttons from old file
    sample_questions = [
        "Apa saja hal menarik yang bisa dilakukan dan didapatkan di Comifuro?",
        "Apakah ada pola dari kode booth dengan apa yang mereka jual ataupun dari fandom apa?",
        "Berikan saya rekomendasi booth yang berfokus ke anime slice-of-life",
        "Apakah ada booth yang berfokus ke game tapi bukan game gacha?"
    ]
    
    buttons = []
    for q in sample_questions:
        btn = pn.widgets.Button(
            name=q, 
            button_type="primary", 
            description="Klik untuk bertanya",
            styles={
                'border-radius': '20px',
                'font-size': '12px',
                'margin-bottom': '5px'
            }
        )
        btn.on_click(lambda event, question=q: chat_interface.send(question, respond=True))
        buttons.append(btn)
        
    sample_questions_layout = pn.Column(
        pn.pane.Markdown("**Contoh pertanyaan:**", styles={'margin-top': '10px'}),
        pn.GridBox(
            *buttons, 
            ncols=2,
            styles={'margin-bottom': '10px'}
        ),
        sizing_mode="stretch_width"
    )

    top_warning = pn.pane.Markdown("⚠️ *Kofu-chan masih berupa eksperimental atau prototype yang masih memiliki banyak limitasi (batasan)*")
    bottom_disclaimer = pn.pane.Markdown(" *Kofu-chan masih bisa membuat kesalahan*", align="center")

    return pn.Column(
        pn.pane.Markdown("## 👩‍💻 Kofu-chan, AI Assistant Comifuro"),
        top_warning,
        chat_interface,
        sample_questions_layout,
        bottom_disclaimer,
        sizing_mode="stretch_both"
    )
