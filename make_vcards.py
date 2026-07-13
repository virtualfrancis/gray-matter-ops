"""Generate the .vcf files for the team contact page.

This list is the single source of truth for contact details. Fill in the real values,
run `python3 make_vcards.py`, then mirror the same values into index.html and delete
the <span class="ph"> wrappers around them.

Emits one vCard per person plus a combined file, so "Save our contacts" drops all four
into the visitor's phone in a single tap.
"""
import os

SITE = "https://virtualfrancis.github.io/gray-matter-ops/"

# ---- FILL THESE IN -----------------------------------------------------------
# file      first     last          role                       email
TEAM = [
    ("vicky",  "Vicky",  "[LAST NAME]", "[ROLE]", ""),
    ("tyler",  "Tyler",  "[LAST NAME]", "[ROLE]", ""),
    ("justin", "Justin", "[LAST NAME]", "[ROLE]", ""),
    ("taylor", "Taylor", "Gow",         "[ROLE]", ""),
]
# ------------------------------------------------------------------------------

NOTE = ("Gray Matter Ops, Duke Design Defense Studio 2026. X49: a localized, opioid-free "
        "nanofiber for prolonged field care.")


def vcard(first, last, role, email):
    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"N:{last};{first};;;",
        f"FN:{first} {last}",
        "ORG:Gray Matter Ops;",
    ]
    if role and not role.startswith("["):
        lines.append(f"TITLE:{role}")
    if email:
        lines.append(f"EMAIL;TYPE=INTERNET,PREF:{email}")
    lines += [f"URL:{SITE}", f"NOTE:{NOTE}", "END:VCARD"]
    return "\r\n".join(lines) + "\r\n"   # vCard spec requires CRLF


out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vcf")
os.makedirs(out, exist_ok=True)

combined, missing = [], []
for slug, first, last, role, email in TEAM:
    card = vcard(first, last, role, email)
    with open(f"{out}/{slug}.vcf", "w", newline="") as f:
        f.write(card)
    combined.append(card)
    if not email:
        missing.append(first)

with open(f"{out}/gray-matter-ops.vcf", "w", newline="") as f:
    f.write("".join(combined))

print(f"wrote {len(TEAM)} vcards + combined -> {out}")
if missing:
    print(f"WARNING: no email yet for {', '.join(missing)}. "
          f"These cards will save a name but no way to reach them.")
