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

**觀念**：一般 SOP 的三個條件、向量微分、兩點邊值、用退化情況驗算 → §2.1.2、§2.1.5

---

## 第 3 題（20%）：$\dot x = u$

題目寫 $J(t_0) = \tfrac12s\,x^2(t_0) + \tfrac12\int_{t_0}^Tru^2\,dt$。

> **關於題目**：$x(t_0)$ 是已知的初始狀態，權重放在它身上只是一個常數，不會影響最佳控制。這應該是 $x^2(T)$ 的筆誤（課本同型題都是終點權重）。以下用 $\tfrac12s\,x^2(T)$ 作答。考試時建議**寫明這個假設**，並補一句：若照字面，$\tfrac12sx^2(t_0)$ 是常數，最佳控制是 $u \equiv 0$。

### A.（10%）閉迴路控制

**對應 LQR**：$\dot x = u$、$J = \tfrac12s\,x^2(T) + \tfrac12\int ru^2\,dt$ → $A = 0$、$B = 1$、$Q = 0$、$R = r$、$S(T) = s$。

**Step 1：Riccati 方程**
$$-\dot S = A^TS + SA - SBR^{-1}B^TS + Q = -\frac{S^2}{r} \;\Rightarrow\; \dot S = \frac{S^2}{r}, \qquad S(T) = s$$

（也可以從頭推：$H = \tfrac12ru^2 + \lambda u$，$H_u = 0 \Rightarrow u = -\lambda/r$；$-\dot\lambda = H_x = 0$。猜 $\lambda = Sx$：$\dot\lambda = \dot Sx + S\dot x = \dot Sx - \frac{S^2}{r}x = 0$ 對所有 $x$ 成立 → $\dot S = S^2/r$。邊界 $\lambda(T) = sx(T)$ → $S(T) = s$。）

**Step 2：分離變數**
$$\frac{dS}{S^2} = \frac{dt}{r} \;\Rightarrow\; \int_{S(t)}^{s}\frac{dS}{S^2} = \int_t^T\frac{d\tau}{r} \;\Rightarrow\; \frac{1}{S(t)} - \frac1s = \frac{T - t}{r}$$
$$\boxed{S(t) = \frac{s\,r}{r + s\,(T - t)}}$$
驗算：$t = T$ 時 $S = s$ ✓；代回 $\dot S = \dfrac{s^2r}{(r + s(T-t))^2} = \dfrac{S^2}{r}$ ✓

**Step 3：增益與閉迴路控制**
$$K(t) = R^{-1}B^TS(t) = \frac{S(t)}{r} = \frac{s}{r + s\,(T - t)}$$
$$\boxed{u^*(t) = -K(t)\,x(t) = -\frac{s}{r + s\,(T - t)}\,x(t)}$$

**最佳成本**：$J^* = \tfrac12S(t_0)\,x^2(t_0) = \dfrac{s\,r\,x^2(t_0)}{2\big(r + s(T - t_0)\big)}$

**解讀**：
- 增益隨時間**變大**：離終點遠時 $K$ 小（時間多，可以慢慢推），到終點時 $K(T) = s/r$
- $s \to \infty$（要求 $x(T) = 0$）：$K(t) \to \dfrac{1}{T - t}$，$u = -\dfrac{x(t)}{T - t}$，也就是「剩下的距離 ÷ 剩下的時間」
- $s \to 0$（不在乎終點）：$K \to 0$，不出力

### B.（10%）開迴路控制，終點固定 $x(T)$

終點固定時終點權重不影響答案（$x(T)$ 已經給定），所以只剩 $J = \tfrac12\int_{t_0}^Tru^2\,dt$。

**Step 1：Hamiltonian**：$H = \tfrac12ru^2 + \lambda u$

**Step 2：三個條件**
- 狀態：$\dot x = u$
- 共態：$-\dot\lambda = \dfrac{\partial H}{\partial x} = 0 \;\Rightarrow\; \lambda(t) = \nu$（常數）
- 駐點：$0 = \dfrac{\partial H}{\partial u} = ru + \lambda \;\Rightarrow\; u = -\dfrac{\nu}{r}$（也是常數）

**Step 3：解狀態方程**
$$x(t) = x(t_0) - \frac{\nu}{r}(t - t_0)$$

**Step 4：邊界條件**：$x(T)$ 固定（$\lambda(T) = \nu$ 是未知數）
$$x(T) = x(t_0) - \frac{\nu}{r}(T - t_0) \;\Rightarrow\; \nu = -\frac{r\,\big(x(T) - x(t_0)\big)}{T - t_0}$$

**答案**：
$$\boxed{u^*(t) = \frac{x(T) - x(t_0)}{T - t_0}}, \qquad x^*(t) = x(t_0) + \frac{x(T) - x(t_0)}{T - t_0}(t - t_0)$$
最小成本 $J^* = \dfrac{r\,\big(x(T) - x(t_0)\big)^2}{2(T - t_0)}$。

**解讀**：控制是常數 → 狀態**等速**從 $x(t_0)$ 走到 $x(T)$。因為系統沒有摩擦（沒有 $x$ 項），早出力晚出力效果一樣，而 $\int u^2$ 在總位移固定時，均勻分配最省（Cauchy–Schwarz）。

**跟 A 的關係**：取 $x(T) = 0$，B 的答案在任意時刻 $t$ 重新計算就是 $u = -x(t)/(T - t)$，正是 A 在 $s \to \infty$ 時的閉迴路控制。沒有擾動時兩者走出同一條軌跡；有擾動時只有閉迴路會修正。

**觀念**：連續 LQR、scalar Riccati 分離變數、終點固定的一般 SOP、開迴路 vs 閉迴路 → §3.2、§3.3.6

---

## 第 4 題（15%）：最大油耗路線

**圖的邊**（只能由左往右）：$a \to b$: 3、$a \to d$: 1、$b \to c$: 2、$b \to e$: 1、$d \to e$: 3、$d \to g$: 2、$c \to f$: 3、$e \to f$: 3、$e \to h$: 2、$g \to h$: 4、$f \to i$: 4、$h \to i$: 2

**Principle of optimality**：令 $J^*(n)$ = 從節點 $n$ 到 $i$ 的**最大**油耗。最大路線的任何後半段也必須是最大的，所以
$$J^*(n) = \max_{m}\big[\,w(n \to m) + J^*(m)\,\big], \qquad J^*(i) = 0$$
從終點逆推：

| 階段 | 節點 | 選項：$w + J^*(\text{下一站})$ | $J^*$ | 決策 |
|---|---|---|---|---|
| 終點 | $i$ | — | 0 | — |
| 1 | $f$ | $\to i$：$4 + 0 = 4$ | 4 | $\to i$ |
| 1 | $h$ | $\to i$：$2 + 0 = 2$ | 2 | $\to i$ |
| 2 | $c$ | $\to f$：$3 + 4 = 7$ | 7 | $\to f$ |
| 2 | $e$ | $\to f$：$3 + 4 = 7$；$\to h$：$2 + 2 = 4$ | 7 | $\to f$ |
| 2 | $g$ | $\to h$：$4 + 2 = 6$ | 6 | $\to h$ |
| 3 | $b$ | $\to c$：$2 + 7 = 9$；$\to e$：$1 + 7 = 8$ | 9 | $\to c$ |
| 3 | $d$ | $\to e$：$3 + 7 = 10$；$\to g$：$2 + 6 = 8$ | 10 | $\to e$ |
| 4 | $a$ | $\to b$：$3 + 9 = 12$；$\to d$：$1 + 10 = 11$ | **12** | $\to b$ |

**順著決策走**：$a \to b \to c \to f \to i$

**答案**：最大油耗路線 $a \to b \to c \to f \to i$，油耗 $3 + 2 + 3 + 4 = 12$。

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
只含 $x_k$、$r_k$、$x_{k+1}$，都能沿軌跡量到，不需系統模型。用 value function approximation $V(x) = W^T\phi(x)$，
- PI 的評分步驟：$W_{j+1}^T[\phi(x_k) - \gamma\phi(x_{k+1})] = r(x_k, h_j(x_k))$
- VI 的評分步驟：$W_{j+1}^T\phi(x_k) = r(x_k, h_j(x_k)) + \gamma W_j^T\phi(x_{k+1})$

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

### D.（5%）**True**

> 「Q 函數方法的主要優點：最小化 Bellman 最佳性方程只需要 Q 函數，不需要系統動態。」

**理由**：用 value function 找最佳控制要
$$u^* = \arg\min_u\sum_{x'}P^u_{xx'}\big[R^u_{xx'} + \gamma V^*(x')\big]$$
必須知道轉移機率 $P^u_{xx'}$（確定性時為 $f$），才知道做 $u$ 之後會到哪個 $x'$。

定義 $Q^*(x, u) = \sum_{x'}P^u_{xx'}[R^u_{xx'} + \gamma V^*(x')]$ 之後，
$$V^*(x) = \min_uQ^*(x, u), \qquad u^* = \arg\min_uQ^*(x, u)$$
只要比較 $Q^*(x, \cdot)$ 的值，不需要 $P^u_{xx'}$ 或 $R^u_{xx'}$。而且 $Q$ 本身可以用 TD（Q-learning）沿軌跡學出來，所以整個過程不需要模型。

**LQR 例子**：$Q(x, u) = \tfrac12[x;\ u]^TG\,[x;\ u]$，$\partial Q/\partial u = 0 \Rightarrow u = -G_{uu}^{-1}G_{ux}x$，只需要 $G$ 的元素，不需要 $A, B$。

### E.（5%）**True**

> 「與 Monte Carlo 不同，TD RL 只用一條樣本軌跡（目前的系統軌跡）更新 value，並使 TD 誤差變小。」

**理由**：
- **Monte Carlo**：根據 value 的定義 $V^\pi(x) = E_\pi\{\sum\gamma^ir_{k+i} \mid x_k = x\}$，從某狀態出發跑完一整個 episode、記錄總成本，**重複多個 episode** 取平均來估計期望值；每個 episode 結束後才更新（需要 exploring starts 讓每個狀態都被造訪）
- **TD**：把 Bellman 方程中的期望值換成沿**單一**樣本路徑（目前軌跡）的確定性版本
  $$V^\pi(x_k) = r_k + \gamma V^\pi(x_{k+1})$$
  每一步得到資料 $(x_k, r_k, x_{k+1})$ 就更新估計，使 TD 誤差
  $$e_k = -\hat V(x_k) + r_k + \gamma\hat V(x_{k+1})$$
  變小。因為 Bellman 方程是一致性方程，估計正確時 $e_k = 0$，所以反覆把 $e_k$ 修小，平均而言會收斂到隨機 Bellman 方程的解

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
