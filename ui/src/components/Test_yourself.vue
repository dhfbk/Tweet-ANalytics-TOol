<template>
  <div>
    <div class="container bigcontainer">
      <!--in base a come sono i testi convertire con v-for-->
      <h1 class="title">2. Challenge yourself</h1>
      <div class="containersubtitle ps-3">
        <p class="subtitle">
          Challenge yourself with our simple quizzes that will help you make your internet experience safer.
        </p>
      </div>

      <div v-for="(question, index) in questions" :key="index">
        <h2>{{ question['q'] }}</h2>
        <ul class="list-group pb-5">
          <li class="list-group-item"
              :class="{'list-group-item-success': question['a'][qIndex]['right'], 'list-group-item-danger': question['a'][qIndex]['wrong']}"
              v-for="(answer, qIndex) in question['a']" :key="qIndex">
            <a class="me-2" href="#" @click.prevent="setAnswer(index, qIndex, true)">
                            <span class="badge rounded-pill"
                                  :class="{'bg-secondary': !question['a'][qIndex]['yes'], 'bg-dark': question['a'][qIndex]['yes']}"
                            >Yes</span>
            </a>
            <a class="me-2" href="#" @click.prevent="setAnswer(index, qIndex, false)">
                            <span class="badge rounded-pill"
                                  :class="{'bg-secondary': !question['a'][qIndex]['no'], 'bg-dark': question['a'][qIndex]['no']}"
                            >No</span>
            </a>
            {{ answer["t"] }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const temp = array[i];
    array[i] = array[j];
    array[j] = temp;
  }
  return array;
}

export default {
  data: function () {
    return {
      questions: []
    }
  },
  methods: {
    setAnswer(index, qIndex, value) {
      let correct = this.questions[index]['a'][qIndex]['c'];
      this.questions[index]['a'][qIndex]['yes'] = value;
      this.questions[index]['a'][qIndex]['no'] = !value;
      if (correct === value) {
        this.questions[index]['a'][qIndex]['right'] = true;
        this.questions[index]['a'][qIndex]['wrong'] = false;
      } else {
        this.questions[index]['a'][qIndex]['right'] = false;
        this.questions[index]['a'][qIndex]['wrong'] = true;
      }
    }
  },
  mounted() {
    let realThis = this;
    realThis.questions = [];
    axios.get(process.env.BASE_API + "/static/questions2.json").then(function (response) {
      let q = response.data;
      for (let question of q) {
        question['a'] = shuffleArray(question['a']);
        for (let answer of question['a']) {
          answer['right'] = false;
          answer['wrong'] = false;
          answer['yes'] = false;
          answer['no'] = false;
        }
        realThis.questions.push(question);
      }
    })
  }
};
</script>

<style src="../style.css"></style>
