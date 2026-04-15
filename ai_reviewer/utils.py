import google.generativeai as genai
import os
import json
import re

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def review_code_with_ai(code, language):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
        You are an expert code reviewer. Analyze the following {language} code.

        Respond ONLY with valid JSON:
        {{
            "score": 1-10,
            "output": "Expected output",
            "errors": [],
            "improvements": [],
            "optimized_code": ""
        }}

        Code:
        ```{language}
        {code}
        ```
        """

        response = model.generate_content(prompt)
        text = response.text.strip()

        json_match = re.search(r'\{.*\}', text, re.DOTALL)

        if json_match:
            return json.loads(json_match.group())

        return {"score": 5, "output": "No response", "errors": [], "improvements": [], "optimized_code": code}

    except Exception as e:
        return {"score": 1, "output": "Error", "errors": [str(e)], "improvements": [], "optimized_code": code}