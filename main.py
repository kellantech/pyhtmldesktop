import tkinter as tk
import tkinter.font

from bs4 import BeautifulSoup as bs4
import re

data = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">

  <title>Title here</title>
<style>
#x{
	background-color:orange;
	margin:15;
}
</style>
</head>

<body>
<h4 style='background-color:green'>test2</h4>
<h1 style='background-color:red;margin: 15;'>hello</h1>
<p style='background-color:blue;left:300;'>test</p>
<p id='x'>
test
::br
t3
</p>
<h1 style='background-color:red;margin: 15;'>hello</h1>
<button onclick='test()'>test</button>

</body>
</html>
"""


soup = bs4(data,'html.parser')


def get_p():
	xs = soup.find('body').findChildren(recursive=True)
	res = []
	for x in xs:
		csty = x['style'].split(';') if 'style' in x.attrs.keys() else []
		ccl = x['onclick'] if 'onclick' in x.attrs.keys() else ""
		cid = x['id'] if 'id' in x.attrs.keys() else None

		res.append({'text':x.text,'elm':x.name,'style':csty,'id':cid,'onclick':ccl})
	return res


iso = lambda d: [x.replace('\n','') for x in re.findall(r'\S+{[\S\s]*?}',d)]


def pcss(c):
  y = iso(c)
  res = []
  for r in y:
    res.append([
      re.search(r'\S+?{',r).group(0)[:-1],
      re.search(r'{[\S\s]*?}',r).group(0),
    ])
  res2 = {}
  for r2 in res:
    res2[r2[0]]=\
      [n.replace('}','').replace('{','').strip() \
                                    for n in r2[1].split(';')]
    if '' in res2[r2[0]]: 
      res2[r2[0]].remove('')
  return res2



main = tk.Tk()
main.configure(background='white')
main.option_add('*font','lucida 11')

fsz = {"h1":32,'h2':24,'h3':21,'h4':16,'p':16,'button':16}


main.geometry('500x500')
main.title(soup.find('title').text)

gsty = pcss(soup.find('style').text)
print(gsty)
class elm:
	def __init__(self,text,x,y,fsi=11,at={},pt={},typ=tk.Label):
		self.sty_attrs = {'text':text,'bg':'white','fg':'black','font':('lucida',fsi),**at}
		self.pos_attrs = {'x':x,'y':y,**pt}
		self.tk = typ(**self.sty_attrs)
		self.fsize = tk.font.Font(font=f'lucida {fsi}').metrics('linespace')

	def render(self):
		self.tk.place(**self.pos_attrs)


p_elm = get_p()


print(p_elm)
ce = []
def parse_style(s):
	catr = {}
	patr = {}
	mgn = 0
	for sty in s:

		pr = sty.split(':')
		if pr[0] == 'color':
			catr['fg'] = pr[1]
		if pr[0] == 'background-color':
			catr['bg'] = pr[1]
		if pr[0] == 'margin':
			mgn = int(pr[1].replace('px',''))
		if pr[0] == 'left':
			patr['x'] = int(pr[1])
		if pr[0] == 'top':
			patr['y'] = int(pr[1])
		
	return catr,mgn,patr
def test():
	global y
	y= 0
	print('!!')
	p_elm[0]['text'] = 'test good'
	render()
	
global y


y = 0
mgn = 0
def render():
	global y,mgn
	for el in p_elm:
		print('--')
		y+=mgn if len(ce) > 0 else 0
		print(el['text'].split('::br'))
		

		for tx2 in el['text'].split('::br'):
			tx = tx2.replace('\n','')
			catr1,mgn1,patr1 = parse_style(el['style'])
			if el['id'] != None:

				catr2,mgn2,patr2 = parse_style(gsty["#"+el['id']])

				catr = {**catr1,**catr2}
				patr = {**patr1, **patr2}
				mgn = mgn1 or mgn2
			else:
				mgn = mgn1
				catr = catr1
				patr = patr1
			if el['elm'] == "button":

				catr['command'] = lambda:exec(el['onclick'],globals())
			print('!!!!!',catr)
			celm = elm(tx,0,y,fsz[el['elm']],catr,patr,(tk.Label if el['elm'] != "button" else tk.Button))
			ce.append(celm)
			ce[-1].render()
			y+=ce[-1].fsize
		y += mgn
		print('-')
render()




main.mainloop()
