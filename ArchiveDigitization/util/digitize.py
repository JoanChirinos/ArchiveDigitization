'''
Archive Digitization

Python file facilitating document digitization

Copyright Joan Chirinos, 2021.
'''

import os

import concurrent.futures
import urllib.request

import util.db

def get_text(id: str) -> str:
    '''
    Get text from text image using Google Vision API

    Parameters
    ----------
    id : str
        the id for the image.

    Returns
    -------
    str
        the text from the image.

    '''
    # build the Google endpoint
    key = os.environ.get('GOOGLE_API_KEY')
    endpoint = f'https://vision.googleapis.com/v1/images:annotate?key={key}'

    # build the image endpoint
    imgUri = f'https://risleyarchives.com/static/imgs/{id}.png'

    # build the request
    ImageSource = {'imageUri': imgUri}
    Image = {'source': ImageSource}
    Feature = {'type': 'DOCUMENT_TEXT_DETECTION',
               'maxResults': 10}
    AnnotateImageRequest = {'image': Image,
                            'features': Feature}
    RawRequest = {'requests': [AnnotateImageRequest]}
    Request = json.dumps(RawRequest)

    # print(Request)

    r = requests.post(endpoint, data=Request)

    # print(r)
    # print(r.text)

    j = json.loads(r.text)
    return j['responses'][0]['fullTextAnnotation']['text']

def main(dbm: 'DBManager', path_to_static: str):
    '''
    Manage the ThreadPoolExecutor.

    Parameters
    ----------
    dbm : DBManager
        the DataBase Manager.
    path_to_static : str
        the path to the static folder.

    Returns
    -------
    type
        Description of returned object.

    '''
    # Here we get the IDs for the docs that need to be digitized
    IDs = dbm.get_file_ids(True, False)

    # Here we create a pool of threads that are each working to send off the
    # images to be digitized
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_id = {executor.submit(get_text, id): id for id in IDs}
        for future in concurrent.futures.as_completed(future_to_url):
            id = future_to_id[future]
            try:
                data = future.result()
                text_file_path = os.path.join(path_to_static,
                                             'text/',
                                             f'{id}.txt')
                with open(text_file_path, 'w+') as f:
                    f.write(data)
                dbm.set_digitized(id)
            except Exception as exc:
                print(f'{id} generated an exception: {exc}')
            else:
                print(f'{id} has been digitized')

'''
Example code from python3.8 docs:

import concurrent.futures
import urllib.request

URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://some-made-up-domain.com/']

# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(data)))

'''
