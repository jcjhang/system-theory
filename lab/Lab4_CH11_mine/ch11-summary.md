# 第十一章 Agentic-RL 重點摘要

> 來源：[hello-agents / 第十一章 Agentic-RL](https://github.com/datawhalechina/hello-agents/blob/main/docs/chapter11/%E7%AC%AC%E5%8D%81%E4%B8%80%E7%AB%A0%20Agentic-RL.md)

本章要回答三個問題：**如何讓智能體具備更強的推理能力？如何更好地使用工具？如何自我改進？** 答案是 Agentic RL（以強化學習訓練智能體）。本章為 HelloAgents 框架加入 RL 訓練能力，從 LLM 訓練基礎講起，經 SFT、GRPO，最後建出完整的訓練 pipeline。

---

## 11.1 從 LLM 訓練到 Agentic RL

### 11.1.1 從強化學習到 Agentic RL

- RL 是處理**序貫決策**問題的學習範式：智能體與環境互動，透過「試錯」最大化長期收益。
- 以 GSM8K 數學題（Janet 的鴨蛋：16 − 3 − 4 = 9，9 × 2 = 18）為例，映射到 RL：
  - **智能體**：基於 LLM 的推理系統
  - **環境**：數學題與驗證系統
  - **狀態**：題目描述＋已有推理步驟
  - **行動**：產生下一步推理或最終答案
  - **獎勵**：答對 +1，答錯 0
- **監督學習的三個侷限**：
  1. 資料品質決定上限，只能模仿、難以超越；
  2. 缺乏探索能力，只能被動學人類給的路徑；
  3. 難以優化長期目標（多步推理的中間過程）。
- RL 讓模型自行產生多個候選答案並依正確性得到獎勵，可學到哪些推理路徑較好，甚至找到比人類標註更好的解法。
- **核心思想**：把 LLM 當作可學習的策略（policy），嵌入智能體的「感知－決策－執行」循環，用 RL 優化多步任務表現。

### 11.1.2 LLM 訓練全景圖

LLM 訓練分為**預訓練（Pretraining）**與**後訓練（Post-training）**兩大階段。

**預訓練**：用 TB 級文本做自監督學習，最常見任務是因果語言建模（Next Token Prediction）：

$$
\mathcal{L}_{\text{pretrain}} = -\sum_{t=1}^{T} \log P(x_t \mid x_1, \dots, x_{t-1}; \theta)
$$

模型因此學到語法、語意、世界知識與基本推理能力。特色是資料量大、計算成本高，學到的是通用語言能力。

**後訓練**：預訓練模型只會「預測下一個字」，不懂得遵循指令、產生有幫助／無害／誠實的回答、拒絕不當請求、以對話方式互動。後訓練就是讓模型對齊人類偏好，包含三步：

| 步驟 | 目標 | 損失／目標函數 |
|---|---|---|
| **1. SFT 監督微調** | 學會遵循指令與對話格式；資料為 (prompt, completion) 對 | $\mathcal{L}_{\text{SFT}} = -\sum_i \log P(y_i \mid x_i; \theta)$ |
| **2. RM 獎勵建模** | 用偏好對比資料（chosen $y_w$ vs. rejected $y_l$）學人類偏好 | $\mathcal{L}_{\text{RM}} = -\mathbb{E}[\log \sigma(r_\phi(x, y_w) - r_\phi(x, y_l))]$ |
| **3. RL 微調（如 PPO）** | 最大化獎勵，同時不偏離參考模型太遠 | $J_{\text{PPO}} = \mathbb{E}[r_\phi(x, y)] - \beta \cdot D_{KL}(\pi_\theta \Vert \pi_{\text{ref}})$ |

- **RLHF** 需要大量人工偏好標註，成本高。
- **RLAIF** 改用強 AI 模型（如 GPT-4）取代人類標註：SFT 模型產生候選 → AI 評分排序 → 訓練 RM → RL。效果接近甚至超越 RLHF，成本大幅降低。

### 11.1.3 Agentic RL 的核心理念

- 傳統後訓練稱為 **PBRFT（Preference-Based Reinforcement Fine-Tuning）**：聚焦**單輪**對話品質，給問題 → 產生回答 → 依品質給分。
- **Agentic RL**：把 LLM 視為嵌在**序貫決策循環**中的可學習策略，需在動態環境中多步互動、取得中間回饋、優化**長期累積獎勵**。
- 例：「分析 GitHub repo 程式碼品質」→ 呼叫 API (+0.1) → 讀程式碼 (+0.1) → 分析合理 (+0.2) → 產生高品質報告 (+0.6)，總獎勵 1.0。

**MDP 角度對比**（MDP 五元組 $(S, A, P, R, \gamma)$）：

| 面向 | PBRFT | Agentic RL |
|---|---|---|
| 狀態 | $s_0 = \text{prompt}$，$T=1$，狀態不變 | $s_t = (\text{prompt}, o_1, \dots, o_t)$，$T \gg 1$，隨行動演化 |
| 行動 | 只有文字生成 $a = y \sim \pi_\theta(y \mid s_0)$ | 文字＋工具呼叫＋環境操作 $a_t \in \{a_t^{\text{text}}, a_t^{\text{tool}}\}$ |
| 轉移 | 無轉移，$P(s' \mid s,a) = \delta(s' - s_{\text{terminal}})$ | $s_{t+1} \sim P(s_{t+1} \mid s_t, a_t)$（如搜尋後狀態含搜尋結果） |
| 獎勵 | 單步 $r(s_0, y)$，通常由 RM 給出 | 多步 $\sum_t \gamma^t r(s_t, a_t)$；可為稀疏、密集或混合 |
| 目標 | $J = \mathbb{E}[r(s_0, y)]$ | $J = \mathbb{E}_{\tau \sim \pi_\theta}[\sum_t \gamma^t r(s_t, a_t)]$，$\tau$ 為完整軌跡 |

- 思維轉變：從「讓模型產生更好的**單一回答**」（回答品質、語言表達、單步決策）→「讓智能體**完成複雜任務**」（任務完成度、行動策略、多步規劃）。LLM 從「對話助手」進化為「自主智能體」，會主動找資訊、知道何時如何用工具、願意走看似「繞路」的中間步驟、從錯誤中學習。

**Agentic RL 欲賦予的六大核心能力**：

1. **推理（Reasoning）**：CoT 提示依賴 few-shot、SFT 只能模仿；RL 能試錯學推理策略、發現資料中沒有的路徑、學會何時深思何時速答。建模為：給問題 $q$，產生推理鏈 $c$ 與答案 $a$，$r = \mathbb{1}[a = a^*]$。
2. **工具使用（Tool Use）**：行動空間擴展為 $\{a^{\text{think}}, a^{\text{tool}}=(\text{tool\_name}, \text{arguments})\}$；學會何時用、用哪個、如何組合。
3. **記憶（Memory）**：上下文有限、靜態 RAG 無法針對任務優化；RL 學記憶管理（記什麼、何時更新、何時刪除）。
4. **規劃（Planning）**：CoT 是線性、無法回溯，提示模板是靜態；RL 學動態規劃、權衡短期與長期收益。
5. **自我改進（Self-Improvement）**：辨識錯誤、分析失敗原因、調整策略。
6. **感知（Perception）**：多模態理解，例如視覺推理、使用視覺工具、視覺規劃。

### 11.1.4 HelloAgents 的 Agentic RL 設計

- 技術選型：**TRL**（Hugging Face 的 RL 函式庫）＋ **Qwen3-0.6B**（小模型，一般 GPU 可訓練）。
- **四層架構**（由下到上）：
  1. **資料集層**：`GSM8KDataset`、`create_sft_dataset()`、`create_rl_dataset()`
  2. **獎勵函數層**：`MathRewardFunction` 基類、`AccuracyReward`、`LengthPenaltyReward`、`StepReward`、`create_*_reward()`
  3. **訓練器層**：`SFTTrainerWrapper`、`GRPOTrainerWrapper`（含 LoRA 支援）
  4. **統一介面層**：`RLTrainingTool`，支援 `action` = `train` / `load_dataset` / `create_reward` / `evaluate`

### 11.1.5 快速上手

```bash
pip install "hello-agents[rl]==0.2.5"
```

流程：`RLTrainingTool().run({...})` 依序做 SFT（10 樣本、1 epoch、LoRA）→ GRPO（5 樣本；`batch_size` 須能被 `num_generations` 整除）→ evaluate。只看過 ~0.7% 訓練資料、只跑一輪，所以準確率很低是正常的。

---

## 11.2 資料集與獎勵函數

資料集定義「要學什麼任務」，獎勵函數定義「什麼是好的行為」，兩者是 RL 訓練的兩大基石。

### 11.2.1 GSM8K 數學推理資料集

- 為什麼選數學：有明確正解可**自動評估**（不需人工或 RM）、需要多步推理、能力可遷移。開放式問答則難以客觀評估。
- **GSM8K**：小學數學應用題，訓練 7,473 筆、測試 1,319 筆，需 2–8 步推理。答案中 `<<48/2=24>>` 標記中間計算，`#### 72` 標記最終答案。
- **三種格式**：

| 格式 | 內容 | 用途 |
|---|---|---|
| 原始 | `question` + `answer`（含解題步驟） | 人類閱讀 |
| SFT | `prompt`（套用對話模板，如 Qwen 的 `<|im_start|>`）＋ `completion`（完整解題與答案） | 學輸出格式與分步推理 |
| RL | `prompt`（同 SFT）＋ `ground_truth`（只有最終答案） | 計算獎勵；迫使模型自行產生推理而非記憶答案 |

- 用 `rl_tool.run({"action": "load_dataset", "format": "sft"/"rl", "max_samples": N})` 載入。

### 11.2.2 獎勵函數設計

- 數學任務簡化為 $r(q, a) = f(a, a^*)$。
- **好的獎勵函數**：清楚定義成功、提供梯度訊號、變異數不過大、易調整與組合。
- **壞的獎勵函數**：只在最後給獎勵、存在**獎勵欺騙（reward hacking）**、目標互相矛盾、變異數過大不收斂。

**三種內建獎勵函數**：

1. **準確率獎勵 AccuracyReward**：$r_{\text{acc}} = 1$ 若 $a = a^*$，否則 0。
   - 需處理答案擷取（找 "Final Answer:"、"####"、或 regex 取最後一個數字）與比對（72.0 vs 72、單位、文字數字）。
   - 優點：簡單直接；缺點：**獎勵稀疏**，無法區分「接近正確」與「完全錯誤」，初期缺乏回饋。
2. **長度懲罰 LengthPenaltyReward**：$r = r_{\text{acc}} - \alpha \cdot \max(0, l - l_{\text{target}})$（預設 $\alpha = 0.001$）。
   - **只在答對時才懲罰**，避免模型為了短而答錯。例：目標 200、實際 500 → $1 - 0.001 \times 300 = 0.7$。
   - 優點：簡潔、降低推理成本；缺點：可能抑制詳細推理、係數需細調。
3. **步驟獎勵 StepReward**：$r = r_{\text{acc}} + \beta \cdot s$（$s$ 為偵測到的步驟數，預設 $\beta = 0.1$），同樣只在答對時給。
   - 例：3 個步驟 → $1.3$。
   - 優點：鼓勵可解釋推理；缺點：可能產生冗餘步驟灌分、步驟偵測不一定準。

**組合策略**：
- 準確率＋長度懲罰 → 簡潔正確（對話／問答系統）
- 準確率＋步驟獎勵 → 詳細推理（教育、可解釋 AI）
- 三者平衡：$r = r_{\text{acc}} - \alpha \max(0, l - l_{\text{target}}) + \beta s$，需小心調 $\alpha, \beta$ 避免某一目標主導。

### 11.2.3 自訂資料集與獎勵函數

- **欄位要求**：
  - SFT：`prompt`、`completion`、（可選）`text`
  - RL：`question`、`prompt`、`ground_truth`、`full_answer`
- **自訂資料集三種方式**：
  1. 準備 `question`/`answer` 原始資料，用 `format_math_dataset(dataset, format_type="sft"|"rl", model_name=...)` 轉換；
  2. 訓練時以 `custom_dataset` 參數直接傳入；
  3. **（推薦）** `rl_tool.register_dataset("name", ds)` 註冊後用 `"dataset": "name"` 引用。
- **自訂獎勵函數簽名**：`def reward(completions: List[str], **kwargs) -> List[float]`，`kwargs["ground_truth"]` 為正解列表。範例依誤差給分（<0.01 → 1.0、<1 → 0.8、<5 → 0.5），可加推理步驟加分。
- 使用方式：`custom_reward` 參數直接傳入，或 **（推薦）** `register_reward_function(name, fn)` 註冊——與 dataset 同名時會自動配對使用。

---

## 11.3 SFT 訓練

SFT 是 RL 訓練的第一步與基礎；沒有 SFT，直接做 RL 常會失敗，因為模型連基本輸出格式都不會。

### 11.3.1 為什麼需要 SFT

- 預訓練模型的目標是預測下一個字而非解題；輸出是自由文字而非結構化格式；沒看過任務相關資料。
- **SFT 的作用**：學輸出格式（"Step 1"、"Final Answer"）、學推理模式、建立基線能力、**縮小 RL 的探索空間**。
- 對比實驗：預訓練模型回答冗長、無結構、無明確答案 → 無法擷取答案、無法給獎勵；SFT 後輸出結構清楚、答案明確，才能用於 RL。
- SFT 是從預訓練模型到 RL 的**橋樑**。

### 11.3.2 LoRA：參數高效微調

- 全量微調 Qwen3-0.6B 約需 12GB（FP16）／24GB（FP32）顯存；7B 以上在消費級 GPU 幾乎不可行。
- **核心想法**：微調時的權重變化是低秩的。凍結 $W \in \mathbb{R}^{d \times k}$，只訓練

$$
\Delta W = BA,\quad B \in \mathbb{R}^{d \times r},\ A \in \mathbb{R}^{r \times k},\ r \ll \min(d,k)
$$

$$
h = Wx + BAx
$$

- 參數量從 $dk$ 降到 $r(d+k)$。例：$d = k = 4096, r = 8$ → 16,777,216 vs. 65,536，**減少 256 倍**。
- 優點：顯存大降、訓練較快、易部署、防過擬合；缺點：效果通常略遜全量微調。
- **關鍵超參數**：
  - `rank r`：典型 4–64，預設 8；越大表達力越強、參數越多
  - `alpha`：縮放因子，實際更新為 $\frac{\alpha}{r} BA$；常設為 rank 或 rank 的 2 倍
  - `target_modules`：通常為注意力層 `q_proj, k_proj, v_proj, o_proj`，也可加 MLP 層 `gate_proj, up_proj, down_proj`

### 11.3.3 SFT 訓練實戰

流程：準備資料 → 設定 LoRA → 設定訓練參數 → 訓練 → 存模型。Loss 逐漸下降代表在學習。

**參數建議**：

| 類別 | 參數 | 建議 |
|---|---|---|
| 資料 | `max_samples` | 快速測試 100–1000；完整訓練用全部 7,473 |
| | `split` | 預設 `"train"`，可用 `"train[:1000]"` |
| 訓練 | `num_epochs` | 從 3 開始；1–2 可能欠擬合、>10 可能過擬合 |
| | `batch_size` | 4GB → 1–2；8GB → 4–8；16GB → 8–16 |
| | `learning_rate` | SFT 5e-5；LoRA 可稍大 1e-4 |
| LoRA | `use_lora` | 建議一律開啟 |
| | `lora_rank` | 小任務 4–8、複雜任務 16–32、大規模 64 |
| | `lora_alpha` | 通常為 rank 的 2 倍 |
| 優化器 | `optimizer` | 預設 AdamW |
| | `weight_decay` | 預設 0.01（0.001–0.1） |
| | `warmup_ratio` | 預設 0.1：前 10% 步數線性升溫後線性衰減 |

完整訓練範例（全資料、rank 16、alpha 32、batch 8）約需 8GB 顯存、30–60 分鐘。

**訓練監控**：
- **Loss**：應下降；不降 → LR 太小或資料有問題；降後回升 → LR 太大或過擬合。
- **梯度範數**：合理範圍 0.1–10；>100 為梯度爆炸（降 LR）；<0.01 為梯度消失。
- **學習率**：依 warmup 策略變化。

**常見問題**：
- 顯存不足 → 減小 `batch_size`／`max_length`、梯度累積、換更小模型
- 速度慢 → 增大 batch、降低 logging 頻率、混合精度
- Loss 不降 → 提高 LR、檢查資料格式、增加 epoch
- 過擬合 → 增加 weight decay、減少 epoch、增加資料

### 11.3.4 模型評估

- 指標：**準確率**、**平均獎勵**、**推理品質**（需人工或評估模型）。
- `rl_tool.run({"action": "evaluate", "model_path": ..., "max_samples": ..., "use_lora": ...})`
- Qwen3-0.6B 在 GSM8K 上：SFT 後約 **40–50%**，經 RL 可再提升到 **60–70%**。
- 建議比較預訓練模型 vs. SFT 模型的準確率以理解 SFT 效果。

---

## 11.4 GRPO 訓練

SFT 只是學會「模仿」，沒有真正學會「思考」；RL 透過試錯優化推理策略，可超越訓練資料的品質。

### 11.4.1 從 PPO 到 GRPO

**PPO 在 LLM 訓練上的問題**：
- 需要訓練 **Value Model**，增加複雜度與顯存；
- 需同時維護**四個模型**（Policy、Reference、Value、Reward），工程複雜；
- 訓練不穩，易出現獎勵崩塌或策略退化。

PPO 目標函數（含 clip）：

$$
J_{\text{PPO}} = \mathbb{E}\left[\min\left(\frac{\pi_\theta}{\pi_{\text{old}}} A,\ \text{clip}\left(\frac{\pi_\theta}{\pi_{\text{old}}}, 1-\epsilon, 1+\epsilon\right) A\right)\right],\quad A(s,a) = r + \gamma V(s') - V(s)
$$

**GRPO（Group Relative Policy Optimization，出自 DeepSeekMath）**：

$$
J_{\text{GRPO}} = \mathbb{E}\left[\frac{\pi_\theta(a \mid s)}{\pi_{\text{ref}}(a \mid s)} \cdot (r(s,a) - \bar{r}_{\text{group}})\right] - \beta \cdot D_{KL}(\pi_\theta \Vert \pi_{\text{ref}})
$$

- 以**組內相對獎勵** $r - \bar{r}_{\text{group}}$ 取代優勢函數 → **不需 Value Model**；
- 只需 **Policy + Reference** 兩個模型；
- 組內相對化**降低獎勵變異數**，提升穩定性；
- 加上 KL 懲罰，防止策略偏離太遠。
- 結論：對 LLM 訓練而言，GRPO 更簡單、更穩定、顯存更低。

### 11.4.2 GRPO 訓練實戰

- **前提**：已完成 SFT（GRPO 需要合理的初始策略），`model_name` 指向 SFT 模型。
- 訓練正常的跡象：平均獎勵逐步上升、KL 維持在合理範圍。

**GRPO 專屬參數**：

| 類別 | 參數 | 建議 |
|---|---|---|
| 生成 | `num_generations` | 每題產生幾個答案（組大小），典型 4–8 |
| | `max_new_tokens` | 256–512 |
| | `temperature` | 0.7–1.0，保持探索性 |
| 優化 | `learning_rate` | 比 SFT 小：1e-6～1e-5；小模型上太大（如 5e-5）會策略崩塌 |
| | `kl_coef` | 0.05–0.1（0.01 太小易偏離、0.5 太大學不動） |
| | `clip_range` | 0.2（同 PPO 的 $\epsilon$） |
| 獎勵 | `reward_type` | `accuracy` / `length_penalty` / `step` / `combined` |
| | `reward_config` | 例如 combined 的各組件權重、目標長度、步驟加分 |

### 11.4.3 GRPO 訓練過程解析

**訓練循環**：
1. **採樣**：每題用目前策略產生 `num_generations` 個答案，形成一「組」；
2. **計算獎勵** $r_i$；
3. **相對獎勵**：$\bar{r} = \frac{1}{N}\sum r_i$，$\hat{r}_i = r_i - \bar{r}$；
4. **策略更新**：以相對獎勵更新，並加 KL 懲罰；
5. 重複直到完成所有 epoch。

**例子**：4 個答案獎勵 [1.0, 1.0, 0.0, 0.8]，平均 0.7 → 相對獎勵 [+0.3, +0.3, −0.7, +0.1]。正確且簡潔的機率提高、錯誤的降低、正確但冗長的只小幅提升。即鼓勵「**比組內平均更好**」的答案。

**KL 散度懲罰**：

$$
D_{KL} = \sum_{t=1}^{T} \log \frac{\pi_\theta(a_t \mid s, a_{<t})}{\pi_{\text{ref}}(a_t \mid s, a_{<t})}
$$

限制更新幅度，避免「遺忘」SFT 學到的格式與知識。`kl_coef` 太小 → 格式混亂；太大 → 難以超越 SFT；建議 0.05–0.1。

**訓練監控指標**：
- **平均獎勵**：應上升；不升 → LR 太小／KL 太大／獎勵設計不良；先升後降 → 過擬合或獎勵崩塌。
- **KL 散度**：合理範圍 0.01–0.1；>0.5 → 偏離太遠（增 `kl_coef` 或降 LR）；<0.001 → 幾乎沒更新（減 `kl_coef` 或增 LR）。
- **準確率**：應提升。
- **生成品質**：需人工檢查格式與推理。
- 監控工具：**Weights & Biases**（推薦，自動記錄 `train/reward`、`train/kl`、`train/loss`、`train/learning_rate`、`train/epoch`）、**TensorBoard**（`tensorboard --logdir=<output_dir>`）、或直接看訓練日誌。

**常見問題與對策**：

| 問題 | 可能原因 | 對策 |
|---|---|---|
| 獎勵不上升 | LR 太小、KL 太大、獎勵設計差、SFT 太弱 | 增 LR（1e-5→5e-5）、減 `kl_coef`（0.1→0.05）、檢查獎勵、重訓 SFT |
| KL 爆炸（>0.5～1.0）、格式混亂 | LR 太大、KL 太小、獎勵太激進 | 降 LR（5e-5→1e-5）、增 `kl_coef`（0.05→0.1）、調獎勵、梯度裁剪 |
| 準確率升但品質降 | 只看準確率、KL 太小、過擬合 | 組合獎勵、增 `kl_coef`、減 epoch 或加資料 |
| OOM | 同時生成多答案＋參考模型輸出 | 減 `num_generations`（8→4）、batch（4→2）、`max_new_tokens`（512→256）、梯度檢查點、混合精度 |

---

## 11.5 模型評估與分析

### 11.5.1 評估指標體系

| 類別 | 指標 | 說明 |
|---|---|---|
| **準確性** | Accuracy | 正確數 / 總題數；簡單但無法區分接近與完全錯誤 |
| | Accuracy@K | 產生 K 個答案至少一個對；反映模型「潛力」 |
| | Numerical Error | $\frac{1}{N}\sum \lvert y_i - \hat{y}_i \rvert$；可區分接近（72.5）與離譜（100） |
| **效率** | Avg Length | 平均 token 數；越短推理成本越低 |
| | Avg Steps | 平均推理步驟；2–5 步較適當，過多代表冗餘 |
| | Inference Time | 實際部署的使用者體驗 |
| **品質** | Format Correctness | 是否含 "Step"、"Final Answer" 等標記 |
| | Reasoning Coherence | 步驟間邏輯是否連貫（需人工或評估模型） |
| | Explainability | 是否易於理解與驗證 |

### 11.5.2 評估實戰

`evaluate` 可一次傳入 `metrics` 列表（`accuracy`、`accuracy_at_k`、`average_length`、`average_steps`、`format_correctness`）與 `k`。建議並列比較**預訓練 / SFT / GRPO** 三個模型的準確率、平均長度、格式正確率。

### 11.5.3 錯誤分析

**四類錯誤**：
- **計算錯誤**：步驟對但算錯（如 48/2 = 25）→ 數值計算能力不足
- **推理錯誤**：解題邏輯錯（運算順序錯）→ 邏輯推理不足
- **理解錯誤**：誤解題意（問「總共」只算一部分）→ 語言理解不足
- **格式錯誤**：答案對但缺 "Final Answer:" → 格式學習不足

範例結果（76 個錯誤）：計算 42.1%、理解 28.9%、推理 23.7%、格式 5.3% → 計算能力最需加強；格式錯誤少代表 SFT 有效。

依難度分組：簡單（1–2 步）78.5%、中等（3–4 步）58.3%、困難（5+ 步）31.6% → **多步推理能力仍待提升**。

### 11.5.4 改進方向

持續迭代：**訓練 → 評估 → 分析錯誤 → 確定問題 → 選擇改進方向 → 重新訓練**。

---

## 11.6 完整訓練流程實戰

### 11.6.1 端到端訓練流程

六個階段：**資料準備 → SFT 訓練 → SFT 評估 → GRPO 訓練 → GRPO 評估 → 儲存結果／部署**。書中以 `AgenticRLPipeline` 類別 + `config.json`（model / data / sft / grpo / eval / monitoring 區塊）實作整條流程，結果寫入 `training_results.json`。

**實務建議**：
- **從小規模開始**：先用 100–1000 筆快速迭代驗證流程與參數，再擴大。
- **資料品質檢查**：必要欄位、空值、重複樣本。
- **資料擴增**：改寫問題（答案不變）、產生相似題、回譯；注意避免引入雜訊。

### 11.6.2 超參數調優

| 方法 | 做法 | 優點 | 缺點 |
|---|---|---|---|
| **網格搜尋** | 窮舉所有組合（如 LR × rank × kl_coef） | 簡單、可找到網格內最佳 | 成本高，參數多時不可行 |
| **隨機搜尋** | 隨機取樣（LR 用對數均勻分布） | 效率高，適合大搜尋空間 | 可能錯過最佳解 |
| **貝氏最佳化** | 以機率模型引導搜尋（如 Optuna） | 樣本效率高 | 實作較複雜、需額外套件 |

### 11.6.3 分散式訓練

HelloAgents 基於 TRL + Hugging Face **Accelerate**，原生支援多 GPU／多節點，**訓練程式碼不需修改**，只要用 `accelerate launch --config_file xxx.yaml train_script.py` 啟動。

- **方案選擇**：
  - 單機多卡（2–8 卡）→ **DDP**（每張卡持完整模型副本，資料切分）
  - 大模型（>7B）→ **DeepSpeed ZeRO-2 / ZeRO-3**（分片優化器狀態、梯度、參數）
  - 多節點叢集 → **ZeRO-3 + Offload**（優化器狀態與參數卸載到 CPU）
- 用 `accelerate config` 互動產生設定檔；多節點時各節點設定不同 `machine_rank`，並指定 `main_process_ip/port`。
- **最佳實踐**：
  - 總 batch = `per_device_batch × num_gpus × gradient_accumulation_steps`，換配置時盡量維持總 batch 一致；
  - 學習率縮放：`lr_new = lr_base × sqrt(batch_new / batch_base)`（例：batch 16→64，5e-5→1e-4）；
  - 除錯：`ACCELERATE_LOG_LEVEL=INFO`、`NCCL_DEBUG=INFO`、`watch -n 1 nvidia-smi`。

### 11.6.4 生產部署

1. **模型匯出**：用 PEFT 載入 LoRA 權重後 `merge_and_unload()` 合併進基礎模型，再 `save_pretrained`（含 tokenizer）。
2. **推理最佳化**：8-bit 量化（`load_in_8bit=True`）、`device_map="auto"`。
3. **API 服務**：用 FastAPI 包裝 `/generate` 端點，`uvicorn api:app --host 0.0.0.0 --port 8000` 啟動。

---

## 11.8 本章小結

**（1）Agentic RL 的本質**：把 LLM 當作可學習策略嵌入「感知－決策－執行」循環，用 RL 優化多步任務。與 PBRFT 的差異：

- 任務性質：單輪對話 → 多步序貫決策
- 狀態空間：靜態 prompt → 動態演化的環境狀態
- 行動空間：純文字 → 文字＋工具＋環境操作
- 獎勵設計：單步品質評估 → 長期累積回報
- 優化目標：短期回應品質 → 長期任務成功

**（2）六大核心能力**：推理、工具使用、記憶、規劃、自我改進、感知。

**（3）訓練流程**：預訓練（通常直接用現成模型）→ **SFT**（學格式與基礎推理）→ **RL / GRPO**（試錯優化推理策略、超越訓練資料）。
**SFT 是基礎，RL 是提升**：沒有 SFT，RL 很難成功；沒有 RL，模型只能模仿訓練資料。

**學習路徑建議**：
- 基礎：RL 基礎（MDP、策略梯度、PPO）、LLM 基礎（Transformer、預訓練、微調）、跑 HelloAgents 範例
- 進階：深入 TRL、自訂資料集、自訂獎勵函數、超參數調優
- 高階：長序列多步推理、工具學習、多智能體協作、追蹤前沿論文

---

## 附錄：關鍵公式速查

| 名稱 | 公式 |
|---|---|
| 預訓練損失 | $-\sum_t \log P(x_t \mid x_{<t}; \theta)$ |
| SFT 損失 | $-\sum_i \log P(y_i \mid x_i; \theta)$ |
| RM 損失 | $-\mathbb{E}[\log \sigma(r_\phi(x,y_w) - r_\phi(x,y_l))]$ |
| RLHF/PPO 目標 | $\mathbb{E}[r_\phi(x,y)] - \beta D_{KL}(\pi_\theta \Vert \pi_{\text{ref}})$ |
| Agentic RL 目標 | $\mathbb{E}_{\tau}[\sum_t \gamma^t r(s_t, a_t)]$ |
| LoRA | $h = Wx + \frac{\alpha}{r} BAx$ |
| GRPO 目標 | $\mathbb{E}\left[\frac{\pi_\theta}{\pi_{\text{ref}}}(r - \bar{r}_{\text{group}})\right] - \beta D_{KL}$ |
| 長度懲罰 | $r_{\text{acc}} - \alpha \max(0, l - l_{\text{target}})$ |
| 步驟獎勵 | $r_{\text{acc}} + \beta s$ |

## 主要參考文獻

- [1] Schulman et al. (2017) — PPO
- [2] Shao et al. (2024) — DeepSeekMath（GRPO）
- [3] Hu et al. (2021) — LoRA
- [4] Cobbe et al. (2021) — GSM8K
- [5] Ouyang et al. (2022) — InstructGPT / RLHF
- [6] Rafailov et al. (2023) — DPO
- [7] Lee et al. (2023) — RLAIF
- [9] von Werra et al. — TRL
- [10] Qwen Team (2025) — Qwen3
