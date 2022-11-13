<template lang="pug">
div
  p
    | Hey, I'm <b>KartoffelCheetah</b> :) !
    | Front-end webdev working from Budapest, Hungary.
    | I'm a staunch supporter of software accessibility
    | and an advocate for Open Source solutions.
  p
    | Currently I'm working in the e-commerce field.
    | Linux is my choice of OS both for work and for personal use.
    | I also dabble a bit in 2D art.
  h2.heading3 Contact
  p TODO
  image-resource(name="Circe_by_John_Collier.jpg", alt="circe")
</template>

<script lang="ts">
  import { defineComponent } from 'vue';
  import ImageResource from '../components/ImageResource.vue';
  export default defineComponent({
    name: 'Home',
    components: {
      ImageResource,
    },
  });
</script>
