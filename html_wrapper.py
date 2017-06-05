# -*- coding: utf-8 -*-
import os, time
from collections import namedtuple
Content = namedtuple("Content", ("pic", "message", "name", "date") )

def generate_tmpl_index(tmpl_fname, msg_fname, dialog):
	"""
	pattern tmpl_fname has {content} key name
	pattern msg_fname has {content.[out, body and date]} keys
	dialog: instance loaded from json dialog 
	"""
	names = ("In", "Out")
	pic_tmpl = "assets/img/{}.png"
	contents = []
	with open(msg_fname) as f:
		tmpl = f.read()
	with open(tmpl_fname) as f:
		data = f.read()
	for msg in dialog:
		content = Content(pic=pic_tmpl.format(msg["out"]), 
						name=names[msg["out"]],
						date=time.asctime(time.gmtime(msg['date'])),
						message=msg["body"]
		)
		contents.append(tmpl.format(content=content))
	return data.format(content='\n'.join(contents))

def test(save_name="index.htm"):
	msg = dict(out= 0, date=1496649976.0, body = "Привет")
	res = []
	for _ in xrange(50):
		msg["out"] = 0
		
		res.append(msg.copy())
		msg["out"] = 1
		
		res.append(msg.copy())

	data = generate_tmpl_index("tmpl.html", "tmpl_msg.html", res)
	with open(save_name, 'w') as f:
		f.write(data)

test()