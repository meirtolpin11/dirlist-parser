from flask import Flask, request, render_template, jsonify
from database import * 
from peewee import *
import json

app = Flask(__name__)

@app.route("/get_folder_children")
def index():
	parent_id = request.args.get("parentId")

	# no parent id - show all available drives 
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
	 DirListInfo.entity_type, DirListInfo.entity_id, DirListInfo.entity_date, DirListInfo.entity_size).where(DirListInfo.entity_root_path == parent_id + "\\").distinct().execute()
	
	children_json = []
	for child in children:
		children_json.append({
			"id": ''.join([child.entity_root_path, child.entity_name]),
			"parentId": parent_id,
			"text": child.entity_name,
			"hasItems": True if child.entity_type == 'DIR' else False,
			"fullPath": ''.join([child.entity_root_path, child.entity_name]),
			"date": child.entity_date,
			"size": child.entity_size
			})


	return jsonify(children_json)

@app.route("/add_file_to_starred")
def add_file_to_cart():
	computer_id = request.args.get("computer_id")
	entity_id = request.args.get("entity_id")

	StarredFiles().insert(computer_id = computer_id, entity_id = entity_id).execute()

	return "OK"

@app.route('/')
def test():
	return render_template('index.html')

app.run()