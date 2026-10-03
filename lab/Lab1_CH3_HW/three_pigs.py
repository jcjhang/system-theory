"""
讓開源模型 (Qwen3.6-27B via Ollama) 講「三隻小豬」的故事。

流程結合 Ch.4 的 Agent 範式：
  1. Brainstorm (Plan-and-Solve 的規劃)：發想 3 個不同的創意方向，自評後選出最好的一個
  2. Outline   (Plan-and-Solve 的規劃)：把選定的方向展開成分場大綱
  3. Draft     (Solve)：依大綱寫出初稿
  4. Reflect   (Reflection)：以「嚴格的文學獎評審」身分，依評分標準提出具體修改意見
  5. Refine    (Reflection)：根據意見改寫出定稿
  最後由程式檢查字數 (上限 3000 字)，超過就請模型精簡。

使用方式：
  OLLAMA_HOST=http://127.0.0.1:11500 python three_pigs.py
"""

import json
import os
import re
import time
import urllib.request

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
MODEL = os.environ.get("MODEL", "qwen3.6:27b")
MAX_CHARS = 3000      # 作業上限
TARGET_CHARS = (1800, 2600)

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """你是一位得過多項大獎的華文奇幻／童話作家，擅長把家喻戶曉的經典故事改寫成讓大人小孩都屏息以待、讀完還會回味的新版本。
你的文字特色：畫面感強烈、對白生動有個性、節奏張弛有度、懂得埋伏筆並在結尾漂亮回收、幽默中帶有深意。
一律使用繁體中文（台灣用語）寫作。"""

# 故事主軸的硬性規定，每個步驟都會附上
HARD_RULES = """【不可違反的故事主軸】
1. 主角是三隻小豬：豬大哥、豬二哥、豬小弟，各自蓋了一棟房子。
2. 有一個反派（可以是大野狼，也可以是你重新詮釋的大野狼）來攻擊他們的房子。
3. 豬大哥的房子必須被徹底摧毀。
4. 豬二哥的房子必須被徹底摧毀。
5. 豬小弟的房子必須成功撐住、存活下來，而且這是故事的高潮。
6. 三棟房子由弱到強的順序與「小弟的房子最後存活」不可改變；但房子的材料、反派的攻擊手段、故事的世界觀都可以大膽創新。"""

CRITERIA = """【評分標準（由頂尖的文學評審綜合排名）】
- 精彩程度：開場是否立刻抓住讀者？衝突與危機是否層層升高？每一次攻擊是否都不一樣、一次比一次驚險？高潮是否讓人屏息？結局是否令人滿足？
- 創意度：世界觀、房子的材料、反派的手段、角色的個性與動機，是否讓人眼睛一亮、不落俗套？有沒有出人意料卻合情合理的轉折？
- 文字功力：畫面感、五感描寫、角色專屬的說話方式、幽默感、節奏、伏筆與回收。
- 深度：讀完後是否留下一點超越「要努力蓋堅固房子」的餘韻？"""

BRAINSTORM_PROMPT = f"""{HARD_RULES}

{CRITERIA}

請為「三隻小豬」的全新改寫版本發想 3 個風格截然不同的創意方向（例如換掉世界觀、換掉房子的意義、讓反派有意想不到的動機……但都必須遵守主軸）。
每個方向請寫出：
- 標題
- 世界觀與一句話概念
- 三棟房子分別是什麼、為何會/不會被摧毀（要合乎該世界的邏輯）
- 反派是誰、手段與動機
- 最大的驚喜或轉折
- 依評分標準給自己打分（精彩 1-10、創意 1-10）

避免老套的做法（例如只是把稻草/木頭/磚頭換成另外三種普通建材，或結尾只是說教）。
最後一行請用這個格式寫出你選擇的方向：
選擇：<標題>"""

OUTLINE_PROMPT = f"""{HARD_RULES}

以下是你剛才的創意發想：
<brainstorm>
{{brainstorm}}
</brainstorm>

請針對你最後「選擇」的那個方向，寫出詳細的分場大綱（6～8 場）。
每一場寫出：發生什麼事、情緒張力的高低、要埋下或回收的伏筆、一句讓人印象深刻的台詞。
務必標明：哪一場豬大哥的房子被摧毀、哪一場豬二哥的房子被摧毀、哪一場豬小弟的房子撐住了。
每一次攻擊的手段都要不同，而且一次比一次驚險。"""

DRAFT_PROMPT = f"""{HARD_RULES}

{CRITERIA}

請依照以下大綱，寫出完整的故事：
<outline>
{{outline}}
</outline>

寫作要求：
- 第一行是故事標題，接著空一行開始正文。
- 字數約 {TARGET_CHARS[0]}～{TARGET_CHARS[1]} 字（絕對不可超過 {MAX_CHARS} 字）。
- 第一段就要把讀者抓進故事裡，不要用「從前從前」這種平淡開場。
- 多用場景與對白「演」出來，少用敘述「說」出來；三隻小豬要有各自鮮明的個性與說話方式。
- 只輸出故事本身，不要任何解說、大綱、字數統計或後記。"""

REFLECT_PROMPT = f"""你現在是一位以嚴厲著稱的兒童文學獎決審評審，你只在乎作品能不能從上百篇改寫版本中脫穎而出。

{HARD_RULES}

{CRITERIA}

以下是參賽稿：
<story>
{{story}}
</story>

請完成以下評審：
1. 主軸檢查：逐條檢查【不可違反的故事主軸】，指出是否有違反或交代不清之處（例如房子「被摧毀」寫得不夠明確）。
2. 依評分標準分別打分（1-10），並指出最弱的三個地方。
3. 提出 5～8 條「具體、可執行」的修改建議（指出是哪一段、要怎麼改，例如哪句台詞可以更有個性、哪裡節奏太快、哪個伏筆沒有回收、哪裡太說教）。
4. 檢查是否有不通順的句子、簡體字或中國大陸用語。
只輸出評審意見，不要改寫故事。"""

REFINE_PROMPT = f"""{HARD_RULES}

{CRITERIA}

以下是你的初稿：
<story>
{{story}}
</story>

以下是決審評審給你的意見：
<feedback>
{{feedback}}
</feedback>

請根據評審意見，改寫出最終定稿，讓它在「精彩程度」與「創意度」上都達到最高水準。
- 保留初稿中好的部分，針對評審指出的問題逐一修正。
- 第一行是故事標題，接著空一行開始正文。
- 字數約 {TARGET_CHARS[0]}～{TARGET_CHARS[1]} 字（絕對不可超過 {MAX_CHARS} 字）。
- 只輸出故事本身，不要任何解說、修改說明或字數統計。"""

SHORTEN_PROMPT = f"""{HARD_RULES}

以下故事超過了 {MAX_CHARS} 字的上限（目前約 {{n}} 字）。
請在保留所有精彩情節、轉折與主軸的前提下，把它精簡到 {TARGET_CHARS[1]} 字以內。
只輸出精簡後的故事本身（第一行為標題）。

<story>
{{story}}
</story>"""


# ---------------------------------------------------------------------------
# Ollama helpers
# ---------------------------------------------------------------------------

def chat(prompt, temperature=0.8, system=SYSTEM_PROMPT):
    """呼叫 Ollama /api/chat，回傳模型輸出文字。"""
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "think": False,
        "options": {
            "temperature": temperature,
            "top_p": 0.95,
            "repeat_penalty": 1.05,
            "num_ctx": 16384,
            "num_predict": 6000,
        },
    }
    req = urllib.request.Request(
        f"{OLLAMA_HOST}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=1800) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    text = data["message"]["content"].strip()
    print(f"   ({time.time() - t0:.0f}s, {data.get('eval_count', '?')} tokens)")
    return text


def count_chars(text):
    """計算字數：不含空白與換行。"""
    return len(re.sub(r"\s", "", text))


def clean_story(text):
    """去掉模型偶爾加上的 markdown 標記或結尾說明。"""
    text = re.sub(r"^```.*?\n|```$", "", text.strip(), flags=re.S)
    text = re.sub(r"^#+\s*", "", text, flags=re.M)
    text = text.replace("**", "")
    text = re.split(r"\n\s*(?:（?字數|【?後記|---)", text)[0]
    return text.strip()


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    log = {}

    print("1/5 Brainstorm ...")
    log["brainstorm"] = chat(BRAINSTORM_PROMPT, temperature=1.0)

    print("2/5 Outline ...")
    log["outline"] = chat(OUTLINE_PROMPT.format(brainstorm=log["brainstorm"]), temperature=0.8)

    print("3/5 Draft ...")
    log["draft"] = clean_story(chat(DRAFT_PROMPT.format(outline=log["outline"]), temperature=0.85))
    print(f"   draft: {count_chars(log['draft'])} 字")

    print("4/5 Reflect ...")
    log["feedback"] = chat(REFLECT_PROMPT.format(story=log["draft"]), temperature=0.3)

    print("5/5 Refine ...")
    story = clean_story(chat(REFINE_PROMPT.format(story=log["draft"], feedback=log["feedback"]), temperature=0.75))

    for _ in range(3):
        n = count_chars(story)
        print(f"   final: {n} 字")
        if n <= MAX_CHARS:
            break
        print("   超過上限，精簡中 ...")
        story = clean_story(chat(SHORTEN_PROMPT.format(n=n, story=story), temperature=0.5))

    log["final"] = story
    with open(os.path.join(out_dir, "process_log.json"), "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    with open(os.path.join(out_dir, "story.txt"), "w", encoding="utf-8") as f:
        f.write(story + "\n")

    print("\n" + "=" * 60)
    print(story)
    print("=" * 60)
    print(f"字數：{count_chars(story)}")


if __name__ == "__main__":
    main()
