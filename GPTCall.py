import requests
import openai 



api_key="YOUR_API_KEY"
# launch vscode from anaconda launcher to have proper environments


def ask_chatgpt(myPrompt, myContent):
    response_text=ask_chatgpt_online(myPrompt,myContent)
    # response_text=ask_local_llama2(myPrompt,myContent)
    #response_text=ask_huggingface_llama2(myPrompt,myContent)
    
    return  response_text

def ask_chatgpt_online(myPrompt, myContent):
    endpoint = "https://api.openai.com/v1/chat/completions"
    headers = {
            'Accept': 'text/event-stream', #'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }    
    msg=[]   

    msg.append({'role': 'user', 'content': myPrompt+myContent})

    data = {
                #'model': 'gpt-4',
                'model': 'gpt-4-1106-preview',
                #'model': 'gpt-3.5-turbo',  # test well then change to gpt-4
                'messages': msg, # f"{prompt} Answer without explanation:" can do it more precise
                'max_tokens': 4096, # Adjust this value to limit the response data
                'temperature': 0.2 # Lower values (e.g., 0.5) will make the output more focused and deterministic, while higher values (e.g., 1.0) will make it more random.
            }
    
    response = requests.post(endpoint, headers=headers, json=data).json()
    
    #testing start
    #print("API Status Code:", response.status_code)
    #print("API Response:", response.text)
    #Testig
    
    if 'choices' in response:
            response_text = response['choices'][0]['message']['content'].strip()   
    else:
            print ('An error occurred while processing your request. Please try again.')
            response_text ="GPT: An error occurred while processing your request. Please try again."    
    return  response_text


def ask_local_llama2(myPrompt, myContent):
    
    endpoint = "http://140.159.50.187:5000/v1/chat/completions"    
    headers = {  "Content-Type": "application/json"     }
    history = []

#     user_message = input("> ")
    history.append({"role": "user", "content": myPrompt+myContent})
    data = {
        "mode": "chat",
        "character": "Example",
        "messages": history
    }

    response = requests.post(endpoint, headers=headers, json=data).json()

    if 'choices' in response:
            response_text = response['choices'][0]['message']['content'].strip()   
    else:
            print ('An error occurred while processing your request. Please try again.')
            response_text ="GPT: An error occurred while processing your request. Please try again."    
    history.append({"role": "assistant", "content": response_text})
    return  response_text
