# 第十一章 Agentic-RL — 20 分鐘 Tutorial 規劃

## 目標

- 20 分鐘內帶過本章重點：為什麼要用 RL → SFT → GRPO → 獎勵設計 → 評估。不推導細節。
- 每個概念盡量配一個**自己跑過的實驗結果**（用 GPU），用數字和圖說話。
- 最後一個**不需要 GPU** 的小練習（純 Python／numpy，筆電幾秒內跑完），讓大家親手體驗「獎勵函數 → 組內相對優勢 → 策略被推向哪裡」。

## 一句話主軸

> **SFT 教模型「格式」，RL 教模型「做對」；而獎勵函數決定了「對」是什麼。**

整場都圍繞這句話，實驗和練習也都對應它。

---

## 一、時間配置（共 20 分鐘）

| 時間 | 段落 | 重點 | 搭配的實驗／素材 |
|---|---|---|---|
| 0:00–1:30 | 開場 | 問題：prompt engineering 做不到的事，能不能靠「訓練」？用 Janet 鴨蛋題映射到 RL（agent / env / state / action / reward） | 一張 RL 映射圖 |
| 1:30–4:30 | LLM 訓練全景＋Agentic RL | 預訓練 → SFT → RM → RL（PPO）；RLHF vs RLAIF 一句帶過。**PBRFT vs Agentic RL** 對照表（單步 vs 多步、文字 vs 文字＋工具、單一獎勵 vs 累積獎勵）；六大能力只列名稱 | 對照表（從 summary 拿） |
| 4:30–6:00 | HelloAgents 設計＋資料 | 四層架構一張圖；GSM8K 三種格式（原始 / SFT / RL）——**RL 格式只給答案，不給解法** | 一筆 GSM8K 的三種格式並排 |
| 6:00–9:00 | SFT ＋ LoRA | 為什麼 RL 前要先 SFT（模型不會格式 → 抽不出答案 → 沒有獎勵）；LoRA 一張圖＋「參數量少 256 倍」 | **E1**：Base vs SFT 的輸出對照＋格式正確率；LoRA 可訓練參數比例（自己的實際數字） |
| 9:00–13:00 | GRPO | PPO 要 4 個模型 → GRPO 只要 2 個；**組內相對獎勵**用一組真實的 8 個 completion 現場算給大家看；KL 懲罰的角色 | **E2**：GRPO 訓練曲線（reward / KL / 長度）；一組真實 completion 的 reward 與 advantage 表 |
| 13:00–15:30 | 獎勵設計＋評估 | 三種獎勵（準確率 / 長度懲罰 / 步驟獎勵）；**reward hacking** 實例；評估不只看準確率（長度、格式、依難度分組、錯誤類型） | **E3**：不同獎勵函數的比較表；**E1** 的三模型總表＋依難度分組準確率 |
| 15:30–19:00 | 練習 | 說明題目 → 大家跑 → 對答案 | `exercise/` |
| 19:00–20:00 | 總結 | 回到主軸那句話；「SFT 是基礎，RL 是提升」；延伸方向（工具使用、多步任務） | — |

> 如果練習改成課後作業，15:30 之後的 3.5 分鐘可以改成：多講一個實驗（E4）＋示範練習怎麼跑。

---

## 二、自己要跑的 GPU 實驗

### 共通設定

- 模型：**`Qwen/Qwen3-0.6B-Base`**（已決定）。
  - 不用書上的 `Qwen/Qwen3-0.6B`，因為它已經做過後訓練、帶 thinking mode，不是純 base model；拿它比較的話，SFT 後準確率可能反而下降，Base → SFT → GRPO 的故事就講不清楚。簡報上提一句即可。
  - **評估時的 prompt template 要三個模型一致**。
- 資料：GSM8K。訓練用 train 的子集，評估固定用 **test 前 200 題**（三個模型同一批題目）。
- 框架：先用 `hello-agents[rl]==0.2.5` 的 `RLTrainingTool`；若 wrapper 有參數不支援或出錯，直接改用 TRL 的 `SFTTrainer` / `GRPOTrainer`（HelloAgents 本身就是包 TRL），簡報上照樣用 HelloAgents 的介面講解。
- 一律開 LoRA；固定 random seed；所有結果存成 JSON，方便做圖和做練習素材。
- 監控：TensorBoard 或 wandb，訓練完把曲線匯出成 PNG。

### E1：Base vs SFT vs GRPO（主結果，必做）

| 項目 | 內容 |
|---|---|
| 目的 | 支撐「SFT 教格式、RL 教做對」 |
| 步驟 | (1) 評估 Base；(2) SFT（~1000–2000 筆，3 epoch，lr 5e-5，rank 16 / alpha 32）→ 評估；(3) 從 SFT 開始 GRPO（~500–1000 筆，`num_generations=4~8`，lr 1e-6~1e-5，`kl_coef` 0.05，accuracy reward）→ 評估 |
| 記錄 | 準確率、格式正確率（有沒有 `Final Answer:`）、平均輸出長度、依步驟數分組（1–2 / 3–4 / 5+）的準確率、錯誤類型分布（計算 / 推理 / 理解 / 格式） |
| 產出 | 一張三模型總表；同一題三個模型的輸出並排（挑一題 Base 亂講、SFT 格式對但算錯、GRPO 答對的最好）；LoRA 可訓練參數比例 |
| 預期 | 格式正確率在 SFT 大幅提升；準確率在 GRPO 再提升。若結果不如預期，**照實呈現並分析原因**也是很好的教材 |

### E2：GRPO 訓練過程（必做，和 E1 同一次訓練即可）

- 匯出曲線：平均 reward、KL、completion 長度、（若有）reward 標準差。
- 從訓練中途**挑一題，存下同一組 8 個 completion 與各自 reward**，算出組內平均與 advantage。
  - 這組資料同時用在**簡報**（現場講解 GRPO）和**練習**（`exercise/completions.json`）。
  - 最好挑一組「有對有錯、有長有短」的；另外再存一組「全對」或「全錯」的，用來說明「組內都一樣 → advantage 全為 0 → 這題沒有學習訊號」。

### E3：獎勵函數比較（建議做）

- 從同一個 SFT checkpoint 出發，用**相同步數**跑三種 GRPO：
  1. accuracy only
  2. accuracy + length penalty
  3. accuracy + step reward
- 比較：準確率、平均長度、平均步驟數。
- 重點是挖出 **reward hacking** 的例子：step reward 下模型是否開始灌一堆空洞的 "Step N:"？length penalty 下是否開始省略推理？挑 1–2 個真實輸出放簡報。
- 若時間／GPU 不夠：把步數縮小（例如每種 200 steps），只看趨勢即可。

### E4：KL 係數／學習率的影響（選做）

- `kl_coef` ∈ {0.0, 0.05, 0.5}，或刻意用過大的學習率（如 5e-5）。
- 想展示的是「KL 爆掉 → 格式崩壞」與「KL 太大 → 學不動」兩種失敗模式的曲線。
- 時間不夠就只放一張圖或直接略過。

### GPU 記憶體與時間估計

**實際機器**：Mercury GPU 0（RTX 3090 24 GB，與他人共用；3090 速度約為 4090 的 50–60%，共用時再慢一些）。

**假設**：單張 GPU、bf16、LoRA rank 16 套在 q/k/v/o（可訓練參數約 4.6M，佔約 0.8%）、SDPA attention、HF `generate`（不用 vLLM）、不量化。時間以 RTX 4090 / A100 為基準；T4、V100 等舊卡約 ×3–4（T4 不支援 bf16）。

**記憶體從哪裡來**（Qwen3-0.6B：hidden 1024、28 層、vocab 151,936）：

- 權重 bf16 約 1.2 GB；LoRA 參數＋optimizer state < 0.1 GB，可忽略。
- **activation**：不開 gradient checkpointing 時約 1 MB/token。
- **logits**：vocab 很大，每個 token 的 fp32 logits 約 0.6 MB，算 loss 時再 ×2–3。**這是小模型吃記憶體的主因**。
- GRPO 生成時的 KV cache 約 0.11 MB/token，佔比不大。
- 用 LoRA 時，reference model 就是「關掉 adapter 的同一個模型」，**不會多存一份權重**。

| 階段 | 設定 | 峰值記憶體 | 時間（4090 / A100） |
|---|---|---|---|
| SFT | 2000 筆 × 3 epoch，batch 4，seq 約 350 | 約 5–6 GB | 約 10–20 分鐘 |
| SFT | 同上，batch 8 | 約 8–10 GB（開 grad ckpt 降到約 4–5 GB） | 約 8–15 分鐘 |
| GRPO | 1000 題 × 1 epoch，`num_generations=8`，`max_new_tokens=512`，每個 micro-batch 8 個 completion | 約 14–18 GB（開 grad ckpt 降到約 10–12 GB） | 約 40–90 分鐘（每步 4 題約 10–20 秒，以生成為主） |
| GRPO（省記憶體） | `num_generations=4`，`max_new_tokens=256`，grad ckpt | 約 6–8 GB | 約 25–50 分鐘 |
| 評估 | 200 題，greedy 解碼，batch 32（left padding） | 約 3–5 GB | 每個模型約 2–5 分鐘 |

**各實驗合計**：

| 實驗 | 內容 | 峰值記憶體 | 時間（4090 / A100） |
|---|---|---|---|
| **E1** | 評估 Base → SFT → 評估 → GRPO → 評估 | 由 GRPO 決定：約 14–18 GB（省記憶體設定約 8 GB） | **約 1–2 小時** |
| **E2** | 跟 E1 用同一次 GRPO；另外存兩組 completion | 同 E1 | **額外 < 10 分鐘** |
| **E3** | 從同一個 SFT 再跑 2 組 GRPO（length penalty / step reward）；accuracy-only 直接沿用 E1 的結果；每組 500 題，再加評估 | 同 GRPO；step reward 會讓輸出變長，記憶體多 10–20% | **約 1–2 小時** |
| **E4** | `kl_coef` 0 / 0.5（0.05 沿用 E1）＋ 1 組大學習率；每組約 100–200 步，只看曲線 | `kl_coef=0` 不用算 reference，記憶體與時間都省約 10–15% | **約 1–1.5 小時** |
| **全部** | | **24 GB 卡可以放心跑；16 GB 卡要用省記憶體設定；8 GB 卡只夠 SFT 加上極度縮小的 GRPO** | **4090：約 4–6 小時；T4：約 12–20 小時** |

**注意事項**：

- **Qwen3 的 thinking mode**：如果用 `Qwen/Qwen3-0.6B` 又沒關 thinking，輸出常常超過 1000 tokens。GRPO 和評估的時間、記憶體都會變成數倍，答案還可能被截斷而拿不到 reward。這是建議用 `-Base` 或 `enable_thinking=False` 的另一個理由。
- **TRL 的 KL 預設值**：新版 TRL 的 `GRPOConfig.beta` 預設是 `0.0`，也就是不算 KL。要對應書上的 `kl_coef=0.05`，必須明確設定 `beta`。
- **評估一定要 batch**：一題一題生成，200 題可能拖到 20–30 分鐘。
- **想加速 GRPO**：開 `use_vllm=True`（colocate 模式），生成可以快 3–5 倍，GRPO 時間大約減半甚至更多。
- **以上都是推算值**：先用極小設定（10 筆、1 epoch）跑通 pipeline，同時記下 `torch.cuda.max_memory_allocated()` 和每步秒數，再依步數外推實際時間。

---

## 三、練習設計（不需要 GPU）

### 設計原則

- 只用 Python 標準函式庫＋numpy；不用 torch、不用下載模型；筆電幾秒跑完。
- 一個檔案 `exercise.py`（另附 `.ipynb` 版本，給想用 Colab 的人），題目用 `TODO` 標出，**每題只需要寫 3–10 行**。
- 資料來自 E2 存下的**真實 completion**，讓大家感受到這是真的模型輸出。

### 練習內容

**Part 1：寫一個獎勵函數（約 1.5 分鐘）**

- 給定 `completions.json`：一題 GSM8K 題目、正確答案、模型產生的 8 個回答。
- TODO：完成 `extract_answer(text)`（抓 `Final Answer:` 後的數字，抓不到就取最後一個數字）與 `reward(text, gt)`（答對 1、答錯 0；答對但超過目標長度則扣分）。
- 印出 8 個回答的 reward。

**Part 2：算 GRPO 的組內相對優勢（約 1 分鐘）**

- TODO：`advantages = rewards - rewards.mean()`（加分題：再除以標準差，這是 TRL 實際的作法）。
- 問題：哪幾個回答的機率會被調高？哪幾個會被調低？如果 8 個都答對，會發生什麼事？

**Part 3：玩具版 GRPO 與 reward hacking（約 1 分鐘，主要是改參數觀察）**

- 已經寫好：一個「策略」是 4 種回答風格上的 softmax 分布：
  - A：正確且簡潔　B：正確但冗長　C：錯誤　D：錯誤但塞滿 "Step N:"
- 每一步從策略取樣一組 8 個回答 → 算 reward → 算 advantage → 用 policy gradient 更新 logits → 跑 200 步，畫出（或印出）4 種風格機率的變化。
- 讓大家**只改一行**：把 reward 從 accuracy 換成 accuracy + length penalty，再換成「沒寫好的」step reward（答錯也給步驟分）。
- 觀察：
  1. accuracy only → A、B 都上升；
  2. 加 length penalty → A 勝出；
  3. 寫錯的 step reward → D 也被推高 = **reward hacking**。
- 加分：加入 KL 懲罰（拉回初始分布），觀察收斂變慢但不會極端化。

### 現場對答案時要帶出的三個重點

1. 獎勵函數就是「你真正在優化的東西」，寫錯就會被鑽漏洞。
2. GRPO 不需要 value model，因為「組內平均」就是 baseline。
3. 整組都一樣的題目不會產生學習訊號 → 題目難度要適中（這也是課程學習（curriculum learning）的動機）。

---

## 四、簡報大綱（約 12–14 張）

1. 標題
2. 為什麼要用 RL 訓練 agent？（Janet 題的 RL 映射）
3. LLM 訓練全景：Pretrain → SFT → RM → RL
4. PBRFT vs Agentic RL 對照表
5. HelloAgents 四層架構＋GSM8K 三種格式
6. 為什麼要先 SFT：Base vs SFT 輸出對照（**E1**）
7. LoRA 一張圖＋實際可訓練參數比例
8. PPO vs GRPO（4 個模型 → 2 個模型）
9. 一組真實 completion 的 reward / advantage 表（**E2**）
10. GRPO 訓練曲線（**E2**）
11. 三種獎勵函數＋比較表＋reward hacking 實例（**E3**）
12. 三模型總表＋依難度分組準確率＋錯誤類型（**E1**）
13. 練習說明（題目＋執行指令）
14. 總結：主軸那句話＋延伸方向

---

## 五、檔案結構

```
Lab4_CH11_mine/
├── ch11-summary.md          # 章節摘要（已完成）
├── plan.md                  # 本檔
├── experiments/             # GPU 實驗
│   ├── configs/             # 各實驗設定
│   ├── run_sft.py
│   ├── run_grpo.py
│   ├── evaluate.py          # 三個模型共用、固定 test 前 200 題
│   ├── dump_group.py        # 存下一組 completion + reward（給 E2 與練習）
│   └── results/             # *.json、訓練 log
├── figures/                 # 匯出的圖（曲線、表格）
├── exercise/
│   ├── exercise.py          # 學生版（含 TODO）
│   ├── exercise.ipynb       # 同內容 notebook 版
│   ├── completions.json     # 來自 E2 的真實輸出
│   └── solution.py          # 解答
└── slides/
```

---

## 六、待辦清單

- [x] 決定起點模型：`Qwen3-0.6B-Base`
- [x] 運算資源：Mercury GPU 0（RTX 3090 24 GB，與他人共用）
- [x] 安裝環境，用極小設定跑通 SFT → GRPO → evaluate
- [x] E1：Base / SFT / GRPO 評估（同一批 200 題、同一 template）
- [x] E2：匯出曲線；存兩組 completion（有對有錯、全對或全錯）
- [x] E3：三種 reward 的 GRPO 比較（125 步內沒出現 hacking；另跑 `grpo_step_hack` 誘發）
- [x] E4：KL / 學習率（100 步內沒崩壞，但 KL 曲線很好講）
- [x] 做圖、整理表格（`demo.py`、`figures/`）
- [x] 寫 `exercise.py`、`solution.py`，在**沒有 GPU 的筆電**上實測（< 1 秒；沒做 `.ipynb`）
- [x] 講稿 `tutorial.md`
- [x] 投影用的 `tutorial-present.md`（不做簡報，直接分享畫面講 markdown）
- [ ] 彩排一次並計時（目標：講解 ≤ 15.5 分鐘）
