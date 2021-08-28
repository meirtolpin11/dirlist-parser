from flask import Flask, request, render_template, jsonify
from database import * 
from peewee import *
import json

app = Flask(__name__)

@app.route("/get_folder_children")
def index():
	parent_id = request.args.get("parentId")
	if parent_id is None or len(parent_id) == 0:
		
		drives = DirListInfo.select(DirListInfo.entity_drive).distinct().execute()
		children_json = []
		for drive in drives:
			children_json.append({
				"id": drive.entity_drive + ":",
				"parentId": None,
				"text": drive.entity_drive + ":\\",
				"hasItems": True
				})

		return jsonify(children_json)


	# quering all the subfolder and files inside the parent folder 
	children = DirListInfo.select(DirListInfo.entity_root_path, DirListInfo.entity_name,\
	 DirListInfo.entity_type, DirListInfo.entity_id).where(DirListInfo.entity_root_path == parent_id + "\\").distinct().execute()
	
	children_json = []
	for child in children:
		children_json.append({
			"id": ''.join([child.entity_root_path, child.entity_name]),
			"parentId": parent_id,
			"text": child.entity_name,
			"hasItems": True if child.entity_type == 'DIR' else False
			})


	return jsonify(children_json)

@app.route('/')
def test():
	return render_template('index.html')

app.run()