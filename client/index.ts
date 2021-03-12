import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import routes from './routes.ts';
import Index from './Index.vue';

(async function () {
  const resp = await (await fetch('http://localhost:5000/static/routing.json')).json();
  console.log(resp);
})();

createApp(Index)
  .use(createRouter({
    history: createWebHistory(),
    routes,
  }))
  .mount('#index')
;
