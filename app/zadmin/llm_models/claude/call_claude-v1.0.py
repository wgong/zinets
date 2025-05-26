import anthropic
import os
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

zi = "字"  
prompt_zi = """
You are an expert in Chinese language, 

can you generate a holistic view on this chinese character  {zi}
in terms of the following attributes:
含义
字形
读音 
字源
常用词组
成语
例句
短故事
诗词
图片
音频 
视频 
电影
参考资料
有趣网站

(1) give the answer in Chinese 
(2) format the answer in valid json and ensure quotes are properly escaped (specifically avoid double-quotes nested in doube-quotes)
(3) whenever possible, give 5 or more examples for the following attributes:

常用词组
成语
例句
短故事
诗词
图片
音频 
视频 
电影
参考资料
有趣网站

"""

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=20000,
    temperature=1,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt_zi.format(zi=zi)
                }
            ]
        }
    ]
)
# print(message.content)
with open(f"claude4_p1_{zi}.json", "w", encoding="utf-8") as f: 
    f.write(message.content)