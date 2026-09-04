import os
import json
from datetime import datetime, timezone
from urllib import request as urlrequest
from urllib.error import HTTPError

from flask import Flask, Response, jsonify, request

app = Flask(__name__)

APP_VERSION = "responsive-rfp-hiring-surge-v2-simple"
MAX_ACCOUNTS = 5

HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Responsive · RFP Hiring Surge</title>
<meta name="description" content="Find companies expanding proposal and RFP teams, then turn the signal into seller-ready outreach." />
<style>
:root{
  --bg:#f5f7f5;
  --surface:#ffffff;
  --ink:#142019;
  --muted:#6e7b72;
  --line:#dde4df;
  --deep:#173d2c;
  --mint:#8be8ba;
  --mint-soft:#eaf9f1;
  --blue:#536dff;
  --blue-soft:#edf0ff;
  --amber:#eea14b;
  --shadow:0 18px 56px rgba(20,32,25,.075);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
html,body{
  margin:0;background:var(--bg);color:var(--ink);
  font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif
}
body{
  min-height:100vh;
  background:
    radial-gradient(circle at 90% 0%,rgba(83,109,255,.08),transparent 24%),
    radial-gradient(circle at 2% 22%,rgba(139,232,186,.13),transparent 22%),
    var(--bg)
}
button,input,select{font:inherit}
button{cursor:pointer}
a{color:inherit}
.shell{max-width:1060px;margin:0 auto;padding:24px 24px 50px}

/* header */
header{
  display:flex;justify-content:space-between;align-items:center;
  padding-bottom:20px;border-bottom:1px solid var(--line)
}
.brand{display:flex;align-items:center;gap:10px}
.logo{
  width:38px;height:38px;border-radius:11px;background:var(--deep);
  color:var(--mint);display:grid;place-items:center;font-weight:950
}
.brand small{
  display:block;font-size:8px;letter-spacing:.14em;font-weight:900;color:var(--muted)
}
.brand strong{display:block;font-size:16px;margin-top:2px;letter-spacing:-.025em}
.live{
  display:flex;gap:7px;align-items:center;font-size:8.5px;color:var(--muted);
  border:1px solid var(--line);border-radius:999px;padding:7px 9px;background:rgba(255,255,255,.8)
}
.live i{width:7px;height:7px;border-radius:50%;background:#55d599}

/* hero */
.hero{padding:58px 0 30px;max-width:850px}
.kicker{
  font-size:8.5px;letter-spacing:.16em;text-transform:uppercase;
  font-weight:900;color:var(--blue)
}
.hero h1{
  font-size:58px;line-height:.99;letter-spacing:-.055em;
  margin:13px 0 17px;max-width:830px
}
.hero h1 em{font-style:normal;color:var(--deep);position:relative;white-space:nowrap}
.hero h1 em:after{
  content:"";position:absolute;left:0;right:0;bottom:2px;height:9px;
  border-radius:999px;background:var(--mint);z-index:-1;transform:rotate(-.7deg)
}
.hero p{
  margin:0;max-width:730px;font-size:15.5px;line-height:1.65;color:var(--muted)
}

/* search */
.search-card{
  background:var(--surface);border:1px solid var(--line);
  border-radius:19px;padding:16px;box-shadow:var(--shadow)
}
.search-row{
  display:grid;grid-template-columns:1fr 1fr .8fr auto;gap:9px;align-items:end
}
.field label{
  display:block;font-size:7.5px;letter-spacing:.11em;text-transform:uppercase;
  color:#7d8980;font-weight:900;margin-bottom:6px
}
.field select{
  width:100%;border:1px solid var(--line);border-radius:10px;
  background:#fbfcfb;padding:10px 11px;color:var(--ink);font-size:10.3px;outline:none
}
.field select:focus{border-color:#a5b1ff;box-shadow:0 0 0 3px rgba(83,109,255,.07)}
.run{
  height:39px;border:0;border-radius:10px;background:var(--deep);color:white;
  padding:0 15px;font-size:9.5px;font-weight:900;white-space:nowrap
}
.run:hover{background:#224d39}
.run:disabled{opacity:.55;cursor:wait}
.warning{
  display:none;margin-top:10px;border-radius:10px;padding:9px 10px;
  background:#fff1f2;border:1px solid #ecc8cc;color:#963f49;
  font-size:8.7px;line-height:1.45
}

/* results */
.results-wrap{margin-top:27px}
.section-head{
  display:flex;justify-content:space-between;gap:20px;align-items:end;margin-bottom:11px
}
.section-head small{
  display:block;font-size:7.5px;letter-spacing:.13em;text-transform:uppercase;
  color:#858f87;font-weight:900;margin-bottom:5px
}
.section-head h2{font-size:21px;letter-spacing:-.035em;margin:0}
.section-head p{margin:0;max-width:390px;text-align:right;font-size:8.8px;line-height:1.5;color:var(--muted)}
.accounts{display:flex;flex-direction:column;gap:8px}
.empty{
  background:rgba(255,255,255,.65);border:1px dashed var(--line);
  border-radius:15px;padding:34px;text-align:center;color:var(--muted);font-size:9.5px
}
.account{
  display:grid;grid-template-columns:52px minmax(0,1fr) 250px auto;
  gap:12px;align-items:center;background:var(--surface);border:1px solid var(--line);
  border-radius:15px;padding:11px;box-shadow:0 8px 28px rgba(20,32,25,.03)
}
.score{
  width:43px;height:43px;border-radius:50%;background:var(--deep);color:var(--mint);
  display:grid;place-items:center;font-size:12px;font-weight:950
}
.company strong{display:block;font-size:10.8px;margin-bottom:3px}
.company span{display:block;font-size:8.5px;color:var(--muted)}
.tags{display:flex;gap:4px;flex-wrap:wrap;margin-top:6px}
.tag{
  border-radius:999px;padding:4px 6px;background:var(--blue-soft);color:#4856a2;
  font-size:7.1px;font-weight:850
}
.why{border-left:1px solid var(--line);padding-left:12px;min-width:0}
.why b{
  display:block;font-size:7px;letter-spacing:.09em;text-transform:uppercase;
  color:#879189;margin-bottom:4px
}
.why p{margin:0;font-size:8.8px;line-height:1.45;color:#566159}
.source{
  display:inline-block;margin-top:5px;max-width:100%;
  font-size:7.2px;color:var(--blue);font-weight:850;text-decoration:none;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis
}
.source:hover{text-decoration:underline}
.generate{
  border:1px solid var(--line);background:#fbfcfb;color:var(--ink);
  border-radius:9px;padding:8px 9px;font-size:7.8px;font-weight:900;white-space:nowrap
}
.generate:hover{border-color:#aeb8b1;background:white}

/* outreach */
.outreach{
  display:none;margin-top:14px;background:var(--surface);border:1px solid var(--line);
  border-radius:18px;padding:17px;box-shadow:var(--shadow)
}
.outreach.active{display:block}
.outreach-top{display:flex;justify-content:space-between;gap:20px;align-items:flex-start}
.outreach-top small{
  display:block;font-size:7.5px;letter-spacing:.12em;text-transform:uppercase;
  color:#858f87;font-weight:900;margin-bottom:5px
}
.outreach-top h3{font-size:18px;letter-spacing:-.03em;margin:0}
.persona{
  background:var(--mint-soft);color:#285d44;border-radius:999px;
  padding:6px 8px;font-size:7.5px;font-weight:900
}
.outreach-grid{display:grid;grid-template-columns:.72fr 1.28fr;gap:11px;margin-top:12px}
.angle{
  background:var(--deep);color:white;border-radius:14px;padding:14px
}
.angle small{font-size:7px;letter-spacing:.1em;color:var(--mint);font-weight:900}
.angle h4{font-size:15px;letter-spacing:-.025em;margin:7px 0 6px}
.angle p{font-size:9px;line-height:1.5;color:#b7c7bd;margin:0}
.angle hr{border:0;border-top:1px solid #315140;margin:11px 0}
.angle b{display:block;font-size:7px;color:#8fa899;letter-spacing:.08em;margin-bottom:4px}
.angle span{display:block;font-size:8.9px;line-height:1.45;color:#edf3ef}
.message{
  border:1px solid var(--line);border-radius:14px;background:#fbfcfb;padding:13px
}
.message-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:9px}
.message-head strong{font-size:9.3px}
.copy{
  border:0;border-radius:8px;background:var(--blue-soft);color:#4b5aaa;
  padding:6px 8px;font-size:7.3px;font-weight:900
}
.subject{font-size:8.2px;font-weight:900;color:#5b665e;margin-bottom:9px}
.email{white-space:pre-wrap;margin:0;font-size:10px;line-height:1.62;color:#414c44}

/* footer */
.future{
  margin-top:24px;text-align:center;color:#7f8981;font-size:8.3px
}
.future b{color:#536058}
footer{
  display:flex;justify-content:space-between;gap:20px;margin-top:34px;
  padding-top:16px;border-top:1px solid var(--line);color:#8a948c;font-size:8px
}

@media(max-width:900px){
  .search-row{grid-template-columns:1fr 1fr}
  .run{width:100%}
  .account{grid-template-columns:52px 1fr auto}
  .why{grid-column:2/4;border-left:0;padding-left:0}
}
@media(max-width:670px){
  .shell{padding:18px 12px 40px}.hero{padding-top:40px}.hero h1{font-size:41px}
  .search-row{grid-template-columns:1fr}.account{grid-template-columns:48px 1fr}
  .generate{grid-column:2;width:max-content}.why{grid-column:2}
  .outreach-grid{grid-template-columns:1fr}.section-head{display:block}.section-head p{text-align:left;margin-top:7px}
  footer{display:block}footer span{display:block;margin-top:4px}
}
</style>
</head>
<body>
<div class="shell">

<header>
  <div class="brand">
    <div class="logo">R</div>
    <div><small>BUILT FOR RESPONSIVE</small><strong>RFP Hiring Surge</strong></div>
  </div>
  <div class="live"><i></i> live signal research</div>
</header>

<section class="hero">
  <div class="kicker">One GTM play, end to end</div>
  <h1>Find companies expanding their <em>proposal teams.</em></h1>
  <p>
    Detect recent RFP, proposal, bid and response-management hiring, rank the strongest accounts,
    and turn each signal into seller-ready outreach for Responsive.
  </p>
</section>

<section class="search-card">
  <div class="search-row">
    <div class="field">
      <label>Market</label>
      <select id="market">
        <option>United States</option>
        <option>North America</option>
        <option>United Kingdom</option>
        <option>Europe</option>
      </select>
    </div>

    <div class="field">
      <label>Company type</label>
      <select id="companyType">
        <option>B2B SaaS companies</option>
        <option>Enterprise software companies</option>
        <option>Cybersecurity companies</option>
        <option>Financial services companies</option>
        <option>Technology companies</option>
      </select>
    </div>

    <div class="field">
      <label>Signal window</label>
      <select id="window">
        <option value="30">Last 30 days</option>
        <option value="90" selected>Last 90 days</option>
        <option value="365">Last 12 months</option>
      </select>
    </div>

    <button class="run" id="runBtn">Find accounts</button>
  </div>
  <div class="warning" id="warning"></div>
</section>

<section class="results-wrap">
  <div class="section-head">
    <div>
      <small>Live results</small>
      <h2 id="resultsTitle">High-intent accounts</h2>
    </div>
    <p>Hiring is treated as a buying signal, not proof of pain. Every result is tied to public evidence.</p>
  </div>

  <div class="accounts" id="accounts">
    <div class="empty">Run the play to find current proposal and RFP hiring signals.</div>
  </div>
</section>

<section class="outreach" id="outreach">
  <div class="outreach-top">
    <div>
      <small>Generated outreach</small>
      <h3 id="outreachCompany">Account</h3>
    </div>
    <div class="persona" id="persona">Recommended persona</div>
  </div>

  <div class="outreach-grid">
    <div class="angle">
      <small>RESPONSIVE ANGLE</small>
      <h4 id="angleTitle">Why this account</h4>
      <p id="angleBody">—</p>
      <hr />
      <b>WHAT THE SIGNAL COULD MEAN</b>
      <span id="hypothesis">—</span>
    </div>

    <div class="message">
      <div class="message-head">
        <strong>Email 01</strong>
        <button class="copy" id="copyBtn">Copy email</button>
      </div>
      <div class="subject" id="subject">Subject: —</div>
      <p class="email" id="email">—</p>
    </div>
  </div>
</section>

<div class="future">
  <b>Future workflow:</b> Salesforce match → Outreach enrollment → seller alert → meetings / pipeline
</div>

<footer>
  <span>Responsive · RFP Hiring Surge</span>
  <span>Public-web signals only · verify before outreach</span>
</footer>

</div>

<script>
const $=id=>document.getElementById(id);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let currentAccounts=[];

function renderAccounts(){
  if(!currentAccounts.length){
    $('resultsTitle').textContent='No strong accounts found';
    $('accounts').innerHTML='<div class="empty">Try a broader company type or longer signal window.</div>';
    return;
  }

  $('resultsTitle').textContent=currentAccounts.length+' high-intent account'+(currentAccounts.length===1?'':'s');

  $('accounts').innerHTML=currentAccounts.map((a,i)=>`
    <div class="account">
      <div class="score">${esc(a.score)}</div>
      <div class="company">
        <strong>${esc(a.company)}</strong>
        <span>${esc(a.company_description||a.domain||'')}</span>
        <div class="tags">${(a.tags||[]).slice(0,3).map(t=>`<span class="tag">${esc(t)}</span>`).join('')}</div>
      </div>

      <div class="why">
        <b>WHY NOW</b>
        <p>${esc(a.why_now)}</p>
        <a class="source" href="${esc(a.source_url)}" target="_blank" rel="noreferrer">${esc(a.source_name||'Source')} ↗</a>
      </div>

      <button class="generate" onclick="showOutreach(${i})">Generate outreach</button>
    </div>
  `).join('');
}

window.showOutreach=function(i){
  const a=currentAccounts[i];
  if(!a)return;

  $('outreachCompany').textContent=a.company;
  $('persona').textContent=(a.personas||[])[0]||'Proposal leader';
  $('angleTitle').textContent=a.hiring_signal||'Relevant hiring signal';
  $('angleBody').textContent=a.responsive_angle||'';
  $('hypothesis').textContent=a.responsive_hypothesis||'';
  $('subject').textContent='Subject: '+(a.email_subject||'');
  $('email').textContent=a.email_body||'';
  $('outreach').classList.add('active');
  $('outreach').scrollIntoView({behavior:'smooth',block:'center'});
}

async function runPlay(){
  const btn=$('runBtn'),warning=$('warning');
  warning.style.display='none';
  btn.disabled=true;
  btn.textContent='Searching…';

  try{
    const res=await fetch('/run-play',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({
        market:$('market').value,
        company_type:$('companyType').value,
        signal_window:Number($('window').value)
      })
    });

    const data=await res.json();
    if(!res.ok)throw new Error(data.error||'Research failed');

    currentAccounts=data.accounts||[];
    $('outreach').classList.remove('active');
    renderAccounts();
  }catch(e){
    warning.textContent=e.message;
    warning.style.display='block';
  }finally{
    btn.disabled=false;
    btn.textContent='Find accounts';
  }
}

$('runBtn').addEventListener('click',runPlay);

$('copyBtn').addEventListener('click',async()=>{
  const text=$('subject').textContent+'\n\n'+$('email').textContent;
  await navigator.clipboard.writeText(text);
  const btn=$('copyBtn'),old=btn.textContent;
  btn.textContent='Copied';
  setTimeout(()=>btn.textContent=old,1000);
});
</script>
</body>
</html>"""


def json_post(url, headers, payload, timeout=60):
    req = urlrequest.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urlrequest.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{exc.code}: {body[:450]}")


def tavily_search(query, time_range=None):
    payload = {
        "query": query,
        "search_depth": "basic",
        "topic": "general",
        "max_results": 8,
        "include_answer": False,
        "include_raw_content": False,
    }
    if time_range:
        payload["time_range"] = time_range

    data = json_post(
        "https://api.tavily.com/search",
        {
            "Authorization": f"Bearer {os.environ.get('TAVILY_API_KEY')}",
            "Content-Type": "application/json",
        },
        payload,
        timeout=30,
    )
    return data.get("results", [])


def extract_output_text(data):
    if isinstance(data.get("output_text"), str):
        return data["output_text"]

    chunks = []
    for item in data.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text" and isinstance(content.get("text"), str):
                chunks.append(content["text"])

    return "\n".join(chunks)


def time_range_for_window(days):
    if days <= 30:
        return "month"
    return "year"


def build_queries(market, company_type):
    return [
        f'{company_type} {market} hiring "proposal manager" OR "proposal specialist" OR "proposal writer"',
        f'{company_type} {market} hiring "RFP manager" OR "RFP specialist" OR "RFP writer"',
        f'{company_type} {market} hiring "bid manager" OR "response manager" OR "proposal operations"',
    ]


def research_hiring(market, company_type, signal_window):
    raw = []
    time_range = time_range_for_window(signal_window)

    for query in build_queries(market, company_type):
        raw.extend(tavily_search(query, time_range))

    seen = set()
    unique = []

    for item in raw:
        url = item.get("url")
        if not url or url in seen:
            continue
        seen.add(url)
        unique.append({
            "title": item.get("title", ""),
            "url": url,
            "snippet": (item.get("content") or "")[:1800],
        })

    return unique[:28]


def response_schema():
    account = {
        "type": "object",
        "properties": {
            "company": {"type": "string"},
            "domain": {"type": "string"},
            "company_description": {"type": "string"},
            "score": {"type": "integer", "minimum": 0, "maximum": 100},
            "tags": {"type": "array", "items": {"type": "string"}},
            "hiring_signal": {"type": "string"},
            "why_now": {"type": "string"},
            "responsive_hypothesis": {"type": "string"},
            "responsive_angle": {"type": "string"},
            "personas": {"type": "array", "items": {"type": "string"}},
            "email_subject": {"type": "string"},
            "email_body": {"type": "string"},
            "source_url": {"type": "string"},
            "source_name": {"type": "string"},
        },
        "required": [
            "company","domain","company_description","score","tags","hiring_signal",
            "why_now","responsive_hypothesis","responsive_angle","personas",
            "email_subject","email_body","source_url","source_name"
        ],
        "additionalProperties": False,
    }

    return {
        "type": "object",
        "properties": {"accounts": {"type": "array", "items": account}},
        "required": ["accounts"],
        "additionalProperties": False,
    }


def analyze_hiring(market, company_type, signal_window, evidence):
    evidence_rows = [
        {
            "id": i + 1,
            "title": x["title"],
            "url": x["url"],
            "snippet": x["snippet"],
        }
        for i, x in enumerate(evidence)
    ]

    prompt = f"""
You are building one account-based GTM play for Responsive.

RESPONSIVE
Responsive is a Strategic Response Management platform for business-critical responses including RFPs, proposals, bids, questionnaires, assessments, and trust-center workflows.

PLAY
RFP Hiring Surge

TARGET
Market: {market}
Company type: {company_type}
Requested signal window: approximately last {signal_window} days

GOAL
Find companies showing a credible, current hiring signal around proposal, RFP, bid, or response-management work.

RULES
- Use only real operating companies supported by the supplied evidence.
- Exclude job boards, staffing agencies, recruiters, consultants, universities, generic articles, and irrelevant vendors.
- Prefer direct proposal/RFP/bid/response roles.
- A single highly relevant opening can qualify, but call it a hiring signal rather than a surge.
- Do not claim the company is struggling, overwhelmed, manually processing RFPs, or needs Responsive.
- The Responsive hypothesis must be phrased as something the signal COULD indicate.
- Do not invent RFP volume, headcount, response time, revenue, pipeline, or internal pain.
- source_url must exactly match one supplied candidate URL.
- Dedupe companies.
- Omit weak evidence.
- Only return accounts scoring 75 or above.
- Return at most {MAX_ACCOUNTS} accounts.

SCORING
90-100 = excellent ICP and a very direct current proposal/RFP hiring signal.
80-89 = strong ICP and direct relevant hiring.
75-79 = credible but somewhat less specific.

FIELDS
company_description: <= 8 words.
tags: 2-3 short tags.
hiring_signal: observable fact only.
why_now: one concise sentence explaining why the hiring signal makes the account timely.
responsive_hypothesis: one sentence explaining what the hiring signal COULD indicate about response-management scale or complexity.
responsive_angle: one sentence explaining why Responsive could be relevant without assuming pain.
personas: 2-3 likely buyer/influencer titles.
email_subject: 2-5 words.
email_body: 55-90 words, formatted:

[First Name],

specific hiring signal.

possible operational implication.

one concise Responsive sentence.

low-friction question?

Use blank lines between paragraphs.
Do not say "I noticed", "I was researching", "based on my research", "congrats", or invent internal facts.
Lead with the event, not Responsive.

EVIDENCE
{json.dumps(evidence_rows, indent=2)}
"""

    data = json_post(
        "https://api.openai.com/v1/responses",
        {
            "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}",
            "Content-Type": "application/json",
        },
        {
            "model": os.environ.get("OPENAI_MODEL", "gpt-5.6-luna"),
            "input": prompt,
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "responsive_rfp_hiring_surge",
                    "strict": True,
                    "schema": response_schema(),
                }
            },
        },
        timeout=90,
    )

    parsed = json.loads(extract_output_text(data))
    allowed_urls = {x["url"] for x in evidence}

    accounts = []
    for account in parsed.get("accounts", []):
        if account.get("source_url") not in allowed_urls:
            continue
        try:
            score = int(account.get("score", 0))
        except Exception:
            continue
        if score < 75:
            continue
        account["score"] = score
        accounts.append(account)

    accounts.sort(key=lambda x: x["score"], reverse=True)
    parsed["accounts"] = accounts[:MAX_ACCOUNTS]
    return parsed


@app.get("/")
def home():
    return Response(HTML, mimetype="text/html")


@app.post("/run-play")
def run_play():
    missing = [
        key for key in ("TAVILY_API_KEY", "OPENAI_API_KEY")
        if not os.environ.get(key)
    ]
    if missing:
        return jsonify({
            "error": "Missing Vercel environment variable(s): " + ", ".join(missing)
        }), 400

    body = request.get_json(silent=True) or {}
    market = str(body.get("market", "United States"))[:80]
    company_type = str(body.get("company_type", "B2B SaaS companies"))[:100]

    try:
        signal_window = int(body.get("signal_window", 90))
    except Exception:
        signal_window = 90

    signal_window = max(30, min(signal_window, 365))

    try:
        evidence = research_hiring(market, company_type, signal_window)
        if not evidence:
            return jsonify({
                "error": "No usable hiring evidence was returned. Try a broader company type or longer signal window."
            }), 404

        result = analyze_hiring(
            market,
            company_type,
            signal_window,
            evidence,
        )
        result["mode"] = "live"
        result["sources_scanned"] = len(evidence)
        result["generated_at"] = datetime.now(timezone.utc).isoformat()
        result["app_version"] = APP_VERSION
        return jsonify(result)

    except Exception as exc:
        return jsonify({
            "error": "Live RFP hiring research failed: " + str(exc)[:550]
        }), 500


@app.get("/health")
def health():
    return jsonify({
        "ok": True,
        "app": "responsive-rfp-hiring-surge",
        "version": APP_VERSION,
        "tavily_configured": bool(os.environ.get("TAVILY_API_KEY")),
        "openai_configured": bool(os.environ.get("OPENAI_API_KEY")),
        "model": os.environ.get("OPENAI_MODEL", "gpt-5.6-luna"),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "3000")))
