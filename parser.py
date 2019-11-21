import requests

def load_data(data_folder):
    url = 'http://mygene.info/v3/query?q=*:*&fetch_all=True&dotfield=True&fields=ensembl.gene,HGNC,MIM,entrezgene,pharos.target_id,umls.cui,unigene,pharmgkb,name,symbol'
    cnt = 0
    total = 1
    print(total)
    while cnt < total:
        doc = requests.get(url).json()
        total = doc['total']
        cnt += len(doc['hits'])
        url = 'http://mygene.info/v3/query?scroll_id=' + doc['_scroll_id']
        print(url)
        print(cnt)
        for _doc in doc['hits']:
            _doc = restructure_output(_doc)
            primary_id = get_primary_id(_doc)
            if primary_id:
                _doc.pop('_score')
                _doc['_id'] = primary_id
                yield _doc


def restructure_output(_doc):
    """Restructure the API output"""
    field_mapping = {'HGNC': 'hgnc',
                     'ensembl.gene': 'ensembl',
                     'MIM': 'omim',
                     'entrezgene': 'entrez',
                     'pharos.target_id': 'pharos',
                     'umls.cui': 'umls'}
    # loop through mapping, change the field name one by one
    for k, v in field_mapping.items():
        if _doc.get(k):
            _doc[v] = _doc.pop(k)
    return _doc

def get_primary_id(_doc):
    """get the primary id for each doc"""
    ID_RANKS = ['entrez', 'ensembl', 'symbol', 'umls', 'hgnc', 'omim', 'pharmgkb', 'pharos']
    for _id in ID_RANKS:
        if _doc.get(_id):
            return (_id + ':' + str(_doc.get(_id)))