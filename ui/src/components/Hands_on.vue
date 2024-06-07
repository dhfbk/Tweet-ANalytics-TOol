<template>
  <div class="container bigcontainer">
    <h1 class="title">3. Analyse</h1>
    <div class="containersubtitle ps-3">
      <p class="subtitle">
        On this page you can find data sets collected from Twitter that refer to gender violence. You can use this tool
        to explore data and learn more about social media dynamics. Follow the instructions in each of the following
        sections and you can play with the data! At the end of the page you will also find some examples on how to
        explore the data.
      </p>
    </div>


    <div class="container">
      <div class="row">
        <div class="col">
          <p><strong>What is a dataset?</strong></p>
          <p>Only few social media sites allow free and open access to your own data. The most important was Twitter
            which, before becoming "X", long allowed free access to its public data, also becoming a point of reference
            for the study of online behavior. On the following page you can select different data collections (datasets)
            created from public Twitter data, specifying the desired time period and the keywords used as search terms.
            For example, the "Woman women" dataset is a collection of tweets published online between 2010 and 2022 that
            contain the words woman/women. When you select a specific dataset, a description of how it was created is
            displayed.
          </p>
        </div>
      </div>
      <div class="row">
        <div class="col" v-if="loaded">
          <p class="pt-1">
            Select a language:
          </p>
          <p class="pt-1">
            <select v-model="selectedLanguage" @change="changeLanguage()"
                    v-if="Object.keys(languages).length !== 0" class="form-select"
                    aria-label="Select dataset">
              <option selected value="">[Select one]</option>
              <option :key="index" :value="index" v-for="(lang, index) in languages">
                {{ lang }}
              </option>
            </select>
          </p>
          <template v-if="selectedLanguage">
            <template v-if="selectedLanguage in datasets">
              <p class="pt-1">
                Select a dataset:
              </p>
              <p class="pt-1">
                <select v-model="selectedDataset" @change="loadDataset()"
                        v-if="Object.keys(datasets[selectedLanguage]).length !== 0" class="form-select"
                        aria-label="Select dataset">
                  <option selected value="">[Select one]</option>
                  <option :key="index" :value="index" v-for="(dataset, index) in datasets[selectedLanguage]">
                    {{ dataset.name }}
                  </option>
                </select>
              </p>
            </template>
            <template v-else>
              <p class="pt-1">
                No datasets.
              </p>
            </template>
          </template>

          <div v-if="selectedDataset">
            <p>{{ datasets[selectedLanguage][selectedDataset]['description'] }}</p>

            <h3>Filters</h3>
            <form id="taskForm" @submit.stop.prevent="submit">
              <div class="row">
                <div class="col-12 input-group mb-3 date input-daterange" id="dr">
                  <span class="input-group-text"><i class="bi bi-calendar-date"></i></span>
                  <span class="input-group-text d-md-flex d-none">From</span>
                  <Datepicker v-bind="dateConfig" class="form-control" id="dr1"
                              v-model="start_date" format="yyyy-MM-dd"
                              autoApply :enableTimePicker="false" :clearable="false"
                              :utc="true"></Datepicker>
                  <span class="input-group-text">to</span>
                  <Datepicker v-bind="dateConfig" class="form-control" id="dr1"
                              v-model="end_date" format="yyyy-MM-dd"
                              autoApply :enableTimePicker="false" :clearable="false"
                              :utc="true"></Datepicker>
                </div>

                <div class="col-10">

                  <div class="input-group mb-3">
                    <input v-model="searchTerm" name="searchTerm" class="form-control" id="searchTerm"
                           placeholder="Cerca parola"/>
                    <button class="btn btn-outline-secondary" type="button" id="button-addon2" @click="resetWord"><i
                        class="bi bi-x"></i></button>
                  </div>

                </div>
                <div class="col-2">
                  <button type="submit" class="btn btn-primary mb-3">Aggiorna</button>
                </div>

              </div>
            </form>


            <h3>Chart</h3>
            <div class="p-3" v-if="loadedDataset">
              <template v-if="datasetError">
                {{ datasetError }}
              </template>
              <div v-else id="vis" style="width: 100%; height: 300px;"></div>
            </div>
            <div v-else class="text-center">
              <div class="spinner-border" role="status">
              </div>
              <br/>
              Loading...
            </div>

            <h3>Tag cloud</h3>
            <div v-if="loadedImage" class="text-center">
              <template v-if="imageError">
                {{ imageError }}
              </template>
              <img v-else :src="imageUrl" alt="Tag cloud" title="Tag cloud" class="tag-cloud"/>
            </div>
            <div v-else class="text-center">
              <div class="spinner-border" role="status">
              </div>
              <br/>
              Loading...
            </div>

            <h3>Hashtag network</h3>
            <div v-if="loadedHashtag" class="text-center">
              <template v-if="hashtagError">
                {{ hashtagError }}
              </template>
              <iframe v-else :srcdoc="hashtagContent" width="100%" height="500"></iframe>
            </div>
            <div v-else class="text-center">
              <div class="spinner-border" role="status">
              </div>
              <br/>
              Loading...
            </div>

          </div>
        </div>
        <div class="col" v-else>
          <div class="spinner-border" role="status">
          </div>
          <br/>
          <p>Loading...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

//import Iltest from "../assets/Iltest";
import axios from "axios";
import vegaEmbed from "vega-embed";
import Datepicker from '@vuepic/vue-datepicker';
import data from "bootstrap/js/src/dom/data.js";
// import '@vuepic/vue-datepicker/dist/main.css'

export default {
  name: "App",
  computed: {
    data() {
      return data
    }
  },
  components: {Datepicker},
  data: function () {
    return {
      loaded: false,

      loadedDataset: false,
      loadedImage: false,
      loadedHashtag: false,

      hashtagError: undefined,
      imageError: undefined,
      datasetError: undefined,

      hashtagContent: "",
      imageUrl: "",
      datasets: {},
      selectedDataset: "",
      selectedLanguage: "",
      languages: {},
      start_date: "",
      end_date: "",
      dateConfig: {},
      searchTerm: "",
    };
  },
  mounted: function () {
    let realThis = this;
    realThis.loaded = false;
    Promise.all([axios.get(process.env.BASE_API + "/api/languages"), axios.get(process.env.BASE_API + "/api/datasets")])
        .then(function (results) {
          realThis.loaded = true;
          realThis.languages = results[0].data;
          const response = results[1];
          for (let datasetName in response.data) {
            if (!(response.data[datasetName]["lang"] in realThis.datasets)) {
              realThis.datasets[response.data[datasetName]["lang"]] = {};
            }
            realThis.datasets[response.data[datasetName]["lang"]][datasetName] = response.data[datasetName];
          }
        });
  },
  methods: {
    resetWord: function () {
      this.searchTerm = "";
      this.submit();
    },
    submit: function () {
      this.reset();

      this.updateDataset({
        "d0": this.start_date.split('T')[0],
        "d1": this.end_date.split('T')[0],
        "words": this.searchTerm
      });
    },
    changeLanguage: function () {
      this.loadedDataset = false;
      this.selectedDataset = "";
    },
    reset: function () {
      this.loadedDataset = false;
      this.loadedImage = false;
      this.loadedHashtag = false;
      this.hashtagError = undefined;
      this.datasetError = undefined;
      this.imageError = undefined;
    },
    loadDataset: function () {
      let realThis = this;
      this.reset();
      this.searchTerm = "";

      let dataset = this.datasets[this.selectedLanguage][this.selectedDataset];
      realThis.start_date = dataset['date_start'];
      realThis.end_date = dataset['date_end'];
      realThis.dateConfig["min-date"] = new Date(Date.parse(realThis.start_date));
      realThis.dateConfig["max-date"] = new Date(Date.parse(realThis.end_date));
      realThis.dateConfig["min-date"].setDate(realThis.dateConfig["min-date"].getDate() - 1);
      realThis.dateConfig["max-date"].setDate(realThis.dateConfig["max-date"].getDate() - 1);

      this.updateDataset({});
    },
    updateDataset: function (pars) {
      let realThis = this;

      // Load chart
      let tmpDatasetUrl = process.env.BASE_API + "/api/dataset/" + this.selectedDataset;
      axios.get(tmpDatasetUrl, {params: pars}).then(function (response) {
        realThis.loadedDataset = true;
        vegaEmbed('#vis', response.data);
      }).catch(function (response) {
        realThis.datasetError = response.response.data.detail;
      }).then(function () {
        realThis.loadedDataset = true;

        // Load network
        let tmpHashtagUrl = process.env.BASE_API + "/api/hashtag/" + realThis.selectedDataset;
        axios.get(tmpHashtagUrl, {params: pars}).then(function (response) {
          realThis.hashtagContent = response.data;
        }).catch(function (response) {
          realThis.hashtagError = response.response.data.detail;
        }).then(function () {
          realThis.loadedHashtag = true;
        });

        // Load word cloud
        let tmpImageUrl = process.env.BASE_API + "/api/wordcloud/" + realThis.selectedDataset;
        const myUrlWithParams = new URL(tmpImageUrl);
        for (let p in pars) {
          myUrlWithParams.searchParams.append(p, pars[p]);
        }

        let myImage = new Image();
        myImage.src = myUrlWithParams.href;
        myImage.onload = () => {
          realThis.imageUrl = myImage.src
          realThis.loadedImage = true;
        }

      });

    }
  },
};
</script>

<style scoped>
h3 {
  margin-top: 30px;
  margin-bottom: 30px;
}

.tag-cloud {
  max-width: 100%;
}
</style>
