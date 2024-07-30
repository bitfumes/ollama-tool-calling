import json

import ollama
import requests


def get_exchange_rate(currency_code):
    res = requests.get(
        f"https://v6.exchangerate-api.com/v6/1234/latest/{currency_code}")
    return json.dumps(res.json()['conversion_rates'])


available_functions = {
    'get_exchange_rate': get_exchange_rate
}

messages = [
    {
        'role': 'user',
        'content': input('Ask about currency conversion :')
    }
]


def askLlm(messages):
    return ollama.chat(
        model="llama3.1",
        messages=messages,
        tools=[
            {
                'type': 'function',
                'function': {
                    'name': 'get_exchange_rate',
                    'description': 'it can get the exchange rate for the currency we need to convert',
                    'parameters': {
                        'properties': {
                            'currency_code': {
                                'description': 'One currency code we want to get exchange rate for.',
                                'type': 'string'
                            },
                        },
                        'required': ['currency_code']
                    }
                }
            }
        ]
    )


result = askLlm(messages)
print(result['message']['content'])

if 'tool_calls' in result['message']:
    function_to_call = available_functions[
        result['message']['tool_calls'][0]['function']['name']
    ]

    res = function_to_call(
        result['message']['tool_calls'][0]['function']['arguments']['currency_code']
    )

    messages.append({'role': 'tool', 'content': res})


final_result = askLlm(messages)


print(final_result['message'])
