## 字子 ZiZi - 学子话字 xzhz

### AI App - ZiZi 
multimodal/multilingual Chinese dictionary powered by AI，built on [Streamlit](https://streamlit.io/) web framework ([Source](https://github.com/wgong/zinets)) : 

### YouTube Channel - 学子话字 xzhz

short videos on Zi's story

### TikTok Channel
syndicated with YouTube

## How to use

```
streamlit run ZiZi.py
```

## Resources and Tools

- [wikiwand-zh-cn](https://www.wikiwand.com/zh-cn/%E7%99%B6%E9%83%A8)

- [《说文解字》与汉字构型 汉字部首释例 王宁主讲 ](https://www.youtube.com/watch?v=aRgrP1gtrFg)

- [chinese-characters](https://www.chinese-characters.org/)

- [shuowen.org](https://github.com/shuowenjiezi/shuowen)
     - json data
     - [store json data in sqlite](https://www.beekeeperstudio.io/blog/sqlite-json)
     - https://www.jvt.me/posts/2023/03/13/sqlite-json/
     - [uniDict](https://github.com/wgong/shuowen)

- [MDBG dictionary](https://www.mdbg.net/chinese/dictionary?page=cc-cedict)
     - [python parser](https://github.com/rubber-duck-dragon/rubber-duck-dragon.github.io/blob/master/cc-cedict_parser/parser.py)

- [书同文学校](https://hanzi.unihan.com.cn) 

- [结巴中文分词](https://github.com/wgong/jieba/tree/master)
     - see ~/.../zistory/jieba/notebook/demo-1.ipynb

- [A handy list of all 214 Chinese radicals, and what they mean](https://www.berlitz.com/blog/chinese-radicals-list)
     - [Mandarin Tutor](https://www.mandarintutor.com/resources/commonradicals)

- [嬉戏实验室](https://blog.xiiigame.com/)
     - [通用规范汉字表 中构字最多的100个部件](https://blog.xiiigame.com/2022-10-10-%E3%80%8A%E9%80%9A%E7%94%A8%E8%A7%84%E8%8C%83%E6%B1%89%E5%AD%97%E8%A1%A8%E3%80%8B%E4%B8%AD%E6%9E%84%E5%AD%97%E6%9C%80%E5%A4%9A%E7%9A%84100%E4%B8%AA%E9%83%A8%E4%BB%B6/)
- [East Asian character emojis](https://chenhuijing.com/blog/east-asian-character-emojis/)
     - [Unicode Emoji List](https://unicode.org/emoji/charts/full-emoji-list.html) (see zistory/zinets/resources/unicode-emoji/v15.1)

- [Genesis in Chinese Pictographs](https://www.icr.org/article/genesis-chinese-pictographs/)

- [漢語拆字字典](https://github.com/kfcd/chaizi)
     - [author](https://github.com/dohliam)

- [Chinese Characters GitHub Repos](https://github.com/topics/chinese-characters)

- [孔子学院](https://ci.cn/)

- [Google Translate](https://translate.google.com/?sl=en&tl=zh-CN&text=ordinary%0A&op=translate)

### Poems
- [Mao](https://www.wikiwand.com/zh/%E6%AF%9B%E6%B3%BD%E4%B8%9C)
          - https://www.wikiwand.com/en/Poetry_of_Mao_Zedong
          - https://www.marxists.org/reference/archive/mao/selected-works/poems/index.htm
          - https://raw.githubusercontent.com/banned-historical-archives/banned-historical-archives0/main/mao-quanji/38-OCR.pdf

- [青禾未秀](https://youtu.be/8svj3Esp9ww?si=Q5ZB6CUrq0Yz1ZH5)

### Classic Music
- [50 Best Classic Music of all time⚜️: Mozart, Tchaikovsky, Vivaldi, Paganini, Chopin](https://youtu.be/6truGSXOGF4?si=E7NcqQ2NHh2ro2_z)
## ToDo

### UI
- write recursive query to display Zi tree (字谱)
test cases: 嶷  𩱷
- POC: zizi\devs\notebook\st_tree_select.py

#### visualization of decomposition
```

藻
     > 艹
     > 澡
          > 氵
          > 喿
               > 品
                    > 口 
                    > 口 
                    > 口 
               > 木

               
濒 = 氵止 少 页 (leaf-nodes), 3 levels
     >  氵 
     > 频
          > 步 
               > 止 
               > 少
          > 页

朝 = 十 日 十 月 

噩

```

畐 - someone who has 1 plot of land is considered blessed and rich



- mark t_zi_part.u_id = '-1' for deletion

### Items
- import docs/zi_part_freq.csv into t_part table with frequency and category info

### tree widget
#### UI control
- pip install streamlit-tree-select

#### chart

- https://github.com/erdogant/d3graph/tree/master
     - d3blocks

- pip install pyecharts

- dtreevis - visualize decisiontree in streamlit 
     - https://discuss.streamlit.io/t/dtreeviz-on-streamlit/9970/5

- menu-tree on sidebar
     - https://github.com/streamlit/streamlit/issues/5889
- streamlit widgets including tree
     - https://nicedouble-streamlitantdcomponentsdemo-app-middmy.streamlit.app/
     - https://github.com/nicedouble/StreamlitAntdComponents/tree/master