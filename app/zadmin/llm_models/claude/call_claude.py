import anthropic
import os
import json
import sys
import time
import logging
from datetime import datetime

FILE_PREFIX = "claude4_p2" # Prefix for output files
# 4 means Claude 4, p2 means prompt template 2

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'{FILE_PREFIX}.log', encoding='utf-8'),
        logging.StreamHandler()  # Also log to console
    ]
)

logger = logging.getLogger(__name__)

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


def extract_json_from_response(response_text):
    """Extract JSON content from markdown code blocks"""
    import re
    
    # Try to find JSON in markdown code blocks
    json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
    match = re.search(json_pattern, response_text, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    
    # If no code blocks, try to find JSON object directly
    json_pattern = r'(\{.*\})'
    match = re.search(json_pattern, response_text, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    
    # If nothing found, return original text
    return response_text.strip()


def read_characters_from_file(filename):
    """Read characters from input file, one per line"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            characters = [line.strip() for line in f if not line.strip().startswith('#') and line.strip()]
        logger.info(f"Successfully loaded {len(characters)} characters from {filename}")
        return characters
    except FileNotFoundError:
        logger.error(f"Input file {filename} not found!")
        return []
    except Exception as e:
        logger.error(f"Error reading file {filename}: {e}")
        return []


def analyze_chinese_character(zi, client):
    """Analyze a Chinese character using Claude 4"""
    
    try:
        logger.info(f"Starting analysis for character: {zi}")
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=6000,
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
        
        # Extract JSON from markdown code blocks if present
        clean_json = extract_json_from_response(response_text)
        
        # Validate JSON before saving
        try:
            json.loads(clean_json)
            file_name = f"{FILE_PREFIX}_{zi}.json"
            logger.info(f"✓ Valid JSON generated for character: {zi}")
            print(f"✓ {zi} -> {file_name}")
            content_to_save = clean_json
        except json.JSONDecodeError as e:
            file_name = f"{FILE_PREFIX}_{zi}.txt"
            logger.warning(f"Invalid JSON for character {zi}: {e}")
            print(f"⚠ {zi} -> {file_name} (needs manual review)")
            content_to_save = response_text  # Save original response for debugging
        
        # Save to file
        with open(file_name, "w", encoding="utf-8") as f: 
            f.write(content_to_save)
        
        logger.info(f"Analysis saved to: {file_name}")
        return True
        
    except Exception as e:
        logger.error(f"Error analyzing character '{zi}': {e}")
        print(f"✗ {zi} -> FAILED: {e}")
        return False


def process_batch(characters, delay_seconds=2):
    """Process a batch of characters with rate limiting"""
    
    # Initialize client once
    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )
    
    total = len(characters)
    successful = 0
    failed = 0
    start_time = datetime.now()
    
    logger.info(f"Starting batch processing of {total} characters")
    print(f"\n🚀 Processing {total} characters...")
    print(f"⏱️  Delay between requests: {delay_seconds} seconds")
    print(f"📝 Logging to: {FILE_PREFIX}.log")
    print("-" * 50)
    
    for i, zi in enumerate(characters, 1):
        print(f"[{i:3d}/{total}] Processing: {zi}")
        
        # Skip if file already exists
        json_file = f"{FILE_PREFIX}_{zi}.json"
        txt_file = f"{FILE_PREFIX}_{zi}.txt"
        
        if os.path.exists(json_file) or os.path.exists(txt_file):
            print(f"    ⏭️  Skipping (already exists)")
            logger.info(f"Skipping character {zi} - file already exists")
            successful += 1
            continue
        
        # Process character
        if analyze_chinese_character(zi, client):
            successful += 1
        else:
            failed += 1
        
        # Progress update every 10 characters
        if i % 10 == 0:
            elapsed = datetime.now() - start_time
            rate = i / elapsed.total_seconds() * 60  # characters per minute
            eta_minutes = (total - i) / rate if rate > 0 else 0
            print(f"    📊 Progress: {successful} success, {failed} failed, {rate:.1f}/min, ETA: {eta_minutes:.1f}min")
        
        # Rate limiting (skip delay for last character)
        if i < total:
            print(f"    ⏳ Waiting {delay_seconds}s...")
            time.sleep(delay_seconds)
    
    # Final summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    print("\n" + "=" * 50)
    print(f"🎯 BATCH PROCESSING COMPLETE")
    print(f"📈 Total processed: {total}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"⏰ Duration: {duration}")
    print(f"📊 Average rate: {total / duration.total_seconds() * 60:.1f} characters/minute")
    print("=" * 50)
    
    logger.info(f"Batch processing completed: {successful} successful, {failed} failed, duration: {duration}")


def main():
    """Main function to run the batch analysis"""
    
    # Check if API key is set
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ Error: Please set ANTHROPIC_API_KEY environment variable")
        logger.error("ANTHROPIC_API_KEY not set")
        sys.exit(1)
    
    # Configuration
    input_file = "elemental_characters.txt"  # Change this to your input file name
    delay_seconds = 2  # Adjust based on your rate limits
    
    # Read characters from file
    print(f"📖 Reading characters from: {input_file}")
    characters = read_characters_from_file(input_file)
    
    if not characters:
        print(f"❌ No characters loaded from {input_file}")
        print(f"💡 Make sure the file exists and contains one character per line")
        sys.exit(1)
    
    # Show first few characters as preview
    preview = characters[:5]
    print(f"📋 Preview: {', '.join(preview)}{'...' if len(characters) > 5 else ''}")
    
    # Confirm before starting
    response = input(f"\n❓ Process {len(characters)} characters? (y/N): ").strip().lower()
    if response != 'y':
        print("❌ Processing cancelled")
        sys.exit(0)
    
    # Start processing
    process_batch(characters, delay_seconds)


if __name__ == "__main__":
    main()