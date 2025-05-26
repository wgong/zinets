import anthropic
import os
import json
import sys

# Improved prompt with better structure and instructions
prompt_zi = """
你是中文语言专家。请对汉字「{zi}」进行全面分析，包含以下方面：

请用中文回答，并严格按照JSON格式输出。注意：
1. 所有字符串值必须用双引号包围
2. 字符串内的双引号需要转义为 \"
3. 确保JSON格式完全有效

请提供以下信息（尽量为每个列表提供5个或更多例子）：

{{
  "汉字": "{zi}",
  "含义": "字符的基本含义和解释",
  "字形": "字形结构分析",
  "读音": {{
    "拼音": "pinyin",
    "声调": "tone number",
    "国际音标": "IPA if available"
  }},
  "字源": "字的起源和演变历史",
  "常用词组": [
    "词组1",
    "词组2",
    "词组3",
    "词组4",
    "词组5"
  ],
  "成语": [
    "成语1",
    "成语2", 
    "成语3",
    "成语4",
    "成语5"
  ],
  "例句": [
    "例句1",
    "例句2",
    "例句3", 
    "例句4",
    "例句5"
  ],
  "短故事": [
    "故事1",
    "故事2",
    "故事3",
    "故事4",
    "故事5"
  ],
  "诗词": [
    "诗词1",
    "诗词2",
    "诗词3",
    "诗词4", 
    "诗词5"
  ],
  "图片建议": [
    "图片描述1",
    "图片描述2",
    "图片描述3",
    "图片描述4",
    "图片描述5"
  ],
  "音频建议": [
    "音频资源1",
    "音频资源2",
    "音频资源3",
    "音频资源4",
    "音频资源5"
  ],
  "视频建议": [
    "视频资源1", 
    "视频资源2",
    "视频资源3",
    "视频资源4",
    "视频资源5"
  ],
  "电影": [
    "电影1",
    "电影2",
    "电影3",
    "电影4",
    "电影5"
  ],
  "参考资料": [
    "资料1",
    "资料2", 
    "资料3",
    "资料4",
    "资料5"
  ],
  "有趣网站": [
    "网站1",
    "网站2",
    "网站3", 
    "网站4",
    "网站5"
  ]
}}

请确保输出的是完全有效的JSON格式。
"""


def analyze_chinese_character(zi):
    """Analyze a Chinese character using Claude 4"""
    
    # Initialize client
    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )
    

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=20000,
            temperature=0.3,  # Reduced for more consistent JSON output
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
        
        # Extract the actual text content
        response_text = message.content[0].text
        
        # Validate JSON before saving
        try:
            json.loads(response_text)
            print(f"✓ Valid JSON generated for character: {zi}")
            file_name = f"claude4_p2_{zi}.json"
        except json.JSONDecodeError as e:
            file_name = f"claude4_p2_{zi}.txt"
            print(f"⚠ Warning: Generated content may not be valid JSON: {e}")
            print("Saving anyway for manual review...")
        
        # Save to file with better naming
        with open(file_name, "w", encoding="utf-8") as f: 
            f.write(response_text)
        
        print(f"Analysis saved to: {file_name}")
        return response_text
        
    except Exception as e:
        print(f"Error analyzing character '{zi}': {e}")
        return None

def main():
    """Main function to run the analysis"""
    
    # Check if API key is set
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: Please set ANTHROPIC_API_KEY environment variable")
        sys.exit(1)
    
    # Test with your character
    zi = "字"
    
    print(f"Analyzing Chinese character: {zi}")
    result = analyze_chinese_character(zi)
    
    if result:
        print("Analysis completed successfully!")
    else:
        print("Analysis failed!")

if __name__ == "__main__":
    main()