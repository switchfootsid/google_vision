import base64
from googleapiclient import discovery
from googleapiclient import errors #handling errors
from oauth2client.client import GoogleCredentials
from oauth2client.service_account import ServiceAccountCredentials

class google_vision:
    """
    Create Google Vision objects and enable OCR/Label Detection
    1. Define OCR method 
    2. Define Label Detection method
    3. HDFS File access
    4. Add exception handling
    5. Add logging and timeout
    """
    
    def __init__(self, path_to_discovery_file):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(path_to_discovery_file)
        self.service = discovery.build('vision', 'v1', credentials=self.credentials)
    
    def get_response(self, photo_file):
        with open(photo_file, 'rb') as image:
            image_content = base64.b64encode(image.read())
            service_request = self.service.images().annotate(body={
                'requests': [{
                    'image': {
                        'content': image_content.decode('UTF-8')
                    },
                    'features': [
                        {
                        'type': 'LOGO_DETECTION',
                        'maxResults': 1
                    },
                        {
                            'type' : 'TEXT_DETECTION',
                            'maxResults': 1
                        }
                    ]
                }]
            })
        
        try:
            response = service_request.execute()

            if 'responses' not in response:
                print 'no response'
                return {}
            else:
                return response
        except:
            return 'null'
