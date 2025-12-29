import google.generativeai as genai


def paraphrase_text(api_key: str, text: str, model: str) -> str:
    """
    Paraphrase given text using Google's Gemini model.

    :param api_key: Your Google API key
    :param text: The text you want to paraphrase
    :param model: Gemini model name
    :return: Paraphrased text as a string
    """
    genai.configure(api_key=api_key)
    prompt = f"Paraphrase the following text without changing its meaning:\n\n{text}"
    model = genai.GenerativeModel(model)
    response = model.generate_content(prompt)
    # The response contains the paraphrased text
    return response.text
