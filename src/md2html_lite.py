# -*- coding: utf-8 -*-
import re, html
E = html.escape


def inl(x):
    x = E(x)
    x = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", x)
    return re.sub(r"`(.+?)`", r"<code>\1</code>", x)


def md2html(text):
    out, i, L = [], 0, text.splitlines()
    num = re.compile(r"^\d+\. ")
    while i < len(L):
        l = L[i]
        if l.startswith("# "):
            i += 1; continue
        if l.startswith("## "):
            out.append(f"<h3>{inl(l[3:])}</h3>"); i += 1; continue
        if l.startswith("|"):
            rows = []
            while i < len(L) and L[i].startswith("|"):
                cells = [c.strip() for c in L[i].strip().strip("|").split("|")]
                if not all(set(c) <= set("-: ") for c in cells):
                    rows.append(cells)
                i += 1
            h = "".join(f"<th>{inl(c)}</th>" for c in rows[0])
            b = "".join("<tr>" + "".join(f"<td>{inl(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
            out.append(f'<div class="tablebox"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>')
            continue
        if num.match(l):
            items = []
            while i < len(L) and num.match(L[i]):
                t = num.sub("", L[i]); i += 1
                while i < len(L) and L[i].startswith("   "):
                    t += " " + L[i].strip(); i += 1
                items.append(f"<li>{inl(t)}</li>")
            out.append('<ol class="pr">' + "".join(items) + "</ol>")
            continue
        if l.strip():
            t = l; i += 1
            while i < len(L) and L[i].strip() and not L[i].startswith(("#", "|")) and not num.match(L[i]):
                t += " " + L[i].strip(); i += 1
            out.append(f'<p class="lede">{inl(t)}</p>')
            continue
        i += 1
    return "\n".join(out)
