import anthropic
import os
import json
import sys
import time
import logging
from datetime import datetime
import click
import sqlite3
FILE_PREFIX = "claude4_p2" # Prefix for output files
# 4 means Claude 4, p2 means prompt template 2


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('claude4_batch.log', encoding='utf-8'),
        logging.StreamHandler()
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


def init_batch_db():
    """Initialize SQLite database for batch tracking"""
    conn = sqlite3.connect('batch_history.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS batches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_id TEXT UNIQUE NOT NULL,
            submitted_at TIMESTAMP NOT NULL,
            input_file TEXT NOT NULL,
            prefix TEXT NOT NULL,
            model TEXT NOT NULL,
            character_count INTEGER NOT NULL,
            status TEXT DEFAULT 'submitted',
            completed_at TIMESTAMP,
            notes TEXT
        )
    ''')
    
    conn.commit()
    conn.close()


def save_batch_info(batch_id, input_file, prefix, model, character_count, notes=""):
    """Save batch information to database"""
    conn = sqlite3.connect('batch_history.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO batches (batch_id, submitted_at, input_file, prefix, model, character_count, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (batch_id, datetime.now(), input_file, prefix, model, character_count, notes))
        
        conn.commit()
        logger.info(f"Saved batch info: {batch_id}")
        return True
    except sqlite3.IntegrityError:
        logger.warning(f"Batch {batch_id} already exists in database")
        return False
    finally:
        conn.close()


def update_batch_status(batch_id, status, completed_at=None):
    """Update batch status in database"""
    conn = sqlite3.connect('batch_history.db')
    cursor = conn.cursor()
    
    if completed_at:
        cursor.execute('''
            UPDATE batches SET status = ?, completed_at = ? WHERE batch_id = ?
        ''', (status, completed_at, batch_id))
    else:
        cursor.execute('''
            UPDATE batches SET status = ? WHERE batch_id = ?
        ''', (status, batch_id))
    
    conn.commit()
    conn.close()


def get_batch_info(batch_id):
    """Get batch information from database"""
    conn = sqlite3.connect('batch_history.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM batches WHERE batch_id = ?
    ''', (batch_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        columns = ['id', 'batch_id', 'submitted_at', 'input_file', 'prefix', 'model', 'character_count', 'status', 'completed_at', 'notes']
        return dict(zip(columns, result))
    return None


def list_all_batches():
    """List all batches from database"""
    conn = sqlite3.connect('batch_history.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM batches ORDER BY submitted_at DESC
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    columns = ['id', 'batch_id', 'submitted_at', 'input_file', 'prefix', 'model', 'character_count', 'status', 'completed_at', 'notes']
    return [dict(zip(columns, row)) for row in results]


def get_last_batch_id():
    """Get the most recent batch ID"""
    conn = sqlite3.connect('batch_history.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT batch_id FROM batches ORDER BY submitted_at DESC LIMIT 1
    ''')
    
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else None


def get_client():
    """Get Anthropic client with API key validation"""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        click.echo(click.style("❌ Error: ANTHROPIC_API_KEY environment variable not set", fg='red'))
        click.echo("💡 Set it with: export ANTHROPIC_API_KEY=your_key_here")
        sys.exit(1)
    
    return anthropic.Anthropic(api_key=api_key)


def read_characters_from_file(filename):
    """Read characters from input file, one per line"""
    try:
        if not os.path.exists(filename):
            click.echo(click.style(f"❌ Input file '{filename}' not found!", fg='red'))
            click.echo(f"💡 Create the file with one character per line")
            return []
            
        with open(filename, 'r', encoding='utf-8') as f:
            characters = [line.strip() for line in f if not line.strip().startswith('#') and line.strip()]
        
        logger.info(f"Successfully loaded {len(characters)} characters from {filename}")
        return characters
    except Exception as e:
        logger.error(f"Error reading file {filename}: {e}")
        click.echo(click.style(f"❌ Error reading file: {e}", fg='red'))
        return []


def create_batch_requests(characters, prefix="claude4_batch"):
    """Create batch requests for all characters"""
    requests = []
    skipped = 0
    
    for i, zi in enumerate(characters):
        # Skip if file already exists
        json_file = f"{prefix}_{zi}.json"
        txt_file = f"{prefix}_{zi}.txt"
        
        if os.path.exists(json_file) or os.path.exists(txt_file):
            logger.info(f"Skipping character {zi} - file already exists")
            skipped += 1
            continue
        
        # Create API-compliant custom_id (no Chinese characters allowed)
        # Use format: char_<index>_<unicode_codepoint>
        unicode_hex = format(ord(zi), '04x')
        custom_id = f"char_{i:04d}_{unicode_hex}"
        
        request = {
            "custom_id": custom_id,
            "params": {
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 6000,
                "temperature": 0.3,
                "messages": [
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
            }
        }
        requests.append(request)
    
    if skipped > 0:
        click.echo(f"⏭️  Skipped {skipped} already processed characters")
    
    logger.info(f"Created {len(requests)} batch requests")
    return requests


def decode_custom_id_to_character(custom_id):
    """Convert API-compliant custom_id back to Chinese character"""
    # Format: char_<index>_<unicode_hex>
    try:
        parts = custom_id.split('_')
        if len(parts) >= 3 and parts[0] == 'char':
            unicode_hex = parts[2]
            return chr(int(unicode_hex, 16))
    except (ValueError, IndexError):
        pass
    
    # Fallback for old format
    return custom_id.replace('char_', '')


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


@click.group()
@click.version_option(version='1.0.0', prog_name='Chinese Character Analyzer')
def cli():
    """
    🔤 Chinese Character Analysis Tool using Claude 4 Batch API
    
    Analyze Chinese characters with comprehensive linguistic and cultural analysis.
    Features 50% cost savings through batch processing.
    """
    pass


@cli.command()
@click.option('--input-file', '-i', default='elemental_characters.txt',
              help='Input file containing characters (one per line)')
@click.option('--prefix', '-p', default='claude4_batch',
              help='Output file prefix')
@click.option('--model', '-m', default='claude-sonnet-4-20250514',
              help='Claude model to use')
@click.option('--max-tokens', default=6000, type=int,
              help='Maximum tokens per response')
@click.option('--temperature', default=0.3, type=float,
              help='Temperature for response generation')
@click.option('--dry-run', is_flag=True,
              help='Show what would be processed without submitting')
@click.option('--notes', default="",
              help='Optional notes about this batch')
def submit(input_file, prefix, model, max_tokens, temperature, dry_run, notes):
    """Submit a new batch for processing"""
    
    # Initialize database
    init_batch_db()
    
    click.echo(click.style("🚀 CLAUDE BATCH PROCESSING", fg='blue', bold=True))
    click.echo("💰 50% cost savings vs standard API")
    click.echo("⏰ Processing within 24 hours")
    click.echo("-" * 40)
    
    # Read characters
    characters = read_characters_from_file(input_file)
    
    if not characters:
        click.echo(click.style(f"❌ No characters loaded from {input_file}", fg='red'))
        return
    
    click.echo(f"📖 Loaded {len(characters)} characters from {input_file}")
    
    # Create batch requests
    requests = create_batch_requests(characters, prefix)
    
    if not requests:
        click.echo(click.style("ℹ️ All characters already processed!", fg='yellow'))
        return
    
    # Show preview
    preview_chars = [req['custom_id'].replace('char_', '') for req in requests[:5]]
    click.echo(f"📋 Will process: {click.style(', '.join(preview_chars), fg='cyan')}{'...' if len(requests) > 5 else ''}")
    click.echo(f"📊 Total: {click.style(str(len(requests)), fg='green')} characters")
    click.echo(f"🎯 Model: {click.style(model, fg='yellow')}")
    click.echo(f"🔧 Settings: max_tokens={max_tokens}, temperature={temperature}")
    if notes:
        click.echo(f"📝 Notes: {click.style(notes, fg='cyan')}")
    
    # Calculate estimated cost
    estimated_output_tokens = len(requests) * 3000  # ~3K tokens per character
    estimated_input_tokens = len(requests) * 200    # ~200 tokens per prompt
    batch_cost = (estimated_output_tokens * 15 + estimated_input_tokens * 3) / 1_000_000 * 0.5  # 50% discount
    click.echo(f"💰 Estimated cost: {click.style(f'${batch_cost:.2f}', fg='green')} (with 50% batch discount)")
    
    if dry_run:
        click.echo(click.style("🔍 DRY RUN - No batch submitted", fg='yellow', bold=True))
        return
    
    # Confirm submission
    if not click.confirm(click.style("\n❓ Submit batch for processing?", fg='blue')):
        click.echo(click.style("❌ Batch submission cancelled", fg='red'))
        return
    
    # Submit batch
    try:
        client = get_client()
        click.echo("⏳ Submitting batch...")
        
        batch = client.messages.batches.create(requests=requests)
        batch_id = batch.id
        
        # Save to database
        save_batch_info(batch_id, input_file, prefix, model, len(requests), notes)
        
        logger.info(f"Batch submitted successfully. Batch ID: {batch_id}")
        
        click.echo(click.style(f"✅ Batch submitted successfully!", fg='green', bold=True))
        click.echo(f"📋 Batch ID: {click.style(batch_id, fg='cyan')}")
        click.echo(f"📊 Processing {len(requests)} characters")
        click.echo(f"⏰ Expected completion: within 24 hours")
        click.echo(f"💾 Batch info saved to database")
        
        click.echo(f"\n💡 Next steps:")
        click.echo(f"   Check status: {click.style(f'python {sys.argv[0]} status {batch_id}', fg='blue')}")
        click.echo(f"   Quick status: {click.style(f'python {sys.argv[0]} status', fg='blue')} (uses latest batch)")
        click.echo(f"   List all:     {click.style(f'python {sys.argv[0]} list', fg='blue')}")
        click.echo(f"   Download:     {click.style(f'python {sys.argv[0]} download {batch_id}', fg='blue')}")
        
    except Exception as e:
        logger.error(f"Error submitting batch: {e}")
        click.echo(click.style(f"❌ Failed to submit batch: {e}", fg='red'))


@cli.command()
@click.argument('batch_id', required=False)
@click.option('--watch', '-w', is_flag=True,
              help='Watch status with auto-refresh every 30 seconds')
def status(batch_id, watch):
    """Check batch processing status"""
    
    # Initialize database
    init_batch_db()
    
    # Use last batch ID if not provided
    if not batch_id:
        batch_id = get_last_batch_id()
        if batch_id:
            click.echo(f"📋 Using latest batch ID: {batch_id}")
        else:
            click.echo(click.style("❌ No batch ID provided and no previous batches found", fg='red'))
            click.echo("💡 Usage: python script.py status <batch_id>")
            click.echo("💡    or: python script.py list  # to see all batches")
            return
    
    client = get_client()
    
    def check_status():
        try:
            batch = client.messages.batches.retrieve(batch_id)
            status_val = batch.processing_status
            
            # Update database status
            if status_val == 'ended':
                update_batch_status(batch_id, 'completed', datetime.now())
            else:
                update_batch_status(batch_id, status_val)
            
            # Get batch info from database
            batch_info = get_batch_info(batch_id)
            
            # Status with color coding
            status_colors = {
                'validating': 'yellow',
                'in_progress': 'blue', 
                'canceling': 'red',
                'canceled': 'red',
                'ended': 'green'
            }
            
            colored_status = click.style(status_val, fg=status_colors.get(status_val, 'white'), bold=True)
            click.echo(f"📊 Batch {click.style(batch_id, fg='cyan')} status: {colored_status}")
            
            # Show batch info from database
            if batch_info:
                click.echo(f"📁 Input file: {click.style(batch_info['input_file'], fg='cyan')}")
                click.echo(f"🏷️  Prefix: {click.style(batch_info['prefix'], fg='yellow')}")
                click.echo(f"📅 Submitted: {click.style(batch_info['submitted_at'], fg='blue')}")
                if batch_info['notes']:
                    click.echo(f"📝 Notes: {click.style(batch_info['notes'], fg='cyan')}")
            
            if hasattr(batch, 'request_counts'):
                counts = batch.request_counts
                total = getattr(counts, 'total', 0)
                succeeded = getattr(counts, 'succeeded', 0)
                errored = getattr(counts, 'errored', 0)
                processing = getattr(counts, 'processing', 0)
                completed = succeeded + errored
                
                # Progress bar
                if total > 0:
                    progress = completed / total
                    bar_length = 30
                    filled_length = int(bar_length * progress)
                    bar = '█' * filled_length + '░' * (bar_length - filled_length)
                    percentage = progress * 100
                    
                    click.echo(f"📈 Progress: [{bar}] {percentage:.1f}% ({completed}/{total})")
                
                if succeeded > 0:
                    click.echo(f"    ✅ Succeeded: {click.style(str(succeeded), fg='green')}")
                if errored > 0:
                    click.echo(f"    ❌ Errored: {click.style(str(errored), fg='red')}")
                if processing > 0:
                    click.echo(f"    ⏳ Processing: {click.style(str(processing), fg='blue')}")
            
            # Show completion info
            if status_val == 'ended':
                click.echo(click.style("🎉 Batch completed! Ready for download.", fg='green', bold=True))
                click.echo(f"💡 Download: python {sys.argv[0]} download {batch_id}")
            
            return status_val
            
        except Exception as e:
            logger.error(f"Error checking batch status: {e}")
            click.echo(click.style(f"❌ Error checking status: {e}", fg='red'))
            return None
    
    if watch:
        click.echo("👀 Watching batch status (Ctrl+C to stop)...")
        click.echo("🔄 Auto-refresh every 30 seconds")
        try:
            while True:
                click.clear()
                status_val = check_status()
                if status_val == 'ended':
                    break
                click.echo(f"\n⏰ Last updated: {datetime.now().strftime('%H:%M:%S')}")
                click.echo("   Press Ctrl+C to stop watching")
                time.sleep(30)
        except KeyboardInterrupt:
            click.echo(click.style("\n⏹️  Stopped watching", fg='yellow'))
    else:
        check_status()


@cli.command()
@click.argument('batch_id', required=False)
@click.option('--prefix', '-p', 
              help='Output file prefix (auto-detected from database if not specified)')
@click.option('--force', is_flag=True,
              help='Force re-download even if files exist')
def download(batch_id, prefix, force):
    """Download and save batch results"""
    
    # Initialize database
    init_batch_db()
    
    # Use last batch ID if not provided
    if not batch_id:
        batch_id = get_last_batch_id()
        if batch_id:
            click.echo(f"📋 Using latest batch ID: {batch_id}")
        else:
            click.echo(click.style("❌ No batch ID provided and no previous batches found", fg='red'))
            return
    
    # Get batch info from database
    batch_info = get_batch_info(batch_id)
    if batch_info and not prefix:
        prefix = batch_info['prefix']
        click.echo(f"🏷️  Using prefix from database: {click.style(prefix, fg='cyan')}")
    elif not prefix:
        prefix = 'claude4_batch'
        click.echo(f"⚠️  No prefix specified, using default: {prefix}")
    
    client = get_client()
    
    try:
        click.echo(f"📦 Downloading results for batch {click.style(batch_id, fg='cyan')}")
        
        batch = client.messages.batches.retrieve(batch_id)
        
        if batch.processing_status != 'ended':
            click.echo(click.style(f"⚠️ Batch not completed yet. Status: {batch.processing_status}", fg='yellow'))
            return
        
        # Get results
        click.echo("⏳ Fetching results...")
        results = client.messages.batches.results(batch_id)
        
        successful = 0
        failed = 0
        skipped = 0
        

        click.echo(f"📦 Downloading results for batch {click.style(batch_id, fg='cyan')}")
        
        batch = client.messages.batches.retrieve(batch_id)
        
        if batch.processing_status != 'ended':
            click.echo(click.style(f"⚠️ Batch not completed yet. Status: {batch.processing_status}", fg='yellow'))
            return
        
        # Get results
        click.echo("⏳ Fetching results...")
        results = client.messages.batches.results(batch_id)
        
        # Convert JSONLDecoder to list of result lines
        result_lines = []
        for result in results:
            result_lines.append(json.dumps(result))
        
        successful = 0
        failed = 0
        skipped = 0
        
        with click.progressbar(result_lines, 
                             label='Processing results') as progress_lines:
            for result_line in progress_lines:
                if not result_line:
                    continue
                    
                try:
                    result = json.loads(result_line)
                    custom_id = result['custom_id']
                    zi = decode_custom_id_to_character(custom_id)
                    
                    file_name_json = f"{prefix}_{zi}.json"
                    file_name_txt = f"{prefix}_{zi}.txt"
                    
                    # Skip if file exists and not forcing
                    if not force and (os.path.exists(file_name_json) or os.path.exists(file_name_txt)):
                        skipped += 1
                        continue
                    
                    if result['result']['type'] == 'succeeded':
                        # Extract response text
                        response_text = result['result']['message']['content'][0]['text']
                        
                        # Extract JSON from response
                        clean_json = extract_json_from_response(response_text)
                        
                        # Validate JSON
                        try:
                            json.loads(clean_json)
                            file_name = file_name_json
                            content_to_save = clean_json
                            logger.info(f"✓ Valid JSON for character: {zi}")
                            successful += 1
                        except json.JSONDecodeError:
                            file_name = file_name_txt
                            content_to_save = response_text
                            logger.warning(f"Invalid JSON for character {zi}")
                            successful += 1
                        
                        # Save file
                        with open(file_name, "w", encoding="utf-8") as f:
                            f.write(content_to_save)
                            
                    else:
                        # Handle error
                        error = result['result']['error']
                        logger.error(f"Error for character {zi}: {error}")
                        failed += 1
                        
                except Exception as e:
                    logger.error(f"Error processing result: {e}")
                    failed += 1
        
        # Update database status
        update_batch_status(batch_id, 'downloaded', datetime.now())
        
        click.echo(click.style(f"\n🎯 DOWNLOAD COMPLETE", fg='green', bold=True))
        if successful > 0:
            click.echo(f"✅ Successful: {click.style(str(successful), fg='green')}")
        if failed > 0:
            click.echo(f"❌ Failed: {click.style(str(failed), fg='red')}")
        if skipped > 0:
            click.echo(f"⏭️  Skipped (already exist): {click.style(str(skipped), fg='yellow')}")
        
        click.echo(f"📁 Files saved with prefix: {click.style(prefix, fg='cyan')}")
        click.echo(f"💾 Database updated with download status")
        
    except Exception as e:
        logger.error(f"Error downloading batch results: {e}")
        click.echo(click.style(f"❌ Error downloading results: {e}", fg='red'))
        click.echo("⏳ Fetching results...")
        results = client.messages.batches.results(batch_id)
        
        successful = 0
        failed = 0
        skipped = 0
        
        with click.progressbar(results.text.strip().split('\n'), 
                             label='Processing results') as result_lines:
            for result_line in result_lines:
                if not result_line:
                    continue
                    
                try:
                    result = json.loads(result_line)
                    custom_id = result['custom_id']
                    zi = custom_id.replace('char_', '')
                    
                    file_name_json = f"{prefix}_{zi}.json"
                    file_name_txt = f"{prefix}_{zi}.txt"
                    
                    # Skip if file exists and not forcing
                    if not force and (os.path.exists(file_name_json) or os.path.exists(file_name_txt)):
                        skipped += 1
                        continue
                    
                    if result['result']['type'] == 'succeeded':
                        # Extract response text
                        response_text = result['result']['message']['content'][0]['text']
                        
                        # Extract JSON from response
                        clean_json = extract_json_from_response(response_text)
                        
                        # Validate JSON
                        try:
                            json.loads(clean_json)
                            file_name = file_name_json
                            content_to_save = clean_json
                            logger.info(f"✓ Valid JSON for character: {zi}")
                            successful += 1
                        except json.JSONDecodeError:
                            file_name = file_name_txt
                            content_to_save = response_text
                            logger.warning(f"Invalid JSON for character {zi}")
                            successful += 1
                        
                        # Save file
                        with open(file_name, "w", encoding="utf-8") as f:
                            f.write(content_to_save)
                            
                    else:
                        # Handle error
                        error = result['result']['error']
                        logger.error(f"Error for character {zi}: {error}")
                        failed += 1
                        
                except Exception as e:
                    logger.error(f"Error processing result: {e}")
                    failed += 1
        
        click.echo(click.style(f"\n🎯 DOWNLOAD COMPLETE", fg='green', bold=True))
        if successful > 0:
            click.echo(f"✅ Successful: {click.style(str(successful), fg='green')}")
        if failed > 0:
            click.echo(f"❌ Failed: {click.style(str(failed), fg='red')}")
        if skipped > 0:
            click.echo(f"⏭️  Skipped (already exist): {click.style(str(skipped), fg='yellow')}")
        
        click.echo(f"📁 Files saved with prefix: {click.style(prefix, fg='cyan')}")
        
    except Exception as e:
        logger.error(f"Error downloading batch results: {e}")
        click.echo(click.style(f"❌ Error downloading results: {e}", fg='red'))


@cli.command()
@click.option('--status-filter', type=click.Choice(['all', 'submitted', 'in_progress', 'completed', 'downloaded']), 
              default='all', help='Filter batches by status')
@click.option('--limit', default=10, type=int, help='Number of recent batches to show')
def list(status_filter, limit):
    """List all batch processing jobs"""
    
    # Initialize database
    init_batch_db()
    
    click.echo(click.style("📋 BATCH HISTORY", fg='blue', bold=True))
    
    batches = list_all_batches()
    
    if not batches:
        click.echo(click.style("📭 No batches found", fg='yellow'))
        click.echo("💡 Submit your first batch: python script.py submit")
        return
    
    # Filter by status
    if status_filter != 'all':
        batches = [b for b in batches if b['status'] == status_filter]
    
    # Limit results
    batches = batches[:limit]
    
    if not batches:
        click.echo(click.style(f"📭 No batches with status '{status_filter}'", fg='yellow'))
        return
    
    click.echo(f"📊 Showing {len(batches)} batches (filtered by: {status_filter})")
    click.echo("-" * 80)
    
    for batch in batches:
        # Status color coding
        status_colors = {
            'submitted': 'yellow',
            'validating': 'yellow', 
            'in_progress': 'blue',
            'completed': 'green',
            'downloaded': 'green',
            'canceled': 'red',
            'failed': 'red'
        }
        
        status_color = status_colors.get(batch['status'], 'white')
        colored_status = click.style(batch['status'].upper(), fg=status_color, bold=True)
        
        click.echo(f"📋 {click.style(batch['batch_id'], fg='cyan')}")
        click.echo(f"   Status: {colored_status}")
        click.echo(f"   📅 Submitted: {click.style(batch['submitted_at'], fg='blue')}")
        click.echo(f"   📁 Input: {click.style(batch['input_file'], fg='yellow')}")
        click.echo(f"   🏷️  Prefix: {click.style(batch['prefix'], fg='green')}")
        click.echo(f"   🔤 Characters: {click.style(str(batch['character_count']), fg='magenta')}")
        click.echo(f"   🤖 Model: {click.style(batch['model'], fg='cyan')}")
        
        if batch['completed_at']:
            click.echo(f"   ✅ Completed: {click.style(batch['completed_at'], fg='green')}")
        
        if batch['notes']:
            click.echo(f"   📝 Notes: {click.style(batch['notes'], fg='cyan')}")
        
        # Quick action suggestions
        if batch['status'] in ['submitted', 'in_progress']:
            click.echo(f"   💡 Check: python script.py status {batch['batch_id']}")
        elif batch['status'] == 'completed':
            click.echo(f"   💡 Download: python script.py download {batch['batch_id']}")
        
        click.echo()
    
    # Summary statistics
    all_batches = list_all_batches()
    total_chars = sum(b['character_count'] for b in all_batches)
    completed_batches = len([b for b in all_batches if b['status'] in ['completed', 'downloaded']])
    
    click.echo(click.style("📈 SUMMARY", fg='blue', bold=True))
    click.echo(f"📊 Total batches: {click.style(str(len(all_batches)), fg='green')}")
    click.echo(f"✅ Completed: {click.style(str(completed_batches), fg='green')}")
    click.echo(f"🔤 Total characters processed: {click.style(str(total_chars), fg='magenta')}")


@cli.command()
@click.argument('batch_id')
@click.option('--notes', prompt=True, help='Update notes for this batch')
def update(batch_id, notes):
    """Update notes for a batch"""
    
    # Initialize database
    init_batch_db()
    
    batch_info = get_batch_info(batch_id)
    if not batch_info:
        click.echo(click.style(f"❌ Batch {batch_id} not found", fg='red'))
        return
    
    conn = sqlite3.connect('batch_history.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE batches SET notes = ? WHERE batch_id = ?
    ''', (notes, batch_id))
    
    conn.commit()
    conn.close()
    
    click.echo(click.style(f"✅ Updated notes for batch {batch_id}", fg='green'))
    click.echo(f"📝 New notes: {click.style(notes, fg='cyan')}")


@cli.command()
@click.option('--backup-file', default=f'batch_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
              help='Backup file name')
def backup(backup_file):
    """Backup all batch information to JSON file"""
    
    # Initialize database
    init_batch_db()
    
    batches = list_all_batches()
    
    if not batches:
        click.echo(click.style("📭 No batches to backup", fg='yellow'))
        return
    
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(batches, f, indent=2, ensure_ascii=False, default=str)
        
        click.echo(click.style(f"💾 Backup created successfully!", fg='green'))
        click.echo(f"📁 File: {click.style(backup_file, fg='cyan')}")
        click.echo(f"📊 Backed up {len(batches)} batches")
        
    except Exception as e:
        click.echo(click.style(f"❌ Backup failed: {e}", fg='red'))


@cli.command()
@click.argument('backup_file')
@click.option('--force', is_flag=True, help='Force restore even if batches already exist')
def restore(backup_file, force):
    """Restore batch information from JSON backup file"""
    
    if not os.path.exists(backup_file):
        click.echo(click.style(f"❌ Backup file '{backup_file}' not found", fg='red'))
        return
    
    # Initialize database
    init_batch_db()
    
    try:
        with open(backup_file, 'r', encoding='utf-8') as f:
            batches = json.load(f)
        
        conn = sqlite3.connect('batch_history.db')
        cursor = conn.cursor()
        
        restored = 0
        skipped = 0
        
        for batch in batches:
            try:
                cursor.execute('''
                    INSERT INTO batches (batch_id, submitted_at, input_file, prefix, model, character_count, status, completed_at, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    batch['batch_id'], batch['submitted_at'], batch['input_file'], 
                    batch['prefix'], batch['model'], batch['character_count'],
                    batch['status'], batch.get('completed_at'), batch.get('notes', '')
                ))
                restored += 1
            except sqlite3.IntegrityError:
                if force:
                    cursor.execute('''
                        UPDATE batches SET submitted_at=?, input_file=?, prefix=?, model=?, 
                               character_count=?, status=?, completed_at=?, notes=?
                        WHERE batch_id=?
                    ''', (
                        batch['submitted_at'], batch['input_file'], batch['prefix'], 
                        batch['model'], batch['character_count'], batch['status'],
                        batch.get('completed_at'), batch.get('notes', ''), batch['batch_id']
                    ))
                    restored += 1
                else:
                    skipped += 1
        
        conn.commit()
        conn.close()
        
        click.echo(click.style(f"✅ Restore completed!", fg='green'))
        click.echo(f"📥 Restored: {click.style(str(restored), fg='green')} batches")
        if skipped > 0:
            click.echo(f"⏭️  Skipped: {click.style(str(skipped), fg='yellow')} (already exist)")
            click.echo("💡 Use --force to overwrite existing batches")
        
    except Exception as e:
        click.echo(click.style(f"❌ Restore failed: {e}", fg='red'))

def ignore_mode(file_name, modes=["_realtime", "_batch"]):
    """Ignore mode name in file_name
    """
    fn = str(file_name)
    for m in modes:
        fn = fn.replace(m, "")
    return fn 

@cli.command()
@click.argument('characters', nargs=-1)
@click.option('--input-file', '-i', 
              help='Input file containing characters (alternative to direct input)')
@click.option('--prefix', '-p', default='claude4_realtime',
              help='Output file prefix')
@click.option('--model', '-m', default='claude-sonnet-4-20250514',
              help='Claude model to use')
@click.option('--max-tokens', default=6000, type=int,
              help='Maximum tokens per response')
@click.option('--temperature', default=0.3, type=float,
              help='Temperature for response generation')
@click.option('--delay', default=2.0, type=float,
              help='Delay between requests (seconds)')
@click.option('--interactive', '-i', is_flag=True,
              help='Interactive mode - prompts for each character')
def realtime(characters, input_file, prefix, model, max_tokens, temperature, delay, interactive):
    """Process characters in real-time mode (immediate results)
    
    Examples:
    \b
        python script.py realtime 水 火 土          # Process specific characters
        python script.py realtime --input-file small_list.txt  # Process from file
        python script.py realtime --interactive     # Interactive mode
    """
    
    click.echo(click.style("⚡ REAL-TIME PROCESSING MODE", fg='blue', bold=True))
    click.echo("🚀 Immediate results with rate limiting")
    click.echo("🧪 Perfect for testing and experimentation")
    click.echo("-" * 40)
    
    # Determine characters to process
    chars_to_process = []
    
    if interactive:
        click.echo("🔤 Interactive mode - enter characters one by one (empty to quit)")
        while True:
            char = click.prompt("Enter character", default="", show_default=False)
            if not char:
                break
            chars_to_process.append(char)
    elif input_file:
        chars_to_process = read_characters_from_file(input_file)
    elif characters:
        chars_to_process = list(characters)
    else:
        click.echo(click.style("❌ No characters provided", fg='red'))
        click.echo("💡 Usage: python script.py realtime 水 火 土")
        click.echo("💡    or: python script.py realtime --input-file chars.txt")
        click.echo("💡    or: python script.py realtime --interactive")
        return
    
    if not chars_to_process:
        click.echo(click.style("❌ No characters to process", fg='red'))
        return
    
    # Filter out already processed characters
    remaining_chars = []
    skipped = 0
    
    for zi in chars_to_process:
        json_file = f"{prefix}_{zi}.json"
        txt_file = f"{prefix}_{zi}.txt"
        
        if os.path.exists(ignore_mode(json_file)) or os.path.exists(ignore_mode(txt_file)):
            skipped += 1
            continue
        remaining_chars.append(zi)
    
    if skipped > 0:
        click.echo(f"⏭️  Skipped {skipped} already processed characters")
    
    if not remaining_chars:
        click.echo(click.style("ℹ️ All characters already processed!", fg='yellow'))
        return
    
    click.echo(f"🔤 Processing: {click.style(', '.join(remaining_chars), fg='cyan')}")
    click.echo(f"📊 Total: {click.style(str(len(remaining_chars)), fg='green')} characters")
    click.echo(f"🎯 Model: {click.style(model, fg='yellow')}")
    click.echo(f"⏱️  Delay: {delay}s between requests")
    
    # Cost estimate
    estimated_output_tokens = len(remaining_chars) * 3000
    estimated_input_tokens = len(remaining_chars) * 200
    realtime_cost = (estimated_output_tokens * 15 + estimated_input_tokens * 3) / 1_000_000
    batch_cost = realtime_cost * 0.5
    
    click.echo(f"💰 Estimated cost: {click.style(f'${realtime_cost:.2f}', fg='red')} (vs ${batch_cost:.2f} in batch mode)")
    
    if not click.confirm(click.style("\n❓ Start real-time processing?", fg='blue')):
        click.echo(click.style("❌ Processing cancelled", fg='red'))
        return
    
    # Process characters in real-time
    client = get_client()
    successful = 0
    failed = 0
    start_time = datetime.now()
    
    with click.progressbar(remaining_chars, label='Processing characters') as progress_chars:
        for i, zi in enumerate(progress_chars):
            try:
                click.echo(f"\n[{i+1:3d}/{len(remaining_chars)}] Processing: {click.style(zi, fg='cyan', bold=True)}")
                
                # Make API call
                message = client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
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
                
                # Extract response
                response_text = message.content[0].text
                clean_json = extract_json_from_response(response_text)
                
                # Validate and save
                try:
                    json.loads(clean_json)
                    file_name = f"{prefix}_{zi}.json"
                    content_to_save = clean_json
                    status_icon = "✅"
                    successful += 1
                except json.JSONDecodeError:
                    file_name = f"{prefix}_{zi}.txt"
                    content_to_save = response_text
                    status_icon = "⚠️"
                    successful += 1
                
                # Save file
                with open(ignore_mode(file_name), "w", encoding="utf-8") as f:
                    f.write(content_to_save)
                
                click.echo(f"    {status_icon} Saved: {click.style(file_name, fg='green')}")
                
                # Show progress every 5 characters
                if (i + 1) % 5 == 0:
                    elapsed = datetime.now() - start_time
                    rate = (i + 1) / elapsed.total_seconds() * 60
                    remaining = len(remaining_chars) - (i + 1)
                    eta_minutes = remaining / rate if rate > 0 else 0
                    click.echo(f"    📊 Progress: {successful} success, {failed} failed, {rate:.1f}/min, ETA: {eta_minutes:.1f}min")
                
                # Rate limiting (skip delay for last character)
                if i < len(remaining_chars) - 1:
                    time.sleep(delay)
                
            except Exception as e:
                logger.error(f"Error processing character '{zi}': {e}")
                click.echo(f"    ❌ Failed: {click.style(str(e), fg='red')}")
                failed += 1
    
    # Final summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    click.echo(click.style(f"\n🎯 REAL-TIME PROCESSING COMPLETE", fg='green', bold=True))
    click.echo(f"✅ Successful: {click.style(str(successful), fg='green')}")
    if failed > 0:
        click.echo(f"❌ Failed: {click.style(str(failed), fg='red')}")
    click.echo(f"⏰ Duration: {duration}")
    click.echo(f"📊 Average rate: {len(remaining_chars) / duration.total_seconds() * 60:.1f} characters/minute")
    click.echo(f"📁 Files saved with prefix: {click.style(prefix, fg='cyan')}")


@cli.command()
@click.option('--input-file', '-i', default='elemental_characters.txt',
              help='Input file to analyze')
def info(input_file):
    """Show information about input file and processing estimates"""
    
    click.echo(click.style("📊 ANALYSIS INFO", fg='blue', bold=True))
    
    # Check input file
    if not os.path.exists(input_file):
        click.echo(click.style(f"❌ Input file '{input_file}' not found", fg='red'))
        return
    
    characters = read_characters_from_file(input_file)
    requests = create_batch_requests(characters)
    
    click.echo(f"📖 Input file: {click.style(input_file, fg='cyan')}")
    click.echo(f"🔤 Total characters: {click.style(str(len(characters)), fg='green')}")
    click.echo(f"⚡ To process: {click.style(str(len(requests)), fg='yellow')}")
    click.echo(f"✅ Already done: {click.style(str(len(characters) - len(requests)), fg='green')}")
    
    if len(requests) > 0:
        # Cost estimates
        estimated_output_tokens = len(requests) * 3000
        estimated_input_tokens = len(requests) * 200
        standard_cost = (estimated_output_tokens * 15 + estimated_input_tokens * 3) / 1_000_000
        batch_cost = standard_cost * 0.5
        
        click.echo(f"\n💰 Cost estimates:")
        click.echo(f"   Standard API: {click.style(f'${standard_cost:.2f}', fg='red')}")
        click.echo(f"   Batch API:    {click.style(f'${batch_cost:.2f}', fg='green')} (50% savings)")
        click.echo(f"   You save:     {click.style(f'${standard_cost - batch_cost:.2f}', fg='blue')}")
        
        click.echo(f"\n⏰ Processing time:")
        click.echo(f"   Batch API: Within 24 hours (often much faster)")
        click.echo(f"   Standard:  ~{len(requests) * 30 / 3600:.1f} hours (30s per character)")


if __name__ == "__main__":
    cli()