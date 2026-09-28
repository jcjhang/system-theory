# 系統理論期中考準備（白話版）

**考試時間：** 2026-10-27
**形式：** 閉書，可帶一張 A4 公式紙
**範圍：**
- Lewis《Optimal Control》Ch 1, 2, 3, 6, 11
- Żak《Systems and Control》Ch 3, 4, 5

---

## 開始之前：這門課在做什麼？

想像你在開車。你的**目標**是「到目的地」，但你不會亂踩油門——你想：
- **快一點到**（時間成本）
- **少花油**（能量成本）
- **不要撞到人**（安全約束）
- **平穩不要暈車**（狀態變化不要太劇烈）

「同時考慮這些」，然後找出**最好的開車方式**——這就是「最佳控制 (Optimal Control)」。

**這門課給你的工具：**
1. **Ch 1**：多變數微積分中的最佳化（不涉及時間）
2. **Ch 2, 3**：帶著時間的最佳化（離散、連續）
3. **Ch 6**：Bellman 的天才想法——倒著想
4. **Ch 11**：不知道系統怎麼運作也能學會控制（強化學習）
5. **Żak Ch 3**：控制之前，先問「這系統能被控制嗎？」
6. **Żak Ch 4**：這系統會不會爆炸？
7. **Żak Ch 5**：另一個角度看最佳控制（變分法、Pontryagin）

---

## 主角登場：DC 馬達

整份筆記用同一個東西當例子——**一顆直流馬達**（像電風扇的馬達）。

- **輸入**：電壓 $u(t)$（你能決定的東西）
- **輸出**：轉速 $\omega(t)$、轉到的角度 $\theta(t)$
- **物理關係**：加壓越大轉越快，但摩擦會讓它減速

**用數學寫出來（連續時間）：**
$$\dot\omega = -a\omega + bu$$

**這條方程在說什麼？**
- $\dot\omega$ 是轉速的變化率
- $-a\omega$：轉得越快，摩擦阻力越大（負號代表把它拉慢）
- $+bu$：加電壓會讓它加速

為了方便舉例，我們令 $a = 1$、$b = 1$，變成：
$$\dot\omega = -\omega + u$$

**更完整的二維版本**（同時管位置和速度）：
$$\dot\theta = \omega, \quad \dot\omega = -\omega + u$$

寫成矩陣：
$$\dot x = \underbrace{\begin{bmatrix}0 & 1\\ 0 & -1\end{bmatrix}}_{A} x + \underbrace{\begin{bmatrix}0\\ 1\end{bmatrix}}_{B} u, \quad x = \begin{bmatrix}\theta\\ \omega\end{bmatrix}$$

**離散版本**（每秒鐘量一次的話）：
$$\omega_{k+1} = 0.9\,\omega_k + 0.1\, u_k$$

**接下來每一章，我們都會用這顆馬達來做例子。**

---

## 零、先備知識（真的從零開始）

### 0.1 什麼是「狀態」？

**狀態 (state)** = 「要描述系統現在的樣子，最少需要幾個數字」。

- 馬達：需要「轉速」+「角度」→ 狀態是 2 維
- 一顆球在空中：需要「位置 (x, y, z)」+「速度 (vx, vy, vz)」→ 狀態是 6 維
- 一顆股票：也許只需要「現在的價格」→ 1 維

我們把這些數字排成一個直行的向量：
$$x = \begin{bmatrix}\theta \\ \omega\end{bmatrix}$$

### 0.2 什麼是「狀態方程」？

**狀態方程 (state equation)** = 「告訴我下一秒（或下一瞬間）狀態怎麼變」。

連續版：$\dot x = f(x, u)$，意思是「現在的狀態和控制決定了狀態變化多快」。
離散版：$x_{k+1} = f(x_k, u_k)$，意思是「下一步的狀態由現在決定」。

**線性系統**是最簡單的情況：
$$\dot x = A x + B u$$
- $A$：告訴你**自然**會怎麼演變（放著不管的話）
- $B$：告訴你**電壓 $u$** 會怎麼推動狀態

### 0.3 矩陣就是「有結構的一堆數字」

- **向量** $x = [x_1, x_2]^T$：一堆數字排成一直行
- **矩陣** $A$：一個表格，能把一個向量變成另一個向量 $Ax$
- **轉置** $A^T$：把矩陣「翻過來」，行變列、列變行
- **逆矩陣** $A^{-1}$：$A$ 的「反向操作」，$A A^{-1} = I$
- **特徵值 $\lambda$**：滿足 $A v = \lambda v$ 的數字，代表「$A$ 在某個方向上的伸縮倍率」

**為什麼特徵值重要？** 若 $\dot x = Ax$，解是 $x(t) = e^{At} x_0$。
- 特徵值都是負的 → 系統會慢慢歸零（**穩定**）
- 有正的 → 會爆炸（**不穩定**）
- 有零的 → 停在某個地方（**臨界**）

### 0.4 什麼是「正定 (positive definite)」？

一個方陣 $P$ 是**正定**（記作 $P > 0$）如果：
> **對任何非零的向量 $x$，都有 $x^T P x > 0$**

**直覺**：如果 $P$ 是正定的，那 $V(x) = x^T P x$ 這個函數就像個「碗」——最低點在原點，其他地方都比 0 大。這是「能量函數」的典型模樣。

**怎麼判斷？** 檢查 $P$ 的**所有特徵值都 $> 0$**。

### 0.5 一個關鍵微分公式

給定二次型 $f(u) = \tfrac{1}{2} u^T R u$（$R$ 對稱）：
$$\frac{\partial f}{\partial u} = R u$$

**這條公式後面會用到很多次！** 特別是最佳化 $u^T R u + \dots$ 那種項。

### 0.6 極值的判斷（多變數微積分）

想找函數 $L(u)$ 的最小值：
1. 找**臨界點**：$\frac{\partial L}{\partial u} = 0$（梯度為零）
2. **確認是不是最小**：Hessian $\frac{\partial^2 L}{\partial u^2} > 0$（正定）

**這是整門課所有推導的基本套路**。

---

## 一、Lewis Ch 1：靜態最佳化

### 大意

「靜態」= **沒有時間、沒有動態**。就是純數學：給我一個函數，找它最小值。這章的意義是**建立 Lagrange multiplier 和 Hamiltonian 的觀念**，後面所有動態最佳化都是從這裡長出來的。

### 1.1 無約束最佳化

要找 $L(u)$ 的最小值？
- 必要條件：$L_u = 0$
- 充分條件：$L_{uu} > 0$

**馬達例子**：假設你想讓馬達達到穩態，最省電又要接近目標轉速：
$$L(u) = \underbrace{\tfrac{1}{2}(\omega - \omega_{\text{ref}})^2}_{\text{離目標多遠}} + \underbrace{\tfrac{1}{2} r u^2}_{\text{電壓有多大}}$$

穩態時 $\omega = u$（因為 $\dot\omega = 0$ 給出 $-\omega + u = 0$）：
$$L(u) = \tfrac{1}{2}(u - \omega_{\text{ref}})^2 + \tfrac{1}{2} r u^2$$
微分：$L_u = (u - \omega_{\text{ref}}) + r u = 0 \Rightarrow u^* = \dfrac{\omega_{\text{ref}}}{1 + r}$

**這告訴你什麼？**
- $r = 0$（完全不在意電費）：$u^* = \omega_{\text{ref}}$，剛好達成目標
- $r$ 很大（很在意電費）：$u^* \to 0$，寧可轉慢一點也要省電
- **這就是控制中永遠的 trade-off**

### 1.2 帶約束的最佳化：Lagrange multiplier 出場

「約束」= 有些條件必須滿足，不能亂選。例如：「最小化 $L(x, u)$，同時 $f(x, u) = 0$」。

**技巧**：發明一個新變數 $\lambda$（Lagrange multiplier），把兩件事合成一件事：
$$H(x, u, \lambda) = L(x, u) + \lambda^T f(x, u)$$
這個 $H$ 叫 **Hamiltonian**（後面每章都會出現）。

**必要條件（三兄弟）**：
$$\frac{\partial H}{\partial \lambda} = 0 \quad(\text{約束}), \quad \frac{\partial H}{\partial x} = 0, \quad \frac{\partial H}{\partial u} = 0$$

**$\lambda$ 有什麼意義？** $\lambda$ 就是「這條約束的價格」——約束放鬆一點，最小值會下降多少。這在動態問題中會變成 **costate**。

---

## 二、Lewis Ch 2：離散時間最佳控制

### 大意

現在有**時間**了！每一秒 $k = 0, 1, 2, \dots, N-1$ 你都要做決定 $u_k$，狀態會演變 $x_{k+1} = f(x_k, u_k)$。

**目標**：整個過程的總成本最小。

### 2.1 一般問題（把 Ch 1 拉長 N 倍）

**成本**（總開銷 = 沿路開銷 + 最後付一筆）：
$$J = \phi(x_N) + \sum_{k=0}^{N-1} L(x_k, u_k)$$

**方法**：每一步都寫一個 Hamiltonian
$$H^k = L(x_k, u_k) + \lambda_{k+1}^T f(x_k, u_k)$$
（注意是 $\lambda_{k+1}$，因為它代表「下一個狀態的價格」）

**三個條件（每一步都要滿足）**：
| 方程 | 用途 | 方向 |
|---|---|---|
| $x_{k+1} = \partial H^k/\partial \lambda_{k+1}$（就是 $f$ 本身）| 狀態方程 | 往前算 |
| $\lambda_k = \partial H^k/\partial x_k$ | 共態方程 | 往後算 |
| $0 = \partial H^k/\partial u_k$ | 決定最佳 $u_k$ | 每步 |

**邊界條件**：
- $x_0$ 一開始就給你了
- $x_N$ 如果「自由」（隨便到哪都可以）→ $\lambda_N = \partial\phi/\partial x_N$
- $x_N$ 如果「固定」（一定要到某個地方）→ 就用該值

這叫**兩點邊值問題**：狀態邊界在 $k=0$、共態邊界在 $k=N$，兩邊解在中間會合。

### 2.2 離散 LQR：本章最重要

「LQR」= Linear Quadratic Regulator。「Linear」= 系統是線性的，「Quadratic」= 成本是二次的。這是**最經典的最佳控制問題**。

**設定**：
- 系統：$x_{k+1} = A x_k + B u_k$
- 成本：$J = \tfrac{1}{2} x_N^T S_N x_N + \tfrac{1}{2}\sum(x_k^T Q x_k + u_k^T R u_k)$
- $Q \ge 0$（state 要小的話 $Q$ 就選大）
- $R > 0$（control 要小的話 $R$ 就選大）
- $S_N \ge 0$（末態要接近零的話 $S_N$ 就選大）

**神奇結果**（不用背推導，記結論）：

最佳控制長這樣：
$$\boxed{u_k^* = -K_k x_k}$$
就是「用一個增益 $K_k$ 乘上目前的狀態」。

$K_k$ 由 **Riccati 方程**倒推：
$$S_k = A^T S_{k+1} A - A^T S_{k+1} B (B^T S_{k+1} B + R)^{-1} B^T S_{k+1} A + Q$$

從 $S_N$ 開始一路往前算 $S_{N-1}, S_{N-2}, \dots$，每一步同時得到：
$$K_k = (B^T S_{k+1} B + R)^{-1} B^T S_{k+1} A$$

**最佳成本**：$J^* = \tfrac{1}{2} x_0^T S_0 x_0$

**為什麼實用？**
- $S_k$ 可以**事先算好**存起來（因為只依賴 $A, B, Q, R$）
- 執行時只做一個矩陣乘法 $u_k = -K_k x_k$，超快

**馬達例子**：$\omega_{k+1} = 0.9\,\omega_k + 0.1\, u_k$，$Q = 1$、$R = 1$、$S_N = 0$、$N = 2$

倒推：
- $S_2 = 0$
- $S_1 = 0.9 \cdot 0 \cdot 0.9 - 0 + 1 = 1$
- $S_0 = 0.9 \cdot 1 \cdot 0.9 - 0.9 \cdot 1 \cdot 0.1 (0.1 \cdot 1 \cdot 0.1 + 1)^{-1} 0.1 \cdot 1 \cdot 0.9 + 1$
        $= 0.81 - 0.081 \cdot (1.01)^{-1} \cdot 0.09 + 1$
        $\approx 0.81 - 0.0072 + 1 \approx 1.803$

$K_0 = 0.1 \cdot 1 \cdot 0.9 / (0.01 + 1) \approx 0.089$

**結論**：$u_0 = -0.089\,\omega_0$。若目前 $\omega_0 = 10$，你會下 $u_0 = -0.89$（用負電壓煞車）。

---

## 三、Lewis Ch 3：連續時間最佳控制

### 大意

跟 Ch 2 一模一樣，但**時間變成連續**：sum 變積分、difference 變微分。故事結構完全相同。

### 3.1 & 3.2 一般問題

- 系統：$\dot x = f(x, u, t)$
- 成本：$J = \phi(x(T), T) + \int_{t_0}^T L(x, u, t)\, dt$
- Hamiltonian：$H = L + \lambda^T f$

**必要條件（跟離散版對照）**：
| 離散 | 連續 |
|---|---|
| $x_{k+1} = \partial H/\partial \lambda_{k+1}$ | $\dot x = \partial H/\partial \lambda$ |
| $\lambda_k = \partial H/\partial x_k$ | $-\dot \lambda = \partial H/\partial x$（多一個負號！） |
| $0 = \partial H/\partial u_k$ | $0 = \partial H/\partial u$ |

**注意連續版共態方程多一個負號**：$-\dot\lambda = \partial H/\partial x$。這是連續版的坑，容易寫錯。

**邊界條件**：$x(t_0)$ 給定；末態的處理和離散類似。

### 3.3 連續 LQR

**設定**：$\dot x = Ax + Bu$，$J = \tfrac{1}{2} x^T(T) S(T) x(T) + \tfrac{1}{2}\int(x^T Q x + u^T R u)\, dt$

**微分 Riccati 方程**：
$$\boxed{-\dot S = A^T S + S A - S B R^{-1} B^T S + Q, \quad S(T)\text{ 給定}}$$

從末端 $S(T)$ **往回積分**到 $t = 0$。

**Kalman gain**：$K(t) = R^{-1} B^T S(t)$
**最佳控制**：$u^*(t) = -K(t) x(t)$
**最佳成本**：$J^* = \tfrac{1}{2} x_0^T S(t_0) x_0$

### 3.4 穩態問題與代數 Riccati (ARE)

當 $T \to \infty$，$S(t)$ 會收斂到一個常數 $S_\infty$，$\dot S = 0$，所以：
$$\boxed{0 = A^T S + S A - S B R^{-1} B^T S + Q \quad\text{(ARE)}}$$

這叫**代數 Riccati 方程**，是**時不變系統無窮長時間 LQR 的答案**。

**能不能解出唯一好的答案？** 需要：
- $(A, B)$ **stabilizable**：不可控的部分自己會穩下來
- $(A, \sqrt{Q})$ **detectable**：不能觀察的部分自己會穩下來

**馬達例子**：$\dot\omega = -\omega + u$，$J = \tfrac{1}{2}\int(\omega^2 + u^2)\, dt$（$A=-1$, $B=1$, $Q=R=1$）

ARE（scalar 版）：$0 = -s - s + 1 - s^2 = -2s - s^2 + 1$
整理：$s^2 + 2s - 1 = 0 \Rightarrow s = -1 + \sqrt 2 \approx 0.414$（取正解）

**最佳 gain**：$K = s = 0.414$
**最佳控制**：$u^* = -0.414\,\omega$
**閉迴路**：$\dot\omega = -\omega - 0.414\omega = -1.414\omega$

**結果解讀**：本來馬達自己會用 $\dot\omega = -\omega$ 的速度歸零（時間常數 1 秒）；加了最佳控制後變 $-1.414\omega$（更快歸零，時間常數約 0.7 秒），代價是花了一些電。

---

## 四、Lewis Ch 6：動態規劃（Dynamic Programming, DP）

### 大意

Bellman 的天才想法：**倒著想**。

**Bellman 最佳性原理**（用白話）：
> 「不管你怎麼走到這裡，接下來要怎麼走**只跟現在的狀態有關**。」

意思是：**只要你現在在同一個狀態，最佳未來策略就一樣**（跟怎麼來的無關）。

**這個想法的力量**：不用一次規劃整個 sequence，只要對「下一步」做最佳化，一步步倒推。

### 6.2 離散版 DP：Bellman 方程

$$J_k^*(x_k) = \min_{u_k}\big[L(x_k, u_k) + J_{k+1}^*(x_{k+1})\big]$$

**用白話**：「從 $x_k$ 出發的最佳總成本 = 這一步的成本 + 從下一個狀態出發的最佳總成本」，選讓右邊最小的 $u_k$。

從末端 $J_N^*(x_N) = \phi(x_N)$ 開始倒推。

**經典應用例（Ch 6 開場）**：飛機 routing 問題。城市之間的邊有 fuel cost，找從 A 到 B 的最省 fuel 路徑。從終點倒推，每個節點記錄「從這裡到終點的最佳成本」與「該走哪條邊」。

**離散 LQR 也能用 DP 推**：假設 $J_k^*(x_k) = \tfrac{1}{2} x_k^T S_k x_k$，代入 Bellman 方程，就會得到跟 Ch 2 一模一樣的 Riccati。這證明**兩個路徑殊途同歸**。

### 6.3 連續版 DP：Hamilton-Jacobi-Bellman (HJB) 方程

把 Bellman 方程取 $\Delta t \to 0$，得到：
$$\boxed{-\frac{\partial J^*}{\partial t} = \min_u\Big[L + \left(\frac{\partial J^*}{\partial x}\right)^T f\Big]}$$

**白話**：「最佳成本 $J^*$ 對時間的變化率 = 那一瞬間可能的最佳選擇下的 Hamiltonian」。

邊界條件：$J^*(x(T), T) = \phi(x(T), T)$

**用 HJB 重新推 LQR 的示範**：
猜 $J^*(x, t) = \tfrac{1}{2} x^T S(t) x$，代入 HJB：
- $-\dot J^* = -\tfrac{1}{2} x^T \dot S x$
- $\partial J^*/\partial x = S x$
- $H = \tfrac{1}{2}(x^T Q x + u^T R u) + x^T S(Ax + Bu)$
- 對 $u$ 微分為零：$u^* = -R^{-1} B^T S x$
- 代回，比較兩邊 $x^T (\cdot) x$：
$$-\dot S = A^T S + S A - S B R^{-1} B^T S + Q$$

**跟 Ch 3 一樣！** 這證明 HJB 和變分法給同一個答案。

**馬達例子**（scalar HJB）：$\dot\omega = -\omega + u$，$L = \tfrac{1}{2}(\omega^2 + u^2)$，猜 $J^* = \tfrac{1}{2} s(t) \omega^2$
- HJB：$-\tfrac{1}{2}\dot s\, \omega^2 = \min_u[\tfrac{1}{2}\omega^2 + \tfrac{1}{2} u^2 + s\omega(-\omega + u)]$
- 對 $u$ 微分：$u + s\omega = 0 \Rightarrow u^* = -s\omega$
- 代回整理：$-\dot s = 1 - 2s - s^2$，即 §3.3 那條 Riccati ✓

### 維度詛咒 (Curse of Dimensionality)

DP 要對**每個狀態**都算最佳成本。狀態每加一維，計算量指數上升。這是為什麼 Ch 11 的強化學習方法很重要。

---

## 五、Lewis Ch 11：強化學習 & 適應性最佳控制

### 大意

**前面所有章節**都要**事先知道 $A, B$**（系統動態）才能算 Riccati。但現實中你可能不知道！

**這章的問題**：能不能**邊做邊學**，讓控制自己收斂到最佳？答案是「可以」——這就是強化學習 (Reinforcement Learning, RL)。

### 11.1 Actor-Critic 架構

- **Actor**（演員）：實際下控制 $u$
- **Critic**（評論家）：告訴你「這個策略有多好」

Actor 依 Critic 的評分改進，兩者輪流疊代。

### 11.2 Markov Decision Process (MDP)

RL 的數學框架。要件：
- 狀態空間 $X$、動作空間 $U$
- **轉移機率** $P_{x,x'}^u$：在狀態 $x$ 選動作 $u$，跳到 $x'$ 的機率
- **獎勵/成本** $R_{x,x'}^u$：這個轉移要付的代價

**Value function**（給定策略 $\pi$）：
$$V^\pi(x) = \mathbb E_\pi\Big[\sum \gamma^i r_i \,\Big|\, x_k = x\Big]$$
- 「從狀態 $x$ 開始，用策略 $\pi$，總體期望成本是多少」
- $\gamma$：折扣因子，未來的成本打點折

**Bellman 方程**（一致性條件）：
$$V^\pi(x) = \sum_u \pi(x, u) \sum_{x'} P_{x,x'}^u [R + \gamma V^\pi(x')]$$

**Bellman optimality**（就是離散版 HJB）：
$$V^*(x) = \min_u \sum_{x'} P_{x,x'}^u [R + \gamma V^*(x')]$$

**對 LQR 來說**：
- 用固定策略 $u = -Kx$ → Bellman = **Lyapunov 方程** $(A-BK)^T P (A-BK) - P + Q + K^T R K = 0$
- 最佳策略 → Bellman optimality = **離散 ARE** $A^T P A - P + Q - A^T P B (B^T P B + R)^{-1} B^T P A = 0$

**結論：Ch 4 的 Lyapunov、Ch 3 的 ARE、Ch 6 的 HJB、Ch 11 的 Bellman，全部連在一起。**

### 11.3 Policy Iteration (PI) & Value Iteration (VI)

兩種找最佳策略的疊代方法：

**Policy Iteration**：
1. 給定策略 $\pi$，**算它的 value**（解 Bellman 一致性方程）
2. **改進策略**：對每個 state 選 greedy 動作
3. 重複直到不變

**Value Iteration**：不完整解 Bellman，只做一步 update
$$V_{j+1}(x) = \min_u \sum P^u[R + \gamma V_j(x')]$$

VI 每步比較輕，但需要更多次疊代才收斂。

### Q Function：不需要模型也能學

Value function 是「這個狀態多好」，Q function 是「這個狀態選這個動作多好」：
$$Q^\pi(x, u) = \sum_{x'} P^u[R^u + \gamma V^\pi(x')]$$

**Q function 的神奇之處**：
- 有了 $Q^*$，最佳動作就是 $u^* = \arg\min_u Q^*(x, u)$
- **不需要知道 $P$（系統動態）**！因為 Q 已經把它包進去了

**DT LQR 的 Q function**：
$$Q(x, u) = \tfrac{1}{2}\begin{bmatrix}x\\u\end{bmatrix}^T \underbrace{\begin{bmatrix}A^T P A + Q & A^T P B\\ B^T P A & B^T P B + R\end{bmatrix}}_{\text{叫它 }S} \begin{bmatrix}x\\u\end{bmatrix}$$

從 $S$ 矩陣的兩個 block ($S_{uu}, S_{ux}$) 可以直接讀出 $K = S_{uu}^{-1} S_{ux}$——**不需要 $A, B$**！

**馬達例子**：假設不知道馬達的 $a$（摩擦係數）。用 Q-learning：
1. 隨機下電壓 $u_k$
2. 觀察 $\omega_k \to \omega_{k+1}$ 和實際 cost
3. 用資料更新 Q function 的參數
4. 慢慢收斂到最佳 $K$

**最終結果和「知道 $a$ 直接解 Riccati」一樣好，但不需要模型。**

---

## 六、Żak Ch 3：線性系統

### 大意

**在你設計控制器之前**，得先問兩個基本問題：
1. **這系統能被控制嗎？**（Reachability / Controllability）
2. **我看得到系統的所有狀態嗎？**（Observability）

如果答案是「否」，再厲害的控制設計也沒用。

### 3.1 可達性 (Reachability) & 可控性 (Controllability)

**可達性**：能不能從**原點**開到**任意目標**？
**可控性**：能不能從**任意起點**開到**原點**？

（連續系統中兩者等價；離散系統要多一點條件才等價。）

**如何檢驗？三種方法都要會**：

**方法 1：可控性矩陣**
$$\mathcal C = [B\ AB\ A^2 B\ \cdots\ A^{n-1} B]$$
系統可控 ⇔ rank$(\mathcal C) = n$

**方法 2：可控性 Gramian**（連續）
$$W(t_0, t_1) = \int_{t_0}^{t_1} e^{-At} B B^T e^{-A^T t}\, dt$$
可控 ⇔ $W$ 非奇異

**方法 3：PBH 特徵值檢驗**
可控 ⇔ rank$[sI - A\ \ B] = n$ 對**每個** $s \in \text{eig}(A)$

**如果部分不可控**：只要「不可控的部分自己會穩定」，就叫 **stabilizable**——雖然不完美，還算能用。

**馬達例子**：
$A = \begin{bmatrix}0 & 1\\ 0 & -1\end{bmatrix}$，$B = \begin{bmatrix}0\\ 1\end{bmatrix}$

可控性矩陣：
$$\mathcal C = [B\ AB] = \begin{bmatrix}0 & 1\\ 1 & -1\end{bmatrix}$$
行列式 $= -1 \ne 0$，rank $= 2$ ✓ **可控**

**物理意義**：只用一個電壓輸入，就能同時操縱位置和轉速——雖然它們不是獨立的，但因為有動態耦合（$\dot\theta = \omega$），電壓最終能同時影響兩者。

### 3.2 可觀察性 (Observability)

**問題**：如果只能量輸出 $y = Cx$，能不能反推出所有狀態 $x$？

**如何檢驗**（跟可控性完全對應）：

**方法 1：可觀察性矩陣**
$$\mathcal O = \begin{bmatrix} C\\ CA\\ \vdots\\ CA^{n-1}\end{bmatrix}$$
可觀察 ⇔ rank$(\mathcal O) = n$

**方法 2：可觀察性 Gramian**：$V = \int e^{A^T t} C^T C e^{At}\, dt$ 非奇異
**方法 3：PBH**：rank$\begin{bmatrix} sI - A\\ C\end{bmatrix} = n$ 對每個 $s \in \text{eig}(A)$

**Detectable**：不可觀察部分自己穩定——類似 stabilizable 的概念。

**馬達例子**：假設只量位置 $\theta$，$C = [1\ \ 0]$。
$$\mathcal O = \begin{bmatrix}1 & 0\\ 0 & 1\end{bmatrix}, \text{ rank} = 2 \checkmark$$
**可觀察**。物理意義：只看位置變化就能推算速度（因為速度是位置的導數）。

---

## 七、Żak Ch 4：穩定性（重要！）

### 大意

**問題**：系統會不會爆炸？會不會收斂到原點？

**Lyapunov 的天才想法**：不用解方程！只要找到一個「能量」函數 $V(x)$：
- $V(x) > 0$（除了 $x = 0$）
- $\dot V(x) < 0$（沿著軌跡在減少）

那系統一定會漸近穩定（能量會流失、狀態會歸零）。

### 4.2 穩定性定義

- **Stable**（穩定，Lyapunov 意義）：狀態不會跑遠。
- **Asymptotically stable**（漸近穩定）：狀態會慢慢回到平衡點。
- **Uniformly exponentially stable**（指數穩定）：$\|x(t)\| \le \gamma e^{-\lambda(t - t_0)} \|x_0\|$，最強的穩定性。

### 4.3 線性系統的 Lyapunov 理論

對 $\dot x = Ax$，選 $V(x) = x^T P x$（$P > 0$）。沿軌跡：
$$\dot V = x^T(A^T P + P A) x$$

**Lyapunov 主定理**：
> $\dot x = Ax$ **漸近穩定** ⇔ 對**任意** $Q > 0$，Lyapunov 方程
> $$\boxed{A^T P + PA = -Q}$$
> **有正定解** $P$。

**實務怎麼用**？
1. 取 $Q = I$
2. 解 Lyapunov 方程得到 $P$
3. 看 $P$ 是不是正定
4. 是 → $A$ 穩定；否 → $A$ 不穩定

MATLAB 一行搞定：`P = lyap(A', Q)`。

**強化版 (Theorem 4.2)**：$Q$ 不用整個正定，只要 $Q = C^T C$ 且 $(A, C)$ 可觀察就行。

### 4.4 用 Lyapunov 算成本！

如果 $A$ 穩定，那積分：
$$\boxed{J = \int_0^\infty x^T(t) Q x(t)\, dt = x^T(0)\, P\, x(0)}$$
其中 $A^T P + P A = -Q$。

**這超神奇！** 你不用真的解 $\dot x = Ax$、不用算積分，只要解**一個代數方程**就得到整個積分成本。

**用途**：在控制器設計中，可以用這個公式來評估「這個 gain 好不好」——把 gain 帶進去，算成本，比較。

**馬達例子**：$A = \begin{bmatrix}0 & 1\\ 0 & -1\end{bmatrix}$
特徵值：解 $\det(sI - A) = 0 \Rightarrow s(s+1) = 0 \Rightarrow s = 0, -1$

有一個特徵值為 0 → **不是漸近穩定**（Lyapunov 方程無正定解）。

**物理意義**：把馬達放著不管，速度會歸零（因摩擦），但位置**不會回到 $\theta = 0$**——它停在最後所在的地方。這叫「臨界穩定」。

**加了 LQR 之後**：閉迴路 $A_c = A - BK$，$K$ 由 ARE 決定，$A_c$ 的所有特徵值會在左半平面 → 漸近穩定。

### 4.5 離散版 Lyapunov

對 $x_{k+1} = A x_k$，$V(x) = x^T P x$：
$$\Delta V = V(x_{k+1}) - V(x_k) = x_k^T(A^T P A - P) x_k$$

**離散 Lyapunov 方程**：
$$\boxed{A^T P A - P = -Q}$$

$A$ 的特徵值都**在單位圓內** ⇔ 對任意 $Q > 0$，解 $P$ 正定。

（**注意**：連續系統看「左半平面」；離散系統看「單位圓內」。這是兩個世界的穩定準則。）

### 4.6 Robust Linear Controllers（大致了解）

系統有不確定性（unmatched）或雜訊時，用 Lyapunov 設計 robust state feedback。

---

## 八、Żak Ch 5：另一個角度的最佳控制

### 大意

Żak 用**變分法 (Calculus of Variations)** 為主軸，涵蓋 LQR、DP、Pontryagin。跟 Lewis 的觀點互補。

### 5.1 各種性能指標

要控制什麼，就選什麼 cost：
- 讓 state 小：$\int x^T x\, dt$
- 讓 output 小：$\int y^T y\, dt = \int x^T C^T C x\, dt$
- 讓 control 小：$\int u^T R u\, dt$
- 讓末態接近零：$x^T(t_f) F x(t_f)$

**LQR 標準型**：
$$J = \tfrac{1}{2} x^T(t_f) F x(t_f) + \tfrac{1}{2}\int(x^T Q x + u^T R u)\, dt$$

### 5.2 變分法（大意即可）

**Functional**：吃**函數**、吐**數字**。例如「這條路徑的長度」。

**問題**：找一條函數 $x(t)$ 讓 functional
$$v(x) = \int_{t_0}^{t_1} F(t, x, \dot x)\, dt$$
達到極值（比如最小）。

**必要條件（Euler-Lagrange 方程）**：
$$\boxed{F_x - \frac{d}{dt} F_{\dot x} = 0}$$

**這條方程你要會**——它是變分法的核心結果。

**與 Lagrange 力學的連結**：$F = L = K - U$（動能減位能）→ Lagrange 運動方程 $\dfrac{d}{dt}\dfrac{\partial L}{\partial \dot q} - \dfrac{\partial L}{\partial q} = 0$。

**Transversality conditions**（端點自由的情境）：
| 情況 | 額外條件 |
|---|---|
| 右端 $x_1$ 自由 | $F_{\dot x}|_{t_1} = 0$ |
| 右端 $t_1$ 自由 | $(F - \dot x F_{\dot x})|_{t_1} = 0$ |

### 5.3 LQR（Żak 的推法）

假設 $V = x^T P x$ 是 Lyapunov 函數。**Theorem 5.2**：如果 state feedback $u^* = -Kx$ 使
$$\min_u\Big(\dot V + x^T Q x + u^T R u\Big) = 0$$
成立，那 $u^*$ 是最佳解。

推導很直接：
- 對 $u$ 微分：$u^* = -R^{-1} B^T P x$（就是熟悉的 Kalman gain）
- 代回，經過一些整理：
$$\boxed{A^T P + PA + Q - PBR^{-1}B^T P = 0}$$
就是**代數 Riccati**。跟 Ch 3 一模一樣，跟 Ch 11 的 LQR Bellman optimality 一模一樣，跟 Ch 6 的 HJB quadratic ansatz 一模一樣。

**看到了嗎？五個不同的推導路徑，都指向同一條 ARE。這是這門課的靈魂。**

### 5.4 動態規劃（同 Lewis Ch 6）

Żak 也講 HJB，內容與 Lewis 重疊。

### 5.5 Pontryagin 極小原理（PMP）—— 帶控制限制

**問題**：如果 $u$ 有硬性限制（比如 $|u| \le 1$，代表最大電壓有限），Euler-Lagrange 不能直接用。這時要用 PMP。

**Hamiltonian**：$H(x, u, p) = F + p^T f$
（$p$ 就是 costate，跟 $\lambda$ 一樣角色）

**Theorem 5.6（PMP）**：
$$\boxed{u^* = \arg\min_{u \in U} H(x, u, p)}$$
$$\dot p = -\left(\frac{\partial H}{\partial x}\right)^T$$
末態邊界：$p(t_f) = \nabla_x \Phi|_{t_f}$（若 $x(t_f)$ 自由）

**與 Euler-Lagrange 的差別**：PMP **允許 $u$ 有限制**；Euler-Lagrange 假設無限制。

### Bang-Bang 控制

如果 $H$ 對 $u$ 是**線性**的（比如 min-time 問題），而 $u$ 有限制 $|u| \le 1$，那對 $u$ 微分為零通常沒解——最佳解在**邊界**。

結果：
$$u^*(t) = -\text{sign}(\text{something involving } p^*(t))$$

意思是「一路踩滿，然後一路踩滿反向」——**在極值之間跳來跳去**，這叫 **bang-bang control**。

**馬達例子（最短時間控制）**：
- 系統：$\dot\theta = \omega$，$\dot\omega = u$（假設沒有摩擦，$a = 0$）
- 限制：$|u| \le 1$
- 目標：從 $x(0)$ 用最短時間到 origin
- 成本：$J = \int_0^{t_f} 1\, dt = t_f$（時間本身）

**Hamiltonian**：$H = 1 + p_1 \omega + p_2 u$

**Costate 方程**：
- $\dot p_1 = -\partial H/\partial \theta = 0 \Rightarrow p_1 = c_1$（常數）
- $\dot p_2 = -\partial H/\partial \omega = -p_1 = -c_1 \Rightarrow p_2 = -c_1 t + c_2$（線性）

**極小化 $H$ 對 $u$**：因為 $H = 1 + p_1 \omega + p_2 u$，對 $u$ 是線性的：
$$u^*(t) = -\text{sign}(p_2(t)) = -\text{sign}(-c_1 t + c_2)$$

因為 $p_2$ 是 $t$ 的線性函數，**最多變號一次**——這代表最佳策略是：
1. 先加最大速（$u = +1$ 或 $-1$）
2. 到某個時刻換方向（$u = -1$ 或 $+1$）
3. 剛好在 origin 停下

**這就是「先滿油、後滿煞車」的直覺解！**

---

## 九、五種語言，同一個真理

考試最愛考「殊途同歸」。以下五個路徑都導向 LQR 的 ARE：

| 路徑 | 核心方程 | 誰的 |
|---|---|---|
| 變分法 / TPBVP | 微分 Riccati | Lewis Ch 3 |
| HJB / quadratic ansatz | HJB → Riccati | Lewis Ch 6 |
| Lyapunov + 最佳化 | Lyapunov 方程改造 | Żak Ch 5 |
| MDP Bellman optimality | 離散 ARE for LQR | Lewis Ch 11 |
| Pontryagin | 對 $u$ 微分為零得到 $u^* = -R^{-1}B^T p$ | Żak Ch 5 |

**都得到 $u^* = -R^{-1} B^T P x = -K x$，其中 $P$ 由 ARE 決定。**

---

## 十、A4 公式紙建議

**建議手寫**（動手寫比印的記得住）。按重要性：

**必寫（第一優先）**：
1. Hamiltonian 定義 $H = L + \lambda^T f$
2. 離散最佳控制三兄弟（state, costate, stationarity）表
3. 連續最佳控制三兄弟表（注意共態方程的負號）
4. 離散 LQR：Riccati、$K_k$、$u^* = -K_k x_k$、$J^* = \tfrac{1}{2} x^T S x$
5. 連續 LQR：微分 Riccati、$K = R^{-1} B^T S$
6. **代數 Riccati (ARE)**：$A^T S + SA - SBR^{-1}B^T S + Q = 0$
7. HJB 方程：$-\partial J^*/\partial t = \min_u H$
8. Lyapunov 方程（連續 & 離散）
9. 可控性矩陣 $[B\ AB\ \cdots\ A^{n-1}B]$
10. 可觀察性矩陣 $[C;\ CA;\ \cdots]$
11. PBH 檢驗
12. Euler-Lagrange $F_x - \tfrac{d}{dt} F_{\dot x} = 0$
13. Pontryagin 極小條件

**若還有空間**：
14. Q function 定義與 LQR Q 矩陣結構
15. Transversality conditions 表
16. Bang-bang 的判別

---

## 十一、複習路線圖

**第 1 週**：把 Ch 0 每個概念都懂（狀態、正定、微積分基礎）
**第 2 週**：Lewis Ch 1 → Ch 2 → Ch 3（LQR 三次都推一次，練熟）
**第 3 週**：Żak Ch 3, 4（可控/可觀察/Lyapunov，多做選擇題型）
**第 4 週**：Lewis Ch 6（HJB） + Żak Ch 5（變分、PMP）
**考前 1 週**：Lewis Ch 11 + 整理 A4 公式紙
**考前 3 天**：手推一次「LQR 從變分、HJB、Lyapunov 三個路徑到 ARE」

---

## 十二、最容易被考的六種題型

1. **給 scalar 系統 + cost**，寫下 Hamiltonian、共態、算出 $u^*$
2. **給 $(A, B)$**，判斷可控性；給 $(A, C)$，判斷可觀察性
3. **給 $A$**，用 Lyapunov 判斷是否漸近穩定
4. **LQR 問題**（連續或離散），寫下 Riccati、算 steady-state gain
5. **Bang-bang 控制推導**（$|u| \le 1$ 的 min-time / min-fuel）
6. **HJB quadratic ansatz** 推 Riccati

**共通策略**：不管題目怎麼問，寫下 $H$、寫下三兄弟（狀態、共態、穩定條件）、寫下邊界條件——你已經拿到一半分數。
