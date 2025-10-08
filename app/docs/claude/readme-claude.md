# ZiNets search by part

## Implementation Complete ✅

**Page Created:** `/home/papagame/projects/wgong/zistory/zinets/app/zadmin/pages/5-Search-Character-Network.py`

### Features Implemented

1. **Character Search by Part**
   - Search box to find all characters containing a specific part (e.g., "心")
   - Searches across all 11 positions in the `t_zi_part` table:
     - `zi_left_up`, `zi_left`, `zi_left_down`
     - `zi_up`, `zi_mid`, `zi_down`
     - `zi_right_up`, `zi_right`, `zi_right_down`
     - `zi_mid_out`, `zi_mid_in`
   - Returns list of matching characters sorted by `u_id`

2. **Character Display**
   - Results displayed as clickable buttons (20 per row)
   - Shows total count of found characters
   - Example: Searching "心" returns 85+ characters

3. **Character Decomposition**
   - Click any character button to view its decomposition tree
   - Uses recursive SQL query to build complete decomposition hierarchy
   - Generates both markdown and visual representations

4. **Dual Visualization**
   - **Left panel:** Markdown tree structure
   - **Right panel:** Interactive pyecharts tree visualization
   - Example markdown format:
     ```markdown
     愁
       - 秋
         - 禾
           - 丿
           - 木
         - 火
       - 心
     ```

5. **Data Management**
   - Character networks cached in session state for performance
   - Decomposition data stored in `character_network` dictionary:
     ```python
     {
       "愁": {
         'tree_data': {...},      # pyecharts tree structure
         'markdown': "...",       # markdown representation
         'df': DataFrame(...)     # decomposition relationships
       }
     }
     ```

6. **Statistics Panel**
   - Expandable statistics showing:
     - Search term used
     - Total characters found
     - Number of characters analyzed
     - List of analyzed characters

### Technical Implementation

**Database Queries:**
- Search query joins `t_zi` and `t_zi_part` tables
- Recursive CTE (Common Table Expression) for tree decomposition
- UNION ALL to combine all 11 part positions

**UI Components:**
- Streamlit columns layout for responsive design
- Dynamic button grid (20 characters per row)
- Pyecharts Tree chart with custom styling (red labels, 30px font)
- HTML components embedding for interactive visualization

**Session State:**
- `search_results`: List of matching characters
- `selected_character`: Currently selected character
- `character_network`: Cache of decomposition data
- `last_search`: Track search history

### Usage Example

1. Enter "心" in search box
2. Click "Search" button
3. System finds 85+ characters containing "心"
4. Characters displayed as clickable buttons
5. Click any character (e.g., "愁")
6. View markdown tree and visual decomposition
7. Repeat for other characters - data is cached for speed

---

# Original Requirements

Create a new page called 
`/home/papagame/projects/wgong/zistory/zinets/app/zadmin/pages/6-Search-Character-Network.py`

It combines features from the following 2 pages:

(1) on page /home/papagame/projects/wgong/zistory/zinets/app/zadmin/pages/2-字分解 Zi Composer.py

one enters "心" in "Search parts" input_text widget,
it found 85 Chinese characters that contain "心" as its part. 
see `search-by-parts.png`

returns the following list stored in `characters` var

```python
characters = [
'想', '憃', '总', '㤅', '悲', '惫', '必', '憋', '惩', '愁', '慈', '怠', '愓', '德', '憝', '恩', '忿', '感', '恭', '憨', '忽',
  '患', '恚', '惠', '慧', '慁', '惑', '急', '忌', '惎', '恳', '恐', '恋', '虑', '懋', '闷', '忞', '愍', '慕', '戁', '恁', '惄', '念', '您',
  '怒', '恧', '愆', '沁', '惹', '忍', '愼', '恕', '思', '态', '忒', '㥏', '忘', '慰', '恶', '息', '悉', '憙', '憸', '憪', '芯', '悬', '恙',
  '意', '慇', '㥯', '悠', '愚', '悆', '怨', '愿', '怎', '悊', '志', '忠', '恣', '㦌', '惢', '怱'
]
```

(2) on page /home/papagame/projects/wgong/zistory/zinets/app/zadmin/pages/4-字形 Zi Structure.py, I can build character network for any given character

see `愁-decomposed.png`

e.g. 愁 will be decomposed and represented as a markdown snippet 

repeat above for each character from `characters` list,

save them in the following dict

```python
character_network = {
    "愁" : """
愁
  - 秋
    - 禾
      - 丿
      - 木
    - 火
  - 心
    """,
}
```

In the end, this new streamlit page will have
- search box
- display found characters as a list of buttons will character as its label
- when clicked, it will show both markdown representation of the character-network and its visual chart


# Questions and Answers

1. Search Functionality:
  - Should the search work like the current "Search parts" feature where entering "心" finds all characters containing that part?
  - Should it support searching for multiple parts simultaneously?

[Answer] if you read the SQL query, it find all characters that contain the given search character as a part in one of the 11 positions. 
No need to render them in st.aggrid()
simply list them as clickable link or button

2. Character Decomposition:
  - I need to understand how page "4-字形 Zi Structure.py" generates the decomposition tree. Could you show me that page or explain the
logic it uses to create the markdown tree structure?
  - Does it use the same t_zi_part table with the 11-position matrix to build the tree?

[Answer] that page has all the SQL query and helper to build the data structure for visualization, I can explain later if it is not clear to you after reviewing the python code behind that page

3. UI Layout:
  - For the character buttons, how many should be displayed per row?
  - Should the markdown and visual chart be displayed side-by-side or one above the other?
  - What kind of visual chart do you want - a tree diagram, network graph, or something else?

[Answer] for inital prototype, just list them 20 per row, 
and reuse current tree diagram for visualization 

4. Visual Chart Implementation:
  - What library should I use for the visual chart? (pyecharts, plotly, streamlit built-in charts, etc.)
  - Should it be interactive (clickable nodes)?

[Answer] just display the tree, we will do the rendering in another app later 

5. Data Storage:
  - Should the character_network dict be cached/saved somewhere, or generated on-demand?

[Answer] store them in memory for now