<template lang="pug">
div
  p I'm a front-end developer.
    | adgnafg dhguifgfigiof experience as a programmer.
    | I enjoy programming in JavaScript and Python3, designing websites and doing 2D art.
    | Whenever possible I use open-source software on Linux. 🐧
  br
  image-resource(name="Circe_by_John_Collier.jpg", alt="circe")
  image-resource(name="Flamber-Bougault.jpg", alt="old ship")
  image-resource(name="Alma_Tadema_Spring.jpg", alt="high res classsical painting")
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
