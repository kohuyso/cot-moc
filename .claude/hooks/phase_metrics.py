#!/usr/bin/env python3
"""Do thoi gian va token theo giai doan (phase) va theo task cua SDLC Harness.

Hai che do:

  hook    (mac dinh khi co stdin) - gan vao Claude Code hooks. Chi ghi "moc" (marker) nhe vao
          .claude/metrics/markers.jsonl: thoi diem, run, phase, task, duong dan transcript.
          Khong bao gio chan agent: moi loi deu bi nuot, luon exit 0, khong in ra stdout.

  report  - doc markers + .harness/runs/*/events.jsonl + transcript cua Claude Code, roi tinh
            thoi gian va token cho tung phase / tung task.

  task    - danh dau task dang lam:  phase_metrics.py task start WBS-1.1 | task end | task show

Nguon du lieu:
  * Phase + thoi gian vao/ra phase : events.jsonl cua harness (TRANSITION_ACCEPTED) - chinh xac, doc-only.
  * Token                          : `usage` cua tung assistant message trong transcript
                                     (hook payload khong co token). Khu trung theo message.id.
  * Task                           : (1) lenh `task start` thu cong, (2) suy ra tu file dang Write/Edit
                                     doi chieu voi "Target Files" cua tung WBS trong implementation-plan,
                                     (3) work_item_id cua slice run.

Chi dung thu vien chuan. Khong ghi vao .harness/ (state.json, events.jsonl la cua controller).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from fnmatch import fnmatch
from pathlib import Path

CODE_PHASES = {"DEV_CODING", "DEV_REVIEW", "CODE_REVIEW"}
EDIT_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit", "write_file", "edit_file"}
IDLE_CAP_SECONDS = 300  # khoang lang > 5 phut khong tinh la "thoi gian lam viec"
TOKEN_KEYS = ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")
SCREEN_RE = re.compile(r"\bSCR-[A-Z]{2,4}-\d{2,3}\b")
MAX_SPLIT = 3          # 1 turn nhac > 3 man hinh = viec cap module (vd viet ca FSD), khong chia cho tung man hinh
STICKY_GAP = 600       # turn khong nhac man hinh nao van tinh cho man hinh truoc neu cach <= 10 phut, cung phase
NO_SCREEN = "(khong gan man hinh)"
MULTI_SCREEN = "(nhieu man hinh / cap module)"


# --------------------------------------------------------------------------- helpers
def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def read_jsonl(path: Path):
    try:
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except ValueError:
                    continue
    except OSError:
        return


def project_root() -> Path:
    # <root>/.claude/hooks/phase_metrics.py
    return Path(__file__).resolve().parents[2]


def metrics_dir(root: Path) -> Path:
    return root / ".claude" / "metrics"


def norm_path(p: str) -> str:
    return p.replace("\\", "/").strip().lower()


# --------------------------------------------------------------------------- harness state
def list_runs(root: Path) -> list[Path]:
    return sorted(p.parent for p in (root / ".harness" / "runs").glob("*/state.json"))


def pick_active_run(root: Path) -> tuple[str | None, dict]:
    """Run dang hoat dong = run chua CLOSED duoc cap nhat gan nhat."""
    best: tuple[str, str, dict] | None = None
    for run_dir in list_runs(root):
        state = read_json(run_dir / "state.json")
        if not isinstance(state, dict):
            continue
        rank = (0 if state.get("phase") == "CLOSED" else 1, str(state.get("updated_at") or ""))
        if best is None or rank > (best[0], best[1]):  # type: ignore[operator]
            best = (rank[0], rank[1], state)  # type: ignore[assignment]
    if best is None:
        return None, {}
    state = best[2]
    return str(state.get("run_id")), state


def plan_files(root: Path, run_id: str) -> list[Path]:
    art = root / ".harness" / "runs" / run_id / "artifacts"
    return [p for p in [art / "implementation-plan.md", *sorted((art / "plans").glob("plan-*.md"))] if p.is_file()]


_WBS_HEAD = re.compile(r"^#{2,4}\s+((?:WBS|Task)\s*[\w.\-]+)\s*[:\-]?\s*(.*)$", re.I)
_BACKTICK = re.compile(r"`([^`\n]+)`")


def parse_wbs_files(root: Path, run_id: str) -> dict[str, list[str]]:
    """{ 'WBS 1.1': ['src/a.py', 'tests/test_a.py'] } lay tu 'Target Files' cua implementation-plan."""
    result: dict[str, list[str]] = {}
    for plan in plan_files(root, run_id):
        try:
            lines = plan.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        current: str | None = None
        for line in lines:
            m = _WBS_HEAD.match(line)
            if m:
                current = re.sub(r"\s+", " ", m.group(1)).upper()
                result.setdefault(current, [])
                continue
            if current and re.search(r"\b(create|modify|test|delete)\b\s*\**\s*:", line, re.I):
                for token in _BACKTICK.findall(line):
                    token = re.sub(r":\d+(-\d+)?$", "", token.strip())  # bo hau to so dong, vd file.py:1-10
                    if "/" in token or "\\" in token or re.search(r"\.\w{1,6}$", token):
                        result[current].append(norm_path(token))
    return {k: v for k, v in result.items() if v}


def infer_task_from_file(root: Path, run_id: str, file_path: str) -> str | None:
    target = norm_path(file_path)
    for task, files in parse_wbs_files(root, run_id).items():
        for f in files:
            if target.endswith("/" + f.lstrip("./")) or target == f:
                return task
    return None


# --------------------------------------------------------------------------- task marker
def task_file(root: Path) -> Path:
    return metrics_dir(root) / "current_task.json"


def last_file(root: Path) -> Path:
    return metrics_dir(root) / "last.json"


def read_manual_task(root: Path) -> str | None:
    data = read_json(task_file(root))
    return str(data["task"]) if isinstance(data, dict) and data.get("task") else None


def write_json_atomic(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, path)


def append_marker(root: Path, marker: dict) -> None:
    path = metrics_dir(root) / "markers.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(marker, ensure_ascii=False) + "\n")


# --------------------------------------------------------------------------- hook mode
def resolve_scope(root: Path, payload: dict, previous: dict) -> dict:
    run_id, state = pick_active_run(root)
    phase = state.get("phase") if state else None
    slice_info = state.get("slice") if isinstance(state.get("slice"), dict) else {}
    slice_task = slice_info.get("work_item_id")

    manual = read_manual_task(root)
    inferred = None
    tool_call = payload.get("toolCall") or {}
    tool_name = payload.get("tool_name") or tool_call.get("name")
    tool_input = payload.get("tool_input") or tool_call.get("args") or {}
    if run_id and phase == "DEV_CODING" and tool_name in EDIT_TOOLS:
        raw = tool_input.get("file_path") or tool_input.get("notebook_path") or tool_input.get("Path")
        if raw:
            inferred = infer_task_from_file(root, run_id, str(raw))
    # suy luan la "dinh": giu task cu cho toi khi gap file cua task khac, va chi trong nhom phase code
    sticky = previous.get("inferred") if run_id == previous.get("run_id") and phase in CODE_PHASES else None
    inferred = inferred or sticky
    task = manual or inferred or slice_task
    return {"run_id": run_id, "phase": phase, "task": task, "inferred": inferred}


def hook_main() -> int:
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        if not isinstance(payload, dict):
            sys.stdout.write("{}\n")
            return 0
        root = project_root()
        event = str(payload.get("hook_event_name") or payload.get("hookEventName") or "")
        previous = read_json(last_file(root)) or {}
        scope = resolve_scope(root, payload, previous)

        changed = any(scope[k] != previous.get(k) for k in ("run_id", "phase", "task"))
        checkpoint = event in {
            "SessionStart", "SessionEnd", "Stop", "SubagentStop",
            "UserPromptSubmit", "PreInvocation", "PostToolUse"
        }
        tool_call = payload.get("toolCall") or {}
        tool_name = payload.get("tool_name") or tool_call.get("name")
        session_id = payload.get("session_id") or payload.get("conversationId")
        transcript = payload.get("transcript_path") or payload.get("transcriptPath")

        if changed or checkpoint:
            append_marker(root, {
                "ts": now_iso(),
                "event": event,
                "session_id": session_id,
                "transcript": transcript,
                "run_id": scope["run_id"],
                "phase": scope["phase"],
                "task": scope["task"],
                "tool": tool_name,
                "reason": "scope_changed" if changed else "checkpoint",
            })
        write_json_atomic(last_file(root), scope)
        # refresh_report(root) - Da tat chay dong bo trong hook de tranh hook timeout (Hook cancelled -> exit 1)
    except Exception:  # noqa: BLE001 - hook khong duoc phep lam hong phien lam viec
        pass
    sys.stdout.write("{}\n")
    return 0


def refresh_report(root: Path) -> None:
    """Tinh lai .claude/metrics/report.md (+ report.json) de file luon khop voi du lieu moi nhat."""
    rep = build_report(root, None, [])
    out = metrics_dir(root)
    for name, text in (("report.md", render_markdown(rep)),
                       ("report.json", json.dumps(to_jsonable(rep), ensure_ascii=False, indent=2))):
        tmp = out / (name + ".tmp")
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, out / name)


# --------------------------------------------------------------------------- task command
def task_main(args: argparse.Namespace) -> int:
    root = project_root()
    if args.action == "show":
        print(read_manual_task(root) or "(khong co task thu cong)")
        return 0
    if args.action == "start":
        if not args.task_id:
            print("thieu <task_id>", file=sys.stderr)
            return 2
        write_json_atomic(task_file(root), {"task": args.task_id, "since": now_iso()})
        label = args.task_id
    else:
        task_file(root).unlink(missing_ok=True)
        label = None
    previous = read_json(last_file(root)) or {}
    scope = resolve_scope(root, {}, {**previous, "inferred": None})
    append_marker(root, {"ts": now_iso(), "event": f"task_{args.action}", "session_id": None, "transcript": None,
                         "run_id": scope["run_id"], "phase": scope["phase"], "task": scope["task"],
                         "tool": None, "reason": "manual"})
    write_json_atomic(last_file(root), scope)
    print(f"task: {label or '(da ket thuc)'}")
    return 0


# --------------------------------------------------------------------------- report
def phase_timeline(root: Path) -> dict[str, list[tuple[datetime, datetime, str]]]:
    """{run_id: [(start, end, phase)]} tu events.jsonl; doan cuoi mo den updated_at/hien tai."""
    timelines: dict[str, list[tuple[datetime, datetime, str]]] = {}
    now = datetime.now(timezone.utc)
    for run_dir in list_runs(root):
        run_id = run_dir.name
        state = read_json(run_dir / "state.json") or {}
        marks: list[tuple[datetime, str]] = []
        for ev in read_jsonl(run_dir / "events.jsonl"):
            ts = parse_ts(ev.get("timestamp"))
            if not ts:
                continue
            if ev.get("event") == "RUN_CREATED":
                marks.append((ts, "INIT"))
            elif ev.get("event") in {"TRANSITION_ACCEPTED", "HUMAN_DECISION_RECORDED"} and ev.get("to"):
                marks.append((ts, str(ev["to"])))
        marks.sort(key=lambda m: m[0])
        segs: list[tuple[datetime, datetime, str]] = []
        for i, (start, phase) in enumerate(marks):
            if i + 1 < len(marks):
                end = marks[i + 1][0]
            else:
                end = parse_ts(state.get("updated_at")) if phase == "CLOSED" else now
                end = max(end or start, start)
            segs.append((start, end, phase))
        timelines[run_id] = segs
    return timelines


def lookup_phase(timeline: dict, run_id: str | None, ts: datetime) -> tuple[str | None, str | None]:
    candidates = [run_id] if run_id in timeline else list(timeline)
    for rid in candidates:
        for start, end, phase in timeline.get(rid, []):
            if start <= ts < end:  # nua mo: phase dai 0 giay khong nuot timestamp nao
                return rid, phase
    return run_id, None


def collect_markers(root: Path) -> list[dict]:
    markers = [m for m in read_jsonl(metrics_dir(root) / "markers.jsonl") if parse_ts(m.get("ts"))]
    markers.sort(key=lambda m: parse_ts(m["ts"]))  # type: ignore[arg-type,return-value]
    return markers


def scope_at(markers: list[dict], times: list[datetime], ts: datetime) -> dict:
    lo, hi, idx = 0, len(times), -1
    while lo < hi:  # bisect_right
        mid = (lo + hi) // 2
        if times[mid] <= ts:
            lo = mid + 1
        else:
            hi = mid
    idx = lo - 1
    return markers[idx] if idx >= 0 else {}


def transcript_files(markers: list[dict], extra: list[str]) -> list[Path]:
    seen: dict[str, Path] = {}
    for raw in [m.get("transcript") for m in markers] + extra:
        if not raw:
            continue
        p = Path(raw)
        if p.is_file():
            seen[str(p.resolve())] = p
            sub = p.with_suffix("") / "subagents"
            if sub.is_dir():
                for s in sub.glob("*.jsonl"):
                    seen[str(s.resolve())] = s
    return list(seen.values())


def load_usage(paths: list[Path], screen_map: list[tuple[str, str]] | None = None) -> tuple[list[dict], list[datetime], int]:
    """Cac assistant turn (khu trung theo message.id), moc thoi gian hoat dong, va so turn hoi-dap thuong bi bo."""
    turns: dict[str, dict] = {}
    activity: list[tuple[datetime, int | None]] = []
    exchanges: dict[int, dict] = {}  # luot hoi-dap: tu 1 prompt cua nguoi den prompt ke tiep
    next_ex = 0
    for path in paths:
        cur: int | None = None  # file con (subagent) khong co prompt rieng -> khong bao gio bi coi la "thuong"
        for rec in read_jsonl(path):
            # 1. Antigravity format
            if rec.get("source") is not None:
                ts = parse_ts(rec.get("created_at"))
                source = rec.get("source")
                rec_type = rec.get("type")
                if source == "USER_EXPLICIT" and rec_type == "USER_INPUT":
                    text = human_prompt_text(rec)
                    if text is not None:
                        cur, next_ex = next_ex, next_ex + 1
                        exchanges[cur] = {"work": False, "force": forced_mode(text)}
                if cur is not None and source == "MODEL" and is_work_content(rec):
                    exchanges[cur]["work"] = True
                if ts and source in {"MODEL", "USER_EXPLICIT"}:
                    activity.append((ts, cur))
                if source != "MODEL" or not ts:
                    continue
                if rec.get("input_tokens") is None:
                    continue
                key = f"{path.resolve()}_{rec.get('step_index')}"
                tokens = {
                    "input_tokens": int(rec.get("input_tokens") or 0),
                    "output_tokens": int(rec.get("output_tokens") or 0),
                    "cache_read_input_tokens": int(rec.get("cache_read_tokens") or 0),
                    "cache_creation_input_tokens": 0,
                }
                screens = find_screens(rec, screen_map)
                model_name = rec.get("model")
                if key in turns:
                    first, seen = turns[key]["ts"], turns[key]["screens"] | screens
                    turns[key] = {"ts": first, "tokens": tokens, "model": model_name, "screens": seen, "ex": cur}
                else:
                    turns[key] = {"ts": ts, "tokens": tokens, "model": model_name, "screens": screens, "ex": cur}
                continue

            # 2. Claude Code format
            ts = parse_ts(rec.get("timestamp"))
            if rec.get("type") == "user" and not rec.get("isSidechain"):
                text = human_prompt_text(rec)
                if text is not None:
                    cur, next_ex = next_ex, next_ex + 1
                    exchanges[cur] = {"work": False, "force": forced_mode(text)}
            if cur is not None and rec.get("type") == "assistant" and is_work_content((rec.get("message") or {}).get("content")):
                exchanges[cur]["work"] = True
            if ts and rec.get("type") in {"assistant", "user"}:
                activity.append((ts, cur))
            if rec.get("type") != "assistant" or not ts:
                continue
            msg = rec.get("message") or {}
            usage = msg.get("usage")
            if not isinstance(usage, dict):
                continue
            key = str(msg.get("id") or rec.get("requestId") or rec.get("uuid"))
            tokens = {k: int(usage.get(k) or 0) for k in TOKEN_KEYS}
            screens = find_screens(msg.get("content"), screen_map)
            if key in turns:
                first, seen = turns[key]["ts"], turns[key]["screens"] | screens
                turns[key] = {"ts": first, "tokens": tokens, "model": msg.get("model"), "screens": seen, "ex": cur}
            else:
                turns[key] = {"ts": ts, "tokens": tokens, "model": msg.get("model"), "screens": screens, "ex": cur}

    activity.sort(key=lambda a: a[0])
    ordered = sorted(turns.values(), key=lambda t: t["ts"])
    # thoi gian cua turn = tu luc turn bat dau den luc turn ke tiep bat dau (gom sinh cau tra loi + chay cong cu),
    # cat toi da IDLE_CAP_SECONDS nhu "Active" cua phase; turn cuoi cung khong co turn sau nen tinh 0
    for i, t in enumerate(ordered):
        nxt = ordered[i + 1]["ts"] if i + 1 < len(ordered) else t["ts"]
        t["dur"] = min((nxt - t["ts"]).total_seconds(), IDLE_CAP_SECONDS)

    def ordinary(ex: int | None) -> bool:
        info = exchanges.get(ex) if ex is not None else None
        if info is None:
            return False
        return info["force"] == "skip" or (info["force"] != "keep" and not info["work"])

    kept = [t for t in ordered if not ordinary(t["ex"])]
    return kept, [ts for ts, ex in activity if not ordinary(ex)], len(ordered) - len(kept)


_TAG = re.compile(r"(?<![\w-])#(nolog|log)\b", re.I)
_HARNESS_CMD = re.compile(r"sdlc[_-]harness|phase_metrics", re.I)


def human_prompt_text(rec: dict) -> str | None:
    """Noi dung prompt do nguoi go; None neu la ket qua cong cu / ban tin he thong."""
    if rec.get("isMeta") or rec.get("toolUseResult") is not None:
        return None
    # Antigravity format
    if rec.get("source") == "USER_EXPLICIT" and rec.get("type") == "USER_INPUT":
        content = rec.get("content")
        if isinstance(content, str):
            m = re.search(r"<USER_REQUEST>\s*(.*?)\s*</USER_REQUEST>", content, re.DOTALL)
            return (m.group(1) if m else content).strip()
        return None
    # Claude Code format
    content = (rec.get("message") or {}).get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
            return None
        texts = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"]
        return "\n".join(texts) if texts else None
    return None


def forced_mode(prompt: str) -> str | None:
    """#nolog -> bo han luot nay; #log -> luon giu. Khong luu noi dung prompt o dau ca."""
    tags = [m.lower() for m in _TAG.findall(prompt or "")]
    return ("skip" if tags[-1] == "nolog" else "keep") if tags else None


def is_work_content(content) -> bool:
    """Luot co cong cu 'lam viec' (ghi/sua file, lenh harness, skill sdlc-*, subagent) khong phai hoi-dap thuong."""
    if isinstance(content, dict):
        tool_calls = content.get("tool_calls") or []
        for call in tool_calls:
            name = call.get("name")
            args = call.get("args") or {}
            if name in EDIT_TOOLS or name in {"Agent", "Task", "Workflow", "run_workflow", "invoke_subagent"}:
                return True
            if name in {"run_command", "Bash", "PowerShell"} and _HARNESS_CMD.search(str(args.get("CommandLine") or args.get("command") or "")):
                return True
        return False
    if not isinstance(content, list):
        return False
    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") == "tool_use":
            name, inp = block.get("name"), block.get("input") or {}
            if name in EDIT_TOOLS or name in {"Agent", "Task", "Workflow"}:
                return True
            if name == "Skill" and str(inp.get("skill", "")).startswith("sdlc-"):
                return True
            if name in {"Bash", "PowerShell"} and _HARNESS_CMD.search(str(inp.get("command", ""))):
                return True
        name = block.get("name")
        args = block.get("args") or {}
        if name in EDIT_TOOLS or name in {"run_workflow", "invoke_subagent"}:
            return True
        if name in {"run_command", "Bash", "PowerShell"} and _HARNESS_CMD.search(str(args.get("CommandLine") or args.get("command") or "")):
            return True
    return False


def load_screen_map(root: Path) -> list[tuple[str, str]]:
    """.claude/metrics/screen-map.json: {"src/features/trip/screens/*": "SCR-TRP-07"} - dung cho code khong chua ma SCR."""
    data = read_json(metrics_dir(root) / "screen-map.json")
    return [(norm_path(k), str(v)) for k, v in data.items()] if isinstance(data, dict) else []


def find_screens(content, screen_map: list[tuple[str, str]]) -> set[str]:
    """Ma SCR-xxx-nn nam trong cac tool_use cua turn (duong dan, noi dung, lenh); them anh xa theo glob file."""
    found: set[str] = set()
    items = []
    if isinstance(content, list):
        items = content
    elif isinstance(content, dict):
        items = content.get("tool_calls") or []
        text_content = content.get("content")
        if isinstance(text_content, str):
            found.update(SCREEN_RE.findall(text_content))

    for block in items:
        if not isinstance(block, dict):
            continue
        inp = block.get("input") or block.get("args") or {}
        found.update(SCREEN_RE.findall(json.dumps(inp, ensure_ascii=False)))
        target = inp.get("file_path") or inp.get("notebook_path") or inp.get("Path")
        if target and screen_map:
            path = norm_path(str(target))
            found.update(scr for pattern, scr in screen_map if fnmatch(path, "*" + pattern.lstrip("*")))
    return found


def active_seconds_between(activity: list[datetime], start: datetime, end: datetime) -> float:
    total, prev = 0.0, None
    for ts in activity:
        if ts < start:
            continue
        if ts >= end:
            break
        if prev is not None:
            total += min((ts - prev).total_seconds(), IDLE_CAP_SECONDS)
        prev = ts
    return total


def fmt_dur(seconds: float) -> str:
    seconds = int(round(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}h{m:02d}m{s:02d}s" if h else (f"{m}m{s:02d}s" if m else f"{s}s")


def blank() -> dict:
    return {"turns": 0, **{k: 0 for k in TOKEN_KEYS}, "wall": 0.0, "active": 0.0, "visits": 0}


def add_tokens(bucket: dict, tokens: dict) -> None:
    bucket["turns"] += 1
    for k in TOKEN_KEYS:
        bucket[k] += tokens[k]


def total_tokens(b: dict) -> int:
    return sum(b[k] for k in TOKEN_KEYS)


def build_report(root: Path, run_filter: str | None, extra_transcripts: list[str]) -> dict:
    timeline = phase_timeline(root)
    if run_filter:
        timeline = {k: v for k, v in timeline.items() if k == run_filter}
    markers = collect_markers(root)
    times = [parse_ts(m["ts"]) for m in markers]  # type: ignore[misc]
    turns, activity, skipped = load_usage(transcript_files(markers, extra_transcripts), load_screen_map(root))

    phases: dict[tuple[str, str], dict] = defaultdict(blank)
    tasks: dict[tuple[str, str, str], dict] = defaultdict(blank)
    models: dict[str, dict] = defaultdict(blank)
    phase_models: dict[tuple[str, str, str], dict] = defaultdict(blank)
    screens: dict[str, dict] = defaultdict(lambda: {**blank(), "phases": set()})
    sticky: tuple[str, datetime, str | None] | None = None  # (man hinh, thoi diem, phase) cua turn truoc
    unattributed = blank()
    grand = blank()

    # thoi gian: theo events.jsonl (phase) - wall = ca thoi gian cho nguoi; active = cat khoang lang
    for rid, segs in timeline.items():
        for start, end, phase in segs:
            b = phases[(rid, phase)]
            b["visits"] += 1
            b["wall"] += (end - start).total_seconds()
            b["active"] += active_seconds_between(activity, start, end)

    # token + thoi gian theo task: gan moi turn vao scope cua marker gan nhat truoc no
    for turn in turns:
        ts = turn["ts"]
        sc = scope_at(markers, times, ts)  # type: ignore[arg-type]
        rid, phase = lookup_phase(timeline, sc.get("run_id"), ts)
        add_tokens(grand, turn["tokens"])

        # --- man hinh: chia deu neu turn nhac 2-3 man hinh; >3 la viec cap module; khong nhac thi ke thua man hinh truoc
        found = sorted(turn["screens"])
        if 1 <= len(found) <= MAX_SPLIT:
            share = [(s, 1 / len(found)) for s in found]
            sticky = (found[0], ts, phase) if len(found) == 1 else None
        elif len(found) > MAX_SPLIT:
            share, sticky = [(MULTI_SCREEN, 1.0)], None
        elif sticky and phase == sticky[2] and (ts - sticky[1]).total_seconds() <= STICKY_GAP:
            share, sticky = [(sticky[0], 1.0)], (sticky[0], ts, phase)
        else:
            share = [(NO_SCREEN, 1.0)]
        for name, w in share:
            sb = screens[name]
            sb["turns"] += w
            for k in TOKEN_KEYS:
                sb[k] += w * turn["tokens"][k]
            sb["active"] += w * turn["dur"]
            sb["phases"].add(phase or "-")

        if not (run_filter and rid != run_filter):
            model_name = str(turn.get("model") or "(khong ro model)")
            mb = models[model_name]
            add_tokens(mb, turn["tokens"])
            mb["active"] += turn["dur"]

        if rid is None or phase is None or (run_filter and rid != run_filter):
            add_tokens(unattributed, turn["tokens"])
            continue
        add_tokens(phases[(rid, phase)], turn["tokens"])
        pmb = phase_models[(rid, phase, model_name)]
        add_tokens(pmb, turn["tokens"])
        pmb["active"] += turn["dur"]
        task = sc.get("task") if sc.get("run_id") in (rid, None) else None
        add_tokens(tasks[(rid, phase, task or "(khong gan task)")], turn["tokens"])

    # thoi gian theo task: cat timeline thanh cac doan theo marker, giao voi doan phase
    for i, m in enumerate(markers):
        start = times[i]
        end = times[i + 1] if i + 1 < len(markers) else datetime.now(timezone.utc)
        if start is None or end is None or end <= start:
            continue
        rid = m.get("run_id")
        if rid not in timeline:
            continue
        for p_start, p_end, phase in timeline[rid]:
            lo, hi = max(start, p_start), min(end, p_end)
            if hi > lo:
                b = tasks[(rid, phase, m.get("task") or "(khong gan task)")]
                b["wall"] += (hi - lo).total_seconds()
                b["active"] += active_seconds_between(activity, lo, hi)

    return {"generated_at": now_iso(), "root": str(root), "markers": len(markers), "transcripts": len(turns),
            "phases": phases, "tasks": tasks, "models": models, "phase_models": phase_models,
            "screens": screens, "unattributed": unattributed, "grand": grand, "skipped_turns": skipped,
            "order": {rid: [p for _, _, p in segs] for rid, segs in timeline.items()}}


def metric_cells(b: dict) -> list[str]:
    return [fmt_dur(b["active"]), str(b["turns"]), f"{b['input_tokens']:,}",
            f"{b['output_tokens']:,}", f"{b['cache_read_input_tokens']:,}",
            f"{b['cache_creation_input_tokens']:,}", f"{total_tokens(b):,}"]


def row(label: list[str], b: dict) -> list[str]:
    return [*label, fmt_dur(b["wall"]), *metric_cells(b)]


def md_table(head: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(out)


def render_markdown(rep: dict) -> str:
    cols = ["Wall", "Active", "Turns", "Input", "Output", "Cache read", "Cache write", "Tong token"]
    lines = [f"# Do luong theo phase / task ({rep['generated_at']})", "",
             f"- Markers: {rep['markers']} | Assistant turns doc duoc: {rep['transcripts']} | "
             f"Turn hoi-dap thuong da bo qua: {rep['skipped_turns']} (khong tinh vao bang nao)",
             "- **Wall** = tu luc vao phase den luc roi phase (gom ca thoi gian cho nguoi duyet).",
             f"- **Active** = tong cac khoang giua hai su kien transcript, moi khoang toi da {IDLE_CAP_SECONDS // 60} phut.",
             "- **Tong token** = input + output + cache read + cache write (cache read re hon nhieu so voi input thuong).",
             ""]
    phase_rows: list[list[str]] = []
    for rid, order in rep["order"].items():
        seen: list[str] = []
        for ph in order:
            if ph not in seen:
                seen.append(ph)
        for ph in seen:
            b = rep["phases"][(rid, ph)]
            phase_rows.append(row([rid, ph, str(b["visits"])], b))
    lines += ["## Theo phase", "", md_table(["Run", "Phase", "Luot", *cols], phase_rows), ""]

    task_rows = [row([rid, ph, task], b) for (rid, ph, task), b in sorted(rep["tasks"].items())
                 if b["turns"] or b["active"]]
    lines += ["## Theo task", ""]
    lines += [md_table(["Run", "Phase", "Task", *cols], task_rows) if task_rows else "_Chua co du lieu task._", ""]

    no_wall_cols = cols[1:]
    model_rows = [[m, *metric_cells(b)] for m, b in sorted(rep["models"].items(), key=lambda x: -total_tokens(x[1]))]
    lines += ["## Theo model", ""]
    lines += [md_table(["Model", *no_wall_cols], model_rows) if model_rows else "_Chua co du lieu model._", ""]

    pm_rows = [[rid, ph, m, *metric_cells(b)] for (rid, ph, m), b in sorted(rep["phase_models"].items())]
    lines += ["## Theo phase & model", ""]
    lines += [md_table(["Run", "Phase", "Model", *no_wall_cols], pm_rows) if pm_rows else "_Chua co du lieu._", ""]

    scr_cols = ["Phase", "Turns", "Active", "Output", "Cache read", "Tong token"]
    real = sorted(((n, b) for n, b in rep["screens"].items() if n.startswith("SCR-")),
                  key=lambda x: -total_tokens(x[1]))
    other = [(n, b) for n, b in rep["screens"].items() if not n.startswith("SCR-")]
    scr_rows = [[n, ", ".join(sorted(b["phases"])), f"{b['turns']:.1f}", fmt_dur(b["active"]),
                 f"{b['output_tokens']:,.0f}", f"{b['cache_read_input_tokens']:,.0f}", f"{total_tokens(b):,.0f}"]
                for n, b in [*real, *other]]
    lines += ["## Theo man hinh (SCR)", "",
              "_Gan theo ma SCR-xxx-nn trong cac lenh agent goi (duong dan, noi dung, lenh). Turn nhac 2-3 man hinh chia deu; "
              f"nhac hon {MAX_SPLIT} thi tinh vao cap module. Khai bao them o `.claude/metrics/screen-map.json`._", "",
              md_table(["Man hinh", *scr_cols], scr_rows) if scr_rows else "_Chua phat hien ma man hinh nao._", ""]

    un = rep["unattributed"]
    if un["turns"]:
        lines += [f"> {un['turns']} turn ({total_tokens(un):,} token) khong gan duoc vao phase nao "
                  "(xay ra truoc khi run duoc tao hoac ngoai moi run).", ""]
    g = rep["grand"]
    lines += [f"**Tong cong:** {g['turns']} turn, {total_tokens(g):,} token "
              f"(input {g['input_tokens']:,}, output {g['output_tokens']:,}, "
              f"cache read {g['cache_read_input_tokens']:,}, cache write {g['cache_creation_input_tokens']:,})"]
    return "\n".join(lines) + "\n"


def to_jsonable(rep: dict) -> dict:
    def flat(d: dict) -> list[dict]:
        return [{"key": list(k) if isinstance(k, tuple) else k, **v} for k, v in d.items()]
    screens = [{"screen": k, **{**v, "phases": sorted(v["phases"])}} for k, v in rep["screens"].items()]
    return {**rep, "phases": flat(rep["phases"]), "tasks": flat(rep["tasks"]),
            "models": flat(rep["models"]), "phase_models": flat(rep["phase_models"]), "screens": screens}


def report_main(args: argparse.Namespace) -> int:
    root = project_root()
    rep = build_report(root, args.run, args.transcript or [])
    text = json.dumps(to_jsonable(rep), ensure_ascii=False, indent=2) if args.format == "json" else render_markdown(rep)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"da ghi {out}")
    else:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        print(text)
    return 0


# --------------------------------------------------------------------------- entry
def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] == "hook":
        return hook_main()
    parser = argparse.ArgumentParser(prog="phase_metrics")
    sub = parser.add_subparsers(dest="cmd", required=True)
    rp = sub.add_parser("report", help="in bao cao thoi gian/token theo phase va task")
    rp.add_argument("--run", help="chi lay 1 run-id")
    rp.add_argument("--format", choices=["md", "json"], default="md")
    rp.add_argument("--out", help="ghi ra file thay vi in ra man hinh")
    rp.add_argument("--transcript", action="append", help="them transcript .jsonl cu (co the lap lai)")
    tp = sub.add_parser("task", help="danh dau task dang lam")
    tp.add_argument("action", choices=["start", "end", "show"])
    tp.add_argument("task_id", nargs="?")
    args = parser.parse_args(argv)
    return report_main(args) if args.cmd == "report" else task_main(args)


if __name__ == "__main__":
    sys.exit(main())
