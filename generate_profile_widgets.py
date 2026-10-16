#!/usr/bin/env python3
"""Generate honest local profile cards from the public GitHub REST API."""
from __future__ import annotations
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
import html, json, os, sys, urllib.error, urllib.request

USER = "ShadinWorld"
API = "https://api.github.com"
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
TOKEN = os.environ.get("GITHUB_TOKEN", "")


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def api_get(path: str):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "Mosharof-Profile-Widgets", "X-GitHub-Api-Version": "2022-11-28"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(API + path, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def svg_shell(width: int, height: int, title: str, subtitle: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">',
        '<defs><linearGradient id="neon" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#39f6e8"/><stop offset="0.52" stop-color="#a78bfa"/><stop offset="1" stop-color="#ffbd69"/></linearGradient><linearGradient id="bar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#39f6e8"/><stop offset="1" stop-color="#6366f1"/></linearGradient></defs>',
        '<rect width="100%" height="100%" rx="22" fill="#0b111b" stroke="#263346" stroke-width="2"/>',
        '<path d="M24 82 H1176" stroke="url(#neon)" stroke-width="2"/>',
        f'<text x="36" y="42" fill="#39f6e8" font-family="Segoe UI,Arial,sans-serif" font-size="15" font-weight="700" letter-spacing="2">{esc(title.upper())}</text>',
        f'<text x="36" y="66" fill="#aab8ca" font-family="Segoe UI,Arial,sans-serif" font-size="13">{esc(subtitle)}</text>',
    ]


def write_activity(events: list[dict], today):
    days = [today - timedelta(days=29-i) for i in range(30)]
    counts = Counter()
    for event in events:
        try:
            d = datetime.fromisoformat(event["created_at"].replace("Z", "+00:00")).date()
            if days[0] <= d <= days[-1]: counts[d] += 1
        except (KeyError, TypeError, ValueError):
            continue
    peak = max(counts.values(), default=0)
    out = svg_shell(1200, 360, "Recent public activity", "Visible public GitHub events over the most recent 30 days")
    left, baseline, plot_h, step, bar_w = 48, 276, 145, 36, 19
    for frac in (0, .25, .5, .75, 1):
        y = baseline - int(plot_h*frac)
        out.append(f'<line x1="{left}" y1="{y}" x2="1150" y2="{y}" stroke="#273447" stroke-width="1"/>')
    for i, day in enumerate(days):
        value = counts.get(day, 0)
        h = 4 if peak == 0 else max(5, int(value/peak*plot_h))
        x = left + i*step
        out.append(f'<rect x="{x}" y="{baseline-h}" width="{bar_w}" height="{h}" rx="4" fill="{"url(#bar)" if value else "#1a2635"}"/>')
    for idx in (0, 7, 14, 21, 29):
        out.append(f'<text x="{left+idx*step}" y="305" fill="#92a1b5" font-family="Segoe UI,Arial,sans-serif" font-size="12">{days[idx].strftime("%b %d")}</text>')
    total = sum(counts.values())
    active_days = sum(1 for d in days if counts.get(d, 0))
    out.append(f'<text x="1150" y="42" text-anchor="end" fill="#e6edf3" font-family="Segoe UI,Arial,sans-serif" font-size="14" font-weight="700">{total} visible events · {active_days} active days</text>')
    out.append('<text x="36" y="340" fill="#6f8097" font-family="Segoe UI,Arial,sans-serif" font-size="11">Public events only; this is not a count of private or all contribution-calendar activity.</text>')
    out.append('</svg>')
    (ASSETS/"public-activity.svg").write_text("\n".join(out)+"\n", encoding="utf-8")


def write_footprint(profile: dict, repos: list[dict], generated_at: str):
    repo_count = int(profile.get("public_repos") or 0)
    followers = int(profile.get("followers") or 0)
    stars = sum(int(r.get("stargazers_count") or 0) for r in repos)
    forks = sum(int(r.get("forks_count") or 0) for r in repos)
    values = [("PUBLIC REPOSITORIES", repo_count, "Owned public repositories"), ("FOLLOWERS", followers, "People following the profile"), ("REPOSITORY STARS", stars, "Stars across owned public repos"), ("FORKS", forks, "Forks across owned public repos")]
    out = svg_shell(1200, 275, "Public profile footprint", f"Public GitHub API snapshot · refreshed {generated_at} UTC")
    x0, y, width, height, gap = 42, 105, 267, 120, 15
    for i,(label,val,note) in enumerate(values):
        x = x0 + i*(width+gap)
        out.extend([f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="14" fill="#101a29" stroke="#2d3b50"/>', f'<path d="M{x+15} {y+4} H{x+width-15}" stroke="url(#neon)" stroke-width="4"/>', f'<text x="{x+16}" y="{y+32}" fill="#aab8ca" font-family="Segoe UI,Arial,sans-serif" font-size="11" font-weight="700">{esc(label)}</text>', f'<text x="{x+16}" y="{y+78}" fill="#f1f5f9" font-family="Segoe UI,Arial,sans-serif" font-size="34" font-weight="700">{val:,}</text>', f'<text x="{x+16}" y="{y+103}" fill="#7e8da3" font-family="Segoe UI,Arial,sans-serif" font-size="10">{esc(note)}</text>'])
    out.append('<text x="42" y="253" fill="#6f8097" font-family="Segoe UI,Arial,sans-serif" font-size="11">Snapshot of public profile and owned public repository totals; excludes private activity.</text>')
    out.append('</svg>')
    (ASSETS/"profile-footprint.svg").write_text("\n".join(out)+"\n", encoding="utf-8")


def write_languages(repos: list[dict], languages: dict[str, int], generated_at: str):
    total = sum(languages.values())
    items = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:7]
    palette = ["#39f6e8", "#a78bfa", "#ffbd69", "#60a5fa", "#f472b6", "#34d399", "#f87171"]
    out = svg_shell(1200, 300, "Language footprint", f"Source bytes in owned public repositories · refreshed {generated_at} UTC")
    if total == 0 or not items:
        out.append('<text x="42" y="150" fill="#e6edf3" font-family="Segoe UI,Arial,sans-serif" font-size="18">No language data was returned for the public repositories.</text>')
        out.append('<text x="42" y="180" fill="#8b949e" font-family="Segoe UI,Arial,sans-serif" font-size="13">The workflow will try again on its next run.</text>')
    else:
        x, y, fullw, h = 42, 112, 1116, 18
        cursor = x
        for i,(name,size) in enumerate(items):
            w = fullw*size/total
            out.append(f'<rect x="{cursor:.2f}" y="{y}" width="{max(1,w):.2f}" height="{h}" rx="3" fill="{palette[i%len(palette)]}"/>')
            cursor += w
        for i,(name,size) in enumerate(items):
            col=i%4; row=i//4; x0=45+col*285; y0=165+row*48
            pct=size/total*100
            out.append(f'<circle cx="{x0}" cy="{y0-4}" r="5" fill="{palette[i%len(palette)]}"/>')
            out.append(f'<text x="{x0+14}" y="{y0}" fill="#e6edf3" font-family="Segoe UI,Arial,sans-serif" font-size="13" font-weight="600">{esc(name)}</text>')
            out.append(f'<text x="{x0+14}" y="{y0+18}" fill="#8b949e" font-family="Segoe UI,Arial,sans-serif" font-size="11">{pct:.1f}% of reported source bytes</text>')
    out.append('<text x="42" y="278" fill="#6f8097" font-family="Segoe UI,Arial,sans-serif" font-size="11">Languages are calculated from GitHub repository language metadata; percentages are not a measure of skill.</text>')
    out.append('</svg>')
    (ASSETS/"language-breakdown.svg").write_text("\n".join(out)+"\n", encoding="utf-8")


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    try:
        profile = api_get(f"/users/{USER}")
        repos = api_get(f"/users/{USER}/repos?per_page=100&type=owner&sort=updated")
        events = api_get(f"/users/{USER}/events/public?per_page=100")
        if not isinstance(profile, dict) or not isinstance(repos, list) or not isinstance(events, list):
            raise RuntimeError("The GitHub API returned an unexpected response type.")
        owned = [r for r in repos if not r.get("fork", False)]
        language_totals = Counter()
        for repo in owned:
            name = repo.get("name")
            if not name: continue
            language_map = api_get(f"/repos/{USER}/{name}/languages")
            if isinstance(language_map, dict):
                language_totals.update({k:int(v) for k,v in language_map.items() if isinstance(v, (int,float))})
        now = datetime.now(timezone.utc)
        generated = now.strftime("%Y-%m-%d %H:%M")
        write_activity(events, now.date())
        write_footprint(profile, owned, generated)
        write_languages(owned, dict(language_totals), generated)
        print(f"Updated 3 local cards from public GitHub API: profile, {len(owned)} owned repositories, {len(events)} public events, {len(language_totals)} languages.")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError, RuntimeError) as exc:
        print(f"Could not refresh all profile cards: {exc}", file=sys.stderr)
        print("Existing SVG cards were left in place; try running this workflow again later.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
