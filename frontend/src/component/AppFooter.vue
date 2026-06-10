<script setup lang="ts">
import img from '@/media/icon/wikibase_symbol_RGB.png'
import { mdiThemeLightDark } from '@mdi/js'
import { useTheme } from 'vuetify'

const theme = useTheme()
</script>

<template>
	<v-container id="app-footer" class="py-6">
        <a class="footer-link" href="https://www.wikimedia.de/impressum/">Imprint</a>
        <a class="footer-link" href="https://www.wikimedia.de/datenschutz/#dataprivacy">Data Protection</a>
	</v-container>
</template>

<style lang="scss">
    #app-footer {
        display: flex;
        justify-content: center;
        gap: 32px;
    }

    .footer-link {
        text-decoration: none;
    }
</style>
