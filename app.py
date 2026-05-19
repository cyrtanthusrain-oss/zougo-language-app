# app.py
# =========================================
# NieR風 造語歌詞変換ツール - 完成形
# Streamlit Version
# =========================================

import streamlit as st
from janome.tokenizer import Tokenizer
import random
import re

# =========================================
# ページ設定
# =========================================

st.set_page_config(
    page_title="NieR風 造語歌詞変換",
    page_icon="🌙",
    layout="wide"
)

# =========================================
# CSS
# =========================================

st.markdown("""
<style>

.main {
    background-color: #0f1117;
    color: white;
}

.stTextArea textarea {
    background-color: #1a1d29;
    color: #f1f1f1;
    border-radius: 12px;
    font-size: 16px;
}

.stButton button {
    width: 100%;
    border-radius: 12px;
    height: 50px;
    font-size: 18px;
    background: linear-gradient(90deg,#4b4f6d,#7b7fa6);
    color: white;
    border: none;
}

.result-box {
    background-color: #161925;
    padding: 20px;
    border-radius: 16px;
    font-size: 18px;
    line-height: 1.8;
    white-space: pre-wrap;
}

.title {
    text-align:center;
    font-size:48px;
    font-weight:bold;
    margin-bottom:0;
}

.subtitle {
    text-align:center;
    color:#9fa6c2;
    margin-top:0;
    margin-bottom:30px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# タイトル
# =========================================

st.markdown(
    "<p class='title'>🌙 NieR風 造語歌詞変換</p>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='subtitle'>儚い架空言語へ歌詞を変換します</p>",
    unsafe_allow_html=True
)

# =========================================
# 辞書
# =========================================

dictionary = {

    # 人称
    "君": "Eila",
    "あなた": "Noeli",
    "私": "Rei",
    "僕": "Aru",
    "自分": "Ego",
    "家族": "Famina",
    "彼女": "Elia",
    "誰か": "Velis",
   
    # 感情
    "愛": "Elia",
    "悲しみ": "Varein",
    "孤独": "Noctis",
    "願い": "Mirel",
    "希望": "Sola",
    "優しさ": "Lethia",
    "絶望": "Velune",
    "温もり": "Noa",

   # 世界・概念
    "ストーリー": "Scripta",
    "物語": "Scripta",
    "奇跡": "Miracla",
    "悲劇": "Tragia",
    "絆": "Vincla",
    "誇り": "Gloria",
    "正解": "Veritas",
    "光": "Sol",
    "闇": "Vel",
    "月": "Luneth",
    "星": "Astria",
    "夜": "Ereth",
    "空": "Ashveil",
    "世界": "Elnor",
    "夢": "Lunaris",

    # 【情景・身体・機械】
    "声": "Vocia",
    "風": "Anemol",
    "胸": "Kardia",
    "心臓": "Kardia",
    "血": "Cruor",
    "壁": "Murus",
    "翼": "Penna",
    "鉄": "Ferro",
    "機械": "Machina",
    "鼓動": "Pulsis",
    "悪夢": "Noctura",

    # 記憶
    "記憶": "Reth",
    "思い出": "Revale",
    "魂": "Elreth",
    "命": "Elnora",
    "存在": "Nores",
    "終焉": "Endveil",

    # 動詞
    "消える": "Noreth",
    "泣く": "Vael",
    "歌う": "Luthiel",
    "生きる": "Elvain",
    "忘れる": "Morteil",
    "眠る": "Lunare",
    "願う": "Mireth",
    "守る": "Rethiel",
    "堕ちる": "Velneth",
    "照らす": "Solen",
    "響く": "Reson",
    "響き始めた": "Resonare",
    "映る": "Visu",
    "否定した": "Negat",
    "預ける": "Credo",
    "塗り替え": "Alba",
    "白く染めた": "Alba",
    "塗り替えた": "Alba",
    "切り裂け": "Secare",
    "信じられる": "Fidere",
    "抱きしめられ": "Amplex",
    "救われた": "Salva",
    "生きていく": "Elvain",

    # 助詞
    "の": " no ",
    "に": " in ",
    "を": " ",
    "は": " ",
    "が": " ",
    "と": " "
}

# =========================================
# サビ用単語
# =========================================

chorus_words = [
    "Eloria",
    "Vaelune",
    "Solmire",
    "Astralune",
    "Endveil",
    "Mirelia",
    "Luneth Elia"
]

# =========================================
# モード
# =========================================

mode = st.sidebar.selectbox(
    "変換モード",
    [
        "Replicant風",
        "Automata風",
        "聖歌風",
        "壊れた機械生命体風"
    ]
)

# =========================================
# 造語率
# =========================================

fake_ratio = st.sidebar.slider(
    "造語率",
    10,
    100,
    70
)

# =========================================
# 雰囲気追加
# =========================================

ellipsis = st.sidebar.checkbox(
    "余韻（...）を追加",
    value=True
)

chorus_mode = st.sidebar.checkbox(
    "サビ演出を追加",
    value=True
)

# =========================================
# モード別処理
# =========================================

def apply_mode(text):

    if mode == "Replicant風":
        return text

    elif mode == "Automata風":
        return text.lower()

    elif mode == "聖歌風":
        return "♪ " + text

    elif mode == "壊れた機械生命体風":
        return re.sub(r"[aeiou]", "-", text.lower())

    return text

# =========================================
# 母音伸ばし
# =========================================

def stretch_vowels(text):

    vowels = "aeiouAEIOU"

    result = ""

    for char in text:

        result += char

        # ランダムで母音を伸ばす
        if char in vowels and random.random() < 0.25:

            result += char * random.randint(1, 3)

    return result


# =========================================
# コーラス化
# =========================================

def chorusify(text):

    effects = [
        "...",
        " Ah...",
        " Ooh...",
        " Laa...",
        " Haa...",
        " Aaaa...",
        " Yeeee..."
    ]

    if random.random() < 0.4:

        text += random.choice(effects)

    return text


# =========================================
# 詩化（改行演出）
# =========================================

def poetic_break(text):

    words = text.split()

    if len(words) > 3 and random.random() < 0.5:

        insert_pos = random.randint(1, len(words) - 1)

        words.insert(insert_pos, "\n")

    return " ".join(words)


# =========================================
# エコー演出
# =========================================

def add_echo(text):

    if random.random() < 0.3:

        words = text.split()

        if len(words) > 0:

            last_word = words[-1]

            if len(last_word) > 4:

                echo = last_word[-3:]

                text += f"\n...{echo}..."

    return text


# =========================================
# 機械生命体ノイズ
# =========================================

def machine_noise(text):

    replacements = {
        "a": "4",
        "e": "3",
        "i": "1",
        "o": "0",
        "u": "_"
    }

    result = ""

    for char in text:

        if char.lower() in replacements and random.random() < 0.15:

            result += replacements[char.lower()]

        else:

            result += char

    return result

# =========================================
# 変換関数（改良版：自動単語分解）
# =========================================

def translate_lyrics(text):
    # Janomeの解析器を準備
    t = Tokenizer()
    
    # 行ごとに処理
    lines = text.split("\n")
    formatted = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 1. 日本語の文章を自動で単語に分解する
        # 例：「胸を叩けば」 -> ["胸", "を", "叩け", "ば"]
        parsed_words = [token.surface for token in t.tokenize(line)]
        
        # 2. 分解した単語ごとに辞書と照らし合わせて置換
        translated_line_words = []
        for word in parsed_words:
            if word in dictionary:
                translated_line_words.append(dictionary[word])
            else:
                # 辞書にない場合はそのまま（「を」などの助詞や辞書未登録の単語）
                translated_line_words.append(word)
        
        # 単語を繋ぎ直して1つの文にする
        current_line = "".join(translated_line_words)

        # 3. 既存の各種モードや演出を適用
        current_line = apply_mode(current_line)     # モード適用
        current_line = stretch_vowels(current_line)  # 母音伸ばし
        current_line = chorusify(current_line)      # コーラス化
        current_line = poetic_break(current_line)   # 詩化

        # 余韻追加
        if ellipsis:
            if random.random() < 0.35:
                current_line += "..."

        formatted.append(current_line)

    # サビ演出
    if chorus_mode:
        formatted.append("")
        formatted.append(random.choice(chorus_words))

    return "\n".join(formatted)

# =========================================
# 入力欄
# =========================================

col1, col2 = st.columns(2)

with col1:

    input_text = st.text_area(
        "歌詞入力",
        height=400,
        placeholder="""例：

君の記憶が消える
月の下で泣いていた

まだ光を探している
"""
    )

with col2:

    st.markdown("### 🌙 変換結果")

    if "output" not in st.session_state:
        st.session_state.output = ""

    st.markdown(
        f"""
        <div class="result-box">
        {st.session_state.output}
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================
# ボタン
# =========================================

col_btn1, col_btn2 = st.columns(2)

with col_btn1:

    if st.button("🌙 造語へ変換"):

        if input_text.strip() == "":
            st.warning("歌詞を入力してください")
        else:

            st.session_state.output = (
                translate_lyrics(input_text)
            )

            st.rerun()

with col_btn2:

    if st.button("🗑 リセット"):

        st.session_state.output = ""
        st.rerun()

# =========================================
# 辞書一覧
# =========================================

with st.expander("📖 使用辞書を見る"):

    st.json(dictionary)

# =========================================
# フッター
# =========================================

st.markdown("---")

st.caption(
    "NieR風 / 架空言語 / 儚い歌詞ジェネレーター"
)