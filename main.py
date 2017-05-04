from vision import google_vision
import requests, re, os
from flask import Flask, jsonify, request
from fuzzywuzzy import fuzz
import subprocess, logging
import elasticsearch
import rule_engine as rules
import extraction as extract

app = Flask(__name__)
direc = os.path.dirname(__file__)
logger = logging.getLogger('service_logger')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('service.log')
handler.setLevel(logging.INFO)
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(format)
logger.addHandler(handler)

@app.route("/automatic_brand_recognition")
def index(log_obj=logger):
    user = request.args.get('user')
    #log_obj = logging.getLogger('service_logger')
    credentials = os.path.join(direc, 'Q_DSaaS_v1-40635af5d3e8.json')
    log_obj.info('Starting logger')
    #Data Sets [REPLACE BY HDFS File Access]
    image_path = os.path.join(direc, 'images/' + user)
    
    #Modules
    vision = google_vision(path_to_discovery_file=credentials, log_obj=log_obj)

    #Requests and Indexing
    response = vision.get_response(image_path)

    #new_db = es_instance.get_es() #indexed elastic_search

    output = {}

    if 'logoAnnotations' in response['responses'][0]:
        output['Google_Vision'] = response['responses'][0]['logoAnnotations'][0]['description']
    else:
        output['Google_Vision'] = 'null'

    if 'textAnnotations' in response['responses'][0]:
        output['OCR'] = response['responses'][0]['textAnnotations'][0]['description']
        ocr = re.sub('[^A-Za-z0-9.//]', " ", output['OCR'])
        output['OCR'] = ocr
    else:
        output['OCR'] = 'null'

    #Test queries for elastic search
    res = elasticsearch.Elasticsearch(hosts='localhost:9200')
    log_obj.info('ES connection made')
    brand_search = res.search(index='brands', body={'query': {'match':{'brand': output['OCR']}}})['hits']['hits']
    tag_search = res.search(index='tags', body={"query": { "multi_match": {"query" : output['OCR'], "fields" : "tagline", "fuzziness": "AUTO"}}})['hits']['hits']

    brand_1, brand_2, brand_3 = brand_search[0]['_source']['brand'], brand_search[1]['_source']['brand'], brand_search[2]['_source']['brand']
    log_obj.info('Retreived top 3 brands from ES')
    tag_1, tag_2, tag_3 = tag_search[0]['_source']['brand'], tag_search[1]['_source']['brand'], tag_search[2]['_source']['brand']
    log_obj.info('Retreived top 3 tags from ES')

    output['Facebook URL'] = extract.get_facebook(output['OCR'])
    output['Website URL'] = extract.get_website_url(output['OCR'])
   

    if output['Google_Vision'] == 'null':
        prediction = rules.rule_ocr_tag(brand_1, brand_2, brand_3, tag_1, tag_2, tag_3)
        output['Brand Prediction'] = prediction
        log_obj.info('Brand-Tag Rule')
        #output['rule'] = 'third'
        return jsonify(output)

    prediction = rules.rule_tag_logo(tag_1, tag_2, tag_3, output['Google_Vision'])
    
    if prediction != 'null':
        output['Brand Prediction'] = rules.rule_tag_logo(tag_1, tag_2, tag_3, output['Google_Vision'])
        log_obj.info('Tag-Logo Rule')
        #output['rule'] = 'second'
        return jsonify(output)
    else:
        output['Brand Prediction'] = rules.rule_brand_logo(brand_1, brand_2, brand_3, output['Google_Vision'])
        log_obj.info('Brand-Logo Rule')
        #output['rule'] = 'first'
        return jsonify(output)

if __name__ == "__main__":
    app.run(host='0.0.0.0')