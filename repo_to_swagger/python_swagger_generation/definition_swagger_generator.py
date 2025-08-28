import json
from repo_to_swagger.prompts import python_swagger_prompt
from repo_to_swagger.llm_client import OpenAiClient



def get_function_definition_swagger(function_definition, context, route):
    openai_ai_client = OpenAiClient()
    messages = [{
        "role": "user",
        "content": python_swagger_prompt.format(route = route, function_definition = function_definition, context = context)
    }]
    response = openai_ai_client.call_chat_completion(messages=messages, temperature=1)
    start_index = response.find('{')
    end_index = response.rfind('}')
    swagger_json_block = response[start_index:end_index + 1]
    return json.loads(swagger_json_block)
