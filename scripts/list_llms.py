import openai

# Set up the client with base URL and API key
openai.api_base = "http://10.227.91.60:4000/v1"
openai.api_key = "sk-1234"

# List the models and print them sorted by ID
models = openai.Model.list()
for m in sorted(models['data'], key=lambda x: x['id']):
    print(m)