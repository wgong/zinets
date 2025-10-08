"""
Search Character Network Page

Combines character search functionality with network decomposition visualization.
Allows users to search for characters containing specific parts and view their decomposition trees.
"""

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pyecharts import options as opts
from pyecharts.charts import Tree

from utils import *

st.set_page_config(layout="wide")
st.subheader("🔍 Search Character Network 🌐")

# Global variables for node management (from Zi Structure page)
NODE_MAP = {}
NODE_DUP = {}

def make_node_id(node):
    """Create unique node ID accounting for duplicates"""
    h = hash(node)
    if h in NODE_DUP:
        v = NODE_DUP.get(h)
        v.append(node)
    else:
        v = [node]
    NODE_DUP[h] = v
    return f"{h}-{str(len(v))}"

def search_characters_by_part(search_part):
    """
    Search for characters that contain the given part in any of the 11 positions.
    Returns a list of characters.
    """
    if not search_part.strip():
        return []

    # Use similar logic to Zi Composer page
    where_clause = f"""
        (
            zi.zi like '%{search_part}%'
            OR zp.zi_left_up like '%{search_part}%'
            OR zp.zi_left like '%{search_part}%'
            OR zp.zi_left_down like '%{search_part}%'
            OR zp.zi_up like '%{search_part}%'
            OR zp.zi_mid like '%{search_part}%'
            OR zp.zi_down like '%{search_part}%'
            OR zp.zi_right_up like '%{search_part}%'
            OR zp.zi_right like '%{search_part}%'
            OR zp.zi_right_down like '%{search_part}%'
            OR zp.zi_mid_out like '%{search_part}%'
            OR zp.zi_mid_in like '%{search_part}%'
        )
    """

    sql_stmt = f"""
        SELECT DISTINCT zi.zi
        FROM t_zi zi
        LEFT JOIN t_zi_part zp ON zi.zi = zp.zi
        WHERE {where_clause}
            AND zi.is_active = 'Y'
            AND CAST(zi.u_id as real) > 0
        ORDER BY CAST(zi.u_id as real)
    """

    with DBConn() as _conn:
        df = pd.read_sql(sql_stmt, _conn)

    return df['zi'].tolist() if not df.empty else []

def get_character_decomposition_tree(root_zi, union_uniq=True):
    """
    Get the decomposition tree for a given character using recursive SQL.
    Returns DataFrame with zi-part relationships.
    """
    union_op = " UNION " if union_uniq else " UNION ALL "

    sql_stmt = f"""
    WITH RECURSIVE
      zi_part_v(zi, part) as (
        select zi,part from (
            select zi, zi_left_up as part from t_zi_part where zi_left_up is not null
             union all
            select zi, zi_left as part from t_zi_part where  zi_left is not null
             union all
            select zi, zi_left_down as part from t_zi_part where  zi_left_down is not null
             union all
            select zi, zi_up as part from t_zi_part where  zi_up is not null
             union all
            select zi, zi_mid as part from t_zi_part where   zi_mid is not null
             union all
            select zi, zi_down as part from t_zi_part where  zi_down is not null
             union all
            select zi, zi_right_up as part from t_zi_part where  zi_right_up is not null
             union all
            select zi, zi_right as part from t_zi_part where  zi_right is not null
             union all
            select zi, zi_right_down as part from t_zi_part where  zi_right_down is not null
             union all
            select zi, zi_mid_out as part from t_zi_part where  zi_mid_out is not null
             union all
            select zi, zi_mid_in as part from t_zi_part where  zi_mid_in is not null
        )
        where zi is not null and part is not null and zi != '' and part != ''
    ),
      child_of(zi, part) AS (
            SELECT zi, part
            FROM zi_part_v WHERE zi='{root_zi}'
        {union_op}
             SELECT zp.zi, zp.part
             FROM  zi_part_v zp join child_of c
                 on zp.zi = c.part
    )
    SELECT * FROM child_of
    """

    with DBConn() as _conn:
        df = pd.read_sql(sql_stmt, _conn)

    return df

def convert_d3graph_to_tree(df, pkg_name="pyecharts"):
    """Convert decomposition DataFrame to tree structure"""
    if df.empty:
        return None

    # Create nodes dictionary
    nodes = {}
    for source, target in df.itertuples(index=False):
        nodes[source] = nodes.get(source, []) + [target]

    # Find root node
    children_nodes = []
    for node in nodes:
        children_nodes.extend(nodes[node])

    root_node = None
    for node in nodes:
        if node not in children_nodes:
            root_node = node
            break

    if not root_node:
        return None

    if pkg_name == "pyecharts":
        return build_tree_pyecharts(root_node, nodes)
    else:
        return build_tree_st_select(root_node, nodes)

def build_tree_pyecharts(node, nodes):
    """Build tree structure for pyecharts"""
    children = nodes.get(node, [])
    if not children:
        return {"name": node}
    tree_node = {"name": node, "children": []}
    for child in children:
        tree_node["children"].append(build_tree_pyecharts(child, nodes))
    return tree_node

def build_tree_st_select(node, nodes):
    """Build tree structure for streamlit tree select"""
    children = nodes.get(node, [])
    node_id = make_node_id(node)
    NODE_MAP[node_id] = node
    if not children:
        return {"label": node, "value": node_id}
    tree_node = {"label": node, "value": node_id, "children": []}
    for child in children:
        tree_node["children"].append(build_tree_st_select(child, nodes))
    return tree_node

def tree_to_markdown(tree_data, indent=0):
    """Convert tree structure to markdown format"""
    if not tree_data:
        return ""

    markdown = ""
    indent_str = "  " * indent

    if isinstance(tree_data, dict):
        name = tree_data.get('name', '')
        if name:
            if indent == 0:
                markdown += f"{name}\n"
            else:
                markdown += f"{indent_str}- {name}\n"

            children = tree_data.get('children', [])
            for child in children:
                markdown += tree_to_markdown(child, indent + 1)

    return markdown

def select_node(data, key_filter=["name"]):
    """Extract nodes from tree structure"""
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str):
                if (not key_filter or key in key_filter):
                    yield key, value
            else:
                yield from select_node(value, key_filter)
    elif isinstance(data, list):
        for item in data:
            yield from select_node(item, key_filter)

def main():
    # Initialize session state
    if 'character_network' not in st.session_state:
        st.session_state.character_network = {}
    if 'selected_character' not in st.session_state:
        st.session_state.selected_character = None
    if 'search_results' not in st.session_state:
        st.session_state.search_results = []

    # Search interface
    col1, col2 = st.columns([3, 1])
    with col1:
        search_part = st.text_input("🔍 Search for characters containing this part:",
                                   value="心", key="search_part")
    with col2:
        search_button = st.button("Search", type="primary")

    # Perform search
    if search_button or (search_part and search_part != st.session_state.get('last_search', '')):
        if search_part.strip():
            with st.spinner(f"Searching for characters containing '{search_part}'..."):
                results = search_characters_by_part(search_part)
                st.session_state.search_results = results
                st.session_state.last_search = search_part
                st.success(f"Found {len(results)} characters containing '{search_part}'")
        else:
            st.session_state.search_results = []

    # Display character buttons (20 per row)
    if st.session_state.search_results:
        st.subheader(f"Characters containing '{search_part}' ({len(st.session_state.search_results)} found):")

        # Create buttons in rows of 20
        chars_per_row = 20
        results = st.session_state.search_results

        for i in range(0, len(results), chars_per_row):
            row_chars = results[i:i + chars_per_row]
            cols = st.columns(len(row_chars))

            for j, char in enumerate(row_chars):
                with cols[j]:
                    if st.button(char, key=f"char_btn_{i}_{j}"):
                        st.session_state.selected_character = char
                        # Generate decomposition for selected character
                        if char not in st.session_state.character_network:
                            with st.spinner(f"Analyzing character '{char}'..."):
                                df = get_character_decomposition_tree(char)
                                tree_data = convert_d3graph_to_tree(df, "pyecharts")
                                if tree_data:
                                    markdown_tree = tree_to_markdown(tree_data)
                                    st.session_state.character_network[char] = {
                                        'tree_data': tree_data,
                                        'markdown': markdown_tree,
                                        'df': df
                                    }
                                else:
                                    st.session_state.character_network[char] = {
                                        'tree_data': None,
                                        'markdown': f"{char}\n  - (No decomposition data available)",
                                        'df': pd.DataFrame()
                                    }

    # Display selected character analysis
    if st.session_state.selected_character:
        char = st.session_state.selected_character
        st.subheader(f"Character Analysis: {char}")

        if char in st.session_state.character_network:
            network_data = st.session_state.character_network[char]

            # Create two columns for markdown and visualization
            col_left, col_right = st.columns([1, 4])

            with col_left:
                st.subheader("Markdown Tree")
                st.code(network_data['markdown'], language='markdown')

            with col_right:
                st.subheader("Visual Tree")
                tree_data = network_data['tree_data']

                if tree_data:
                    # Extract all parts for title
                    zi_parts = []
                    for z in select_node(tree_data):
                        if z[1] not in zi_parts:
                            zi_parts.append(z[1])
                    part_str = ", ".join(zi_parts)

                    # Create pyecharts tree
                    label_opts = opts.LabelOpts(font_size=30, color="red")
                    html_data = (
                        Tree()
                        .add("", [tree_data], symbol="rect", symbol_size=40, label_opts=label_opts)
                        .set_global_opts(title_opts=opts.TitleOpts(title=f"{char}: {part_str}"))
                        .render_embed()
                    )

                    # Display in streamlit
                    components.html(html_data, scrolling=True, height=400)
                else:
                    st.info("No decomposition data available for this character.")
        else:
            st.info("Click on a character button above to see its decomposition.")

    # Display statistics
    if st.session_state.search_results:
        with st.expander("Statistics", expanded=False):
            st.write(f"**Search term:** {search_part}")
            st.write(f"**Characters found:** {len(st.session_state.search_results)}")
            st.write(f"**Characters analyzed:** {len(st.session_state.character_network)}")

            if st.session_state.character_network:
                st.write("**Analyzed characters:**")
                analyzed_chars = list(st.session_state.character_network.keys())
                st.write(" ".join(analyzed_chars))

if __name__ == '__main__':
    main()