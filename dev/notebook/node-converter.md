`d3graph` data structure:

```
source,target
node1,node2
node1,node3
node3,node4
node3,node6
node4,node5-1
node4,node5-2
node4,node5-3
```



`streamlit_tree_select` node data structure:

```
nodes = [
    {
        "label": "node1", "value": "node1",
        "children": [
            {"label": "node2", "value": "node2"},
            {
                "label": "node3", "value": "node3",
                "children": [
                    {
                        "label": "node4", "value": "node4",
                        "children": [
                            {"label": "node5", "value": "node5-1"},
                            {"label": "node5", "value": "node5-2"},
                            {"label": "node5", "value": "node5-3"},
                        ], 
                    }, 
                    {"label": "node6", "value": "node6"},
                ],
            },
        ],
    },
]
```

`pyecharts` node data structure:

```
nodes = [
    {
        "name": "node1",
        "children": [
            {"name": "node2"},
            {
                "name": "node3",
                "children": [
                    {
                        "name": "node4",
                        "children": [
                            {"name": "node5"},
                            {"name": "node5"},
                            {"name": "node5"},
                        ], 
                    }, 
                    {"name": "node6"},
                ],
            },
        ],
    }
]
```