import streamlit as st
import logging
import time
from pathlib import Path
from faq import ingest_faq_data, faq_chain
from sql import sql_chain
from router import router  # Import router instance instead of SemanticRouter class

# Set page configuration
st.set_page_config(
    page_title="E-Commerce Chatbot",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for a more modern chat interface
st.markdown("""
<style>
/* Main container styling */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Chat header styling */
.chat-header {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.chat-header h1 {
    margin-left: 1rem;
    margin-bottom: 0;
    color: #2c3e50;
    font-size: 1.8rem;
}

/* Chat message styling */
.stChatMessage {
    padding: 1rem;
    border-radius: 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
}

/* User message styling */
.stChatMessage[data-testid*="user"] {
    background-color: #e3f2fd !important;
    border-bottom-right-radius: 0.2rem !important;
}

/* Assistant message styling */
.stChatMessage[data-testid*="assistant"] {
    background-color: #f0f4f8 !important;
    border-bottom-left-radius: 0.2rem !important;
}

/* Avatar styling */
.stChatMessageAvatar {
    background-color: #ffffff !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Input area styling */
.stChatInputContainer {
    padding: 0.5rem;
    border-radius: 0.5rem;
    background-color: #f8f9fa;
    box-shadow: 0 -2px 5px rgba(0,0,0,0.05);
}

/* Sidebar styling */
.css-1d391kg, .css-1lcbmhc {  /* Sidebar classes */
    background-color: #f8f9fa;
}

/* Button styling */
button[kind="primary"] {
    background-color: #4285f4;
    border-radius: 0.5rem;
}

/* Expander styling */
.streamlit-expanderHeader {
    background-color: #f0f4f8;
    border-radius: 0.5rem;
    padding: 0.5rem;
}

/* Link styling */
a {
    color: #4285f4;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# Add sidebar content
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3050/3050525.png", width=100)
    st.title("E-Commerce Chatbot")
    st.markdown("---")
    
    st.subheader("About")
    st.markdown(
        """
        E-Commerce Chatbot is your one-stop shop for all your shopping needs. 
        Our AI assistant can help you find products, answer questions, 
        and provide support.
        """
    )
    
    st.markdown("---")
    
    st.subheader("Quick Links")
    st.markdown(
        """
        - [Browse Categories](#)
        - [Today's Deals](#)
        - [Your Orders](#)
        - [Customer Service](#)
        """
    )
    
    st.markdown("---")
    
    # Add a clear chat button
    if st.button("Clear Chat", key="clear_chat"):
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 Hi there! I'm your E-Commerce Chatbot. I can help you with:\n* Finding products in our store\n* Answering questions about our policies\n* Tracking your orders\n* Processing returns\n\nHow can I help you today?"}
        ]
        st.rerun()

# Load FAQ data
faqs_path = Path(__file__).parent / "resources/faq_data.csv"
ingest_faq_data(faqs_path)


def ask(query):
    route_result = router(query)
    route = route_result.name if route_result else None
    
    # Log the route and confidence for debugging
    print(f"Query: {query}")
    print(f"Route: {route}")
    if route_result and hasattr(route_result, 'confidence'):
        print(f"Confidence: {route_result.confidence}")
    
    if route == 'faq':
        return faq_chain(query)
    elif route == 'sql':
        return sql_chain(query)
    elif route is None:
        # If no route is matched, default to SQL for product queries
        return sql_chain(query)
    else:
        return f"Route {route} not implemented yet"

# Create main content area with columns
col1, col2 = st.columns([3, 1])

with col1:
    # Create a header with logo and title
    st.markdown(
        """
        <div class="chat-header">
            <img src="https://cdn-icons-png.flaticon.com/512/3050/3050525.png" alt="E-Commerce Chatbot" width="50">
            <h1>E-Commerce Chatbot</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    # Add a container for example queries
    with st.expander("Example Queries", expanded=True):
        st.markdown(
            """
            Try asking:
            - What is your return policy?
            - Show me Nike shoes under Rs 3000
            - Do you offer cash on delivery?
            - Find running shoes with high ratings
            - How can I track my order?
            """
        )

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "👋 Hi there! I'm your E-Commerce Chatbot. I can help you with:\n* Finding products in our store\n* Answering questions about our policies\n* Tracking your orders\n* Processing returns\n\nHow can I help you today?"}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🛒"):
        st.markdown(message["content"])

# Accept user input
query = st.chat_input("Ask me anything about our products or policies...")

# Process the query and generate a response
if query:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    
    # Display user message in chat message container
    with st.chat_message("user", avatar="👤"):
        st.markdown(query)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar="🛒"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Get response from the assistant
        response = ask(query)
        
        # Simulate typing effect
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})


