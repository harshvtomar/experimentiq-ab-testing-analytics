// Execute from a temporary directory linked to the Codex primary JS dependencies.
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {Workbook, SpreadsheetFile, FileBlob} from '@oai/artifact-tool';

const root=process.argv[2];
if(!root) throw new Error('Pass the repository root');
const out=path.join(root,'reports/session3');
const data=JSON.parse(await fs.readFile(path.join(out,'workbook_inputs.json'),'utf8'));
const wb=Workbook.create();
const names=['Executive Dashboard','Scenario Inputs','Revenue & Contribution','Sensitivity Analysis','Experiment Results','Statistical Evidence','Dictionary & Methodology'];
const sheets=Object.fromEntries(names.map(n=>[n,wb.worksheets.add(n)]));
const ink='#18364D',blue='#176BBA',teal='#168776',muted='#EEF3F8';
const money='$#,##0.00;($#,##0.00);"-"';
const dec='0.0000;(0.0000);"-"';
const pct='0.0%;(0.0%);"-"';
const val=(s,a,x)=>s.getRange(a).values=[[x]];
const formula=(s,a,x)=>{s.getRange(a).formulas=[[x]];s.getRange(a).format.font.color=x.includes("'!")?'#00804A':'#172B40';};
function header(s,address,values){s.getRange(address).values=[values];s.getRange(address).format={fill:ink,font:{bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:36,horizontalAlignment:'center',verticalAlignment:'center'};}
function note(s,row,text){val(s,'C'+row,text);s.getRange(`C${row}:K${row}`).merge();s.getRange(`C${row}:K${row}`).format={wrapText:true,rowHeight:42,font:{color:'#526577',size:10}};}
for(const n of names){
 const s=sheets[n];s.showGridLines=false;s.tabColor=ink;
 s.getRange('A1:L60').format.font={name:'Arial',size:10,color:ink};
 s.getRange('A1:B60').format.columnWidth=3;
 s.getRange('C1:C60').format.columnWidth=36;
 s.getRange('D1:K60').format.columnWidth=17;
 s.getRange('C1:K60').format.rowHeight=24;
 val(s,'C2',n);s.getRange('C2:K2').merge();s.getRange('C2:K2').format={fill:ink,font:{size:16,bold:true,color:'#FFFFFF'},rowHeight:36};
}
const inputs=sheets['Scenario Inputs'];
note(inputs,4,'All commercial inputs below are hypothetical and editable. These are not observed retailer costs or margins.');
header(inputs,'C6:E6',['Assumption','Editable value','Definition']);
const inputRows=[['Eligible audience',data.assumptions.audience,'Whole assigned customers'],['Contribution margin',data.assumptions.margin,'Margin on incremental revenue'],['Delivery cost ($/customer)',data.assumptions.delivery_cost,'Incremental cost versus no email'],['Fixed setup cost ($)',data.assumptions.fixed_cost,'Incurred even at zero audience'],['Effect multiplier',data.assumptions.multiplier,'0 to 1; scales effect and interval']];
inputs.getRange('C7:E11').values=inputRows;
inputs.getRange('D7:D11').format={fill:'#FFF1C7',font:{color:'#0000FF'}};
inputs.getRange('E7:E11').format.columnWidth=43;
inputs.getRange('D7').setNumberFormat('#,##0');inputs.getRange('D8').setNumberFormat(pct);inputs.getRange('D9:D10').setNumberFormat(money);inputs.getRange('D11').setNumberFormat('0.00');
inputs.getRange('D7').dataValidation={rule:{type:'whole',operator:'between',formula1:0,formula2:1e12}};
for(const r of [8,11])inputs.getRange('D'+r).dataValidation={rule:{type:'decimal',operator:'between',formula1:0,formula2:1}};
for(const r of [9,10])inputs.getRange('D'+r).dataValidation={rule:{type:'decimal',operator:'between',formula1:0,formula2:1e12}};
val(inputs,'C13','Input status');
formula(inputs,'D13','=IF(COUNT(D7:D11)<>5,"Missing / nonnumeric",IF(OR(D7<0,D7>1000000000000,MOD(D7,1)<>0,D8<0,D8>1,D9<0,D9>1000000000000,D10<0,D10>1000000000000,D11<0,D11>1),"Invalid","Valid"))');
inputs.getRange('D13:E13').merge();
note(inputs,16,'Yellow / blue text: editable inputs. Green: cross-sheet links in the model. Dark text: calculated outputs. Imported experimental measurements stay separate.');
note(inputs,19,'Clear an input to make financial outputs unavailable. Zero is valid. Costs are incremental versus control. Multiplier below 1 is not conservative for negative effects.');

const exp=sheets['Experiment Results'];
note(exp,4,'Source: Kevin Hillstrom, MineThatData randomized email challenge (2008). Two-week outcomes. Original URL and checksum are in Dictionary & Methodology.');
header(exp,'C6:J6',['Arm','Assigned','Conversions','Conversion rate','Visitors','Visit rate','Observed spend ($)','Spend/customer ($)']);
exp.getRange('C7:J9').values=data.arms.map(r=>[r.arm,r.n,r.conversions,r.conversion_rate,r.visits,r.visit_rate,r.total_spend,r.spend_per_customer]);
exp.getRange('D7:E9').setNumberFormat('#,##0');exp.getRange('F7:F9').setNumberFormat('0.0000%');exp.getRange('G7:G9').setNumberFormat('#,##0');exp.getRange('H7:H9').setNumberFormat('0.0000%');exp.getRange('I7:J9').setNumberFormat(money);
header(exp,'C13:H13',['Contrast vs control','Revenue effect ($/customer)','95% lower','95% upper','Raw p','Holm p']);
const rev=data.revenue.filter(r=>r.reference==='Control');
exp.getRange('C14:H15').values=rev.map(r=>[r.treatment,r.effect,r.ci_low,r.ci_high,r.p_raw,r.p_adjusted]);
exp.getRange('D14:F15').setNumberFormat(dec);exp.getRange('G14:H15').setNumberFormat('0.000E+00');
note(exp,18,'All assigned customers are denominators, including zero outcomes. Total observed revenue is not incremental revenue. CIs are pointwise, not Holm-adjusted.');
exp.freezePanes.freezeRows(6);

const model=sheets['Revenue & Contribution'];
note(model,4,'One shared assumption set compares interventions versus no-email control. Monetary outputs are conditional scenarios in source dollars.');
header(model,'C5:F5',['Calculation','Control',"Men's email","Women's email"]);
const labels={6:'Eligible audience',7:'Contribution margin',8:'Delivery cost / customer',9:'Fixed setup cost',10:'Effect multiplier',11:'Input status',12:'Measured revenue effect',13:'Measured 95% lower',14:'Measured 95% upper',16:'Effective revenue uplift',17:'Projected incremental revenue',18:'Incremental gross contribution',19:'Variable delivery costs',20:'Fixed incremental costs',21:'Total incremental costs',22:'Net campaign contribution',23:'Conditional lower net value',24:'Conditional upper net value',26:'Break-even effective uplift',27:'Break-even margin',28:'Maximum delivery cost',29:'Net return / incremental cost',30:'Scenario classification'};
for(const [r,l] of Object.entries(labels))val(model,'C'+r,l);
for(const [j,col] of ['D','E','F'].entries()){
 for(let r=6;r<=10;r++)formula(model,col+r,`=IF(ISNUMBER('Scenario Inputs'!$D$${r+1}),'Scenario Inputs'!$D$${r+1},"n.a.")`);
 formula(model,col+'11',"='Scenario Inputs'!$D$13");
 for(let r=12;r<=14;r++)if(j===0)val(model,col+r,0);else formula(model,col+r,`='Experiment Results'!${['D','E','F'][r-12]}${13+j}`);
 const calcs={16:`${col}12*${col}10`,17:`${col}6*${col}16`,18:`${col}17*${col}7`,19:`${col}6*${col}8`,20:`${col}9`,21:`SUM(${col}19:${col}20)`,22:`${col}18-${col}21`,23:`${col}6*${col}10*${col}7*${col}13-${col}21`,24:`${col}6*${col}10*${col}7*${col}14-${col}21`,26:`IF(${col}6*${col}7>0,${col}21/(${col}6*${col}7),"n.a.")`,27:`IF(${col}17>0,${col}21/${col}17,"n.a.")`,28:`IF(${col}6>0,${col}16*${col}7-${col}9/${col}6,"n.a.")`,29:`IF(${col}21>0,${col}22/${col}21,"n.a.")`,30:`IF(ABS(${col}22)<=0.000000001,"break-even",IF(${col}22>0,"favorable","unfavorable"))`};
 for(const [r,f] of Object.entries(calcs)){
   if(j===0)val(model,col+r,+r>=26?(+r===30?'incremental baseline':'n.a.'):0);
   else formula(model,col+r,`=IF(${col}$11<>"Valid","n.a.",${f})`);
 }
}
model.getRange('D6:F30').setNumberFormat(money);
model.getRange('D6:F6').setNumberFormat('#,##0');model.getRange('D7:F7').setNumberFormat(pct);model.getRange('D10:F10').setNumberFormat('0.00');model.getRange('D12:F16').setNumberFormat(dec);model.getRange('D26:F26').setNumberFormat(dec);model.getRange('D27:F27').setNumberFormat(pct);model.getRange('D28:F28').setNumberFormat(dec);model.getRange('D29:F29').setNumberFormat(pct);
for(const r of [17,21,22])model.getRange(`C${r}:F${r}`).format={fill:muted,font:{bold:true},borders:{bottom:{style:'thin',color:'#B6C4D0'}}};
model.getRange('D22:F24').conditionalFormats.add('cellIs',{operator:'lessThan',formula:0,format:{font:{color:'#A62626'},fill:'#FFF0ED'}});
note(model,33,'Break-even uplift is the required effective revenue/customer after the multiplier. A margin threshold above 100% is infeasible. A negative affordable cost means free delivery still fails to cover setup.');
note(model,36,'Undefined thresholds are n.a. Zero audience does not cancel setup costs. Negative uplift has no positive-margin break-even threshold under nonnegative costs.');

const sens=sheets['Sensitivity Analysis'];
note(sens,4,'One driver varies at a time; other inputs remain linked to Scenario Inputs. Simple affine formulas are used, not native What-If Data Tables.');
const grids=[{row:6,label:'Margin',values:[0,.2,.4,.6,.8,1],kind:'margin'}, {row:18,label:'Delivery cost',values:[0,.02,.05,.1,.2,.3,.5,1],kind:'cost'}, {row:30,label:'Audience',values:[0,1000,5000,10000,25000,50000,100000],kind:'audience'}];
for(const g of grids){
 header(sens,`C${g.row}:F${g.row}`,[g.label,"Men's email net ($)","Women's email net ($)",'Control net ($)']);
 g.values.forEach((v,i)=>{const row=g.row+1+i;val(sens,'C'+row,v);val(sens,'F'+row,0);
 for(const [dst,src] of [['D','E'],['E','F']]){
 const ref=r=>`'Revenue & Contribution'!${src}$${r}`;
 const n=g.kind==='audience'?`$C${row}`:ref(6),m=g.kind==='margin'?`$C${row}`:ref(7),c=g.kind==='cost'?`$C${row}`:ref(8);
 formula(sens,dst+row,`=IF(${ref(11)}<>"Valid","n.a.",${n}*${ref(16)}*${m}-${n}*${c}-${ref(9)})`);
 }
 });
 sens.getRange(`D${g.row+1}:F${g.row+g.values.length}`).setNumberFormat(money);
 sens.getRange(`C${g.row+1}:C${g.row+g.values.length}`).setNumberFormat(g.kind==='margin'?pct:g.kind==='cost'?money:'#,##0');
}

const evidence=sheets['Statistical Evidence'];
note(evidence,4,'Retrospective plan committed before Session 2 inference, after descriptive means were known. This is not preregistration.');
header(evidence,'C6:K6',['Outcome','Contrast','Effect','95% lower','95% upper','Raw p','Holm p','Family','Unit']);
const all=[...data.binary,...data.revenue];
evidence.getRange('C7:K15').values=all.map(r=>[r.outcome,r.comparison,r.effect,r.ci_low,r.ci_high,r.p_raw,r.p_adjusted,r.family,r.outcome==='spend'?'$/customer':'fraction']);
evidence.getRange('D6:D15').format.columnWidth=40;evidence.getRange('J6:J15').format.columnWidth=32;
evidence.getRange('E7:G15').setNumberFormat('0.000000');evidence.getRange('H7:I15').setNumberFormat('0.000E+00');
note(evidence,18,'Binary: two-sided Fisher exact tests; Newcombe/Wilson risk-difference intervals. Revenue: 10,000 customer bootstrap replications, seed 20261020, percentile intervals; separate Welch p-values.');
note(evidence,21,'Holm applies within declared families, not globally. Intervals are pointwise. None of 12 planned subgroup interactions survived Holm adjustment; no targeting policy is validated.');
note(evidence,24,'Conditional net intervals use N × multiplier × margin × revenue interval minus costs. Assumptions are fixed and nonnegative. This excludes commercial and extrapolation uncertainty.');

const dash=sheets['Executive Dashboard'];
note(dash,4,'64,000 randomized customers. Two-week outcomes. Evidence supports contemporary replication; commercial profitability depends on explicit assumptions.');
header(dash,'C6:H6',['Intervention','Assigned customers','Conversion rate','Spend/customer ($)','Net scenario ($)','Lower net ($)']);
for(let i=0;i<3;i++){
 const row=7+i,src=7+i,col=['D','E','F'][i];
 formula(dash,'C'+row,`='Experiment Results'!C${src}`);
 formula(dash,'D'+row,`='Experiment Results'!D${src}`);
 formula(dash,'E'+row,`='Experiment Results'!F${src}`);
 formula(dash,'F'+row,`='Experiment Results'!J${src}`);
 formula(dash,'G'+row,`='Revenue & Contribution'!${col}22`);
 formula(dash,'H'+row,`='Revenue & Contribution'!${col}23`);
}
dash.getRange('D7:D9').setNumberFormat('#,##0');dash.getRange('E7:E9').setNumberFormat('0.00%');dash.getRange('F7:H9').setNumberFormat(money);dash.getRange('C7:H9').format.font.color=ink;
note(dash,11,'Scenario values are hypothetical, linked to the yellow input cells. Revenue is not profit. Lower net values are conditional transformations of pointwise revenue intervals.');
function chart(s,type,range,title,start,end,format){
 const c=s.charts.add(type,range);c.title=title;c.titleTextStyle.fontSize=12;c.titleTextStyle.typeface='Arial';c.setPosition(start,end);
 c.xAxis={axisType:'textAxis',textStyle:{typeface:'Arial',fontSize:10}};
 c.yAxis={numberFormatCode:format,numberFormatSourceLinked:false,textStyle:{typeface:'Arial',fontSize:10}};
 c.legend={position:'bottom',textStyle:{typeface:'Arial',fontSize:10}};
 c.series.items.forEach((s,i)=>{s.fill=[blue,teal,'#61758A'][i%3];if(type==='line')s.line={fill:[blue,teal,'#61758A'][i%3],style:'solid',width:2};});
 return c;
}
chart(dash,'bar',[dash.getRange('C6:C9'),dash.getRange('E6:E9')],'Observed conversion rate','C14','G28','0.0%').hasLegend=false;
chart(dash,'bar',[dash.getRange('C6:C9'),dash.getRange('G6:G9')],'Hypothetical net contribution ($)','H14','L28','$#,##0').hasLegend=false;
note(dash,30,'Before rollout: measure costs and margins, set an economic threshold, and run a contemporary randomized replication with unsubscribe, complaint and deliverability guardrails.');
chart(sens,'line',sens.getRange('C6:F12'),'Margin sensitivity: net contribution ($)','H6','L20','$#,##0');

const dict=sheets['Dictionary & Methodology'];
dict.getRange('C2:K2').unmerge();dict.getRange('C2:D2').merge();
const notes=[
 ['Original source','https://blog.minethatdata.com/2008/03/minethatdata-e-mail-analytics-and-data.html'],
 ['CSV source','http://www.minethatdata.com/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv'],
 ['Source SHA-256',data.metadata.source_sha256],
 ['Conversion rate','Customers who purchased / assigned customers. No post-treatment exclusions.'],
 ['Visit rate','Customers who visited / assigned customers; not number of sessions.'],
 ['Revenue per customer','Total spend / assigned customers, including zero spend. Source dollars; no currency conversion.'],
 ['Net contribution','Audience × historical revenue effect × multiplier × assumed margin − audience × delivery cost − fixed setup.'],
 ['Break-even uplift','Total costs / (audience × margin); effective uplift after multiplier. Undefined if denominator is zero.'],
 ['Break-even margin','Total costs / projected incremental revenue when revenue is positive; above 100% is infeasible.'],
 ['Maximum delivery cost','Effective uplift × margin − fixed setup / audience. Negative means no nonnegative delivery price is affordable.'],
 ['Net return on cost','Net contribution / incremental campaign cost; undefined at zero cost. Not measured or realized ROI.'],
 ['Statistical uncertainty','Existing 95% pointwise percentile interval transformed under fixed assumptions. No joint treatment-choice guarantee.'],
 ['Commercial uncertainty','Costs, margin and multiplier are not estimated from the randomized experiment. Change inputs to explore them.'],
 ['Extrapolation uncertainty','Historical effects may not transfer to a contemporary audience. No future realized-profit prediction interval.'],
 ['Data handling','64,000 rows, 6,562 repeated rows retained. No original customer IDs or dates. Raw source bytes are excluded from this workbook.'],
 ['Verification boundary','Recalculated and exported with Artifact Tool; independent Python and SQL reconciliation. Native Microsoft Excel and Power BI Desktop are not verified.']
];
header(dict,'C6:D6',['Term / source','Definition']);
dict.getRange('C7:D22').values=notes;dict.getRange('D6:D22').format.columnWidth=110;dict.getRange('C7:D22').format={wrapText:true,rowHeight:46};

// Test actual dependency recalculation with representative changed/blank/zero inputs.
const verification=[];
for(const [label,values] of [['demo',[10000,.4,.05,500,1]],['changed',[20000,.2,.1,1000,.5]],['zero audience',[0,.4,.05,500,1]],['zero costs',[10000,.4,0,0,1]],['zero margin',[10000,0,.05,500,1]],['missing margin',[10000,null,.05,500,1]],['invalid margin',[10000,1.2,.05,500,1]]]){
 inputs.getRange('D7:D11').values=values.map(x=>[x]);wb.recalculate();
 verification.push({label,inputs:values,model:model.getRange('E16:F30').values});
}
inputs.getRange('D7:D11').values=inputRows.map(r=>[r[1]]);wb.recalculate();
await fs.writeFile(path.join(out,'excel_recalculation_checks.json'),JSON.stringify(verification,null,2));
console.log((await wb.inspect({kind:'table',range:"'Revenue & Contribution'!C16:F30",include:'values,formulas',tableMaxRows:16,tableMaxCols:4,maxChars:4500})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:30},summary:'Formula error scan',maxChars:2000})).ndjson);
await fs.mkdir(path.join(out,'previews'),{recursive:true});
for(const [name,range] of [['Executive Dashboard','C2:L32'],['Scenario Inputs','C2:K21'],['Revenue & Contribution','C2:K38'],['Sensitivity Analysis','C2:L39'],['Experiment Results','C2:K20'],['Statistical Evidence','C2:K26'],['Dictionary & Methodology','C2:D23']]){
 const img=await wb.render({sheetName:name,range,scale:1,format:'png'});
 await fs.writeFile(path.join(out,'previews',name.replaceAll(' ','_').replaceAll('&','and')+'.png'),new Uint8Array(await img.arrayBuffer()));
}
const target=path.join(out,'ExperimentIQ_Business_Analytics_Report.xlsx');
await (await SpreadsheetFile.exportXlsx(wb)).save(target);
const reopened=await SpreadsheetFile.importXlsx(await FileBlob.load(target));
reopened.recalculate();
const saved=reopened.worksheets.getItem('Revenue & Contribution').getRange('E22:F24').values;
await fs.writeFile(path.join(out,'excel_reopen_values.json'),JSON.stringify(saved));
console.log('Exported and reopened '+target);console.log(JSON.stringify(saved));
const files=['ExperimentIQ_Business_Analytics_Report.xlsx','workbook_inputs.json','excel_recalculation_checks.json','excel_reopen_values.json'];
const hashes={};for(const file of files)hashes[file]=crypto.createHash('sha256').update(await fs.readFile(path.join(out,file))).digest('hex');
hashes['scripts/build_workbook.mjs']=crypto.createHash('sha256').update(await fs.readFile(path.join(root,'scripts/build_workbook.mjs'))).digest('hex');
await fs.writeFile(path.join(out,'excel_verification_manifest.json'),JSON.stringify({engine:'Artifact Tool',native_microsoft_excel_verified:false,hashes},null,2));
