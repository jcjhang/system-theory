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

**離散版本**（每 0.1 秒量一次，用 Euler 近似 $\omega_{k+1} \approx \omega_k + 0.1\,\dot\omega_k$）：
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
- **特徵值 $\lambda$**：見下面 0.3.1，這個概念需要多花一點時間

#### 0.3.1 特徵值與特徵向量：矩陣的「天生方向」

**先看一個例子。** 令
$$A = \begin{bmatrix}2 & 1\\ 1 & 2\end{bmatrix}$$
拿幾個向量給 $A$ 乘乘看：

| 輸入 $v$ | 輸出 $Av$ | 發生什麼事 |
|---|---|---|
| $[1,\ 0]^T$ | $[2,\ 1]^T$ | 方向變了（歪掉了） |
| $[1,\ 1]^T$ | $[3,\ 3]^T = 3\cdot[1,\ 1]^T$ | **方向沒變，只被放大 3 倍** |
| $[1,\ -1]^T$ | $[1,\ -1]^T = 1\cdot[1,\ -1]^T$ | **方向沒變，放大 1 倍（不變）** |

大部分向量被 $A$ 一乘，方向都會跑掉；但有少數「天生方向」，$A$ 只會把它**拉長或縮短**，不會轉彎。
- 這些特別的方向叫**特徵向量 (eigenvector)** $v$
- 被拉長的倍數叫**特徵值 (eigenvalue)** $\lambda$
- 寫成式子就是 $Av = \lambda v$

上例中：$\lambda_1 = 3$（方向 $[1,1]^T$），$\lambda_2 = 1$（方向 $[1,-1]^T$）。

**怎麼算特徵值？**
$Av = \lambda v \Rightarrow (A - \lambda I)v = 0$。要有**非零**的 $v$ 滿足這條，$A - \lambda I$ 必須「不可逆」，也就是：
$$\det(A - \lambda I) = 0$$

**2×2 速算公式**（考試超好用）：
$$\lambda^2 - \underbrace{(a_{11} + a_{22})}_{\text{trace（對角線和）}}\lambda + \underbrace{(a_{11}a_{22} - a_{12}a_{21})}_{\det A} = 0$$

- 上例：trace $= 4$、det $= 3$ → $\lambda^2 - 4\lambda + 3 = 0$ → $\lambda = 1, 3$ ✓
- **馬達** $A = \begin{bmatrix}0 & 1\\ 0 & -1\end{bmatrix}$：trace $= -1$、det $= 0$ → $\lambda^2 + \lambda = 0$ → $\lambda = 0, -1$
- 小技巧：**三角矩陣**（對角線一邊全是 0）的特徵值就是對角線元素，馬達的 $A$ 就是這種，直接看出 $0, -1$

**特徵值也可能是複數。** 例如 $A = \begin{bmatrix}0 & 1\\ -1 & 0\end{bmatrix}$：trace $= 0$、det $= 1$ → $\lambda^2 + 1 = 0$ → $\lambda = \pm j$。
複數特徵值代表「沒有任何方向是只伸縮不轉彎的」——這個矩陣本身就是在「轉」，對應到系統就是**振盪**。

#### 0.3.2 為什麼特徵值決定系統穩不穩定？

**第一步：先看一維。** $\dot x = a x$ 的解是
$$x(t) = e^{at} x_0$$
（驗算：$\dot x = a e^{at} x_0 = a x$ ✓）

| $a$ | $x(t)$ 的行為 | 例：$x_0 = 10$ |
|---|---|---|
| $a = -1 < 0$ | 指數衰減 → 歸零 | $t=1$: 3.68；$t=3$: 0.50；$t=5$: 0.07 |
| $a = 0$ | 永遠不變 | 永遠是 10 |
| $a = +1 > 0$ | 指數爆炸 | $t=1$: 27；$t=3$: 201；$t=5$: 1484 |

**第二步：多維時，特徵向量把問題「拆成好幾個一維」。**
如果初始狀態剛好在特徵向量方向 $x_0 = v$，那解就是
$$x(t) = e^{\lambda t} v$$
（驗算：$\dot x = \lambda e^{\lambda t} v = e^{\lambda t} (Av) = A x$ ✓）
意思是：**沿著特徵向量方向，系統就像一維的 $\dot x = \lambda x$**，只是把 $a$ 換成 $\lambda$。

一般的 $x_0$ 可以拆成特徵向量的組合 $x_0 = c_1 v_1 + c_2 v_2$，於是
$$x(t) = c_1 e^{\lambda_1 t} v_1 + c_2 e^{\lambda_2 t} v_2$$
每個方向各自獨立演化。**只要有一個方向爆炸，整個系統就爆炸**；要全部方向都衰減，系統才會歸零。

（$x(t) = e^{At}x_0$ 裡的 $e^{At}$ 叫**矩陣指數**，考試很少要你直接算它；真正重要的是上面這個「拆成特徵方向」的想法。）

**第三步：複數特徵值怎麼看？** $\lambda = \sigma + j\omega$ 時，
$$e^{\lambda t} = \underbrace{e^{\sigma t}}_{\text{大小：由實部決定}} \cdot \underbrace{(\cos\omega t + j\sin\omega t)}_{\text{轉圈：由虛部決定}}$$
- **實部 $\sigma$** 決定「越來越大還是越來越小」
- **虛部 $\omega$** 決定「振盪多快」
- 所以判斷穩定**只看實部**

**結論：**
- 所有特徵值的**實部 $< 0$** → 系統會慢慢歸零（**漸近穩定**）
- 有任何一個**實部 $> 0$** → 會爆炸（**不穩定**）
- 有**實部 $= 0$**、其餘 $< 0$ → 不會歸零也不會爆炸（**臨界**，例如停在某處或持續振盪）
  - ⚠️ 例外：實部為 0 的特徵值如果**重複出現**，可能會「線性成長」而變成不穩定。例：沒摩擦的馬達 $A = \begin{bmatrix}0 & 1\\ 0 & 0\end{bmatrix}$（$\lambda = 0, 0$），解是 $\theta(t) = \theta_0 + \omega_0 t$，角度一直變大。

**馬達實際算一次**（$\lambda = 0, -1$）：
- $\lambda_1 = 0$：解 $Av = 0$ → $v_1 = [1,\ 0]^T$（純角度方向）
- $\lambda_2 = -1$：解 $(A + I)v = 0$，即 $\begin{bmatrix}1 & 1\\ 0 & 0\end{bmatrix}v = 0$ → $v_2 = [1,\ -1]^T$
- 把 $x_0 = [\theta_0,\ \omega_0]^T$ 拆開：$c_1 = \theta_0 + \omega_0$、$c_2 = -\omega_0$
- 解：
$$\theta(t) = (\theta_0 + \omega_0) - \omega_0 e^{-t}, \qquad \omega(t) = \omega_0 e^{-t}$$
- 解讀：$\lambda = -1$ 那個方向衰減掉 → **轉速歸零**；$\lambda = 0$ 那個方向保持不變 → **角度停在 $\theta_0 + \omega_0$**，不會回到 0。這正是 §4.4 說的「臨界穩定」。

**離散系統的版本**：$x_{k+1} = A x_k$ 的解是 $x_k = A^k x_0$，沿特徵方向變成 $\lambda^k$。
所以離散系統看的是 **$|\lambda| < 1$**（在單位圓內）。例：$\omega_{k+1} = 0.9\,\omega_k$ → $\omega_k = 0.9^k \omega_0$ → 歸零 ✓。

| | 連續 $\dot x = Ax$ | 離散 $x_{k+1} = Ax_k$ |
|---|---|---|
| 沿特徵方向 | $e^{\lambda t}$ | $\lambda^k$ |
| 穩定條件 | $\text{Re}(\lambda) < 0$（左半平面） | $\lvert\lambda\rvert < 1$（單位圓內） |

### 0.4 什麼是「正定 (positive definite)」？

**先從一維開始。** $V(x) = p x^2$：
- $p > 0$ → 碗口朝上的拋物線，只有 $x = 0$ 時等於 0，其他地方都 $> 0$
- $p < 0$ → 碗倒過來
- 「正定」就是把「$p > 0$」推廣到矩陣

**矩陣版的定義**：一個**對稱**方陣 $P$ 是**正定**（記作 $P > 0$）如果：
> **對任何非零的向量 $x$，都有 $x^T P x > 0$**

**$x^T P x$ 展開長什麼樣？** 設 $P = \begin{bmatrix}p_{11} & p_{12}\\ p_{12} & p_{22}\end{bmatrix}$，則
$$x^T P x = p_{11}x_1^2 + 2p_{12}x_1x_2 + p_{22}x_2^2$$
就是一個「二次多項式」，所以叫**二次型 (quadratic form)**。這門課的成本函數 $x^TQx$、$u^TRu$ 全都是這種東西。

**三個例子：**

| $P$ | $x^T P x$ | 結論 |
|---|---|---|
| $\begin{bmatrix}2 & 0\\ 0 & 3\end{bmatrix}$ | $2x_1^2 + 3x_2^2$ | 非零時一定 $> 0$ → **正定** $P > 0$ |
| $\begin{bmatrix}1 & 1\\ 1 & 1\end{bmatrix}$ | $(x_1 + x_2)^2$ | 永遠 $\ge 0$，但 $x = [1,-1]^T$ 時 $= 0$ → **半正定** $P \ge 0$ |
| $\begin{bmatrix}1 & 2\\ 2 & 1\end{bmatrix}$ | $x_1^2 + 4x_1x_2 + x_2^2$ | $x = [1,-1]^T$ 時 $= -2 < 0$ → **不是正定** |

**直覺**：正定的 $V(x) = x^T P x$ 就像一個「碗」——最低點在原點，其他地方都比 0 大。半正定則像「水溝」，有一整條線的高度都是 0。

**怎麼判斷？**
1. **特徵值法**：$P$ 的**所有特徵值都 $> 0$** ⇔ 正定（$\ge 0$ ⇔ 半正定）
   - 驗證上表：$\begin{bmatrix}1 & 2\\ 2 & 1\end{bmatrix}$ 的 trace $= 2$、det $= -3$ → $\lambda = 3, -1$，有負的 → 不是正定 ✓
2. **2×2 速算**：$p_{11} > 0$ **且** $\det P > 0$ ⇔ 正定
   - $\begin{bmatrix}2 & 0\\ 0 & 3\end{bmatrix}$：$2 > 0$、det $= 6 > 0$ ✓
   - $\begin{bmatrix}1 & 1\\ 1 & 1\end{bmatrix}$：det $= 0$ → 不是正定（只是半正定）

（這些判準只對**對稱矩陣**成立。最佳控制裡的 $P, Q, R, S$ 都取對稱——因為 $x^TPx$ 只看得到 $P$ 的對稱部分，例如 $\begin{bmatrix}1 & 2\\ 0 & 1\end{bmatrix}$ 和 $\begin{bmatrix}1 & 1\\ 1 & 1\end{bmatrix}$ 算出來的 $x^TPx$ 一模一樣，所以乾脆都寫成對稱的。）

**為什麼課本一直要求 $Q \ge 0$、$R > 0$？**
- $Q \ge 0$（半正定就好）：允許你「不在意某些狀態」。例如只在意轉速、不在意角度，就取 $Q = \begin{bmatrix}0 & 0\\ 0 & 1\end{bmatrix}$
- $R > 0$（一定要正定）：每一個控制方向都要付錢，否則控制器會「免費無限出力」；而且公式裡要算 $R^{-1}$，$R$ 必須可逆

**為什麼碗形 = 能量函數？** 這是 §4 Lyapunov 的伏筆：如果 $V(x)$ 是一個碗，而且系統沿著軌跡走時 $V$ 一直**下降**，那狀態只能一路滑到碗底——也就是原點。

> ⚠️ **別搞混**：「正定」和「穩定」是兩件事，看的是**不同矩陣**的特徵值。
> - **穩定**：看系統矩陣 $A$ 的特徵值，**實部**要全 $< 0$（0.3.2）
> - **正定**：看能量矩陣 $P$（對稱）的特徵值，要全 $> 0$（本節）
>
> 兩者怎麼連起來（Lyapunov 方程），留到 §4.3 再講。

### 0.5 一個關鍵微分公式

**「對向量微分」是什麼意思？** $f(u)$ 是一個數字、$u$ 是一個向量時，$\dfrac{\partial f}{\partial u}$ 就是把「對每個分量的偏微分」排成一個向量（也就是**梯度**）：
$$\frac{\partial f}{\partial u} = \begin{bmatrix}\partial f/\partial u_1\\ \partial f/\partial u_2\\ \vdots\end{bmatrix}$$

**核心公式**：給定二次型 $f(u) = \tfrac{1}{2} u^T R u$（$R$ 對稱）：
$$\boxed{\frac{\partial f}{\partial u} = R u}$$

**跟一維比較就很好記**：$\tfrac{1}{2} r u^2$ 微分是 $r u$；矩陣版長得一模一樣。（前面的 $\tfrac{1}{2}$ 就是為了抵消平方微分後的 2。）

**2 維驗算**（不用背，看一次就好）：$R = \begin{bmatrix}r_1 & r_{12}\\ r_{12} & r_2\end{bmatrix}$
$$f = \tfrac{1}{2}(r_1 u_1^2 + 2r_{12}u_1u_2 + r_2 u_2^2)$$
$$\frac{\partial f}{\partial u_1} = r_1 u_1 + r_{12}u_2, \qquad \frac{\partial f}{\partial u_2} = r_{12}u_1 + r_2 u_2$$
排起來正好是 $\begin{bmatrix}r_1 & r_{12}\\ r_{12} & r_2\end{bmatrix}\begin{bmatrix}u_1\\ u_2\end{bmatrix} = Ru$ ✓

**常用微分表**（推 LQR 時一直用到）：

| 函數 | 對 $u$ 的微分 | 一維類比 |
|---|---|---|
| $\tfrac{1}{2}u^T R u$ | $Ru$ | $\tfrac12 ru^2 \to ru$ |
| $b^T u$（$b$ 是常數向量） | $b$ | $bu \to b$ |
| $x^T M u$（$x$ 跟 $u$ 無關） | $M^T x$ | $mxu \to mx$ |
| $\tfrac{1}{2}(Ax + Bu)^T S (Ax + Bu)$ | $B^T S (Ax + Bu)$ | 連鎖律：外層 $S(\cdot)$ 乘上內層導數 $B^T$ |

> **符號：$u^*$（讀作 u-star）** = 「**最佳的** $u$」，也就是讓成本最小的那個 $u$。星號 $*$ 在這門課都是「最佳」的意思：$u^*$ 最佳控制、$x^*$ 最佳軌跡、$J^*$ 最小成本（$J$ 是 Ch 2 起「總成本」的代號，§2.1 定義；Ch 1 的成本還叫 $L$，所以最小成本寫 $L^*$）。沒有星號的 $u$ 是「任意一個候選的 $u$」。

**小預告：Kalman gain 就是這樣來的。** 連續 LQR（§3.3.2）的駐點條件，就是要最小化
$$\tfrac{1}{2}u^T R u + \lambda^T B u \quad(\text{其他跟 } u \text{ 無關的項省略})$$
套上表：$Ru + B^T\lambda = 0$；再用 §2.2.2 的猜法 $\lambda = Sx$，得 $u^* = -R^{-1}B^T S x$。**一行就推完了**，這就是 $K = R^{-1}B^TS$。（離散版 §2.2.2 用的是同一招，只是多了 $B^TSB$ 一項，原因見 §3.3.3；§6.3 用 HJB 推 LQR 時也會再遇到同一個式子。）

### 0.6 極值的判斷（多變數微積分）

**先複習一維。** 想找 $L(u)$ 的最小值：
1. 一階導數 $= 0$：找到「平的地方」（候選點）
2. 二階導數 $> 0$：確認那裡是「碗底」而不是「山頂」

例：$L(u) = (u - 3)^2 + 1$
- $L'(u) = 2(u - 3) = 0 \Rightarrow u = 3$
- $L''(u) = 2 > 0$ → 是最小值，$L_{\min} = 1$

對照：$L = -(u-3)^2$ 在 $u = 3$ 也有 $L' = 0$，但 $L'' = -2 < 0$ → 那是**最大值**。所以第 2 步不能省。

**多維版本——完全同一套邏輯，只是換成向量/矩陣：**

| | 一維 | 多維 |
|---|---|---|
| 一階條件 | $L'(u) = 0$ | **梯度** $\dfrac{\partial L}{\partial u} = 0$（每個分量都是 0） |
| 二階條件 | $L''(u) > 0$ | **Hessian** $\dfrac{\partial^2 L}{\partial u^2} > 0$（正定，見 0.4） |

**Hessian** 就是「所有二階偏導數排成的矩陣」：
$$\frac{\partial^2 L}{\partial u^2} = \begin{bmatrix}\partial^2 L/\partial u_1^2 & \partial^2 L/\partial u_1 \partial u_2\\ \partial^2 L/\partial u_2 \partial u_1 & \partial^2 L/\partial u_2^2\end{bmatrix}$$
**為什麼「Hessian $> 0$」要用正定來判斷？**

先注意符號：矩陣寫 $> 0$ **不是**「每個元素都大於 0」，而是「**正定**」（0.4 的記號）。例如 $\begin{bmatrix}1 & 2\\ 2 & 1\end{bmatrix}$ 每個元素都是正的，但它不是正定。

**關鍵想法：多維的最小值 = 往每個方向走都變大。** 站在候選點 $u^*$，往任一方向 $d$ 走一小步，函數變多少？用泰勒展開：
$$L(u^* + d) \approx L(u^*) + \underbrace{\left(\frac{\partial L}{\partial u}\right)^T d}_{\text{梯度} = 0，\text{這項消失}} + \tfrac12\, d^T \underbrace{\frac{\partial^2 L}{\partial u^2}}_{\text{Hessian，簡寫 } \nabla^2 L} d$$
所以
$$L(u^* + d) - L(u^*) \approx \tfrac12\, d^T (\nabla^2 L)\, d$$

要 $u^*$ 是最小值，就要**不管往哪個方向 $d$ 走**，這個差都 $> 0$，也就是
$$d^T (\nabla^2 L)\, d > 0 \quad \text{對所有 } d \ne 0$$
這正是 0.4 正定的定義。所以「Hessian 正定」就是「往每個方向都是碗口朝上」的數學寫法。

**一維對照**：一維只有左、右兩個方向，上式變成 $\tfrac12 L''(u^*)\,d^2$。$d^2$ 永遠 $\ge 0$，所以只要 $L'' > 0$ 就夠了。多維的方向有無限多個，才需要「正定」這個比較強的條件。

**用 2 維例子驗證**：上面的 $L = u_1^2 + u_1u_2 + u_2^2 - 3u_1$，在 $u^* = (2, -1)$ 往 $d = (d_1, d_2)$ 走：
$$L(u^* + d) - L(u^*) = d_1^2 + d_1 d_2 + d_2^2 = \tfrac12\, d^T\begin{bmatrix}2 & 1\\ 1 & 2\end{bmatrix} d$$
（二次函數的泰勒展開剛好是精確的。）Hessian 正定 → 不管 $d$ 是什麼都 $> 0$ → 往哪走都變大 → 最小值 ✓

**反例：馬鞍點。** $L = u_1^2 - u_2^2$ 在原點的梯度是 0，但 Hessian $= \begin{bmatrix}2 & 0\\ 0 & -2\end{bmatrix}$ 不是正定：
- 沿 $u_1$ 方向走：$L = d_1^2 > 0$，變大
- 沿 $u_2$ 方向走：$L = -d_2^2 < 0$，**變小**

所以原點不是最小值，而是一個「馬鞍」：前後是上坡，左右是下坡。只檢查梯度 $= 0$ 會被騙，這就是為什麼要檢查 Hessian 是否正定。

**2 維例子**：$L(u_1, u_2) = u_1^2 + u_1u_2 + u_2^2 - 3u_1$
1. 梯度 $= 0$：
$$\frac{\partial L}{\partial u_1} = 2u_1 + u_2 - 3 = 0, \qquad \frac{\partial L}{\partial u_2} = u_1 + 2u_2 = 0$$
解聯立 → $u_1 = 2$、$u_2 = -1$
2. Hessian：$\begin{bmatrix}2 & 1\\ 1 & 2\end{bmatrix}$，就是 0.3.1 那個矩陣，特徵值 $1, 3$ 都 $> 0$ → 正定 → **是最小值**，$L_{\min} = -3$

**最常見的形式——二次函數**：$L(u) = \tfrac{1}{2}u^T R u + b^T u$
- 梯度（查 0.5 的表）：$Ru + b = 0 \Rightarrow u^* = -R^{-1}b$
- Hessian $= R$
- 所以 **$R > 0$ 就保證這是唯一的最小值**——這又是課本要求 $R > 0$ 的原因

**§1.1 的馬達例子**就是一維版的這個套路：$L_u = 0$ 得 $u^* = \omega_{\text{ref}}/(1+r)$，而 $L_{uu} = 1 + r > 0$ 確認是最小值。

> **整門課所有推導的基本套路**：
> 1. 把要最小化的東西寫出來（從 Ch 1 開始，這個東西通常叫 **Hamiltonian $H$**，見下方說明）
> 2. 對控制 $u$ 微分，令它 $= 0$ → 解出 $u^*$
> 3. 檢查二階導數 / Hessian $> 0$ → 確認是最小

**Hamiltonian $H$ 是什麼？（先有個印象，§1.2 正式介紹）**

第零章的例子都是「直接最小化一個函數」。但從 Ch 1 開始，問題會多一個「規則」：$u$ 不能亂選，狀態必須遵守狀態方程 $\dot x = f(x, u)$。

Hamiltonian 就是把「**成本**」和「**規則**」綁成一個式子的技巧：
$$H = \underbrace{L}_{\text{成本}} + \lambda^T \underbrace{f}_{\text{規則（狀態方程）}}$$
- $\lambda$ 是一個輔助變數（Lagrange multiplier，之後叫 **costate 共態**），可以想成「違反規則要付的價格」
- 綁好之後，就能套用上面的套路：對 $u$ 微分 $= 0$ 解出 $u^*$，彷彿沒有規則一樣

所以之後看到「對 $H$ 微分」，意思就是「在遵守規則的前提下找最佳 $u$」。

### 0.7 第零章統整

**一句話記住每個概念：**

| 概念 | 一句話 | 後面在哪裡用到 |
|---|---|---|
| 狀態 $x$ | 描述系統「現在」最少需要的數字 | 全部章節 |
| 狀態方程 $\dot x = Ax + Bu$ | $A$ = 放著不管怎麼變，$B$ = 控制怎麼推它 | 全部章節 |
| 特徵值 $\lambda$ | 矩陣在「天生方向」上的伸縮倍率 | 穩定性（Ż Ch 4）、PBH 檢驗（Ż Ch 3） |
| 穩定 | 看 **$A$** 的特徵值：連續看 $\text{Re}(\lambda) < 0$，離散看 $\lvert\lambda\rvert < 1$ | Ż Ch 4、LQR 閉迴路 |
| 正定 $P > 0$ | 看 **$P$** 的特徵值全 $> 0$；$x^TPx$ 是一個碗 | 成本 $Q, R$、Lyapunov 函數、Riccati 解 $S$ |
| 向量微分 | $\tfrac12 u^TRu \to Ru$，跟一維 $\tfrac12 ru^2 \to ru$ 一樣 | 每次推 $u^*$ |
| 極值 | 梯度 $= 0$ 找候選點，Hessian 正定確認是最小 | 每次推 $u^*$ |
| 星號 $u^*, J^*$ | 「最佳的」：最佳控制、最小成本 | 全部章節 |
| Hamiltonian $H$ | 成本 $+\ \lambda^T\times$ 規則，綁成一個式子再微分 | Ch 1 起每一章 |

**三個一定要會的計算：**
1. **2×2 特徵值**：$\lambda^2 - (\text{trace})\lambda + \det = 0$
2. **2×2 正定**：$p_{11} > 0$ 且 $\det P > 0$
3. **二次函數最小值**：$\tfrac12 u^TRu + b^Tu$ → $u^* = -R^{-1}b$（需要 $R > 0$）

**兩個最容易搞混的地方：**
- 「穩定」看 $A$，「正定」看 $P$——不同矩陣、不同條件（實部 $< 0$ vs. 特徵值 $> 0$）
- 矩陣的「$> 0$」是**正定**，不是「每個元素都大於 0」

**這些概念怎麼串起來：** 後面每一章都在做同一件事——寫出一個成本（二次型，要正定）→ 對 $u$ 微分找最佳控制（0.5、0.6）→ 檢查閉迴路系統的特徵值，確認它穩定（0.3）。

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

**$f$ 是什麼？為什麼要「$= 0$」？**

$f(x, u)$ 就是**把約束寫成一個函數**。任何一條等式規則「左邊 = 右邊」，都可以移項變成「左邊 − 右邊 = 0」，那個「左邊 − 右邊」就叫 $f$。

| 原本的規則 | 移項 | $f(x, u)$ |
|---|---|---|
| 馬達穩態：$\omega = u$ | $-\omega + u = 0$ | $-\omega + u$ |
| 預算：$x + u = 5$ | $x + u - 5 = 0$ | $x + u - 5$ |
| 圓上：$x^2 + u^2 = 1$ | $x^2 + u^2 - 1 = 0$ | $x^2 + u^2 - 1$ |

「$= 0$」**不是額外的物理條件，只是統一的寫法**。這樣寫的好處：
- 滿足約束時 $f = 0$，所以 $H = L + \lambda f = L + \lambda \cdot 0 = L$——在約束上 $H$ 和 $L$ 完全一樣，最小化 $H$ 就等於最小化 $L$
- $\partial H / \partial \lambda = f$，令它 $= 0$ 就把約束拿回來

⚠️ **同一個字母 $f$，兩種用法**：
- 0.2 的 $\dot x = f(x, u)$：$f$ 是**狀態方程**（系統怎麼動）
- 這裡的 $f(x, u) = 0$：$f$ 是**約束**
- 兩者在 Ch 2 會合流：狀態方程 $x_{k+1} = f(x_k, u_k)$ 本身就是約束，移項寫成 $f(x_k, u_k) - x_{k+1} = 0$，每個時間點都要遵守

**技巧**：發明一個新變數 $\lambda$（Lagrange multiplier），把兩件事合成一件事：
$$H(x, u, \lambda) = L(x, u) + \lambda^T f(x, u)$$
這個 $H$ 叫 **Hamiltonian**（後面每章都會出現）。

**必要條件（三兄弟）**：
$$\frac{\partial H}{\partial \lambda} = 0 \quad(\text{約束}), \quad \frac{\partial H}{\partial x} = 0, \quad \frac{\partial H}{\partial u} = 0$$

**為什麼是這三條？**

**先數未知數：** 有 $x$、$u$、$\lambda$ 三個未知數，就需要三條方程來解，一個變數配一條。

**第一條最簡單：** $\dfrac{\partial H}{\partial \lambda} = f(x, u) = 0$，就是約束本身。把 $\lambda$ 放進 $H$，對它微分就會把約束「吐」回來。

**後兩條從哪來？** 用 scalar（$x$、$u$ 都是一維）推一次，想法跟 0.6「往每個方向走都不能變小」一樣，只是現在**只能沿著約束走**：

1. **能走的方向**：要一直滿足 $f = 0$，小步 $(dx, du)$ 必須讓 $f$ 不變：
$$f_x\, dx + f_u\, du = 0$$
所以 $dx$ 不能亂選，它被 $du$ 決定了。真正自由的只有 $du$。
2. **最小值的條件**：沿著這些方向走，$L$ 的變化都要 $= 0$：
$$dL = L_x\, dx + L_u\, du = 0$$
3. **加一個零進去**：第 1 步那條等於 0，所以乘上任意數 $\lambda$ 加進來不影響結果：
$$dL = (L_x + \lambda f_x)\, dx + (L_u + \lambda f_u)\, du$$
4. **選一個好的 $\lambda$**：$\lambda$ 可以隨便挑，就挑讓 $dx$ 前面的括號 $= 0$ 的那個：
$$L_x + \lambda f_x = 0 \quad\Longleftrightarrow\quad \frac{\partial H}{\partial x} = 0$$
5. **剩下的 $du$ 是自由的**：$dL = (L_u + \lambda f_u)\, du$ 對任意 $du$ 都要 $= 0$，括號只能是 0：
$$L_u + \lambda f_u = 0 \quad\Longleftrightarrow\quad \frac{\partial H}{\partial u} = 0$$

（因為 $H = L + \lambda f$，所以 $H_x = L_x + \lambda f_x$、$H_u = L_u + \lambda f_u$。）

**一句話：** $\lambda$ 的作用是把「被約束綁住的 $dx$」消掉，讓問題變回 0.6 那種「每個變數各自微分 $= 0$」的無約束問題。

**用馬達驗證**（$L = \tfrac12(\omega - \omega_{\text{ref}})^2 + \tfrac12 ru^2$，$f = -\omega + u$）：
- 能走的方向：$-d\omega + du = 0 \Rightarrow d\omega = du$（電壓加多少，穩態轉速就加多少）
- 不用 $\lambda$ 直接算：$dL = (\omega - \omega_{\text{ref}})\,d\omega + ru\,du = \big[(\omega - \omega_{\text{ref}}) + ru\big]\,du = 0$，這就是 §1.1 的 $L_u = 0$
- 用 $\lambda$：$H_\omega = 0$ 給 $\lambda = \omega - \omega_{\text{ref}}$，$H_u = 0$ 給 $ru + \lambda = 0$，合起來正是同一條方程
- 所以 $\lambda$ 只是把「一條合併的方程」**拆成兩條比較好寫的**，答案完全一樣

**幾何直覺（選讀）：** 在約束上的最小點，$L$ 的梯度必須跟約束曲線**垂直**（否則沿著曲線走一點就能讓 $L$ 變小）。而 $f$ 的梯度本來就垂直於曲線 $f = 0$，所以兩個梯度平行：$\nabla L = -\lambda \nabla f$。移項就是 $H_x = 0$、$H_u = 0$。

**$\lambda$ 有什麼意義？** $\lambda$ 就是「這條約束的價格」——約束改動一點，最小成本會跟著變多少（下面馬達例子會實際算給你看）。這在動態問題中會變成 **costate**。

**馬達例子：把 §1.1 用 Lagrange 重做一次**

§1.1 我們偷懶了：直接把穩態條件 $\omega = u$ 代進去。現在把它當成**約束**正式處理：
- 成本：$L(\omega, u) = \tfrac12(\omega - \omega_{\text{ref}})^2 + \tfrac12 r u^2$
- 約束（穩態 $\dot\omega = 0$）：$f(\omega, u) = -\omega + u = 0$
- 這裡 $\omega$ 扮演 $x$ 的角色，$u$ 還是控制

**Step 1：寫 Hamiltonian**
$$H = \tfrac12(\omega - \omega_{\text{ref}})^2 + \tfrac12 r u^2 + \lambda(-\omega + u)$$

**Step 2：三兄弟**
$$\frac{\partial H}{\partial \lambda} = -\omega + u = 0 \;\Rightarrow\; \omega = u \qquad(\text{就是約束本身})$$
$$\frac{\partial H}{\partial \omega} = (\omega - \omega_{\text{ref}}) - \lambda = 0 \;\Rightarrow\; \lambda = \omega - \omega_{\text{ref}}$$
$$\frac{\partial H}{\partial u} = r u + \lambda = 0 \;\Rightarrow\; \lambda = -r u$$

**Step 3：解聯立**
後兩條的 $\lambda$ 相等：$\omega - \omega_{\text{ref}} = -ru$，再代入 $\omega = u$：
$$u(1 + r) = \omega_{\text{ref}} \;\Rightarrow\; \boxed{u^* = \frac{\omega_{\text{ref}}}{1+r}}, \qquad \lambda^* = -\frac{r\,\omega_{\text{ref}}}{1+r}$$
**跟 §1.1 答案一模一樣** ✓，而且還多拿到一個 $\lambda^*$。

**代數字**：$\omega_{\text{ref}} = 10$、$r = 1$
- $u^* = 5$、$\omega^* = 5$、$\lambda^* = -5$
- 最小成本：把 $\omega^*, u^*$ 代回成本函數 $L$，記作 $L^* = L(\omega^*, u^*) = \tfrac12(5-10)^2 + \tfrac12\cdot 5^2 = 25$

**$\lambda$ 是「價格」的實際意思**：假設馬達多了一個固定負載 $c$，穩態約束變成 $-\omega + u = c$（也就是 $\omega = u - c$，同樣電壓轉得比較慢）。重新求最小成本會得到
$$L^*(c) = \frac{(10 + c)^2}{4}$$
- $c = 0$：$L^* = 25$（跟上面一樣）
- $c = 1$：$L^* = 30.25$，多了約 5
- 導數：$\dfrac{dL^*}{dc}\Big\rvert_{c=0} = 5 = -\lambda^*$

也就是說，**約束每改一單位，最小成本就變 $\lvert\lambda^*\rvert$ 這麼多**（正負號看約束怎麼寫，這裡是 $dL^*/dc = -\lambda^*$）。$\lambda$ 不只是解題工具，它本身就帶著「這條約束有多貴」的資訊。

**既然直接代入就能解，為什麼要學 Lagrange？**
- 這個例子的約束很簡單，可以直接解出 $\omega = u$。但很多約束解不出來（例如非線性），Lagrange 不需要先解約束
- 到了 Ch 2、Ch 3，**每一個時間點**都有一條約束（狀態方程 $x_{k+1} = f(x_k, u_k)$），根本不可能一一代入。這時每個時間點配一個 $\lambda_k$，就是 **costate**，而三兄弟就變成 Ch 2 那張「狀態方程、共態方程、駐點條件」的表

### 1.3 第一章統整

**兩種問題、兩套做法：**

| | 無約束（§1.1） | 有約束（§1.2） |
|---|---|---|
| 問題 | 最小化 $L(u)$ | 最小化 $L(x, u)$，且 $f(x, u) = 0$ |
| 做法 | 直接微分 | 先寫 $H = L + \lambda^T f$，再微分 |
| 必要條件 | $L_u = 0$ | $H_\lambda = 0$（約束）、$H_x = 0$、$H_u = 0$ |
| 充分條件 | $L_{uu} > 0$ | （沿約束方向的）二階條件 $> 0$ |

**解題 SOP（有約束時）：**
1. 把約束移項成 $f(x, u) = 0$
2. 寫 Hamiltonian $H = L + \lambda^T f$
3. 寫三兄弟：$H_\lambda = 0$、$H_x = 0$、$H_u = 0$
4. 解聯立，得到 $x^*, u^*, \lambda^*$

**三個關鍵觀念：**
- **$\lambda$ 的作用**：把被約束綁住的 $dx$ 消掉，讓有約束的問題變回「每個變數各自微分 $= 0$」
- **$\lambda$ 的意義**：約束的**價格**——約束改一單位，最小成本變 $\lvert\lambda^*\rvert$（馬達例：多一單位負載，成本多約 5）
- **trade-off**：成本裡的權重 $r$ 決定「追目標」和「省電」誰比較重要（馬達例：$u^* = \omega_{\text{ref}}/(1+r)$）

**馬達例子的答案（兩種做法一樣）：** $u^* = \dfrac{\omega_{\text{ref}}}{1+r}$、$\lambda^* = -\dfrac{r\,\omega_{\text{ref}}}{1+r}$

**往後怎麼用：** Ch 2、3 的約束變成「每個時間點的狀態方程」，每個時間點配一個 $\lambda_k$（costate）。三兄弟會變成：
- $H_\lambda = 0$ → **狀態方程**（順著時間算，$k$ 由小到大）
- $H_x = 0$ → **共態方程**（逆著時間算，$k$ 由大到小；因為時間耦合，這條不再是 $= 0$，而是 $\lambda_k = \partial H^k / \partial x_k$）
- $H_u = 0$ → **駐點條件**（決定 $u_k^*$）

---

## 二、Lewis Ch 2：離散時間最佳控制

### 大意：從 Ch 1 到 Ch 2 多了什麼？

Ch 1 只做**一次**決定。Ch 2 要**連續做 $N$ 次決定**：在每個時間點 $k = 0, 1, \dots, N-1$ 都選一個控制 $u_k$。

麻煩的地方是**每次決定都會影響未來**：
$$x_0 \xrightarrow{u_0} x_1 \xrightarrow{u_1} x_2 \xrightarrow{u_2} \cdots \xrightarrow{u_{N-1}} x_N$$
$u_0$ 不只影響 $x_1$，還會透過 $x_1$ 影響 $x_2, x_3, \dots$ 一路到最後。所以不能每一步只顧眼前，要**整段一起考慮**。

好消息：**工具完全沿用 Ch 1**（Hamiltonian、Lagrange multiplier、對 $u$ 微分 $= 0$），只是約束從「一條」變成「每個時間點各一條」。

| | Ch 1 | Ch 2 |
|---|---|---|
| 決定幾次 | 1 次 | $N$ 次（$u_0, \dots, u_{N-1}$） |
| 約束 | 1 條 $f(x, u) = 0$ | 每步 1 條：$x_{k+1} = f(x_k, u_k)$ |
| $\lambda$ | 1 個 | 每步 1 個：$\lambda_1, \dots, \lambda_N$（叫 **costate**） |

### 2.1 一般問題

#### 2.1.1 問題長什麼樣

- **系統**：$x_{k+1} = f(x_k, u_k)$，$x_0$ 已知
- **成本**（總開銷 = 沿路每步的開銷 + 最後結算一筆）：
$$J = \underbrace{\phi(x_N)}_{\text{終點成本}} + \sum_{k=0}^{N-1} \underbrace{L(x_k, u_k)}_{\text{每一步的成本}}$$
- **目標**：選 $u_0, \dots, u_{N-1}$ 讓 $J$ 最小

（$J$ 就是 0.5 提過的「總成本」代號，從這章開始正式使用。課本寫成 $J_i$，表示「從時間 $i$ 開始算」，我們一律從 $0$ 開始。）

**$N$（總共幾步）是誰決定的？** 也是**你**，它是問題定義的一部分（Lewis Ch 2 都假設 $N$ 固定、事先給定）。三種常見情況：

| 情況 | $N$ 怎麼來 | 例子 |
|---|---|---|
| 任務有**截止時間** | 截止時間 ÷ 取樣時間 | 「2 秒內讓馬達停下」，每 0.1 秒控制一次 → $N = 20$ |
| **沒有終點**，要一直穩住 | 取 $N \to \infty$，直接用常數 $K_\infty$（2.2.5），不用選 $N$ | 讓馬達一直維持在某個轉速 |
| **越快越好** | $N$ 本身就是要最小化的東西，成本取 $J = N$ | 最短時間問題（Lewis Ex 2.1-1a；Żak Ch 5 的 bang-bang） |

「在 $N$ 步內一定要到終點」可以用**終點固定** $x_N = r_N$（硬性），或用很大的終點成本 $\phi$（軟性，見下）。

**終點成本 $\phi$ 是做什麼的？**

$\phi$ **不是物理上真的要付的錢，是你自己加的「要求」**：你在不在意最後停在哪裡。成本本來就是設計者選的（Lewis：系統由物理決定，成本由你決定）。

- **為什麼需要它**：注意總和只加到 $N-1$，所以最後的狀態 $x_N$ **完全沒被算進 $L$**。如果你在意 $x_N$，只能靠 $\phi$
- **生活例子**：開車到目的地，「路上花多少油」是 $L$；「最後有沒有停在車位裡」是 $\phi$。只算 $L$ 的話，最省油的做法可能是停在離車位 10 公尺的地方
- **不在意就設 $\phi = 0$**，完全合法（2.1.4 就是這樣）

**有沒有 $\phi$ 差很多**：馬達例子最後一步 $\omega_2 = (0.9 - 0.1K_1)\,\omega_1$，終點權重 $\phi = \tfrac12 s\,\omega_2^2$ 取不同的 $s$：

| $s$ | 0 | 1 | 10 | 100 | $\to \infty$ |
|---|---|---|---|---|---|
| $K_1$ | 0 | 0.089 | 0.818 | 4.5 | $\to 9$ |
| $\omega_2 / \omega_1$ | 0.9 | 0.891 | 0.818 | 0.45 | $\to 0$ |

- $s = 0$：最後一步**完全放棄**（$u_1 = 0$），因為 $\omega_2$ 不管多大都不用付錢——這就是 2.1.4 的 $u_1^* = 0$
- $s$ 越大，越用力在最後把轉速壓到 0
- $s \to \infty$：等於**硬性規定** $\omega_2 = 0$，也就是 2.1.2 Step 3 的「終點固定」。所以終點成本可以看成「終點固定」的**軟性版本**：不強制，但偏離要付錢

**馬達版本**（本章主例子）：$\omega_{k+1} = 0.9\,\omega_k + 0.1\,u_k$，$N = 2$，
$$J = \tfrac12 \sum_{k=0}^{1}(\omega_k^2 + u_k^2)$$
意思是：每一步都希望轉速小（$\omega_k^2$）、電壓也小（$u_k^2$）；沒有終點成本（$\phi = 0$）。

#### 2.1.2 解法：每個時間點配一個 $\lambda$

**Step 1：每一步寫一個 Hamiltonian**
$$H^k = L(x_k, u_k) + \lambda_{k+1}^T f(x_k, u_k)$$
- 上標 $k$ 表示「第 $k$ 步的」Hamiltonian，不是次方
- 為什麼配 $\lambda_{k+1}$ 而不是 $\lambda_k$？因為第 $k$ 步的約束是「產生 $x_{k+1}$」的那條，所以它的價格標成 $k+1$。課本也說這是「事後諸葛」的選擇，只是讓公式比較整齊

**Step 2：三個條件（每一步都要滿足）**

| 條件 | 寫開來 | 名稱 | 方向 |
|---|---|---|---|
| $x_{k+1} = \dfrac{\partial H^k}{\partial \lambda_{k+1}}$ | $x_{k+1} = f(x_k, u_k)$ | 狀態方程 | 從 $x_0$ **順著時間**算（$k = 0 \to N$） |
| $\lambda_k = \dfrac{\partial H^k}{\partial x_k}$ | $\lambda_k = \left(\dfrac{\partial f}{\partial x_k}\right)^T \lambda_{k+1} + \dfrac{\partial L}{\partial x_k}$ | 共態方程 | 從 $\lambda_N$ **逆著時間**算（$k = N \to 0$） |
| $0 = \dfrac{\partial H^k}{\partial u_k}$ | $0 = \left(\dfrac{\partial f}{\partial u_k}\right)^T \lambda_{k+1} + \dfrac{\partial L}{\partial u_k}$ | 駐點條件 | 每步解出 $u_k$ |

> **「順著時間」和「逆著時間」是什麼？**
> - **順著時間**：$k$ 由小到大，$k = 0 \to 1 \to 2 \to \cdots \to N$，跟真實時間流動同方向。狀態方程用「現在」算「下一步」：知道 $x_0$ 就能算 $x_1$，再算 $x_2$……
> - **逆著時間**：$k$ 由大到小，$k = N \to N-1 \to \cdots \to 0$。共態方程用「下一步」算「現在」：$\lambda_k$ 要用 $\lambda_{k+1}$ 算，所以必須先知道**最後**的 $\lambda_N$，再一路算回 $\lambda_{N-1}, \lambda_{N-2}, \dots$
> - **怎麼看出方向**：看等號左邊是誰。$x_{k+1} = f(x_k, \dots)$ 左邊是較晚的 → 順著時間；$\lambda_k = (\cdots)\lambda_{k+1} + \cdots$ 左邊是較早的 → 逆著時間
> - 馬達例（2.1.4）：$\omega_0 = 10 \to \omega_1 \to \omega_2$ 是順著時間；$\lambda_2 = 0 \to \lambda_1$ 是逆著時間

**為什麼 $\lambda_k$ 一定要逆著時間算？**

關鍵在 $\lambda_k$ 的意義（§1.2：$\lambda$ 是價格）：
$$\lambda_k = \text{「如果 } x_k \text{ 多一單位，從第 } k \text{ 步到結束的總成本會多多少」}$$

**「現在的狀態值多少」取決於「它將來會造成什麼」**——就像一張股票現在值多少，要看它未來能賺多少。所以要算 $\lambda_k$，得先知道**後面**的事。

**用連鎖律拆開**：$x_k$ 多一單位，會從兩條路影響總成本：
1. **這一步馬上付的**：第 $k$ 步的成本 $L$ 變多 $\dfrac{\partial L}{\partial x_k}$
2. **傳給下一步的**：$x_{k+1}$ 會跟著變 $\dfrac{\partial f}{\partial x_k}$ 單位，而 $x_{k+1}$ 每一單位的價格是 $\lambda_{k+1}$

加起來：
$$\lambda_k = \underbrace{\frac{\partial L}{\partial x_k}}_{\text{這一步付的}} + \underbrace{\left(\frac{\partial f}{\partial x_k}\right)^T \lambda_{k+1}}_{\text{傳到下一步的代價}}$$
這**就是共態方程**。算 $\lambda_k$ 需要 $\lambda_{k+1}$，算 $\lambda_{k+1}$ 需要 $\lambda_{k+2}$……一路追到最後。

**最後一步的價格是直接知道的**：到了終點 $N$，後面沒有下一步了，只剩終點成本 $\phi$，所以 $\lambda_N = \dfrac{\partial\phi}{\partial x_N}$。這就是逆著時間的起點。

**對照：**

| | 狀態 $x_k$ | 共態 $\lambda_k$ |
|---|---|---|
| 意義 | 系統現在在哪 | 現在的狀態值多少錢 |
| 由什麼決定 | **過去**（上一步在哪、做了什麼） | **未來**（之後會造成多少成本） |
| 已知的一端 | 起點 $x_0$ | 終點 $\lambda_N$ |
| 計算方向 | 順著時間 | 逆著時間 |

**馬達例子實際看**（$\omega_0 = 10$、$\phi = 0$，接 2.1.4 的結果）：
- $\lambda_2 = 0$：終點沒有成本，$\omega_2$ 多一單位不用付錢
- $\lambda_1 = \underbrace{\omega_1}_{\tfrac12\omega_1^2 \text{ 的斜率}} + 0.9 \times \underbrace{\lambda_2}_{0} = 8.911$：$\omega_1$ 多一單位，這一步多付 8.911，傳給 $\omega_2$ 的 0.9 單位不用錢
- $\lambda_0 = \omega_0 + 0.9 \times \lambda_1 = 10 + 0.9 \times 8.911 = 18.02$：$\omega_0$ 多一單位，這一步多付 10，還有 0.9 單位傳到 $\omega_1$，每單位值 8.911
- 驗算：$J^* = \tfrac12 S_0\,\omega_0^2$，對 $\omega_0$ 微分 $= S_0\,\omega_0 = 1.802 \times 10 = 18.02$ ✓ 正是 $\lambda_0$

**這也解釋了為什麼 $u_k$ 要靠 $\lambda_{k+1}$**：做決定時要知道「下一步的狀態值多少錢」，才能判斷現在花電去改變它划不划算。而這個價格來自未來——所以才會出現「$x$ 從頭算、$\lambda$ 從尾算」的兩點邊值問題。

**所以共態 (costate) 到底是什麼？三個角度：**

| 角度 | 共態 $\lambda_k$ 是… |
|---|---|
| **身份**（怎麼來的） | 第 $k-1$ 步那條約束（狀態方程）的 Lagrange multiplier。每個時間點一個，所以排起來變成一串 $\lambda_1, \dots, \lambda_N$ |
| **意義**（代表什麼） | 狀態的**價格**：$x_k$ 多一單位，剩下的最小成本多多少。（經濟學叫「影子價格 shadow price」） |
| **行為**（怎麼算） | 有自己的「動態方程」（共態方程），像狀態一樣一步一步演化，只是方向相反 |

**為什麼叫「共態」？**
- **co- 的意思是「搭檔、對偶」**（數學裡 cosine、covector 的 co- 都是這個意思）。共態是狀態的**搭檔**：維度跟 $x_k$ 一樣（$x$ 有 $n$ 個分量，$\lambda$ 也有 $n$ 個），每個狀態分量都配一個自己的價格
- 課本（Lewis）的說法：這個原本只是「虛構的」Lagrange multiplier，結果竟然有自己的動態方程，所以乾脆把它當成系統的另一組變數，稱為 **costate**，它的方程稱為 **adjoint system（伴隨系統）**
- **「對偶」的直覺**：$\lambda^T dx$ 是一個**數字**（狀態變了 $dx$，成本變多少）。狀態描述「系統在哪」，共態把「狀態的變化」翻譯成「成本的變化」

**名字來自物理（選讀）**：Hamiltonian 這個名字來自古典力學。力學裡描述系統要兩組變數：**位置** $q$ 和**動量** $p$，它們滿足
$$\dot q = \frac{\partial H}{\partial p}, \qquad \dot p = -\frac{\partial H}{\partial q}$$
跟 Ch 3 的連續時間條件 $\dot x = \dfrac{\partial H}{\partial \lambda}$、$\dot\lambda = -\dfrac{\partial H}{\partial x}$ **一模一樣**。所以狀態 $x$ 對應位置、共態 $\lambda$ 對應動量——共態就是最佳控制裡的「動量」。

**實用上**：課本也說「我們其實不在乎 $\lambda$ 是多少，但這個方法必須先算出它，才能得到最佳控制」。$\lambda$ 是中間工具；LQR 的 $\lambda_k = S_k x_k$ 就是把它消掉的方法。

**跟 Ch 1 對照**：第一條、第三條跟 Ch 1 一模一樣。**第二條不一樣**：Ch 1 是 $H_x = 0$，這裡是 $H_x = \lambda_k$。為什麼？

因為 $x_k$ 在**兩個地方**出現：
1. 它是第 $k$ 步的起點 → 出現在 $H^k$ 裡
2. 它是第 $k-1$ 步約束的「結果」→ 出現在 $\lambda_k^T(f(x_{k-1}, u_{k-1}) - x_k)$ 這一項，貢獻 $-\lambda_k$

兩個加起來對 $x_k$ 微分 $= 0$：$\dfrac{\partial H^k}{\partial x_k} - \lambda_k = 0$，就是共態方程。**多出來的 $\lambda_k$ 就是「時間把前後兩步綁在一起」的痕跡。**

**Step 3：邊界條件（頭尾怎麼處理）**
- **起點**：$x_0$ 已知，直接用
- **終點 $x_N$ 自由**（沒規定一定要到哪）→ $\lambda_N = \dfrac{\partial \phi}{\partial x_N}$
  - 直覺：$\lambda_N$ 是「終點狀態的價格」，而終點狀態只出現在 $\phi$ 裡，所以價格就是 $\phi$ 的斜率
  - 沒有終點成本（$\phi = 0$）→ $\lambda_N = 0$
- **終點 $x_N$ 固定**（一定要到 $r_N$）→ 直接用 $x_N = r_N$ 當條件，$\lambda_N$ 變成未知數去解

#### 2.1.3 為什麼難解：兩點邊值問題

整理一下手上有的資訊：
- 狀態 $x$：知道**起點** $x_0$，狀態方程**順著時間**推（$x_0 \to x_1 \to \cdots$）
- 共態 $\lambda$：知道**終點** $\lambda_N$，共態方程**逆著時間**推（$\lambda_N \to \lambda_{N-1} \to \cdots$）
- 但兩者互相需要：順著推 $x$ 要知道 $u_k$，而 $u_k$ 要靠 $\lambda_{k+1}$；逆著推 $\lambda$ 又要知道 $x_k$

$$\underbrace{x_0}_{\text{已知}} \longrightarrow x_1 \longrightarrow \cdots \longrightarrow x_N \qquad \lambda_1 \longleftarrow \cdots \longleftarrow \lambda_{N-1} \longleftarrow \underbrace{\lambda_N}_{\text{已知}}$$

條件分散在**頭和尾兩端**，沒辦法單純從一邊一路算到底——這就叫**兩點邊值問題 (two-point boundary-value problem, TPBVP)**。一般只能**解聯立**。2.2 的 LQR 會給一個漂亮的破解法。

#### 2.1.4 馬達例子：實際解一次

$\omega_{k+1} = 0.9\,\omega_k + 0.1\,u_k$，$J = \tfrac12\sum_{k=0}^{1}(\omega_k^2 + u_k^2)$，$N = 2$

**Step 1：Hamiltonian**
$$H^k = \tfrac12(\omega_k^2 + u_k^2) + \lambda_{k+1}(0.9\,\omega_k + 0.1\,u_k)$$

**Step 2：三個條件**
- 狀態：$\omega_{k+1} = 0.9\,\omega_k + 0.1\,u_k$
- 共態：$\lambda_k = \dfrac{\partial H^k}{\partial \omega_k} = \omega_k + 0.9\,\lambda_{k+1}$
- 駐點：$0 = \dfrac{\partial H^k}{\partial u_k} = u_k + 0.1\,\lambda_{k+1} \;\Rightarrow\; u_k = -0.1\,\lambda_{k+1}$

**Step 3：邊界**：$\phi = 0$、終點自由 → $\lambda_2 = 0$

**Step 4：從尾巴逆著時間解**（$k = 1$ 先，再 $k = 0$）
- $k = 1$：$u_1 = -0.1\,\lambda_2 = 0$
  - 很合理：$u_1$ 只會影響 $\omega_2$，但成本根本不算 $\omega_2$，花電也沒好處
- $\lambda_1 = \omega_1 + 0.9 \cdot 0 = \omega_1$
- $k = 0$：$u_0 = -0.1\,\lambda_1 = -0.1\,\omega_1$

**Step 5：解聯立（兩點邊值的「會合」）**
$u_0$ 需要 $\omega_1$，但 $\omega_1$ 又由 $u_0$ 決定：
$$\omega_1 = 0.9\,\omega_0 + 0.1\,u_0 = 0.9\,\omega_0 - 0.01\,\omega_1 \;\Rightarrow\; \omega_1 = \frac{0.9}{1.01}\,\omega_0$$
代回：
$$\boxed{u_0^* = -\frac{0.09}{1.01}\,\omega_0 \approx -0.0891\,\omega_0, \qquad u_1^* = 0}$$

**代數字**（$\omega_0 = 10$）：$u_0^* = -0.891$、$\omega_1 = 8.911$、$u_1^* = 0$、$\omega_2 = 8.020$
$$J^* = \tfrac12(10^2 + 0.891^2 + 8.911^2 + 0^2) \approx 90.1$$

**$\lambda$ 的意義又出現了**：$\lambda_1 = \omega_1$，意思是「$\omega_1$ 多一單位，剩下的成本多 $\omega_1$」——剛好就是 $\tfrac12\omega_1^2$ 的斜率。$\lambda_k$ 就是「第 $k$ 步狀態的價格」。

### 2.2 離散 LQR：本章最重要

#### 2.2.1 設定

「LQR」= **L**inear **Q**uadratic **R**egulator：系統是**線性**的、成本是**二次**的、目標是把狀態**調節**到 0。這是最經典的最佳控制問題。

- 系統：$x_{k+1} = A x_k + B u_k$
- 成本：
$$J = \tfrac{1}{2} x_N^T S_N x_N + \tfrac{1}{2}\sum_{k=0}^{N-1}(x_k^T Q x_k + u_k^T R u_k)$$

| 權重 | 要求 | 調大代表 |
|---|---|---|
| $Q$ | $\ge 0$ | 更在意「過程中的狀態」要小 |
| $R$ | $> 0$ | 更在意「電壓/控制」要小（必須正定，因為要算 $R^{-1}$） |
| $S_N$ | $\ge 0$ | 更在意「終點狀態」要小 |

2.1.4 的馬達例子就是 LQR：$A = 0.9$、$B = 0.1$、$Q = 1$、$R = 1$、$S_N = 0$。

#### 2.2.2 關鍵想法：猜 $\lambda_k = S_k x_k$

2.1.4 最麻煩的是 Step 5 解聯立。$N = 2$ 還好，$N = 100$ 就很痛苦。

**「痛苦」具體是什麼？全部要一起解。** 以 scalar 馬達、$N = 100$ 為例：

| 未知數 | 個數 | 對應的方程 | 個數 |
|---|---|---|---|
| $\omega_1, \dots, \omega_{100}$ | 100 | 狀態方程 | 100 |
| $\lambda_1, \dots, \lambda_{100}$ | 100 | 共態方程 99 條 + 邊界 $\lambda_{100} = 0$ | 100 |
| $u_0, \dots, u_{99}$ | 100 | 駐點條件 | 100 |

**300 個未知數、300 條方程，而且不能拆開一步一步解。** 為什麼？想從 $\omega_0$ 順著時間算出 $\omega_1$，需要 $u_0$；$u_0$ 要靠 $\lambda_1$；把共態方程展開，
$$\lambda_1 = \omega_1 + 0.9\,\omega_2 + 0.9^2\,\omega_3 + \cdots + 0.9^{98}\,\omega_{99}$$
$\lambda_1$ 竟然要用到**所有未來的轉速**，而那些轉速又要靠 $u_0$ 才算得出來——整段時間繞成一個圈，所以只能 300 條一起解。

$N = 2$ 時剛好運氣好：$\lambda_2 = 0$，所以 $\lambda_1 = \omega_1$，圈很小，只剩一條方程要解。

（一般做法：線性問題可以交給電腦解大型聯立；非線性問題常用「打靶法 (shooting)」——先猜一個 $\lambda$ 初值，順著算到終點，看邊界條件差多少再修正猜測。手算都很痛苦。）

**LQR 的做法正是「每個相鄰時間分開解，共 $N$ 次」：** 猜 $\lambda_k = S_k x_k$ 之後，「價格」不再需要知道未來的**狀態**，只需要知道下一步的**矩陣** $S_{k+1}$。於是那個圈被切斷，300 條聯立變成：
- 逆著時間：$S_{100} \to S_{99} \to \cdots \to S_0$，每一步一條公式，共 100 次
- 順著時間：$x_0 \to x_1 \to \cdots \to x_{100}$，每一步 $u_k = -K_k x_k$，共 100 次

**觀察**：2.1.4 裡 $\lambda_1 = \omega_1$，**共態跟狀態成正比**。LQR 的成本是二次的，「價格」（斜率）就會是線性的——就像 $\tfrac12 s x^2$ 的斜率是 $s x$。所以大膽猜：
$$\boxed{\lambda_k = S_k\, x_k}$$
（$S_k$ 是一個待定的矩陣。終點時 $\lambda_N = \partial\phi/\partial x_N = S_N x_N$，猜法在終點成立 ✓）

**代入駐點條件**：LQR 的駐點條件是 $0 = R u_k + B^T \lambda_{k+1}$（用 0.5 的微分表），代入猜測：
$$R u_k = -B^T S_{k+1} x_{k+1} = -B^T S_{k+1}(A x_k + B u_k)$$
把 $u_k$ 移到同一邊：
$$(B^T S_{k+1} B + R)\, u_k = -B^T S_{k+1} A\, x_k$$
$$\boxed{u_k^* = -K_k x_k, \qquad K_k = (B^T S_{k+1} B + R)^{-1} B^T S_{k+1} A}$$

**最佳控制是「現在的狀態 × 一個增益」！** 不用解聯立，而且是**回授 (feedback)**：量到現在的 $x_k$ 就能算出 $u_k$。（2.1.4 的解法算出來的是一串事先排好的 $u_k$，叫**開迴路 (open-loop)**，遇到干擾就不會修正。）

**代入共態方程**：LQR 的共態方程是 $\lambda_k = Q x_k + A^T \lambda_{k+1}$，代入猜測和 $x_{k+1} = (A - BK_k)x_k$：
$$S_k x_k = Q x_k + A^T S_{k+1}(A - B K_k)\, x_k$$
對所有 $x_k$ 都成立，所以：
$$\boxed{S_k = A^T S_{k+1}(A - B K_k) + Q}$$
這就是**離散 Riccati 方程**。把 $K_k$ 代進去展開，就是課本的樣子：
$$S_k = A^T S_{k+1} A - A^T S_{k+1} B (B^T S_{k+1} B + R)^{-1} B^T S_{k+1} A + Q$$
（考試寫哪個都可以，**上面那個比較好算**。）

**最佳成本**：$J^* = \tfrac{1}{2} x_0^T S_0 x_0$

#### 2.2.3 LQR 解題 SOP

1. **逆著時間算（離線）**：從 $S_N$ 開始，$k = N-1, N-2, \dots, 0$，每一步：
   - 先算 $K_k = (B^T S_{k+1} B + R)^{-1} B^T S_{k+1} A$
   - 再算 $S_k = A^T S_{k+1}(A - B K_k) + Q$
2. **順著時間跑（線上）**：從 $x_0$ 開始，每一步 $u_k = -K_k x_k$，$x_{k+1} = A x_k + B u_k$

**為什麼實用？** $S_k$、$K_k$ 只依賴 $A, B, Q, R, S_N$，跟 $x_0$ 無關，可以**事先算好**存起來；執行時每步只做一次乘法。兩點邊值問題被拆成「先全部逆著時間算 $S, K$、再全部順著時間跑 $x, u$」兩段，各自都很好算。

#### 2.2.4 馬達例子：用 Riccati 重做 2.1.4

$A = 0.9$、$B = 0.1$、$Q = R = 1$、$S_2 = 0$。scalar 版公式：
$$K_k = \frac{0.1 \cdot S_{k+1} \cdot 0.9}{0.01\, S_{k+1} + 1}, \qquad S_k = 0.9\, S_{k+1}(0.9 - 0.1\, K_k) + 1$$

| $k$ | $S_{k+1}$ | $K_k$ | $S_k$ |
|---|---|---|---|
| 1 | $S_2 = 0$ | $0$ | $0 + 1 = 1$ |
| 0 | $S_1 = 1$ | $\dfrac{0.09}{1.01} \approx 0.0891$ | $0.9 \cdot 1 \cdot (0.9 - 0.00891) + 1 \approx 1.802$ |

**跟 2.1.4 對答案：**
- $K_1 = 0$ ↔ $u_1^* = 0$ ✓
- $K_0 = 0.0891$ ↔ $u_0^* = -0.0891\,\omega_0$ ✓
- $J^* = \tfrac12 S_0\,\omega_0^2 = \tfrac12 \cdot 1.802 \cdot 100 \approx 90.1$ ✓

**同一個答案，但這次完全不用解聯立。**

#### 2.2.5 如果 $N$ 很大？增益會收斂

同一個馬達，把 $N$ 拉長，看「距離終點還剩 $j$ 步」時的增益：

| 剩幾步 $j$ | 1 | 2 | 3 | 5 | 10 | 20 | 30 | $\infty$ |
|---|---|---|---|---|---|---|---|---|
| $K$ | 0 | 0.089 | 0.159 | 0.256 | 0.354 | 0.382 | 0.384 | **0.384** |
| $S$ | 1 | 1.80 | 2.43 | 3.30 | 4.18 | 4.44 | 4.45 | **4.45** |

**$S_N$ 選不同值，最後都收斂到同一個 $K_\infty$**（同一個馬達）：

| 剩幾步 $j$ | 1 | 2 | 5 | 10 | 20 | 30 |
|---|---|---|---|---|---|---|
| $S_N = 0$ | 0 | 0.089 | 0.256 | 0.354 | 0.382 | 0.384 |
| $S_N = 10$ | 0.818 | 0.695 | 0.504 | 0.410 | 0.385 | 0.384 |
| $S_N = 100$ | 4.5 | 2.64 | 1.02 | 0.507 | 0.390 | 0.384 |

$S_N$ 只影響「快到終點那幾步」的增益；離終點夠遠時，$K$ 由 $A, B, Q, R$ 決定，跟 $S_N$ 無關。

- 離終點很遠時，$K$ 幾乎是**常數**。課本 §2.4 的「穩態 (steady-state)」就是直接用這個常數 $K_\infty$，實作更簡單
- 常數 $S_\infty$ 滿足 $S = A^T S (A - BK) + Q$（令 $S_k = S_{k+1}$），叫**離散代數 Riccati 方程 (DARE)**。馬達：$s^2 + 18s - 100 = 0 \Rightarrow s \approx 4.45$
- 閉迴路 $\omega_{k+1} = (0.9 - 0.1 \cdot 0.384)\,\omega_k = 0.862\,\omega_k$，$\lvert 0.862 \rvert < 1$ → 穩定（0.3.2 的離散判準），而且比不控制（0.9）收斂得快

### 2.3 第二章統整

**一般問題的 SOP：**
1. 寫每一步的 $H^k = L + \lambda_{k+1}^T f$
2. 三個條件：狀態方程（順著時間）、共態方程 $\lambda_k = \partial H^k/\partial x_k$（逆著時間）、駐點條件 $\partial H^k/\partial u_k = 0$
3. 邊界：$x_0$ 已知；終點自由 → $\lambda_N = \partial\phi/\partial x_N$；終點固定 → $x_N = r_N$
4. 解聯立（兩點邊值問題）

**LQR 的 SOP：**
1. 從 $S_N$ 逆著時間算 $K_k$、$S_k$（Riccati）
2. 順著時間跑 $u_k = -K_k x_k$
3. 最佳成本 $J^* = \tfrac12 x_0^T S_0 x_0$

**什麼時候用哪一套？**（LQR **不能**取代一般 SOP）

LQR 的「猜 $\lambda_k = S_k x_k$」只有在**線性系統 + 二次成本**時才成立。其他情況都要回到一般 SOP：

| 情況 | 例子 | 用哪套 |
|---|---|---|
| 線性系統 + 二次成本 + 終點自由 | 本章馬達例子 | **LQR**（Riccati） |
| 終點固定 $x_N = r_N$ | Lewis Ex 2.1-2a（最小能量到指定終點） | 一般 SOP |
| 非線性系統 | $x_{k+1} = x_k^2 + u_k$ | 一般 SOP |
| 非二次成本 | 最省油 $\sum \lvert u_k\rvert$、最短時間 $J = N$ | 一般 SOP |
| 控制有上下限 $\lvert u\rvert \le 1$ | bang-bang | 一般 SOP 的延伸（Żak Ch 5 PMP） |

而且：
- **LQR 本身就是從一般 SOP 推出來的**（2.2.2 用的就是那三個條件），不會一般 SOP 就推不出 Riccati
- 常考題型「給 scalar 系統 + 成本，寫 $H$、共態、解 $u^*$」考的就是一般 SOP
- Ch 3（連續時間）、Żak Ch 5（PMP）用的都是同一套三條件，只是換成連續版

**關鍵觀念：**
- **共態方程比 Ch 1 多一個 $\lambda_k$**：因為 $x_k$ 同時是上一步的結果、下一步的起點
- **兩點邊值**：$x$ 的條件在頭、$\lambda$ 的條件在尾，一般要解聯立
- **LQR 的破解法**：猜 $\lambda_k = S_k x_k$ → 最佳控制變成回授 $u_k = -K_k x_k$，Riccati 逆著時間算就好
- **$N \to \infty$**：$K_k$ 收斂成常數 $K_\infty$，對應 DARE；閉迴路特徵值在單位圓內

---

## 三、Lewis Ch 3：連續時間最佳控制

### 大意：從 Ch 2 到 Ch 3 多了什麼？

Ch 2 每隔一段時間（馬達例子是 0.1 秒）才做一次決定。但真實的馬達、飛機、溫度都是**連續**在變的，控制也可以隨時調整。Ch 3 就是把 Ch 2 的時間格子**切到無限細**。

**好消息：故事完全一樣**，只是換符號：

| | Ch 2（離散） | Ch 3（連續） |
|---|---|---|
| 時間 | $k = 0, 1, \dots, N$ | $t$ 從 $t_0$ 連續走到 $T$ |
| 系統 | $x_{k+1} = f(x_k, u_k)$ | $\dot x = f(x, u, t)$ |
| 成本 | $\phi(x_N) + \sum L$ | $\phi(x(T)) + \int L\, dt$ |
| 控制 | 一串數字 $u_0, \dots, u_{N-1}$ | 一條曲線 $u(t)$ |
| 共態 | 一串數字 $\lambda_1, \dots, \lambda_N$ | 一條曲線 $\lambda(t)$ |
| Hamiltonian | $H^k = L + \lambda_{k+1}^T f$ | $H = L + \lambda^T f$ |
| 兩點邊值 | $x_0$ 在頭、$\lambda_N$ 在尾 | $x(t_0)$ 在頭、$\lambda(T)$ 在尾 |
| LQR | Riccati **差分**方程 | Riccati **微分**方程 |
| 穩態 | DARE | ARE |
| 閉迴路穩定 | $\lvert\lambda\rvert < 1$ | $\text{Re}(\lambda) < 0$ |

**核心想法：連續 = 離散的取樣時間 $\Delta t \to 0$。** 本章會一直用這個想法：連續版的每一條公式，都可以從 Ch 2 的公式取極限得到，**不用重新背一套**。

**兩個馬達版本怎麼對應？** Ch 2 的 $\omega_{k+1} = 0.9\,\omega_k + 0.1\,u_k$，就是連續 $\dot\omega = -\omega + u$ 用 $\Delta t = 0.1$ 做 Euler 近似：
$$\omega_{k+1} = \omega_k + \Delta t\,(-\omega_k + u_k) = (1 - \Delta t)\,\omega_k + \Delta t\, u_k$$
成本也要對應：積分 $\int L\, dt \approx \sum L\,\Delta t$，所以每一步的成本應該乘上 $\Delta t$。

（Ch 2 例子的 $Q = R = 1$ 沒有乘 0.1，等於每步的權重都放大了 10 倍。不過 **$Q$、$R$ 同乘一個數不會改變 $K$**，只會讓 $S$ 跟著放大同樣倍數——成本整個乘 10，最佳的 $u$ 不會變。§3.3.5 比較數字時會用到這點。）

### 3.1 變分法 (Calculus of Variations)

Lewis §3.1 很短，只是介紹「對**函數**求極值」的工具：以前是找一個**數字** $u$ 讓成本最小，現在要找一整條**曲線** $u(t)$。完整的推導（Euler-Lagrange 方程）Żak §5.2 講得比較清楚，放在本筆記第八章。

這章只需要知道：連續時間的必要條件，就是對 $x(t)$、$u(t)$、$\lambda(t)$ 這三條曲線**各自要求「微調不會讓成本變小」**。跟 Ch 1 的三兄弟、Ch 2 的三個條件是同一個精神。

### 3.2 一般問題

#### 3.2.1 問題長什麼樣

- **系統**：$\dot x = f(x, u, t)$，$x(t_0)$ 已知
- **成本**：
$$J = \underbrace{\phi(x(T), T)}_{\text{終點成本}} + \int_{t_0}^{T} \underbrace{L(x, u, t)}_{\text{每一瞬間的成本率}}\, dt$$
- **（可選）終點約束**：$\psi(x(T), T) = 0$，例如「終點的位置一定要是 0，速度不管」
- **目標**：選整條控制曲線 $u(t)$（$t_0 \le t \le T$），讓 $J$ 最小

$\phi$ 和 $T$ 的角色跟 Ch 2 的 $\phi$、$N$ 完全一樣（見 2.1.1）。$L$ 現在是**成本率**（每秒付多少），所以要積分。

#### 3.2.2 三個條件

**Hamiltonian**：
$$H(x, u, \lambda, t) = L + \lambda^T f$$
（這次 $\lambda$ 不用標 $k+1$：連續時間裡「這一瞬間」和「下一瞬間」是同一個 $t$。）

| 條件 | 寫開來 | 名稱 | 方向 |
|---|---|---|---|
| $\dot x = \dfrac{\partial H}{\partial \lambda}$ | $\dot x = f$ | 狀態方程 | 從 $x(t_0)$ **順著時間** |
| $-\dot\lambda = \dfrac{\partial H}{\partial x}$ | $-\dot\lambda = \left(\dfrac{\partial f}{\partial x}\right)^T \lambda + \dfrac{\partial L}{\partial x}$ | 共態方程 | 從 $\lambda(T)$ **逆著時間** |
| $0 = \dfrac{\partial H}{\partial u}$ | $0 = \left(\dfrac{\partial f}{\partial u}\right)^T \lambda + \dfrac{\partial L}{\partial u}$ | 駐點條件 | 每一瞬間解出 $u(t)$ |

跟 Ch 2 比：第一條、第三條一模一樣；**第二條多了一個負號**。

#### 3.2.3 負號從哪來？從 Ch 2 取極限

把連續問題切成 $\Delta t$ 的小格子（就像馬達的 0.9 / 0.1 那樣）：
- 系統：$x_{k+1} = x_k + \Delta t\, f(x_k, u_k)$
- 每步成本：$L\,\Delta t$

套 Ch 2 的共態方程 $\lambda_k = \partial H^k / \partial x_k$，其中 $H^k = L\,\Delta t + \lambda_{k+1}^T(x_k + \Delta t\, f)$：
$$\lambda_k = \lambda_{k+1} + \Delta t\left(\frac{\partial L}{\partial x} + \left(\frac{\partial f}{\partial x}\right)^T \lambda_{k+1}\right) = \lambda_{k+1} + \Delta t\, \frac{\partial H}{\partial x}$$
移項、除以 $\Delta t$：
$$\frac{\lambda_{k+1} - \lambda_k}{\Delta t} = -\frac{\partial H}{\partial x} \quad\xrightarrow{\ \Delta t \to 0\ }\quad \dot\lambda = -\frac{\partial H}{\partial x}$$

**負號的意思**：Ch 2 的共態方程是「**舊的 = 新的 + 這一步的代價**」（$\lambda_k$ 比 $\lambda_{k+1}$ 多了這一步的 $\Delta t\, \partial H/\partial x$）。但導數 $\dot\lambda$ 的定義是「**新的 − 舊的**」，方向剛好相反，所以多一個負號。

**白話**：$\lambda$ 是「狀態的價格」，衡量的是「從現在到結束的成本」。時間往前走，這一瞬間的代價付掉了，剩下的就少一點——所以 $\dot\lambda = -(\text{這一瞬間付掉的})$。Ch 2 馬達例子的 $\lambda_0 = 18.02 \to \lambda_1 = 8.91 \to \lambda_2 = 0$ 就是這樣一路變小。

**駐點條件為什麼沒有負號？** $\partial H^k / \partial u_k = \Delta t \left(\partial L/\partial u + (\partial f/\partial u)^T \lambda_{k+1}\right) = 0$，兩邊除以 $\Delta t$ 就是 $\partial H/\partial u = 0$。這條沒有「新減舊」，所以不會多出負號。

> ⚠️ **考試最常錯**：把連續共態方程寫成 $\dot\lambda = +\partial H/\partial x$。
> 記法：跟物理的 Hamilton 方程一樣（2.1.2 選讀）——$\dot q = \partial H/\partial p$、$\dot p = -\partial H/\partial q$。**狀態正號、共態負號。**

#### 3.2.4 邊界條件

跟 Ch 2 的 Step 3 一樣，只是連續時間多了一種情況：**終點時間 $T$ 本身也可以是自由的**。

| 終點情況 | 條件 | 對應 Ch 2 |
|---|---|---|
| $T$ 固定、$x(T)$ 自由 | $\lambda(T) = \dfrac{\partial\phi}{\partial x(T)}$ | $\lambda_N = \partial\phi/\partial x_N$ |
| $T$ 固定、$x(T)$ 固定 $= r$ | $x(T) = r$，$\lambda(T)$ 變成待解的未知數 | $x_N = r_N$ |
| $T$ 固定、$x(T)$ 部分固定 $\psi(x(T)) = 0$ | $\lambda(T) = \dfrac{\partial\phi}{\partial x} + \left(\dfrac{\partial\psi}{\partial x}\right)^T \nu$（$\nu$ 是新的 multiplier） | — |
| $T$ 自由（例如最短時間） | 上面的條件之外，再加 $\left(\dfrac{\partial\phi}{\partial t} + \left(\dfrac{\partial\psi}{\partial t}\right)^T\nu + H\right)\Big\rvert_{t=T} = 0$ | 2.1.1 的「越快越好」 |

課本（Lewis 3.2-10）把這些合成一條：
$$(\phi_x + \psi_x^T \nu - \lambda)^T\big\rvert_T\, dx(T) + (\phi_t + \psi_t^T \nu + H)\big\rvert_T\, dT = 0$$

**讀法**：某個量如果「可以動」（$dx(T) \ne 0$ 或 $dT \ne 0$），它前面的括號就必須 $= 0$；如果它「被固定」（$= 0$），那一項自動消失。上表就是把四種情況代進去的結果，**考試記表就好**。

#### 3.2.5 一個好用的性質：$H$ 沿著最佳軌跡是常數

如果 $f$、$L$ 都**不直接含 $t$**（時不變系統），那沿著最佳解 $H$ 不會變：
$$\frac{dH}{dt} = \frac{\partial H}{\partial t} + \underbrace{\frac{\partial H}{\partial x}\dot x + \frac{\partial H}{\partial \lambda}\dot\lambda}_{= H_x f + f \cdot (-H_x) = 0} + \underbrace{\frac{\partial H}{\partial u}\dot u}_{H_u = 0} = \frac{\partial H}{\partial t} = 0$$
（物理上就是**能量守恆**。）

**用途**：$T$ 自由、$\phi$ 不含 $t$ 時，上表最後一行給 $H(T) = 0$，所以**整段都是 $H(t) = 0$**，多了一條方程可以用。Żak Ch 5 的最短時間（bang-bang）問題會用到。

#### 3.2.6 為什麼還是難：兩點邊值問題

跟 2.1.3 一模一樣：$x$ 知道**頭** $x(t_0)$、$\lambda$ 知道**尾** $\lambda(T)$，兩者又互相需要。差別只是從「$2N$ 條差分方程」變成「$2n$ 條微分方程」，一半條件在頭、一半在尾。

一般解法：
- **線性系統**：常常可以手算解析解（下面 3.2.7 的例子）
- **非線性系統**：數值解，例如**打靶法**——猜 $\lambda(t_0)$，順著時間積分到 $T$，看邊界條件差多少再修正
- **LQR**：用 3.3 的 $\lambda = Sx$ 破解，跟 Ch 2 一樣

#### 3.2.7 馬達例子：最省電加速（Lewis Ex 3.2-3 同型題）

這題跟課本 Ex 3.2-3（用最少能量加熱房間）的數學**一模一樣**，只是把溫度換成轉速。考試很可能出這種題型。

**問題**：馬達從靜止 $\omega(0) = 0$ 出發，要在 $T = 1$ 秒時達到 $\omega_{\text{ref}} = 10$，而且**最省電**：
$$\dot\omega = -\omega + u, \qquad J = \tfrac12 \int_0^1 u^2\, dt$$
（成本只算電，不算轉速——這裡轉速是「目標」，不是「懲罰」。跟 Ch 2 的例子不同。）

**Step 1：Hamiltonian**
$$H = \tfrac12 u^2 + \lambda(-\omega + u)$$

**Step 2：三個條件**
- 狀態：$\dot\omega = -\omega + u$
- 共態：$-\dot\lambda = \dfrac{\partial H}{\partial \omega} = -\lambda \;\Rightarrow\; \dot\lambda = \lambda \;\Rightarrow\; \lambda(t) = \lambda(1)\, e^{t-1}$
- 駐點：$0 = \dfrac{\partial H}{\partial u} = u + \lambda \;\Rightarrow\; u = -\lambda$

**Step 3：用 $\lambda(1)$ 表示一切**
共態方程裡沒有 $\omega$，可以先解（上面已解），只是 $\lambda(1)$ 還不知道。把 $u = -\lambda(1)e^{t-1}$ 代入狀態方程，從 $\omega(0) = 0$ 解出：
$$\omega(t) = -\lambda(1)\, e^{-1} \sinh t \qquad \left(\sinh t = \tfrac{e^t - e^{-t}}{2}\right)$$
（驗算：左邊微分 $= -\lambda(1)e^{-1}\cosh t$；右邊 $-\omega + u = \lambda(1)e^{-1}\sinh t - \lambda(1)e^{-1}e^{t} = -\lambda(1)e^{-1}\cosh t$ ✓）

**Step 4a：終點固定 $\omega(1) = 10$**
$$10 = -\lambda(1)\, e^{-1}\sinh 1 \;\Rightarrow\; \lambda(1) = -\frac{10\,e}{\sinh 1} \approx -23.13$$
$$\boxed{u^*(t) = \frac{10\, e^{t}}{\sinh 1} \approx 8.51\, e^{t}, \qquad \omega^*(t) = 10\,\frac{\sinh t}{\sinh 1}}$$
- 電壓從 $u(0) = 8.51$ 一路升到 $u(1) = 23.13$
- 最小成本 $J^* = \tfrac12\int_0^1 (8.51\,e^t)^2\, dt \approx 115.6$

**為什麼電壓越來越大？** 越早加的電壓，效果越容易被摩擦「吃掉」：$t$ 時刻多出來的轉速，到終點只剩 $e^{-(1-t)}$ 倍。越晚加越划算，所以最佳策略是**前面少加、後面多加**。

這正是 $\lambda(t) = \lambda(1)e^{t-1}$ 在說的事：$\lvert\lambda(t)\rvert$ 是「此刻轉速多一單位值多少」，**越接近終點越值錢**（早期的轉速，最後都會被摩擦耗掉）。

**注意：這是開迴路 (open-loop)**。$u^*(t)$ 只是時間的函數，事先就算好了；中途如果有擾動，它不會修正（2.2.2 講過）。

**Step 4b：終點自由（軟性要求）**
不強制到 10，改成加一個終點成本 $\phi = \tfrac12 s\,(\omega(1) - 10)^2$。
- 邊界條件換成：$\lambda(1) = \dfrac{\partial\phi}{\partial\omega(1)} = s\,(\omega(1) - 10)$
- 再配上 Step 3 的 $\omega(1) = -\lambda(1)e^{-1}\sinh 1 \approx -0.432\,\lambda(1)$，解得：
$$\omega(1) = \frac{10 \times 0.432\, s}{1 + 0.432\, s}$$

| $s$ | 0 | 1 | 10 | 100 | $\to\infty$ |
|---|---|---|---|---|---|
| $\omega(1)$ | 0 | 3.02 | 8.12 | 9.77 | $\to 10$ |

**跟 2.1.1 的 $s$ 表是同一個故事**：$s = 0$ 完全不在意終點 → 乾脆不加電（$u = 0$）；$s \to \infty$ → 等於終點固定（Step 4a）。**終點成本就是「終點固定」的軟性版本。**

### 3.3 連續 LQR

#### 3.3.1 設定

- 系統：$\dot x = Ax + Bu$
- 成本：
$$J = \tfrac12 x^T(T)\, S(T)\, x(T) + \tfrac12 \int_{t_0}^{T} (x^T Q x + u^T R u)\, dt$$
- 權重的意義和要求跟 2.2.1 的表完全一樣：$S(T) \ge 0$、$Q \ge 0$、$R > 0$

#### 3.3.2 一樣猜 $\lambda = S(t)\, x$

把 2.2.2 的破解法原封不動搬過來：
$$\lambda(t) = S(t)\, x(t)$$
（終點：$\lambda(T) = \partial\phi/\partial x = S(T)\,x(T)$，猜法在終點成立 ✓）

LQR 的 Hamiltonian：$H = \tfrac12(x^T Q x + u^T R u) + \lambda^T(Ax + Bu)$

**代入駐點條件**：$0 = Ru + B^T\lambda$（用 0.5 的微分表）
$$\boxed{u^* = -K(t)\, x, \qquad K(t) = R^{-1} B^T S(t)}$$

**代入共態方程**：$-\dot\lambda = Qx + A^T\lambda$。左邊用乘法律微分 $\lambda = Sx$：
$$\dot\lambda = \dot S x + S\dot x = \dot S x + S(A - BR^{-1}B^TS)\,x$$
代進去：
$$-\dot S x - SAx + SBR^{-1}B^TSx = Qx + A^TSx$$
對所有 $x$ 都成立，所以：
$$\boxed{-\dot S = A^TS + SA - SBR^{-1}B^TS + Q, \qquad S(T)\text{ 給定}}$$
這就是**微分 Riccati 方程**。

**最佳成本**：$J^* = \tfrac12 x_0^T S(t_0)\, x_0$

**步驟跟 2.2.2 一模一樣**：猜 $\lambda = Sx$ → 駐點條件給出 $u = -Kx$ → 共態方程給出 $S$ 的方程。

#### 3.3.3 為什麼 $K$ 比離散版簡單？

| | 離散（2.2.2） | 連續 |
|---|---|---|
| $K$ | $(B^TS_{k+1}B + R)^{-1} B^TS_{k+1}A$ | $R^{-1}B^TS$ |

連續版少了 $B^TSB$，也少了 $A$。用 Euler 近似取極限：$A_d = I + A\Delta t$、$B_d = B\Delta t$、$R_d = R\Delta t$，代入離散公式：
$$K = (\Delta t^2\, B^TSB + \Delta t\, R)^{-1}\, \Delta t\, B^TS(I + A\Delta t) = (R + \Delta t\, B^TSB)^{-1} B^TS(I + A\Delta t) \;\xrightarrow{\ \Delta t \to 0\ }\; R^{-1}B^TS$$

**直覺**：離散時 $u_k$ 要「維持一整格」，會實實在在改變下一步的狀態，所以要把「改變狀態造成的未來成本」$B^TSB$ 也算進去。連續時，每一瞬間的 $u$ 只推動狀態一點點（$\Delta t$ 那麼多），這一項變成高階的小量而消失，只剩電費 $R$。

#### 3.3.4 Riccati 怎麼解：逆著時間積分

- 這是一條**微分方程**，條件給在**終點** $S(T)$，所以要從 $T$ 往回積分到 $t_0$（跟 2.2.3 從 $S_N$ 逆著時間算一樣）
- **實作技巧**（Lewis 3.3）：令 $\tau = T - t$（「剩下多少時間」），方程變成
$$\frac{dS}{d\tau} = A^TS + SA - SBR^{-1}B^TS + Q, \qquad S\big\rvert_{\tau = 0} = S(T)$$
  負號不見了，從 $\tau = 0$ 順著積分就好，一般的 ODE 求解器都能用
- 純量 (scalar) 情況可以用分離變數得到解析解（Lewis Ex 3.3-4），但考試多半只要求**寫出方程**或**求穩態解**（3.4）

#### 3.3.5 馬達例子：連續版的 2.2.4 / 2.2.5

$\dot\omega = -\omega + u$，$J = \tfrac12\int_0^T (\omega^2 + u^2)\, dt$，$S(T) = 0$。也就是 $A = -1$、$B = 1$、$Q = R = 1$。

Scalar Riccati：
$$-\dot s = -2s - s^2 + 1, \qquad s(T) = 0, \qquad K = s$$
用剩餘時間 $\tau = T - t$ 寫：$\dfrac{ds}{d\tau} = 1 - 2s - s^2$

**增益隨「剩多少時間」的變化，跟 Ch 2 對照**（離散版的成本已經乘上 $\Delta t$，前面說過這不影響 $K$）：

| 剩餘時間 $\tau$ | 0.1 | 0.2 | 0.5 | 1 | 2 | 3 | $\infty$ |
|---|---|---|---|---|---|---|---|
| 離散 $\Delta t = 0.1$（**就是 2.2.5 的表**） | 0 | 0.089 | 0.256 | 0.354 | 0.382 | 0.384 | 0.384 |
| 離散 $\Delta t = 0.01$ | 0.082 | 0.156 | 0.297 | 0.383 | 0.410 | 0.411 | 0.411 |
| **連續** | 0.090 | 0.163 | 0.301 | 0.386 | 0.413 | 0.414 | **0.414** |

**看出什麼？**
1. **形狀一樣**：離終點近 → $K$ 小（快結束了，花電不划算）；離終點遠 → 收斂到常數
2. **$\Delta t$ 越小，離散越接近連續**。Ch 2 的 $K_\infty = 0.384$ 跟連續的 $0.414$ 差一點，是因為 0.1 秒的格子還不夠細
3. **$S$ 也一樣**：Ch 2 的 $S_\infty = 4.45$ 乘上 $\Delta t = 0.1$ 得 $0.445$，跟連續的 $0.414$ 很接近（$\Delta t = 0.01$ 時是 $0.417$）
4. **終點權重不影響長期增益**：改成 $S(T) = 10$，$s$ 從 10 一路降到 $\tau = 1$ 時的 0.55、$\tau = 2$ 時的 0.42、$\tau = 3$ 時的 0.415——還是收斂到 0.414（同 2.2.5「$S_N$ 選不同值，最後都收斂到同一個 $K_\infty$」）

### 3.4 穩態：代數 Riccati 方程 (ARE)

#### 3.4.1 從 Riccati 到 ARE

當 $T \to \infty$（或離終點夠遠），$S$ 不再變化，$\dot S = 0$：
$$\boxed{0 = A^TS + SA - SBR^{-1}B^TS + Q \quad\text{(ARE)}}$$
這跟 2.2.5 的 DARE 是同一個想法：令 $S_k = S_{k+1}$。

得到的 $K_\infty = R^{-1}B^TS_\infty$ 是**常數**，$u = -K_\infty x$ 就是一個**固定增益的回授控制**，實務上最常用。它也是無窮時間成本 $J = \tfrac12\int_0^\infty (x^TQx + u^TRu)\, dt$ 的真正最佳解。

#### 3.4.2 ARE 什麼時候有好的解？

ARE 是**二次方程**，可能有好幾個解（馬達例子就有兩個根）。要挑對的那一個：
- $(A, B)$ **stabilizable** → 存在有界的極限解 $S_\infty \ge 0$
- 再加上 $(A, \sqrt Q)$ **observable**（$\sqrt Q$ 指任何滿足 $C^TC = Q$ 的 $C$）→ $S_\infty > 0$ 唯一，而且閉迴路 $A - BK_\infty$ **漸近穩定**
- 只要求 detectable 也行，但這時 $S_\infty$ 只保證 $\ge 0$

**白話**：
- **stabilizable**：不穩定的部分，控制推得動
- **observable / detectable**：不穩定的部分，成本看得到（看不到就不會想去修它）

兩個都滿足，LQR 就**保證**閉迴路穩定。這就是 Żak Ch 3 可控性、可觀察性派上用場的地方。

**挑解規則**：取**正定**的那個解（純量就取正的根），它同時也是讓閉迴路穩定的那個。

#### 3.4.3 馬達（一維）

ARE：$0 = -2s - s^2 + 1 \;\Rightarrow\; s^2 + 2s - 1 = 0 \;\Rightarrow\; s = -1 \pm \sqrt 2$

- 取正根 $s = \sqrt 2 - 1 \approx 0.414$（另一根 $-2.414$ 是負的，不是正定）
- $K = 0.414$，$u^* = -0.414\,\omega$
- 閉迴路：$\dot\omega = -\omega - 0.414\,\omega = -1.414\,\omega$ → 穩定 ✓
- **錯的根會怎樣？** $K = -2.414$ → $\dot\omega = (-1 + 2.414)\,\omega = +1.414\,\omega$，**爆炸**。錯的根剛好就是讓系統不穩定的那個
- 條件檢查：$(A, B) = (-1, 1)$ 可控、$(A, \sqrt Q) = (-1, 1)$ 可觀察 ✓

**結果解讀**：馬達本來自己會以 $\dot\omega = -\omega$ 歸零（時間常數 1 秒）；加了最佳控制變成 $-1.414\,\omega$（時間常數約 0.7 秒，收斂更快），代價是花了一些電。

**一般的 $q$、$r$ 會怎樣？** $J = \tfrac12\int(q\omega^2 + ru^2)\, dt$，ARE 解出
$$K = -1 + \sqrt{1 + q/r}, \qquad \text{閉迴路極點} = -\sqrt{1 + q/r}$$
- $q/r \to 0$（電很貴）：$K \to 0$，極點 $\to -1$，就是馬達原本的樣子（不控制）
- $q/r$ 越大：極點往左移，收斂越快，但越耗電
- **只跟比值 $q/r$ 有關**（呼應「$Q$、$R$ 同乘一個數不改變 $K$」）

#### 3.4.4 馬達（二維）：用 LQR 設計位置控制器

這是課本 Ex 3.4-1（Newton 系統）的同型題，**2×2 ARE 手解**很可能考。

**問題**：讓馬達的**角度**回到 0。
$$A = \begin{bmatrix}0 & 1\\ 0 & -1\end{bmatrix},\quad B = \begin{bmatrix}0\\ 1\end{bmatrix},\quad Q = \begin{bmatrix}1 & 0\\ 0 & 0\end{bmatrix}\ (\text{只在意角度}),\quad R = 1$$
回顧 0.3.2：不控制時特徵值是 $0, -1$，角度停在某處，不會回到 0。

**Step 1：設 $S$**，令 $S = \begin{bmatrix}s_1 & s_2\\ s_2 & s_3\end{bmatrix}$（對稱，所以只有 3 個未知數）

**Step 2：算各項**
$$A^TS + SA = \begin{bmatrix}0 & s_1 - s_2\\ s_1 - s_2 & 2(s_2 - s_3)\end{bmatrix}, \qquad SBR^{-1}B^TS = \begin{bmatrix}s_2^2 & s_2 s_3\\ s_2 s_3 & s_3^2\end{bmatrix}$$

**Step 3：ARE 的三個元素各自 $= 0$**（從最簡單的開始解）
- (1,1)：$-s_2^2 + 1 = 0 \;\Rightarrow\; s_2 = 1$
  （$s_2 = -1$ 代入下一條會得到複數，所以不要）
- (2,2)：$2(s_2 - s_3) - s_3^2 = 0 \;\Rightarrow\; s_3^2 + 2s_3 - 2 = 0 \;\Rightarrow\; s_3 = -1 + \sqrt 3 \approx 0.732$（取正）
- (1,2)：$s_1 - s_2 - s_2 s_3 = 0 \;\Rightarrow\; s_1 = 1 + 0.732 = 1.732$

**Step 4：檢查正定**（0.4 的 2×2 速算）：$s_1 = 1.732 > 0$、$\det S = 1.732 \times 0.732 - 1 = 0.268 > 0$ ✓

**Step 5：增益**
$$K = R^{-1}B^TS = [\,s_2\ \ s_3\,] = [\,1\ \ 0.732\,], \qquad u^* = -\theta - 0.732\,\omega$$
這就是一個 **PD 控制器**（比例作用在角度、微分作用在轉速），只是增益是「最佳化算出來的」，不是試出來的。

**Step 6：閉迴路驗證**
$$A - BK = \begin{bmatrix}0 & 1\\ -1 & -1.732\end{bmatrix}$$
trace $= -1.732$、det $= 1$ → $\lambda^2 + 1.732\lambda + 1 = 0$ → $\lambda = -0.866 \pm 0.5j$，實部 $< 0$ → **穩定** ✓。原本 $\lambda = 0$ 的那個方向也被拉回來了。

> ⚠️ **成本「看不到」就不會修**：如果改成只在意轉速 $Q = \begin{bmatrix}0 & 0\\ 0 & 1\end{bmatrix}$，解出 $K = [\,0\ \ 0.414\,]$——**角度完全不回授**，閉迴路特徵值是 $0, -1.414$，角度還是停在原地。原因是 $C = [\,0\ \ 1\,]$ 時 $(A, C)$ **不可偵測**（λ = 0 那個方向成本看不到，自己又不會衰減），不滿足 3.4.2 的條件。

#### 3.4.5 另一種解法：Hamiltonian 矩陣（選讀，可以當驗算）

把 $u = -R^{-1}B^T\lambda$ 代入狀態方程和共態方程，兩條合起來寫：
$$\frac{d}{dt}\begin{bmatrix}x\\ \lambda\end{bmatrix} = \underbrace{\begin{bmatrix}A & -BR^{-1}B^T\\ -Q & -A^T\end{bmatrix}}_{\text{Hamiltonian 矩陣 } \mathcal H} \begin{bmatrix}x\\ \lambda\end{bmatrix}$$
- $\mathcal H$ 的特徵值**成對出現**：有 $\mu$ 就有 $-\mu$
- **穩定的那一半（實部 $< 0$）就是最佳閉迴路 $A - BK_\infty$ 的極點**
- 把穩定特徵值的特徵向量寫成 $\begin{bmatrix}X\\ \Lambda\end{bmatrix}$，則 $S_\infty = \Lambda X^{-1}$（就是 $\lambda = Sx$ 的意思）

**馬達一維驗算**：$\mathcal H = \begin{bmatrix}-1 & -1\\ -1 & 1\end{bmatrix}$，trace $= 0$、det $= -2$ → $\mu^2 - 2 = 0$ → $\mu = \pm 1.414$
- 穩定的 $\mu = -1.414$ 正是 3.4.3 的閉迴路極點 ✓
- 特徵向量：$(\mathcal H + 1.414 I)v = 0$ → $0.414\, v_1 - v_2 = 0$ → $v = [\,1,\ 0.414\,]^T$ → $S = 0.414 / 1 = 0.414$ ✓

#### 3.4.6 偷懶版：有限時間也直接用常數 $K_\infty$

有限時間 $T$ 的真正最佳解是時變的 $K(t)$（3.3.5 的表），但離終點遠時 $K(t) \approx K_\infty$，所以實務上常常**整段都直接用 $K_\infty$**（Lewis 叫 suboptimal feedback）。代價是快到終點那段不是最佳的，但實作簡單很多。

任意固定增益 $K$ 的成本，都可以用 Lyapunov 型的方程算出來：
$$-\dot S = (A - BK)^TS + S(A - BK) + K^TRK + Q$$
穩態時就是 Żak Ch 4 的 Lyapunov 方程（把 $A$ 換成閉迴路 $A - BK$、把 $Q$ 換成 $Q + K^TRK$）。

### 3.5 頻域結果（大致了解即可）

**Chang-Letov 方程**：不用解 ARE，直接從轉移函數找最佳閉迴路極點。單輸入、$Q = qC^TC$ 時：
$$\Delta_{cl}(s)\,\Delta_{cl}(-s) = \Delta(s)\,\Delta(-s) + \frac{q}{r}\, N(s)\, N(-s)$$
- $\Delta(s) = \det(sI - A)$：開迴路特徵多項式
- $N(s)$：開迴路轉移函數 $C(sI - A)^{-1}B$ 的分子
- 右邊的根對稱於虛軸，**取左半平面那一半**就是最佳閉迴路極點

**馬達驗算**：$\Delta(s) = s + 1$、$N(s) = 1$
$$\Delta_{cl}(s)\,\Delta_{cl}(-s) = (1 + s)(1 - s) + \frac{q}{r} = 1 + \frac{q}{r} - s^2$$
根是 $s = \pm\sqrt{1 + q/r}$，取左半平面 → $-\sqrt{1 + q/r}$，跟 3.4.3 一樣 ✓

**根軌跡的意義**：$q/r$ 從 0 變到 $\infty$ 時，最佳極點從「開迴路極點（不穩定的會鏡射到左半平面）」移動到「開迴路零點（同樣鏡射）或無窮遠」。可以用來挑 $q/r$。

### 3.6 第三章統整

**Ch 2 ↔ Ch 3 公式對照（考試前看這張）：**

| | 離散（Ch 2） | 連續（Ch 3） |
|---|---|---|
| Hamiltonian | $H^k = L + \lambda_{k+1}^T f$ | $H = L + \lambda^T f$ |
| 狀態方程 | $x_{k+1} = f$ | $\dot x = f$ |
| 共態方程 | $\lambda_k = \partial H^k/\partial x_k$ | $-\dot\lambda = \partial H/\partial x$ ⚠️**負號** |
| 駐點條件 | $\partial H^k/\partial u_k = 0$ | $\partial H/\partial u = 0$ |
| 終點自由 | $\lambda_N = \partial\phi/\partial x_N$ | $\lambda(T) = \partial\phi/\partial x(T)$ |
| LQR 增益 | $K_k = (B^TS_{k+1}B + R)^{-1}B^TS_{k+1}A$ | $K = R^{-1}B^TS$ |
| Riccati | $S_k = A^TS_{k+1}(A - BK_k) + Q$ | $-\dot S = A^TS + SA - SBR^{-1}B^TS + Q$ |
| 穩態 | DARE | ARE：$0 = A^TS + SA - SBR^{-1}B^TS + Q$ |
| 最佳成本 | $\tfrac12 x_0^TS_0x_0$ | $\tfrac12 x_0^TS(t_0)x_0$ |
| 閉迴路穩定 | $\lvert\lambda(A - BK)\rvert < 1$ | $\text{Re}\,\lambda(A - BK) < 0$ |
| 馬達 $K_\infty$ | 0.384（$\Delta t = 0.1$） | 0.414 |

**一般問題 SOP（連續）：**
1. 寫 $H = L + \lambda^T f$
2. 三個條件：$\dot x = f$、$-\dot\lambda = \partial H/\partial x$、$\partial H/\partial u = 0$
3. 用駐點條件把 $u$ 寫成 $\lambda$ 的函數
4. 先解共態方程（常常跟 $x$ 無關），再解狀態方程，全部用未知的 $\lambda(T)$ 表示
5. 查 3.2.4 的邊界條件表，解出 $\lambda(T)$

**LQR SOP（連續）：**
1. 寫 Riccati：$-\dot S = A^TS + SA - SBR^{-1}B^TS + Q$，$S(T)$ 給定
2. 要穩態就令 $\dot S = 0$ 解 ARE，**取正定解**（2×2 時從最簡單的元素開始解）
3. $K = R^{-1}B^TS$，$u^* = -Kx$
4. 驗算：$A - BK$ 的特徵值實部都 $< 0$

**關鍵觀念：**
- **連續 = 離散的 $\Delta t \to 0$**：負號、較簡單的 $K$ 都是取極限的結果，不用另外背
- **負號的意義**：$\lambda$ 是「剩下的成本」的斜率，時間往前走，剩下的越來越少
- **終點成本 = 終點固定的軟性版**：3.2.7 的 $s$ 表和 2.1.1 的 $s$ 表是同一個故事
- **ARE 有多個解**：取正定的那個；需要 stabilizable + detectable 才保證閉迴路穩定
- **LQR 只跟 $Q : R$ 的比例有關**

**什麼時候用哪一套？** 跟 2.3 的表一樣：線性 + 二次成本 + 終點自由 → LQR（Riccati）；終點固定（例 3.2.7a）、非線性、非二次成本 → 一般 SOP；$u$ 有上下限 → Żak Ch 5 的 PMP；$T$ 自由 → 一般 SOP 再加 $H(T) = 0$。

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
4. 是 → $A$ 漸近穩定；否 → **不是**漸近穩定（可能是臨界，也可能是不穩定）

MATLAB 一行搞定：`P = lyap(A', Q)`。

**白話：碗 + 往下滑**
1. $P > 0$ → $V(x) = x^TPx$ 是一個碗，只有原點是最低點（0.4）
2. $A^TP + PA = -Q$ 且 $Q > 0$ → $\dot V = -x^TQx < 0$，不管狀態在哪，碗的高度都一直下降
3. 一直往下、又只有一個碗底 → 狀態只能滑到原點 → **漸近穩定**

**一維例子**（最好懂）：$\dot x = ax$，取 $V = px^2$
$$\dot V = 2px\dot x = 2ap\,x^2$$
要 $V$ 是碗：$p > 0$；要 $\dot V < 0$：$2ap < 0 \Rightarrow a < 0$。跟 0.3.2「$a < 0$ 就穩定」一模一樣。

**二維例子**：$A = \begin{bmatrix}0 & 1\\ -2 & -3\end{bmatrix}$（trace $=-3$、det $=2$ → $\lambda = -1, -2$，應該要穩定）

令 $P = \begin{bmatrix}a & b\\ b & c\end{bmatrix}$，解 $A^TP + PA = -I$：
$$\begin{bmatrix}-4b & a-3b-2c\\ a-3b-2c & 2b-6c\end{bmatrix} = \begin{bmatrix}-1 & 0\\ 0 & -1\end{bmatrix}$$
得 $b = \tfrac14,\ c = \tfrac14,\ a = \tfrac54$，即 $P = \begin{bmatrix}5/4 & 1/4\\ 1/4 & 1/4\end{bmatrix}$。

2×2 速算檢查：$p_{11} = \tfrac54 > 0$、$\det P = \tfrac{5}{16} - \tfrac{1}{16} = \tfrac14 > 0$ → $P$ 正定 → **穩定** ✓（跟特徵值的結論一致）

**⚠️ 常見誤解**：「穩定」**不等於**「$A$ 負定」。例：$A = \begin{bmatrix}-1 & 10\\ 0 & -1\end{bmatrix}$ 特徵值 $-1, -1$，是穩定的；但它的對稱部分 $\begin{bmatrix}-1 & 5\\ 5 & -1\end{bmatrix}$ 有特徵值 $+4$，所以 $A$ 不是負定。判斷穩定要看 $A$ 的特徵值，或用 Lyapunov 解出 $P$ 再檢查 $P$。

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
| 右端 $x_1$ 自由 | $F_{\dot x}\big\rvert_{t_1} = 0$ |
| 右端 $t_1$ 自由 | $(F - \dot x F_{\dot x})\big\rvert_{t_1} = 0$ |

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

## 九、多種語言，同一個真理

考試最愛考「殊途同歸」。以下這些路徑都導向 LQR 的 Riccati / ARE：

| 路徑 | 核心方程 | 誰的 |
|---|---|---|
| 三條件 + 猜 $\lambda_k = S_k x_k$（sweep method），離散 | Riccati 差分方程 → DARE | Lewis Ch 2（§2.2.2） |
| 三條件 + 猜 $\lambda = Sx$（sweep method），連續 | 微分 Riccati → ARE | Lewis Ch 3（§3.3.2） |
| HJB / quadratic ansatz | HJB → Riccati | Lewis Ch 6 |
| Lyapunov + 最佳化 | Lyapunov 方程改造 | Żak Ch 5 |
| MDP Bellman optimality | 離散 ARE for LQR | Lewis Ch 11 |
| Pontryagin | 對 $u$ 微分為零得到 $u^* = -R^{-1}B^T p$ | Żak Ch 5 |

**連續版都得到 $u^* = -R^{-1} B^T P x = -K x$，其中 $P$ 由 ARE 決定。** 離散版（Ch 2、Ch 11）是 $K = (B^TPB + R)^{-1}B^TPA$，取 $\Delta t \to 0$ 就變回連續版（§3.3.3）。

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

**共通策略**：不管題目怎麼問，寫下 $H$、寫下三兄弟（狀態方程、共態方程、駐點條件 $\partial H/\partial u = 0$）、寫下邊界條件——你已經拿到一半分數。
