"use strict";

import { createApp, ref } from '/static/libraries/vue.js'
// import the root component App from a single-file component.
import App from '/components/app.vue'

createApp({
    setup() {
      // component logic
      // declare some reactive state here.
  
      return {
        // exposed to template
      }
    }
  }).mount('#app')