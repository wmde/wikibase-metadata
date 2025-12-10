<script setup lang="ts">
import img from '@/media/icon/wikibase_symbol_RGB_cropped.png'
import routes, { currentPath } from '@/routes'
import { mdiGithub, mdiThemeLightDark } from '@mdi/js'
import { useTheme } from 'vuetify'

const theme = useTheme()
</script>

<template>
	<v-container class="pa-1 header">
		<v-container class="ma-0 pa-0 left-header shrink">
			<v-container class="ma-0 pa-0 icon shrink"><v-img :src="img" eager /></v-container>
			<v-container class="ma-0 pa-0 title shrink">Wikibase Ecosystem</v-container>
		</v-container>
		<v-container class="ma-0 pa-0 right-header shrink">
			<v-btn
				class="github"
				href="https://github.com/wmde/wikibase-metadata"
				density="comfortable"
				:icon="mdiGithub"
			/>
			<v-btn
				class="theme-switch"
				v-on:click="theme.toggle()"
				density="comfortable"
				:icon="mdiThemeLightDark"
			/>
		</v-container>
	</v-container>
	<v-container class="link-container">
		<template v-for="route in Object.keys(routes)" :key="route">
			<v-btn
				v-if="routes[route]"
				:variant="currentPath == route ? 'outlined' : 'tonal'"
				density="compact"
				:href="route"
			>
				{{ routes[route].name }}
			</v-btn>
		</template>
	</v-container>
</template>

<style lang="css">
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
	height: 50px;
	width: 50px;
}
.title {
	flex-grow: 1;
}
.link-container {
	display: flex;
	flex-flow: row wrap;
	gap: 6px;

}
</style>
