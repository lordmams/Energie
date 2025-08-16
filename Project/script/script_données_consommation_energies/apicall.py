import requests

sourceUrl = "https://odre.opendatasoft.com/api/explore/v2.0"
def query_dataset_records(
        dataset_id, 
        select=None, 
        where=None, 
        group_by=None, 
        order_by=None, 
        limit=None, 
        offset=None, 
        refine=None, 
        exclude=None, 
        lang=None, 
        timezone=None):
    # Base URL for the API endpoint
    base_url = sourceUrl+"/catalog/datasets/{}/records".format(dataset_id)
    
    # Construct query parameters
    params = {}
    if select:
        params['select'] = select
    if where:
        params['where'] = where
    if group_by:
        params['group_by'] = group_by
    if order_by:
        params['order_by'] = order_by
    if limit:
        params['limit'] = limit
    if offset:
        params['offset'] = offset
    if refine:
        params['refine'] = refine
    if exclude:
        params['exclude'] = exclude
    if lang:
        params['lang'] = lang
    if timezone:
        params['timezone'] = timezone
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() 
        data = response.json() 
        return data
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return None
    
def export_dataset_to_csv(dataset_id, delimiter=";", list_separator=",", quote_all=False, with_bom=False):
    base_url = sourceUrl+"/catalog/datasets/{}/exports/csv".format(dataset_id)
    
    params = {
        'delimiter': delimiter,
        'list_separator': list_separator,
        'quote_all': quote_all,
        'with_bom': with_bom
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() 
        
        if 'text/csv' in response.headers.get('content-type', ''):
            return response.content
        else:
            print("Unexpected response content type:", response.headers.get('content-type'))
            return None
    except requests.exceptions.RequestException as e:
        print("Error exporting dataset:", e)
        return None

dataset_id = "consommation-nationale-horaire-de-gaz-donnees-provisoires-grtgaz-terega-v2"

csv_data = export_dataset_to_csv(dataset_id)
if csv_data:
    # Save CSV data to a file
    with open("exported_dataset.csv", "wb") as csv_file:
        csv_file.write(csv_data)
    print("Dataset exported to 'exported_dataset.csv'")
else:
    print("Failed to export dataset.")
    
dataset_id = "consommation-nationale-horaire-de-gaz-donnees-provisoires-grtgaz-terega-v2"

data = query_dataset_records(dataset_id,select="consommation_journaliere_mwh_pcs",limit=10)
if data:
    print("Received data from API:", data)
else:
    print("Failed to fetch data from API.")
