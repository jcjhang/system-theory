# System Theory 期中考 2024 詳解

> 題目：`mid-2024.pdf`（Oct. 22, 2024，open-book）
> 建議先自己寫一遍再對答案。每題最後的「觀念」連到 `midterm-prepare.md` 的章節。

---

## 第 1 題（15%）：周長最小的長方形

### A.（8%）

**問題**：最小化 $L(x, y) = 2x + 2y$，約束 $f(x, y) = xy - a^2 = 0$（$x, y > 0$）。

**Step 1：Hamiltonian**
$$H = 2x + 2y + \lambda(xy - a^2)$$

**Step 2：必要條件**
$$H_x = 2 + \lambda y = 0 \tag{1}$$
$$H_y = 2 + \lambda x = 0 \tag{2}$$
$$H_\lambda = xy - a^2 = 0 \tag{3}$$

**Step 3：解聯立**
- (1) − (2)：$\lambda(y - x) = 0$。若 $\lambda = 0$，(1) 變成 $2 = 0$，矛盾，所以 $\lambda \ne 0$，得 $x = y$
- 代入 (3)：$x^2 = a^2$，長度取正 → $x = y = a$
- 代回 (1)：$\lambda^* = -\dfrac{2}{a}$

**Step 4：確認是最小值**
沿著約束 $y = a^2/x$，$L(x) = 2x + \dfrac{2a^2}{x}$：
$$L'(x) = 2 - \frac{2a^2}{x^2} = 0 \Rightarrow x = a, \qquad L''(x) = \frac{4a^2}{x^3} > 0$$
所以是最小值。（直覺：$x \to 0$ 或 $x \to \infty$ 時 $L \to \infty$。）

**答案**：最小周長的長方形是**邊長 $a$ 的正方形**，$x^* = y^* = a$，$L^* = 4a$，$\lambda^* = -2/a$。

**補充（$\lambda$ 的意義）**：令面積 $c = a^2$，則 $L^*(c) = 4\sqrt c$，
$$\frac{dL^*}{dc} = \frac{2}{\sqrt c} = \frac{2}{a} = -\lambda^*$$
面積每增加一單位，最小周長約增加 $2/a$。

### B.（7%）

**等高線**：$L = 2x + 2y = c$ ⇔ $y = -x + c/2$，是一族**斜率 −1 的平行直線**，往右上方 $L$ 越大。

**約束**：$xy = a^2$ ⇔ $y = a^2/x$，是第一象限的**雙曲線**，經過 $(a/2,\ 2a)$、$(a,\ a)$、$(2a,\ a/2)$，以兩軸為漸近線。

**最佳點**：把等高線從左下往右上推，第一條碰到雙曲線的是 $L = 4a$（直線 $x + y = 2a$），兩者在 $(a, a)$ **相切**。
- $L < 4a$ 的等高線（例如 $x + y = a$）碰不到雙曲線 → 不可行
- $L > 4a$ 的等高線（例如 $x + y = 3a$）跟雙曲線交於兩點 → 可行但不是最小

**梯度**：在 $(a, a)$，$\nabla L = (2,\ 2)$、$\nabla f = (y,\ x) = (a,\ a)$，兩者平行，$\nabla L = -\lambda\nabla f$，$\lambda = -2/a$ ✓

```
 y        示意圖（只畫 L = 4a 那條等高線）
2a ┤╲ ·              ·  雙曲線 xy = a²
   │ ╲ ·             ╲  等高線 x + y = 2a（L = 4a）
   │  ╲  ·           ●  (a, a)：相切點 = 最小值
 a ┤   ╲  ●  ↗ ∇L ∥ ∇f
   │    ╲   ·
   │     ╲     ·   ·   ·
   └──────┼──────┼──────── x
          a      2a
（L = 2a 的直線 x + y = a 在這條的左下方，碰不到雙曲線；
  L = 6a 的直線 x + y = 3a 在右上方，跟雙曲線交於兩點。）
```

圖上要標出：至少三條等高線（$L = 2a, 4a, 6a$）和 $L$ 增大的方向、雙曲線、相切點 $(a, a)$、兩個梯度方向。

**觀念**：Lagrange 三兄弟、相切 ⇔ 梯度平行、二階確認、$\lambda$ 是約束的價格 → §1.2

---

## 第 2 題（15%）：雙線性離散系統

$$x_{k+1} = Ax_k + Dx_ku_k + bu_k, \qquad J = \tfrac12x_N^TS_Nx_N + \tfrac12\sum_{k=0}^{N-1}(x_k^TQx_k + ru_k^2)$$
$x_k \in \mathbb R^n$，$u_k \in \mathbb R$（純量），$S_N \ge 0$、$Q \ge 0$、$r > 0$。

### A.（5%）最佳控制

**Hamiltonian**：
$$H^k = \tfrac12(x_k^TQx_k + ru_k^2) + \lambda_{k+1}^T(Ax_k + Dx_ku_k + bu_k)$$

**駐點條件**：$u_k$ 是純量，$\lambda_{k+1}^T(Dx_k + b)\,u_k$ 對 $u_k$ 的微分是純量 $\lambda_{k+1}^T(Dx_k + b)$：
$$0 = \frac{\partial H^k}{\partial u_k} = ru_k + \lambda_{k+1}^T(Dx_k + b)$$
$$\boxed{u_k = -\frac1r\,\lambda_{k+1}^T(Dx_k + b) = -\frac1r\,(Dx_k + b)^T\lambda_{k+1}}$$

**二階確認**：$\partial^2H^k/\partial u_k^2 = r > 0$，是最小值。

$u_k$ 同時依賴狀態 $x_k$ 和共態 $\lambda_{k+1}$，而且兩者**相乘**（$\lambda_{k+1}^TDx_k$ 這一項），所以稱為 **bilinear state–costate feedback**。

### B.（10%）消去 $u_k$ 後的狀態、共態方程

**狀態方程**：
$$x_{k+1} = \frac{\partial H^k}{\partial\lambda_{k+1}} = Ax_k + (Dx_k + b)\,u_k$$

**共態方程**：對 $x_k$ 微分（$u_k$ 當常數）：
- $\partial_{x_k}\tfrac12x_k^TQx_k = Qx_k$
- $\partial_{x_k}\lambda_{k+1}^TAx_k = A^T\lambda_{k+1}$
- $\partial_{x_k}\lambda_{k+1}^TDx_k\,u_k = u_kD^T\lambda_{k+1}$

$$\lambda_k = \frac{\partial H^k}{\partial x_k} = Qx_k + A^T\lambda_{k+1} + u_kD^T\lambda_{k+1} = Qx_k + (A + u_kD)^T\lambda_{k+1}$$

**代入 A 的 $u_k$**：
$$\boxed{x_{k+1} = Ax_k - \frac1r\,(Dx_k + b)(Dx_k + b)^T\lambda_{k+1}}$$
$$\boxed{\lambda_k = Qx_k + A^T\lambda_{k+1} - \frac1r\,D^T\lambda_{k+1}\,\lambda_{k+1}^T(Dx_k + b)}$$

（第二式用了 $u_kD^T\lambda_{k+1} = -\frac1r\big[(Dx_k + b)^T\lambda_{k+1}\big]D^T\lambda_{k+1}$，而方括號裡是純量，可以移到後面寫成 $\lambda_{k+1}^T(Dx_k + b)$。）

**邊界條件**：$x_0$ 給定；$x_N$ 自由 → $\lambda_N = \dfrac{\partial}{\partial x_N}\big(\tfrac12x_N^TS_Nx_N\big) = S_Nx_N$。

**驗算**：令 $D = 0$（系統變成線性），得到
$$x_{k+1} = Ax_k - \frac1r\,bb^T\lambda_{k+1}, \qquad \lambda_k = Qx_k + A^T\lambda_{k+1}$$
正是 LQR 的狀態、共態方程（Lewis 表 2.2-1，$B = b$、$R = r$）✓

**說明**：這是一個非線性的兩點邊值問題（$x_0$ 在頭、$\lambda_N$ 在尾，而且方程裡有 $\lambda\lambda^Tx$ 這種乘積）。LQR 的猜法 $\lambda_k = S_kx_k$ 不再成立，一般只能用數值方法解。

**為什麼這題「寫完三條件就結束」，第 3B 題卻要一路解到底？** 不是離散 vs 連續的差別，是**題目要求停在哪**：
- 第 2 題問的是「最佳控制**的形式**」和「消去 $u_k$ 後的方程」→ 寫出三條件、代換完就是答案。真要解出 $u_k$ 的數值，得解這個非線性兩點邊值問題，手算不可能
- 第 3B 題問的是「$u^*(t)$ **是多少**」→ 三條件只給出形狀（$u$ 是常數），還要解狀態方程、用終點條件定出常數
- 反過來，離散題如果要數值答案也要解到底，例如 §2.1.4 的馬達（Step 4、5 解聯立）

**觀念**：一般 SOP 的三個條件、向量微分、兩點邊值、用退化情況驗算 → §2.1.2、§2.1.5

---

## 第 3 題（20%）：$\dot x = u$

題目寫 $J(t_0) = \tfrac12s\,x^2(t_0) + \tfrac12\int_{t_0}^Tru^2\,dt$。

> **關於題目**：$x(t_0)$ 是已知的初始狀態，權重放在它身上只是一個常數，不會影響最佳控制。這應該是 $x^2(T)$ 的筆誤（課本同型題都是終點權重）。以下用 $\tfrac12s\,x^2(T)$ 作答。考試時建議**寫明這個假設**，並補一句：若照字面，$\tfrac12sx^2(t_0)$ 是常數，最佳控制是 $u \equiv 0$。

### A.（10%）閉迴路控制

**先想清楚要做什麼**：「閉迴路」= 控制要寫成**現在狀態的函數** $u(t) = -K(t)\,x(t)$，不能只是一條事先算好的 $u(t)$ 曲線。系統是線性的、成本是二次的 → 這就是 LQR，而 LQR 的 $K(t)$ 由 Riccati 方程算出。所以流程是：**對應到 LQR 標準式 → 解 Riccati → 得到 $K(t)$**。

**Step 0：把題目對到 LQR 標準式**

連續 LQR 的標準式（§3.3）長這樣：
$$\dot x = A\,x + B\,u, \qquad J = \tfrac12\,x^T(T)\,S(T)\,x(T) + \tfrac12\int_{t_0}^{T}\big(x^TQx + u^TRu\big)\,dt$$

本題是純量（$x$、$u$ 都是一個數），所以轉置都可以拿掉：$x^TQx = Qx^2$、$u^TRu = Ru^2$。逐項比對：

| 標準式 | 本題 | 所以 |
|---|---|---|
| $\dot x = A\,x + B\,u$ | $\dot x = u$（沒有 $x$ 項，$u$ 前面係數是 1） | $A = 0$，$B = 1$ |
| 積分裡的 $Qx^2$ | 積分裡只有 $ru^2$，沒有 $x^2$ | $Q = 0$ |
| 積分裡的 $Ru^2$ | $ru^2$ | $R = r$ |
| 終點項 $\tfrac12S(T)\,x^2(T)$ | $\tfrac12s\,x^2(T)$ | $S(T) = s$ |

白話：$Q = 0$ 代表「過程中 $x$ 離 0 多遠不扣分」，只有終點 $x(T)$ 會被罰 $s$ 倍；過程中只在乎省力（$ru^2$）。

**Step 1：寫出 Riccati 方程，逐項代入**

連續時間 Riccati 方程（§3.3）：
$$-\dot S = A^TS + SA - SBR^{-1}B^TS + Q$$

一項一項代 $A = 0$、$B = 1$、$R = r$、$Q = 0$：
- $A^TS = 0 \cdot S = 0$
- $SA = S \cdot 0 = 0$
- $SBR^{-1}B^TS = S \cdot 1 \cdot \tfrac1r \cdot 1 \cdot S = \dfrac{S^2}{r}$
- $Q = 0$

所以
$$-\dot S = 0 + 0 - \frac{S^2}{r} + 0 \quad\Rightarrow\quad \dot S = \frac{S^2}{r}, \qquad S(T) = s$$

注意邊界條件在**終點** $T$，所以這個方程要**從 $T$ 往回解**（跟 Ch 2 的 Riccati 從 $N$ 往回算一樣）。

<details>
<summary>（不記得 Riccati 公式？從 Hamiltonian 自己推一次）</summary>

- $H = L + \lambda f = \tfrac12ru^2 + \lambda u$
- 駐點：$H_u = ru + \lambda = 0 \Rightarrow u = -\lambda/r$
- 共態：$-\dot\lambda = H_x = 0$（$H$ 裡沒有 $x$）
- 猜 $\lambda(t) = S(t)\,x(t)$（sweep），兩邊對 $t$ 微分：
  $\dot\lambda = \dot S\,x + S\,\dot x = \dot S\,x + S\,u = \dot S\,x + S\cdot\big(-\tfrac{Sx}{r}\big) = \big(\dot S - \tfrac{S^2}{r}\big)x$
- 又 $\dot\lambda = 0$，而且要對所有 $x$ 成立 → $\dot S = S^2/r$
- 終點條件 $\lambda(T) = \partial\phi/\partial x(T) = s\,x(T)$，對照 $\lambda(T) = S(T)x(T)$ → $S(T) = s$

結果跟上面一樣。
</details>

**Step 2：解 $\dot S = S^2/r$（分離變數）**

把 $S$ 都移到左邊、$t$ 都移到右邊：
$$\frac{dS}{dt} = \frac{S^2}{r} \quad\Rightarrow\quad \frac{dS}{S^2} = \frac{dt}{r}$$

兩邊從「現在 $t$」積到「終點 $T$」（因為我們知道的是 $S(T) = s$）：
$$\int_{S(t)}^{s}\frac{dS}{S^2} = \int_{t}^{T}\frac{d\tau}{r}$$

（$\tau$ 只是積分用的「啞變數」，跟 $dt$ 是同一個東西換個名字。因為 $t$ 已經拿去當積分下限了，如果寫成 $\int_t^T \frac{dt}{r}$，同一個 $t$ 同時代表「固定的下限」和「跑動的變數」，會搞混。積完之後 $\tau$ 會消失，只剩上下限 $T$ 和 $t$。左邊同理：積分變數 $S$ 從 $S(t)$ 跑到 $s$。）

左邊：$\int S^{-2}\,dS = -\dfrac1S$，所以 $\Big[-\dfrac1S\Big]_{S(t)}^{s} = -\dfrac1s + \dfrac1{S(t)}$

右邊：$\dfrac{T - t}{r}$

兩邊相等：
$$\frac{1}{S(t)} - \frac1s = \frac{T - t}{r} \quad\Rightarrow\quad \frac{1}{S(t)} = \frac1s + \frac{T - t}{r} = \frac{r + s\,(T - t)}{s\,r}$$

倒過來：
$$\boxed{S(t) = \frac{s\,r}{r + s\,(T - t)}}$$

驗算：
- $t = T$：$S = \dfrac{sr}{r} = s$ ✓（邊界條件對）
- 微分：$\dot S = \dfrac{sr \cdot s}{(r + s(T-t))^2} = \dfrac{1}{r}\cdot\dfrac{(sr)^2}{(r + s(T-t))^2} = \dfrac{S^2}{r}$ ✓（方程對）

**Step 3：從 $S(t)$ 得到增益與閉迴路控制**

LQR 的增益公式 $K(t) = R^{-1}B^TS(t)$，代 $R = r$、$B = 1$：
$$K(t) = \frac1r \cdot 1 \cdot S(t) = \frac{S(t)}{r} = \frac{s}{r + s\,(T - t)}$$
$$\boxed{u^*(t) = -K(t)\,x(t) = -\frac{s}{r + s\,(T - t)}\,x(t)}$$

這就是閉迴路：每個時刻量 $x(t)$，乘上 $-K(t)$ 就是當下的控制。

**最佳成本**：LQR 的最佳成本是 $J^* = \tfrac12\,x^T(t_0)\,S(t_0)\,x(t_0)$，純量就是把 $t = t_0$ 代進 $S(t)$：
$$J^* = \tfrac12S(t_0)\,x^2(t_0) = \frac{s\,r\,x^2(t_0)}{2\big(r + s(T - t_0)\big)}$$

**解讀**：
- 增益隨時間**變大**：離終點遠時 $K$ 小（時間多，可以慢慢推），到終點時 $K(T) = s/r$
- $s \to \infty$（要求 $x(T) = 0$）：$K(t) \to \dfrac{1}{T - t}$，$u = -\dfrac{x(t)}{T - t}$，也就是「剩下的距離 ÷ 剩下的時間」
- $s \to 0$（不在乎終點）：$K \to 0$，不出力

### B.（10%）開迴路控制，終點固定 $x(T)$

#### 先搞懂：B 跟 A 差在哪？

把 $\dot x = u$ 想成一台車：$x$ 是**位置**，$u$ 是**速度**（你直接決定速度），$\int ru^2$ 是耗能（速度的**平方**）。

A 和 B 是**同一台車、同樣的耗能**，只有「終點的規定」不一樣：

| | A | B |
|---|---|---|
| 終點規定 | **沒到 0 就罰錢** $\tfrac12s\,x^2(T)$（沒到也行，只是被罰） | **一定要準時到** $x(T)$（硬性規定） |
| $\tfrac12s\,x^2(T)$ | 終點位置由你決定 → 罰金會變 → **要留著** | 終點已經規定好 → 罰金是固定數字 → **丟掉** |
| 終點條件（三條件最後一步用的） | $\lambda(T) = s\,x(T)$ | $x(T) = $ 給定值 |
| 題目要的 | 閉迴路 $u = -K(t)\,x(t)$ | 開迴路 $u^*(t)$ |
| 用的方法 | 三條件 + **Riccati 捷徑**（有 $S$） | **只用三條件**（沒有 $S$） |

**為什麼 B 沒有 $S$？** 不管 A 還是 B，底層都是同一套「Hamiltonian 三條件」。Riccati（$S$）只是一個**捷徑**，靠的是猜 $\lambda(t) = S(t)\,x(t)$，而這個猜法要從終點開始成立：
- A 的終點條件 $\lambda(T) = s\,x(T)$ 剛好是「數字 × $x$」→ 令 $S(T) = s$，猜法起得了頭 → 有 $S$
- B 的終點條件只說「$x(T)$ 要等於給定值」，$\lambda(T)$ 是個未知數，不是「數字 × $x$」→ 猜法起不了頭 → **沒有 $S$**，直接把三條件算完就好

所以 B 不是換了新方法，而是**回到最原本的三條件**，不走捷徑。（下面最後會驗證：A 其實也能用 B 的算法算，答案一樣。）

#### 再猜答案（用數字）

題目問：**速度要怎麼安排，才能準時到達、又最省能量？**

假設 $x(t_0) = 0$、$x(T) = 10$、$T - t_0 = 2$ 秒、$r = 1$。要在 2 秒內走 10：

| 安排 | 速度 | $\int u^2\,dt$ |
|---|---|---|
| 前 1 秒衝、後 1 秒停 | 10, 0 | $10^2 \times 1 + 0 = 100$ |
| 前 1 秒 7、後 1 秒 3 | 7, 3 | $49 + 9 = 58$ |
| **全程等速** | 5, 5 | $25 + 25 = \mathbf{50}$ |

因為成本是**平方**，忽快忽慢會被重罰，**平均分配最省**。所以答案應該是「等速走完」：
$$u = \frac{\text{要走的距離}}{\text{可用的時間}} = \frac{x(T) - x(t_0)}{T - t_0}$$

下面用三條件把它**證明**出來。

#### 正式步驟

成本只剩 $J = \tfrac12\int_{t_0}^Tr\,u^2\,dt$（$s$ 那項丟掉了）。

**目標**：求 $u^*(t)$（每個時刻的速度）。

**路線圖**：三條件會先告訴我們 $u$ 的「**形狀**」，但裡面會留一個**未知常數**；最後要靠**終點條件**把常數定出來。

| Step | 用哪條 | 得到什麼 | 還缺什麼 |
|---|---|---|---|
| 2 | 駐點 $\partial H/\partial u = 0$ | $u = -\lambda/r$ | 不知道 $\lambda$ |
| 3 | 共態 $-\dot\lambda = \partial H/\partial x$ | $\lambda = \nu$（常數）→ $u$ 是常數 | 不知道 $\nu$ 是多少 |
| 4 | 狀態 $\dot x = \partial H/\partial\lambda = u$ | $x(t)$ 用 $u$ 表示 | 還沒用到終點 |
| 5 | 終點條件 $x(T) = $ 給定值 | **解出 $u$ 的值** | — |

**Step 1：寫 Hamiltonian** $H = L + \lambda f$
- $L$ = 積分裡的東西 = $\tfrac12ru^2$
- $f$ = $\dot x$ 的右邊 = $u$

$$H = \tfrac12ru^2 + \lambda u$$

**Step 2：對 $u$ 微分 = 0（駐點條件）→ 把 $u$ 用 $\lambda$ 表示**
$$\frac{\partial H}{\partial u} = ru + \lambda = 0 \;\Rightarrow\; u = -\frac{\lambda}{r}$$

**Step 3：共態方程 $-\dot\lambda = \partial H/\partial x$ → 求 $\lambda$ 長什麼樣**

$H = \tfrac12ru^2 + \lambda u$ 裡面**沒有 $x$**，所以
$$-\dot\lambda = \frac{\partial H}{\partial x} = 0 \;\Rightarrow\; \lambda \text{ 不隨時間變，是常數，叫它 } \nu$$

代回 Step 2：$u = -\nu/r$，**也是常數**。→ 已經證明了「等速」，只差這個常數是多少。

**Step 4：解狀態方程 → 位置隨時間怎麼走**

**為什麼要解這個？** 到 Step 3 為止只知道「$u$ 是某個常數」，但不知道是多少。唯一還沒用的資訊是**終點條件 $x(T) = $ 給定值**——可是它講的是**位置 $x$**，不是速度 $u$。要用它，得先知道「速度 $u$ 會讓位置走到哪」，也就是解狀態方程，把 $x(T)$ 寫成 $u$ 的式子。

（這就是三兄弟的第一條：$\dot x = \partial H/\partial\lambda = u$。前兩條決定 $u$ 的形狀，這條把 $u$ 和終點連起來。）

**怎麼解**：$\dot x = u$，$u$ 是常數，兩邊從 $t_0$ 積到 $t$：
$$x(t) - x(t_0) = \int_{t_0}^{t} u\,d\tau = u\,(t - t_0)$$
$$x(t) = x(t_0) + u\,(t - t_0)$$
白話：速度固定，位置 = 起點 + 速度 × 經過時間，一條直線。代 $t = T$ 就得到「終點會在哪」：$x(T) = x(t_0) + u\,(T - t_0)$。

**Step 5：用終點條件定出常數**（← A 和 B 唯一不同的一步）

終點固定 → 代 $t = T$，必須等於給定的 $x(T)$：
$$x(T) = x(t_0) + u\,(T - t_0) \;\Rightarrow\; \boxed{u^* = \frac{x(T) - x(t_0)}{T - t_0}}$$

跟一開始猜的一樣 ✓（如果題目要 $\lambda$：$\nu = -ru^* = -\dfrac{r\,(x(T) - x(t_0))}{T - t_0}$）

**Step 6：最小成本**（$u^*$ 是常數，積分 = 常數 × 時間長度）
$$J^* = \tfrac12\,r\,(u^*)^2\,(T - t_0) = \frac{r\,\big(x(T) - x(t_0)\big)^2}{2(T - t_0)}$$
（數字例：$\tfrac12 \cdot 1 \cdot 25 \cdot 2 = 25$，就是上表的 50 再乘 $\tfrac12$ ✓）

**最佳軌跡**：$x^*(t) = x(t_0) + \dfrac{x(T) - x(t_0)}{T - t_0}(t - t_0)$（直線）

**為什麼是「開迴路」？** 答案只跟起點、終點、時間有關，出發前就算好了，**途中不看**現在的 $x(t)$。途中被推了一下，它不會修正。

#### 一句話記流程

> 寫 $H$ → $\partial H/\partial u = 0$ 得 $u(\lambda)$ → $-\dot\lambda = \partial H/\partial x$ 解出 $\lambda$ → 代回得 $u$ → 解 $\dot x$ → **用終點條件定常數**（固定：$x(T) = $ 給定值；自由：$\lambda(T) = \partial\phi/\partial x$）

#### 驗證：A 也能用 B 的算法算

Step 1–4 完全照抄（$u = -\nu/r$，$x(T) = x(t_0) - \frac{\nu}{r}(T - t_0)$），Step 5 改用 A 的終點條件 $\nu = \lambda(T) = s\,x(T)$：

$$x(T) = x(t_0) - \frac{s\,x(T)}{r}(T - t_0) \;\Rightarrow\; x(T) = \frac{r\,x(t_0)}{r + s(T - t_0)} \;\Rightarrow\; u = -\frac{s\,x(T)}{r} = -\frac{s\,x(t_0)}{r + s(T - t_0)}$$

把「起點」換成「現在」（$t_0 \to t$、$x(t_0) \to x(t)$）：$u = -\dfrac{s}{r + s(T - t)}\,x(t)$，**就是 3A 用 Riccati 算出來的答案** ✓。所以 Riccati 真的只是捷徑。

再讓 $s \to \infty$（罰金無限大 = 一定要到 0）：$u \to -\dfrac{x(t_0)}{T - t_0}$，就是 B 取 $x(T) = 0$ 的答案。A 和 B 在這裡接起來。

#### 另一條路（套公式）

這是「終點固定、最小能量」問題，A4 上有 Gramian 公式。$A = 0$、$B = 1$、$R = r$ → $G = \int_{t_0}^T\tfrac1r\,d\tau = \tfrac{T - t_0}{r}$，$u = R^{-1}B^TG^{-1}\big(x(T) - x(t_0)\big) = \tfrac{x(T) - x(t_0)}{T - t_0}$，答案相同。

**觀念**：終點固定的一般 SOP、開迴路 vs 閉迴路 → §3.2、§3.3.6

---

## 第 4 題（15%）：最大油耗路線

**圖的邊**（只能由左往右）：$a \to b$: 3、$a \to d$: 1、$b \to c$: 2、$b \to e$: 1、$d \to e$: 3、$d \to g$: 2、$c \to f$: 3、$e \to f$: 3、$e \to h$: 2、$g \to h$: 4、$f \to i$: 4、$h \to i$: 2

**先把圖按「層」整理**（只能由左往右，所以每走一步就往右一層）：

| 從哪層 → 到哪層 | 邊（油耗） |
|---|---|
| 第 0 層 → 第 1 層 | $a \to b$: 3、$a \to d$: 1 |
| 第 1 層 → 第 2 層 | $b \to c$: 2、$b \to e$: 1、$d \to e$: 3、$d \to g$: 2 |
| 第 2 層 → 第 3 層 | $c \to f$: 3、$e \to f$: 3、$e \to h$: 2、$g \to h$: 4 |
| 第 3 層 → 終點 | $f \to i$: 4、$h \to i$: 2 |

**要算的東西**：$J^*(n)$ =「**從節點 $n$ 出發走到 $i$，最多能燒多少油**」。題目要的是 $J^*(a)$ 和那條路線。

**Principle of optimality 白話**：如果最大路線經過某個節點 $m$，那從 $m$ 到終點的那一段，本身也一定是「從 $m$ 出發的最大路線」（否則換成更大的那段，總油耗就更大，矛盾）。所以站在節點 $n$，只要比較：
$$J^*(n) = \max_{\text{下一站 } m}\big[\underbrace{w(n \to m)}_{\text{這一步的油耗}} + \underbrace{J^*(m)}_{\text{從 } m \text{ 之後最多再燒多少}}\big], \qquad J^*(i) = 0$$

**為什麼從終點逆推？** 算 $J^*(n)$ 需要「下一站」的 $J^*$。離終點越近的節點，下一站越少、越早知道答案。所以從 $i$ 開始，一層一層往左算（跟 Ch 2 的共態、Riccati 逆著時間算是同一個道理）。

**逐層計算**：

**終點**：$J^*(i) = 0$（已經到了，不用再燒油）

**第 3 層**（只差一步到 $i$，各只有一條路）：
- $f$：只能 $\to i$，$J^*(f) = 4 + J^*(i) = 4 + 0 = 4$
- $h$：只能 $\to i$，$J^*(h) = 2 + 0 = 2$

**第 2 層**（下一站都在第 3 層，$J^*(f) = 4$、$J^*(h) = 2$ 已知）：
- $c$：只能 $\to f$，$3 + J^*(f) = 3 + 4 = 7$ → $J^*(c) = 7$
- $e$：兩個選擇，比大小
  - $\to f$：$3 + J^*(f) = 3 + 4 = 7$
  - $\to h$：$2 + J^*(h) = 2 + 2 = 4$
  - 取大的 → $J^*(e) = 7$，決策：$e \to f$
- $g$：只能 $\to h$，$4 + J^*(h) = 4 + 2 = 6$ → $J^*(g) = 6$

**第 1 層**（$J^*(c) = 7$、$J^*(e) = 7$、$J^*(g) = 6$ 已知）：
- $b$：$\to c$：$2 + 7 = 9$；$\to e$：$1 + 7 = 8$ → $J^*(b) = 9$，決策 $b \to c$
- $d$：$\to e$：$3 + 7 = 10$；$\to g$：$2 + 6 = 8$ → $J^*(d) = 10$，決策 $d \to e$

**第 0 層**（$J^*(b) = 9$、$J^*(d) = 10$ 已知）：
- $a$：$\to b$：$3 + 9 = 12$；$\to d$：$1 + 10 = 11$ → $J^*(a) = \mathbf{12}$，決策 $a \to b$

（注意 $a$ 的決策：$d$ 後面的路比較大（10 > 9），但 $a \to d$ 這一步只有 1，加起來反而輸。**要看「這一步 + 之後」的總和**，不能只看其中一個。）

**整理成表**（考試可以直接畫這張）：

| 層 | 節點 | 每個選項：這一步 + $J^*$(下一站) | $J^*$（取最大） | 決策（往哪走） |
|---|---|---|---|---|
| 終點 | $i$ | — | 0 | — |
| 3 | $f$ | $\to i$：$4 + 0 = 4$ | 4 | $\to i$ |
| 3 | $h$ | $\to i$：$2 + 0 = 2$ | 2 | $\to i$ |
| 2 | $c$ | $\to f$：$3 + 4 = 7$ | 7 | $\to f$ |
| 2 | $e$ | $\to f$：$3 + 4 = 7$；$\to h$：$2 + 2 = 4$ | 7 | $\to f$ |
| 2 | $g$ | $\to h$：$4 + 2 = 6$ | 6 | $\to h$ |
| 1 | $b$ | $\to c$：$2 + 7 = 9$；$\to e$：$1 + 7 = 8$ | 9 | $\to c$ |
| 1 | $d$ | $\to e$：$3 + 7 = 10$；$\to g$：$2 + 6 = 8$ | 10 | $\to e$ |
| 0 | $a$ | $\to b$：$3 + 9 = 12$；$\to d$：$1 + 10 = 11$ | **12** | $\to b$ |

**怎麼讀這張表**：每一列回答「站在這個節點，往哪走最好、之後最多燒多少」。「選項」欄的第二個數字一定是**上面已經算好**的某一列 $J^*$。

**最後順著決策走出路線**：從 $a$ 開始查「決策」欄，一路接下去：
- $a$ 的決策 $\to b$
- $b$ 的決策 $\to c$
- $c$ 的決策 $\to f$
- $f$ 的決策 $\to i$

**答案**：最大油耗路線 $a \to b \to c \to f \to i$，油耗 $3 + 2 + 3 + 4 = 12$（$= J^*(a)$ ✓）。

（算 $J^*$ 是**逆著**走，找路線是**順著**走——跟 LQR「先逆著算 $K$、再順著跑」一樣。）

**補充**：
- 表格同時給出從**任何**節點出發的最大路線（例如從 $d$：$d \to e \to f \to i$，10），這就是 DP 的回授性質
- 貪婪法（每步挑最大的邊）從 $a$ 會走 $a \to b$（3）→ $c$（2）或 $e$（1）中挑 $c$ → $f$ → $i$，這題剛好也得 12，但一般不保證；要用 principle of optimality 才有保證
- 驗證：從 $a$ 到 $i$ 共 6 條路徑，油耗分別為 $a\text{-}b\text{-}c\text{-}f\text{-}i = 12$、$a\text{-}b\text{-}e\text{-}f\text{-}i = 11$、$a\text{-}b\text{-}e\text{-}h\text{-}i = 8$、$a\text{-}d\text{-}e\text{-}f\text{-}i = 11$、$a\text{-}d\text{-}e\text{-}h\text{-}i = 8$、$a\text{-}d\text{-}g\text{-}h\text{-}i = 9$，最大確實是 12 ✓（題目要求用 principle of optimality，答題以上表為主）

**觀念**：Bellman 最佳性原理、逆推、max 與 min 同理 → §6.1

---

## 第 5 題（35%）：是非題

### A.（5%）**False**

> 「DP 求最佳策略通常是用 stagewise forward in time 收到的因果經驗。」

**錯誤所在**：DP 是**逆著時間**（backward in time）從終點開始，用 Bellman 最佳性原理
$$J_k^*(x_k) = \min_{u_k}\big[L(x_k, u_k) + J_{k+1}^*(x_{k+1})\big], \qquad J_N^* = \phi$$
一步步往回算。它是**離線**方法，需要完整的系統模型（才能由 $x_k, u_k$ 算出 $x_{k+1}$，或知道轉移機率 $P^u_{xx'}$）。

**改正**：「DP 是逆著時間、需要完整系統動態的離線方法。用 causal experiences received stagewise forward in time 來找最佳策略的是**強化學習**（以 Bellman 方程 $V(x_k) = r_k + \gamma V(x_{k+1})$ 為基礎的 TD 方法）。」

### B.（5%）**True**

> 「PI 與 VI 用在一般確定性系統時，都能用沿系統軌跡量到的資料線上即時執行。」

**理由**：確定性系統的 Bellman 方程
$$V^h(x_k) = r(x_k, h(x_k)) + \gamma V^h(x_{k+1})$$

符號（Lewis 11.1 的記法）：
- $h$ = **策略 (policy)**：一個「看狀態決定控制」的函數，$u_k = h(x_k)$。確定性系統用 $h$；一般 MDP 的隨機策略寫成 $\pi(x, u)$（在狀態 $x$ 選動作 $u$ 的機率）。LQR 的例子：$h(x) = -Kx$
- $V^h(x_k)$ = 從 $x_k$ 開始、**一直照策略 $h$ 走**的總（折扣）成本，所以右上角標 $h$
- $r(x_k, u_k)$ = 這一步的成本（等同 Ch 2 的 $L$），$\gamma$ = 折扣因子
- 整條式子 =「這一步的成本 + 打折後的『下一個狀態開始的總成本』」，跟 Ch 6 的 Bellman 方程同形，只是 $u$ 被固定成 $h(x_k)$、沒有 $\min$

只含 $x_k$、$r_k$、$x_{k+1}$，都能沿軌跡量到，不需系統模型。用 value function approximation $V(x) = W^T\phi(x)$，
- PI 的評分步驟：$W_{j+1}^T[\phi(x_k) - \gamma\phi(x_{k+1})] = r(x_k, h_j(x_k))$
- VI 的評分步驟：$W_{j+1}^T\phi(x_k) = r(x_k, h_j(x_k)) + \gamma W_j^T\phi(x_{k+1})$

**$W$ 和 $\phi$ 是什麼？**
- **問題**：$V^h(x)$ 是一個**未知的函數**，「找一個函數」很難
- **做法**：假設它可以寫成幾個**已知函數的加權和**：
$$V(x) = W^T\phi(x) = w_1\phi_1(x) + w_2\phi_2(x) + \cdots + w_L\phi_L(x)$$
  - $\phi(x)$ = **基底函數 (basis functions)**，也叫特徵：**你自己選**的已知函數，例如 $x_1^2$、$x_1x_2$、$x_2^2$
  - $W$ = **權重**：**未知、要學的**幾個數字
- 這樣「找一個函數」就變成「找幾個數字 $W$」

**LQR 的例子**：value 一定是二次型 $V(x) = x^TPx$。$x \in \mathbb R^2$ 時展開
$$x^TPx = p_{11}x_1^2 + 2p_{12}x_1x_2 + p_{22}x_2^2$$
所以取 $\phi(x) = [x_1^2,\ x_1x_2,\ x_2^2]^T$、$W = [p_{11},\ 2p_{12},\ p_{22}]^T$，**完全精確**。學到 $W$ 就等於學到 $P$。

**為什麼這樣就不需要模型？** 代進 PI 的評分式 $W^T[\phi(x_k) - \gamma\phi(x_{k+1})] = r_k$：$\phi(x_k)$、$\phi(x_{k+1})$、$r_k$ 都是**量到的數字**，所以每一筆資料就是一條「$W$ 的線性方程」。$W$ 有 $L$ 個未知數，收集 $\ge L$ 筆資料就能解。

**scalar 數字例子**（馬達 $\omega_{k+1} = 0.9\,\omega_k + 0.1\,u_k$，但**假裝不知道** 0.9、0.1）：
- 固定策略 $h(\omega) = -0.5\,\omega$，每步成本 $r = \omega^2 + u^2$，$\gamma = 1$
- 取 $\phi(\omega) = \omega^2$，只有一個權重 $W$（就是 $P$）
- 量一筆資料：$\omega_k = 1$ → 下 $u_k = -0.5$ → 量到 $\omega_{k+1} = 0.85$、$r_k = 1 + 0.25 = 1.25$
- 代入：$W(1^2 - 0.85^2) = 1.25 \Rightarrow W = 1.25 / 0.2775 \approx 4.50$
- 驗算（知道模型的話）：閉迴路 $\omega_{k+1} = 0.85\,\omega_k$，Lyapunov $P - 0.85^2P = 1.25$ → $P \approx 4.50$ ✓。**沒用到 $A, B$ 就得到同樣的 $P$**

**PI、VI 的評分步驟是怎麼來的？**（「評分」= policy evaluation，算出目前策略的 value；$j$ 是**第幾輪疊代**，$k$ 是**時間步**，兩者不同）

兩者都是把 $V(x) = W^T\phi(x)$ 代進 Bellman 方程，差別只在**右邊的 $V$ 用新的還是舊的**：

| | PI（Policy Iteration） | VI（Value Iteration） |
|---|---|---|
| Bellman 式 | $V_{j+1}(x_k) = r_k + \gamma\,V_{\color{red}{j+1}}(x_{k+1})$ | $V_{j+1}(x_k) = r_k + \gamma\,V_{\color{red}{j}}(x_{k+1})$ |
| 意思 | 兩邊是**同一個未知** $V_{j+1}$ → 把 Bellman 方程**完整解出來** | 右邊用**上一輪的舊** $V_j$（已知）→ 只**更新一次** |
| 代入 $V = W^T\phi$ | $W_{j+1}^T\phi(x_k) = r_k + \gamma\,W_{j+1}^T\phi(x_{k+1})$ | $W_{j+1}^T\phi(x_k) = r_k + \gamma\,W_j^T\phi(x_{k+1})$ |
| 整理 | 未知的 $W_{j+1}$ 都移到左邊：$W_{j+1}^T[\phi(x_k) - \gamma\phi(x_{k+1})] = r_k$ | 右邊全是已知數字，直接就是「$W_{j+1}^T\phi(x_k) = $ 一個數」 |

（$r_k = r(x_k, h_j(x_k))$：用**這一輪的策略** $h_j$ 跑出來的這一步成本。）

**為什麼會有「新的 / 舊的」兩種寫法？** 因為 Bellman 方程 $V = r + \gamma V'$ 的未知數 $V$ **出現在等號兩邊**，而解這種方程本來就有兩種方法。用 scalar 例子最清楚，這一筆資料的 Bellman 方程是：
$$W = 1.25 + 0.7225\,W$$

- **方法一：直接解（= PI）**。把 $W$ 都移到左邊：$W(1 - 0.7225) = 1.25 \Rightarrow W = 4.50$。右邊的 $W$ 跟左邊是**同一個未知數**，所以 PI 兩邊都寫 $W_{j+1}$
- **方法二：代入再代入（= VI）**。先隨便猜一個 $W$，代進右邊算出新的 $W$，再代回去……一直重複：$0 \to 1.25 \to 2.15 \to 2.81 \to \cdots \to 4.50$。右邊用的是**上一次算出來的**，所以 VI 右邊寫 $W_j$、左邊寫 $W_{j+1}$

兩種方法解的是**同一條方程**，最後得到**同一個答案**。「新的 / 舊的」不是兩種不同的 Bellman 方程，只是「**一次解完**」和「**慢慢逼近**」兩種解法。

（方法二會收斂，是因為每次代入誤差會乘上 $0.7225 < 1$，越來越小。）

**那為什麼不都用方法一？**
- **方法一每步比較重**：真實問題的 $W$ 有很多個分量，每輪都要解一組聯立方程；方法二只要代數字
- **方法一需要「好的」策略**：如果目前的策略讓系統不穩定，總成本是無限大，直接解會解出沒有意義的答案。例：策略 $u = +3\,\omega$ → 閉迴路 $\omega_{k+1} = 1.2\,\omega_k$（發散），每步成本 $r = (1 + 9)\,\omega^2 = 10\,\omega^2$，方程 $W(1 - 1.2^2) = 10$ 解出 $W \approx -22.7$——**成本是負的**，顯然錯了。這就是「PI 的初始策略必須 admissible（讓系統穩定）」的原因；VI 是慢慢逼近，不用一開始就有好策略

**PI 和 VI 是二選一嗎？** 跑一次演算法時通常選一種，但它們其實是**同一個迴圈的兩個極端**：

$$\text{評分（算 } V\text{）} \;\to\; \text{改進策略（} h_{j+1} = \arg\min_u [r + \gamma V]\text{）} \;\to\; \text{評分} \;\to\; \cdots$$

- **改進策略**那一步，PI 和 VI **完全一樣**
- 差別只在**評分**那一步要「代入再代入」幾次：

| 評分時代入幾次 | 名稱 |
|---|---|
| 1 次就改進策略 | **VI** |
| 幾次（例如 5 次）再改進策略 | **Generalized PI (GPI)**（Lewis 11.3） |
| 代到收斂（= 直接解）再改進策略 | **PI** |

所以不是兩種互斥的方法，而是一條光譜：越往 PI，每輪越重、輪數越少；越往 VI，每輪越輕、輪數越多。選哪個看問題：模型大、方程難解 → 偏 VI；有一個穩定的初始策略、想少跑幾輪 → 偏 PI。

（Ch 2 的 Riccati 逆推 $S_k \leftarrow S_{k+1}$ 其實就是 LQR 的 VI：每步只更新一次，同時改進增益 $K$。）

**用上面的馬達資料**（$\omega_k = 1$、$\omega_{k+1} = 0.85$、$r_k = 1.25$、$\gamma = 1$，策略固定 $u = -0.5\,\omega$，只看評分這一步）：
- **PI**：$W(1 - 0.85^2) = 1.25$，**一次**就解出 $W = 4.50$
- **VI**：從 $W_0 = 0$ 開始，每輪 $W_{j+1} \cdot 1 = 1.25 + 0.7225\,W_j$：

| 輪 $j$ | 1 | 2 | 3 | 5 | 10 | 20 | $\infty$ |
|---|---|---|---|---|---|---|---|
| $W_j$ | 1.25 | 2.15 | 2.81 | 3.62 | 4.33 | 4.50 | 4.50 |

  每輪很輕鬆（不用解方程，代數字就好），但要**很多輪**才到 4.50。這正是第 5C 題說的「PI 每步工作多、步數少；VI 每步簡單、步數多」。

收集多組資料後用批次最小平方或 RLS 線上求解 $W$，再更新策略。這就是 TD 學習下的線上最佳適應控制（Lewis 11.5）。

**補充（寫出來可加分）**：
- PI 的初始策略必須是 admissible（讓系統穩定、成本有限）；VI 不需要
- regression vector 要 persistently exciting，所以要加探索雜訊
- 若策略改進用 $V$（例如 LQR 的 $K = (B^TPB + R)^{-1}B^TPA$）仍需部分模型；用 actor NN 只需 $g(x)$（即 $B$），用 Q-learning 則完全不需要
- 若用「精確計算」（直接解 Bellman 方程）來做 PI/VI，就需要模型且是離線的；本題敘述指的是 TD 實作

### C.（5%）**True**

> 「PI 每一步更新 value 時做較多工作，所以收斂所需步數較少；VI 只做一次 value 更新，最容易實作。」

**理由**：
- **PI** 每一步完整求解 Bellman 方程（有限 $N$ 個狀態時是 $N$ 條聯立線性方程；LQR 時是解一次 Lyapunov 方程）
  $$V_{j+1}(x) = \sum_u\pi_j(x, u)\sum_{x'}P^u_{xx'}[R^u_{xx'} + \gamma V_{j+1}(x')]$$
  得到目前策略的真正 value，所以收斂需要的步數少（有限 MDP 在有限步內收斂；LQR 時就是 Hewer 演算法，為 Newton 法，二次收斂）
- **VI** 每一步只做一次代入
  $$V_{j+1}(x) = \sum_u\pi_j(x, u)\sum_{x'}P^u_{xx'}[R^u_{xx'} + \gamma V_j(x')]$$
  不用解聯立方程，最容易實作；但不會得到目前策略的真正 value，一般要無限多步才收斂（LQR 時是 Lyapunov 遞迴）
- 兩者的折衷：Generalized PI，評分時做數次代入

**補充**：VI 的另一個優點是初始策略不必穩定。

**「PI 不是一步到位嗎？那『每一步』是什麼？」** PI 的「一步到位」只是**評分**那一步：對**目前這個策略**，直接解出它的 value。但目標是**最佳策略**，而目前的策略不一定最好，所以還要外面一層迴圈：

$$\underbrace{\text{評分 } h_j}_{\text{PI：一次解完}} \to \text{改進成 } h_{j+1} \to \text{評分 } h_{j+1} \to \text{改進成 } h_{j+2} \to \cdots$$

題目說的「每一步」= 外層的**第 $j$ 輪**（評分 + 改進一次）。5B 的例子把策略固定在 $u = -0.5\,\omega$，所以只示範了評分，沒有改進。

**完整跑一次**（同一個馬達 $\omega_{k+1} = 0.9\,\omega_k + 0.1\,u_k$，$r = \omega^2 + u^2$，$\gamma = 1$，$V = W\omega^2$）：
- 評分：策略 $u = -K\omega$ → 解 $W = \dfrac{1 + K^2}{1 - (0.9 - 0.1K)^2}$（就是 5B 的「方法一」）
- 改進：$\min_u[\omega^2 + u^2 + W(0.9\,\omega + 0.1\,u)^2]$，對 $u$ 微分 $= 0$ → 新的 $K = \dfrac{0.09\,W}{1 + 0.01\,W}$

| 輪 $j$ | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| **PI** 的 $K_j$ | 0.5（初始） | 0.388 | 0.3837 | 0.3837 |
| **PI** 的 $W_j$ | 4.50 | 4.454 | 4.4536 | 4.4536 |

PI **兩輪**就收斂到最佳 $K = 0.384$、$W = 4.45$（跟 Ch 2 §2.2.5 的 $K_\infty$、$S_\infty$ 一樣 ✓）。

VI 從 $W_0 = 0$ 開始、每輪只代入一次再改進：

| 輪 $j$ | 1 | 2 | 3 | 5 | 10 | 20 | 40 |
|---|---|---|---|---|---|---|---|
| **VI** 的 $W_j$ | 1.00 | 1.80 | 2.43 | 3.30 | 4.18 | 4.44 | 4.45 |
| **VI** 的 $K_j$ | 0 | 0.089 | 0.159 | 0.256 | 0.354 | 0.382 | 0.384 |

VI 要**幾十輪**。（這張表跟 Ch 2 §2.2.5 的 Riccati 逆推表**一模一樣**——Riccati 逆推就是 LQR 的 VI。）

這就是本題：**PI 每輪重（要解方程）、輪數少；VI 每輪輕（代數字）、輪數多**。

### D.（5%）**True**

> 「Q 函數方法的主要優點：最小化 Bellman 最佳性方程只需要 Q 函數，不需要系統動態。」

**理由**：用 value function 找最佳控制要
$$u^* = \arg\min_u\sum_{x'}P^u_{xx'}\big[R^u_{xx'} + \gamma V^*(x')\big]$$
必須知道轉移機率 $P^u_{xx'}$（確定性時為 $f$），才知道做 $u$ 之後會到哪個 $x'$。

定義 $Q^*(x, u) = \sum_{x'}P^u_{xx'}[R^u_{xx'} + \gamma V^*(x')]$ 之後，
$$V^*(x) = \min_uQ^*(x, u), \qquad u^* = \arg\min_uQ^*(x, u)$$
只要比較 $Q^*(x, \cdot)$ 的值，不需要 $P^u_{xx'}$ 或 $R^u_{xx'}$。而且 $Q$ 本身可以用 TD（Q-learning）沿軌跡學出來，所以整個過程不需要模型。

**LQR 例子**：$Q(x, u) = \tfrac12[x;\ u]^TG\,[x;\ u]$，$\partial Q/\partial u = 0 \Rightarrow u = -G_{uu}^{-1}G_{ux}x$，只需要 $G$ 的元素，不需要 $A, B$。

**跟 5B、5C 的 PI / VI 有什麼關係？** Q 函數補的是 PI / VI **迴圈裡的另一半**。

PI / VI 每一輪有兩步（5C）：

| 步驟 | 用 $V$ 做 | 需要模型嗎？ |
|---|---|---|
| 評分 | $V(x_k) = r_k + \gamma V(x_{k+1})$，資料就能算（5B） | **不用** |
| 改進 | $h_{j+1}(x) = \arg\min_u\big[r(x, u) + \gamma V(\underbrace{f(x, u)}_{\text{下一個狀態}})\big]$ | **要**：得知道做 $u$ 之後會到哪 |

5C 的馬達例子其實偷用了模型：改進公式 $K = \dfrac{0.09\,W}{1 + 0.01\,W}$ 裡的 0.09、0.01 就是從 $A = 0.9$、$B = 0.1$ 來的。所以**只用 $V$ 的話，評分不需要模型，改進還是需要**（5B 補充第三點也提到）。

**Q 函數的解法**：把「做 $u$ 之後會到哪」直接包進函數裡，學 $Q(x, u)$ 而不是 $V(x)$。改進就變成
$$h_{j+1}(x) = \arg\min_u Q_j(x, u)$$
只要比較 $Q$ 的值，**兩步都不需要模型**。這就是 **Q-learning = 把 PI / VI 套在 $Q$ 上**：
- 評分：$Q(x_k, u_k) = r_k + \gamma\,Q(x_{k+1}, h_j(x_{k+1}))$，一樣用資料、一樣可以 PI（直接解）或 VI（代入一次）
- 改進：$h_{j+1}(x) = \arg\min_u Q(x, u)$

**馬達例子**：$Q(\omega, u) = \omega^2 + u^2 + W(0.9\,\omega + 0.1\,u)^2$，展開成 $[\omega\ \ u]\,G\,[\omega\ \ u]^T$：
$$G = \begin{bmatrix}1 + 0.81W & 0.09W\\ 0.09W & 1 + 0.01W\end{bmatrix}, \qquad K = G_{uu}^{-1}G_{u\omega} = \frac{0.09\,W}{1 + 0.01\,W}$$
跟 5C 的改進公式**一模一樣**，但 Q-learning 是**直接從資料學出 $G$ 的三個數字**，不需要知道 0.9、0.1。最佳時（$W = 4.45$）$G_{uu} = 1.045$、$G_{u\omega} = 0.401$ → $K = 0.384$ ✓

**5B–5E 串起來**：

| 題 | 講的是 |
|---|---|
| 5B | PI / VI 的**評分**可以用資料做（不用模型） |
| 5C | PI 和 VI 的差別：評分時解完 vs 代入一次 |
| 5D | 用 $Q$ 取代 $V$，讓**改進**也不用模型 |
| 5E | 評分「用資料做」的具體方法：TD，沿單一軌跡把 TD 誤差修小 |

### E.（5%）**True**

> 「與 Monte Carlo 不同，TD RL 只用一條樣本軌跡（目前的系統軌跡）更新 value，並使 TD 誤差變小。」

**理由**：
- **Monte Carlo**：根據 value 的定義 $V^\pi(x) = E_\pi\{\sum\gamma^ir_{k+i} \mid x_k = x\}$，從某狀態出發跑完一整個 episode、記錄總成本，**重複多個 episode** 取平均來估計期望值；每個 episode 結束後才更新（需要 exploring starts 讓每個狀態都被造訪）
- **TD**：把 Bellman 方程中的期望值換成沿**單一**樣本路徑（目前軌跡）的確定性版本
  $$V^\pi(x_k) = r_k + \gamma V^\pi(x_{k+1})$$
  每一步得到資料 $(x_k, r_k, x_{k+1})$ 就更新估計，使 TD 誤差
  $$e_k = -\hat V(x_k) + r_k + \gamma\hat V(x_{k+1})$$
  變小。因為 Bellman 方程是一致性方程，估計正確時 $e_k = 0$，所以反覆把 $e_k$ 修小，平均而言會收斂到隨機 Bellman 方程的解

**5E 跟 PI / VI 是什麼關係？** 不是「偏向 PI 或 VI」，而是**另一個獨立的選擇**。做評分時其實要決定兩件事：

| 要決定的事 | 選項 | 哪一題 |
|---|---|---|
| ① 評分**用什麼資料、什麼方程** | **Monte Carlo**：跑完整段、加總成本（用 value 的定義）<br>**TD**：只用一步 $(x_k, r_k, x_{k+1})$ + Bellman 方程 | 5E |
| ② 評分**做到多完整** | **PI**：解到底<br>**VI**：代入一次 | 5C |

兩個選擇可以自由搭配。5B 那兩條式子其實都是 **TD**：
- PI 版：讓 TD 誤差 $e_k = -W_{j+1}^T\phi(x_k) + r_k + \gamma W_{j+1}^T\phi(x_{k+1}) = 0$（兩邊都用新的 $W$）
- VI 版：讓 $e_k = -W_{j+1}^T\phi(x_k) + r_k + \gamma W_j^T\phi(x_{k+1}) = 0$（右邊用舊的 $W$）

**馬達例子對比**（策略 $u = -0.5\,\omega$，從 $\omega = 1$ 出發，閉迴路 $\omega_{k+1} = 0.85\,\omega_k$，每步成本 $1.25\,\omega_k^2$）：
- **Monte Carlo**：一直跑下去，把成本加起來
  $$1.25\,(1 + 0.85^2 + 0.85^4 + \cdots) = \frac{1.25}{1 - 0.7225} = 4.50$$
  要跑**很長一段**（理論上無限長）才加得完，跑完才更新
- **TD**：只用第一步的資料 $(\omega_k = 1,\ r_k = 1.25,\ \omega_{k+1} = 0.85)$，套 Bellman 方程 $W = 1.25 + 0.7225\,W$ → $W = 4.50$
  **一步就夠**，邊跑邊更新

兩者得到同一個答案；TD 靠 Bellman 方程「借用」下一個狀態的估計值，所以不用等整段跑完。

**TD 是 PI / VI 專用，還是 Q-learning 也用？兩邊都用。** Q-learning 不是跟 PI / VI 對立的另一派，而是「**PI / VI 套在 $Q$ 上**」（5D）。所以整個 RL 其實是三個獨立的選擇疊起來：

| 選擇 | 選項 | 題目 |
|---|---|---|
| 學哪個函數 | $V(x)$ 或 $Q(x, u)$ | 5D |
| 評分用什麼資料 | Monte Carlo 或 **TD** | 5E |
| 評分做多完整 | PI 或 VI | 5C |

**Q-learning = 學 $Q$ + 用 TD + （通常是）VI**。它的 TD 誤差長得跟 $V$ 版一樣，只是把 $V$ 換成 $Q$：

| | TD 誤差 $e_k$ |
|---|---|
| $V$ 版（5B、5E） | $-V(x_k) + r_k + \gamma\,V(x_{k+1})$ |
| $Q$ 版（Q-learning） | $-Q(x_k, u_k) + r_k + \gamma\,\min_u Q(x_{k+1}, u)$ |

（$Q$ 版裡的 $\min_u$ 就是「順便改進策略」，所以 Q-learning 是 VI 風格：每步代入一次、同時改進。Lewis 11.3 的式 (11.3-43)–(11.3-47) 給了用 Q 函數的 PI 和 VI 兩種版本，11.5 再把它做成線上 Q-learning。）

### F.（10%）**證明**：DT LQR 的 Bellman 方程是 Lyapunov 方程，最佳性方程是 DARE

**設定**：$x_{k+1} = Ax_k + Bu_k$，
$$V^h(x_k) = \tfrac12\sum_{i=k}^\infty(x_i^TQx_i + u_i^TRu_i), \qquad r(x_k, u_k) = \tfrac12(x_k^TQx_k + u_k^TRu_k)$$
$Q \ge 0$、$R > 0$，$\gamma = 1$。課本中：
- (11.5-7) Bellman 方程：$V^h(x_k) = r(x_k, u_k) + V^h(x_{k+1})$
- (11.5-5) Bellman 最佳性方程（DT HJB）：$V^*(x_k) = \min_{u_k}\big[r(x_k, u_k) + V^*(x_{k+1})\big]$

LQR 的 value 是狀態的二次式，令 $V(x) = \tfrac12x^TPx$，$P = P^T$。

**(1) Bellman 方程 → Lyapunov 方程**

取穩定的線性回授策略 $u_k = h(x_k) = -Kx_k$，則 $x_{k+1} = (A - BK)x_k$。代入 (11.5-7)、兩邊乘 2：
$$x_k^TPx_k = x_k^TQx_k + x_k^TK^TRKx_k + x_k^T(A - BK)^TP(A - BK)x_k$$
即
$$x_k^T\big[(A - BK)^TP(A - BK) - P + Q + K^TRK\big]x_k = 0$$
此式對所有狀態軌跡、所有 $x_k$ 都成立，且括號內矩陣對稱，所以
$$\boxed{(A - BK)^TP\,(A - BK) - P + Q + K^TRK = 0}$$
這是閉迴路矩陣 $A - BK$ 的**離散 Lyapunov 方程**（形式 $\bar A^TP\bar A - P = -\bar Q$，$\bar A = A - BK$、$\bar Q = Q + K^TRK$），而且**對 $P$ 是線性的**。因此 Bellman 方程就是線性 Lyapunov 方程。$\blacksquare$

（$K$ 穩定 → $\lvert\lambda(A - BK)\rvert < 1$ → 此 Lyapunov 方程有唯一解 $P$，即策略 $K$ 的成本。）

**(2) Bellman 最佳性方程 → DARE**

$V^*(x) = \tfrac12x^TPx$ 代入 (11.5-5)、兩邊乘 2：
$$x_k^TPx_k = \min_{u_k}\Big[x_k^TQx_k + u_k^TRu_k + (Ax_k + Bu_k)^TP(Ax_k + Bu_k)\Big]$$

右邊對 $u_k$ 微分令為零（駐點條件，即 DT Hamiltonian $\partial H/\partial u_k = 0$）：
$$2Ru_k + 2B^TP(Ax_k + Bu_k) = 0 \;\Rightarrow\; u_k^* = -(B^TPB + R)^{-1}B^TPA\,x_k = -Kx_k$$
二階導數 $2(B^TPB + R) > 0$，確為最小。

代回右邊。記 $M = B^TPB + R$、$N = B^TPA$，則 $u_k^* = -M^{-1}Nx_k$，右邊與 $u$ 有關的部分為
$$u_k^{*T}Mu_k^* + 2u_k^{*T}Nx_k = x_k^TN^TM^{-1}Nx_k - 2x_k^TN^TM^{-1}Nx_k = -x_k^TN^TM^{-1}Nx_k$$
所以
$$x_k^TPx_k = x_k^T\big[Q + A^TPA - A^TPB(B^TPB + R)^{-1}B^TPA\big]x_k \qquad \forall x_k$$
得
$$\boxed{A^TPA - P + Q - A^TPB\,(B^TPB + R)^{-1}B^TPA = 0}$$
這就是**離散代數 Riccati 方程 (DARE)**，對 $P$ 是非線性的。$\blacksquare$

**補充（另一種寫法）**：把 (2) 的 $u^* = -Kx$ 代回 (1)，得 $(A - BK)^TP(A - BK) - P + Q + K^TRK = 0$，再代入 $K = (B^TPB + R)^{-1}B^TPA$ 展開，也會得到 DARE。這也說明：DARE 就是「增益 $K$ 恰為對 $P$ 的 greedy 改進」時的 Lyapunov 方程，PI（Hewer 演算法）反覆解 Lyapunov、更新 $K$，收斂到 DARE 的解。

**觀念**：DP vs RL、PI/VI、Q 函數、TD vs Monte Carlo、LQR 的 Bellman 方程 → §11

---

## 配分與重點回顧

| 題 | 配分 | 核心觀念 |
|---|---|---|
| 1 | 15% | Lagrange、相切 ⇔ 梯度平行、二階確認 |
| 2 | 15% | 一般 SOP 三個條件、向量微分、消去 $u$ |
| 3 | 20% | scalar Riccati 分離變數（閉迴路）、終點固定一般 SOP（開迴路） |
| 4 | 15% | Bellman 最佳性原理逆推（max） |
| 5 | 35% | DP vs RL、PI vs VI、Q 函數、TD vs MC、LQR 的 Bellman 方程 |
