# Import necessary modules
import streamlit as st
import streamlit.components.v1 as components  # For embedding custom HTML
import requests
from bs4 import BeautifulSoup
from generate_knowledge_graph import generate_knowledge_graph

# Set up Streamlit page configuration
st.set_page_config(
    page_icon=None, 
    layout="wide",  # Use wide layout for better graph display
    initial_sidebar_state="auto", 
    menu_items=None
)

# Set the title of the app
st.title("Knowledge Graph From Text")

# Sidebar section for user input method
st.sidebar.title("Input document")
input_method = st.sidebar.radio(
    "Choose an input method:",
    ["Upload txt", "Input text", "Input URL"],  # Added URL option
)

# Case 1: User chooses to upload a .txt file
if input_method == "Upload txt":
    # File uploader widget in the sidebar
    uploaded_file = st.sidebar.file_uploader(label="Upload file", type=["txt"])
    
    if uploaded_file is not None:
        # Read the uploaded file content and decode it as UTF-8 text
        text = uploaded_file.read().decode("utf-8")
 
        # Button to generate the knowledge graph
        if st.sidebar.button("Generate Knowledge Graph"):
            with st.spinner("Generating knowledge graph..."):
                # Call the function to generate the graph from the text
                net = generate_knowledge_graph(text)
                st.success("Knowledge graph generated successfully!")
                
                # Save the graph to an HTML file
                output_file = "knowledge_graph.html"
                net.save_graph(output_file) 

                # Open the HTML file and display it within the Streamlit app
                HtmlFile = open(output_file, 'r', encoding='utf-8')
                components.html(HtmlFile.read(), height=1000)

# Case 2: User chooses to directly input text
elif input_method == "Input text":
    # Text area for manual input
    text = st.sidebar.text_area("Input text", height=300)

    if text:  # Check if the text area is not empty
        if st.sidebar.button("Generate Knowledge Graph"):
            with st.spinner("Generating knowledge graph..."):
                # Call the function to generate the graph from the input text
                net = generate_knowledge_graph(text)
                st.success("Knowledge graph generated successfully!")
                
                # Save the graph to an HTML file
                output_file = "knowledge_graph.html"
                net.save_graph(output_file) 

                # Open the HTML file and display it within the Streamlit app
                HtmlFile = open(output_file, 'r', encoding='utf-8')
                components.html(HtmlFile.read(), height=1000)

# Case 3: User chooses to input a URL
else:
    # URL input field
    url = st.sidebar.text_input("Enter URL:")
    
    if url:  # Check if URL is provided
        if st.sidebar.button("Generate Knowledge Graph"):
            with st.spinner("Fetching and processing URL..."):
                try:
                    # Fetch the webpage content
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                    response = requests.get(url, headers=headers, timeout=10)
                    response.raise_for_status()
                    
                    # Parse and sanitize HTML content
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()
                    
                    # Extract text content
                    text = soup.get_text()
                    
                    # Clean up whitespace
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text = ' '.join(chunk for chunk in chunks if chunk)
                    
                    if text:
                        # Call the function to generate the graph from the URL content
                        net = generate_knowledge_graph(text)
                        st.success("Knowledge graph generated successfully!")
                        
                        # Save the graph to an HTML file
                        output_file = "knowledge_graph.html"
                        net.save_graph(output_file) 

                        # Open the HTML file and display it within the Streamlit app
                        HtmlFile = open(output_file, 'r', encoding='utf-8')
                        components.html(HtmlFile.read(), height=1000)
                    else:
                        st.error("No text content found at the provided URL.")
                        
                except requests.exceptions.RequestException as e:
                    st.error(f"Error fetching URL: {str(e)}")
                except Exception as e:
                    st.error(f"Error processing content: {str(e)}")