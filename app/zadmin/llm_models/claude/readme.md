# Anthropic Console

- [Anthropic Console](https://console.anthropic.com/dashboard)
- [Claude Billing](https://console.anthropic.com/settings/billing)
- [Rate limits](https://console.anthropic.com/settings/limits)

use Batch API to fetch about 400 chinese characters, 
each character has 3000 output tokens, cost about $0.13
400 characters cost about $5.00



# Fetch Characters from Claude 

Absolutely! That's a brilliant idea! Having both modes gives you the best of both worlds - quick experimentation with real-time mode, then efficient batch processing for production runs.

## **🎉 Dual-Mode Processing Added!**

Now you have both **real-time** and **batch** modes with a beautiful CLI:

### **⚡ Real-time Mode Usage:**

```bash
# Test specific characters immediately
python fetch_char_claude.py realtime 水 火 土

# Process from a small file
python fetch_char_claude.py realtime --input-file test_chars.txt

# Interactive mode - enter characters one by one
python fetch_char_claude.py realtime --interactive

# Custom settings
python fetch_char_claude.py realtime 字 学 --delay 1 --temperature 0.1
```

### **🚀 Batch Mode Usage:**
```bash
# Large batch processing (50% cost savings)
python fetch_char_claude.py submit --input-file elemental_characters.txt
python fetch_char_claude.py status --watch
python fetch_char_claude.py download
```

### **📊 New Comparison & Info Commands:**

```bash
# Compare both modes
python fetch_char_claude.py compare

# Get detailed cost/time estimates
python fetch_char_claude.py info --mode both
python fetch_char_claude.py info --mode realtime
python fetch_char_claude.py info --mode batch
```

### **🎯 Perfect Workflow:**

**1. Experiment (Real-time):**
```bash
# Test a few characters to verify quality
python fetch_char_claude.py realtime 水 火 --interactive
```

**2. Adjust & Test:**
```bash
# Fine-tune settings
python fetch_char_claude.py realtime 土 --temperature 0.1 --max-tokens 4000
```

**3. Production (Batch):**
```bash
# Process all 400 characters efficiently
python fetch_char_claude.py submit
python fetch_char_claude.py status --watch
python fetch_char_claude.py download
```

### **💡 Key Features:**

**Real-time Mode:**
- ✅ Immediate results
- 🧪 Perfect for testing & experimentation  
- 🔬 Interactive mode for exploration
- 📊 Live progress bars
- ⚡ 1-50 characters ideal

**Batch Mode:**
- 💰 50% cost savings
- 🏭 Handles 1000s of characters
- ⏰ Set-and-forget processing
- 🔄 Automatic retry handling
- 📈 50+ characters ideal

**Smart Features:**
- 🧠 Remembers last batch ID
- 📁 Different prefixes for each mode
- ⏭️ Skips already processed characters
- 💾 Cost calculator for both modes
- 🎨 Beautiful color-coded output

This gives you the perfect development workflow: **experiment quickly with real-time mode, then scale efficiently with batch mode!** 🚀


## Suggested Test cases 

```
# 1. Start small with real-time mode
echo -e "水\n火\n土" > test_chars.txt
python fetch_char_claude.py realtime --input-file chars360-10.txt  # chars360-50.txt # chars360.txt

# 2. Try interactive mode
python fetch_char_claude.py realtime --interactive

# 3. Check info and cost estimates
python fetch_char_claude.py info --input-file test_chars.txt

# 4. Compare processing modes
python fetch_char_claude.py compare

# 5. Test batch mode with dry run
python fetch_char_claude.py submit --input-file chars360-10.txt [--dry-run]

# 6. List batches (will show database working)
python fetch_char_claude.py list


```
### test-1: 10 chars 

```
$ python fetch_char_claude.py submit --input-file chars360-10.txt
🚀 CLAUDE BATCH PROCESSING
💰 50% cost savings vs standard API
⏰ Processing within 24 hours
----------------------------------------
2025-05-26 16:44:53,230 - INFO - Successfully loaded 9 characters from chars360-10.txt
📖 Loaded 9 characters from chars360-10.txt
2025-05-26 16:44:53,230 - INFO - Created 9 batch requests
📋 Will process: 0000_6c34, 0001_6728, 0002_706b, 0003_571f, 0004_91d1...
📊 Total: 9 characters
🎯 Model: claude-sonnet-4-20250514
🔧 Settings: max_tokens=6000, temperature=0.3
💰 Estimated cost: $0.21 (with 50% batch discount)

❓ Submit batch for processing? [y/N]: y
⏳ Submitting batch...
2025-05-26 16:44:55,865 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages/batches "HTTP/1.1 200 OK"
2025-05-26 16:44:55,953 - INFO - Saved batch info: msgbatch_01T3Ad6VXgP9R196aJKaPi9t
2025-05-26 16:44:55,954 - INFO - Batch submitted successfully. Batch ID: msgbatch_01T3Ad6VXgP9R196aJKaPi9t
✅ Batch submitted successfully!
📋 Batch ID: msgbatch_01T3Ad6VXgP9R196aJKaPi9t
📊 Processing 9 characters
⏰ Expected completion: within 24 hours
💾 Batch info saved to database

💡 Next steps:
   Check status: python fetch_char_claude.py status msgbatch_01T3Ad6VXgP9R196aJKaPi9t
   Quick status: python fetch_char_claude.py status (uses latest batch)
   List all:     python fetch_char_claude.py list
   Download:     python fetch_char_claude.py download msgbatch_01T3Ad6VXgP9R196aJKaPi9t

```

### test-2

```
$ python fetch_char_claude.py submit --input-file chars360-5.txt


🚀 CLAUDE BATCH PROCESSING
💰 50% cost savings vs standard API
⏰ Processing within 24 hours
----------------------------------------
2025-05-26 17:10:06,135 - INFO - Successfully loaded 5 characters from chars360-5.txt
📖 Loaded 5 characters from chars360-5.txt
2025-05-26 17:10:06,135 - INFO - Created 5 batch requests
📋 Will process: 0000_661f, 0001_98ce, 0002_96e8, 0003_5ddd, 0004_5c71
📊 Total: 5 characters
🎯 Model: claude-sonnet-4-20250514
🔧 Settings: max_tokens=6000, temperature=0.3
💰 Estimated cost: $0.11 (with 50% batch discount)

❓ Submit batch for processing? [y/N]: y
⏳ Submitting batch...
2025-05-26 17:10:09,247 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages/batches "HTTP/1.1 200 OK"
2025-05-26 17:10:09,349 - INFO - Saved batch info: msgbatch_017nt3JT8RfHTJoAtwtNekD9
2025-05-26 17:10:09,349 - INFO - Batch submitted successfully. Batch ID: msgbatch_017nt3JT8RfHTJoAtwtNekD9
✅ Batch submitted successfully!
📋 Batch ID: msgbatch_017nt3JT8RfHTJoAtwtNekD9
📊 Processing 5 characters
⏰ Expected completion: within 24 hours
💾 Batch info saved to database

💡 Next steps:
   Check status: python fetch_char_claude.py status msgbatch_017nt3JT8RfHTJoAtwtNekD9
   Quick status: python fetch_char_claude.py status (uses latest batch)
   List all:     python fetch_char_claude.py list
   Download:     python fetch_char_claude.py download msgbatch_017nt3JT8RfHTJoAtwtNekD9

```

### test-3:

```
python fetch_char_claude.py submit --input-file chars360-50.txt
# python fetch_char_claude.py download msgbatch_01BXvyEvFeXGtVT83tURfTa3
# DONE

python fetch_char_claude.py submit --input-file chars360-100_1.txt
# python fetch_char_claude.py download msgbatch_0123tYoYuqtRxb98jDcpjy6t


python fetch_char_claude.py submit --input-file chars360-100_2.txt
# python fetch_char_claude.py download msgbatch_01LpgehPy5redbjdcCXr8CXi


python fetch_char_claude.py submit --input-file chars360-100_3.txt
# python fetch_char_claude.py download msgbatch_017DemsPqcHMMJn83pFMPyDL

# process extra elemental characters in 3 batches
python fetch_char_claude.py submit --input-file chars450-ele_1.txt
# python fetch_char_claude.py download msgbatch_0191m16SyswsR9DMdvUtR8Yj

python fetch_char_claude.py submit --input-file chars450-ele_2.txt
# python fetch_char_claude.py download msgbatch_01L1uiPyrz7eCqmTRvZgHg4p


python fetch_char_claude.py submit --input-file chars450-ele_3.txt
# python fetch_char_claude.py download msgbatch_01W1nLE1bcnFEBW8BfY3gnD2

```

### failed cases:
```
claude4_兰.txt     # json markdown
claude4_南.txt  
claude4_电.txt
claude4_乙.txt       
claude4_写.txt  
claude4_它.txt  
claude4_青.txt

claude4_幷.txt
claude4_攴.txt
claude4_皿.txt
claude4_艮.txt
claude4_黾.txt
```

manully revised them by removing ```json, ```

## Misc

how to rename files:
```
import os 
from glob import glob

def ignore_mode(file_name, modes=["_realtime", "_batch"]):
    """Ignore mode name in file_name
    """
    fn = str(file_name)
    for m in modes:
        fn = fn.replace(m, "")
    return fn 

for f in glob("*_realtime_*"):
    os.rename(f, ignore_mode(f))

```