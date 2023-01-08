<template lang="pug">
div
  p
    profile-badge(:profile-badge="KartoffelCheetah", alt-override="", style="margin-right: 3px;")
    | Hey, I'm <b>KartoffelCheetah</b> :) !
    | Front-end webdev working in e-commerce.
    | Base of operations in Budapest, Hungary since 2018.
    | I'm a staunch supporter of software accessibility
    | and an advocate of Open Source.
  p
    | My choice of OS is Linux both for work and for personal use.
    | I also dabble a bit in 2D art.
  h2.heading3 Contact
  p TODO
  image-resource(name="Circe_by_John_Collier.jpg", alt="circe")
</template>

<script lang="ts">
  import { defineComponent } from 'vue';
  import ImageResource from '../components/ImageResource.vue';
  import ProfileBadge, { KartoffelCheetah } from '../components/ProfileBadge.vue';

  export default defineComponent({
    name: 'Home',
    components: {
      ImageResource,
      ProfileBadge,
    },
    data () {
      return {
        KartoffelCheetah,
      };
    },
  });
</script>
