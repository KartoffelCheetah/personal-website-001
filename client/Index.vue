<template lang="pug">
h1 {{ animals.length }} animal components
hr
ul(:class="$style.index")
  li(v-for="ani in animals", :key="ani.name")
    animal(:animal="ani")
button(v-if="!animals.includes(missingAnimal)", type="button", @click="animals.push(missingAnimal)")
  | Add {{ missingAnimal.name }}
ol(v-else)
  li It's good that we have baby (°)&gt
</template>
<script lang="ts">
  import { defineComponent } from 'vue';
  import Animal, { AnimalType } from './components/Animal.vue';

  export default defineComponent({
    name: 'Index',
    components: { Animal },
    data () {
      fetch('http://localhost:5000/static/routing.json').then(e => {
        console.log('success');
        console.log(e);
      });
      return {
        missingAnimal: {
          name: 'baby chickens',
          image: './640px-Küken_vor_dem_ersten_Ausflug.jpg',
          title: 'HerbertT. Chicks before their first outing',
        } as AnimalType,
        animals: [
          {
            name: 'dog',
            image: './640px-Felis_silvestris_catus_lying_on_rice_straw.jpg',
            title: 'Ch Toveri Arvokas owned by Mrs Joan Bateman. Photo by sannse at the City of Birmingham Championship Dog Show, 29th August 2003',
          },
          {
            name: 'kitten',
            image: './Finnish_Spitz_600.jpg',
            title: 'Basile Morin. Bicolor (cinnamon and white) Felis silvestris catus (domestic cat), with a scratch near the left eye, lying in the sun on rice straw, in Laos',
          },
        ] as AnimalType[],
      };
    },
  });
</script>
<style module>
  .index
    list-style-type none
</style>
