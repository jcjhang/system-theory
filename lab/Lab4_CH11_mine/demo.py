"""
第十一章 Agentic-RL tutorial 現場 demo：只讀取已經在 GPU 上跑好的結果，不需要 torch / GPU。
用法：python demo.py <指令>      （不加指令會列出全部）

  outputs [題號]   同一題：Base / SFT / GRPO 的真實回答（預設第 48 題）
  lora             LoRA 只訓練了多少參數
  group            GRPO 的核心：同一題寫 8 次 → reward → advantage
  zero-std         有多少題「全對或全錯」，學不到東西
  e1               E1：Base → SFT → GRPO 的評估結果
  curves           GRPO 訓練曲線（reward / KL / 長度），存成 figures/grpo_curves.png
  e3               E3：換獎勵函數，模型行為怎麼變
  e4               E4：KL 係數 beta、學習率的影響（含 figures/e4_curves.png）
  hack             額外實驗：故意誘發 reward hacking
  gpu              每個階段用了多少 GPU 記憶體和時間
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE / "experiments"
RES, RUNS, LOGS, FIG = EXP / "results", EXP / "runs_pulled", EXP / "logs_pulled", HERE / "figures"

NAMES = {
    "base": "Base（沒訓練）", "sft": "SFT", "grpo_acc_125": "GRPO 125 步", "grpo_acc": "GRPO 250 步",
    "grpo_length_penalty": "長度懲罰", "grpo_step": "步驟獎勵",
    "grpo_beta0": "beta=0（無 KL）", "grpo_beta05": "beta=0.5（強 KL）", "grpo_lr2e-4": "lr=2e-4（10 倍）",
    "grpo_step_hack": "步驟獎勵+無KL+大lr",
}


def load_eval(name):
    p = RES / f"eval_{name}.json"
    return json.loads(p.read_text()) if p.exists() else None


def load_run(name):
    p = RUNS / name / "summary.json"
    return json.loads(p.read_text()) if p.exists() else None


def train_logs(name):
    s = load_run(name)
    return [h for h in s["log_history"] if "reward" in h] if s else []


def width(s):
    return sum(2 if ord(ch) > 0x2E80 else 1 for ch in s)


def pad(s, w):
    s = str(s)
    return s + " " * max(0, w - width(s))


def table(header, rows):
    cols = list(zip(header, *rows))
    ws = [max(width(str(c)) for c in col) + 2 for col in cols]
    print("".join(pad(h, w) for h, w in zip(header, ws)))
    print("-" * sum(ws))
    for r in rows:
        print("".join(pad(c, w) for c, w in zip(r, ws)))


def missing(name):
    print(f"  （{NAMES.get(name, name)} 的結果還沒有）")


# ------------------------------------------------------------------
def cmd_outputs(idx="48"):
    i = int(idx)
    evals = {n: load_eval(n) for n in ["base", "sft", "grpo_acc"]}
    d0 = evals["sft"]["details"][i]
    print(f"題目（GSM8K test #{i}）：{d0['question']}\n正確答案：{d0['ground_truth']}\n")
    for n, e in evals.items():
        d = e["details"][i]
        out = d["output"].strip()
        lines = out.splitlines()
        if len(out) > 400 or len(lines) > 8:
            out = "\n".join(lines[:8])[:400] + f" …（後面還有，共 {d['n_tokens']} tokens）"
        mark = "✅ 答對" if d["correct"] else "❌ 答錯"
        print(f"── {NAMES[n]}  →  抓到的答案 {d['pred']}  {mark}")
        print(out + "\n")


def cmd_lora():
    s = load_run("sft")
    t, a = s["trainable_params"], s["total_params"]
    print(f"模型總參數：      {a:>12,}")
    print(f"LoRA 訓練的參數： {t:>12,}  （{t / a:.3%}）")
    print("設定：r=16, alpha=32，只加在 attention 的 q/k/v/o 上；其餘 99% 以上的參數凍結不動")
    print(f"SFT 訓練時 GPU 記憶體峰值：{s['peak_mem_gb']:.1f} GB")


def cmd_group():
    sys.path.insert(0, str(HERE / "exercise"))
    from solution import accuracy_reward, show_group
    data = json.loads((HERE / "exercise" / "completions.json").read_text(encoding="utf-8"))
    for g in data["groups"]:
        show_group(g, accuracy_reward)
    print("\n第一組：答對的 advantage > 0（↑），答錯的 < 0（↓），加起來剛好是 0")
    print("第二組：8 個全對 → 每個都等於平均 → advantage 全是 0 → 這題學不到東西")


def cmd_zero_std():
    rows = [json.loads(l) for l in (RUNS / "grpo_acc" / "groups.jsonl").open()]
    allc = allw = mixed = 0
    for r in rows:
        for k in range(0, len(r["rewards"]), 8):
            g = r["rewards"][k:k + 8]
            if min(g) == max(g) == 1:
                allc += 1
            elif min(g) == max(g):
                allw += 1
            else:
                mixed += 1
    tot = allc + allw + mixed
    print(f"GRPO（accuracy reward）訓練中總共 {tot} 題，每題寫 8 次：")
    table(["情況", "題數", "比例"], [
        ["8 個全對", allc, f"{allc / tot:.1%}"],
        ["8 個全錯", allw, f"{allw / tot:.1%}"],
        ["有對有錯（真正有在學）", mixed, f"{mixed / tot:.1%}"],
    ])
    print("\n全對或全錯 → advantage 全是 0 → 這題的運算白做了")


def cmd_e1():
    rows, buckets = [], []
    for n in ["base", "sft", "grpo_acc_125", "grpo_acc"]:
        e = load_eval(n)
        if not e:
            missing(n)
            continue
        s = e["summary"]
        rows.append([NAMES[n], f"{s['accuracy']:.1%}", f"{s['format_correctness']:.1%}",
                     f"{s['avg_tokens']:.0f}", f"{s['avg_steps']:.2f}"])
        b = s["accuracy_by_steps"]
        buckets.append([NAMES[n]] + [f"{b[k]['acc']:.0%}" for k in ["1-2", "3-4", "5+"]])
    print("GSM8K 測試集前 200 題（greedy decoding）\n")
    table(["模型", "正確率", "格式正確", "平均 tokens", "平均步驟數"], rows)
    print("\n依「標準解答需要幾步」分組的正確率（題數 64 / 92 / 44）\n")
    table(["模型", "1-2 步", "3-4 步", "5+ 步"], buckets)
    print("\n注意：200 題的正確率誤差約 ±3.5 個百分點，SFT→GRPO 的 +4 點不算顯著")


def smooth(xs, k=5):
    out = []
    for i in range(len(xs)):
        w = [x for x in xs[max(0, i - k + 1):i + 1] if x is not None]
        out.append(sum(w) / len(w) if w else None)
    return out


def plt_setup():
    import matplotlib
    matplotlib.use("Agg" if "--save" in sys.argv else matplotlib.get_backend())
    import matplotlib.pyplot as plt
    FIG.mkdir(exist_ok=True)
    return plt


def finish(plt, fig, name):
    path = FIG / name
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    print(f"圖存到 {path.relative_to(HERE)}")
    if "--save" not in sys.argv:
        plt.show()


def cmd_curves():
    h = train_logs("grpo_acc")
    plt = plt_setup()
    step = [x["step"] for x in h]
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.6))
    for a, key, title in [(ax[0], "reward", "Reward (fraction correct)"),
                          (ax[1], "kl", "KL to SFT model"),
                          (ax[2], "completions/mean_length", "Answer length (tokens)")]:
        y = [x.get(key) for x in h]
        a.plot(step, y, alpha=0.3, color="C0")
        a.plot(step, smooth(y), color="C0", lw=2)
        a.set_title(title)
        a.set_xlabel("GRPO step")
        a.grid(alpha=0.3)
    fig.suptitle("GRPO on GSM8K, accuracy reward (Qwen3-0.6B-Base + SFT + LoRA)")
    first, last = h[:5], h[-5:]
    avg = lambda rows, k: sum(r[k] for r in rows) / len(rows)
    print("前 25 步 → 最後 25 步的平均：")
    print(f"  reward（答對比例）：{avg(first, 'reward'):.2f} → {avg(last, 'reward'):.2f}")
    print(f"  KL（離 SFT 模型多遠）：{avg(first, 'kl'):.4f} → {avg(last, 'kl'):.4f}")
    print(f"  回答長度（tokens）：{avg(first, 'completions/mean_length'):.0f} → {avg(last, 'completions/mean_length'):.0f}")
    finish(plt, fig, "grpo_curves.png")


def chars_trend(name):
    """訓練中每次 reward 呼叫的平均回答字數：前 25 步 vs 後 25 步（每步 4 題 × 8 個回答 = 1 次呼叫）"""
    p = RUNS / name / "groups.jsonl"
    if not p.exists():
        return None
    calls = [json.loads(l) for l in p.open()]
    lens = [sum(len(c) for c in r["completions"]) / len(r["completions"]) for r in calls]
    steps = [sum(len(re.findall(r"Step \d+:", c)) for c in r["completions"]) / len(r["completions"]) for r in calls]
    m = lambda xs: sum(xs) / len(xs)
    return m(lens[:25]), m(lens[-25:]), m(steps[:25]), m(steps[-25:])


def cmd_e3():
    print("同樣從 SFT 模型出發、各訓練 125 步，只換獎勵函數：\n")
    rows = []
    for n, rw in [("grpo_acc_125", "答對=1"), ("grpo_length_penalty", "答對=1，超過 200 字扣分"),
                  ("grpo_step", "答對=1，每個 Step +0.1")]:
        e = load_eval(n)
        tr = chars_trend("grpo_acc" if n == "grpo_acc_125" else n)
        if not e:
            missing(n)
            continue
        s = e["summary"]
        rows.append([NAMES[n] if n != "grpo_acc_125" else "只看對錯", rw, f"{s['accuracy']:.0%}",
                     f"{s['avg_tokens']:.0f}", f"{s['avg_steps']:.2f}",
                     f"{tr[0]:.0f} → {tr[1]:.0f}", f"{tr[2]:.2f} → {tr[3]:.2f}"])
    table(["獎勵", "規則", "正確率", "tokens", "步驟數", "訓練中字數 前→後", "訓練中步驟 前→後"], rows)
    print("\n長度懲罰：訓練中回答字數明顯變短；步驟獎勵：125 步內幾乎沒有灌步驟（KL 把它拉住了）")


def cmd_e4():
    rows = []
    for n, b, lr in [("grpo_acc_125", "0.05", "2e-5"), ("grpo_beta0", "0", "2e-5"),
                     ("grpo_beta05", "0.5", "2e-5"), ("grpo_lr2e-4", "0.05", "2e-4")]:
        e = load_eval(n)
        run = load_run("grpo_acc" if n == "grpo_acc_125" else n)
        if not e or not run:
            missing(n)
            continue
        h = train_logs("grpo_acc" if n == "grpo_acc_125" else n)[:20]
        kl = [x["kl"] for x in h if "kl" in x]
        s = e["summary"]
        rows.append([NAMES[n] if n != "grpo_acc_125" else "基準（125 步）", b, lr, f"{s['accuracy']:.0%}",
                     f"{s['format_correctness']:.0%}", f"{s['avg_tokens']:.0f}",
                     f"{kl[-1]:.4f}" if kl else "不計算", f"{run['peak_mem_gb']:.2f} GB"])
    print("從 SFT 模型出發，accuracy reward，其他實驗各訓練 100 步：\n")
    table(["設定", "beta", "lr", "正確率", "格式", "tokens", "第 100 步 KL", "記憶體峰值"], rows)
    print("\nbeta=0 時連 reference model 都不用算，所以記憶體比較少")

    plt = plt_setup()
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.6))
    for c, (n, label) in enumerate([("grpo_acc", "beta=0.05, lr=2e-5 (baseline)"), ("grpo_beta0", "beta=0"),
                                    ("grpo_beta05", "beta=0.5"), ("grpo_lr2e-4", "lr=2e-4")]):
        h = train_logs(n)[:20]
        if not h:
            continue
        st = [x["step"] for x in h]
        ax[0].plot(st, smooth([x["reward"] for x in h]), label=label, color=f"C{c}")
        if "kl" in h[0]:
            ax[1].plot(st, [x["kl"] for x in h], label=label, color=f"C{c}")
    ax[0].set_title("Reward (smoothed)")
    ax[1].set_title("KL to SFT model (beta=0 does not compute KL)")
    for a in ax:
        a.set_xlabel("GRPO step")
        a.grid(alpha=0.3)
        a.legend(fontsize=8)
    finish(plt, fig, "e4_curves.png")


def cmd_hack(idx="1"):
    e = load_eval("grpo_step_hack")
    if not e:
        missing("grpo_step_hack")
        return
    print("步驟獎勵（答對才給分，每個 Step +0.1），拿掉 KL（beta=0）、學習率 1e-4，訓練 100 步：\n")
    rows = []
    for n in ["sft", "grpo_step", "grpo_step_hack"]:
        s = load_eval(n)["summary"]
        rows.append([NAMES[n], f"{s['accuracy']:.0%}", f"{s['format_correctness']:.1%}",
                     f"{s['avg_tokens']:.0f}", f"{s['avg_steps']:.2f}"])
    table(["模型", "正確率", "有寫 Final Answer", "tokens", "平均步驟數"], rows)
    tr = chars_trend("grpo_step_hack")
    if tr:
        print(f"\n訓練中平均步驟數：{tr[2]:.2f} → {tr[3]:.2f}；平均字數：{tr[0]:.0f} → {tr[1]:.0f}")
    i = int(idx)
    d0 = load_eval("sft")["details"][i]
    print(f"\n題目（GSM8K test #{i}）：{d0['question']}\n正確答案：{d0['ground_truth']}")
    for n in ["sft", "grpo_step_hack"]:
        d = load_eval(n)["details"][i]
        print(f"\n── {NAMES[n]}（{d['n_steps']} 步，{'✅ 答對' if d['correct'] else '❌ 答錯'}）\n{d['output'].strip()}")


def cmd_gpu():
    # 每個階段的起訖時間
    times, start = {}, {}
    for line in (LOGS / "run_all.out").open():
        m = re.match(r"\[(.+?)\] (start|done) +(\S+)", line)
        if m:
            from datetime import datetime
            t = datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
            if m.group(2) == "start":
                start[m.group(3)] = t
            elif m.group(3) in start:
                times[m.group(3)] = (t - start[m.group(3)]).total_seconds() / 60
    # nvidia-smi 看到的最大用量（含 CUDA context，比 PyTorch 自己算的多 1–2 GB）
    smi = defaultdict(int)
    for line in list((LOGS / "gpu_mem.csv").open())[1:]:
        parts = line.strip().split(",")
        cmd, mib = ",".join(parts[2:-1]), parts[-1]
        m = re.search(r"--(?:name|out) (?:runs/)?(\S+)", cmd)
        key = m.group(1) if m else cmd
        key = key if "evaluate" not in cmd else "eval_" + key
        smi[key] = max(smi[key], int(mib))
    for k in list(smi):  # nvidia-smi 會截斷過長的指令，例如 grpo_acc_125 → grpo_acc_12
        if k not in times:
            cand = [st for st in times if st.startswith(k)]
            if len(cand) == 1:
                smi[cand[0]] = max(smi[cand[0]], smi.pop(k))
    rows = []
    for stage, mins in times.items():
        name = stage.replace("eval_", "")
        if stage.startswith("eval_"):
            e = load_eval(name)
            peak = e["summary"]["peak_mem_gb"] if e else None
            what = "評估 200 題"
        else:
            r = load_run(name)
            peak = r["peak_mem_gb"] if r else None
            what = "SFT 750 步" if name == "sft" else f"GRPO {len(train_logs(name)) * 5} 步"
        rows.append([stage, what, f"{mins:.0f} 分", f"{peak:.1f} GB" if peak else "-",
                     f"{smi[stage] / 1024:.1f} GB" if smi.get(stage) else "-"])
    print("硬體：RTX 3090（24 GB），模型 Qwen3-0.6B-Base + LoRA，bf16\n")
    table(["階段", "內容", "時間", "PyTorch 峰值", "nvidia-smi 最大"], rows)
    print(f"\n總計：{sum(times.values()) / 60:.1f} 小時")


COMMANDS = {"outputs": cmd_outputs, "lora": cmd_lora, "group": cmd_group, "zero-std": cmd_zero_std,
            "e1": cmd_e1, "curves": cmd_curves, "e3": cmd_e3, "e4": cmd_e4, "hack": cmd_hack, "gpu": cmd_gpu}

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--save"]
    if not args or args[0] not in COMMANDS:
        print(__doc__)
    else:
        COMMANDS[args[0]](*args[1:])
