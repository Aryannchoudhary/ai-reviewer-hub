from google import genai
import os

client = genai.Client(api_key=os.getenv("Gemini_API_Key"))

def review_code_with_ai(code, language):
    """
    Generate structured JSON review from Gemini AI.
    """
    try:
        prompt = f"""
        You are an expert code reviewer. Analyze the following {language} code.

        Respond ONLY with valid JSON in this exact structure:
        {{
            "score": 1-10,
            "output": "Expected output or 'No output/prints errors'",
            "errors": ["List of error descriptions"],
            "improvements": ["List of improvement suggestions"],
            "optimized_code": "Full optimized/improved code version"
        }}

        Code:
        ```{language}
        {code}
        ```

        Be concise, actionable. Fix all issues in optimized_code.
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        # Basic JSON extraction (may need improvement later)
        import json
        import re
        text = response.text.strip()
        # Extract JSON block
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            review_json = json.loads(json_match.group())
            return review_json
        return {"score": 5, "output": "Review unavailable", "errors": ["AI response not JSON"], "improvements": [], "optimized_code": code}
    except Exception as e:
        return {"score": 1, "output": "Error", "errors": [str(e)], "improvements": [], "optimized_code": code}

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"AI review is currently unavailable: {str(e)}"