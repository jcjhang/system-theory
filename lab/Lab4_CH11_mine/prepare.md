# Tutorial 個人準備筆記

> 這份是給自己看的，不是講稿。目的是：上台前把「講得出來」變成「被問也答得出來」。
> 順序依 tutorial 的段落排列；每段最後有「可能被問的問題」。

---

## 縮寫對照表

**訓練方法**

| 縮寫 | 全名 | 一句話 |
|---|---|---|
| SFT | Supervised Fine-Tuning（監督微調） | 給標準答案，讓模型照著學 |
| RM | Reward Model（獎勵模型） | 幫回答打分的模型，用人類偏好資料訓練 |
| RLHF | Reinforcement Learning from Human Feedback | 人類標偏好 → 訓練 RM → 用 RL 優化 |
| RLAIF | Reinforcement Learning from AI Feedback | 同 RLHF，但偏好改由強大的 AI 模型來標 |
| RLVR | Reinforcement Learning with Verifiable Rewards | reward 由程式驗證（對答案、跑測試），不需要 RM；**我們的實驗屬於這種** |
| PBRFT | Preference-Based Reinforcement Fine-Tuning（基於偏好的強化微調） | 書上對傳統後訓練的統稱：單輪對話、看一次回答打一次分 |
| DPO | Direct Preference Optimization | 直接用偏好對算 loss，不用 RM、不用 RL 迴圈 |

**RL 演算法與概念**

| 縮寫 | 全名 | 一句話 |
|---|---|---|
| MDP | Markov Decision Process（馬可夫決策過程） | 描述 RL 問題的框架：狀態、行動、轉移、獎勵、折扣 |
| PPO | Proximal Policy Optimization | 經典 RL 演算法，需要額外的 value model 估計 advantage |
| GRPO | Group Relative Policy Optimization（群組相對策略優化） | 同一題生成一組答案，和組內平均比，不需要 value model |
| DAPO | Decoupled Clip and Dynamic sAmpling Policy Optimization | GRPO 的改良版，TRL 新版的預設 loss |
| KL | Kullback–Leibler divergence（KL 散度） | 衡量兩個機率分布差多少；用來限制模型不要偏離原本太遠 |
| NLL | Negative Log-Likelihood（負對數似然） | $-\log P(\text{正確答案})$，即 cross-entropy loss |
| PRM | Process Reward Model（過程獎勵模型） | 對每個推理步驟打分，而不是只看最後答案 |

**模型、資料與工具**

| 縮寫 | 全名 | 一句話 |
|---|---|---|
| LoRA | Low-Rank Adaptation（低秩適應） | 凍結原模型，只訓練兩個小矩陣 |
| PEFT | Parameter-Efficient Fine-Tuning | 只訓練少量參數的微調方法統稱；也是 Hugging Face 的套件名 |
| TRL | Transformer Reinforcement Learning | Hugging Face 的 SFT / RL 訓練函式庫 |
| CoT | Chain-of-Thought（思維鏈） | 讓模型一步一步寫出推理過程 |
| GSM8K | Grade School Math 8K | 約 8.5K 題小學數學應用題資料集 |
| EOS | End of Sequence | 告訴模型「寫完了，停下來」的特殊 token |

---

## 0. 上台前 5 分鐘複習清單

- [ ] 主軸一句話：**SFT 教模型「格式」，RL 教模型「做對」；獎勵函數決定「對」是什麼。**
- [ ] 三個數字：Base **4.5%** → SFT **51.0%** → GRPO **55.0%**（GSM8K test 前 200 題）
- [ ] GRPO 的一行公式：$\hat{A}_i = \dfrac{r_i - \text{mean}(r)}{\text{std}(r)}$，不需要 value model
- [ ] 我們踩到的坑：Base 模型不會輸出 `<|im_end|>`，改用 `<|endoftext|>` 當 EOS
- [ ] GRPO 的進步 +4 pt **沒有統計顯著**，要誠實講
- [ ] 練習的執行指令：`python exercise.py`（只需要 numpy）

---

## 1. RL 基本觀念（被問到「RL 到底在優化什麼」時要能講清楚）

### 1.1 MDP 與策略

- MDP $(S, A, P, R, \gamma)$：狀態、行動、轉移、獎勵、折扣。
- **策略 $\pi_\theta(a \mid s)$**：給定狀態，輸出行動的機率分布。**LLM 本身就是一個策略**：狀態 = 目前為止的文字，行動 = 下一個 token（或整段回答）。
- 目標：$J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta}\left[\sum_t \gamma^t r_t\right]$。

### 1.2 Policy gradient（GRPO/PPO 的根）

$$
\nabla_\theta J = \mathbb{E}\left[\nabla_\theta \log \pi_\theta(a \mid s) \cdot A(s, a)\right]
$$

- 直覺：**把 advantage 為正的行動機率調高、為負的調低**，調多少看 advantage 大小。
- 為什麼要 **advantage** 而不是直接用 reward？若所有 reward 都是正的（例如都 0.8–1.0），直接用 reward 會把所有行動都往上推，只是推的程度不同，變異數很大。減掉一個 **baseline**（平均水準）後，「比平均好」才往上、「比平均差」往下，梯度方向不變但變異數小很多。
  - 減 baseline 不改變梯度期望值（因為 $\mathbb{E}[\nabla \log \pi \cdot b] = b \cdot \nabla \sum \pi = 0$）。這句被問到時很好用。
- PPO 用 **value model $V(s)$** 估 baseline；GRPO 用**同一題多個答案的平均 reward** 當 baseline。

### 1.3 稀疏 vs 密集獎勵

- 稀疏：只在最後給（GSM8K 答對 +1）。好處是不會被中間獎勵誤導；壞處是初期訊號少。
- 密集：每步都給（工具呼叫成功 +0.1）。學得快，但容易被 hack。
- 我們的實驗全部是**稀疏、單步**：一題 → 一段回答 → 一個 reward。**嚴格說是 PBRFT 的設定**，只是 reward 來自可驗證的規則而非 reward model。被問「這哪裡 agentic？」時要承認這點（見 §8）。

---

## 2. LLM 訓練流程

| 階段 | 資料 | Loss / 目標 | 一句話 |
|---|---|---|---|
| 預訓練 | 海量文本 | next-token NLL | 學語言與世界知識 |
| SFT | (prompt, completion) | 只在 completion 上算 NLL | 學格式與指令遵循 |
| RM | (prompt, chosen, rejected) | $-\log\sigma(r_w - r_l)$（Bradley–Terry） | 學人類偏好打分 |
| RL（PPO / GRPO） | 只要 prompt ＋ 打分方式 | 最大化 reward − β·KL | 學「做對 / 做好」 |

- **RLHF**：RM 由人類偏好訓練。**RLAIF**：偏好由強模型標註。
- **DPO**（書的參考文獻 [6]，章節沒展開）：直接用偏好對算 loss，跳過 RM 和 RL 迴圈。被問到可以一句帶過：「DPO 是離線、用偏好對；GRPO 是線上、自己採樣自己打分。」
- **RLVR**（Reinforcement Learning with Verifiable Rewards）：reward 由程式驗證（數學答案、單元測試），不用 RM。**我們的 GSM8K 實驗就是 RLVR**，DeepSeek-R1 也是這條路線。

### 為什麼 SFT 要「只在 completion 上算 loss」

- prompt 是題目，模型不需要學會「出題」；只對答案部分算 loss，訓練訊號全部用在學「怎麼回答」。
- TRL 的 prompt–completion 格式預設就這樣做（`completion_only_loss`）。

---

## 3. PBRFT vs Agentic RL（書的核心觀念）

要能**不看稿**講出這張表：

| | PBRFT | Agentic RL |
|---|---|---|
| 狀態 | $s_0$ = prompt，$T = 1$ | $s_t$ = prompt＋歷次觀察，$T \gg 1$ |
| 行動 | 只有生成文字 | 文字＋工具呼叫＋環境操作 |
| 轉移 | 無（一步就結束） | 環境回饋改變狀態（例如搜尋結果） |
| 獎勵 | 最後一次打分 | 可在中間步驟給 |
| 目標 | 單次回答品質 | 長期累積回報 |

**六大能力**：推理、工具使用、記憶、規劃、自我改進、感知。tutorial 只列名稱即可，但要能各舉一個例子。

---

## 4. LoRA

- $W' = W + \frac{\alpha}{r} BA$，$B \in \mathbb{R}^{d\times r}$、$A \in \mathbb{R}^{r\times k}$，只訓練 $A, B$。
- 初始化：$B = 0$，所以訓練開始時模型與原本**完全相同**（這是為什麼 LoRA 不會一開始就把模型弄壞）。
- **我們的實際數字**：r = 16、α = 32、套在 q/k/v/o → 可訓練參數 **4,587,520 / 600,637,440 = 0.764%**。
- `merge_and_unload()`：把 $\frac{\alpha}{r}BA$ 加回 $W$，得到一個普通模型，推論不會變慢。
- **侷限（我們親身遇到）**：LoRA 只改 attention 的投影矩陣，**沒有改 embedding / lm_head**。如果某個 token 的 embedding 在預訓練時根本沒學好（例如 Base 模型的 `<|im_end|>`），LoRA 很難讓模型學會輸出它。解法：(1) 換成模型熟悉的 token（我們的做法）；(2) 把 `embed_tokens`、`lm_head` 加進 `modules_to_save` 一起訓練。

### 可能被問

- **Q：rank 要怎麼選？** 任務越複雜越大；GSM8K 這種格式＋簡單推理，8–16 就夠。α 常設為 r 或 2r，實際縮放是 α/r。
- **Q：LoRA 會比全量微調差多少？** 通常略差，但小資料量時差距不大，還能防過擬合。

---

## 5. GRPO（最可能被追問的部分）

### 5.0 先抓住 RL 在問的唯一一個問題

> **「這個回答，比『預期』好還是差？」**

- 比預期好 → 讓模型以後更常這樣寫（提高這段文字的機率）
- 比預期差 → 讓模型以後少這樣寫（降低機率）

為什麼一定要跟「預期」比，而不是直接看分數？想像兩題：

| | 簡單題 | 難題 |
|---|---|---|
| 模型平常的表現 | 10 次對 9 次 | 10 次對 1 次 |
| 這次答對，拿 1 分 | 理所當然，沒什麼好學 | **很難得，要大力強化** |
| 這次答錯，拿 0 分 | **很反常，要大力修正** | 本來就常錯，稍微修正 |

同樣是 1 分，在兩題代表的意義完全不同。直接用分數更新，模型會一直被簡單題「獎勵」，學不到重點。**「分數 − 預期」就叫 advantage（優勢）**，它才是真正的學習訊號。

PPO 和 GRPO 的差別，只在於**「預期」怎麼算**。

### 5.1 PPO 為什麼麻煩

用「學生寫考卷」來比喻 PPO 需要的 4 個角色：

| 角色 | 比喻 | 做什麼 |
|---|---|---|
| Policy model | **學生** | 寫答案，也是我們要訓練的對象 |
| Reward model | **閱卷老師** | 幫答案打分（我們的實驗用程式對答案取代） |
| Reference model | **學生剛學完 SFT 時的自己** | 當錨點，避免學生為了分數變得面目全非（KL 懲罰） |
| **Value model** | **預測分數的家教** | 看到題目（甚至寫到一半的答案）就預測「這題你大概會拿幾分」，也就是「預期」 |

麻煩都出在**家教（value model）**：

1. **它跟學生一樣大**：0.6B 的學生就要配一個 0.6B 的家教，記憶體和計算都翻倍。
2. **它也要訓練**：一開始家教亂猜，advantage 就跟著亂，學生被錯誤的訊號帶著走。等於要同時教好兩個人。
3. **它要猜的東西很難**：要從「寫到一半的答案」猜最後會拿幾分，對 LLM 來說很難猜準。

### 5.2 GRPO 的想法：不請家教，讓學生自己跟自己比

> **同一題，讓學生寫 8 次。8 次的平均分，就是這題的「預期」。**

- 不用訓練任何額外模型，「預期」直接從資料算出來。
- 難易度自動被考慮進去：簡單題 8 次平均很高，答對也不會多加分；難題平均很低，答對一次就被大力強化。
- 這就是「**G**roup **R**elative」的意思：在同一組（group）裡比相對好壞，像是「同一題內的常態化計分」。

**用我們實驗的真實資料走一遍**（蠟筆題，正解 32，模型寫了 8 次）：

| # | 答案 | reward | 和平均比 | 結果 |
|---|---|---|---|---|
| 1, 2, 6 | 32 ✓ | 1 | 1 − 0.375 = **+0.625** | 提高機率 |
| 0, 3, 4, 5, 7 | 108、70、22、26、57 ✗ | 0 | 0 − 0.375 = **−0.375** | 降低機率 |

- 平均 = 3/8 = 0.375，就是模型目前對這題的「預期」。
- 答對的 3 個：+0.625 × 3 = +1.875；答錯的 5 個：−0.375 × 5 = −1.875。**加總剛好是 0**。這不是巧合：減掉平均之後，正負一定互相抵消。所以 GRPO 做的事情是**把機率從錯的答案「搬」到對的答案**，而不是全部一起往上推。
- 實際上 TRL 還會再除以標準差（0.484），變成 +1.29 / −0.77。這只是把數字縮放到差不多的大小，正負方向不變。好處是：不管 reward 是 0/1 還是 0.9/1.0，每次更新的力道都差不多。

**接著怎麼更新**：答案 1 裡的每個 token（例如 `19*2=38`、`38-6=32`）機率都往上調；答案 0 裡的每個 token（例如 `6*19`）機率都往下調。

- **一整段答案共用同一個分數**。所以答案 6 雖然中間有一句多餘的話，但最後答對，那句話也一起被強化了。這是 GRPO（以及所有只看最終答案的方法）的侷限。

### 5.2.1 兩個「安全裝置」：clip 和 KL

GRPO 也沿用了 PPO 的兩個煞車，它們管的是不同的事：

| | 比喻 | 跟誰比 | 防止什麼 |
|---|---|---|---|
| **clip** | **限速**：每次更新最多只能改一點點 | 上一步的自己 | 單次更新走太遠（短期） |
| **KL 懲罰** | **橡皮筋**：拉著你，不讓你離 SFT 模型太遠 | SFT 時的自己（reference） | 長期累積下來偏離太多，例如格式崩壞、為了分數鑽漏洞 |

- 我們的實驗每批資料只更新一次，clip 幾乎沒有觸發（log 裡 `clip_ratio` 全是 0），真正有作用的是 KL。
- 練習 Part 3 可以直接看到橡皮筋的效果：只用步驟獎勵時，「灌步驟」衝到 100%；加上 KL 後被拉住，只到 40% 左右。

### 5.2.2 整理成一張圖

```
           同一題
             │
     ┌───────┼───────┐   1. 讓模型寫 G 次（G = 8）
     ▼       ▼       ▼
   答案1   答案2 … 答案8
     │       │       │   2. 每個答案打分（對 = 1，錯 = 0）
     ▼       ▼       ▼
     1       0  …    1
      \      |      /    3. 算組內平均 = 「預期」
       ───  平均  ───
     │       │       │   4. advantage = 分數 − 平均（再除以標準差）
     ▼       ▼       ▼
   +1.29  −0.77 … +1.29
     │       │       │   5. 正的提高機率、負的降低機率
     └───────┴───────┘      ＋ clip（限速）＋ KL（橡皮筋）
```

### 5.2.3 完整公式（被問到才需要）

$$
\mathcal{L} = -\frac{1}{G}\sum_i \frac{1}{|o_i|}\sum_t \left[\min\left(\rho_{i,t}\hat{A}_i,\ \text{clip}(\rho_{i,t}, 1-\epsilon, 1+\epsilon)\hat{A}_i\right) - \beta\, \text{KL}_{i,t}\right],\quad \rho = \frac{\pi_\theta}{\pi_{\text{old}}},\quad \hat{A}_i = \frac{r_i - \text{mean}(r)}{\text{std}(r) + \epsilon}
$$

對照上面的直覺：$\hat{A}_i$ 是「和組內平均比」；$\min(\cdot, \text{clip}(\cdot))$ 是限速；$-\beta\,\text{KL}$ 是橡皮筋；$\frac{1}{|o_i|}\sum_t$ 是「整段答案共用同一個分數，平均到每個 token」。

- **書上的公式是簡化版**：只減平均、沒除標準差、沒有 clip。原論文（DeepSeekMath）和 TRL 都會除以標準差。練習裡兩種都有（`normalize=True/False`）。
- **KL 用的估計式**：TRL 用 $k_3 = \frac{\pi_\text{ref}}{\pi_\theta} - \log\frac{\pi_\text{ref}}{\pi_\theta} - 1$，永遠 ≥ 0、變異數小。不用背，被問時知道「是 per-token 的估計，不是精確 KL」即可。
- **用 LoRA 時的 reference model**：就是「把 adapter 關掉的同一個模型」，不用多存一份權重，所以記憶體很省。這也讓 GRPO + LoRA 在我們的實驗裡只用了 4.1 GB。

### 5.3 組內全對或全錯 → 沒有學習訊號

- 全對或全錯時 std = 0，所有 $\hat{A}_i = 0$，這題對梯度沒有貢獻。
- **我們的數據**：GRPO 訓練的 1000 組中，**202 組全對、103 組全錯，共 30.5% 的題目沒有提供學習訊號**，但生成的成本照付（TRL log 的 `frac_reward_zero_std` 就是在監控這個，平均也是 0.305）。
- 延伸：這就是為什麼要挑**難度適中**的題目，也是 curriculum learning、DAPO 的 dynamic sampling 的動機。

### 5.4 我們的設定，和書上的差異

| 參數 | 我們 | 書上 | 理由 |
|---|---|---|---|
| `num_generations` | 8 | 4–8 | |
| `max_completion_length` | 256 | 512 | SFT 後平均約 117 tokens，256 夠用又省時間 |
| `temperature` | 0.8 | 0.7–1.0 | |
| `learning_rate` | 2e-5 | 1e-5 | LoRA 通常可用較大 lr；只跑 250 步 |
| `beta`（KL） | 0.05 | 0.05 | **TRL 預設 0.0，必須自己設** |
| `loss_type` | `grpo` | — | TRL 新版預設 `dapo` |
| `scale_rewards` | `group` | — | 除以組內 std |
| 每步題數 | 4 題 × 8 = 32 個回答 | | `per_device_train_batch_size=8` × `gradient_accumulation_steps=4` |

- TRL 的 `per_device_train_batch_size` 指的是「**回答數**」，不是題數。這點容易搞混。

### 可能被問

- **Q：GRPO 跟 PPO 比，缺點是什麼？** 每題要生成 G 個回答，生成成本高（我們每步 18–25 秒，大部分花在生成）；全對或全錯的題目沒有訊號；advantage 是整段回答共用，沒有 token 層級的 credit assignment。
- **Q：為什麼要 KL？** 防止模型為了 reward 偏離 SFT 太遠，例如格式崩壞、語言退化；也是對 reward hacking 的一道保險（練習 Part 3 可以看到）。
- **Q：DeepSeek-R1 是不是就用這個？** 是，R1 用 GRPO ＋ 可驗證獎勵（答案正確性＋格式）。

---

## 6. 獎勵設計

- 三種內建獎勵：準確率、長度懲罰（答對才扣）、步驟獎勵（答對才加）。
- **「答對才扣 / 才加」的理由**：如果答錯也能拿長度分，模型會學到「寫短一點的錯答案」也有分。
- **Reward hacking**：模型找到拿高分的捷徑，卻沒有真的完成任務。
  - 練習 Part 3 的例子：步驟獎勵讓「正確但灌 10 個空洞步驟」的風格衝到 100%。
  - E3 的實驗結果見 §9：125 步、β=0.05 時沒有出現灌步驟；β=0＋lr 1e-4 時 100 步就灌到平均 9.5 步，還順便不寫 `Final Answer:` 了（見 §9 最後）。
- 我們實際用的參數：長度目標 200 字元、α = 0.001；步驟獎勵每步 +0.1。

---

## 7. 評估的注意事項（被質疑數據時要能回應）

- **測試集**：GSM8K test 前 200 題，greedy decoding，最多 400 tokens，所有模型用同一個 prompt template。
- **統計誤差**：準確率 p ≈ 0.5、n = 200 時，標準誤 $\sqrt{p(1-p)/n} \approx$ **3.5 個百分點**。
- **SFT → GRPO 的配對比較**：SFT 錯、GRPO 對：**23 題**；SFT 對、GRPO 錯：**15 題**。McNemar 檢定 p ≈ 0.26，**不顯著**。正確的講法是「有改善的趨勢」，要確認需要更多測試題或更長的訓練。
- **Base 4.5% 的意義**：Base 模型不會照格式回答，答案擷取會退回去抓「最後一個數字」，有些是碰巧對的（9 題對的裡面有 6 題沒有 `Final Answer:`）。所以 Base 的數字主要代表「**無法使用**」，而不是真實的數學能力。
- **錯誤分類是啟發式的**：沒寫 `Final Answer:` → 格式錯誤；有 `a op b = c` 算錯 → 計算錯誤；其餘歸為推理／理解錯誤。書上分成四類，但推理和理解很難自動區分，所以合併。
- 答對不代表推理對：練習資料蠟筆題的第 6 個回答，中間步驟有一句多餘的錯誤，但最後答案對，一樣拿 reward 1。這是 outcome reward 的侷限，對應 process reward model（PRM）的動機。

---

## 8. 實驗過程中踩到的坑（很好的 tutorial 素材）

1. **Qwen3-0.6B vs Qwen3-0.6B-Base**：書上用的 `Qwen3-0.6B` 已經做過後訓練（有 thinking mode），拿它當「預訓練模型」比較並不公平，所以我們改用 `-Base`。
2. **Base 模型不會停**：第一次 SFT 後，模型寫完答案不會停，接著冒出 `(COLOR)` 之類的怪字、自己出新題目，每次都寫到 400 tokens 上限。
   - 原因：`<|im_end|>` 在 Base 模型裡幾乎沒訓練過，答完後它的機率只有 0.0004，下一個 token 的分布幾乎是平的。LoRA 只改 attention，推不動。
   - 解法：EOS 改用 Base 模型熟悉的 `<|endoftext|>`；pad 改用 `<|fim_pad|>`。pad 和 EOS 不能相同，否則 EOS 可能被當成 padding 遮掉，沒算進 loss。
   - 修好後：SFT 平均輸出從 400 tokens 降到 **117 tokens**。
3. **TRL 預設 `beta = 0`**：沒設的話就沒有 KL 懲罰，和書上不一樣。
4. **TRL 版本差異**：新版改用 `warmup_steps`（可以填比例），沒有 `warmup_ratio`。書上的 HelloAgents 參數名稱與 TRL 不完全對應。

### 被問「這跟 agentic 有什麼關係？」

誠實的回答：**我們的實驗是單步的（PBRFT 的形式），只是用 RL 訓練推理能力。** 真正的 Agentic RL 要把工具呼叫、環境回饋放進 rollout（多輪互動），reward 也可以在中間步驟給。TRL 新版的 `GRPOTrainer` 已經有 `tools`、`environment_factory` 參數支援多輪 rollout，這是自然的下一步。但 GRPO 的核心機制（採樣一組 → 組內比較 → 更新）完全一樣。

---

## 9. 實驗結果速查

### 硬體與時間（Mercury GPU 0，RTX 3090，與他人共用）

| 階段 | 時間 | PyTorch 峰值 | nvidia-smi 最大 |
|---|---|---|---|
| Base 評估（200 題，batch 50） | 3.6 分 | 4.4 GB | 8.5 GB |
| SFT（2000 筆 × 3 epoch，750 步） | 19.6 分 | 2.0 GB | 2.5 GB |
| GRPO accuracy 250 步 | 91.6 分（每步 18–25 秒） | 4.1 GB | 13.2 GB |
| GRPO 長度懲罰／步驟獎勵 125 步 | 42 / 45 分 | 4.1 GB | 11.4 / 13.6 GB |
| GRPO β=0 / β=0.5 / lr=2e-4，各 100 步 | 35 / 37 / 38 分 | 3.7 / 4.1 / 4.1 GB | 11.2 / 9.0 / 9.0 GB |
| 每次評估 | 2–4 分 | 4.3–4.4 GB | 8.5–8.7 GB |
| **E1–E4 合計** | **5.6 小時** | | |

nvidia-smi 看到的比 PyTorch 峰值多很多（GRPO 最多差到 9 GB），因為 PyTorch 的 caching allocator 會保留釋放掉的記憶體；生成時每批長度不同，碎片多，保留得更多。被問「需要多大的卡」：實際用量約 4 GB，16 GB 卡應該夠，12 GB 可能要把 batch 或 `num_generations` 調小。β=0 少 0.36 GB 是因為不用算 reference model 的 log-prob。詳見 `experiments/logs_pulled/gpu_mem.csv`，或 `python demo.py gpu`。

### E1：三個模型

| | Base | SFT | GRPO 125 步 | GRPO 250 步 |
|---|---|---|---|---|
| 準確率 | 4.5% | 51.0% | 54.0% | **55.0%** |
| 格式正確率 | 4.5% | 96.5% | 97.0% | 98.0% |
| 平均 tokens | 386 | 117 | 122 | 123 |
| 平均步驟數 | 0.0 | 3.8 | 3.9 | 3.8 |
| 1–2 步的題目 | 7.8% | 71.9% | 73.4% | 70.3% |
| 3–4 步 | 4.3% | 41.3% | 45.7% | 50.0% |
| 5+ 步 | 0.0% | 40.9% | 43.2% | 43.2% |

- SFT 的訓練 loss 從 0.92 降到 0.37。
- GRPO 的訓練 reward 從約 0.50 升到約 0.69（每步只看 4 題，曲線抖動大），KL 從 0.0005 升到 0.01。

### E2：一組真實回答（蠟筆題，正解 32）

8 個回答對 3 個 → 答對的 $\hat{A} = +1.29$、答錯的 $\hat{A} = -0.77$。完整內容在 `exercise/completions.json`。

### E3：換獎勵函數（各 125 步，從 SFT 出發）

| 獎勵 | 正確率 | 平均 tokens | 平均步驟 | 訓練中平均字數 前 25 步 → 後 25 步 | 訓練中步驟數 |
|---|---|---|---|---|---|
| 只看對錯（acc 125 步） | 54% | 122 | 3.87 | 299 → 321 | 3.49 → 3.61 |
| 長度懲罰 | 52% | 109 | 3.71 | 314 → 278（−11%） | 3.55 → 3.55 |
| 步驟獎勵 | 52% | 119 | 3.87 | 313 → 308 | 3.58 → 3.67 |

- 長度懲罰有效且沒傷到正確率（差距在誤差內）。
- 步驟獎勵 125 步內**沒有**明顯灌步驟。可能原因：β=0.05 的 KL；lr 小；SFT 模型本來就很少寫多餘步驟，8 個回答裡很少出現「多寫步驟又答對」的樣本可以被強化（GRPO 只能強化模型**已經會**寫出來的東西）。
- 最長的 19 步輸出是重複迴圈（degenerate repetition），SFT 本來就有類似現象（≥8 步：SFT 9 個、acc125 與 step 各 12 個），不是 reward hacking。
- 額外實驗 `grpo_step_hack`（步驟獎勵、β=0、lr=1e-4、100 步）專門用來誘發 hacking，結果見下面。

### E4：β 與學習率（各 100 步，accuracy reward）

| 設定 | 正確率 | 格式 | tokens | 第 100 步 KL | KL 最大 | 記憶體 |
|---|---|---|---|---|---|---|
| 基準 β=0.05、lr=2e-5（125 步 checkpoint） | 54% | 97% | 122 | 0.0038 | 0.0044 | 4.09 GB |
| β=0 | 54% | 96% | 119 | 不計算 | — | 3.73 GB |
| β=0.5 | 52% | 98% | 114 | 0.0012 | 0.0012 | 4.09 GB |
| lr=2e-4 | 56% | 100% | 122 | 0.0234 | 0.047（約第 40 步） | 4.09 GB |

- **lr=2e-4 的 KL 先衝到 0.047 再被拉回 0.023**：最直觀的「橡皮筋」畫面（`figures/e4_curves.png` 右圖）。
- β=0.5 時 KL 幾乎不動，訓練 reward 爬最慢。
- 正確率差異全部在 ±3.5 的誤差內。**不要講成「lr 大比較好」**：100 步太短，只能說 β 和 lr 控制「離 SFT 多遠、多快」。被問「為什麼大 lr 沒壞掉」：LoRA 只改 0.76% 參數、而且 KL 有拉住；更長的訓練才可能看到崩壞。
- 基準是 125 步的 checkpoint（我們沒有存 100 步的），比較時要說明。
- 所有 GRPO 實驗的 `clip_ratio` 都是 0：每批只更新一次，新舊策略相同，clip 不會觸發。

### 額外：誘發 reward hacking（`grpo_step_hack`）

設定：步驟獎勵、β=0、lr=1e-4（基準的 5 倍）、100 步。訓練 40.6 分鐘、PyTorch 峰值 3.74 GB（β=0 不用 reference）。

| | 正確率 | 有寫 `Final Answer:` | 平均 tokens | 平均步驟數 |
|---|---|---|---|---|
| SFT | 51% | 96.5% | 117 | 3.81 |
| 步驟獎勵 β=0.05（125 步） | 52% | 97.0% | 119 | 3.87 |
| 步驟獎勵 β=0、lr=1e-4（100 步） | 51% | **6.5%** | **215** | **9.49** |

- **成功誘發**：步驟數 3.8 → 9.5，正確率不變。訓練中平均步驟 4.25 → 8.63、字數 364 → 557；超過 256 token 上限被截斷的比例在第 55 步最高到 64%。
- **典型輸出**（test #1，robe 題）：算完 `2+1=3` 之後重複「It takes 3 bolts of fiber.」三次，沒有 `Final Answer:`。
- **第二個漏洞**：`extract_answer` 抓不到 `Final Answer:` 會退回抓最後一個數字，所以不寫 `Final Answer:` 也拿得到分。可能的原因：省下的 token 可以拿去多寫步驟、不會在 256 上限前被截斷。被問到時的重點：**模型優化的是「打分程式實際接受什麼」，不是「我們希望它怎麼寫」。**
- 評估時同樣靠 fallback 抓答案，所以正確率仍有 51%；錯誤分類裡 91 題被歸為「格式錯誤」。
- 對照 E3：β=0.05、lr=2e-5 時 125 步沒灌水 → KL 和小學習率能拖慢，但根本解法是改獎勵函數（步驟加分設上限、重複步驟不計分、沒寫 `Final Answer:` 就 0 分）。
- 這組不在 `run_all.out` 的分段計時裡，所以 `demo.py gpu` 的 5.6 小時沒有包含它；全部加起來約 6.3 小時。

---

## 10. 練習：要先自己跑過一次

- `exercise/exercise.py`（學生版，3 個 TODO）、`exercise/solution.py`（解答）、`exercise/completions.json`。
- 只需要 Python 3.8+ 與 numpy，本機 < 1 秒。
- 對答案時要帶出的三個重點：
  1. 獎勵函數就是你真正在優化的東西，寫錯就會被鑽漏洞（Part 3 的「灌步驟」）。
  2. GRPO 不需要 value model，因為組內平均就是 baseline（Part 2）。
  3. 整組都一樣的題目沒有學習訊號（大富翁題那組全對 → advantage 全是 0）。
- Part 3 的已知行為：只用準確率獎勵時，三種正確風格的 reward 一樣，所以誰勝出帶有隨機性（換 seed 會不同）。被問到時這正好說明「reward 一樣，模型就沒有理由偏好簡潔」。

---

## 11. 延伸閱讀（被問「想深入要看什麼」）

- **GRPO**：DeepSeekMath（Shao et al., 2024）
- **R1**：DeepSeek-R1（2025），GRPO ＋ 可驗證獎勵產生長推理
- **DAPO**：GRPO 的改良（dynamic sampling、去掉 KL、token-level loss），TRL 新版的預設 `loss_type`
- **PPO**：Schulman et al., 2017
- **LoRA**：Hu et al., 2021
- **TRL 文件**：GRPOTrainer 的參數說明，特別是 `beta`、`scale_rewards`、`loss_type`
