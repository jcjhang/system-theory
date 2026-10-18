# 系統理論 A4 公式紙（雙面）

> 範圍：Lewis Ch 1、2、3、6、11；Żak Ch 3、4、5。以整個範圍為準，不針對特定考古題。
> 列印：8–9pt、兩欄、窄邊界。**正面** = 工具、Lewis Ch 1–3、Żak Ch 3–4；**背面** = Żak Ch 5、Lewis Ch 6、11、是非題。

---

# 正面

## 0. 符號表（先對照題目，認出每個字母是誰，再套公式）

**系統與時間**

| 符號 | 意思 | 例（馬達） |
|---|---|---|
| $x$（$x_k$, $x(t)$） | **狀態**：系統現在的樣子，$n$ 維 | 轉速 $\omega$ |
| $u$ | **控制**：你能選的輸入，$m$ 維 | 電壓 |
| $y$ | **輸出**：量得到的東西 $y = Cx + Du$ | 感測器讀數 |
| $k$, $N$ / $t$, $t_0$, $T$ | 離散第 $k$ 步、終點 $N$ / 連續時間、起點、終點 | |
| $\tau$, $\sigma$ | 積分用的啞變數（積完消失） | |
| $f$（$f^k$） | 系統方程右邊：$x_{k+1} = f$ 或 $\dot x = f$ | $-\omega + u$ |
| $A$ ($n\times n$) | $x$ 自己怎麼變（$\dot x$ 或 $x_{k+1}$ 裡 $x$ 的係數） | $-1$ |
| $B$ ($n\times m$) | $u$ 怎麼推動 $x$（$u$ 的係數） | $1$ |
| $C$, $D$ | 輸出 $y = Cx + Du$ 的係數 | |

**成本**（$J$ = 要最小化的總分）

| 符號 | 意思 | 在 LQR 裡 |
|---|---|---|
| $L$（$L^k$） | 每一刻 / 每一步的成本（積分或求和**裡面**的東西） | $\tfrac12(x^TQx + u^TRu)$ |
| $\phi$ | **終點**成本（積分**外面**、只看 $x(T)$ 或 $x_N$） | $\tfrac12x^TS(T)x$ |
| $Q$ ($n\times n$, $\ge 0$) | 狀態偏離 0 的罰分權重；積分裡沒有 $x^2$ → $Q = 0$ | 純量 $q$ |
| $R$ ($m\times m$, $> 0$) | 用力（控制）的罰分權重 | 純量 $r$ |
| $S_N$ / $S(T)$ | 終點罰分權重（題目給的） | 純量 $s$ |
| $\psi = 0$, $r_N$ / $r$ | 終點**約束**（硬性規定），$x(T) = r$ 表示終點固定的目標值 | |
| $J^*$ | 最佳（最小）成本 | $\tfrac12x_0^TS_0x_0$ |

**最佳化用的輔助量**

| 符號 | 意思 |
|---|---|
| $\lambda$（$\lambda_k$, $\lambda(t)$） | **共態** / Lagrange 乘數：約束的「價格」，$\lambda = \partial J^*/\partial x$。Żak 寫成 $p$ |
| $H$ | **Hamiltonian** $= L + \lambda^Tf$（離散配 $\lambda_{k+1}$）。Żak：$H = F + p^Tf$ |
| $\nu$ | 終點約束 $\psi = 0$ 的乘數（終點固定時 $\lambda(T)$ 的未知常數） |
| $H_x, L_u, f_x, \phi_x$ | 下標 = 偏微分：$H_x = \partial H/\partial x$，$f_x$ = Jacobian |
| $S_k$ / $S(t)$ | Riccati 解（隨時間變）；$\lambda = Sx$；$J^* = \tfrac12x^TSx$ |
| $P$ | Riccati 穩態解（ARE / DARE）；或 Lyapunov 方程的解；或 RL 的 $V = \tfrac12x^TPx$ |
| $K$ | 回授增益：$u = -Kx$ |
| $G$ | 終點固定最小能量的**可達 Gramian**（C、D 節）；RL 的 **Q 函數矩陣**（I 節）— 兩個不同東西 |
| $W$, $V$ | Żak 的可控 / 可觀察 Gramian（E 節）；$W$ 在 I 節是 VFA 權重、$V$ 是 value function |
| $F$, $\Phi$, $U$ | Żak：積分裡的東西（= Lewis 的 $L$）、終點成本（= $\phi$）、$u$ 允許的範圍 |
| $a, b, q, r, s$ | 純量版的 $A, B, Q, R, S(T)$ |

**RL（Ch 11）**

| 符號 | 意思 |
|---|---|
| $r_k$ | 第 $k$ 步的**獎勵 / 成本**（≠ 上面的 $r$ 權重） |
| $\gamma$ | 折扣因子 $0 \le \gamma < 1$ |
| $\pi(x, u)$ / $h(x)$ | 策略（機率型 / 確定型） |
| $V^\pi(x)$, $V^*$ | 照策略走下去的總成本 / 最佳總成本（= Ch 6 的 $J^*$） |
| $Q^\pi(x, u)$ | 這步先做 $u$、之後照 $\pi$ 的總成本（≠ 權重矩陣 $Q$） |
| $P^u_{xx'}$, $R^u_{xx'}$ | 在 $x$ 做 $u$ 跑到 $x'$ 的機率、那一步的成本；閉迴路 Markov chain 的 $P$ = 轉移矩陣（≠ Riccati 的 $P$） |
| $e_k$, $\alpha$, $\phi(x)$ | TD 誤差、學習率、VFA 基底函數（≠ 終點成本 $\phi$） |
| $j$ | 疊代次數（不是時間） |

## A. 工具

- **微分**（$R, S$ 對稱）：$\partial_u\tfrac12u^TRu = Ru$；$\partial_u b^Tu = b$；$\partial_x\lambda^TMx = M^T\lambda$；$\partial_u x^TMu = M^Tx$；$\partial_u\tfrac12(Ax+Bu)^TS(Ax+Bu) = B^TS(Ax+Bu)$。乘積項：對誰微分，其他當常數
- **比較係數**：$x^TMx = 0\ \forall x \Rightarrow M + M^T = 0$；$x^TSAx = \tfrac12x^T(A^TS + SA)x$
- **2×2**：$\lambda^2 - \text{tr}\,\lambda + \det = 0$；$\begin{bmatrix}a&b\\c&d\end{bmatrix}^{-1} = \frac{1}{ad-bc}\begin{bmatrix}d&-b\\-c&a\end{bmatrix}$；對稱 $P > 0 \Leftrightarrow p_{11} > 0,\ \det P > 0$（一般：特徵值全正 / 主子式全正）
- **極值**：梯度 0 + Hessian 正定；$\tfrac12u^TRu + b^Tu$ 最小點 $-R^{-1}b$；$\lambda_{\min}(Q)\lVert x\rVert^2 \le x^TQx \le \lambda_{\max}(Q)\lVert x\rVert^2$
- **解**：$x(t) = e^{A(t-t_0)}x_0 + \int_{t_0}^te^{A(t-\tau)}Bu\,d\tau$；$e^{At} = \mathcal L^{-1}[(sI - A)^{-1}]$；三角矩陣特徵值 = 對角線；離散 $x_k = A^kx_0 + \sum_{i=0}^{k-1}A^{k-1-i}Bu_i$
- **穩定**：連續 $\text{Re}\,\lambda < 0$；離散 $\lvert\lambda\rvert < 1$
- **積分**：$\int\frac{ds}{s^2} = -\frac1s$；$\int\frac{ds}{(s-s_1)(s-s_2)} = \frac{1}{s_1-s_2}\ln\left\lvert\frac{s-s_1}{s-s_2}\right\rvert$；$\int\frac{ds}{a^2 - s^2} = \frac1a\tanh^{-1}\frac sa$；$\sinh, \cosh = \frac{e^t \mp e^{-t}}{2}$
- **離散化**：Euler $x_{k+1} = (I + A\tau)x_k + B\tau u_k$，成本 $\times\tau$；ZOH $A^s = e^{A\tau}$，$B^s = \int_0^\tau e^{At}B\,dt$

## B. Lewis Ch 1：靜態最佳化

📐 **標準式**：$\min_{u}L(x, u)$ s.t. $f(x, u) = 0$；$u \in \mathbb R^m$ 自由選、$x \in \mathbb R^n$ 由約束決定、$f \in \mathbb R^n$（約束條數 = $x$ 維度）。無約束：$\min_uL(u)$

- 無約束：$L_u = 0$，$L_{uu} > 0$
- 約束 $f(x, u) = 0$：$H = L + \lambda^Tf$，$H_\lambda = 0$、$H_x = 0$、$H_u = 0$（$\lambda^T = -L_xf_x^{-1}$）
- 幾何：最佳點 $\nabla L \parallel \nabla f$（等高線與約束相切）
- 敏感度：$dL^* = -\lambda^Tdf$（約束右邊改 $df$，最小成本改 $-\lambda^Tdf$）
- 二階：沿約束方向的 Hessian $> 0$（或把約束代入後看二階導數）

## C. Lewis Ch 2：離散時間

📐 **標準式**：$x_{k+1} = f^k(x_k, u_k)$，$J = \phi(N, x_N) + \sum_{k=0}^{N-1}L^k(x_k, u_k)$（$\phi$ = 終點成本，$L^k$ = 每步成本）
$H^k = L^k + \lambda_{k+1}^Tf^k$：狀態 $x_{k+1} = f^k$；共態 $\lambda_k = f_x^T\lambda_{k+1} + L_x$（逆時間）；駐點 $0 = f_u^T\lambda_{k+1} + L_u$
邊界：$x_0$ 給定；$x_N$ 自由 $\lambda_N = \phi_{x_N}$；$x_N$ 固定 $= r_N$（$\lambda_N$ 待解）

**LQR（終點自由）** 📐 $x_{k+1} = Ax_k + Bu_k$，$J = \tfrac12x_N^TS_Nx_N + \tfrac12\sum_{k=0}^{N-1}(x_k^TQx_k + u_k^TRu_k)$；$Q \ge 0$、$R > 0$、$S_N \ge 0$ 對稱。對照題目逐項讀出 $A, B, Q, R, S_N$（純量：$x^TQx = qx^2$；積分 / 求和裡沒有 $x^2$ 項 → $Q = 0$）
- $\lambda_k = Qx_k + A^T\lambda_{k+1}$，$u_k = -R^{-1}B^T\lambda_{k+1}$；猜 $\lambda_k = S_kx_k$
- $K_k = (B^TS_{k+1}B + R)^{-1}B^TS_{k+1}A$，$u_k = -K_kx_k$，$J^* = \tfrac12x_0^TS_0x_0$
- $S_k = A^TS_{k+1}(A - BK_k) + Q = (A - BK_k)^TS_{k+1}(A - BK_k) + K_k^TRK_k + Q$
- 穩態 DARE（📐 無限時間 $J = \tfrac12\sum_{k=0}^{\infty}(x^TQx + u^TRu)$，無終點項）：$P = A^TPA - A^TPB(B^TPB + R)^{-1}B^TPA + Q$；$(A, B)$ stabilizable、$(A, \sqrt Q)$ detectable → 唯一正定解、$\lvert\lambda(A - BK)\rvert < 1$
- 固定 $K$ 的成本（📐 $u_k = -Kx_k$ 給定，$J = \tfrac12\sum_0^\infty(\cdot) = \tfrac12x_0^TPx_0$）：$P = (A - BK)^TP(A - BK) + Q + K^TRK$

**終點固定、最小能量** 📐 $x_{k+1} = Ax_k + Bu_k$，$J = \tfrac12\sum_{k=0}^{N-1}u_k^TRu_k$（$Q = 0$），$x_0$ 給定、$x_N = r_N$ → 開迴路
- $G = \sum_{k=0}^{N-1}A^{N-1-k}BR^{-1}B^T(A^T)^{N-1-k}$（可達 Gramian，需非奇異）
- $u_k = R^{-1}B^T(A^T)^{N-1-k}G^{-1}(r_N - A^Nx_0)$，$J^* = \tfrac12(r_N - A^Nx_0)^TG^{-1}(r_N - A^Nx_0)$

## D. Lewis Ch 3：連續時間

📐 **標準式**：$\dot x = f(x, u, t)$，$J = \phi\big(x(T), T\big) + \int_{t_0}^TL(x, u, t)\,dt$，（可有）終點約束 $\psi\big(x(T), T\big) = 0$
$H = L + \lambda^Tf$：$\dot x = f$；$-\dot\lambda = H_x = f_x^T\lambda + L_x$ ⚠️；$0 = H_u$
邊界通式：$(\phi_x + \psi_x^T\nu - \lambda)^T\rvert_T\,dx(T) + (\phi_t + \psi_t^T\nu + H)\rvert_T\,dT = 0$

| $T$ | $x(T)$ | 條件 |
|---|---|---|
| 固定 | 自由 | $\lambda(T) = \phi_x$ |
| 固定 | 固定 | $x(T) = r$ |
| 固定 | $\psi = 0$ | $\lambda(T) = \phi_x + \psi_x^T\nu$ |
| 自由 | 自由 / $\psi$ | 上列 + $(\phi_t + \psi_t^T\nu + H)\rvert_T = 0$ |

- $f, L$ 不含 $t$ → $H$ 沿最佳軌跡為常數；$T$ 自由時 $H \equiv 0$
- 順序：$u(\lambda)$ → 解共態 → 解狀態 → 邊界定常數

**LQR** 📐 $\dot x = Ax + Bu$，$J = \tfrac12x^T(T)S(T)x(T) + \tfrac12\int_{t_0}^T(x^TQx + u^TRu)\,dt$
- $K = R^{-1}B^TS$，$u = -Kx$，$J^* = \tfrac12x_0^TS(t_0)x_0$，$-\dot S = A^TS + SA - SBR^{-1}B^TS + Q$，$S(T)$ 給定
- Scalar 📐 $\dot x = ax + bu$，$J = \tfrac12s(T)x^2(T) + \tfrac12\int(qx^2 + ru^2)dt$（$A = a$, $B = b$, $Q = q$, $R = r$）：$-\dot s = 2as - \frac{b^2}{r}s^2 + q$ → 分離變數，從 $t$ 積到 $T$；$K = bs/r$
- **ARE**（📐 $T \to \infty$：$J = \tfrac12\int_0^\infty(x^TQx + u^TRu)dt$）：$0 = A^TS + SA - SBR^{-1}B^TS + Q$，取正定解；scalar 閉迴路極點 $-\sqrt{a^2 + b^2q/r}$
- Hamiltonian 矩陣：$\begin{bmatrix}\dot x\\ \dot\lambda\end{bmatrix} = \begin{bmatrix}A & -BR^{-1}B^T\\ -Q & -A^T\end{bmatrix}\begin{bmatrix}x\\ \lambda\end{bmatrix}$（代入 $u = -R^{-1}B^T\lambda$）：特徵值 $\pm\mu$ 成對；穩定那半 = 閉迴路極點；$S = \Lambda X^{-1}$
- Chang-Letov 📐 單輸入單輸出 $\dot x = Ax + bu$，$y = Cx$，$J = \tfrac12\int_0^\infty(qy^2 + ru^2)dt$（即 $Q = qC^TC$）；$\Delta(s) = \det(sI - A)$，$\frac{N(s)}{\Delta(s)} = C(sI - A)^{-1}b$：$\Delta_c(s)\Delta_c(-s) = \Delta(s)\Delta(-s) + \frac qrN(s)N(-s)$，取左半平面根
- 固定 $K$（📐 $u = -Kx$ 給定，$J = \tfrac12x_0^TPx_0$）：$(A - BK)^TP + P(A - BK) + Q + K^TRK = 0$

**終點固定、最小能量** 📐 $\dot x = Ax + Bu$，$J = \tfrac12\int_{t_0}^Tu^TRu\,dt$（$Q = 0$），$x(t_0) = x_0$、$x(T) = r$ → 開迴路
- $G = \int_{t_0}^Te^{A(T-\tau)}BR^{-1}B^Te^{A^T(T-\tau)}d\tau$
- $u(t) = R^{-1}B^Te^{A^T(T-t)}G^{-1}\big(r - e^{A(T-t_0)}x_0\big)$，$J^* = \tfrac12(\cdot)^TG^{-1}(\cdot)$

## E. Żak Ch 3：可控、可觀察

📐 **標準式**：$\dot x = Ax + Bu$，$y = Cx + Du$（離散 $x_{k+1} = Ax_k + Bu_k$）；$x \in \mathbb R^n$。可控看 $(A, B)$，可觀察看 $(A, C)$

| | 可控（reachable） | 可觀察 |
|---|---|---|
| 秩 | $[B\ AB\ \cdots\ A^{n-1}B]$ | $[C;\ CA;\ \cdots;\ CA^{n-1}]$ |
| PBH | $[sI - A\ \ B]$ 秩 $n$，$\forall s \in \text{eig}A$ | $[sI - A;\ C]$ 秩 $n$，$\forall s \in \text{eig}A$ |
| Gramian | $W = \int_{t_0}^{t_1}e^{-At}BB^Te^{-A^Tt}dt$ 非奇異 | $V = \int_{t_0}^{t_1}e^{A^Tt}C^TCe^{At}dt$ 非奇異 |
| 弱化 | stabilizable | detectable |

- 把 $x_0 \to x(t_1)$ 的控制：$u(t) = B^Te^{-A^Tt}W^{-1}\big(e^{-At_1}x(t_1) - e^{-At_0}x_0\big)$
- 重建 $x_0$（$t_0 = 0$）：$g = y - \int_0^tCe^{A(t-\tau)}Bu\,d\tau - Du$，$x_0 = V^{-1}\int_0^{t_1}e^{A^Tt}C^Tg\,dt$
- 離散：reachable ⇒ controllable（$A$ 非奇異才等價）；controllable ⇔ $\text{range}(A^n) \subset \text{range}[B\ \cdots\ A^{n-1}B]$。連續：兩者等價
- 不可達 ⇔ 存在 $T$：$TAT^{-1} = \begin{bmatrix}A_1 & A_2\\ 0 & A_4\end{bmatrix}$、$TB = \begin{bmatrix}B_1\\ 0\end{bmatrix}$；$A_4$ 穩定 → stabilizable
- 對偶：$(A, B)$ 可控 ⇔ $(A^T, B^T)$ 可觀察；相似轉換不改變可控 / 可觀察

## F. Żak Ch 4：穩定性

📐 **標準式**：$\dot x = f(t, x)$，平衡點 $f(t, x_e) = 0$（常取 $x_e = 0$）；線性 $\dot x = Ax$（離散 $x_{k+1} = Ax_k$）

- **stable**：$\forall\varepsilon\ \exists\delta$，$\lVert x(t_0)\rVert < \delta \Rightarrow \lVert x(t)\rVert < \varepsilon\ \forall t \ge t_0$；**convergent**：$x \to x_e$；**漸近穩定** = stable **且** convergent；**uniform**：$\delta$（及 $T$）與 $t_0$ 無關；**uniformly exponentially**：$\lVert x(t)\rVert \le \gamma e^{-\lambda(t-t_0)}\lVert x_0\rVert$，$\gamma \ge 1$
- **Lyapunov 函數**：$V > 0$，$\dot V < 0$（或 $\le 0$）
- 連續 $A^TP + PA = -Q$；離散 $A^TPA - P = -Q$。漸近穩定 ⇔ 任 $Q > 0$ 的解 $P > 0$；可放寬 $Q = C^TC$、$(A, C)$ 可觀察。**由 $Q$ 解 $P$**
- 解：$P = \int_0^\infty e^{A^Tt}Qe^{At}dt$；$P = \sum_{k \ge 0}(A^T)^kQA^k$。唯一解條件：連續 $\lambda_i + \lambda_j \ne 0$；離散 $\lambda_i\lambda_j \ne 1$
- **二次型指標**（📐 沿 $\dot x = Ax$、$A$ 穩定）：$\int_0^\infty x^TQx\,dt = x_0^TPx_0$；$\int_0^\infty t\,x^TQx\,dt = x_0^TP_1x_0$，$A^TP_1 + P_1A = -P$
  離散 $\sum x_k^TQx_k = x_0^TPx_0$；$\sum k\,x_k^TQx_k = x_0^T(P_1 - P)x_0$，$A^TP_1A - P_1 = -P$
- 轉移函數 → 狀態空間：$E(s) = \frac{b_{n-1}s^{n-1} + \cdots + b_0}{s^n + a_{n-1}s^{n-1} + \cdots + a_0}$ → 伴隨型 $A$（最後一列 $-a_0 \cdots -a_{n-1}$），初值由 Hankel 型方程 $[a_1\ \cdots\ 1;\ \cdots;\ 1\ 0 \cdots]\,x(0) = [b_0;\ \cdots;\ b_{n-1}]$
- **Robust**：$\dot x = Ax + Bu + f + Bh$，$\lVert h\rVert \le \gamma_h\lVert u\rVert + \alpha_h\lVert x\rVert$，$\lVert f\rVert \le \alpha_f\lVert x\rVert$；$A$ 穩定、$A^TP + PA = -2Q$；若 $\alpha_f < \frac{\lambda_{\min}(Q)}{\lambda_{\max}(P)}$、$\gamma_h < 1$，則 $u = -\gamma B^TPx$，$\gamma > \frac{\alpha_h^2}{4(\lambda_{\min}(Q) - \alpha_f\lambda_{\max}(P))(1 - \gamma_h)}$ 穩定

---

# 背面

## G. Żak Ch 5：變分法、LQR、PMP

- 指標：$\int x^Tx$（狀態小）、$\int x^TC^TCx$（輸出小）、$\int u^TRu$（能量小）、$x^T(t_f)Fx(t_f)$（終點）；$R$ 可取對稱 $\tfrac12(R + R^T)$
- 變分：$\delta v = \frac{d}{d\alpha}v(x + \alpha\delta x)\rvert_{\alpha = 0}$；極值 ⇒ $\delta v = 0$
- **Euler-Lagrange** 📐 $\min J = \int_{t_0}^{t_1}F(t, x, \dot x)\,dt$，$x(t_0)$ 給定（$x(t_1)$、$t_1$ 給定或自由）：$F_x - \frac{d}{dt}F_{\dot x} = 0$（多變數：每個 $x_i$ 一條）
  - $F$ 不含 $x$ → $F_{\dot x} = $ 常數；$F$ 不含 $t$ → $F - \dot xF_{\dot x} = $ 常數
- **Transversality**：$x(t_1)$ 自由 $F_{\dot x}\rvert_{t_1} = 0$；$t_1$ 自由 $(F - \dot xF_{\dot x})\rvert_{t_1} = 0$；終點在 $x = g(t)$ 上 $(F + (\dot g - \dot x)F_{\dot x})\rvert_{t_1} = 0$
- **LQR（Żak）** 📐 $\dot x = Ax + Bu$，$J = \int_0^\infty(x^TQx + u^TRu)dt$（無 $\tfrac12$）：$V = x^TPx$，$\min_u(\dot V + x^TQx + u^TRu) = 0$ ⇒ 最佳，$u = -R^{-1}B^TPx$，$A^TP + PA + Q - PBR^{-1}B^TP = 0$，$J = x_0^TPx_0$（注意 Żak 沒有 $\tfrac12$）
- **HJB** 📐 $\dot x = f(x, u)$，$J = \int_t^\infty F(x, u)d\tau$：$0 = \min_u[F + \nabla J^{*T}f]$；多個候選解時取**讓閉迴路穩定**、$J^*(x(\infty)) = 0$ 的那個
- **PMP** 📐 $\dot x = f(x, u)$，$J = \Phi\big(x(t_f)\big) + \int_{t_0}^{t_f}F(x, u)dt$，$u(t) \in U$（有界集合）：$H = F + p^Tf$，$u^* = \arg\min_{u \in U}H$，$\dot p = -(\partial H/\partial x)^T$；$x(t_f)$ 自由 → $p(t_f) = \nabla_x\Phi$；$x(t_f)$ 固定 → $p(t_f)$ 待解
- **Bang-bang** 📐 $\dot x = Ax + Bu$，$\lvert u_i\rvert \le 1$，最短時間 $J = \int_{t_0}^{t_f}1\,dt$（$F = 1$，$t_f$ 自由）→ $H = 1 + p^T(Ax + Bu)$ 對 $u$ 線性 → $u^* = -\text{sign}(B^Tp)$（$B^Tp$ = switching function）；切換次數 = 變號次數（二階實極點系統最多切換 1 次）

## H. Lewis Ch 6：動態規劃

📐 **標準式**：$x_{k+1} = f^k(x_k, u_k)$，$J_i(x_i) = \phi(N, x_N) + \sum_{k=i}^{N-1}L^k(x_k, u_k)$；$J_k^*(x)$ = 從時間 $k$、狀態 $x$ 出發的最小剩餘成本。路徑題：節點 = 狀態，邊上數字 = $L$，終點 $\phi = 0$

- **原理**：最佳策略的剩餘部分，對當時的狀態也是最佳 → 逆推
- $J_k^*(x_k) = \min_{u_k}[L^k(x_k, u_k) + J_{k+1}^*(x_{k+1})]$，$J_N^* = \phi$；最大化把 min 換 max
- 格點：每個狀態 × 每個允許的 $u$；限制 = 不列入；不在格點上線性內插
- 結果：回授 $u^*(x, k)$；格點上全域最佳；短視（只看眼前）不保證最佳
- 計算量：列舉所有序列隨 $N$ 指數成長；DP 隨 $N$ 線性、隨**狀態維度**指數成長（維度詛咒）
- **HJB** 📐 $\dot x = f(x, u, t)$，$J(x, t) = \phi\big(x(T), T\big) + \int_t^TL\,d\tau$：$-J_t^* = \min_u[L + J_x^{*T}f] = \min_uH(x, u, J_x^*, t)$，$J^*(x, T) = \phi$；$\lambda = J_x^*$ 滿足 Ch 3 共態方程
- **猜二次式**：$J^* = \tfrac12x^TSx$（離散 $S_k$）→ 對 $u$ 微分 → 代回 → 對所有 $x$ 比較 → Riccati
- 選擇：線性二次無限制 → Riccati；有限選項 / 限制 / 低維非線性 → DP；高維單一軌跡 → 三條件數值解；$u$ 有界解析解 → PMP；模型未知 → RL

## I. Lewis Ch 11：強化學習

- **MDP** $(X, U, P, R)$：$P^u_{xx'} = \Pr\{x' \mid x, u\}$；Markov 性質；策略 $\pi(x, u) = \Pr\{u \mid x\}$（確定性 $u = h(x)$）
- $V^\pi(x) = E_\pi\{\sum_{i \ge 0}\gamma^ir_{k+i} \mid x_k = x\}$，$0 \le \gamma < 1$（$\gamma = 1$ 需終止或穩定）
- **Bellman**：$V^\pi(x) = \sum_u\pi\sum_{x'}P^u_{xx'}[R^u_{xx'} + \gamma V^\pi(x')]$；確定性 $V^h(x_k) = r_k + \gamma V^h(x_{k+1})$
- **最佳性**：$V^*(x) = \min_u\sum_{x'}P^u_{xx'}[R^u_{xx'} + \gamma V^*(x')]$（= 離散 HJB；兩邊同一個 $V$ → 疊代）
- **閉迴路 Markov chain**：$p_{ij} = \sum_u\pi(i, u)P^u_{ij}$，$V = \gamma PV + (P \odot R)\mathbf 1 \Rightarrow V = (I - \gamma P)^{-1}(P \odot R)\mathbf 1$；穩態分布 $p_\infty^T = p_\infty^TP$（$\lambda = 1$ 的左特徵向量），$p(i) = 1/T_i$（平均回訪時間）；$p_{k+1}^T = p_k^TP$；$(P \odot R)\mathbf 1 = c$（$c_i = \sum_u\pi\sum_jP^u_{ij}R^u_{ij}$ = 走一步期望成本）；長期平均成本 $\bar V = p_\infty^Tc$。先檢查 $P$ 每列和 = 1；穩態要補 $\sum p = 1$；ergodic ⇒ 有確定性最佳策略
- **LQR** 📐 $x_{k+1} = Ax_k + Bu_k$，策略 $u_k = -Kx_k$，$r_k = \tfrac12(x_k^TQx_k + u_k^TRu_k)$，$V(x_k) = \sum_{i \ge k}r_i = \tfrac12x_k^TPx_k$（$\gamma = 1$）：Bellman ⇔ $(A - BK)^TP(A - BK) - P + Q + K^TRK = 0$（Lyapunov，對 $P$ 線性）；最佳性 ⇔ DARE（非線性），$u = -(B^TPB + R)^{-1}B^TPAx$；離散 Hamiltonian $H = r_k + V(x_{k+1}) - V(x_k)$ = TD 誤差

**PI / VI**（$j$ = 疊代，非時間；改進 = greedy $h' = \arg\min_u[r + \gamma V(x')]$，保證 $V^{h'} \le V^h$）

| | PI | VI |
|---|---|---|
| 評分 | 完整解 Bellman（$N$ 條線性方程） | 只代入一次 $V_{j+1} = r + \gamma V_j(x')$ |
| 收斂 | 輪數少；有限 MDP 有限步 | 輪數多；$0 < \gamma < 1$ 時收斂 |
| 起點 | admissible（穩定） | 任意 |
| LQR | Hewer：每輪解 Lyapunov | Lyapunov 遞迴（= 離散 Riccati 逆推） |
| 連續 LQR | Kleinman：$(A - BK)^TP + P(A - BK) + Q + K^TRK = 0$，$K = R^{-1}B^TP$ | — |

- 折衷：Generalized PI（評分做幾次代入）；非同步 VI（每次只更新部分狀態）
- 迭代策略評估 $V^{i+1} = \sum\pi\sum P[R + \gamma V^i]$ 是 contraction，收斂到 Bellman 解
- **Q 函數**：$Q^\pi(x, u) = \sum_{x'}P^u_{xx'}[R + \gamma V^\pi(x')]$；$V^\pi(x) = Q^\pi(x, \pi(x))$；$u^* = \arg\min_uQ^*$（**不需 $P$**）
  - $Q^*(x, u) = \sum P[R + \gamma\min_{u'}Q^*(x', u')]$（min 和期望值的順序與 $V$ 版相反）
  - LQR：$Q(x, u) = \tfrac12\begin{bmatrix}x\\u\end{bmatrix}^TG\begin{bmatrix}x\\u\end{bmatrix}$，$G = \begin{bmatrix}A^TPA + Q & A^TPB\\ B^TPA & B^TPB + R\end{bmatrix}$，$K = G_{uu}^{-1}G_{ux}$
  - **Q-learning**：$Q(x_k, u_k) \leftarrow Q + \alpha_k[r_k + \gamma\min_uQ(x_{k+1}, u) - Q(x_k, u_k)]$；$\sum\alpha_k = \infty$、$\sum\alpha_k^2 < \infty$，每個 $(x, u)$ 無限次造訪
- **TD**：$e_k = r_k + \gamma\hat V(x_{k+1}) - \hat V(x_k)$

| | 精確 | Monte Carlo | TD |
|---|---|---|---|
| 模型 | 要 | 不用 | 不用 |
| 資料 | — | 多趟、整趟後更新、需 exploring starts | 單一軌跡、每步更新 |

- **VFA / ADP**：$V \approx W^T\phi(x)$；LQR 時 $\phi$ = 二次項（$n(n+1)/2$ 個）、$W = P$ 元素；$W_{j+1}^T[\phi(x_k) - \gamma\phi(x_{k+1})] = r_k$，最小平方 / RLS；regression vector 需 **persistently exciting**（加探索雜訊）
- 改進：用 $V$ 需 $g$（$B$）與 $A$；加 actor NN 只需 $g$；Q-learning 都不需
- **IRL** 📐 $\dot x = f(x) + g(x)u$，$V(x(t)) = \int_t^\infty r\,d\tau$，$r = Q(x) + u^TRu$：$V(x(t)) = \int_t^{t+T}r\,d\tau + V(x(t + T))$ 不需 $f$；$u = -\tfrac12R^{-1}g^T\nabla V$ 需 $g$；混合式（$K$ 分段常數）
- **同步（11.7）**：critic、actor 同時連續調整；需完整 $f, g$

## J. 是非題快查

答題：✓ 寫主要理由（必要時一兩行證明）；✗ 指出錯處並改正或舉反例。

| 敘述 | | 理由 / 改正 |
|---|---|---|
| Lagrange 必要條件即保證最小 | ✗ | 要檢查（沿約束的）二階條件 |
| 三個條件 / PMP 給全域最佳 | ✗ | 必要條件；DP 才是全域（格點上） |
| 離散 Hamiltonian 配 $\lambda_k$ | ✗ | 配 $\lambda_{k+1}$ |
| 連續共態 $\dot\lambda = H_x$ | ✗ | $-\dot\lambda = H_x$ |
| 終點固定時 $\lambda(T) = \phi_x$ | ✗ | $x(T) = r$，$\lambda(T)$ 待解 |
| 終點固定的最小能量控制是開迴路 | ✓ | 需可達 Gramian 非奇異 |
| 有限時間 LQR 增益為常數 | ✗ | 時變；遠離終點才趨近 $K_\infty$ |
| 離散與連續 LQR 增益公式相同 | ✗ | 離散多 $B^TSB$ 與 $A$；$\Delta t \to 0$ 才相同 |
| ARE 任一解皆可 | ✗ | 取正定（stabilizing）解 |
| 只要 $(A, B)$ 可控，任何 $Q \ge 0$ 的 LQR 都穩定 | ✗ | 還需 $(A, \sqrt Q)$ detectable |
| $Q, R$ 同乘常數不改變 $K$ | ✓ | $S$ 同比例放大 |
| $H$ 沿最佳軌跡恆為常數 | ✗ | 需 $f, L$ 不含 $t$ |
| DP 用順時間的經驗求解 | ✗ | 逆時間、離線、需模型；順時間是 RL |
| DP 容易處理控制限制 | ✓ | 不允許的不列入候選 |
| DP 計算量隨 $N$ 指數成長 | ✗ | 隨 $N$ 線性；隨狀態維度指數 |
| 每步選眼前最便宜即為最佳 | ✗ | 需加上之後的最佳值 |
| HJB 的 $\partial J^*/\partial x$ 就是共態 | ✓ | 可推回 Ch 3 共態方程 |
| 連續 reachable ⇔ controllable | ✓ | 離散需 $A$ 非奇異 |
| 只量部分狀態就一定無法知道全部狀態 | ✗ | 可觀察即可重建 |
| 可控性在相似轉換下會改變 | ✗ | 不變 |
| convergent 即漸近穩定 | ✗ | 還需 stable |
| 穩定的 $A$ 必負定 | ✗ | 看特徵值實部 |
| 先選 $P > 0$ 算出 $Q$ 即可判穩定 | ✗ | 須由 $Q > 0$ 解 $P$；算出的 $Q$ 不定時無結論 |
| 離散穩定看特徵值實部 | ✗ | 看 $\lvert\lambda\rvert < 1$ |
| E-L 可處理 $\lvert u\rvert \le 1$ | ✗ | 用 PMP |
| bang-bang 出現在 $H$ 對 $u$ 二次時 | ✗ | 對 $u$ 線性時 |
| Bellman 方程對任何策略成立且可給評分 | ✓ | 一致性方程；最佳性方程才有 min |
| PI 可從任意策略開始 | ✗ | 需 admissible；VI 才任意 |
| PI 輪數少、VI 每輪便宜 | ✓ | PI 完整解；VI 只代入一次 |
| VI 每輪得到目前策略的真 value | ✗ | 只代入一次 |
| PI / VI 的 $j$ 是時間 | ✗ | 疊代次數 |
| 用 $V$ 改進策略不需模型 | ✗ | 需模型；Q 才不需 |
| TD 需完整一趟才更新 | ✗ | 每步；Monte Carlo 才整趟 |
| 學習時一直照目前策略即可 | ✗ | 需探索（PE） |
| LQR 的 Bellman 方程對 $P$ 是線性的 | ✓ | Lyapunov；最佳性（DARE）非線性 |
| IRL 需知道 $A$ | ✗ | 只需 $B$ |

## K. 考場流程

寫 $H$ → 對 $u$ 微分（有界取範圍內最小）→ 共態（連續加負號）→ 邊界（固定 / 自由）→ LQR 猜二次式比較係數 → 驗算（代終點、退化成已知情況、檢查正定與穩定）。問 closed-loop 答 $u = -K(\cdot)x$；問 open-loop 答 $u^*(t)$。
