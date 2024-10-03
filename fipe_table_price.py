import requests

#Função para encontrar o código da marca
def search_brand_code(mark):
    url = 'https://parallelum.com.br/fipe/api/v1/carros/marcas'
    response = requests.get(url)
    marks = response.json()

    for item in marks:
        if item['nome'].upper() == mark.upper():
            return item['codigo']
    return None


#Função para encontrar o código do modelo da marca
def search_model_code(mark_code, model_name):
    url = f'https://parallelum.com.br/fipe/api/v1/carros/marcas/{mark_code}/modelos'
    response = requests.get(url)
    models = response.json()['modelos']

    for item in models:
        if model_name.upper() in item['nome'].upper():
            return item['codigo']
    return None

#Função para encontrar o preço da marca e do modelo
def search_price(mark_code, model_code, age):
    url = f'https://parallelum.com.br/fipe/api/v1/carros/marcas/{mark_code}/modelos/{model_code}/anos'
    response = requests.get(url)
    years = response.json()

    for item in years:
        if str(age) in item['nome']:
            url_price = f'https://parallelum.com.br/fipe/api/v1/carros/marcas/{mark_code}/modelos/{model_code}/anos/{item['codigo']}'
            response_price = requests.get(url_price)
            price = response_price.json()
            return price['Valor']
    return None


#Função que encontra o preço da tabela fipe
def search_fipe_price(mark, model, age):
    mark_code = search_brand_code(mark)
    if not mark_code:
        return print('Marca não encontrada!')

    model_code = search_model_code(mark_code, model)
    if not model_code:
        return print('Modelo não encontrado!')

    price = search_price(mark_code, model_code, age)
    if price:
        return print(f'O preço do {mark} {model} {age} na tabela FIPE é {price}.')
    else:
        return print('Ano não encontrado!')


mark = str(input('Marca: ')).capitalize()
model = str(input('Modelo: ')).capitalize()
age = int(input('Ano: '))

search_fipe_price(mark, model, age)
