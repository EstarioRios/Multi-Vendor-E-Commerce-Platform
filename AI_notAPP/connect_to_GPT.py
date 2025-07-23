from openai import OpenAI


async def comment_ban_GPT(request):
    client = OpenAI(api_key="", base_url="https://api.gapgpt.app/v1")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": f"درصورتی عبارت نامناسب است تنها بگو: ban در غیر این صورت بگو noban {str(request)}",
            }
        ],
    )
    finall_respone = response.choices[0].message.content
    if str(finall_respone) == "ban":
        return False
    elif str(finall_respone) == "noban":
        return True
    else:
        return True
