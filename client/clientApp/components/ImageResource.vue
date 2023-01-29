<template lang="pug">
div.imageResourceContainer(
		:style="{ paddingTop }",
	)
	img.imageResourceImg(
		v-for="t in thumbnails",
		:key="t.contentUrl"
		:src="t.contentUrl",
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
	import { ImageObject } from '../plugins/restApi/imageProxy.ts';

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
				thumbnails: [] as ImageObject[],
			};
		},
		async mounted () {
			const imageObject = await this.$images[this.name];
			// TODO add a prop to allow the download of specific `thid`s.
			if (imageObject) {
				this.src = imageObject.contentUrl;
				this.paddingTop = `${imageObject.height / imageObject.width * 100}%`;
				this.thumbnails = imageObject.thumbnail;
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
