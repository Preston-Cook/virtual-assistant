import openai
from api_secrets import OAI_API_KEY

# Add API key as attr to openai object
openai.api_key = OAI_API_KEY

def ask_computer(prompt):
    # Define specifications per documentation
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=100,
    )
    # Return computer answer as str
    return response["choices"][0]["text"]