<template lang="pug">
div
	p
		profile-badge(:profile-badge="KCProfileBadge", alt-override="", style="margin-right: 3px;")
		| Hey, I'm <b>KartoffelCheetah</b>, web frontend developer :) !
		br
		| I'm occasionally working on a couple of smaller projects, but most
		| of my time is spent on a supermarket chain's international
		| <em>e-commerce</em> platform (and on the sites running on this
		| platform).
		br
		| My base of operations is in Budapest, Hungary :) .
	p
		| It's worth noting that I'm a staunch supporter of software
		| accessibility and an advocate of Open Source technologies.
		| My choice of OS is Linux both for work and for personal use.
		| I also dabble a bit in 2D art.
	h2.heading3 Contact
	p TODO
	image-resource(name="sunday_sketches_003_001.jpg", alt="TODO")
</template>

<script lang="ts">
	import { defineComponent } from 'vue';
	import ImageResource from '../components/ImageResource.vue';
	import ProfileBadge, { KCProfileBadge } from '../components/ProfileBadge.vue';

	export default defineComponent({
		name: 'Home',
		components: {
			ImageResource,
			ProfileBadge,
		},
		data () {
			return {
				KCProfileBadge,
			};
		},
	});
</script>
