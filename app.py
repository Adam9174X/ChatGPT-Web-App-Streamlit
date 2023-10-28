import openai
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="ChatGPT Plus", page_icon="Photos/GPT-4.png", layout="wide")  # Set the layout to wide

st.markdown("""
<style>
.css-1dp5vir {
    background-image: none; 
}

.sidebar {
    background-color: #202123;
    width: 260px;
}

.css-vk3wp9 {
    background: transparent;
}

.css-1nm2qww {
    color: #fff;
}
            
div.stButton > button:first-child {
    background-color: transparent;
    color: #fff;
    width: 225px;
    height: 37px;
    border-radius: 5px;
    border: 1px solid white;
    top: 30px;
    outline: none;
}
            
div.stButton > button:first-child:hover {
    background-color: rgba(255, 255, 255, 0.1);
    color: #fff;
    border: 1px solid white;
}

div.stButton > button:first-child:active {
    background-color: rgba(255, 255, 255, 0.1);
    color: #fff;
    border: 1px solid white;
}

div.stButton > button:first-child:not(:active) {
    color: #fff;
    border: 1px solid white;
}

.logo{ 
    font-family: Arial, sans-serif;
    color: #000;
}
            
.plus{
    background-color: #ffdd00;
    color: #fff;
    border-radius: 5px;
    font-size: 30px;
}

.stChatFloatingInputContainer {
    position: fixed;
    magirn-left: 0;
    magrin-right: 0px;
    magrin-bottom: 0;
    magrin-top: 0;
    right: 350px;
    bottom: -20px;
}

.stChatInputContainer {
    background-color: #ffffff;
    border: 5px solid #fff;
    color: #000;
    box-shadow: 0 0 8px 0 rgba(0, 0, 0, 0.25);
    height: 50px;
    width: 595px;
    outline: none;
}

.st-bf {
    border: none;
    width: 595px;
    height: 50px;
}

.css-1ezpuiy {
    background-color: transparent;
}

.css-1ywhr4r, .css-14o3ued, .css-1hq24vn {
    position: absolute;
    right: 0;
    left: -55px;
    bottom: 0;
    top: -1px;
    width: 39px;
    height: 39px;
}

.st-d0 {
    border: 5px solid #fff;
}

</style>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
    
# Sidebar
if st.sidebar.button('&nbsp;&nbsp;+&nbsp;&nbsp;&nbsp;New Chat&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'):
    st.session_state.messages = []
    st.session_state.show_label = True  # Set a session state variable to show the label

#st.sidebar.markdown('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-moon-fill" viewBox="0 0 16 16"><path d="M6 .278a.768.768 0 0 1 .08.858 7.208 7.208 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277.527 0 1.04-.055 1.533-.16a.787.787 0 0 1 .81.316.733.733 0 0 1-.031.893A8.349 8.349 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.752.752 0 0 1 6 .278z"/></svg>&nbsp;&nbsp;&nbsp;Dark Mode',
                #    unsafe_allow_html=True)

model_values = {
    "GPT-3.5": {"value": "gpt-3.5-turbo", "avatar": "Photos/GPT-3.5.png"},
    "GPT-4": {"value": "gpt-4", "avatar": "Photos/GPT-4.png"}
}

selected_option = option_menu(
    menu_title=None,
    options=["GPT-3.5", "GPT-4"],
    icons=["lightning-fill", "stars"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "height": "50px",
            "width": "300px",
            "display": "flex",
            "justify-content": "center",
            "align-items": "center",
        },
        "icon": { 
            "color" : "#19c37d",
        },
        "nav-link": {
            "height": "40px",
            "width": "130px",
        },
        "nav-link-selected": {
            "background-color": "#ffffff",
            "color": "#202123",
            "font-weight": "normal",
        },
    },
    
)

openai.api_key = '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'
    
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = model_values["GPT-3.5"]["value"]  # Set default model

# Check if the selected model has changed, and clear messages if it has
if st.session_state.get("openai_model", "") != model_values[selected_option]["value"]:
    st.session_state["openai_model"] = model_values[selected_option]["value"]
    st.session_state.messages = []
    st.session_state.show_label = True

# Update the selected model in session state
selected_model = st.session_state["openai_model"]

# Check if the label should be shown and display it accordingly
if st.session_state.get("show_label", True):
    st.markdown("<br><br><br><br><br><center><h1 class='logo'>ChatGPT <span class='plus'>Plus</span></h1></center>", unsafe_allow_html=True)

for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message.get("avatar")):
            st.markdown(message["content"])

if prompt := st.chat_input("Send a Message..."):
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "Photos/User.png"})
    with st.chat_message("user", avatar="Photos/User.png"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=model_values[selected_option]["avatar"]):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response, "avatar": model_values[selected_option]["avatar"]})

# Hide the label after the message is sent
st.session_state.show_label = False

