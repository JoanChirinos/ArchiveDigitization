"""
ArchiveDigitization

Helper functions for the main Flask file

Copyright Joan Chirinos, 2021.
"""

import json, requests, sys, os

def verify_auth_args(*args: str) -> bool:
    """
    Verify arguments from user-inputted authentication forms

    Parameters
    ----------
    *args : str
        The non-keyworded arguments to verify

    Returns
    -------
    bool
        True if all form elemens are valid.
        False otherwise.

    """
    # TODO: Robustify. Possibly using **kwargs and arg-specific verification
    # TODO: Return some sequence or mapping corresponding to which args are
    #       invalid
    for arg in args:
        if len(arg.strip()) == 0 or arg.strip() != arg:
            return False
    return True


def get_text(imgUri: str) -> str:
    '''
    Get text from text image using Google Vision API

    Parameters
    ----------
    imgUri : str
        the URI for the image.

    Returns
    -------
    str
        the text from the image.

    '''
    # build the endpoint
    key = os.environ.get('GOOGLE_API_KEY')
    endpoint = f'https://vision.googleapis.com/v1/images:annotate?key={key}'

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

    print(r)
    print(r.text)

    j = json.loads(r.text)
    return j['responses'][0]['fullTextAnnotation']['text']
