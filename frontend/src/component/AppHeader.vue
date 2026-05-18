<script setup lang="ts">
import img from '@/media/icon/wikibase_symbol_RGB.png'
import { mdiThemeLightDark } from '@mdi/js'
import { useTheme } from 'vuetify'

const theme = useTheme()
</script>

<template>
	<v-container class="ma-0 pa-0 header-container">
		<v-container class="px-6 py-4 header">
			<v-container class="ma-0 pa-0 left-header shrink">
				<v-container class="ma-0 pa-0 icon shrink"><v-img :src="img" eager /></v-container>
				<v-container class="ma-0 pa-0 title-container shrink">
					<v-container class="ma-0 pa-0 title shrink">Wikibase Ecosystem</v-container>
					<v-container class="ma-0 pa-0 subtitle shrink">
						Discover stable Wikibases around the world
					</v-container>
				</v-container>
			</v-container>
			<v-container class="ma-0 pa-0 right-header shrink">
				<v-btn
					v-if="false"
					class="theme-switch"
					v-on:click="theme.toggle()"
					density="comfortable"
					:icon="mdiThemeLightDark"
				/>
			</v-container>
		</v-container>
	</v-container>
</template>

<style lang="css">
.header-container {
	max-width: 100%;
	width: 100%;
	outline-color: oklch(0.708 0 0);
	background-color: white;
	border-bottom: 1px solid oklch(92.8% 0.006 264.531);
}
.header {
	display: flex;
	flex-flow: row wrap;
	align-items: center;
	justify-content: space-between;
}
.left-header {
	display: flex;
	flex-flow: row wrap;
	gap: 8px;
	align-items: center;
}
.right-header {
	display: flex;
	flex-flow: row wrap;
	gap: 8px;
	align-items: center;
}
.shrink {
	width: auto;
}
.icon .v-img {
	width: 96px;
}
.title-container {
	flex-grow: 1;
}
.title {
	font-size: 20px;
	font-weight: 700;
	font-family: Montserrat;
}
.subtitle {
	font-size: 16px;
	font-family: Roboto;
}
</style>
