# Rag with Link Application

## Overview

Rag with Link Application is a chat application built with Streamlit and LangChain. The app allows users to create and manage multiple chat sessions, each associated with a specific external link. The chat sessions leverage the OpenAI GPT-3.5-turbo model to provide intelligent responses based on the content of the provided link.

## Features

- **Multiple Chat Sessions**: Create and manage multiple chat sessions, each identified by a unique link.
- **Dynamic Link Handling**: The name of each chat session is automatically updated based on the provided link.
- **Sidebar Configuration**: Enter your OpenAI API key once in the sidebar and it will be used across all chat sessions.
- **Interactive Chat Interface**: Engage in a conversation with the AI, which uses the content from the provided link to respond intelligently.

## Requirements

- Python 3.11 or higher
- Streamlit
- LangChain
- OpenAI API Key

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/alessandro-mannolini/streamlit_rag.git
   cd streamlit_rag
    ```

2. **Create and activate a conda environments**
    ```bash
    conda create -n rag python=3.11
    conda activate rag
    ```

3. **Install the requirements.txt**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Set up your OpenAI API key:
 - In the Streamlit sidebar, enter your OpenAI API key. This key will be used for all chat sessions. The input will be hidden for security.

Create a new chat session:
 - Click the "Crea Nuova Chat" button in the sidebar to create a new chat session. You will be prompted to enter a link. The name of the chat session will be derived from the link.

Interact with the chat:
 - Once the link is processed, you can start typing your questions in the chat input box. The AI will use the content from the provided link to respond.

Manage multiple sessions:
 - You can switch between different chat sessions using the select box in the sidebar. Each session retains its conversation history and link context.

## File Structure

 - app.py: The main Streamlit application file.
 - rag.py: Contains the ChatRAG class which manages the interaction with the LangChain and OpenAI models.
 - requirements.txt: Lists the required Python packages.

## Contact

For any questions or suggestions, please open an issue or contact me at alessandro.mannolini@gmail.com.