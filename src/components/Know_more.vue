<template>
  <div>
    <div class="container bigcontainer">
      <!--in base a come sono i testi convertire con v-for-->
      <div>
        <h1 class="title">1. Learn more</h1>
        <div class="containersubtitle ps-3">
          <p class="subtitle">
            In this section you will find some general information on social media.
          </p>
        </div>
      </div>

      <div class="accordion pb-5" id="accordionExample">

        <div v-for="(question, index) in questions" class="accordion-item" :key="index">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                    :data-bs-target="'#collapse' + index" aria-expanded="true" :aria-controls="'collapse' + index">
              {{ index + 1 }}. {{ question["q"] }}
            </button>
          </h2>
          <div :id="'collapse' + index" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
            <div class="accordion-body" v-html="question['r']">
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data: function () {
    return {
      questions: []
    }
  },
  mounted() {
    let realThis = this;
    axios.get(process.env.BASE_API + "/static/questions1.json").then(function (response) {
      realThis.questions = response.data;
    })
  }
};
</script>

<style src="../style.css"></style>
