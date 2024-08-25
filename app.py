from fastapi import FastAPI, Request
import uvicorn
import streamlit as st
import requests
import json
import asyncio

# Initialize FastAPI
app = FastAPI()

# FastAPI Endpoints
@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/bfhl")
async def get_operation_code():
    response = {
        "operation_code": 1
    }
    return response

@app.post("/process")
async def process_request(request: Request):
    # Get the request body
    body = await request.json()

    # Extract the required data from the request body
    user_id = body.get("user_id", "")
    college_email = body.get("college_email", "")
    college_roll_number = body.get("college_roll_number", "")
    numbers = body.get("numbers", [])
    alphabets = body.get("alphabets", [])

    # Find the highest lowercase alphabet
    lowercase_alphabets = [char for char in alphabets if char.islower()]
    highest_lowercase_alphabet = max(lowercase_alphabets) if lowercase_alphabets else ""

    # Prepare the response
    response = {
        "status": "success",
        "user_id": user_id,
        "college_email": college_email,
        "college_roll_number": college_roll_number,
        "numbers": numbers,
        "alphabets": alphabets,
        "highest_lowercase_alphabet": highest_lowercase_alphabet
    }

    return response

# Streamlit Application
def process_data(data):
    # Send a POST request to the FastAPI backend
    url = "http://localhost:8000/process"  # Use localhost for development; replace with cloud URL when deployed
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the response data
        response_data = response.json()
        return response_data
    else:
        return {"error": "Failed to process the data"}

def render_response(response_data, selected_option):
    if "error" in response_data:
        st.error(response_data["error"])
    else:
        st.success("Data processed successfully!")

        # Render the response based on the selected option
        if selected_option == "Alphabets & Numbers":
            if "alphabets_numbers" in response_data:
                result = response_data["alphabets_numbers"]
                st.write("Alphabets and Numbers:")
                for item in result:
                    st.write(f"- {item}")
            else:
                st.write("No data found for Alphabets and Numbers.")
        elif selected_option == "Symbols":
            if "symbols" in response_data:
                result = response_data["symbols"]
                st.write("Symbols:")
                for item in result:
                    st.write(f"- {item}")
            else:
                st.write("No data found for Symbols.")
        # Add more options as needed

def main():
    st.set_page_config(page_title="21BCE1310")

    # Set background color
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #D3D3D3;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Header
    st.header("Bajaj Finserv Health Challenge: By Preeti Modi")

    # Big Title
    st.markdown("<h1 style='text-align: center; color: yellow;'>21BCE1310</h1>", unsafe_allow_html=True)

    # Get user input
    input_data = st.text_area("Enter JSON data", placeholder='{"data": ["A", "C", "z"]}')

    # Create a dropdown for selecting the option
    options = ["Alphabets & Numbers", "Symbols"]
    selected_option = st.selectbox("Select an option", options)

    if st.button("Process Data"):
        # Parse the input JSON
        try:
            data = json.loads(input_data)
        except json.JSONDecodeError:
            st.error("Invalid JSON format")
            return

        # Process the data
        response = process_data(data)

        # Render the response based on the selected option
        render_response(response, selected_option)

# Run FastAPI and Streamlit together
def start_fastapi():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, server.run)

if __name__ == "__main__":
    # Start FastAPI in the background
    start_fastapi()
    
    # Run the Streamlit app
    main()
