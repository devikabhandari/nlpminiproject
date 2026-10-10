# -*- coding: utf-8 -*-
"""
Author:
    lprtk

Description:
    This script is part of a project called SmartTextSummarizer, realized as part of 
    an introduction course to Linux and Git / GitHub. The project allows to set up 
    a secure webapp with a functionality allowing to summarize a text file according 
    to a number of sentence. Specifically, this file contains the layout of the webapp.

License:
    MIT License
"""

#--------------------------------- PACKAGES ----------------------------------
from html import escape
from io import BytesIO
import sys
from pathlib import Path

from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "backend" / "src_functionality"))

import app_function

import hash_function

from PIL import Image

import sgbd

import streamlit as st

from sqlite3 import connect

#--------------------------------- FUNCTIONS ---------------------------------
def uploaded_text(uploaded_file) -> str:
    if uploaded_file.name.lower().endswith(".docx"):
        document = Document(BytesIO(uploaded_file.getvalue()))
        paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
        table_text = [cell.text for table in document.tables for row in table.rows for cell in row.cells if cell.text.strip()]
        return "\n".join(paragraphs + table_text)
    return uploaded_file.getvalue().decode("utf-8-sig")


def word_document_bytes(text: str) -> bytes:
    document = Document()
    document.add_paragraph(text)
    output = BytesIO()
    document.save(output)
    return output.getvalue()


def pdf_document_bytes(text: str) -> bytes:
    output = BytesIO()
    document = SimpleDocTemplate(
        output,
        pagesize=letter,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=inch,
        bottomMargin=inch,
    )
    styles = getSampleStyleSheet()
    story = [Paragraph("SmartTextSummarizer Summary", styles["Title"]), Spacer(1, 0.2 * inch)]
    for line in text.splitlines() or [""]:
        safe_line = escape(line).encode("cp1252", errors="replace").decode("cp1252")
        story.append(Paragraph(safe_line or "&nbsp;", styles["BodyText"]))
        story.append(Spacer(1, 0.08 * inch))
    document.build(story)
    return output.getvalue()


    # App
def main() -> None:
    """
    This method allows to launch the webapp by calling modules defined with the 
    functionalities necessary for the functioning of the application.

    Returns
    -------
    None.

    """
    #---------------------------------- SQLITE 3 -----------------------------
        # Connection to MogoDB database
    conn = connect("data.db", check_same_thread=False)
    c = conn.cursor()
    
    #------------------------------- PAGE SETTINGS ---------------------------
    image = Image.open(PROJECT_ROOT / "image" / "logoAI.png")
    
    st.set_page_config(
         page_title="DPV presents SmartTextSummarizer",
         page_icon=image,
         layout="wide",
         initial_sidebar_state="expanded",
         menu_items={
             "Get help": "https://github.com/lprtk/text-summarizer",
             "Report a bug": "https://github.com/lprtk/text-summarizer/issues",
             "About": "Hi, welcome on my App! If you have a bug or anythings that which prevents you from use the functionalities of the App, please report it to my GitHub page."
         }
    )
    
    #------------------------------- DESIGN / CODE ---------------------------
    col1, col2 = st.columns([1, 2])
    col1.image(image, width=190)
    col2.subheader(
        "DPV presents"
        )
    col2.caption("AI-Powered Text Summarization Using Natural Language Processing")
    
    st.markdown(
        """
        <h1 style='text-align: center'>
            <font color='#FFFFFF'>
                SmartTextSummarizer
            </font>
        </h1>
        """, True
        )
    
    st.markdown(
        """
        <h2 style='font-family: Arial'>
            <font color='#FFFFFF'>
                Welcome to SmartTextSummarizer
            </font>
        </h2>
        """, True
        )
    
    st.markdown(
        """
        <h4 style='text-align: justify'>
            <font color= '#FFFFFF'>
                Have a long article or document to read? Paste your text, choose your preferred summary length and summarization method, and generate a concise summary in seconds.
            </font>
        </h4>
        """, True
        )
    
    st.markdown("<br/>", True)
    
    st.markdown(
        """
        <h4 style='text-align: center'>
            <font color='#FFFFFF'>
                Designed to make long-form reading more efficient
            </font>
        </h4>
        """, True
        )
    
    col1, col2, col3 = st.columns(3)
    col1.markdown("### Quick Text Summarization")
    col2.markdown("### Extractive and Abstractive Methods")
    col3.markdown("### Adjustable Summary Length")
    
    st.markdown("<br/>", True)
    
    #-------------------------------- APP CONTENT ----------------------------
    menu = ["Home", "LogIn", "SignUp"]
    
    st.sidebar.markdown(
        """
        <h4>
            <font color='#FFFFFF'>
                Connexion 🔒
            </font>
        </h4>
        """, True
        )
    
    choice = st.sidebar.selectbox("Menu", menu)
    
    col1, col2, col3 = st.columns(3)
    
    if choice == "Home":
        st.markdown(
            """
            <h2 style='font-family: Arial'>
                <font color='#FFFFFF'>
                    Home
                </font>
            </h2>
            """, True
            )
    
        st.markdown(
            """
            <h4>
                <font color='#FFFFFF'>
                    About the App 🔎
                </font>
            </h4>
            """, True
            )
        
        with st.expander("About"):
            st.markdown(
                """
                <p>
                    <font color='#FFFFFF'>
                        SmartTextSummarizer helps you turn long text into a concise summary. Log in, upload a text file, select a summary length and download the result.
                    </font>
                </p>
                """, True
                )
                
        with st.sidebar:
            st.info(
                """
                ☝ Please use the menu above to authenticate yourself before using the App.
                """
                )
    
    elif choice == "LogIn":
        st.markdown(
            """
            <h2 style='font-family: Arial'>
                <font color='#FFFFFF'>
                    LogIn Section 🔐
                </font>
            </h2>
            """, True
            )
        
        with st.sidebar:
            # User ID
            user = st.empty()
            username = user.text_input("User Name", key=1)
            
            # User passeword
            pswd = st.sidebar.empty()
            password = pswd.text_input("Password", type="password", key=2)
            
            # Callback
            col1, col2, col3 = st.columns(3)
            
            loggedin_check = col1.checkbox(label="LogIn", 
                                           key="LoggedIn")
            
            if not loggedin_check:
                forgotten_check = col3.checkbox(label="Forgot password", 
                                                key="ForgottenCheck")
                
                if forgotten_check:
                    st.markdown("<br/>", True)
                    
                    st.markdown(
                        """
                        <h3 style='font-family: Arial'>
                            <font color='#FFFFFF'>
                                Forgot your password 🔏
                            </font>
                        </h3>
                        """, True
                        )
                    
                    # Call function
                    app_function.forgot_password()
        
        if loggedin_check:
            # ID verification
            sgbd.create_usertable()
            hashed_pswd = hash_function.make_hashes(password)
            result = sgbd.login_user(username, hash_function.check_hashes(password, hashed_pswd))
            
            if result:
                st.success(f"✔️ Hi {username}, you have successfully Logged In!")
                
                # Reset text area
                username = user.text_input("User Name", value="", key=3)
                password = pswd.text_input("Password", value="", key=4)
                
                #-------------------------------------------------------------
                # App content
                
                st.markdown("<br/>", True)
                
                st.markdown(
                    """------------------------------------------------------------""", True
                    )
                
                
                st.markdown(
                    """
                    <h2 style='font-family: Arial'>
                        <font color='#FFFFFF'>
                            How to use the application's functionalities:
                        </font>
                    </h2>
                    <ol>
                        <li>Paste text or upload a .txt or Word (.docx) file to summarize.</li>
                        <li>Select the length of the summary that SmartTextSummarizer should make.
                        <li>Download your data: you just have to click on the button to download the summary of your text.</li>
                    </ol>
                    """, True
                    )
                
                st.markdown("<br/>", True)
                
                st.markdown(
                    """
                    <h3 style='font-family: Arial'>
                        <font color='#FFFFFF'>
                            1. Add text or upload a document
                        </font>
                    </h3>
                    """, True
                    )
                st.caption("Paste up to 500 words, or upload a .txt or Word (.docx) document.")
                input_type = st.radio("Input type", ["Paste text", "Upload a document"], horizontal=True)
                data = ""
                source_name = "summary"

                if input_type == "Paste text":
                    data = st.text_area(
                        "Text to summarize (maximum 500 words)",
                        height=180,
                        placeholder="Paste your text here...",
                    )
                    word_count = len(data.split())
                    st.caption(f"{word_count}/500 words")
                    if word_count > 500:
                        st.error("Please shorten the pasted text to 500 words or fewer.")
                        data = ""
                else:
                    upload_file = st.file_uploader(
                        "Choose a .txt or Word (.docx) file",
                        type=["txt", "docx"],
                    )
                    if upload_file:
                        st.write("● Filename: ", upload_file.name)
                        st.write("● File type: ", upload_file.type or "Unknown")
                        st.write("● File size: ", upload_file.size)
                        source_name = Path(upload_file.name).stem
                        try:
                            data = uploaded_text(upload_file)
                        except Exception as error:
                            st.error(f"Could not read this document: {error}")

                if data.strip():
                    sentences = app_function.read_article(data)
                    length_file = len(sentences)
                    st.write("● Number of sentences:", length_file)
                    if length_file:
                        length = [str(index) for index in range(length_file + 1)]
                        st.markdown("### 2. Select a length for the summary")
                        length_choice = int(st.selectbox("Summary length (sentences)", length))

                        if length_choice > 0:
                            resumed_text = app_function.generate_summary(data, length_choice)
                            st.success("Summary ready")
                            st.text_area("Plain-text summary preview", value=resumed_text, height=180, disabled=True)
                            st.markdown("### 3. Download your summary")
                            docx_bytes = word_document_bytes(resumed_text)
                            pdf_bytes = pdf_document_bytes(resumed_text)
                            download_col1, download_col2 = st.columns(2)
                            download_col1.download_button(
                                "Download Word document",
                                data=docx_bytes,
                                file_name=f"{source_name}_summary.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            )
                            download_col2.download_button(
                                "Download PDF",
                                data=pdf_bytes,
                                file_name=f"{source_name}_summary.pdf",
                                mime="application/pdf",
                            )
                    else:
                        st.warning("No sentences were found in the supplied text.")
                    
                #-------------------------------------------------------------
                
                # LogOut configuration
                loggedout_check = col3.checkbox(label="LogOut", 
                                                key="LoggedOut",
                                                on_change=app_function.log_out)
                
                with st.sidebar:
                    st.sidebar.markdown("<br/>", True) 
                    col1, col2 = st.columns(2)
                
                    # Reset password configuration
                    resetpswd_check = col1.checkbox(label="Reset password", 
                                                    key="ResetPswd")
                
                with st.sidebar:
                    col1, col2 = st.columns(2)
                
                    # Delete account configuration
                    deleteaccount_check = col1.checkbox(label="Delete account", 
                                                        key="DeletedAccount")
                
                # LogOut process
                if loggedout_check:
                    st.warning("Disconnect, see you soon! 👋")
                    
                # Reset password process
                if resetpswd_check:
                    with st.sidebar:
                        st.markdown("<br/>", True)
                        
                        st.markdown(
                            """
                            <h3 style='font-family: Arial'>
                                <font color='#FFFFFF'>
                                    Reset your password 🔏
                                </font>
                            </h3>
                            """, True
                            )
                    
                        # Call function
                        app_function.reset_password()
                    
                # Delete account process
                if deleteaccount_check:
                    with st.sidebar:
                        st.markdown("<br/>", True)
                        
                        st.markdown(
                            """
                            <h3 style='font-family: Arial'>
                                <font color='#FFFFFF'>
                                    Delete your account 🔒
                                </font>
                            </h3>
                            """, True
                            )
    
                        # Call function
                        app_function.delete_account()
                    
            else:
                # Reset text area
                username = user.text_input("User Name", value="", key=20)
                password = pswd.text_input("Password", value="", key=21)
                
                # Information message
                st.error("❌ Incorrect Username/Password. Please retry.")
                
                with st.sidebar:
                    col1, col2, col3 = st.columns(3)
                    
                    # Callback
                    loggedin_retry = col3.checkbox(label="Retry", 
                                                   key="LoggedTry", 
                                                   on_change=app_function.log_error)
        else:
            st.info(
                """
                👈 Please use the menu in the left side to authenticate yourself before using the App.
                """
                )
    
    elif choice == "SignUp":
        st.markdown(
            """
            <h2 style='font-family: Arial'>
                <font color='#FFFFFF'>
                    Create New Account 👀
                </font>
            </h2>
            """, True
            )
    
        st.info(
            """
            Welcome on our App! 👋 You are not already register, create your account to use our analytics tools.
            """
            )
                
        new_user = st.text_input("User Name")
        question = st.selectbox("Question",["What is your favorite color?",
                                            "What was the name of your school?",
                                            "In which city did you grow up?"])
        answer = st.text_input("Answer")
        new_password = st.text_input("Password", type="password")
        
        st.sidebar.markdown(
            """
            <h4>
                <font color='#FFFFFF'>
                    About the App 🔎
                </font>
            </h4>
            """, True
            )
        
        with st.sidebar.expander("About"):
            st.markdown(
                """
                <p>
                    <font color='#FFFFFF'>
                        Do you want to quickly summarize a text? Use The 
                        SmartTextSummarizer helps you turn long text into a concise summary. Log in, upload a text file, select a summary length and download the result.
                    </font>
                </p>
                """, True
                )
        
        if st.button("SignUp"):
            sgbd.create_usertable()
            sgbd.add_userdata(new_user, hash_function.make_hashes(new_password), question, answer)
            st.success("✔️ You have successfully created a valid account!")
            st.info("Go to LogIn Menu to login. 🔐")
    
    #---------------------------------- SQLITE 3 -----------------------------
        # Close the database
    conn.commit()
    c.close()


if __name__ == '__main__':
	main()