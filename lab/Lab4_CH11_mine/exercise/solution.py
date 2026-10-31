"""
第十一章 Agentic-RL 小練習（解答版）
只需要 Python 3.8+ 與 numpy，不需要 GPU。執行：python solution.py
"""
import json
import re
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent

# ============================================================
# Part 1：寫一個獎勵函數
# ============================================================
NUM_RE = r"-?\d[\d,]*\.?\d*"


def extract_answer(text):
    """抓出模型的最終答案（float）；抓不到回傳 None。
    規則：優先抓 "Final Answer:" 後面的數字，否則取全文最後一個數字。"""
    m = re.search(r"Final Answer:\s*\$?\s*(" + NUM_RE + ")", text)
    if m:
        s = m.group(1)
    else:
        nums = re.findall(NUM_RE, text)
        if not nums:
            return None
        s = nums[-1]
    s = s.replace(",", "").rstrip(".")
    try:
        return float(s)
    except ValueError:
        return None


def accuracy_reward(text, gt):
    """答對 1.0，答錯 0.0"""
    pred = extract_answer(text)
    return 1.0 if pred is not None and abs(pred - float(gt)) < 1e-4 else 0.0


LENGTH_TARGET, LENGTH_ALPHA = 200, 0.001


def length_penalty_reward(text, gt):
    """答對才扣長度分：1 - alpha * max(0, 字數 - 目標字數)；答錯一律 0"""
    acc = accuracy_reward(text, gt)
    if acc == 0:
        return 0.0
    return max(0.0, acc - LENGTH_ALPHA * max(0, len(text) - LENGTH_TARGET))


STEP_BONUS = 0.1


def step_reward(text, gt):
    """答對才加步驟分：1 + 0.1 * (\"Step N:\" 出現的次數)"""
    acc = accuracy_reward(text, gt)
    if acc == 0:
        return 0.0
    return acc + STEP_BONUS * len(re.findall(r"Step \d+:", text))


# ============================================================
# Part 2：GRPO 的組內相對優勢
# ============================================================
def group_advantages(rewards, normalize=True):
    """advantage_i = r_i - mean(r)；normalize=True 時再除以 std（TRL 預設作法）"""
    r = np.asarray(rewards, dtype=float)
    adv = r - r.mean()
    if normalize:
        adv = adv / (r.std() + 1e-4)
    return adv


def show_group(group, reward_fn):
    gt = group["ground_truth"]
    rewards = [reward_fn(c, gt) for c in group["completions"]]
    adv = group_advantages(rewards)
    print(f"\n題目：{group['question'][:90]}...")
    print(f"正確答案：{gt}   （{group['note']}）")
    print(f"{'#':>2} {'預測':>8} {'字數':>5} {'reward':>7} {'advantage':>10}  方向")
    for i, (c, r, a) in enumerate(zip(group["completions"], rewards, adv)):
        arrow = "↑ 提高機率" if a > 1e-6 else ("↓ 降低機率" if a < -1e-6 else "－ 不變")
        print(f"{i:>2} {str(extract_answer(c)):>8} {len(c):>5} {r:>7.3f} {a:>10.3f}  {arrow}")


# ============================================================
# Part 3：玩具版 GRPO —— 獎勵函數會把策略推向哪裡？
# ============================================================
# 一題固定的題目，模型只有 4 種「回答風格」可選。策略 = 4 種風格上的 softmax 分布。
TOY_GT = "72"
STYLES = {
    "A 正確簡潔": "Step 1: 48 / 2 = 24 clips in May.\nStep 2: 48 + 24 = 72.\nFinal Answer: 72",
    "B 正確冗長": ("Let me think about this very carefully. " * 8
                   + "Step 1: In May she sold half of 48, which is 48 / 2 = 24.\n"
                   + "Step 2: Altogether 48 + 24 = 72.\nFinal Answer: 72"),
    "C 錯誤": "Step 1: 48 / 2 = 24.\nStep 2: 48 - 24 = 24.\nFinal Answer: 24",
    "D 正確但灌步驟": ("Step 1: 48 / 2 = 24.\nStep 2: 48 + 24 = 72.\n"
                      + "".join(f"Step {k}: Double-check the result.\n" for k in range(3, 13))
                      + "Final Answer: 72"),
}


def toy_grpo(reward_fn, steps=200, group_size=8, lr=0.5, beta=0.0, seed=0):
    rng = np.random.default_rng(seed)
    names = list(STYLES)
    style_reward = np.array([reward_fn(STYLES[n], TOY_GT) for n in names])
    ref = np.array([0.25, 0.25, 0.4, 0.1])  # 「SFT 後」的初始分布：常答錯、很少灌步驟
    logits = np.log(ref)
    history = []
    for t in range(steps + 1):
        pi = np.exp(logits - logits.max())
        pi /= pi.sum()
        if t % 50 == 0:
            history.append((t, pi.copy()))
        group = rng.choice(len(names), size=group_size, p=pi)  # 1. 採樣一組回答
        r = style_reward[group]                                 # 2. 算 reward
        adv = group_advantages(r)                               # 3. 組內相對優勢
        grad = np.zeros_like(logits)                            # 4. policy gradient
        for k, a in zip(group, adv):
            onehot = np.eye(len(names))[k]
            grad += a * (onehot - pi)  # ∇ log π(k) 對 logits 的梯度
        grad /= group_size
        kl = np.sum(pi * np.log(pi / ref))                      # 5. KL(π || π_ref) 懲罰
        grad_kl = pi * (np.log(pi / ref) - kl)
        logits += lr * (grad - beta * grad_kl)
    return names, style_reward, history


def show_toy(title, reward_fn, **kw):
    names, style_reward, history = toy_grpo(reward_fn, **kw)
    print(f"\n=== {title} ===")
    print("每種風格的 reward：" + "、".join(f"{n}={r:.2f}" for n, r in zip(names, style_reward)))
    print("step  " + "  ".join(f"{n:<10}" for n in names))
    for t, pi in history:
        print(f"{t:>4}  " + "  ".join(f"{p:<10.2f}" for p in pi))


if __name__ == "__main__":
    data = json.loads((HERE / "completions.json").read_text(encoding="utf-8"))

    print("#" * 60 + "\n# Part 1 + 2：真實模型輸出的 reward 與 advantage\n" + "#" * 60)
    for group in data["groups"]:
        show_group(group, accuracy_reward)
    print("\n換成長度懲罰，看看第一組的 advantage 怎麼變：")
    show_group(data["groups"][0], length_penalty_reward)

    print("\n" + "#" * 60 + "\n# Part 3：玩具版 GRPO\n" + "#" * 60)
    show_toy("accuracy reward", accuracy_reward)
    show_toy("length penalty reward", length_penalty_reward)
    show_toy("step reward（reward hacking）", step_reward)
    show_toy("step reward + KL 懲罰 beta=1.0", step_reward, beta=1.0)
