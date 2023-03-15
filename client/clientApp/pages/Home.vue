<template lang="pug">
div.kcAutoHyphens
	p.kcParagraph
		profile-badge(:profile-badge="KCProfileBadge", alt-override="", style="margin-right: 3px;")
		| Hey, I'm <strong>KartoffelCheetah</strong>, front-end web developer :) !
		br
		| Welcome to my Lair!
	h2.kcHeading3 About me
	p.kcParagraph
		strong I start with a few words concerning my work as an FE dev.
		br
		| My base of operations is in Budapest, Hungary.
		br
		| Most of my work consists of the development of a supermarket chain's international
		| <em>e-commerce</em> &#43; administrative platforms. It involves maintaining
		| and developing the different sites running on the framework.
		| Between 2018-2021 I worked as the sole FE developer of the
		| project and since then as part of a team of (very cool) FE developers.
	p.kcParagraph
		| I&apos;m a staunch supporter of software accessibility,
		| an advocate of Open Source technologies&#47;art&#47;etc.
		| My choice of OS is Linux 🐧 both for work and personal use.
		| Lastly, I also dabble a bit in 2D art.
	h2.kcHeading3 Contact
	p.kcParagraph TODO
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
