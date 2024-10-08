const axios = require('axios');

const BASE_URL = 'https://parallelum.com.br/fipe/api/v1/carros/marcas';

async function getBrandCode(mark) {
    let request = await axios.get(BASE_URL);
    let response = request.data;

    for (let item of response) {
        if (item.nome.toUpperCase() === mark.toUpperCase()) {
            return item.codigo;
        }
    }
    return 'Marca não encontrada';
}

async function getModelCode(code_brand, model_name) {
    try {
        let url = `${BASE_URL}/${code_brand}/modelos`
        let request = await axios.get(url);
        let response = request.data.modelos;

        for(let item of response) {
            if (item.nome.toUpperCase().includes(model_name.toUpperCase())) {
                return item.codigo;
            }
        }
        return 'Modelo não encontrado';
    }catch(error) {
        console.log('Erro na requisição: ', error.message)
        return 'Erro ao buscar o modelo'
    }
}

async function getPrice(code_brand, code_model, age) {
    try {
        let url = `${BASE_URL}/${code_brand}/modelos/${code_model}/anos`;
        let request = await axios.get(url);
        let response = request.data;

        for (let item of response) {
            if (item.nome.includes(String(age))) {
                let priceUrl = `${BASE_URL}/${code_brand}/modelos/${code_model}/anos/${item.codigo}`;
                let response_price = await axios.get(priceUrl);
                let price = response_price.data.Valor;
                return price;
            }
        }
        return 'Ano não encontrado';
    } catch (error) {
        console.error('Erro na requisição:', error.message);
        return 'Erro ao buscar o preço';
    }
}

async function getFipePrice(brand, model, age) {
    try {
        let brandCode = await getBrandCode(brand);
        if (brandCode === 'Marca não encontrada') {
            console.log(brandCode);
            return;
        }

        let modelCode = await getModelCode(brandCode, model);
        if (modelCode === 'Modelo não encontrado') {
            console.log(modelCode);
            return;
        }

        let price = await getPrice(brandCode, modelCode, age);
        console.log(`O preço do ${model} (${age}) é: ${price}`);
    } catch(error) {
        console.log('Erro ao procurar o preço na tabela FIPE: ', error.message)
        return `Erro ao procurar o preço!`
    }
}
