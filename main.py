import os
import argparse

from prompts import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions, call_function
from config import MAX_ITERS

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="Enter user prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()


    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("API key not found")
    
    client = genai.Client(api_key = api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")
    
    for i in range(MAX_ITERS):
        result = generate_content(client, messages, args.verbose)
        if result:
            print(result)
            break
    else:
        print("Error: Maximum limit of model reached")
        exit(1)
        

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt),
        )
    if not response.usage_metadata:
        raise RuntimeError("API request failed")
    if verbose: 
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    for candidate in response.candidates:
        messages.append(candidate.content)
    if not response.function_calls:
        return f"Response: {response.text}"
    function_call_result_list = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call,verbose)
        if not function_call_result.parts:
            raise Exception
        if function_call_result.parts[0].function_response == None:
            raise Exception
        if function_call_result.parts[0].function_response.response == None:
            raise Exception
        function_call_result_list.append(function_call_result.parts[0]) 
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
    messages.append(types.Content(role="user", parts=function_call_result_list))
if __name__ == "__main__":
    main()