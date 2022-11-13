import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import routes from './routes.ts';
import restApi from './plugins/restApi';
import Index from './Index.vue';

createApp(Index)
  .use(createRouter({
    history: createWebHistory(),
    routes,
  }))
  .use(restApi, 'http://localhost:5000')
  .mount('#index')
;
