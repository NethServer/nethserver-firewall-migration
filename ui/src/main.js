/*
 * Copyright (C) 2019 Nethesis S.r.l.
 * http://www.nethesis.it - nethserver@nethesis.it
 *
 * This script is part of NethServer.
 *
 * NethServer is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License,
 * or any later version.
 *
 * NethServer is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with NethServer.  If not, see COPYING.
 */

import Vue from 'vue'
import VueI18n from "vue-i18n"
import Router from 'vue-router'
import VueToggleButton from 'vue-js-toggle-button';
import DocInfo from "./directives/DocInfo.vue";

import App from './App.vue'
import Dashboard from './views/Dashboard.vue'
import About from './views/About.vue'
import "./filters/filters"

window.c3 = require('c3');

Vue.config.productionTip = false
Vue.use(VueToggleButton);
Vue.component('doc-info', DocInfo);

Vue.use(VueI18n)
const i18n = new VueI18n();

Vue.use(Router)
const router = new Router({
    mode: 'hash',
    base: process.env.BASE_URL,
    routes: [
      { path: '/', redirect: '/dashboard'},
      { path: '/dashboard', component: Dashboard },
      { path: '/about', name: 'about', component: About },
      { path: "*", redirect: "/" }
    ]
})
router.replace("/dashboard")

var app = new Vue({
    i18n,
    router,
    render: h => h(App)
})

var nethserver = window.nethserver;

nethserver.fetchTranslatedStrings(function (data) {
    i18n.setLocaleMessage('cockpit', data)
    i18n.locale = 'cockpit'
    app.$mount('#app') // Start VueJS application
})
