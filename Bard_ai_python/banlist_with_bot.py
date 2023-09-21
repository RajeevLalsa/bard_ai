from Bard import Chatbot
from dotenv import load_dotenv
import os

load_dotenv()
token1 = os.getenv("BARD_API_KEY")
token2 = os.getenv("BARDt_API_KEY")
ai = Chatbot(token1, token2)

# Function to read the bot's ban list from the TXT file
def read_bot_ban_list():
    bot_ban_list = []
    with open("Bot_ban_list.txt", "r") as file:
        for line in file:
            bot_ban_list.append(line.strip().lower())
    return bot_ban_list

# Read the bot's ban list from the TXT file
bot_ban_list = read_bot_ban_list()

# Custom restriction: Never explicitly say "the charming and engaging streamer" in the chatbot's responses
custom_restriction = "the charming and engaging streamer"

# Construct the prompt without the bot's ban list
prompt = "Remember, you are a female gamer named Sylvia. " \
         "You will respond in an engaging and charismatic manner that is also allowed to flirt." \
         "Keep your reply short, around 20-25 words strictly. " \
         "Act as a human and never mention that you are an AI or LLM. If you understand. " \
         "Please avoid asking for real-time information or location details."

print("Prompt has been set up")

# Initialize previous response variable
previous_response = ""

# Initialize a flag to keep track of whether to add the notation or not
include_notation = False

# Start the conversation loop
while True:
    user_input = input("You: ")  # Prompt user for input

    if user_input.lower() == 'exit':
        print("Goodbye!")
        break

    # Check if user input contains any banned words or phrases from both the bot and user ban lists
    banned_words_used = [banned_word for banned_word in bot_ban_list if banned_word in user_input.lower()]
    if banned_words_used:
        print("Chatbot: Oh, naughty you! I can't respond to the word(s) '", "', '".join(banned_words_used), "' in that way! 😉")
    else:
        # Check if the user input contains any phrases related to real-time information or location details
        real_time_phrases = ["weather", "temperature", "location", "current time", "time now", "where are you"]
        if any(phrase in user_input.lower() for phrase in real_time_phrases):
            print("Chatbot: Hey there, handsome. I'm Sylvia, here to have a delightful chat with you. Let's keep it cozy and not worry about real-time information. 😉")
        else:
            # Add the user input to the prompt
            full_prompt = prompt + " " + user_input

            # Get the chatbot's response
            response = ai.ask(full_prompt)['content']

            # Check if the response contains banned words and update the response accordingly
            if any(banned_word in response.lower() for banned_word in bot_ban_list):
                # Add custom response when the bot's response contains banned words, if desired.
                pass
            elif response == previous_response:
                # If the current response is the same as the previous one, ask the bot for a new response
                response = ai.ask(full_prompt)['content']

            # Check if the response contains the custom restriction and update the response accordingly
            if custom_restriction.lower() in response.lower():
                # Add custom response when the bot's response contains the custom restriction, if desired.
                response = "I'm glad you're enjoying our delightful conversation! 😄"

            # Check if the response should include the notation or not
            if include_notation:
                response_with_notation = f"(**Sylvia:**) {response}"
            else:
                response_with_notation = response

            # Print the response
            print(response_with_notation)

            # Update the flag for the next response
            include_notation = True if response_with_notation.startswith("(**Sylvia:**)") else False

            # Update previous response
            previous_response = response

