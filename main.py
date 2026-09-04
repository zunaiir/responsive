import os
import json
from datetime import datetime, timezone
from urllib import request as urlrequest
from urllib.error import HTTPError

from flask import Flask, Response, jsonify, request

app = Flask(__name__)
APP_VERSION = "responsive-rfp-hiring-surge-v1-live"
MAX_ACCOUNTS = 6

HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Responsive · RFP Hiring Surge</title>
<meta name="description" content="A signal-led GTM workflow concept built for Responsive." />
<style>
:root{--bg:#f6f7f4;--surface:#fff;--ink:#132019;--muted:#6f7b73;--line:#dfe5df;--forest:#183b2b;--mint:#a6f3cf;--mint-soft:#ecfbf4;--blue:#5577ff;--blue-soft:#edf1ff;--amber:#f3a64a;--amber-soft:#fff5e7;--red:#d85c67;--red-soft:#fff0f1;--shadow:0 18px 60px rgba(19,32,25,.08)}
*{box-sizing:border-box}html{scroll-behavior:smooth}html,body{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}body{min-height:100vh;background:radial-gradient(circle at 88% -10%,rgba(85,119,255,.09),transparent 28%),radial-gradient(circle at 8% 24%,rgba(166,243,207,.16),transparent 25%),var(--bg)}button,input,select{font:inherit}button{cursor:pointer}a{color:inherit}.shell{max-width:1250px;margin:0 auto;padding:24px 26px 58px}
.topbar{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--line);padding-bottom:21px}.brand{display:flex;align-items:center;gap:11px}.mark{width:40px;height:40px;border-radius:12px;background:var(--forest);color:var(--mint);display:grid;place-items:center;font-weight:950;font-size:17px}.brand-copy small{display:block;font-size:8.5px;letter-spacing:.15em;font-weight:900;color:var(--muted)}.brand-copy strong{display:block;font-size:17px;margin-top:2px;letter-spacing:-.025em}.live-pill{display:flex;gap:7px;align-items:center;border:1px solid var(--line);background:rgba(255,255,255,.75);border-radius:999px;padding:7px 10px;color:var(--muted);font-size:8.5px;font-weight:800}.live-pill i{width:7px;height:7px;border-radius:50%;background:#58d49b;box-shadow:0 0 12px rgba(88,212,155,.7)}
.hero{padding:58px 0 34px;max-width:950px}.kicker{font-size:9px;letter-spacing:.16em;text-transform:uppercase;font-weight:900;color:var(--blue)}.hero h1{font-size:61px;line-height:.98;letter-spacing:-.055em;margin:14px 0 18px;max-width:940px}.hero h1 em{font-style:normal;color:var(--forest);position:relative;white-space:nowrap}.hero h1 em:after{content:"";position:absolute;left:0;right:0;bottom:2px;height:9px;background:var(--mint);border-radius:999px;z-index:-1;transform:rotate(-.6deg)}.hero p{font-size:16px;line-height:1.65;color:var(--muted);max-width:790px;margin:0}.flow{display:flex;gap:8px;flex-wrap:wrap;margin-top:21px}.flow span{font-size:8.7px;font-weight:850;border:1px solid var(--line);background:rgba(255,255,255,.72);border-radius:999px;padding:7px 9px;color:#5e6961}.flow b{color:var(--ink)}
.workspace{display:grid;grid-template-columns:300px minmax(0,1fr);gap:14px;align-items:start}.builder{position:sticky;top:16px;background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:17px;box-shadow:var(--shadow)}.builder h2{font-size:15px;letter-spacing:-.025em;margin:0 0 5px}.builder>p{font-size:9.5px;color:var(--muted);line-height:1.5;margin:0 0 17px}.field{margin-bottom:12px}.field label{display:block;font-size:7.8px;letter-spacing:.12em;text-transform:uppercase;color:#7b867e;font-weight:900;margin-bottom:6px}.field select{width:100%;border:1px solid var(--line);border-radius:10px;background:#fbfcfa;color:var(--ink);padding:10px 11px;font-size:10.5px;outline:none}.run{width:100%;border:0;border-radius:11px;background:var(--forest);color:#fff;padding:12px;font-size:10.5px;font-weight:900}.run:hover{background:#214c39}.run:disabled{opacity:.55;cursor:wait}.builder-note{border-top:1px solid var(--line);margin-top:13px;padding-top:11px;font-size:8.5px;line-height:1.48;color:#8a948c}.warning{display:none;margin-top:11px;padding:10px;border-radius:10px;border:1px solid #efc9ce;background:var(--red-soft);color:#9b3f49;font-size:9px;line-height:1.45}
.output{display:flex;flex-direction:column;gap:14px}.card{min-width:0;background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:18px;box-shadow:0 10px 34px rgba(19,32,25,.045)}.card-head{display:flex;justify-content:space-between;gap:18px;align-items:flex-start;margin-bottom:14px}.card-head small{display:block;font-size:7.8px;letter-spacing:.13em;text-transform:uppercase;font-weight:900;color:#858f87;margin-bottom:5px}.card-head h3{font-size:17px;letter-spacing:-.026em;margin:0}.card-head p{max-width:430px;text-align:right;margin:0;font-size:9px;line-height:1.47;color:var(--muted)}.logic-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:7px}.logic{border:1px solid var(--line);border-radius:12px;background:#fafbf9;padding:10px}.logic span{display:block;font-size:7.2px;letter-spacing:.09em;text-transform:uppercase;font-weight:900;color:#89928b;margin-bottom:5px}.logic strong{display:block;font-size:9.8px;line-height:1.4}
.accounts{display:flex;flex-direction:column;gap:8px}.empty{border:1px dashed var(--line);border-radius:14px;text-align:center;padding:34px;color:var(--muted);font-size:10px}.account{display:grid;grid-template-columns:54px minmax(0,1fr) 270px;gap:12px;align-items:center;border:1px solid #e2e7e2;background:#fcfdfb;border-radius:15px;padding:11px;cursor:pointer;transition:.15s ease}.account:hover{border-color:#bcc8bf;transform:translateY(-1px)}.score{width:44px;height:44px;border-radius:50%;display:grid;place-items:center;background:var(--forest);color:var(--mint);font-size:13px;font-weight:950}.account-main strong{display:block;font-size:11px;margin-bottom:3px}.account-main>span{font-size:8.7px;color:var(--muted)}.tags{display:flex;gap:4px;flex-wrap:wrap;margin-top:6px}.tag{font-size:7.3px;font-weight:850;padding:4px 6px;background:var(--blue-soft);color:#4555a6;border-radius:999px}.reason{border-left:1px solid var(--line);padding-left:12px;min-width:0}.reason small{display:block;font-size:7.2px;letter-spacing:.08em;font-weight:900;color:#89928b;margin-bottom:4px}.reason p{font-size:8.9px;line-height:1.43;color:#566059;margin:0}.source{display:inline-block;margin-top:6px;max-width:100%;font-size:7.5px;color:var(--blue);font-weight:850;text-decoration:none;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.source:hover{text-decoration:underline}
.brief-layout{display:grid;grid-template-columns:.83fr 1.17fr;gap:12px}.signal-card{background:var(--forest);border-radius:16px;padding:15px;color:#fff}.signal-card small{display:block;font-size:7.5px;letter-spacing:.12em;font-weight:900;color:var(--mint)}.signal-card h4{font-size:18px;letter-spacing:-.03em;margin:8px 0 6px}.signal-card p{font-size:9.4px;line-height:1.5;color:#b5c5bb;margin:0}.brief-section{margin-top:13px;padding-top:11px;border-top:1px solid #315343}.brief-section b{display:block;font-size:7.5px;letter-spacing:.08em;color:#8eaa99;margin-bottom:5px}.brief-section span{display:block;font-size:9.3px;line-height:1.45;color:#ebf2ed}.action-panel{border:1px solid var(--line);border-radius:16px;background:#fcfdfb;padding:14px}.action-row{display:grid;grid-template-columns:92px 1fr;gap:10px;padding:8px 0;border-bottom:1px solid var(--line)}.action-row:last-of-type{border-bottom:0}.action-row b{font-size:7.5px;letter-spacing:.08em;color:#89928b}.action-row span{font-size:9.3px;line-height:1.45}.action-buttons{display:flex;gap:7px;flex-wrap:wrap;margin-top:12px}.action-buttons button{border:1px solid var(--line);background:#fff;border-radius:9px;padding:7px 9px;font-size:8px;font-weight:900;color:#536058}.action-buttons button.primary{background:var(--blue);color:#fff;border-color:var(--blue)}
.message{margin-top:12px;border:1px solid var(--line);border-radius:14px;padding:13px;background:#fafbf9}.message-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:9px}.message-top strong{font-size:9.5px}.copy{border:0;border-radius:8px;background:var(--blue-soft);color:#4c5baf;padding:6px 8px;font-size:7.5px;font-weight:900}.subject{font-size:8.5px;font-weight:900;color:#5a655d;margin-bottom:9px}.email{white-space:pre-wrap;font-size:10.2px;line-height:1.62;color:#414b44;margin:0}
.orchestration{display:grid;grid-template-columns:repeat(6,1fr);gap:7px}.node{border:1px solid var(--line);border-radius:12px;background:#fafbf9;padding:10px;position:relative;min-height:72px}.node:not(:last-child):after{content:"→";position:absolute;right:-8px;top:50%;transform:translateY(-50%);color:#8c968e}.node span{display:block;font-size:7px;letter-spacing:.08em;text-transform:uppercase;color:#8c958e;font-weight:900}.node strong{display:block;font-size:9px;line-height:1.35;margin-top:5px}
.bottom-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}.quality-list{display:flex;flex-direction:column;gap:7px}.quality{display:grid;grid-template-columns:18px 1fr;gap:8px;align-items:start;border-bottom:1px solid var(--line);padding:7px 0}.quality:last-child{border-bottom:0}.check{width:17px;height:17px;border-radius:50%;background:var(--mint-soft);color:#24704c;display:grid;place-items:center;font-size:8px;font-weight:950}.quality strong{display:block;font-size:9px;margin-bottom:2px}.quality span{font-size:8.2px;color:var(--muted);line-height:1.4}.hypothesis-box{background:var(--blue-soft);border-radius:13px;padding:12px;margin-bottom:10px}.hypothesis-box small{font-size:7px;letter-spacing:.1em;color:#5968b1;font-weight:900}.hypothesis-box p{font-size:9.3px;line-height:1.5;margin:6px 0 0;color:#48516f}.metric-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:7px}.metric{border:1px solid var(--line);border-radius:11px;padding:9px;background:#fafbf9}.metric span{display:block;font-size:7px;color:#8b958d;margin-bottom:4px}.metric strong{font-size:10px}
footer{display:flex;justify-content:space-between;gap:20px;border-top:1px solid var(--line);padding-top:17px;margin-top:35px;color:#8a948c;font-size:8.3px}
@media(max-width:1000px){.workspace{grid-template-columns:1fr}.builder{position:static}.brief-layout,.bottom-grid{grid-template-columns:1fr}.orchestration{grid-template-columns:repeat(3,1fr)}}@media(max-width:720px){.shell{padding:18px 12px 42px}.hero{padding-top:40px}.hero h1{font-size:42px}.logic-grid{grid-template-columns:1fr 1fr}.account{grid-template-columns:52px 1fr}.reason{grid-column:2;border-left:0;padding-left:0}.orchestration{grid-template-columns:1fr 1fr}.node:not(:last-child):after{display:none}.card-head{display:block}.card-head p{text-align:left;margin-top:7px}}
</style>
</head>
<body>
<div class="shell">
<header class="topbar"><div class="brand"><div class="mark">R</div><div class="brand-copy"><small>BUILT FOR RESPONSIVE</small><strong>RFP Hiring Surge</strong></div></div><div class="live-pill"><i></i> live GTM workflow</div></header>
<section class="hero"><div class="kicker">Signal → Seller → Pipeline</div><h1>Turn proposal-team hiring into an <em>actionable GTM play.</em></h1><p>Find B2B companies showing a surge in RFP, proposal, bid, questionnaire, or response-management hiring. Qualify the signal, match it to a Responsive use case, give sellers the context to act, and define how the play should be measured.</p><div class="flow"><span><b>1.</b> Detect the signal</span><span><b>2.</b> Score the account</span><span><b>3.</b> Build the seller brief</span><span><b>4.</b> Route + measure</span></div></section>
<main class="workspace">
<aside class="builder"><h2>Run the RFP Hiring Surge play</h2><p>Tavily searches the live web for proposal and response-related hiring. OpenAI qualifies the signal and turns it into seller-ready context.</p><div class="field"><label>Market</label><select id="market"><option>United States</option><option>North America</option><option>United Kingdom</option><option>Europe</option></select></div><div class="field"><label>Target company</label><select id="companyType"><option>B2B SaaS companies</option><option>Enterprise software companies</option><option>Cybersecurity companies</option><option>Financial services companies</option><option>Technology companies</option></select></div><div class="field"><label>Signal window</label><select id="window"><option value="30">Last 30 days</option><option value="90" selected>Last 90 days</option><option value="365">Last 12 months</option></select></div><div class="field"><label>Minimum score</label><select id="minScore"><option value="70">70 · exploratory</option><option value="75" selected>75 · qualified</option><option value="80">80 · high intent</option></select></div><button class="run" id="runBtn">Find live hiring signals</button><div class="builder-note">This play treats hiring as a buying signal, not proof of pain. Every recommendation links back to public evidence and preserves seller judgment.</div><div class="warning" id="warning"></div></aside>
<div class="output">
<section class="card"><div class="card-head"><div><small>01 · Play definition</small><h3>RFP Hiring Surge</h3></div><p>Hypothesis: companies expanding proposal / bid / response teams may be experiencing enough response volume or complexity to justify a more scalable system.</p></div><div class="logic-grid"><div class="logic"><span>Market</span><strong id="logicMarket">United States</strong></div><div class="logic"><span>ICP</span><strong id="logicType">B2B SaaS companies</strong></div><div class="logic"><span>Signal</span><strong>Proposal / RFP hiring</strong></div><div class="logic"><span>Action</span><strong>Seller alert + outbound</strong></div></div></section>
<section class="card"><div class="card-head"><div><small>02 · Live audience</small><h3>Accounts with a credible response-management signal</h3></div><p>Prioritize real operating companies with recent hiring evidence. Agencies, staffing firms, job boards and irrelevant “RFP” mentions are excluded.</p></div><div class="accounts" id="accounts"><div class="empty">Run the play to find current accounts.</div></div></section>
<section class="card"><div class="card-head"><div><small>03 · Seller activation</small><h3 id="briefHeading">Select an account</h3></div><p>The same evidence that qualifies the account becomes the seller context, Responsive hypothesis, persona recommendation and outreach angle.</p></div><div class="brief-layout"><div class="signal-card"><small>SELLER BRIEF</small><h4 id="briefCompany">Waiting on live research</h4><p id="briefWhy">Run the play to generate an evidence-backed seller brief.</p><div class="brief-section"><b>RESPONSIVE HYPOTHESIS</b><span id="briefHypothesis">—</span></div><div class="brief-section"><b>WHY THIS COULD MATTER</b><span id="briefImpact">—</span></div></div><div class="action-panel"><div class="action-row"><b>PERSONA</b><span id="persona">—</span></div><div class="action-row"><b>ROUTE TO</b><span id="route">—</span></div><div class="action-row"><b>SEQUENCE</b><span id="sequence">—</span></div><div class="action-row"><b>SELLER ACTION</b><span id="sellerAction">—</span></div><div class="action-buttons"><button class="primary">Create Salesforce alert</button><button>Enroll in Outreach</button><button id="evidenceBtn">View evidence</button></div></div></div><div class="message"><div class="message-top"><strong>Email 01 · signal-led</strong><button class="copy" id="copyBtn">Copy email</button></div><div class="subject" id="subject">Subject: —</div><p class="email" id="email">Run the play to generate a seller-ready email.</p></div></section>
<section class="card"><div class="card-head"><div><small>04 · Workflow design</small><h3>How the play moves through the GTM stack</h3></div><p>Salesforce remains the system of record. Research, enrichment, scoring, activation and seller alerts operate around it.</p></div><div class="orchestration"><div class="node"><span>Signal</span><strong>Tavily hiring research</strong></div><div class="node"><span>Qualify</span><strong>OpenAI signal scoring</strong></div><div class="node"><span>Enrich</span><strong>Clay / ZoomInfo</strong></div><div class="node"><span>System of record</span><strong>Salesforce match</strong></div><div class="node"><span>Activate</span><strong>Outreach sequence</strong></div><div class="node"><span>Seller</span><strong>Alert + context</strong></div></div></section>
<div class="bottom-grid"><section class="card"><div class="card-head"><div><small>Guardrails</small><h3>Data quality before automation</h3></div></div><div class="quality-list"><div class="quality"><div class="check">✓</div><div><strong>Dedupe on Salesforce account + domain</strong><span>Never create a new account because the research layer found another URL.</span></div></div><div class="quality"><div class="check">✓</div><div><strong>Suppress customers and active opportunities</strong><span>Do not enroll accounts already in a live commercial motion.</span></div></div><div class="quality"><div class="check">✓</div><div><strong>Require a verifiable hiring source</strong><span>No account is activated from a model-only inference.</span></div></div><div class="quality"><div class="check">✓</div><div><strong>Respect suppression + consent fields</strong><span>Sequence enrollment happens only after CRM eligibility checks.</span></div></div><div class="quality"><div class="check">✓</div><div><strong>Human review for ambiguous signals</strong><span>Automation stops when the company or signal cannot be confidently matched.</span></div></div></div></section><section class="card"><div class="card-head"><div><small>Measurement</small><h3>Prove incremental impact</h3></div></div><div class="hypothesis-box"><small>TEST HYPOTHESIS</small><p>Accounts showing recent proposal / RFP hiring will create more meetings and opportunities than similar ICP accounts without the signal.</p></div><div class="metric-grid"><div class="metric"><span>PRIMARY</span><strong>Meeting rate</strong></div><div class="metric"><span>SECONDARY</span><strong>Opportunity rate</strong></div><div class="metric"><span>REVENUE</span><strong>Pipeline created</strong></div></div><div class="hypothesis-box" style="margin-top:8px;margin-bottom:0;background:var(--amber-soft)"><small style="color:#996023">EXPERIMENT</small><p style="color:#6f5638">Hold out a matched control audience and compare positive replies, meetings, opportunity creation, velocity and cost per meeting.</p></div></section></div>
</div></main>
<footer><span>Responsive · RFP Hiring Surge · GTM engineering concept</span><span>Public-web signals only · verify before activation</span></footer>
</div>
<script>
const $=id=>document.getElementById(id);const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));let currentAccounts=[];
function renderAccounts(){if(!currentAccounts.length){$('accounts').innerHTML='<div class="empty">No strong evidence-backed accounts were found. Try a broader ICP, longer signal window or lower score threshold.</div>';return}$('accounts').innerHTML=currentAccounts.map((a,i)=>`<div class="account" onclick="selectAccount(${i})"><div class="score">${esc(a.score)}</div><div class="account-main"><strong>${esc(a.company)}</strong><span>${esc(a.company_description||a.domain||'')}</span><div class="tags">${(a.tags||[]).slice(0,4).map(t=>`<span class="tag">${esc(t)}</span>`).join('')}</div></div><div class="reason"><small>HIRING SIGNAL</small><p>${esc(a.hiring_signal)}</p><a class="source" href="${esc(a.source_url)}" target="_blank" rel="noreferrer">${esc(a.source_name||'View evidence')} ↗</a></div></div>`).join('')}
window.selectAccount=function(i){const a=currentAccounts[i];if(!a)return;$('briefHeading').textContent=a.company+' · seller brief';$('briefCompany').textContent=a.company;$('briefWhy').textContent=a.why_now;$('briefHypothesis').textContent=a.responsive_hypothesis;$('briefImpact').textContent=a.business_impact;$('persona').textContent=(a.personas||[]).join(' · ');$('route').textContent=a.route_to;$('sequence').textContent=a.sequence_name;$('sellerAction').textContent=a.seller_action;$('subject').textContent='Subject: '+a.email_subject;$('email').textContent=a.email_body;$('evidenceBtn').onclick=()=>window.open(a.source_url,'_blank','noopener,noreferrer')}
async function runPlay(){const btn=$('runBtn'),warn=$('warning');warn.style.display='none';btn.disabled=true;btn.textContent='Researching hiring signals…';$('logicMarket').textContent=$('market').value;$('logicType').textContent=$('companyType').value;try{const res=await fetch('/run-play',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({market:$('market').value,company_type:$('companyType').value,signal_window:Number($('window').value),minimum_score:Number($('minScore').value)})});const data=await res.json();if(!res.ok)throw new Error(data.error||'Play failed');currentAccounts=data.accounts||[];renderAccounts();if(currentAccounts.length)selectAccount(0)}catch(e){warn.textContent=e.message;warn.style.display='block'}finally{btn.disabled=false;btn.textContent='Find live hiring signals'}}
$('runBtn').addEventListener('click',runPlay);$('copyBtn').addEventListener('click',async()=>{const text=$('subject').textContent+'\n\n'+$('email').textContent;await navigator.clipboard.writeText(text);const btn=$('copyBtn'),old=btn.textContent;btn.textContent='Copied';setTimeout(()=>btn.textContent=old,1000)});
</script>
</body></html>'''


def json_post(url, headers, payload, timeout=60):
    req = urlrequest.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    try:
        with urlrequest.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{exc.code}: {body[:450]}")


def tavily_search(query, time_range=None):
    payload = {"query": query, "search_depth": "basic", "topic": "general", "max_results": 8, "include_answer": False, "include_raw_content": False}
    if time_range:
        payload["time_range"] = time_range
    data = json_post("https://api.tavily.com/search", {"Authorization": f"Bearer {os.environ.get('TAVILY_API_KEY')}", "Content-Type": "application/json"}, payload, timeout=30)
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


def build_queries(market, company_type):
    return [
        f'{company_type} {market} hiring "proposal manager" OR "proposal specialist" OR "proposal writer"',
        f'{company_type} {market} hiring "RFP manager" OR "RFP specialist" OR "RFP writer"',
        f'{company_type} {market} hiring "bid manager" OR "bid specialist" OR "bid writer"',
        f'{company_type} {market} hiring "response manager" OR "response management" OR "questionnaire manager"',
        f'{company_type} {market} jobs proposals RFP bids questionnaires enterprise sales',
    ]


def time_range_for_window(days):
    return "month" if days <= 30 else "year"


def research_hiring(market, company_type, signal_window):
    raw = []
    for query in build_queries(market, company_type):
        raw.extend(tavily_search(query, time_range_for_window(signal_window)))
    seen, unique = set(), []
    for result in raw:
        url = result.get("url")
        if not url or url in seen:
            continue
        seen.add(url)
        unique.append({"title": result.get("title", ""), "url": url, "snippet": (result.get("content") or "")[:1800]})
    return unique[:35]


def response_schema():
    account = {"type":"object","properties":{
        "company":{"type":"string"},"domain":{"type":"string"},"company_description":{"type":"string"},"score":{"type":"integer","minimum":0,"maximum":100},"tags":{"type":"array","items":{"type":"string"}},"hiring_signal":{"type":"string"},"why_now":{"type":"string"},"responsive_hypothesis":{"type":"string"},"business_impact":{"type":"string"},"personas":{"type":"array","items":{"type":"string"}},"route_to":{"type":"string"},"sequence_name":{"type":"string"},"seller_action":{"type":"string"},"email_subject":{"type":"string"},"email_body":{"type":"string"},"source_url":{"type":"string"},"source_name":{"type":"string"}},
        "required":["company","domain","company_description","score","tags","hiring_signal","why_now","responsive_hypothesis","business_impact","personas","route_to","sequence_name","seller_action","email_subject","email_body","source_url","source_name"],"additionalProperties":False}
    return {"type":"object","properties":{"accounts":{"type":"array","items":account}},"required":["accounts"],"additionalProperties":False}


def analyze_hiring(market, company_type, signal_window, minimum_score, evidence):
    candidates = [{"id":i+1,"title":x["title"],"url":x["url"],"snippet":x["snippet"]} for i,x in enumerate(evidence)]
    prompt = f'''You are a GTM intelligence analyst designing a live account-based play for Responsive.

RESPONSIVE CONTEXT
Responsive is a Strategic Response Management platform used to manage business-critical responses such as RFPs, bids, questionnaires, assessments, and trust-center workflows.

PLAY
Name: RFP Hiring Surge
Market: {market}
Target account type: {company_type}
Requested signal window: approximately the last {signal_window} days
Minimum score to return: {minimum_score}

PLAY HYPOTHESIS
Companies adding proposal, RFP, bid, questionnaire, or response-management capacity may be experiencing enough response volume, complexity, or cross-functional coordination pressure to make Strategic Response Management relevant.

YOUR TASK
From the supplied web evidence, identify up to {MAX_ACCOUNTS} REAL operating companies with a credible hiring signal related to proposal management, proposal writing / operations, RFP management, bid management, response management, or security/customer questionnaires when clearly connected to business responses.

STRICT RULES
- Only use companies explicitly supported by supplied evidence.
- Exclude job boards, recruiting agencies, staffing firms, consultants, generic articles, and irrelevant vendors.
- Company should reasonably match "{company_type}".
- Do not infer a hiring surge from one unrelated role. One highly relevant new role may qualify, but call it a hiring signal, not a surge.
- Never claim the company is struggling, overwhelmed, manually processing RFPs, or needs Responsive unless the source explicitly says so.
- Responsive hypothesis must be framed as a hypothesis.
- Do not invent RFP volume, response time, revenue, headcount, pipeline, or process problems.
- source_url MUST exactly equal one supplied candidate URL.
- Dedupe companies. Omit weak or ambiguous evidence.
- Prefer recent, direct employer hiring evidence.

SCORING
90-100 = excellent ICP + highly relevant current response/proposal hiring signal.
80-89 = strong ICP + direct relevant hiring signal.
75-79 = credible but less specific or lower-confidence signal.
Below {minimum_score} = omit.

OUTPUT
company_description <= 8 words.
tags = 2-4 short tags.
hiring_signal = observable fact only.
why_now = why the signal makes the account timely without claiming pain.
responsive_hypothesis = one sentence explaining what the signal COULD indicate about response-management needs.
business_impact = why scalable response management could matter commercially, without invented metrics.
personas = 2-4 likely buyer/influencer titles.
route_to = concise seller-routing recommendation.
sequence_name = short name such as "RFP Growth" or "Proposal Scale".
seller_action = one concrete next action.
email_subject = 2-5 words.
email_body = 55-90 words, formatted:
[First Name],\n\nspecific hiring signal.\n\npossible operational implication.\n\none concise Responsive value proposition.\n\nlow-friction question?
Do not say "I noticed", "I was researching", "based on my research", "congrats", or pretend to know internal pain. Lead with the company event, not Responsive.

EVIDENCE
{json.dumps(candidates, indent=2)}'''
    data = json_post("https://api.openai.com/v1/responses", {"Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}", "Content-Type":"application/json"}, {"model":os.environ.get("OPENAI_MODEL","gpt-5.6-luna"),"input":prompt,"text":{"format":{"type":"json_schema","name":"responsive_rfp_hiring_surge","strict":True,"schema":response_schema()}}}, timeout=90)
    parsed = json.loads(extract_output_text(data))
    allowed = {x["url"] for x in evidence}
    accounts = []
    for a in parsed.get("accounts", []):
        if a.get("source_url") not in allowed:
            continue
        try:
            score = int(a.get("score",0))
        except Exception:
            continue
        if score < minimum_score:
            continue
        a["score"] = score
        accounts.append(a)
    accounts.sort(key=lambda x:x["score"], reverse=True)
    parsed["accounts"] = accounts[:MAX_ACCOUNTS]
    return parsed

@app.get("/")
def home():
    return Response(HTML, mimetype="text/html")

@app.post("/run-play")
def run_play():
    missing = [k for k in ("TAVILY_API_KEY","OPENAI_API_KEY") if not os.environ.get(k)]
    if missing:
        return jsonify({"error":"Missing Vercel environment variable(s): "+", ".join(missing)}),400
    body = request.get_json(silent=True) or {}
    market = str(body.get("market","United States"))[:80]
    company_type = str(body.get("company_type","B2B SaaS companies"))[:100]
    try: signal_window = max(30,min(int(body.get("signal_window",90)),365))
    except Exception: signal_window = 90
    try: minimum_score = max(70,min(int(body.get("minimum_score",75)),90))
    except Exception: minimum_score = 75
    try:
        evidence = research_hiring(market, company_type, signal_window)
        if not evidence:
            return jsonify({"error":"No usable hiring evidence was returned. Try a broader target market or longer signal window."}),404
        result = analyze_hiring(market, company_type, signal_window, minimum_score, evidence)
        result.update({"mode":"live","sources_scanned":len(evidence),"generated_at":datetime.now(timezone.utc).isoformat(),"app_version":APP_VERSION})
        return jsonify(result)
    except Exception as exc:
        return jsonify({"error":"Live RFP hiring research failed: "+str(exc)[:550]}),500

@app.get("/health")
def health():
    return jsonify({"ok":True,"app":"responsive-rfp-hiring-surge","version":APP_VERSION,"tavily_configured":bool(os.environ.get("TAVILY_API_KEY")),"openai_configured":bool(os.environ.get("OPENAI_API_KEY")),"model":os.environ.get("OPENAI_MODEL","gpt-5.6-luna")})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT","3000")))
