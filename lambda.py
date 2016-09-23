import json
from datetime import datetime
from StringIO import StringIO

import boto3


def lambda_handler(event, context):
	s3 = boto3.resource('s3')

	bucket = s3.Bucket('utdmakerspace')

	obj = bucket.Object('events.json')

	data = json.load(obj.get()['Body'])

	for event in data:
		end = datetime.strptime(event['end'], '%Y-%m-%dT%H:%M:%S')
		now = datetime.now()

		if end < now:
			print event['title']
			event['expired'] = True

	data = [x for x in data if 'expired' not in x]

	obj.upload_fileobj(StringIO(json.dumps(data)))
