"""Build the portfolio PDF from canonical aggregate exports (requires reportlab)."""
from pathlib import Path
import csv
from xml.sax.saxutils import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
import os
FONT_DIR = Path(os.environ.get("EXPERIMENTIQ_FONT_DIR", "/usr/share/fonts/truetype/dejavu"))
pdfmetrics.registerFont(TTFont("IQSans", str(FONT_DIR/"DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("IQSans-Bold", str(FONT_DIR/"DejaVuSans-Bold.ttf")))
pdfmetrics.registerFontFamily("IQSans",normal="IQSans",bold="IQSans-Bold",italic="IQSans",boldItalic="IQSans-Bold")
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/session4'
def rows(path):
    with (ROOT/path).open() as f: return list(csv.DictReader(f))
kpis = rows('reports/arm_kpis.csv')
binary = [r for r in rows('reports/session2/binary.csv') if r['outcome']=='conversion' and r['reference']=='Control']
revenue = [r for r in rows('reports/session2/revenue.csv') if r['reference']=='Control']
econ = [r for r in rows('reports/session3/demonstration_scenarios.csv') if r['treatment']!='Control']
navy=colors.HexColor('#17344A'); teal=colors.HexColor('#087F83'); gray=colors.HexColor('#516473')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleIQ',fontName='IQSans-Bold',fontSize=32,leading=37,textColor=navy,spaceAfter=14))
styles.add(ParagraphStyle(name='SectionIQ',fontName='IQSans-Bold',fontSize=21,leading=26,textColor=navy,spaceAfter=15))
styles.add(ParagraphStyle(name='SubIQ',fontName='IQSans-Bold',fontSize=12,leading=16,textColor=teal,spaceBefore=12,spaceAfter=7))
styles.add(ParagraphStyle(name='BodyIQ',fontName='IQSans',fontSize=10,leading=15,textColor=navy,spaceAfter=10))
styles.add(ParagraphStyle(name='SmallIQ',fontName='IQSans',fontSize=8,leading=11,textColor=gray,spaceAfter=7))
styles.add(ParagraphStyle(name='CellIQ',fontName='IQSans',fontSize=9,leading=12,textColor=navy))
styles.add(ParagraphStyle(name='HeadIQ',fontName='IQSans-Bold',fontSize=9,leading=12,textColor=colors.white))
story=[]
def p(t,style='BodyIQ'): story.append(Paragraph(t,styles[style]))
def h(t): p(t,'SubIQ')
def table(headers,data,widths):
    cells=[[Paragraph(escape(str(x)),styles['HeadIQ']) for x in headers]]+[[Paragraph(escape(str(x)),styles['CellIQ']) for x in row] for row in data]
    t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),navy),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#F0F5F8'),colors.white]),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9),('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor('#CAD7DE'))]))
    story.extend([t,Spacer(1,12)])
def shot(name,width=490):
    path=ROOT/'screenshots/session4'/name
    if not path.exists(): raise FileNotFoundError(path)
    from PIL import Image as PI
    with PI.open(path) as im: w,hh=im.size
    story.append(Image(str(path),width=width,height=width*hh/w))
def new(title): story.append(PageBreak()); p(title,'SectionIQ')
p('INDEPENDENT ANALYTICS CASE STUDY','SmallIQ')
p('ExperimentIQ','TitleIQ')
p('A/B Testing &amp; Incremental Revenue Optimization','SubIQ')
p('From randomized evidence to a conditional business decision.','SectionIQ')
p('A retailer must decide whether to send a men\'s merchandise email, a women\'s merchandise email, or no email. ExperimentIQ analyzes Kevin Hillstrom\'s authentic 64,000-customer experiment and connects statistical evidence to transparent campaign economics.')
table(['64,000 customers','3 randomized arms','2-week outcomes'],[['Authentic source data','Distinct treatment comparisons','Conversion primary; visits and spend secondary']],[164,164,162])
shot('executive-desktop.png')
p('Actual live Streamlit dashboard, captured during Session 4 QA. This is an independent portfolio project, not a client engagement or a claim of realized business impact.','SmallIQ')
new('01  Data, design and analytical foundation')
p('The original challenge describes random assignment to two merchandise emails and a no-email control. Each row is one assigned customer observation. All outcome denominators include the full assigned arm, including non-visitors and customers with zero spending.')
table(['Arm','Assigned','Conversion','Visit','Spend/customer'],[[r['arm'],f"{int(r['n']):,}",f"{float(r['conversion_rate'])*100:.4f}%",f"{float(r['visit_rate'])*100:.4f}%",f"${float(r['spend_per_customer']):.4f}"] for r in kpis],[110,75,95,95,115])
p(f"Total observed spend: <b>${sum(float(r['total_spend']) for r in kpis):,.2f}</b>. Dollars follow the source convention; no current-price or currency-conversion claim is made.")
h('Quality controls that preserve the experiment')
p('The pipeline validates 64,000 rows and 12 original columns, with no missing or invalid values found. It retains all 6,562 repeated rows after first occurrence because no original customer IDs establish duplication. The original Surburban spelling remains intact; normalization is stored separately. Source bytes are pinned by SHA-256 and customer-level files stay outside Git while redistribution rights are unresolved.')
h('Reproducible architecture')
for title,body in [('Acquire and validate','Original CSV -> checksum -> schema and quality checks -> separate normalized fields.'),('Analyze independently','Python KPIs and 12 SQLite analyses reconcile eight KPI fields; statistics use the same preserved assignment population.'),('Translate and report','Inference -> canonical economics -> nine-page Streamlit app, seven-sheet Excel report and Power BI import assets.')]:
    p(f'<b>{title}.</b> {body}')
h('Integrity is assessed, not assumed from a tidy file')
p('Realized arm sizes need not be exactly equal. An equal-allocation sample-ratio diagnostic is preliminary because original allocation logs are unavailable. Baseline summaries use only pre-treatment attributes. No invented dates, event stream, customer identifiers or lifetime value are introduced.')
new('02  Statistical evidence and uncertainty')
p('Both emails show evidence of improved conversion versus control in this historical experiment. Effect size, uncertainty and the declared testing family accompany each conclusion.')
table(['Versus control','Conversion difference (pp)','95% pointwise CI (pp)','Primary Holm p'],[[r['treatment'],f"+{100*float(r['effect']):.4f}",f"[{100*float(r['ci_low']):.4f}, {100*float(r['ci_high']):.4f}]",f"{float(r['p_adjusted']):.4g}"] for r in binary],[110,130,145,105])
table(['Versus control','Revenue/customer difference','95% bootstrap CI'],[[r['treatment'],f"+${float(r['effect']):.4f}",f"[${float(r['ci_low']):.4f}, ${float(r['ci_high']):.4f}]"] for r in revenue],[120,190,180])
h('Methods and interpretation')
p('Binary outcomes use two-sided Fisher exact tests and Newcombe/Wilson risk-difference intervals. Holm adjusts p-values within declared families: two primary conversion comparisons, separate secondary endpoint families, and an exploratory email-versus-email family. Intervals are pointwise, not simultaneous or multiplicity-adjusted.')
p('Spending is sparse and right-skewed. A within-arm empirical customer bootstrap uses 10,000 replications and seed 20261020, retaining zero spending. Percentile intervals quantify sampling uncertainty in mean differences. Revenue p-values come from a separate approximate Welch test; they are not bootstrap sign counts.')
p('A 95% confidence interval describes the long-run coverage of the procedure, not a 95% probability that this fixed effect lies inside this particular interval. The plan is retrospective, not preregistered: descriptive outcomes were already known.')
h('What the evidence does not justify')
p('None of the 12 planned subgroup interaction tests rejects after Holm correction. A significant result in one subgroup and a non-significant result in another is not itself evidence of a difference. No validated subgroup targeting rule is recommended.')
p('Absolute and relative changes differ: a 0.6805-percentage-point conversion difference is not a 0.6805% relative increase. Historical assignment effects do not establish present-day performance, profitability or customer lifetime value.')
new('03  Business economics under explicit assumptions')
p('Original costs and margins are unavailable. The simulator therefore requires explicit hypothetical assumptions before presenting an economic conclusion.')
p('<b>Net contribution = N x k x d x m - N x c - F</b><br/>N: audience; k: effect multiplier; d: incremental revenue/customer; m: contribution margin; c: delivery cost/customer; F: fixed setup cost.')
p('Illustration only: N = 10,000, m = 40%, c = $0.05, F = $500, k = 1. These are modeled contributions in source-dollar units, not observed profits or forecasts.')
table(['Treatment','Net contribution','Conditional interval'],[[r['treatment'],f"${float(r['net_value']):,.2f}",f"[${float(r['net_low']):,.2f}, ${float(r['net_high']):,.2f}]"] for r in econ],[115,145,230])
h('Break-even and sensitivity')
p('Maximum affordable delivery cost is k x d x m - F/N when N is positive. Under the illustration, the thresholds are '+', '.join(f"{r['treatment']}: ${float(r['max_delivery_cost']):.4f}/customer" for r in econ)+'. Negative thresholds mean free delivery still cannot cover setup. Undefined ratios remain blank.')
p('The conditional interval transforms the historical revenue interval with fixed nonnegative inputs. It excludes uncertainty in costs, margins, delivery, competitive conditions and transfer to a modern audience. Zero audience retains setup cost; zero margin retains all costs; zero campaign cost makes return-on-cost undefined.')
new('04  Interactive decision support')
shot('economics-desktop.png',490)
p('Actual live simulator. Inputs are editable; exported Excel starts with the labeled demonstration, not the current browser scenario.','SmallIQ')
h('Controls that expose assumptions')
p('The live app separates observed experimental outcomes from hypothetical commercial inputs. Users can change treatment, audience, margin, delivery cost, setup cost and effect multiplier. Sensitivity charts show how net contribution changes with audience, margin and delivery cost. A current-scenario CSV preserves the selected inputs.')
h('Boundary checks are part of the analysis')
p('Automated tests cover zero audience, zero margin, missing assumptions, negative uplift, very large audiences, break-even equality and zero incremental campaign cost. Independent SQL comparisons cover undefined outputs as well as finite numbers. Live checks confirm the disabled-assumptions state, zero audience and treatment switching.')
new('05  Decision, delivery and limitations')
h('Recommended next decision')
p('Use the historical positive treatment-versus-control evidence to design a contemporary randomized replication. Predefine a commercially meaningful minimum effect, allocation, analysis families and sample size. Measure contribution margins, delivery costs, deliverability, unsubscribe and complaint guardrails. Choose rollout criteria before seeing the new results; do not deploy retrospective subgroup targeting.')
h('Verified deliverables')
table(['Deliverable','Verification boundary'],[['Python / SQL','75 local automated tests passed; hosted CI: 64 unit + 11 authentic integration. Twelve SQL analyses and 11 economic fields independently reconciled.'],['Streamlit','All nine live pages opened; filters, changed outcomes/treatments, no-data state and scenario controls checked. Custom download events completed.'],['Excel','Seven worksheets, 113 formulas, three charts. Artifact Tool export/reopen and changed-input checks; LibreOffice headless recalculation. No native Microsoft Excel verification.'],['Power BI','Aggregate tables, keys and source values tested; Power Query and DAX specifications supplied. No native PBIX, DAX execution or rendered Power BI report.']],[100,390])
h('Limits that matter for decisions')
p('Historical 2008 data and two-week outcomes; source-reported randomization without original assignment logs or customer IDs; no observed costs or margins; pointwise uncertainty and retrospective analysis choices; no validated segment targeting. The source host remains a reproduction dependency. Raw redistribution permission is unconfirmed.')
h('Explore and reproduce')
p('<link href="https://github.com/harshvtomar/experimentiq-ab-testing-analytics" color="#087F83">GitHub: harshvtomar/experimentiq-ab-testing-analytics</link><br/><link href="https://experimentiq-ab-testing-analytics.streamlit.app/" color="#087F83">Live: experimentiq-ab-testing-analytics.streamlit.app</link>')
p('Source: Kevin Hillstrom, MineThatData Email Analytics and Data Mining Challenge (March 2008).<br/><link href="https://blog.minethatdata.com/2008/03/minethatdata-e-mail-analytics-and-data.html" color="#087F83">Original challenge and experimental design</link>','SmallIQ')
p('Run src.pipeline, src.statistical_pipeline and src.business_pipeline, then pytest with EXPERIMENTIQ_REQUIRE_DATA=1. README provides exact installation commands. Methods, machine-readable results and QA evidence are versioned in docs/ and reports/.','SmallIQ')
p('ExperimentIQ demonstrates reproducible analytics, independent reconciliation and decision support with explicit uncertainty. It does not claim achieved commercial gains.','BodyIQ')
def footer(canvas,doc):
    canvas.setStrokeColor(teal);canvas.setLineWidth(2);canvas.line(42,38,553,38)
    canvas.setFont('IQSans',8);canvas.setFillColor(gray);canvas.drawString(42,24,'EXPERIMENTIQ  |  INDEPENDENT PORTFOLIO CASE STUDY')
    canvas.drawRightString(553,24,str(doc.page))
OUT.mkdir(parents=True,exist_ok=True)
SimpleDocTemplate(str(OUT/'ExperimentIQ_Final_Case_Study.pdf'),pagesize=(595,842),rightMargin=52,leftMargin=52,topMargin=42,bottomMargin=52,title='ExperimentIQ - Final Case Study',author='harshvtomar').build(story,onFirstPage=footer,onLaterPages=footer)
