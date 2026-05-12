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
            
            return {"user": "Kofu-chan", "avatar": "🌸", "object": response.text}
        except Exception as e:
            return {"user": "Kofu-chan", "avatar": "🌸", "object": f"Maaf Goshujin-sama, terjadi error: {e}"}

    chat_interface = pn.chat.ChatInterface(
        callback=handle_chat_response,
        sizing_mode="stretch_both",
        show_undo=False,
        show_rerun=False,
        show_clear=True,
        user="Goshujin-sama",
        avatar="👤"
    )
    
    chat_interface.send(
        "Halo👋! Saya Kofu-chan. Silakan bertanya apa saja tentang Comifuro!", 
        user="Kofu-chan", 
        avatar="🌸",
        respond=False
    )

    # Sample Questions Mapping: {Short Label: Full Question}
    sample_questions_map = {
        "Hal menarik di Comifuro?": "Apa saja hal menarik yang bisa dilakukan dan didapatkan di Comifuro?",
        "Pola kode booth & fandom?": "Apakah ada pola dari kode booth dengan apa yang mereka jual ataupun dari fandom apa?",
        "Rekomendasi anime slice-of-life": "Berikan saya rekomendasi booth yang berfokus ke anime slice-of-life",
        "Booth game non-gacha?": "Apakah ada booth yang berfokus ke game tapi bukan game gacha?"
    }
    
    def on_sample_click(event):
        sample_questions_layout.visible = False
        short_q = event.obj.name
        full_q = sample_questions_map.get(short_q, short_q)
        chat_interface.send(full_q, respond=True)

    buttons = []
    for short_q in sample_questions_map.keys():
        btn = pn.widgets.Button(
            name=short_q, 
            button_type="light",
            styles={
                'border-radius': '15px',
                'font-size': '10px',
                'border': '1px solid #007bff',
                'color': '#007bff'
            },
            sizing_mode="stretch_width"
        )
        btn.on_click(on_sample_click)
        buttons.append(btn)
        
    sample_questions_layout = pn.Column(
        pn.pane.Markdown("**Saran pertanyaan:**", styles={'margin': '5px 0 0 0', 'font-size': '11px', 'color': '#666'}),
        pn.GridBox(
            *buttons, 
            ncols=2,
            sizing_mode="stretch_width"
        ),
        sizing_mode="stretch_width",
        styles={'padding': '5px'}
    )

    # Watcher to handle visibility based on chat history
    def update_samples_visibility(event):
        if len(event.new) > 1:
            sample_questions_layout.visible = False
        else:
            sample_questions_layout.visible = True
    
    chat_interface.param.watch(update_samples_visibility, 'objects')

    top_warning = pn.pane.Markdown("⚠️ *Kofu-chan masih prototype dan memiliki limitasi*", styles={'font-size': '12px', 'color': '#888', 'margin': '0 10px'})
    bottom_disclaimer = pn.pane.Markdown("*Mungkin bisa memberikan jawaban yang salah*", align="center", styles={'font-size': '11px', 'color': '#aaa'})

    return pn.Column(
        top_warning,
        chat_interface,
        sample_questions_layout,
        bottom_disclaimer,
        sizing_mode="stretch_both"
    )
