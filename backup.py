from flask import Flask, render_template, request
import requests
import json
import openai

app = Flask(__name__)

# Google Custom Search API settings
api_key = "AIzaSyCEI-BooRpFhxkomPJTlTLVmAwCZxf_wP0"
cse_id = "96b7b695dbdff498d"

# Function to reset chat history when the server restarts
def reset_chat_history():
    return []

# Initialize chat history
chat_history = reset_chat_history()

@app.route("/")
def index():
    return render_template("index.html", chat_history=chat_history)

@app.route("/send", methods=["POST"])
@app.route("/send", methods=["POST"])
@app.route("/send", methods=["POST"])
def send_message():
    user_input = request.form["user_input"]
    response = process_input(user_input)
    
    # Format user input
    formatted_user_input = f"You: {user_input}"
    
    # Format bot response
    formatted_bot_response = f"Chatbot: {response}"
    
    # Append the formatted messages to chat history
    chat_history.append({"user": formatted_user_input, "bot": formatted_bot_response})
    
    return render_template("index.html", chat_history=chat_history)

def process_input(user_input):
    # Standard responses for simple questions
    if user_input.lower() == "help":
        return "Sure! How can I assist you?"
    elif user_input.lower() in ["hi", "hello","Hi","Hello"]:
        return "Hello! How can I help you today?"
    elif user_input.lower() in ["how are you?","How Are You?","how are you","How Are You"]:
        return "Hey ! I am good , what about you"
    elif user_input.lower() in ["what is oms?"]:
        return "OMS can stand for order management system, which is a computer software system that automates the process of managing orders. It can help businesses manage, sell, and fulfill orders across multiple sales channels, both online and offline."

    # Check if the user is asking for the definition of OMS
    elif user_input.lower() == "what is oms?":

        # Use the Datamuse API to get the definition of OMS
        url = "https://api.datamuse.com/words"
        params = {
            "rel_jja": "oms"
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        # Extract the definition of OMS
        definition = None
        for item in data:
            if "defs" in item:
                definition = item["defs"][0]
                break
        
        # Return the definition of OMS along with search results
        if definition:
            # Fetch Google search results using Custom Search API
            url = f"https://www.googleapis.com/customsearch/v1"
            params = {
                "q": user_input,
                "cx": cse_id,
                "key": api_key
            }
            
            # Send the request and get the response
            response = requests.get(url, params=params)
            data = json.loads(response.text)
            
            # Extract the top 3 search results
            results = []
            for item in data["items"][:3]:
                results.append(f"**{item['title']}**\n{item['link']}")
            
            # Combine definition and search results into a formatted response
            return f"{definition}\n\nHere are the top 3 search results:\n\n{'\n\n'.join(results)}"
        else:
            return "I couldn't find a definition for OMS."
    
    else:
        # Set up the Google Custom Search API request
        url = f"https://www.googleapis.com/customsearch/v1"
        params = {
            "q": user_input,
            "cx": cse_id,
            "key": api_key
        }
        
        # Send the request and get the response
        response = requests.get(url, params=params)
        data = json.loads(response.text)
        
        # Extract the top 3 search results
        results = []
        for item in data["items"][:3]:
            results.append(f"**{item['title']}**\n{item['link']}")
        
        # Return a formatted response
        if results:
            return f"Here are the top 3 search results:\n\n{'\n\n'.join(results)}"
        else:
            return "No results found."

if __name__ == "__main__":
    app.run(debug=True)