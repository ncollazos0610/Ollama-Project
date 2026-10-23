import ollama

# Realizar una llamada al modelo descargado
response = ollama.chat(
    model='llama3.2:1b', 
    messages=[
  { 'role': 'user',
    'content': '¿Puedes explicarme qué es una API en una sola frase?',
  },
])

# Imprimir la respuesta del LLM
print(response['message']['content'])
