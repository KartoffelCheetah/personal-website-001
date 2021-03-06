<template lang="pug">
div(:class="$style.animal")
  img(:src="animal.image", :alt="animal.title", width="200")
  h2 {{ animal.name }}
</template>

<script lang="ts">
  export type AnimalType = {
    name: string;
    image: string;
    title: string;
  };

  export default {
    name: 'Animal',
    props: {
      animal: {
        type: Object as () => AnimalType,
      },
    },
  };
</script>

<style module>
  .animal
    display flex
    align-items center
    gap 1em
    border 2px solid aquamarine
    background grey
</style>
