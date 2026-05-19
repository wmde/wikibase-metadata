<script setup lang="ts">
defineProps<{ label: string; entities: number; entityDate: Date }>()
</script>

<template>
	<v-container class="ma-0 milestone">
		<v-container class="ma-0 pa-0 shrink milestone-label">
			<v-container class="ma-0 pa-0 shrink milestone-q">{{ label }}</v-container>
			<v-container class="ma-0 pa-0 shrink milestone-count">
				{{ entities }} {{ entities == 1 ? 'entity' : 'entities' }}
			</v-container>
		</v-container>
		<v-container class="ma-0 pa-0 shrink milestone-date">
			{{ entityDate.toLocaleDateString('de') }}
			{{ entityDate.toLocaleTimeString('de') }}
		</v-container>
	</v-container>
</template>

<style lang="css">
.milestone {
	display: flex;
	flex-flow: row nowrap;
	justify-content: space-between;
	align-items: center;
	gap: 0.25rem;
	background-color: oklch(98.5% 0.002 247.839);
	border: 1px solid oklch(92.8% 0.006 264.531);
	border-radius: 0.25rem;
}
.milestone-q {
	font-family: Roboto;
	font-size: 16px;
	color: rgb(0, 0, 0);
	font-weight: 500;
}
.milestone-count {
	font-family: Roboto;
	font-size: 14px;
	color: rgb(102, 102, 102);
}
.milestone-date {
	font-family: Roboto;
	font-size: 16px;
	color: rgb(0, 0, 0);
	text-align: right;
}
</style>
