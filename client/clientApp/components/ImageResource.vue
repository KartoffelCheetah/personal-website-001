<template lang="pug">
div.imageResourceContainer(
    :style="{ paddingTop }",
  )
  img.imageResourceImg(
    v-for="t in thumbnails",
    :key="t"
    :src="t",
    alt="",
    aria-hidden="true",
  )
  img.imageResourceImg(
    :src="src",
    :alt="alt",
    loading="lazy",
  )
</template>

<script lang="ts">
  import { defineComponent } from 'vue';

  export default defineComponent({
    name: 'ImageResource',
    props: {
      name: {
        type: String,
        required: true,
      },
      alt: {
        type: String,
        required: true,
      },
    },
    data () {
      return {
        paddingTop: '0',
        src: '',
        thumbnails: [] as string[],
      };
    },
    async mounted () {
      const imageObject = await this.$images[this.name];
      if (imageObject) {
        this.src = this.$serverHost+imageObject.contentUrl;
        this.paddingTop = `${imageObject.height / imageObject.width * 100}%`;
        this.thumbnails = imageObject.thumbnailUrl.map(t => this.$serverHost+t);
      }
    },
  });
</script>

<style>
  .imageResource
    &Container
      position relative
    &Img
      position absolute
      top 0
      width: 100%;
      max-width 100%
      max-height 100%
</style>
