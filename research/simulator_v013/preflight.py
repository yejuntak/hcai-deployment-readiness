"""Non-generative server-template/tokenizer diagnostics; no text truncation."""
import urllib.request
import simulator as s

def post(path,payload):
 req=urllib.request.Request('http://127.0.0.1:8765'+path,data=s.canonical(payload),headers={'Content-Type':'application/json'},method='POST')
 class NoRedirect(urllib.request.HTTPRedirectHandler):
  def redirect_request(self,*a,**kw):raise ValueError('REDIRECT_REJECTED')
 with urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect()).open(req,timeout=30) as r:b=r.read(2000001)
 if len(b)>2000000:raise ValueError('PROBE_TOO_LARGE')
 return s.strict_json(b)

def probe(request,post_fn=post):
 body={'messages':request['messages'],'chat_template_kwargs':request.get('chat_template_kwargs',{})}
 rendered=post_fn('/apply-template',body)['prompt']
 if any(rendered.count(m['content'])!=1 for m in request['messages'] if m['content']):raise ValueError('MESSAGE_CONTENT_NOT_RETAINED')
 tokens=post_fn('/tokenize',{'content':rendered,'add_special':False,'parse_special':True})['tokens']
 if not isinstance(tokens,list) or any(type(t) is not int for t in tokens):raise ValueError('TOKENIZER_SHAPE')
 if len(tokens)+request['max_tokens']+64>8192:raise ValueError('CONTEXT_BUDGET_WITH_MARGIN')
 return {'rendered_prompt':rendered,'token_ids':tokens,'input_tokens':len(tokens),'maximum_output_tokens':request['max_tokens'],
  'safety_margin_tokens':64,'model_calls':0,'method':'server-template diagnostic; inference-specific special tokens checked against usage','request_sha256':s.sha(s.canonical(request))}
