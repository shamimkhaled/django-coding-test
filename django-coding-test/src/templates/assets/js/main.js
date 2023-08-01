window.$ = window.jQuery = require('jquery');
import 'startbootstrap-sb-admin-2/js/sb-admin-2'
import 'select2';
import Vue from 'vue';
import * as $ from 'jquery'

import '../scss/main.scss'

import axios from 'axios';

// Read the CSRF token from the meta tag
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').content;

// Set the CSRF token in the Axios headers for Django
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.headers.common["X-CSRFToken"] = csrfToken;



window.Vue = Vue


Vue.component('create-product', require('./components/product/CreateProduct.vue').default)

const main = new Vue({
    el: '#app'
})




