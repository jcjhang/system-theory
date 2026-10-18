# MDP 手算練習（Lewis §11.2）

老師提示：Lewis **§11.2 Markov Decision Processes** 可能會考一題。這份對應 §11.2 的內容。PI / VI 屬於 §11.3，已經在 `practice-pi-vi.md`。數字都設計成分數，**所有數字都用程式驗算過**。

> 編號注意：`midterm-prepare.md` 的「11.1」對應 Lewis §11.2（Bellman 方程）；筆記的「11.2」是 PI / VI，對應 Lewis §11.3。

---

## 先搞懂：§11.2 在講什麼

`practice-pi-vi.md` 第 1 題（機器人電量）**其實就是一個 MDP**。§11.2 只是把它寫成正式的樣子，再多講兩件事：**隨機策略**，以及**矩陣寫法**。

**MDP = $(X, U, P, R)$**

| 符號 | 意思 | 機器人例子 |
|---|---|---|
| $X$ | 狀態集合 | {H, L} |
| $U$ | 動作集合 | {W, C} |
| $P^u_{xx'}$ | 在 $x$ 做 $u$，跑到 $x'$ 的**機率** | $P^W_{HL} = \tfrac12$ |
| $R^u_{xx'}$ | 在 $x$ 做 $u$、跑到 $x'$ 時付的**成本** | $R^W_{LL} = 4$ |
| $\pi(x, u)$ | 策略：在 $x$ 選 $u$ 的**機率** | 「H 時一半工作一半充電」 |
| $\gamma$ | 折扣 $0 \le \gamma < 1$ | $\tfrac12$ |

- **Markov 性質**：下一步去哪只看「現在的狀態和動作」，不看以前怎麼來的。
- **確定性策略**：每個狀態只選一個動作（機率 1），寫成 $u = h(x)$。`practice-pi-vi.md` 用的都是這種。
- **隨機策略**：同一個狀態可以用機率混合好幾個動作，例如 $\pi(H, W) = \pi(H, C) = \tfrac12$。

**§11.2 的主線：策略一旦固定，MDP 就變成 Markov chain**

選動作的自由沒了，每個狀態「下一步去哪」的機率就固定了。這叫**閉迴路 Markov chain**，跟控制裡「$u = -Kx$ 代進去得到閉迴路 $A - BK$」是同一個意思。

| | 控制（LQR） | MDP |
|---|---|---|
| 開迴路 | $x_{k+1} = Ax + Bu$ | $P^u_{xx'}$（每個 $u$ 一張轉移表） |
| 策略 | $u = -Kx$ | $\pi(x, u)$ |
| 閉迴路 | $x_{k+1} = (A - BK)x$ | $p_{xx'} = \sum_u\pi(x, u)P^u_{xx'}$（一張轉移矩陣 $P$） |
| 評分 | Lyapunov 方程（Example 11.2-1） | $V = c + \gamma PV$（$N$ 條線性方程） |

**§11.2 的公式**（以下 $N$ = 狀態數）

| 用途 | 公式 | 書上式號 |
|---|---|---|
| 閉迴路轉移矩陣 | $p_{ij} = \sum_u\pi(i, u)\,P^u_{ij}$，每列加起來 = 1 | (11.2-2) |
| 每個狀態走一步的期望成本 | $c_i = \sum_u\pi(i, u)\sum_jP^u_{ij}R^u_{ij}$，即 $c = (P \odot R)\mathbf 1$ | (11.2-33) |
| Bellman 方程（評分） | $V = c + \gamma PV$ ⇒ $V = (I - \gamma P)^{-1}c$ | (11.2-17)、(11.2-33) |
| Bellman 最佳性方程 | $V^*(x) = \min_u\sum_{x'}P^u_{xx'}\big[R^u_{xx'} + \gamma V^*(x')\big]$ | (11.2-20) |
| 最佳動作 | $u^* = \arg\min_u(\text{同上})$ | (11.2-21) |
| 機率分布怎麼走 | $p_{k+1}^T = p_k^TP$，$p_k^T = p_0^TP^k$ | (11.2-34, 35) |
| 穩態分布 | $p_\infty^T = p_\infty^TP$（$P$ 在特徵值 1 的**左**特徵向量），元素加起來 = 1 | (11.2-36) |
| 平均回訪時間 | $T_i = 1/p_\infty(i)$ | |
| 長期平均每步成本 | $\bar V = p_\infty^T(P \odot R)\mathbf 1 = p_\infty^Tc$ | (11.2-39) |

$P \odot R$ 是**逐元素相乘**（Hadamard 積），$(P \odot R)\mathbf 1$ 就是「每列 $p_{ij}r_{ij}$ 加起來」= 走一步的期望成本。手算時直接算 $c_i$ 比較快。

---

## 答題模板

1. **寫出閉迴路 $P$**：每個狀態，把各動作的轉移機率乘上 $\pi(x, u)$ 再加起來。**檢查每列和 = 1**
2. **寫出 $c$**：每個狀態，把各動作的期望成本乘上 $\pi(x, u)$ 再加起來
3. **評分**：寫 $V = c + \gamma PV$（$N$ 條聯立），解出 $V$；或用 $(I - \gamma P)^{-1}c$
4. **穩態**：解 $p^T = p^TP$ 加上 $\sum p = 1$
5. **最佳性**：每個狀態對每個動作算 $\sum_{x'}P^u_{xx'}[R^u_{xx'} + \gamma V(x')]$，取 min

---

## 第 1 題：隨機策略的閉迴路 Markov chain（機器人電量）

跟 `practice-pi-vi.md` 第 1 題**同一個 MDP**，$\gamma = \tfrac12$：

| 狀態 | 動作 | 成本 | 下一步 |
|---|---|---|---|
| H | W（工作） | 0 | H（$\tfrac12$）、L（$\tfrac12$） |
| H | C（充電） | 1 | H（1） |
| L | W（硬撐工作） | 4 | L（1） |
| L | C（充電） | 2 | H（1） |

這次用**隨機策略**：每個狀態都丟銅板，$\pi(x, W) = \pi(x, C) = \tfrac12$。

**(a)** 寫出閉迴路轉移矩陣 $P$ 和期望成本向量 $c$。
**(b)** 求這個策略的 value $V$。和最佳策略的 $V^* = (\tfrac45, \tfrac{12}{5})$ 比較。
**(c)** 從 $p_0 = (1, 0)$（一開始在 H）出發，算 $p_1, p_2$。求穩態分布 $p_\infty$ 和平均回訪時間。
**(d)** 求長期平均每步成本。

### (a) 閉迴路 $P$ 和 $c$

**轉移矩陣**：每個狀態「各動作的機率 × 那個動作的轉移」加起來。

H 那一列：
- 做 W（機率 $\tfrac12$）：到 H $\tfrac12$、到 L $\tfrac12$ → 貢獻 H $\tfrac14$、L $\tfrac14$
- 做 C（機率 $\tfrac12$）：到 H 1 → 貢獻 H $\tfrac12$
- 合計：$p_{HH} = \tfrac14 + \tfrac12 = \tfrac34$，$p_{HL} = \tfrac14$

L 那一列：
- 做 W（$\tfrac12$）：到 L 1 → 貢獻 L $\tfrac12$
- 做 C（$\tfrac12$）：到 H 1 → 貢獻 H $\tfrac12$
- 合計：$p_{LH} = \tfrac12$，$p_{LL} = \tfrac12$

$$P = \begin{bmatrix}p_{HH} & p_{HL}\\ p_{LH} & p_{LL}\end{bmatrix} = \begin{bmatrix}\tfrac34 & \tfrac14\\[2pt] \tfrac12 & \tfrac12\end{bmatrix}$$
檢查：每列和 = 1 ✓

**期望成本**：每個狀態「各動作的機率 × 那個動作的成本」加起來。
- $c_H = \tfrac12 \cdot 0 + \tfrac12 \cdot 1 = \tfrac12$
- $c_L = \tfrac12 \cdot 4 + \tfrac12 \cdot 2 = 3$

$$c = \begin{bmatrix}\tfrac12\\ 3\end{bmatrix}$$

（這題的成本不管跑到哪個 $x'$ 都一樣，所以不用分 $R_{xx'}$。第 2 題會遇到成本跟著 $x'$ 變的情況。）

### (b) 評分

**方法一：寫聯立**（$V = c + \gamma PV$，一個狀態一條）
$$V(H) = \tfrac12 + \tfrac12\big[\tfrac34V(H) + \tfrac14V(L)\big] = \tfrac12 + \tfrac38V(H) + \tfrac18V(L)$$
$$V(L) = 3 + \tfrac12\big[\tfrac12V(H) + \tfrac12V(L)\big] = 3 + \tfrac14V(H) + \tfrac14V(L)$$

整理（$V$ 移到左邊）：
$$\tfrac58V(H) - \tfrac18V(L) = \tfrac12 \quad\cdots(1)$$
$$-\tfrac14V(H) + \tfrac34V(L) = 3 \quad\cdots(2)$$

(1) × 8：$5V(H) - V(L) = 4$ → $V(L) = 5V(H) - 4$
代入 (2) × 4：$-V(H) + 3V(L) = 12$ → $-V(H) + 15V(H) - 12 = 12$ → $14V(H) = 24$
$$V(H) = \tfrac{12}{7} \approx 1.714, \qquad V(L) = 5 \cdot \tfrac{12}{7} - 4 = \tfrac{32}{7} \approx 4.571$$

**方法二：矩陣**（考試若要求用 (11.2-33)）
$$I - \gamma P = \begin{bmatrix}1 - \tfrac38 & -\tfrac18\\[2pt] -\tfrac14 & 1 - \tfrac14\end{bmatrix} = \begin{bmatrix}\tfrac58 & -\tfrac18\\[2pt] -\tfrac14 & \tfrac34\end{bmatrix}$$
$\det = \tfrac58 \cdot \tfrac34 - \tfrac18 \cdot \tfrac14 = \tfrac{15}{32} - \tfrac{1}{32} = \tfrac{7}{16}$

$2 \times 2$ 反矩陣（對角交換、反對角變號、除以 det）：
$$(I - \gamma P)^{-1} = \frac{16}{7}\begin{bmatrix}\tfrac34 & \tfrac18\\[2pt] \tfrac14 & \tfrac58\end{bmatrix}$$
$$V = \frac{16}{7}\begin{bmatrix}\tfrac34 \cdot \tfrac12 + \tfrac18 \cdot 3\\[2pt] \tfrac14 \cdot \tfrac12 + \tfrac58 \cdot 3\end{bmatrix} = \frac{16}{7}\begin{bmatrix}\tfrac34\\[2pt] 2\end{bmatrix} = \begin{bmatrix}\tfrac{12}{7}\\[2pt] \tfrac{32}{7}\end{bmatrix} \checkmark$$

**比較**：

| 策略 | $V(H)$ | $V(L)$ |
|---|---|---|
| 丟銅板（本題） | 1.714 | 4.571 |
| 最佳 $(W, C)$（`practice-pi-vi.md`） | **0.8** | **2.4** |

隨機策略比較差：一半的機會在 L 硬撐工作（成本 4），也有一半的機會在 H 白白充電。
這呼應書上的一句話：在 ergodic 假設下，**每個 MDP 都有一個確定性的最佳策略**，所以最佳化時只要在每個狀態比較「單一動作」就好（(11.2-20) 對 $u$ 取 min，而不是對 $\pi$）。

### (c) 機率分布與穩態

**機率分布怎麼走**：$p_{k+1}^T = p_k^TP$（**列向量乘在左邊**）。
$$p_1^T = \begin{bmatrix}1 & 0\end{bmatrix}P = \begin{bmatrix}\tfrac34 & \tfrac14\end{bmatrix}$$
$$p_2^T = \begin{bmatrix}\tfrac34 & \tfrac14\end{bmatrix}P = \begin{bmatrix}\tfrac34 \cdot \tfrac34 + \tfrac14 \cdot \tfrac12 & \tfrac34 \cdot \tfrac14 + \tfrac14 \cdot \tfrac12\end{bmatrix} = \begin{bmatrix}\tfrac{11}{16} & \tfrac{5}{16}\end{bmatrix}$$

（再一步 $p_3 = (\tfrac{43}{64}, \tfrac{21}{64}) \approx (0.672, 0.328)$，越來越接近下面的穩態。）

**穩態**：$p^T = p^TP$，也就是「再走一步分布不變」。設 $p = (p_H, p_L)$：
$$p_H = \tfrac34p_H + \tfrac12p_L \;\Rightarrow\; \tfrac14p_H = \tfrac12p_L \;\Rightarrow\; p_H = 2p_L$$
（第二條方程跟第一條是同一條，所以要再加「機率和 = 1」）
$$p_H + p_L = 1 \;\Rightarrow\; 3p_L = 1 \;\Rightarrow\; p_\infty = \big(\tfrac23, \tfrac13\big)$$

意思：跑很久以後，機器人 $\tfrac23$ 的時間在高電量、$\tfrac13$ 的時間在低電量。

**平均回訪時間** $T_i = 1/p_\infty(i)$：
- $T_H = \tfrac{1}{2/3} = \tfrac32$：從 H 出發，平均 1.5 步回到 H
- $T_L = \tfrac{1}{1/3} = 3$：從 L 出發，平均 3 步回到 L

<details>
<summary>（直接驗算 $T_L = 3$）</summary>

從 L 出發：$\tfrac12$ 機率直接留在 L（1 步回來）；$\tfrac12$ 機率去 H。在 H 每步有 $\tfrac14$ 機率去 L，平均要 4 步才離開 H 到 L。
$T_L = \tfrac12 \cdot 1 + \tfrac12 \cdot (1 + 4) = 3$ ✓
</details>

**特徵值觀點**：$P$ 的特徵值是 1 和 $\text{tr}P - 1 = \tfrac54 - 1 = \tfrac14$。
- $\lambda = 1$：右特徵向量是 $\mathbf 1$（因為每列和 = 1）；**左**特徵向量是 $p_\infty$
- 另一個 $\lambda = \tfrac14$，$|\lambda| < 1$，所以 $p_k \to p_\infty$。$p_k$ 和 $p_\infty$ 的差距每步縮成 $\tfrac14$：$p_H$ 跟 $\tfrac23$ 的差是 $\tfrac13 \to \tfrac{1}{12} \to \tfrac{1}{48}$
- $\gamma < 1$ 時 $\gamma P$ 的特徵值都 $< 1$，所以 $I - \gamma P$ 一定可逆，(b) 一定解得出來

### (d) 長期平均每步成本

$$\bar V = p_\infty^Tc = \tfrac23 \cdot \tfrac12 + \tfrac13 \cdot 3 = \tfrac13 + 1 = \tfrac43$$

意思：跑很久之後，平均每步付 $\tfrac43$。（這是**不折扣**的平均；(b) 的 $V$ 是**有折扣**的總和，兩個是不同的量。）

---

## 第 2 題：看狀態圖、成本跟著 $x'$ 變、驗證最佳性

（仿 Lewis Figure 11.2-1 的畫法：每條箭頭標 $P$ 和 $R$。）兩個狀態 A、B，兩個動作 $u_1$、$u_2$，$\gamma = \tfrac12$：

```
在 A 做 u1：  A → A  P = 1/2, R = 1        在 B 做 u1：  B → A  P = 1,   R = 4
              A → B  P = 1/2, R = 3
在 A 做 u2：  A → B  P = 1,   R = 1        在 B 做 u2：  B → A  P = 1/2, R = 2
                                                         B → B  P = 1/2, R = 0
```

**(a)** 對策略 $h = (u_1, u_2)$（A 做 $u_1$、B 做 $u_2$），寫出 $P$、$R$、$P \odot R$、$c = (P \odot R)\mathbf 1$，並求 $V^h$。
**(b)** 寫出 Bellman 最佳性方程（兩條）。說明它為什麼是**非線性**的，而 (a) 的 Bellman 方程是**線性**的。
**(c)** 驗證 $V^* = (2, 2)$ 滿足最佳性方程，並求最佳動作。
**(d)** 用 (a) 的 $V^h$ 做一次改進，看會不會得到 (c) 的最佳策略。

### (a) 給定策略的評分

策略是確定性的，所以每個狀態只抄那個動作的箭頭。

A 做 $u_1$：$p_{AA} = \tfrac12$（$r = 1$），$p_{AB} = \tfrac12$（$r = 3$）
B 做 $u_2$：$p_{BA} = \tfrac12$（$r = 2$），$p_{BB} = \tfrac12$（$r = 0$）

$$P = \begin{bmatrix}\tfrac12 & \tfrac12\\[2pt] \tfrac12 & \tfrac12\end{bmatrix}, \quad R = \begin{bmatrix}1 & 3\\ 2 & 0\end{bmatrix}, \quad P \odot R = \begin{bmatrix}\tfrac12 \cdot 1 & \tfrac12 \cdot 3\\[2pt] \tfrac12 \cdot 2 & \tfrac12 \cdot 0\end{bmatrix} = \begin{bmatrix}\tfrac12 & \tfrac32\\[2pt] 1 & 0\end{bmatrix}$$

$c = (P \odot R)\mathbf 1$ = 每列加起來：
$$c = \begin{bmatrix}\tfrac12 + \tfrac32\\[2pt] 1 + 0\end{bmatrix} = \begin{bmatrix}2\\ 1\end{bmatrix}$$
（白話：從 A 出發走一步平均付 2，從 B 出發平均付 1。）

**Bellman 方程** $V = c + \gamma PV$：
$$V(A) = 2 + \tfrac12\big[\tfrac12V(A) + \tfrac12V(B)\big] = 2 + \tfrac14V(A) + \tfrac14V(B)$$
$$V(B) = 1 + \tfrac12\big[\tfrac12V(A) + \tfrac12V(B)\big] = 1 + \tfrac14V(A) + \tfrac14V(B)$$

兩式相減：$V(A) - V(B) = 1$
兩式相加，令 $S = V(A) + V(B)$：$S = 3 + \tfrac12S$ → $S = 6$
$$V^h(A) = \tfrac72 = 3.5, \qquad V^h(B) = \tfrac52 = 2.5$$

### (b) Bellman 最佳性方程

每個狀態，把**每個動作**都寫出來，取 min（照 (11.2-20)：$\sum_{x'}P^u_{xx'}[R^u_{xx'} + \gamma V^*(x')]$）：

$$V^*(A) = \min\Big\{\underbrace{\tfrac12\big[1 + \tfrac12V^*(A)\big] + \tfrac12\big[3 + \tfrac12V^*(B)\big]}_{u_1},\; \underbrace{1 + \tfrac12V^*(B)}_{u_2}\Big\}$$
$$V^*(B) = \min\Big\{\underbrace{4 + \tfrac12V^*(A)}_{u_1},\; \underbrace{\tfrac12\big[2 + \tfrac12V^*(A)\big] + \tfrac12\big[0 + \tfrac12V^*(B)\big]}_{u_2}\Big\}$$

整理 $u_1$ 在 A 那項：$2 + \tfrac14V^*(A) + \tfrac14V^*(B)$；$u_2$ 在 B 那項：$1 + \tfrac14V^*(A) + \tfrac14V^*(B)$。

**為什麼非線性？** 因為有 **min**。$\min\{\cdot, \cdot\}$ 不是線性函數（兩條直線取下緣是折線），所以這是 $N$ 條**非線性**方程，不能一次解出來，要嘛猜答案再驗證，要嘛用 PI / VI 疊代。
(a) 的 Bellman 方程策略已經固定，**沒有 min**，所以是 $N$ 條**線性**方程，直接解聯立。
（LQR 版本：Bellman 方程 = Lyapunov 方程，對 $P$ 線性；最佳性方程 = DARE，對 $P$ 非線性。見 `midterm-2024-sol.md` 5F，也就是 Lewis Example 11.2-1。）

### (c) 驗證 $V^* = (2, 2)$

代 $V^*(A) = V^*(B) = 2$ 進 (b) 的右邊，每個動作算一次：

| 狀態 | $u_1$ | $u_2$ | min | 等於左邊？ | 最佳動作 |
|---|---|---|---|---|---|
| A | $2 + \tfrac14 \cdot 2 + \tfrac14 \cdot 2 = 3$ | $1 + \tfrac12 \cdot 2 = 2$ | 2 | $= V^*(A) = 2$ ✓ | $u_2$ |
| B | $4 + \tfrac12 \cdot 2 = 5$ | $1 + \tfrac14 \cdot 2 + \tfrac14 \cdot 2 = 2$ | 2 | $= V^*(B) = 2$ ✓ | $u_2$ |

兩條都成立 → $V^* = (2, 2)$，最佳策略 $h^* = (u_2, u_2)$：兩個狀態都做 $u_2$。

（為什麼「代進去成立」就夠了？因為 $\gamma < 1$ 時最佳性方程的解是唯一的。）

### (d) 用 $V^h$ 改進一次

用 (a) 的 $V^h = (3.5, 2.5)$，每個狀態把每個動作都算一次（就是 `practice-pi-vi.md` 的「改進」步驟）：

| 狀態 | $u_1$ | $u_2$ | 選 |
|---|---|---|---|
| A | $2 + \tfrac14(3.5 + 2.5) = 3.5$ | $1 + \tfrac12 \cdot 2.5 = 2.25$ | **$u_2$**（變了） |
| B | $4 + \tfrac12 \cdot 3.5 = 5.75$ | $1 + \tfrac14(3.5 + 2.5) = 2.5$ | $u_2$ |

（檢查：目前策略選的那格 = $V^h$ 自己：A 的 $u_1$ = 3.5、B 的 $u_2$ = 2.5 ✓）

新策略 $(u_2, u_2)$ = (c) 的最佳策略。一次改進就到了；它的 value 是 $(2, 2)$，比 $(3.5, 2.5)$ 小，符合「改進不會變差」。

---

## 第 3 題：觀念是非題（§11.2）

| 敘述 | | 理由 / 改正 |
|---|---|---|
| Markov 性質：下一個狀態的機率只看目前的狀態與動作 | ✓ | 不看歷史 |
| 確定性系統 $x_{k+1} = f(x_k, u_k)$ 不是 MDP | ✗ | 是機率為 1 的特例 |
| 固定策略後，MDP 變成 Markov chain | ✓ | 轉移機率 $p_{xx'} = \sum_u\pi P^u$ 固定，沒有選擇了 |
| 閉迴路轉移矩陣 $P$ 每**行**（column）和為 1 | ✗ | 每**列**（row）和為 1（從某狀態出發，去所有地方的機率和） |
| $P$ 一定有特徵值 1 | ✓ | 每列和 = 1 → $P\mathbf 1 = \mathbf 1$ |
| 穩態分布是 $P$ 在 $\lambda = 1$ 的**右**特徵向量 | ✗ | **左**特徵向量；右特徵向量是 $\mathbf 1$ |
| $0 \le \gamma < 1$ 時 Bellman 方程的解唯一 | ✓ | $I - \gamma P$ 可逆 |
| 有 $N$ 個狀態時，Bellman 方程是 $N$ 條線性方程 | ✓ | (11.2-17) |
| 有 $N$ 個狀態時，Bellman 最佳性方程也是 $N$ 條線性方程 | ✗ | 有 min → 非線性 |
| 最佳策略可能必須是隨機策略 | ✗ | ergodic 假設下必存在**確定性**最佳策略 |
| 有限時間的逆推 (11.2-13) 就是 DP，要知道 $P$、$R$，離線、逆時間 | ✓ | Ch 6 |
| Bellman 方程兩邊是同一個 $V$，因為用了無限時間成本 | ✓ | 有限時間時左邊是 $V_k$、右邊是 $V_{k+1}$ |
| $p_\infty(i)$ = 平均回訪時間 $T_i$ | ✗ | $p_\infty(i) = 1/T_i$ |
| DT LQR 的 Bellman 方程是 Lyapunov 方程 | ✓ | Example 11.2-1：$(A - BK)^TP(A - BK) - P + Q + K^TRK = 0$ |
| DT LQR 的 Hamiltonian $H(x_k, u_k)$ 就是 TD 誤差 | ✓ | (11.2-31)：$x^TQx + u^TRu + V(x_{k+1}) - V(x_k)$ |

---

## 總整理

| 題目給你 | 你要做 | 公式 |
|---|---|---|
| MDP + 策略（可能是隨機的） | 閉迴路 $P$、$c$ | $p_{ij} = \sum_u\pi P^u_{ij}$，$c_i = \sum_u\pi\sum_jP^u_{ij}R^u_{ij}$ |
| 策略的 value | 解 $N$ 條線性聯立 | $V = c + \gamma PV = (I - \gamma P)^{-1}c$ |
| 長期行為 | 解 $p^T = p^TP$、$\sum p = 1$ | $T_i = 1/p_\infty(i)$，$\bar V = p_\infty^Tc$ |
| 某個 $V$ 是不是最佳 | 每個動作代一次，取 min，看是否等於自己 | (11.2-20, 21) |
| LQR 版 | Bellman → Lyapunov，最佳性 → DARE | Example 11.2-1 |

**考場提醒**：
- 閉迴路 $P$ 算完**先檢查每列和 = 1**
- 成本跟 $x'$ 有關時，期望成本要**每條箭頭的 $P \times R$ 加起來**，不是 $R$ 直接平均
- 穩態方程 $p^T = p^TP$ 會少一條（有一條是多餘的），一定要補 $\sum p = 1$
- 有折扣的總成本 $V$ 和不折扣的平均成本 $\bar V$ 是不同的東西
