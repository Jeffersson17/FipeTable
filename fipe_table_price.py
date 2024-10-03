import requests

BASE_URL = 'https://parallelum.com.br/fipe/api/v1/carros/marcas'

# Função para encontrar o código da marca
def search_brand_code(mark):
    url = f'{BASE_URL}'
    response = requests.get(url)
    marks = response.json()

    for item in marks:
        if item['nome'].upper() == mark.upper():
            return item['codigo']
    return None

# Lista todas as marcas disponiveis
def list_brands():
    url = f'{BASE_URL}'
    response = requests.get(url)
    brands = response.json()
    names_brands = []

    for item in brands:
        names_brands.append(item['nome'])
    return names_brands

# Função para encontrar o código do modelo da marca
def search_model_code(mark_code, model_name):
    url = f'{BASE_URL}/{mark_code}/modelos'
    response = requests.get(url)
    models = response.json()['modelos']

    for item in models:
        if model_name.upper() in item['nome'].upper():
            return item['codigo']
    return None

# Lista todas as marcas disponiveis
def list_models(code_mark):
    url = f'{BASE_URL}/{code_mark}/modelos'
    response = requests.get(url)
    models = response.json()['modelos']
    names_models = [item['nome'] for item in models]
    return names_models

# Função para listar todos os anos do modelo escolhido
def list_ages(code_mark, code_model):
    url = f'{BASE_URL}/{code_mark}/modelos/{code_model}/anos'
    response = requests.get(url)
    age = response.json()
    ages = []


    for item in age:
        ages.append(item['nome'])
    return ages

# Função para encontrar o preço da marca e do modelo
def search_price(mark_code, model_code, age):
    url = f'{BASE_URL}/{mark_code}/modelos/{model_code}/anos'
    response = requests.get(url)
    years = response.json()

    for item in years:
        if str(age) in item['nome']:
            url_price = f'{BASE_URL}/{mark_code}/modelos/{model_code}/anos/{item['codigo']}'
            response_price = requests.get(url_price)
            price = response_price.json()
            return price['Valor']
    return None

# Função que encontra o preço da tabela fipe
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

# Exibi as marcas
print('↓↓↓ Marcas ↓↓↓')
print(list_brands())
mark = str(input('\nMarca: ')).upper()

# Busca e exibi os modelos da marca selecionada
print(f'↓↓↓ Modelos do(a) {mark} ↓↓↓')
code_mark = search_brand_code(mark)
print(list_models(code_mark))
model = str(input('Modelo: ')).upper()

# Busca e exibi os anos da marca e modelo selecionado
print(f'↓↓↓ Anos do(a) {mark} {model} ↓↓↓')
code_model = search_model_code(code_mark, model)
print(list_ages(code_mark, code_model))
age = int(input('Ano: '))

# Busca e exibi o preço da tabela FIPE para o veículo selecionado
search_fipe_price(mark, model, age)