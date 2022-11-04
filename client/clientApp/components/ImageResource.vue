<template lang="pug">
p {{ width }} x {{ height }}
div.imageResourceContainer
  img.imageResourceImg(v-for="t in thumbnails" :key="t" :src="t", alt="", :width="width")
  img.imageResourceImg.imageResourceMain(:src="src", :alt="alt")
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
        src: '',
        width: 0,
        height: 0,
        thumbnails: [] as string[],
      };
    },
    async mounted () {
      const imageObject = await this.$images[this.name];
      if (imageObject) {
        this.src = this.$serverHost+imageObject.contentUrl;
        this.width = imageObject.width;
        this.height = imageObject.height;
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
      max-width 100%
      max-height 100%
    &Main
      position relative
</style>
