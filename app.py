import streamlit as st
from txtai.pipeline import Summary
from PyPDF2 import PdfReader

st.set_page_config(layout="wide")

@st.cache_resource
def summary_text(text):
    summary = Summary()
    text = (text)
    result = summary(text)
    return result

def extract_text_from_pdf(file_path, page_num):
    with open(file_path, 'rb') as f:
        reader = PdfReader(f)
        if page_num < 0 or page_num >= len(reader.pages):
            st.error(f"Invalid page number. Please choose a page between 0 and {len(reader.pages)}")
            return None
        page = reader.pages[page_num]
        text = page.extract_text()
    return text

choice = st.sidebar.selectbox("Select Your Choice", ["Summarize Text", "Summarize Document"])

if choice == "Summarize Text":
    st.subheader("Summarize Text")
    input_text = st.text_area("Enter your text here...")
    if input_text is not None:
        if st.button("Summarize Text"):
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown("***Your Input Text ***")
                st.info(input_text)
            with col2:
                result = summary_text(input_text)
                st.markdown("***Your Summary ***")
                st.success(result)

elif choice == "Summarize Document":
    st.subheader("Summarize Document")
    input_doc = st.file_uploader("Upload your document here...", type = ['pdf'])
    if input_doc is not None:
        num_pages = st.sidebar.selectbox("Select Page", range(1, len(PdfReader(input_doc).pages) + 1 ))
        if st.button("Summarize Document"):
            with open("doc_file.pdf", "wb") as f:
                f.write(input_doc.getbuffer())
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown("***Extracted Text From Document (Page {})***".format(num_pages))
                extracted_text = extract_text_from_pdf("doc_file.pdf", num_pages - 1)
                st.info(extracted_text)
            with col2:
                result = extract_text_from_pdf("doc_file.pdf", num_pages - 1)
                st.markdown("***Your Summary ***")
                summary_result = summary_text(result)
                st.success(summary_result)