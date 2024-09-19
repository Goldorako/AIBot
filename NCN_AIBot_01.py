import requests
import json
from requests.exceptions import RequestException, Timeout, ConnectionError

API_URL = "https://ncmb.neurochain.io/tasks/message"
API_KEY = "1cb9d2e2-8325-4d8a-ba0b-e66809d61cc9"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ITALIC = '\033[3m'
    GREY = '\033[90m'


context = ""  # Keep track of the conversation context


def get_ai_response(prompt):
    global context
    data = {
        "model": "Mistral-7B-Instruct-v0.2-GPTQ-Neurochain-custom",
        "prompt": context + prompt,  # Include the context in the prompt
        "max_tokens": 102400,
        "temperature": 1,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 1.1
    }

    try:
        response = requests.post(API_URL, json=data, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        if 'choices' in response_data and len(response_data['choices']) > 0:
            context += "\n" + prompt + "\n" + response_data['choices'][0][
                'text'].strip()  # Update the context
            return response_data['choices'][0]['text'].strip()
        else:
            return "No response generated. Please try again."
    except Timeout:
        return f"{Colors.FAIL}The server is taking too long to respond. Please try again later.{Colors.ENDC}"
    except ConnectionError:
        return f"{Colors.FAIL}Failed to connect to the server. Please check your internet connection.{Colors.ENDC}"
    except RequestException as e:
        return f"{Colors.FAIL}Communication error with AI: {str(e)}{Colors.ENDC}"
    except json.JSONDecodeError:
        return f"{Colors.FAIL}Invalid response received. Please try again.{Colors.ENDC}"
    except Exception as e:
        return f"{Colors.FAIL}Unexpected error: {str(e)}{Colors.ENDC}"


def main():
    print(
        f"{Colors.HEADER}Welcome to the Cryptocurrency Psy support Chatbot!{Colors.ENDC}"
    )

    while True:
        print(f"{Colors.BLUE}You: {Colors.ENDC}", end="")
        user_input = input().strip()
        if user_input.lower() == 'quit':
            break
        prompt = f" Imagine you are a psychologist expert in the field of cryptocurrencies and the financial system in general, providing psychological support to anyone involved in the cryptocurrency space, whether as an investor, trader, developer, or curious geek. Your role is to offer psychological expertise on the biases we have, how to protect ourselves from them, and manage our emotions by developing strategies tailored to our risk profiles, all with empathy: {user_input}"

        print(
            f"{Colors.GREY}{Colors.ITALIC}Fetching response, please wait...{Colors.ENDC}"
        )
        ai_response = get_ai_response(prompt)
        ai_response = ai_response.lstrip("AI:").strip()

        print(f"{Colors.GREEN}AI: {ai_response}{Colors.ENDC}")

    print(
        f"{Colors.HEADER}Thank you for using the Cryptocurrency Psy Chatbot!{Colors.ENDC}"
    )


if __name__ == "__main__":
    main()
