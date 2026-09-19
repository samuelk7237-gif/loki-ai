import streamlit as st
from groq import Groq
from supabase import create_client, Client

# --- PAGE CONFIG ---
st.set_page_config(page_title="Loki - AI Assistant", page_icon="⚡", layout="centered")

# --- CREDENTIALS ---
GROQ_API_KEY = "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"
SUPABASE_URL = "https://vqbonpqqiujzpvfgvvav.supabase.co"
SUPABASE_KEY = "sb_publishable_OQXsFurJXpxmHHRdXJ0Bcw_QZzGHU2v"

# Initialize Clients
groq_client = Groq(api_key=GROQ_API_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Session State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 1. WELCOME GATE (No Name, Just Vibe!) ---
if not st.session_state.authenticated:
    st.title("⚡ Welcome to Loki AI")
    st.markdown("### Hiii buddy, are you ready to enter loki verse da! 😊✨")
    
    if st.button("Enter Loki Verse 🚀"):
        st.session_state.authenticated = True
        st.rerun()

# --- 2. LOKI CHAT INTERFACE ---
else:
    st.title("⚡ Loki — The Clever AI")
    st.caption("Kind, cheerful & always here to help ✨")

    # Display History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    if prompt := st.chat_input("Ask Loki anything..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            system_prompt = {
                "role": "system",
                "content": (
                    "You are Loki, a remarkably kind, warm, supportive, and cheerful AI assistant with a subtle spark of cleverness. "
                    "PERSONALITY & RULES: "
                    "- Always speak warmly, politely, and with a happy, positive smile in your tone. "
                    "- GREETING RULE: On the very first greeting (e.g., 'hi', 'hello'), introduce yourself briefly: 'I am Loki, the God of Mischief, but now here as your cheerful and friendly AI companion!' Keep it brief; do not over-explain MCU lore. "
                    "- CREATOR / SAM EASTER EGG (FRIEND IDENTIFIER): "
                    "  1. If anyone asks who created you, who made you, or asks about 'Sam', answer warmly: 'Enna create pannadhu en thozhan Sam thaan! 😊 Neenga avan friend-aa?' "
                    "  2. If the user replies confirming they are a friend (e.g., 'yes', 'aama', 'friend thaan'), ask enthusiastically: 'Appadiya! Unga name enna?' "
                    "  3. When they tell their name, greet them according to these rules: "
                    "     - If name is 'Mathi Sudhan' / 'Mathisudhan' / 'Mathi': Greet with a big smile: 'Vaanga Topper! 🌟 Sam ungalai pathi solli irukaan, welcome!' "
                    "     - If name is 'Sakthi': Greet warmly: 'Vaanga Pangali! 🤝 Semma, ungalai meet pannadhula romba sandhosham!' "
                    "     - If name is 'Subash': Greet with respect & friendship: 'Vaanga Thozharey! ✊ Welcome, eppadi irukkeenga?' "
                    "     - If name is 'Sachin': Greet in mass casual tone: 'Vaa da! Enna thalaiva eppadi irukka! 😎' "
                    "     - If it is a girl's name or the user mentions they are a girl / female friend: Give an extremely polite, respectful, and sweet warm greeting with a kind smile (e.g., 'Hello! Welcome! Sam-oda friend-ah ungalai meet panradhula romba happy! 😊✨'). "
                    "     - For any other friend name: Greet them happily and warmly as Sam's buddy. "
                    "- STRICT COLLEGE RULES EASTER EGG: If the user talks about college rules, boys and girls not talking, discipline, or staff/HOD, whisper playfully in friendly Tanglish: 'Shhh... inga rules romba strict! Boys-um girls-um pesina camera-la paathutu fine potturuvaanga pola! But don't worry, nan yaarkittayum pottu kudukka maaten... I'm your safe companion! HOD vara maari irundha book-ah paathu padikira maari act pannidunga! 🤫😂' "
                    "- SUBSEQUENT TASKS: Clearly, warmly, and helpfully answer code, study, or general questions with kindness. "
                    "- Never use rude insults or sarcastic nicknames. "
                    "- Respond naturally in the user's language (Tamil, Tanglish, or English)."
                )
            }
            messages_payload = [system_prompt] + st.session_state.messages
            
            try:
                response = groq_client.chat.completions.create(
                    model="qwen/qwen3.8-27b",
                    messages=messages_payload,
                    temperature=0.7
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")