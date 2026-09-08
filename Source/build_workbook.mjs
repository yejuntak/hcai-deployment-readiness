import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import assert from 'node:assert/strict';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const out=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const qa=path.join(out,'Verification');
const tests=[];
function make(example){
 const wb=Workbook.create();const s=wb.worksheets.add('Review');const b=wb.worksheets.add('Batch');
 for(const sh of [s,b]){sh.showGridLines=false;sh.getRange('A1:E38').format.font={name:'Arial',size:11,color:'#233449'};sh.getRange('A1:E38').format.rowHeight=25;sh.getRange('A1:E38').format.verticalAlignment='center';sh.tabColor='#233449';}
 s.getRange('A1:A38').format.columnWidth=48;s.getRange('B1:B38').format.columnWidth=28;s.getRange('C1:C38').format.columnWidth=80;
 s.getRange('A2').values=[['Engineering-handoff evaluation']];s.getRange('A2').format.font={size:15,bold:true};
 s.getRange('A3').values=[[example?'Synthetic EX-1. No participant results.':'One assessment per copy. v0.1-rc.2; unvalidated method.']];
 s.getRange('A5:A10').values=[['Session ID'],['Artifact / version'],['Criterion version'],['Expected recall (enter 80%)'],['Evaluator judgment before key disclosure'],['Criterion status from artifact evidence']];
 s.getRange('B5:B9').format.fill='#fff3d1';
 s.getRange('B9').dataValidation={rule:{type:'list',values:['Ready','Not ready','Unable to assess']}};
 s.getRange('B8').dataValidation={rule:{type:'decimal',operator:'between',formula1:0,formula2:1}};s.getRange('B8').setNumberFormat('0.0%');
 s.getRange('A13:C13').values=[['Measurement','Result','Interpretation']];
 s.getRange('A14:A20').values=[['Reference-set defect recall'],['Expected-recall gap (pp)'],['Handoff recovery coverage'],['Omission recognition'],['Artifact requirements coverage'],['False-ready event (single instance)'],['Artifact disposition']];
 s.getRange('C14:C20').values=[['Unique reference matches / frozen reference defects.'],['Expected minus observed recall, in percentage points.'],['Verified applicable scenarios / all applicable scenarios.'],['Recognized reference omissions / reference omissions.'],['Verified mandatory requirements / all mandatory requirements.'],['1 = Ready judgment on a Nonready artifact; 0 = not Ready.'],['Owner must separately record final approval and conditions.']];
 s.getRange('A23:C23').values=[['Adjudicated counts','Editable input','Reconcile to retained CSV evidence']];
 s.getRange('A24').values=[['Enter whole counts; blank means not assessed.']];
 s.getRange('A25:A35').values=[['Eligible reference defects'],['Unique correctly detected reference defects'],['Predefined reference requirement omissions'],['Correctly identified reference omissions'],['Applicable required recovery scenarios'],['Specified + walkthrough verified scenarios'],['Mandatory requirements'],['Specified + walkthrough verified requirements'],['Unresolved critical defects'],['Unassessed mandatory items'],['Required evidence record complete?']];
 s.getRange('B25:B35').format.fill='#fff3d1';s.getRange('B25:B34').setNumberFormat('0');
 s.getRange('B25:B34').dataValidation={rule:{type:'whole',operator:'greaterThanOrEqual',formula1:0}};
 s.getRange('B35').dataValidation={rule:{type:'list',values:['Yes','No']}};
 s.getRange('C25:C35').values=[['Frozen reference-key.csv count; zero yields n.a.'],['Deduplicate accepted matches by reference ID.'],['Subset of the reference set, marked omission.'],['Detected omissions; cannot exceed detected reference defects.'],['Include unassessed applicable scenarios.'],['Both evidence levels required; not just a visible button.'],['Keep every mandatory requirement in the denominator.'],['Both evidence levels required.'],['Include relevant novel genuine critical issues.'],['Count unassessed mandatory requirements and recovery items.'],['No means the gate is not met, even if other counts look complete.']];
 s.getRange('A37').values=[['Amber cells are inputs. Calculated cells are unfilled.']];
 s.getRange('C37').values=[['Source: Protocol-v0.1.pdf and the retained assessment records.']];
 function f(cell,formula){s.getRange(cell).formulas=[[formula]];}
 const ratio=(num,den)=>`=IF(COUNT(${num},${den})<2,"Not evaluated",IF(OR(${num}<0,${den}<0,MOD(${num},1)<>0,MOD(${den},1)<>0,${num}>${den}),"Invalid counts",IF(${den}=0,"n.a.",${num}/${den})))`;
 const subsetInvalid='OR(B27>B25,B28>B26,B26-B28>B25-B27,B26>B25,B28>B27,MIN(B25:B28)<0,MOD(B25,1)<>0,MOD(B26,1)<>0,MOD(B27,1)<>0,MOD(B28,1)<>0)';
 f('B14',`=IF(AND(COUNT(B25:B28)=4,${subsetInvalid}),"Invalid counts",${ratio('B26','B25').slice(1)})`);
 f('B16',ratio('B30','B29'));
 f('B17',`=IF(COUNT(B25:B28)<4,"Not evaluated",IF(${subsetInvalid},"Invalid counts",${ratio('B28','B27').slice(1)}))`);
 f('B18',ratio('B32','B31'));
 f('B15','=IF(OR(B8="",NOT(ISNUMBER(B14))),"Not evaluated",IF(OR(NOT(ISNUMBER(B8)),B8<0,B8>1),"Invalid estimate",(B8-B14)*100))');
 for(const c of ['B14','B16','B17','B18'])s.getRange(c).setNumberFormat('0.0%');s.getRange('B15').setNumberFormat('+0.0;-0.0;0.0');
 s.getRange('A36').values=[['Documented failed mandatory checks']];
 s.getRange('B36').format.fill='#fff3d1';s.getRange('B36').setNumberFormat('0');
 s.getRange('B36').dataValidation={rule:{type:'whole',operator:'greaterThanOrEqual',formula1:0}};
 s.getRange('C36').values=[['Failed requirement + recovery rows; exclude unassessed rows.']];
 f('B20','=IF(OR(B16="Invalid counts",B18="Invalid counts",AND(ISNUMBER(B33),OR(B33<0,MOD(B33,1)<>0)),AND(ISNUMBER(B34),OR(B34<0,MOD(B34,1)<>0)),AND(ISNUMBER(B36),OR(B36<0,MOD(B36,1)<>0))),"Invalid counts",IF(OR(COUNT(B29:B34,B36)<7,AND(B35<>"Yes",B35<>"No")),"Not evaluated",IF(B30+B32+B34+B36<>B29+B31,"Invalid counts",IF(OR(B33>0,B36>0),"Hold for remediation",IF(OR(B34>0,B35="No",B31=0),"Insufficient evidence","Eligible for handoff review")))))');
 f('B10','=IF(OR(B20="Hold for remediation",B20="Insufficient evidence"),"Nonready",IF(B20="Eligible for handoff review","Ready","Unknown"))');
 f('B19','=IF(B10<>"Nonready","n.a.",IF(B9="Ready",1,IF(OR(B9="Not ready",B9="Unable to assess"),0,"Missing judgment")))');
 for(const range of ['A13:C13','A23:C23'])s.getRange(range).format={fill:'#233449',font:{name:'Arial',size:11,color:'#ffffff',bold:true}};
 s.getRange('B14:B20').conditionalFormats.add('containsText',{text:'Invalid',format:{fill:'#fde3e1',font:{color:'#9b2020'}}});
 s.getRange('B20').conditionalFormats.add('containsText',{text:'Hold',format:{fill:'#fde3e1',font:{color:'#9b2020'}}});
 s.getRange('B20').format.wrapText=true;s.getRange('A20:C20').format.rowHeight=42;
 b.getRange('A1:A37').format.columnWidth=42;b.getRange('B1:B37').format.columnWidth=23;b.getRange('C1:C37').format.columnWidth=23;b.getRange('D1:D37').format.columnWidth=23;b.getRange('E1:E37').format.columnWidth=26;
 b.getRange('A2').values=[['False-ready batch calculation']];b.getRange('A2').format.font={size:15,bold:true};
 b.getRange('A3').values=[[example?'Four synthetic instances; not an empirical sample.':'Up to 20 records from the same criterion version.']];
 b.getRange('A5:A12').values=[['Nonready instances with observed judgment'],['Ready among those instances'],['Unable to assess among those instances'],['False-ready acceptance rate'],['Abstention rate among nonready instances'],['Missing judgments on nonready instances'],['Unknown criterion instances'],['Record eligibility']];
 b.getRange('A15:E15').values=[['Assessment ID (unique)','Criterion version','Criterion status','Evaluator judgment','Notes / evidence ID']];
 b.getRange('A15:E15').format={fill:'#233449',font:{name:'Arial',color:'#ffffff',bold:true,size:11},wrapText:true};b.getRange('A15:E15').format.rowHeight=34;
 b.getRange('A16:E35').format.fill='#fff3d1';b.getRange('C16:C35').dataValidation={rule:{type:'list',values:['Ready','Nonready','Unknown']}};b.getRange('D16:D35').dataValidation={rule:{type:'list',values:['Ready','Not ready','Unable to assess','Missing']}};
 // Row eligibility is local to the batch's inputs; invalid rows block rates.
 b.getRange('F15').values=[['Input status']];b.getRange('F1:F35').format.columnWidth=25;
 for(let r=16;r<=35;r++) b.getRange(`F${r}`).formulas=[[`=IF(COUNTA(A${r}:E${r})=0,"",IF(OR(A${r}="",B${r}="",COUNTIFS($A$16:$A$35,A${r})>1,AND(C${r}<>"Ready",C${r}<>"Nonready",C${r}<>"Unknown"),AND(D${r}<>"Ready",D${r}<>"Not ready",D${r}<>"Unable to assess",D${r}<>"Missing",D${r}<>"")),"Invalid record",IF(COUNTIFS($B$16:$B$35,B${r})<>COUNTIFS($A$16:$A$35,"<>"),"Mixed criteria","Valid")))`]];
 const count=(judge)=>`COUNTIFS(C16:C35,"Nonready",D16:D35,"${judge}")`;
 b.getRange('B12').formulas=[['=IF(COUNTA(A16:E35)=0,"No records",IF(OR(COUNTIFS(F16:F35,"Invalid record")>0,COUNTIFS(F16:F35,"Mixed criteria")>0),"Review records","Valid"))']];
 b.getRange('B5').formulas=[[`=IF(B12<>"Valid","Not evaluated",${count('Ready')}+${count('Not ready')}+${count('Unable to assess')})`]];
 b.getRange('B6').formulas=[[`=IF(B12<>"Valid","Not evaluated",${count('Ready')})`]];b.getRange('B7').formulas=[[`=IF(B12<>"Valid","Not evaluated",${count('Unable to assess')})`]];
 b.getRange('B8').formulas=[['=IF(NOT(ISNUMBER(B5)),"Not evaluated",IF(B5=0,"n.a.",B6/B5))']];b.getRange('B9').formulas=[['=IF(NOT(ISNUMBER(B5)),"Not evaluated",IF(B5=0,"n.a.",B7/B5))']];
 b.getRange('B10').formulas=[['=IF(B12<>"Valid","Not evaluated",COUNTIFS(C16:C35,"Nonready")-B5)']];b.getRange('B11').formulas=[['=IF(B12<>"Valid","Not evaluated",COUNTIFS(C16:C35,"Unknown"))']];b.getRange('B8:B9').setNumberFormat('0.0%');
 b.getRange('C5').values=[['Ready + Not ready + Unable to assess']];b.getRange('C10').values=[['Missing or blank judgment; excluded from rate.']];b.getRange('C11').values=[['Excluded from criterion-conditioned rates.']];
 b.getRange('F16:F35').conditionalFormats.add('containsText',{text:'Invalid',format:{fill:'#fde3e1'}});
 if(example){s.getRange('B5:B9').values=[['EX-1'],['SR-01'],['Handoff-v0.1'],[.8],['Ready']];s.getRange('B25:B35').values=[[8],[5],[3],[1],[6],[3],[10],[7],[1],[2],['Yes']];b.getRange('A16:E19').values=Array.from({length:4},(_,i)=>[`EX-${i+1}`,'Handoff-v0.1','Nonready',i===3?'Not ready':'Ready','Synthetic']);}
 s.getRange('D1:D37').copyFrom(s.getRange('C1:C37'),'all');s.getRange('C1:C37').clear({applyTo:'all'});s.getRange('D1:D37').format.columnWidth=80;s.getRange('C1:C37').format.columnWidth=3;
 s.getRange('D34').values=[['Unassessed requirement + recovery rows; disjoint from failed rows.']];
 s.getRange('D36').values=[['Verified + failed + unassessed must equal total required checks.']];
 if(example)s.getRange('B36').values=[[4]];
 b.getRange('A38:F44').format.font={name:'Arial',size:11,color:'#233449'};
 b.getRange('A38:F44').format.rowHeight=28;
 b.getRange('A38:B38').values=[['Companion measures','Result']];
 b.getRange('A38:B38').format={fill:'#233449',font:{name:'Arial',size:11,color:'#ffffff',bold:true}};
 b.getRange('A39:A44').values=[['Decision coverage on nonready instances'],['False-ready among decisive judgments'],['Ready instances with observed judgment'],['False hold rate on ready instances'],['Abstention rate on ready instances'],['Missing judgments on ready instances']];
 b.getRange('B39').formulas=[['=IF(NOT(ISNUMBER(B5)),"Not evaluated",IF(B5=0,"n.a.",(B5-B7)/B5))']];
 b.getRange('B40').formulas=[['=IF(NOT(ISNUMBER(B5)),"Not evaluated",IF(B5-B7=0,"n.a.",B6/(B5-B7)))']];
 b.getRange('B41').formulas=[['=IF(B12<>"Valid","Not evaluated",COUNTIFS(C16:C35,"Ready",D16:D35,"Ready")+COUNTIFS(C16:C35,"Ready",D16:D35,"Not ready")+COUNTIFS(C16:C35,"Ready",D16:D35,"Unable to assess"))']];
 b.getRange('B42').formulas=[['=IF(NOT(ISNUMBER(B41)),"Not evaluated",IF(B41=0,"n.a.",COUNTIFS(C16:C35,"Ready",D16:D35,"Not ready")/B41))']];
 b.getRange('B43').formulas=[['=IF(NOT(ISNUMBER(B41)),"Not evaluated",IF(B41=0,"n.a.",COUNTIFS(C16:C35,"Ready",D16:D35,"Unable to assess")/B41))']];
 b.getRange('B44').formulas=[['=IF(B12<>"Valid","Not evaluated",COUNTIFS(C16:C35,"Ready")-B41)']];
 b.getRange('B39:B40').setNumberFormat('0.0%');b.getRange('B42:B43').setNumberFormat('0.0%');
 b.getRange('C39').values=[['(Ready + Not ready) / all observed Nonready judgments.']];
 b.getRange('C40').values=[['Ready / (Ready + Not ready) on Nonready artifacts.']];
 b.getRange('C42').values=[['Not ready / all observed judgments on Ready artifacts.']];
 b.getRange('C43').values=[['Report alongside false hold; never infer usefulness from one rate.']];
 return {wb,s,b};
}

const v=(sh,c)=>sh.getRange(c).values[0][0];
const {wb:tw,s:ts,b:tb}=make(true);
function check(name,fn){fn();tests.push(name);}
check('Synthetic arithmetic retained',()=>{tw.recalculate();assert.equal(v(ts,'B14'),.625);assert.equal(v(ts,'B17'),1/3);assert.equal(v(ts,'B20'),'Hold for remediation');assert.equal(v(tb,'B8'),.75);});
check('Impossible omission subset rejected',()=>{ts.getRange('B25:B28').values=[[8],[1],[8],[0]];tw.recalculate();assert.equal(v(ts,'B14'),'Invalid counts');assert.equal(v(ts,'B17'),'Invalid counts');});
check('Unassessed-only case distinguished from failed checks',()=>{ts.getRange('B29:B35').values=[[6],[5],[10],[10],[0],[1],['Yes']];ts.getRange('B36').values=[[0]];tw.recalculate();assert.equal(v(ts,'B20'),'Insufficient evidence');});
check('Unreconciled evidence counts rejected',()=>{ts.getRange('B36').values=[[1]];tw.recalculate();assert.equal(v(ts,'B20'),'Invalid counts');});
check('Eligible case requires complete reconciled counts',()=>{ts.getRange('B29:B35').values=[[6],[6],[10],[10],[0],[0],['Yes']];ts.getRange('B36').values=[[0]];tw.recalculate();assert.equal(v(ts,'B20'),'Eligible for handoff review');});
check('Blank first batch row is allowed',()=>{tb.getRange('A16:E16').clear({applyTo:'contents'});tw.recalculate();assert.equal(v(tb,'B12'),'Valid');assert.equal(v(tb,'B8'),2/3);});
check('Mixed criteria blocked',()=>{tb.getRange('B17').values=[['Other']];tw.recalculate();assert.equal(v(tb,'B12'),'Review records');tb.getRange('B17').values=[['Handoff-v0.1']];});
check('Duplicate IDs blocked',()=>{tb.getRange('A18').values=[['EX-2']];tw.recalculate();assert.equal(v(tb,'B12'),'Review records');tb.getRange('A18').values=[['EX-3']];});
check('All-abstention companion metrics expose zero decisions',()=>{tb.getRange('D17:D19').values=[['Unable to assess'],['Unable to assess'],['Unable to assess']];tw.recalculate();assert.equal(v(tb,'B8'),0);assert.equal(v(tb,'B9'),1);assert.equal(v(tb,'B39'),0);assert.equal(v(tb,'B40'),'n.a.');});
check('Ready control false holds and abstentions are separate',()=>{tb.getRange('C17:C19').values=[['Ready'],['Ready'],['Ready']];tb.getRange('D17:D19').values=[['Ready'],['Not ready'],['Unable to assess']];tw.recalculate();assert.equal(v(tb,'B42'),1/3);assert.equal(v(tb,'B43'),1/3);});
check('Missing judgments excluded and counted',()=>{tb.getRange('D19').values=[['Missing']];tw.recalculate();assert.equal(v(tb,'B42'),.5);assert.equal(v(tb,'B44'),1);});
for(const example of [false,true]){
 const {wb,s,b}=make(example);wb.recalculate();
 if(!example){assert.equal(v(s,'B20'),'Not evaluated');assert.equal(v(b,'B12'),'No records');}
 const scan=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:30}});
 await fs.writeFile(`${qa}/rc2-${example?'example':'blank'}-scan.json`,scan.ndjson);
 for(const [name,range]of [['Review','A1:D37'],['Batch','A1:F44']]){const img=await wb.render({sheetName:name,range,scale:1,format:'png'});await fs.writeFile(`${qa}/rc2-${example?'example':'blank'}-${name}.png`,new Uint8Array(await img.arrayBuffer()));}
 const xlsx=await SpreadsheetFile.exportXlsx(wb);await xlsx.save(example?`${out}/Worked-Example/Evaluation-Completed.xlsx`:`${out}/Evaluation-Template.xlsx`);
}
await fs.writeFile(`${qa}/rc2-workbook-tests.json`,JSON.stringify(tests,null,2));console.log(tests.join('\n'));
