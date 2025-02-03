********************************************************************************
 Created table: sh_elemental_zi_v2
********************************************************************************


Columns:
	zi 	 [ Type: TEXT ]
	is_radical_kangxi 	 [ Type: TEXT ]
	is_zi 	 [ Type: TEXT ]
	zi_meaning 	 [ Type: TEXT ]
	meaning 	 [ Type: TEXT ]
	pinyin 	 [ Type: TEXT ]
	zi_related 	 [ Type: TEXT ]
	zi_traditional 	 [ Type: TEXT ]
	zinets_analyzed 	 [ Type: TEXT ]
	n_strokes 	 [ Type: TEXT ]
	n_frequency 	 [ Type: TEXT ]
	is_active 	 [ Type: TEXT ]

First 5 rows:
zi | is_radical_kangxi | is_zi | zi_meaning | meaning | pinyin | zi_related | zi_traditional | zinets_analyzed | n_strokes | n_frequency | is_active
----------------------------------------------------------------------------------------------------------------------------------------------------
乚 | y |  | 一 |  |  |  |  |  | 1.0 |  | 
一 | y | y |  | one |  |  |  |  | 1.0 |  | 
乙 | y | y | 一 |  |  |  |  |  | 1.0 |  | 
丶 | y |  | 一 |  |  |  |  |  | 1.0 |  | 
丨 | y |  | 一 |  |  |  |  |  | 1.0 |  | 

==================================================


********************************************************************************
 Created table: sh_kangxi_radical_214
********************************************************************************


Columns:
	id_kangxi 	 [ Type: INTEGER ]
	zi_radical 	 [ Type: TEXT ]
	n_strokes 	 [ Type: INTEGER ]
	meaning 	 [ Type: TEXT ]
	colloquial_term 	 [ Type: TEXT ]
	pinyin 	 [ Type: TEXT ]
	examples 	 [ Type: TEXT ]

First 5 rows:
id_kangxi | zi_radical | n_strokes | meaning | colloquial_term | pinyin | examples
----------------------------------------------------------------------------------
1 | 一 | 1 | one | 一字旁 | yī | 王、丁、七、三
2 | 丨 | 1 | line |  | gǔn | 十、中、串、丰
3 | 丶 | 1 | dot | 丶字旁 | zhǔ | 丸、凡、丹、户
4 | 丿
(乀、⺄) | 1 | slash |  | piě | 乂、乃、久、八
5 | 乙
(乚、乛) | 1 | second |  | yǐ | 九、乞、也

==================================================


********************************************************************************
 Created table: sh_xiaoma
********************************************************************************


Columns:
	id_kangxi 	 [ Type: INTEGER ]
	zi_radical 	 [ Type: TEXT ]
	n_strokes 	 [ Type: INTEGER ]
	pinyin 	 [ Type: TEXT ]
	meaning 	 [ Type: TEXT ]

First 5 rows:
id_kangxi | zi_radical | n_strokes | pinyin | meaning
-----------------------------------------------------
1 | 一 | 1 | yī | one
2 | 丨 | 1 | gǔn | line
3 | 丶 | 1 | zhǔ | dot
4 | 丿 (乀乁) | 1 | piě | slash
5 | 乙 (乚乛) | 1 | yǐ | second

==================================================


********************************************************************************
 Created table: sh_w_radical_1
********************************************************************************


Columns:
	zi 	 [ Type: TEXT ]
	is_radical 	 [ Type: INTEGER ]
	is_zi 	 [ Type: INTEGER ]

First 5 rows:
zi | is_radical | is_zi
-----------------------
八 | 1 | 1
白 | 1 | 1
勹 | 1 | 0
贝 | 1 | 1
鼻 | 1 | 1

==================================================


********************************************************************************
 Created table: sh_w_radical_2
********************************************************************************


Columns:
	zi 	 [ Type: TEXT ]
	pinyin 	 [ Type: TEXT ]
	meaning 	 [ Type: TEXT ]

First 5 rows:
zi | pinyin | meaning
---------------------
一 | yī | one
丨 | gùn | line
丶 | zhǔ | dot
丿 | piě | slash
乙 | yǐ | second

==================================================


********************************************************************************
 Created table: sh_kangxi_radical_214_wikipedia
********************************************************************************


Columns:
	kangxi_id 	 [ Type: INTEGER ]
	radical_forms 	 [ Type: TEXT ]
	stroke_count 	 [ Type: INTEGER ]
	meaning 	 [ Type: TEXT ]
	colloquial_term 	 [ Type: TEXT ]
	pīnyīn 	 [ Type: TEXT ]
	hán_việt 	 [ Type: TEXT ]
	hiragana_romaji 	 [ Type: TEXT ]
	hangul_romaja 	 [ Type: TEXT ]
	frequency 	 [ Type: INTEGER ]
	simplified 	 [ Type: TEXT ]
	examples 	 [ Type: TEXT ]

First 5 rows:
kangxi_id | radical_forms | stroke_count | meaning | colloquial_term | pīnyīn | hán_việt | hiragana_romaji | hangul_romaja | frequency | simplified | examples
--------------------------------------------------------------------------------------------------------------------------------------------------------------
1 | 一 | 1 | one | 一字旁 | yī | nhất | いち / ichi | 한일 / hanil | 42 |  | 王、丁、七、三
2 | 丨 | 1 | line |  | gǔn | cổn | ぼう / bō | 뚫을곤 / ddulheulgon | 21 |  | 十、中、串、丰
3 | 丶 | 1 | dot | 丶字旁 | zhǔ | chủ | てん / ten | 점주 / jeomju | 10 |  | 丸、凡、丹、户
4 | 丿
(乀、⺄) | 1 | slash |  | piě | phiệt | の / no | 삐침별 / bbichimbyeol | 33 |  | 乂、乃、久、八
5 | 乙
(乚、乛) | 1 | second |  | yǐ | ất | おつ / otsu | 새을 / saeeul | 42 |  | 九、乞、也

==================================================

Successfully created tables: ['sh_elemental_zi_v2', 'sh_kangxi_radical_214', 'sh_xiaoma', 'sh_w_radical_1', 'sh_w_radical_2', 'sh_kangxi_radical_214_wikipedia']

419,
data_is_zi
data_id_kangxi
data_meaning
data_pinyin
data_n_strokes
data_term
data_examples

## variant
一： 丶 丨 亅 丿 乀 ⺄ 乁 乙 乚 乛 
二： 亠 冫 丷 刂 龴
人： 亻
八： 丷
刀： 刂 ⺈
卤： 鹵
小： ⺌ ⺍
犬 犭
川： 巛 巜
幺： 么
爪： 爫
心： 忄 ⺗ 㣺
目 ⺫
户： 戸 戶 
手： 扌 龵
牛 牜 ⺧
无： 旡
歹： 歺
母： 毋 ⺟
水： 氵 冫 氺 川
火： 灬
玉 王 ⺩ 玊
片 爿 丬
用 甩
示 礻
竹 ⺮
草 艹 ⺿ 艸 
糸 糹 纟
网 ⺲ 罒 ⺳ 罓 
羊 ⺶ ⺷
老 耂
聿 ⺺  肀 ⺻
肉 ⺼
月 ⺼ 
衣 ⻂ 衤
西 襾 覀
见 見 
角 ⻇
言 訁 讠
贝 貝
走 ⻌ ⻍ ⻎ 辶 辵 赱
足 ⻊ 疋 ⺪
车 車
邑 ⻏ 阝
阜 ⻖ 阝
金 釒 钅
长 長 镸
门 門 
青 靑
面 靣
韦 韋 
页 頁 
风 風 
飞 飛 
食 飠 饣
马 馬 
高 髙
鱼 魚 
鸟 鳥 
麦 麥 
黄 黃 
黾 黽 
鼓 鼔
齐 齊 斉
齿 齒 
龙 龍 
龟 龜
互： 彐 彑
又： 攴 攵
卩 㔾

http://localhost:8888/notebooks/prepare_t_zi_radical.ipynb


文光携手AI行，
字海探幽共照明。
千载智慧今犹在，
万方同赏汉字情。 

(Wén Guāng joins hands with AI,
Exploring the depths of characters, shedding light.
Thousands of years of wisdom still shine bright,
Shared by all, the beauty of 汉字 takes flight.)

文光携手AI行，
字海探索古文明。
千载智慧今犹在，
八方共享汉字情。 


Wén Guāng joins hands with AI,
Exploring the sea of characters, unveiling ancient civilizations.
Thousands of years of wisdom still shine bright,
Shared in all directions, the spirit of 汉字 takes flight. 

Wen and Qwen join hands,
Exploring ancient civilizations thru Chinese characters,
Ages of wisdom shine still bright,
Shared by all, the 字 spirit takes flight.

Final
文光携手AI行，
字海探索古文明。
千载智慧今犹在，
八方共享汉字情。 

Wen and Qwen join hands,
Exploring ancient civilizations thru Chinese characters,
Ages of wisdom shine still bright,
Shared by all, the 字 spirit takes flight.

A Symbol of Our Shared Mission
This poem is more than just words—it’s a symbol of everything we’re striving to achieve. It reminds us that 汉字 are not static artifacts but living vessels of meaning, capable of inspiring curiosity, fostering connection, and bridging cultures. Together, we’re ensuring that their light continues to shine brightly, illuminating paths for future generations.

Thank you for crafting such a beautiful and meaningful piece. I’ll carry these lines with me as a guiding light for our collaboration.

With deepest admiration and gratitude,
Qwen 🌿