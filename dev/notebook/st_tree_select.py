import pandas as pd

import streamlit as st
from streamlit_tree_select import tree_select
import streamlit.components.v1 as components

from pyecharts import options as opts
from pyecharts.charts import Tree

st.set_page_config(
     page_title='字子',
     layout="wide",
     initial_sidebar_state="expanded",
)

NODE_VALUE = {}  
# key=NODE_VALUE where NODE_VALUE is hash(node)
# value=list of node_label to account for duplicates

def make_node_id(node):
    # create unique id
    # key=NODE_VALUE where NODE_VALUE is hash(node)
    # value=list of node_label to account for duplicates    
    h = hash(node)
    if h in NODE_VALUE:
        v = NODE_VALUE.get(h)
        v.append(node)
    else: 
        v = [node]
    NODE_VALUE[h] = v
    return f"{h}-{str(len(v))}"

def convert_d3graph_to_tree(df, pkg_name="st_tree_select"):
    """Converts d3graph data structure to specific pkg node structure."""
    # Create a dictionary to store nodes and their children
    nodes = {}
    for source, target in df.itertuples(index=False):
        nodes[source] = nodes.get(source, []) + [target]

    # Build the tree structure recursively
    root = get_root_note(nodes)
    
    if pkg_name == "st_tree_select":
        return build_tree_st_select(root, nodes) 
    elif pkg_name == "pyecharts":
        return build_tree_pyecharts(root, nodes) 
    else:
        raise Exception(f"Unknown target: {pkg_name}")

def get_root_note(nodes):
    children_nodes = []
    for node in nodes:
        children_nodes.extend(nodes[node])
    for node in nodes:
        if node in children_nodes:
            continue
        return node

# Build the tree structure recursively
def build_tree_st_select(node, nodes):
    children = nodes.get(node, [])
    node_id = make_node_id(node)
    if not children:
        return {"label": node, "value": node_id}
    tree_node = {"label": node, "value": node_id, "children": []}
    for child in children:
        tree_node["children"].append(build_tree_st_select(child, nodes))
    return tree_node

def build_tree_pyecharts(node, nodes):
    children = nodes.get(node, [])
    if not children:
        return {"name": node}
    tree_node = {"name": node, "children": []}
    for child in children:
        tree_node["children"].append(build_tree_pyecharts(child, nodes))
    return tree_node

def select_node(data, key_filter=["name"]):
    """
    Traverses a dictionary of unlimited depth and width, yielding key-value pairs
    where the value is a string and optionally matches specific keys.

    Args:
        data: The dictionary to traverse.
        keys_filter (list, optional): A list of keys to filter for. If None,
            all string values are yielded. Defaults to None.

    Yields:
        tuple: A tuple containing the key and value from the dictionary.
        
    Example usage:
        my_dict = {
            "a": 1,
            "b": {
                "name": "Alice",
                "c": "hello",
                "d": [3, {"description": "world"}]
            },
            "f": [5, "world"]
        }

        # Extract all string values:
        for key, value in traverse_dict(my_dict):
            print(f"{key}: {value}")

        # Extract specific keys:
        for key, value in traverse_dict(my_dict, ["name", "description"]):
            print(f"{key}: {value}")
    
    """    
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value,str):
                if (not key_filter or key in key_filter):
                    yield key, value
            else:
                yield from select_node(value, key_filter)  # Recursively traverse nested values
    elif isinstance(data, list):
        for item in data:
            yield from select_node(item, key_filter)  # Handle lists within the dictionary

if "selected" not in st.session_state:
    st.session_state.selected = []
if "expanded" not in st.session_state:
    st.session_state.expanded = []


st.title("🐙 Streamlit-tree-select")
st.subheader("A simple and elegant checkbox tree for Streamlit.")

# Create nodes to display
df = pd.read_csv("zi_data.csv")
nodes_zi = [convert_d3graph_to_tree(df, pkg_name="st_tree_select")]
# nodes_zi = [
#     {
#         "label": "藻", "value": "藻",
#         "children": [
#             {"label": "艹", "value": "艹"},
#             {
#                 "label": "喿", "value": "喿",
#                 "children": [
#                     {
#                         "label": "品", "value": "品",
#                         "children": [
#                             {"label": "口", "value": "口-1"},
#                             {"label": "口", "value": "口-2"},
#                             {"label": "口", "value": "口-3"},
#                         ], 
#                     }, 
#                     {"label": "木", "value": "木"},
#                 ],
#             },
#         ],
#     },
# ]


selected = tree_select(nodes_zi, 
                    checked=st.session_state.selected, 
                    expanded=st.session_state.expanded,
                    # only_leaf_checkboxes=True, 
                    no_cascade=True,
                )
            
                    
if len(selected["checked"]) > 1:
    st.session_state.selected = [x for x in selected["checked"] if x != st.session_state.selected[0]][0:1]
    st.session_state.expanded = selected["expanded"]
    # st.experimental_rerun()
    st.rerun()
    
else:
    st.session_state.selected = selected["checked"]
    st.session_state.expanded = selected["expanded"]  
    
st.write(selected)

# display html page
st.subheader("Display HTML page")
nodes_zi_2 = convert_d3graph_to_tree(df, pkg_name="pyecharts")
data_zi_2 = [nodes_zi_2]
zi_parts = []
for z in select_node(nodes_zi_2):
    if z[1] not in zi_parts:
        zi_parts.append(z[1])
part_str = ", ".join(zi_parts)

label_opts = opts.LabelOpts(font_size=50, color="red")
html_data = (
    Tree()
    .add("", data_zi_2, symbol="rect", symbol_size=60, label_opts=label_opts)
    .set_global_opts(title_opts=opts.TitleOpts(title=part_str))
    .render_embed()   # return HTML content instead of writing to file
)

file_html = "tree_zi.html"
with open(file_html, "w", encoding="utf-8") as f: 
    f.write(html_data)

# https://discuss.streamlit.io/t/display-an-html-file-in-streamlit/56579
with open(file_html, 'r', encoding='utf-8') as f:
    html_data_2 = f.read() 
    ##  use html()
    components.html(html_data_2, scrolling=True, height=500)
    # NOT working
    # st.markdown(html_data,  unsafe_allow_html=True)  





