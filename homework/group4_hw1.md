## System Theory HW1
###### 111061540張晉承 115061522陳双双
---
### Static Optimization
#### 1.Unconstrained Optimization

目標：尋求控制向量 $u \in \mathbb{R}^m$，使純量成本函數 $L(u)$ 最小化。

#### Taylor Series Expansion

$$dL = L_u^T du + \frac{1}{2} du^T L_{uu} du + O(3)$$

- **$L_u = \frac{\partial L}{\partial u}$**：梯度向量（Gradient，維度 $m \times 1$），決定一階變化方向與斜率。
- **$L_{uu} = \frac{\partial^2 L}{\partial u^2}$**：海森矩陣（Hessian / Curvature Matrix，維度 $m \times m$），決定局部曲率形狀。
- **$O(3)$**：三次及以上的高階微小項，當 $du \to 0$ 時可忽略。

#### 極值判定條件

- **一階必要條件（找臨界點 / 駐點）**：

$$L_u = 0$$


- **二階充分條件（判定極值型態）**：
  - **Local Minimum**：$L_{uu} > 0$（正定矩陣，所有特徵值 $> 0$）。
  - **Local Maximum**：$L_{uu} < 0$（負定矩陣，所有特徵值 $< 0$）。
  - **Saddle Point**：
  $L_{uu}$ 為不定矩陣（特徵值有正有負，在 $2 \times 2$ 矩陣中表現為 $\vert{}L_{uu}\vert{} < 0$）。
  - **Singular Point**：
  $\vert{}L_{uu}\vert{} = 0$（至少一個特徵值為 $0$），二階無法判定，需檢驗更高階項。



#### Quadratic Surfaces

$$L(u) = \frac{1}{2} u^T Q u + S^T u \quad (Q = Q^T)$$

- **最佳控制輸入**：$u^* = -Q^{-1}S$
- **曲率矩陣**：$L_{uu} = Q$（若 $Q > 0$ 則 $u^*$ 必為全域極小點）
- **最小成本值**：$L^* = -\frac{1}{2} S^T Q^{-1} S$
- **幾何特性**：梯度向量必定**垂直於等高線**，並指向數值增加最快的方向。

---

#### 2.Optimization with Equality Constraints

目標：在滿足物理約束方程式 $f(x, u) = 0$（$f \in \mathbb{R}^n$）的前提下，最小化成本 $L(x, u)$。

- $u \in \mathbb{R}^m$：可主動調節的控制向量。
- $x \in \mathbb{R}^n$：由物理約束決定的輔助狀態向量。

#### 一階變分推導（維持 $df = 0$）

1. **全微分關係**：

$$\begin{cases} dL = L_u^T du + L_x^T dx \\ df = f_u du + f_x dx = 0 \end{cases}$$


2. **消去相依變數 $dx$**（假設 $f_x$ 非奇異）：

$$dx = -f_x^{-1} f_u du$$


3. **一階必要條件**：

$$dL = \left( L_u^T - L_x^T f_x^{-1} f_u \right) du = 0 \implies L_u - f_u^T f_x^{-T} L_x = 0$$



---

#### 3.Lagrange Multipliers and the Hamiltonian

##### 線性相依觀點

將微分散開寫成增廣矩陣：


$$\begin{bmatrix} dL \\ df \end{bmatrix} = \begin{bmatrix} L_x^T & L_u^T \\ f_x & f_u \end{bmatrix} \begin{bmatrix} dx \\ du \end{bmatrix} = 0$$


因需存在非零解且不互相矛盾，係數矩陣列向量必須**線性相依**，存在拉格朗日乘子向量 $\lambda \in \mathbb{R}^n$ 滿足：


$$\begin{bmatrix} 1 & \lambda^T \end{bmatrix} \begin{bmatrix} L_x^T & L_u^T \\ f_x & f_u \end{bmatrix} = 0 \implies \begin{cases} L_x^T + \lambda^T f_x = 0 \\ L_u^T + \lambda^T f_u = 0 \end{cases}$$


由第一式可得：$\lambda^T = -L_x^T f_x^{-1}$。

##### Lagrange Multipliers $\lambda$

$$\left. \frac{\partial L}{\partial f} \right\vert{}_{du=0} = -\lambda$$

- $-\lambda$ 是 $L$ 關於控制量 $u$ 保持不變的限制條件的偏導數。它表示當約束條件改變時，保持控制量不變對效能指標的影響。

##### Hamiltonian Function Definition

將帶約束問題轉換為無約束純量形式：


$$H(x, u, \lambda) \triangleq L(x, u) + \lambda^T f(x, u)$$