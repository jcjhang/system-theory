# 期末專題總覽：以強化學習操作電網（Grid2Op）

## 一句話總結

訓練一個 RL agent 扮演**電網調度員**。每 5 分鐘它觀察電網狀態（線路潮流、負載、發電機、線路是否連接），
然後選擇一個動作：切換變電站的匯流排（bus）、重新連接線路、調整發電機出力等。
目標是在各種情境下**讓電網盡可能長時間運轉、不發生停電**，同時維持低營運成本。
我們要在 **Grid2Op** 模擬器上實作多種 RL 演算法，並與簡單的 baseline 比較。

---

## 1. 用白話說明問題

電網其實是一張**圖（graph）**：

- **節點 = 變電站（substation）。** 每個變電站裡（通常）有 **2 條匯流排（bus）**，
  每個元件（線路端點、發電機、負載）都接在 bus 1 或 bus 2 上。
- **邊 = 輸電線路。** 每條線路有**熱容量上限**。關鍵指標是 `rho = 潮流 / 上限`，
  `rho > 1` 代表該線路**過載**。
- **發電機**發電、**負載**用電，任何時刻供需都必須平衡。

會出什麼問題：

- 用電量與再生能源（風、光）不斷變動，潮流跟著改變，線路就可能過載。
- 線路過載持續約 3 個時間步，**保護裝置會把它跳脫**。它原本的潮流會轉移到其他線路，
  使其他線路也過載，形成**連鎖故障（cascading failure）**。
- 線路也可能隨機跳脫（「opponent」，模擬暴風、故障），或因**計畫性維修**而停用。
- **遊戲結束** = 停電：負載無法被供應，或電網被切成孤島（islanding）。

調度員（我們的 agent）可以做什麼：

| 動作類型 | 作用 | 成本 | 動作空間 |
|---|---|---|---|
| **拓撲：bus split** | 在變電站內把元件在 bus 1 / bus 2 之間移動，藉此改變潮流路徑 | 幾乎免費（切開關） | **離散、極大**：每個變電站有 `2^(元件數-1) - 1` 種組態，大型電網上可超過 6.5 萬種 |
| **拓撲：線路開關** | 切斷或重新連接線路 | 幾乎免費 | 離散，每條線路 1 個 |
| **再調度（redispatch）** | 調高或調低火力機組出力（受爬坡限制） | 要花錢 | 連續，每台發電機 1 維 |
| **削減（curtailment）** | 限制再生能源出力 | 要花錢 | 連續 |
| **儲能** | 電池充電或放電 | 小 | 連續 |

規則（全部由 Grid2Op 強制執行）：操作線路或變電站後有冷卻時間（cooldown）、每步可變更的線路與變電站數量有上限、
發電機爬坡限制，以及 **AC 潮流**物理。

**為什麼用 RL？** 拓撲動作空間是組合爆炸的、動態是非線性的（AC 潮流）、時間跨度很長
（一個月約 8,064 步），而且充滿不確定性。傳統最佳化（在 DC 近似上做 MILP）無法擴展到大規模，
人類調度員則主要靠經驗。

## 2. 轉成 RL 問題

- **狀態 / 觀測**：每條線路的 `rho`、線路狀態、發電機 `p`、負載 `p`、拓撲向量
  （每個元件接在哪條 bus）、冷卻時間、過載計時器、時間（小時/星期）、維修資訊、預測值。
- **動作**：離散的拓撲動作、連續的再調度/削減，或兩者都有。
- **轉移**：Grid2Op 執行 AC 潮流計算（pandapower 或更快的 **LightSim2Grid** backend），
  並套用保護跳脫、維修與 opponent 攻擊。
- **獎勵**（由我們設計）。常見選擇（RL2Grid）：
  `R = α·存活 + β·線路裕度/過載項 + η·(−營運成本)`
- **回合結束**：停電，或情境（chronic）跑完。
- **主要指標**：**存活率（survival rate）** = 撐過的步數比例（1.0 = 撐完整個月）。L2RPN 另外使用標準化
  **分數**：−100 = 立即停電，0 = 什麼都不做的 agent，80 = 撐完情境，100 = 撐完且營運成本再降 20%。
- **Safe RL 觀點（CMDP）**：獎勵維持存活/成本，另外加上帶上限的**成本訊號（cost）**：
  - LSI：切負載或孤島，硬限制（總和 = 0）
  - TLO：線路過載與跳脫，軟預算 `Σ cost ≤ τ`

## 3. 平台：Grid2Op

- 文件：https://grid2op.readthedocs.io/en/latest/
- 安裝：`pip install grid2op lightsim2grid`（LightSim2Grid 比預設的 pandapower backend 快很多）
- 內建環境（第一次 `make` 時下載）：
  - `l2rpn_case14_sandbox`：IEEE 14-bus，14 個變電站、20 條線路。**從這裡開始。**
  - `l2rpn_neurips_2020_track1` / `track2`：IEEE 118-bus，含攻擊或不同再生能源比例
  - `l2rpn_wcci_2022`、`l2rpn_idf_2023`：更大的電網，含儲能與削減
- RL 整合：`grid2op.gym_compat` 提供 Gymnasium wrapper，可直接接 Stable-Baselines3、CleanRL、RLlib。
- 實用功能：`obs.simulate(action)` 可做一步前瞻（「如果這樣做會怎樣」）。Grid2Op 也有用於評估的
  `Runner`，以及 L2RPN 計分模組。

最小範例：

```python
import grid2op
from lightsim2grid import LightSimBackend
from grid2op.gym_compat import GymEnv, BoxGymObsSpace, DiscreteActSpace

env = grid2op.make("l2rpn_case14_sandbox", backend=LightSimBackend())
genv = GymEnv(env)
genv.observation_space = BoxGymObsSpace(env.observation_space,
    attr_to_keep=["rho", "line_status", "topo_vect", "gen_p", "load_p", "timestep_overflow"])
genv.action_space = DiscreteActSpace(env.action_space,
    attr_to_keep=["set_bus", "set_line_status_simple"])   # 或使用縮減後的動作清單
# -> 把 genv 丟進 SB3 / CleanRL：PPO、DQN……
```

## 4. 各篇參考文獻的重點

| # | 論文 | 對我們的意義 |
|---|---|---|
| 1 | **Marot et al., "Learning to Run a Power Network Challenge: a Retrospective Analysis"**（NeurIPS 2020 Competition, PMLR 133） | 定義了**任務、Grid2Op 與 L2RPN 計分方式**。兩個賽道：*Robustness*（隨機線路攻擊）與 *Adaptability*（未見過的再生能源比例）。**冠軍們的做法**：(1) 把**動作空間縮減**到約 200–1000 個好的拓撲動作；(2) **「除非有線路接近上限，否則什麼都不做」**；(3) 執行前**用 `simulate()` 驗證候選動作**（前 5 名中有 4 隊這麼做）；(4) 在此之上訓練 RL：百度用 PARL + 演化搜尋（第 1 名）、華為先模仿學習再用 PPO 微調（第 2 名）、第 3 名用 DDQN。一個單純對 200 個動作做模擬的專家系統，也在其中一個賽道拿到第 2 名。 |
| 2 | **Marchesini et al., "RL2Grid: Benchmarking RL in Power Grid Operations"**（arXiv 2503.23101） | 建立在 Grid2Op 上的**標準化單一 agent benchmark**（Gymnasium + CleanRL，程式碼：`github.com/emarche/RL2Grid`）。電網從 bus14 到 bus118，含維修、opponent、電池等變體。拓撲任務有**難度等級**（依存活率排序的縮減動作集）；再調度任務是連續動作。**啟發式**：*idle*（所有 `rho < 0.95` 時不動作）與 *recovery*（安全時把拓撲恢復原狀）。提供 **CMDP 版本**（LSI、TLO）。**結果**：原版 DQN、PPO、SAC 表現不佳；PPO + 啟發式在 bus14 上存活率約 0.99，但在 bus36、bus118 上仍很低；Lagrangian PPO 也很掙扎。但 RL 仍勝過 idle 與 MILP baseline。**可作為我們實驗設計的範本。** |
| 3 | **Marchesini, Boguslawski et al., "MARL2Grid-TR: A Multi-Agent RL Benchmark in Power Grid Operations"**（ICLR 2026） | **多 agent** 延伸（PettingZoo）。電網切成多個區域，每個 agent 控制部分變電站，可設定局部或全域可觀測。Baseline：**MAPPO、QPLEX、MASAC、Lagrangian MAPPO**。在 bus14 拓撲控制上，**MAPPO 存活率 0.79**、集中式 PPO 0.38、QPLEX 0.04、什麼都不做 0.18。idle 啟發式在多 agent 拓撲任務中反而*有害*，但在再調度任務中有幫助。再調度與削減是相對容易的問題。適合作為「超越單一 agent」的延伸方向。 |
| 4 | **Cui, Ye, Hu, Tang, Lin, Strbac, "Online Preventive Control for Transmission Overload Relief Using Safe RL with Enhanced Spatial-Temporal Awareness"**（IEEE TPWRS 39(1), 2024） | **Safe RL + 更好的網路架構。** 把過載紓解（透過**再調度 + 線路與 busbar 切換**降低過載線路的 `rho`）建模為 **CMDP**，用 **IPO（Interior-point Policy Optimization，PPO 的 log-barrier 版本）** 求解。狀態編碼器使用**圖神經網路（edge-conditioned convolution）處理空間結構 + LSTM 處理時間結構**。在過載降低、限制滿足、對不確定性的強健度上都勝過基於模型與 RL 的 baseline。適合作為「safe RL + GNN」的變體方向。 |

**整體脈絡**：[1] 定義問題並展示哪些技巧有效；[2] 把它整理成乾淨的 benchmark，附上 baseline 與 safe RL 任務；
[3] 延伸到多 agent 控制；[4] 展示一個結合時空（GNN + LSTM）策略的先進 safe RL 方法。

## 5. 我們要做什麼

教授給的目標是**實作多種 RL 演算法來達成目標**，而目標就是在 Grid2Op 情境下讓電網持續運轉（且成本低）。
我們組有 4 個人，整體做法是：

1. **第 0 步（共用基礎）**：以現成的 RL2Grid benchmark 為基礎，統一環境、觀測/動作格式、獎勵、評估腳本與 baseline。
2. **4 個方向分頭研究**：每人負責一個 RL 方向，使用同一套設定與相同的訓練預算。
3. **統一比較**：用同一個評估腳本、同一組測試情境，比較 4 個方向的結果。
4. **組合與分析**：把有效的元素組合成最終模型，並做消融實驗（ablation），說明哪些技巧真的有用。
5. *（選做延伸）* 擴展到更大的電網（bus36/bus118）或多 agent。

## 6. 第 0 步：共用基礎（大部分已有現成的）

不需要從零開始寫。輸入/輸出格式、獎勵、演算法實作都已經有現成的 benchmark，我們只需要補上少數部分。

### 6.1 Grid2Op 本身提供的
- **環境與情境資料**：`grid2op.make("l2rpn_case14_sandbox")`，chronics 已內建。
- **觀測/動作格式**：`grid2op.gym_compat`（`GymEnv`、`BoxGymObsSpace`、`DiscreteActSpace`、`BoxGymActSpace`），直接轉成 Gymnasium 格式。
- **評估工具**：`Runner` 可批次跑多個情境；`grid2op.utils` 有 L2RPN 官方計分類別（如 `ScoreL2RPN2020`），輸出 −100 到 100 的分數。
- **內建 baseline agent**：`DoNothingAgent`、`RecoPowerlineAgent`（自動重新連線）、`TopologyGreedy` 等。

### 6.2 RL2Grid（文獻 2 的官方程式碼，MIT 授權）：我們的共用基礎
- Repo：https://github.com/emarche/RL2Grid
- **標準化任務**：`bus14`、`bus36-MO-v0`、`bus118-MOB-v0`，含難度等級；縮減後的動作集已算好（`env/action_spaces.zip`）。
- **已定義好**：觀測、獎勵（`env/reward.py`）、idle/recovery 啟發式（`env/heuristic.py`，開關在 `env/config.py`）、CMDP cost（`env/cmdp.py`）。
- **已實作演算法**（CleanRL 風格，單檔好改）：`alg/dqn`、`alg/ppo`、`alg/sac`、`alg/td3`、`alg/lagr_ppo`。
- **訓練指令**：`python main.py --env-id bus14 --action-type topology --alg PPO`
- **好處**：大家的輸入/輸出格式、獎勵、動作集都和正式發表的 benchmark 一致，報告可以直接和論文數字比較（例如 bus14 上 PPO + 啟發式存活率約 0.99）。

另外 RTE 官方的 **l2rpn-baselines**（https://github.com/Grid2op/l2rpn-baselines）有 PPO_SB3 等範例，可作參考。

### 6.3 需要我們自己補的
1. **執行環境（重要）**：RL2Grid README 註明**只在 Linux 測試過，且有一個 Grid2Op 修改導致 macOS 無法使用**。
   需要 Linux 機器（實驗室伺服器 / 工作站 / Colab）或 Docker。
   版本鎖定：Python 3.12、`grid2op==1.11.0`、`lightsim2grid==0.9`、`gymnasium==0.29.1`、PyTorch 2.2+。
2. **統一的 `evaluate.py`**：RL2Grid 內建的 `Evaluator`（`env/eval.py`）只在訓練中隨機跑 3 個 episode、只看存活率，
   沒有固定測試集和 L2RPN 分數。我們要寫一個腳本：載入訓練好的模型，在**固定的測試 chronics** 上執行，
   輸出存活率、L2RPN 分數、過載步數、動作次數、營運成本。
3. **Greedy-simulate baseline**：每步對縮減動作集逐一 `simulate()`，選讓最大 `rho` 最低的動作。
   它是強力對照組，也是方向 B 模仿學習的「老師」。可從 Grid2Op 內建的 greedy agent 修改。
4. **Logging**：RL2Grid 預設用 wandb（需在 `main.py` 設定 entity/project），也可以改成 tensorboard。

### 6.4 公平比較規則（大家都要遵守）
- 共用的環境設定、動作集、獎勵、評估腳本**不能私下修改**；要改就全組一起改。
- 每個方向給**相同的訓練預算**（例如相同的 env steps 或 CPU 時數）。
- 每個方法至少 **3 個 seed**，報告平均值 ± 信賴區間。
- 測試 chronics 固定，訓練時不能使用。

## 7. 四個研究方向（每人一個）

| 成員 | 方向 | 核心方法 | 要回答的問題 | 起點（RL2Grid） | 難度／風險 |
|---|---|---|---|---|---|
| **A** | **Value-based** | DQN → Double + Dueling + PER | 經典 L2RPN 做法在統一設定下表現如何？哪些 DQN 改良真的有用？ | `alg/dqn` | 低。實作成熟，最容易先出結果 |
| **B** | **Policy gradient + 模仿學習** | PPO（可加 action masking）；再試 **BC（從 Greedy 專家學）→ PPO 微調**（華為第 2 名的做法） | 專家預訓練能不能大幅提升樣本效率與最終表現？ | `alg/ppo` + 自己加 BC | 中。PPO 是 RL2Grid 最強 baseline，很可能是最好的一組 |
| **C** | **Safe RL** | Lagrangian PPO，進階可做 **IPO**（文獻 4）；cost 用過載（TLO）或切負載/孤島（LSI） | 加入安全限制後，能不能在存活率差不多的情況下明顯減少過載？ | `alg/lagr_ppo` + 自己加 IPO | 中高。論文中 Lagrangian PPO 表現不好，調得起來就最有研究價值 |
| **D** | **結構感知網路** | 把 PPO 的 MLP 換成 **GNN**（PyTorch Geometric，以變電站/線路建圖），進階加 **LSTM**（文獻 4 的時空感知） | 利用電網拓撲結構能不能學得更好、更能泛化到沒看過的情境？ | `alg/ppo` + 自己換網路 | 中高。需要自己設計圖的表示方式 |

- **D 的替代方案**：若大家對多 agent 較有興趣，D 可改做 **MAPPO**（文獻 3），但設定和其他三組差異較大，比較時要另外說明。
- **為什麼這樣分**：
  - 涵蓋 RL 的主要類別（value-based、policy gradient + 模仿、safe RL、網路架構），報告可以寫成系統性比較，符合「實作多種 RL 演算法」。
  - 方向之間可以組合：B、C、D 都基於 PPO，最後可疊加成最終模型（例如 BC 預訓練 + GNN + Lagrangian）。
  - 每組都報告**有無推論階段 `simulate()` 驗證**的結果：取策略的前 k 個動作逐一模擬，執行最好的那個。這是 L2RPN 冠軍們公認最有效的技巧。

## 8. 統一評估流程
- **主要任務**：`bus14` 拓撲控制（difficulty 0 起步，再試更高難度）。
- **對照組**：Do-Nothing、自動重新連線、Greedy-simulate。
- **指標**：**平均存活率**、**L2RPN 分數**、過載步數、動作次數、營運成本。
- **圖表**：學習曲線（多 seed）、各情境存活率熱圖、動作使用分布直方圖。
- **消融實驗**：有無 idle 啟發式、有無動作縮減（不同難度等級）、有無 simulate 驗證、不同獎勵權重。
- **共用結果表**：每週把最新數字更新到同一張表（例如 `results/summary.md`）。

## 9. 時程（假設約 6–8 週）

| 週次 | 工作 |
|---|---|
| 第 1 週 | 第 0 步：在 Linux 上裝好 RL2Grid、跑通 `bus14` PPO、寫好 `evaluate.py` 與 Greedy baseline |
| 第 2–4 週 | 各自研究方向 A–D，每週同步一次並更新共用結果表 |
| 第 5 週 | 中期比較，挑出有效的元素 |
| 第 6 週起 | 組合成最終模型、消融實驗；選做擴展到 bus36/118 |
| 最後 | 期末報告與投影片 |

## 10. 建議的專案結構
```
final/
├── overview.md            # 本檔案（專題總覽與分工計畫）
├── rl2grid/               # fork 的 RL2Grid（共用基礎）
│   ├── alg/               # dqn（A）、ppo + bc（B）、lagr_ppo / ipo（C）、ppo_gnn（D）
│   └── env/               # 獎勵、啟發式、cost（共用，改動需全組同意）
├── scripts/               # evaluate.py、greedy_baseline.py、plot.py
├── results/               # log、曲線、summary.md（共用結果表）
└── report/                # 期末報告與投影片
```

## 11. 可能遇到的坑
- **macOS 無法跑 RL2Grid**：請在 Linux 或 Docker 上執行（見 6.3）。
- **模擬很慢**：使用 LightSim2Grid、平行環境，並先用較短的訓練 chronics。
- **失敗訊號稀疏且延遲**：大部分時間步都是安全的，沒有 idle 啟發式的話 agent 學不到多少東西；
  加上之後，每一步都是「危險時刻」。
- **非法動作**（冷卻中）會被默默忽略，請使用 action masking 或懲罰。
- **大型電網的動作空間極大**：不要嘗試在所有拓撲上學習。
- **不同 seed 之間變異很大**：一律報告平均值 ± 信賴區間。
- 從論文得到的預期：case14 是可解的（加上技巧後存活率 ≥0.9），而 bus36/118 即使是已發表的 baseline 也很難。先從小的開始。

## 參考文獻
1. A. Marot et al., *Learning to Run a Power Network Challenge: a Retrospective Analysis*, PMLR 133, 2021. https://proceedings.mlr.press/v133/marot21a.html
2. E. Marchesini et al., *RL2Grid: Benchmarking Reinforcement Learning in Power Grid Operations*, arXiv:2503.23101, 2025. https://arxiv.org/abs/2503.23101 （程式碼：https://github.com/emarche/RL2Grid）
3. E. Marchesini, E. Boguslawski et al., *MARL2Grid-TR: A Multi-Agent RL Benchmark in Power Grid Operations*, ICLR 2026.
4. H. Cui, Y. Ye, J. Hu, Y. Tang, Z. Lin, G. Strbac, *Online Preventive Control for Transmission Overload Relief Using Safe Reinforcement Learning With Enhanced Spatial-Temporal Awareness*, IEEE Trans. Power Systems 39(1):517–532, 2024. doi:10.1109/TPWRS.2023.3257259
