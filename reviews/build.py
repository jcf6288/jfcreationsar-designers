# Rebuilds reviews/index.html from reviews/data.json.  Usage: python3 -I reviews/build.py
import json, html, datetime, os
here=os.path.dirname(os.path.abspath(__file__))
D=json.load(open(os.path.join(here,"data.json"),encoding="utf-8"))
MIN_STARS=D["min_stars"]
GOOGLE=[(g["name"],g["text"]) for g in D["google"]]
EBAY=D["ebay"]["comments"]
EB_POS=D["ebay"]["positive"]; EB_N=D["ebay"]["ratings"]
d=D["etsy"]
n=len(d); avg=sum(x["stars"] for x in d)/n
rows=[]
for x in d:
    m=x["message"].strip()
    if not m or x["stars"]<MIN_STARS: continue
    rows.append((datetime.datetime.strptime(x["date"],"%m/%d/%Y"),x["stars"],x["name"],m))
rows.sort(reverse=True)
e=html.escape
def card(who,txt,src,stars=5,date=None):
    meta=f"{src}"+(f" · {date.strftime('%B %Y')}" if date else "")
    return f'<article class="r"><p class="s" aria-label="{stars} out of 5 stars">{"★"*stars}{"☆"*(5-stars)}</p><p class="t">{e(txt)}</p><p class="m">— {e(who)} · {e(meta)}</p></article>'
eb="\n".join(card("eBay buyer",t,"eBay feedback") for t in EBAY)
g="\n".join(card(w,t,"Google review") for w,t in GOOGLE)
et="\n".join(card(w,t,"Etsy review",s,dt) for dt,s,w,t in rows)
page=f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Customer Reviews | JFCreationsAR Custom Laser Engraving, Redfield, Arkansas</title>
<meta name="description" content="Read real customer reviews of JFCreationsAR, a veteran-owned custom laser engraving business in Redfield, Arkansas. BBB Accredited, A+ rating.">
<style>
body{{font-family:Georgia,serif;max-width:820px;margin:0 auto;padding:20px;color:#222;line-height:1.5}}
h1{{margin-bottom:4px}} .sum{{background:#f4f1ea;padding:14px 18px;border-radius:8px;margin:14px 0}}
.r{{border-bottom:1px solid #ddd;padding:12px 0}} .s{{color:#b8860b;margin:0;letter-spacing:2px}}
.t{{margin:4px 0}} .m{{margin:0;color:#666;font-size:.9em}} a{{color:#8a5a00}}
</style></head><body>
<h1>JFCreationsAR Customer Reviews</h1>
<p>Veteran-owned custom laser engraving in Redfield, Arkansas, serving Central Arkansas and shipping nationwide.</p>
<div class="sum"><p><strong>Etsy:</strong> rated {avg:.2f} out of 5 across {n} reviews. <strong>eBay:</strong> {EB_POS} positive feedback, {EB_N} ratings. <strong>Google:</strong> {D['google_rating']} stars. <strong>BBB:</strong> <a href="https://www.bbb.org/us/ar/redfield/profile/custom-gifts/jfcreationsar-0935-90410944">BBB Accredited Business, A+ rating</a>.</p>
<p>Reviews below are copied word for word from the customers' own posts. Customer names are shortened for privacy.</p></div>
<h2>Google reviews</h2>
{g}
<h2>eBay feedback</h2>
{eb}
<h2>Etsy reviews</h2>
<p>Our Etsy shop is closed while we focus on our own website. These reviews are from customers who ordered while it was open.</p>
{et}
<p><a href="https://www.jfcreationsar.com">Back to JFCreationsAR.com</a></p>
</body></html>'''
open(os.path.join(here,"index.html"),"w",encoding="utf-8",newline="\n").write(page)
print(n,round(avg,2),len(rows),len(GOOGLE))
