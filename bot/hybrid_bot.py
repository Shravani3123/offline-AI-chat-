from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import time # Import time to measure response time

# --- Determine Device for Computation (GPU if available, else CPU) ---
# Check if CUDA (NVIDIA GPU support) is available. If so, use 'cuda'.
# Otherwise, fall back to using the 'cpu'.
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🤖 Using device: {device}\n") # Inform the user which device is being used

# --- Load Model and Tokenizer ---
# We are using 'microsoft/DialoGPT-medium' for offline operation.
# This model is primarily designed for generating conversational dialogue.
# While it can respond to general queries, its strength is in continuing a conversation,
# not necessarily providing highly accurate factual information like a search engine.
model_name = "microsoft/DialoGPT-medium"

try:
    # Load the tokenizer from the pre-trained model.
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    # Load the model and immediately move it to the determined device (GPU or CPU).
    model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
    # Add a padding token to the tokenizer if it doesn't have one, needed for batching and attention mask.
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    print("Model loaded successfully. This chatbot works offline after the initial download.")
except Exception as e:
    # Provide a helpful error message if model loading fails,
    # often due to no internet connection for the initial download.
    print(f"Error loading model or tokenizer: {e}")
    print("Please ensure you have an active internet connection for the first run to download the model.")
    print("Once downloaded, the model will be cached, and you can run the chatbot offline.")
    exit() # Exit the program if the model cannot be loaded

print("🤖 Offline AI Chatbot is ready! Type 'exit' to quit.\n")

# --- Initialize Chat History for Conversational Memory ---
# This variable will store the encoded IDs of the entire conversation.
# It will be updated after each turn (user input + bot response) to provide context
# for the next generation.
chat_history_ids = None

# --- Start Chat Loop ---
while True:
    try:
        user_input = input("You: ")
    except EOFError:
        print("\nBot: End of input detected. Exiting chat.")
        break # Break loop on EOFError to prevent crashing

    if user_input.lower() == "exit":
        print("Bot: Goodbye! Chat session ended.")
        break # Exit the loop if the user types 'exit'

    start_time = time.time() # Record the start time to measure response duration

    # Tokenize the new user input.
    # The return_tensors='pt' ensures it returns PyTorch tensors.
    new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt').to(device)

    # Concatenate the new user input with the existing chat history.
    # If it's the first turn (chat_history_ids is None), use only the new input.
    if chat_history_ids is None:
        input_ids_for_generation = new_user_input_ids
    else:
        # Concatenate along dimension -1 (the sequence length dimension)
        input_ids_for_generation = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)

    # --- Create Attention Mask ---
    # An attention mask is a tensor with 1s for actual tokens and 0s for padding tokens.
    # This helps the model distinguish real input from padding, crucial when pad_token == eos_token.
    attention_mask = torch.ones(input_ids_for_generation.shape, device=device)

    # --- Generate Response with Optimization ---
    # Use torch.no_grad() context manager:
    # This disables gradient calculations, which are only needed during training.
    # Disabling them significantly speeds up inference and reduces memory usage.
    with torch.no_grad():
        output_ids = model.generate(
            input_ids_for_generation,
            attention_mask=attention_mask, # Pass the attention mask
            max_length=150,           # Maximum length of the generated response (including prompt).
            pad_token_id=tokenizer.eos_token_id, # ID for padding tokens.
            do_sample=True,           # Enable sampling for more diverse responses.
            top_k=50,                 # Sample from the top K most likely tokens.
            top_p=0.95,               # Sample from the smallest set of tokens whose cumulative probability exceeds P.
            temperature=0.75,         # Controls the randomness of predictions. Higher values mean more random.
            no_repeat_ngram_size=3    # Prevent repetition of n-grams (sequences of 3 words) in the output.
        )

    # Decode the generated response:
    # Slice output_ids to exclude the input prompt tokens (including the history)
    # to get only the newly generated part of the conversation.
    reply = tokenizer.decode(output_ids[:, input_ids_for_generation.shape[-1]:][0], skip_special_tokens=True)

    end_time = time.time() # Record the end time
    response_time = end_time - start_time # Calculate the time taken for response generation

    # Print the bot's reply and the measured response time.
    print(f"Bot: {reply} (Response time: {response_time:.2f} seconds)")

    # Update chat_history_ids for the next turn.
    # The entire generated sequence (input + new reply) becomes the new history.
    chat_history_ids = output_ids

    # --- Log Chat to File ---
    # Open 'chat_log.txt' in append mode ('a') with UTF-8 encoding.
    # Write the user's input and the bot's reply to the log file.
    with open("chat_log.txt", "a", encoding="utf-8") as f:
        f.write(f"You: {user_input}\nBot: {reply}\n\n")
