# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ZiNets is a Streamlit-based web application for studying Chinese characters using the **Zi-Matrix approach** to decompose 5000 Chinese characters into their basic radical components. The application provides an interactive tool for analyzing character structure, decomposition patterns, and relationships between elemental characters.

## Technology Stack

- **Framework**: Streamlit (Python web framework)
- **Database**: SQLite for data persistence
- **UI Components**:
  - streamlit-aggrid for data grids
  - streamlit-option-menu for navigation
  - streamlit-tree-select for hierarchical data
- **Data Processing**: pandas, sqlite3
- **Chinese Language Processing**: pypinyin for pronunciation analysis
- **Text Similarity**: rapidfuzz for character comparison

## Development Commands

### Running the Application
```bash
# Start the Streamlit app
streamlit run ZiNets.py

# Alternative using shell script
./001_run_app.sh
```

### Dependencies
```bash
# Install required packages
pip install -r requirements.txt
```

## Core Architecture & Zi-Matrix Approach

### Character Decomposition Matrix
The application uses a **positional matrix system** to decompose Chinese characters into component parts:

- **Spatial Positions**: `zi_left_up`, `zi_up`, `zi_right_up`, `zi_left`, `zi_mid`, `zi_right`, `zi_left_down`, `zi_down`, `zi_right_down`
- **Special Positions**: `zi_mid_in` (inner components), `zi_mid_out` (outer components)

This 11-position matrix allows systematic decomposition of complex characters into their elemental parts.

### Database Schema

#### Core Tables
- `t_zi`: Main character table (5000+ Chinese characters)
- `t_ele_zi`: Elemental characters (basic building blocks/radicals)
- `t_zi_part`: Character decomposition data using the matrix approach
- `t_zi_part_pinyin`: Pronunciation similarity analysis between characters and components

#### Key Columns in t_zi_part
```sql
zi text,                    -- Main character
zi_left_up, zi_up, zi_right_up,    -- Top row positions
zi_left, zi_mid, zi_right,          -- Middle row positions
zi_left_down, zi_down, zi_right_down, -- Bottom row positions
zi_mid_in, zi_mid_out,             -- Special inner/outer positions
desc_cn, desc_en,                  -- Descriptions
is_active                          -- Status flag
```

## Application Structure

### Main Entry Point
- `ZiNets.py`: Main application entry point that loads README and sets up configuration

### Core Modules
- `utils.py`: Database operations, UI utilities, character processing functions
- `ui_layout.py`: UI configuration and form layouts for all data tables

### Key Pages (pages/ directory)
1. **元字 Editor**: Manage elemental characters (basic radicals)
2. **字分解 Zi Composer**: Interactive character decomposition using the matrix approach
3. **字典 Zi Editor**: Character dictionary management
4. **字形 Zi Structure**: Character structure analysis
5. **笔记 Notes**: Note-taking and documentation
6. **语文-数学-科学教材 Textbook**: Educational content management

## Key Features

### Character Decomposition (Zi Composer)
- Visual matrix interface for decomposing characters into positional components
- Real-time part selection from organized elemental character library
- Search and filter capabilities across decomposition data
- Export functionality for analysis

### Elemental Character Management
- Categorization system for radicals and basic components
- Frequency analysis showing how often each element appears in other characters
- Kangxi radical integration
- Pinyin pronunciation tracking

### Data Analysis Capabilities
- Character composition pattern analysis
- Pronunciation similarity calculations between characters and their phonetic components
- Statistical reporting on character frequency and usage
- Cross-referencing with HSK (Chinese proficiency test) levels

## Configuration

### Database Configuration
- Default database: `zi.sqlite` (can be changed in CFG["DB_FILENAME"])
- Supports multiple database formats for different development stages

### UI Configuration
- Wide layout optimized for character decomposition interface
- Configurable grid pagination and display options
- Multi-column form layouts defined in `ui_layout.py`

## Development Workflow

### Adding New Characters
1. Use "字典 Zi Editor" page to add basic character information
2. Use "字分解 Zi Composer" to define decomposition using the matrix approach
3. Validate against elemental character library in "元字 Editor"

### Data Analysis
- Use built-in frequency analysis tools to identify common patterns
- Export CSV data for external analysis
- Cross-reference with educational standards (HSK levels)

### Database Operations
- All database operations go through `utils.py` functions
- Supports both development and production SQL execution modes
- Built-in debugging and logging capabilities

## Important Implementation Details

### Character Matrix System
The core innovation is the systematic decomposition approach that maps any Chinese character to an 11-position matrix, enabling:
- Consistent decomposition methodology across all characters
- Pattern recognition for similar character structures
- Automated analysis of component frequency and relationships

### Pronunciation Analysis
- Integration with pypinyin for pronunciation extraction
- Similarity calculation between characters and their phonetic components
- Support for heteronym analysis (multiple pronunciations)

### Educational Integration
- HSK level mapping for educational sequencing
- Category-based organization for systematic learning
- Multi-language support (Chinese and English descriptions)

This application represents a comprehensive digital approach to understanding Chinese character composition and structure through systematic decomposition and analysis.