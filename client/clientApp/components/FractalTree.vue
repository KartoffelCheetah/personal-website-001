<template lang="pug">
canvas(
	ref="drawingBoard"
	:width="sizeW",
	:height="sizeH",
)
</template>

<script lang="ts">
	import { defineComponent } from 'vue';

	export default defineComponent({
		name: 'FractalTree',
		props: {
			sizeW: {
				type: Number,
				required: true,
			},
			sizeH: {
				type: Number,
				required: true,
			},
		},
		mounted () {
			const ctx = (this.$refs.drawingBoard as HTMLCanvasElement).getContext('2d') as CanvasRenderingContext2D;
			function draw (startX: number, startY: number, len: number, angle: number): void {
				// Based on: https://lautarolobo.xyz/blog/use-javascript-and-html5-to-code-a-fractal-tree/
				ctx.fillStyle = ctx.strokeStyle = 'wheat';
				ctx.beginPath();
				ctx.save();
				ctx.translate(startX, startY);
				ctx.rotate(angle * Math.PI/180);
				ctx.moveTo(0, 0);
				ctx.lineTo(0, -len);
				ctx.stroke();
				if (len < 10) {
					ctx.restore();
					return;
				}

				for (const i of [-1, +1]) {
					draw(0, -len, len*0.9, i*15);
				}

				ctx.restore();
			}
			draw(this.sizeW/2, this.sizeH - 2, 14, 0);
		},
	});
</script>
