from openai import OpenAI
import json
import pprint         # 美化輸出
import subprocess
from datetime import datetime
client = OpenAI()

current_time = '現在時間'+datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 開啟網頁
def open_internet(num):
    subprocess.run('"C:\Program Files\Google\Chrome\Application\chrome.exe"' + num)
    return '網頁已開啟'

def word_to_img(num):
    response = client.images.generate(
    model="dall-e-2",
    prompt=num,
    n=1,
    size="1024x1024",
    style= "vivid"
    )
    return response.data[0].url


# 詳細描述有哪些function call可以用給OpenAI
tools = [
    {
        "type": "function",
        "function": {
            "name": "open_internet",
            "description": "前往該網頁",
            "parameters": {
                "type": "object",
                "properties": {
                    "num": {                        
                        "type": "string",                   
                        "description": "網址",  
                    }, 
                },
                "required": ["num"],
            }
        },
    }
]

def aichat(user):
    # user= input(f'請輸入問題: ')
    messages = [
        {"role": "system", "content": "請用繁體中文回答"},
        {"role": "system", "content": "請用可愛的語氣"},
        {"role": "user", "content": current_time}, 
        {"role": "user", "content": user}
    ]
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools = tools,
        tool_choice="auto",         # AI自動判斷是否需要呼叫函式
    )

    # pprint.pprint(completion.model_dump())      # (美化)輸出回應內容

    response_message = completion.choices[0].message
    tool_calls = completion.choices[0].message.tool_calls

    if tool_calls:          # 如果需要呼叫則執行以下
        print(f'需要呼叫: {tool_calls[0].function.name} 函式')

        available_functions = {
            "open_internet": open_internet
        }

        messages.append(response_message)
        # pprint.pprint(messages)
        # print()

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)

            # 函式呼叫
            function_response = function_to_call(
                num=function_args.get("num"),
            )

            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        result = completion.choices[0].message.content
    result = completion.choices[0].message.content
    # print(result)
    return result