<template>
    <div class="container" id="app">
        <h1>Buscar Preço na Tabela FIPE</h1>
        <div class="mb-3 row">
            <v-combobox
            v-model="selectedBrand"
            label="Selecione a Marca"
            :items="listBrand"
            @change="listModels"
            ></v-combobox>
        </div>
        <div class="mb-3 row">
            <v-combobox
            v-model="selectedModel"
            label="Selecione o Modelo"
            :items="listModel"
            @change="listAges"
            ></v-combobox>
        </div>
        <div class="mb-3 row">
            <v-combobox
            v-model="selectedAge"
            label="Selecione o Ano"
            :items="listAge"
            ></v-combobox>
        <p id="result">{{ result }}</p>
        </div>
        <div id="button-submit">
            <button class="btn btn-success" @click="fetchFipePrice">BUSCAR</button>
        </div>
        <footer class="footer">
            <div class="container">
                <div class="text-center">
                    <p>&copy; 2024 Jeffersson Barros</p>
                </div>
            </div>
        </footer>
    </div>
</template>

<script>
export default {
    name: 'PriceFipeTable',
    data() {
        return {
            selectedBrand:"",
            selectedModel:"",
            selectedAge:"",
            listBrand: [],
            listModel: [],
            listAge: [],
            result: "",
        }
    },

    created() {
        this.listBrands()
    },

    methods: {
        async fetchFipePrice() {
            this.result = await getFipePrice(this.selectedBrand, this.selectedModel, this.selectedAge)
        },
        async listBrands() {
            try {
                const response = await axios.get(BASE_URL);
                this.listBrand = response.data.map(brand => brand.nome);
            } catch (error) {
                console.error('Erro ao buscar as marcas:', error.message);
            }
        },
        async listModels() {
            if (!this.selectedBrand) return "Não foi possivel encontrar os modelos";
            try {
                const codeBrand = await getBrandCode(this.selectedBrand);
                console.log('Código da marca selecionada:', codeBrand);
                const response = await axios.get(`${BASE_URL}/${codeBrand}/modelos`);
                this.listModel = response.data.modelos.map(model => model.nome)
                console.log('Modelos carregados:', this.listModel);

            } catch(error) {
                console.error('Erro ao buscar os modelos:', error.message);
            }
        },
        async listAges() {
            try {
                const codeBrand = await getBrandCode(this.selectedBrand);
                const codeModel = await getModelCode(codeBrand, this.selectedModel)
                const response = await axios.get(`${BASE_URL}/${codeBrand}/modelos/${codeModel}/anos`);
                this.listAge = response.data.map(age => age.nome)

            } catch(error) {
                console.error('Erro ao buscar os anos:', error.message);
            }
        }
    }
}

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
        return `O preço do(a) ${brand} ${model} ${age} é: ${price}`;
    } catch(error) {
        console.log('Erro ao procurar o preço na tabela FIPE: ', error.message)
        return `Erro ao procurar o preço!`
    }
}
</script>

<style>
h1 {
    font-family: 'Courier New', Courier, monospace;
    text-align: center;
    margin: 30px;
}

label {
    font-family: 'Copperplate';
}

#result {
    margin: 15px;
    font-family: 'Copperplate';
    text-align: center
}

#button-submit{
  margin: 5px;
  text-align: right;
}
</style>