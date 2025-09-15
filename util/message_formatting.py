
def format_messages(messages: list[dict]) -> list[dict]:
    """Recebe as mensagens no formato {prompt: string, response: string}[]
    do backend e tranforma em
    [
      {content: string, role: "user"},
      {content: string, role: "assistant"},
      ...
    ]
    """
    formattedMessages = []
    for message in messages:
        formattedMessages.append(
            {"role": "user", "content": message["prompt"]})
        formattedMessages.append(
            {"role": "assistant", "content": message["response"]})
    return formattedMessages


def format_message(message: str):
    """
    Formata a mensagem para inserir caracteres "$" no início e fim de caracteres
    especiais LaTeX, para garantir a exibição correta em markdown.
    """
    message = message.replace("\\(", "$")
    message = message.replace("\\)", "$")
    return message