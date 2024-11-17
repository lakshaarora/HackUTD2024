// Define chat_history as a global array to hold the chat history
let chat_history = [];

// Function to handle appending messages to chat interface page
function appendToHistory(message) {
    const chatWindow = document.getElementById('chat-window');
    // Create a message in the chat window (Both user and bot will appear here)
    chatWindow.innerHTML += `<p><strong>User:</strong> ${message}</p>`;
    // Append the message to the chat history array
    chat_history.push(`User: ${message}\n`);
    // Scroll to the bottom of the chat window
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Function to send a message and simulate bot responses
function sendMessage() {
    const userInput = document.getElementById('user-input').value;

    if (userInput.trim() !== "") {
        // Only append user message to chat history
        appendToHistory(userInput);

        // Show bot is typing ("...")
        const chatWindow = document.getElementById('chat-window');
        const botMessageElement = document.createElement('p');
        botMessageElement.innerHTML = `<strong>Bot:</strong> ...`;
        chatWindow.appendChild(botMessageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;

        // Clear input field after message is sent
        document.getElementById('user-input').value = '';
    }
}

function downloadChatHistory() {
    // Send chat history to the server for download
    fetch('/download_history', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ chat_history: chat_history })
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        } else {
            throw new Error('Failed to download chat history');
        }
    })
    .then(blob => {
        // Create a link to trigger the download
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'history.txt';
        link.click();
    })
    .catch(error => {
        console.error('Error downloading chat history:', error);
    });
}


$(document).ready(function() {
    // Function to handle the form submission
    async function handleSubmit() {
        const user_input = $('#user-input').val(); // Get user input
        if (user_input.trim() !== "") {
            appendToHistory(user_input); // Display user message in the chat
            $('#user-input').val(''); // Clear the input field

            try {
                // Create a unique ID for the "working" message using a timestamp
                const uniqueId = `working-message-${Date.now()}`;
                
                const chatWindow = document.getElementById("chat-window");
            
                // Add a placeholder message to the chat window with a unique ID
                chatWindow.innerHTML += `<p id="${uniqueId}"><strong>Bot:</strong> We are working. Please give us one second. Thank you!</p>`;
                
                // Send the user input to your backend
                const response = await fetch('/process_input', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ input: user_input })
                });
            
                if (response.ok) {
                    const data = await response.json(); // Parse the JSON response
                    let formattedResponse = data.response; // Extract the plain text string
            
                    // Step 1: Remove all asterisks (*) globally
                    formattedResponse = formattedResponse.replace(/\*/g, '');
            
                    // Step 2: Replace multiple newlines (e.g., "\n\n") with a single newline
                    formattedResponse = formattedResponse.replace(/\n\s*\n/g, '\n');
            
                    // Step 3: Replace single newlines with HTML <br> for line breaks
                    formattedResponse = formattedResponse.replace(/\n/g, '<br>');
            
                    // Update the most recent "working" message with the actual bot response
                    const workingMessageElement = document.getElementById(uniqueId);
                    if (workingMessageElement) {
                        workingMessageElement.innerHTML = `<strong>Bot:</strong><br>${formattedResponse}`;
                        // Append the bot's response to the chat history
                        chat_history.push(`Bot: ${formattedResponse}\n`);
                    }       
                } else {
                    const errorText = `Error: ${response.status} - ${response.statusText}`;
                    document.getElementById("chat-window").innerHTML += `<p><strong>Bot:</strong> ${errorText}</p>`;
                }
            } catch (error) {
                document.getElementById("chat-window").innerHTML += `<p><strong>Bot:</strong> Error: ${error.message}</p>`;
            }
        }
    }

    // Trigger the handleSubmit function when submit button is clicked
    $('#submit_btn').click(handleSubmit);

    // Trigger the handleSubmit function when Enter key is pressed (key code 13 for Enter)
    $(document).keypress(function(event) {
        if (event.which === 13) { // Enter key pressed
            handleSubmit();
        }
    });
});