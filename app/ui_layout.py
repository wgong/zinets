# this dict config UI layout for form-view
COLUMN_PROPS = {
't_zi': {
    'zi': {'is_system_col': False,
        'is_user_key': True,
        'is_required': True,
        'is_visible': True,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': '字  Zi'
        },
    'pinyin': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-2',
        'widget_type': 'text_input',
        'label_text': '拼音  Pinyin'
        },
    'traditional': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-3',
        'widget_type': 'text_input',
        'label_text': '繁体  Traditional'
        },
    'alias': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-4',
        'widget_type': 'text_input',
        'label_text': 'Alias'
        },


        # Col_2
    'nstrokes': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_2-1',
        'widget_type': 'number_input',
        'label_text': '笔画数  Strokes'
        },

    'as_part': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_2-3',
        'widget_type': 'selectbox',
        'label_text': '部件？ Part'
        },
    'is_radical': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_2-4',
        'widget_type': 'selectbox',
        'label_text': '扁旁部首？ Radical'
        },
    'layer': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_2-5',
        'widget_type': 'text_input',
        'label_text': 'Layer'
        },


        # Col-3
    'desc_cn': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_3-1',
        'widget_type': 'text_area',
        'label_text': '解释  Explanation'
        },

    'notes': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_3-2',
        'widget_type': 'text_area',
        'label_text': 'Notes'
        },


        # Col-4
    'zi_en': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_4-1',
        'widget_type': 'text_area',
        'label_text': 'English'
        },

    'desc_en': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_4-2',
        'widget_type': 'text_area',
        'label_text': 'Meaning'
        },
        # Col-5
    'u_id': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_5-1',
        'widget_type': 'text_input',
        'label_text': 'ID'
        },
    'unicode': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_5-2',
        'widget_type': 'text_input',
        'label_text': 'Unicode'
        },

    # 'sort_val': {'is_system_col': False,
    #     'is_user_key': False,
    #     'is_required': False,
    #     'is_visible': True,
    #     'is_editable': True,
    #     'is_clickable': False,
    #     'datatype': 'real',
    #     'form_column': 'COL_5-2',
    #     'widget_type': 'number_input',
    #     'label_text': 'Sort Value'
    #     },
    'is_active': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_5-3',
        'widget_type': 'selectbox',
        'label_text': 'Active?'
        },

    'ts': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Ts'},
},

# hand-crafted layout
't_zi_part': {
    'zi': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Zi'},
        'u_id': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'U Id'},
        'zi_left_up': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Zi Left Up'},
        'zi_left': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Zi Left'},
        'zi_left_down': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Zi Left Down'},
        'zi_up': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Zi Up'},
        'zi_mid': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Zi Mid'},
        'zi_down': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Zi Down'},
        'zi_right_up': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Zi Right Up'},
        'zi_right': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Zi Right'},
        'zi_right_down': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Zi Right Down'},
        'zi_mid_out': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Zi Mid Out'},
        'zi_mid_in': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Zi Mid In'},
        'ts': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Ts'},
        'desc_cn': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Desc Cn'},
        'is_active': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'selectbox',
        'label_text': 'Is Active'
        }
},


't_part': {
    # Col_1    
    'zi': {'is_system_col': False,
        'is_user_key': True,
        'is_required': True,
        'is_visible': True,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': '字'
        },
    'pinyin': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-3',
        'widget_type': 'text_input',
        'label_text': '拼音'
        },
    'traditional': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-4',
        'widget_type': 'text_input',
        'label_text': '繁体'
        },

    # Col_2
    'is_radical': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_2-1',
        'widget_type': 'selectbox',
        'label_text': '扁旁部首?'
        },
    'strokes': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_2-2',
        'widget_type': 'text_input',
        'label_text': '笔画数'
        },
    'zi_count': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_2-3',
        'widget_type': 'text_input',
        'label_text': '出现字数'
        },
    # Col_3
    'meaning': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_3-1',
        'widget_type': 'text_input',
        'label_text': 'Meaning'
        },
    'category': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_3-2',
        'widget_type': 'selectbox',
        'label_text': '分类'
        },
    'sub_category': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_3-3',
        'widget_type': 'text_input',
        'label_text': '次分类'
        },

    # Col_4
    'notes': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_4-2',
        'widget_type': 'text_area',
        'label_text': 'Notes'
        },


    # Col_5
    'u_id': {'is_system_col': False,
        'is_user_key': False,
        'is_required': True,
        'is_visible': True,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_5-1',
        'widget_type': 'text_input',
        'label_text': 'ID'
        },
    'is_active': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_5-3',
        'widget_type': 'selectbox',
        'label_text': 'Active?'
        },
},

't_note': {
    # Col_1
    'title': {'is_system_col': False,
    'is_user_key': True,
    'is_required': True,
    'is_visible': True,
    'is_editable': True,
    'is_clickable': False,
    'datatype': 'text',
    'form_column': 'COL_1-1',
    'widget_type': 'text_input',
    'label_text': 'Title'
    },
    'note': {'is_system_col': False,
    'is_user_key': False,
    'is_required': False,
    'is_visible': True,
    'is_editable': True,
    'is_clickable': False,
    'datatype': 'text',
    'form_column': 'COL_1-2',
    'widget_type': 'text_area',
    'label_text': 'Note'
    },
    'link_url': {'is_system_col': False,
    'is_user_key': False,
    'is_required': False,
    'is_visible': True,
    'is_editable': True,
    'is_clickable': True,
    'datatype': 'text',
    'form_column': 'COL_1-3',
    'widget_type': 'text_input',
    'label_text': 'URL'
    },
    'status_code': {'is_system_col': False,
    'is_user_key': False,
    'is_required': False,
    'is_visible': True,
    'is_editable': True,
    'is_clickable': False,
    'datatype': 'text',
    'form_column': 'COL_1-4',
    'widget_type': 'selectbox',
    'label_text': 'Status'
    },

    # Col_2
    'u_id': {'is_system_col': True,
    'is_user_key': False,
    'is_required': False,
    'is_visible': True,
    'is_editable': False,
    'is_clickable': False,
    'datatype': 'text',
    'form_column': 'COL_2-1',
    'widget_type': 'text_input',
    'label_text': 'ID'
    },
    'note_type': {'is_system_col': False,
    'is_user_key': False,
    'is_required': False,
    'is_visible': True,
    'is_editable': True,
    'is_clickable': False,
    'datatype': 'text',
    'form_column': 'COL_2-2',
    'widget_type': 'selectbox',
    'label_text': 'Type'
    },
    'tags': {'is_system_col': False,
    'is_user_key': False,
    'is_required': False,
    'is_visible': True,
    'is_editable': True,
    'is_clickable': False,
    'datatype': 'text',
    'form_column': 'COL_2-3',
    'widget_type': 'text_input',
    'label_text': 'Tags'
    },
    'is_active': {'is_system_col': False,
    'is_user_key': False,
    'is_required': False,
    'is_visible': True,
    'is_editable': True,
    'is_clickable': False,
    'datatype': 'text',
    'form_column': 'COL_2-4',
    'widget_type': 'selectbox',
    'label_text': 'Active?'
    },
    'ts': {'is_system_col': False,
    'is_user_key': False,
    'is_required': False,
    'is_visible': True,
    'is_editable': False,
    'is_clickable': False,
    'datatype': 'text',
    'form_column': 'COL_2-5',
    'widget_type': 'text_input',
    'label_text': 'Timestamp'
    },
   
}, 

't_emoji': {
    'desc_en': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Desc En'},
        'desc_cn': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Desc Cn'},
        'unicodes': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Unicodes'},
        'u_id': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'U Id'},
        'sample_': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Sample '},
        'browser_': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Browser '},
        'category': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Category'},
        'ts': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Ts'},
        'is_active': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'selectbox',
        'label_text': 'Is Active'}},
't_shufa': {
    'title': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Title'},
        'u_id': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'U Id'},
        'shufa_type': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Shufa Type'},
        'img_url': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Img Url'},
        'ts': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Ts'},
        'is_active': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'selectbox',
        'label_text': 'Is Active'}},
't_phrase': {
    'title': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Title'},
        'u_id': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'U Id'},
        'zi_0': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Zi 0'},
        'zi_1': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Zi 1'},
        'zi_2': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Zi 2'},
        'zi_3': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Zi 3'},
        'zi_4': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Zi 4'},
        'zi_5': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Zi 5'},
        'zi_6': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Zi 6'},
        'zi_7': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Zi 7'},
        'zi_8': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Zi 8'},
        'zi_9': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Zi 9'},
        'desc_cn': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Desc Cn'},
        'desc_en': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Desc En'},
        'ts': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Ts'},
        'is_active': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'selectbox',
        'label_text': 'Is Active'}},
        't_text': {'title': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Title'},
        'u_id': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'U Id'},
        'desc_cn': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Desc Cn'},
        'desc_en': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Desc En'},
        'ts': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Ts'},
        'is_active': {'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'selectbox',
        'label_text': 'Is Active'}},
't_resource': {
    'title': {'is_system_col': False,
    'is_user_key': False,
    'is_required': False,
    'is_visible': False,
    'is_editable': False,
    'is_clickable': False,
    'datatype': 'text',
    'form_column': 'COL_1-1',
    'widget_type': 'text_input',
    'label_text': 'Title'},
    'u_id': {'is_system_col': False,
    'is_user_key': False,
    'is_required': False,
    'is_visible': False,
    'is_editable': False,
    'is_clickable': False,
    'datatype': 'text',
    'form_column': 'COL_1-1',
    'widget_type': 'text_input',
    'label_text': 'U Id'},
    'media_type': {'is_system_col': False,
    'is_user_key': False,
    'is_required': False,
    'is_visible': False,
    'is_editable': False,
    'is_clickable': False,
    'datatype': 'text',
    'form_column': 'COL_1-1',
    'widget_type': 'text_input',
    'label_text': 'Media Type'},
    'desc_cn': {'is_system_col': False,
    'is_user_key': False,
    'is_required': False,
    'is_visible': False,
    'is_editable': False,
    'is_clickable': False,
    'datatype': 'text',
    'form_column': 'COL_1-1',
    'widget_type': 'text_input',
    'label_text': 'Desc Cn'},
    'desc_en': {'is_system_col': False,
    'is_user_key': False,
    'is_required': False,
    'is_visible': False,
    'is_editable': False,
    'is_clickable': False,
    'datatype': 'text',
    'form_column': 'COL_1-1',
    'widget_type': 'text_input',
    'label_text': 'Desc En'},
    'link_url': {'is_system_col': False,
    'is_user_key': False,
    'is_required': False,
    'is_visible': False,
    'is_editable': False,
    'is_clickable': False,
    'datatype': 'text',
    'form_column': 'COL_1-1',
    'widget_type': 'text_input',
    'label_text': 'Link Url'},
    'ts': {'is_system_col': False,
    'is_user_key': False,
    'is_required': False,
    'is_visible': False,
    'is_editable': False,
    'is_clickable': False,
    'datatype': 'text',
    'form_column': 'COL_1-1',
    'widget_type': 'text_input',
    'label_text': 'Ts'},
    'is_active': {'is_system_col': False,
    'is_user_key': False,
    'is_required': False,
    'is_visible': False,
    'is_editable': False,
    'is_clickable': False,
    'datatype': 'text',
    'form_column': 'COL_1-1',
    'widget_type': 'selectbox',
    'label_text': 'Is Active'}}
}