import { ref, type Ref } from 'vue'

export type SearchResult = {
	searchInfo: {
		search: string
	}
	search: {
		id: string
		title: string
		pageid: number
		repository: string
		url: string
		concepturi: string
		label: string
		description: string
		match: {
			type: string
			language: string
			text: string
		}
	}[]
	success: number
}

class DataFetcher {
	data: Ref<SearchResult | undefined>
	actionApiUrl: string | null
	loading: Ref<boolean>
	status: Ref<{ code: number; text: string } | undefined>

	constructor(actionApiUrl: string | null) {
		this.actionApiUrl = actionApiUrl
		this.data = ref()
		this.loading = ref(false)
		this.status = ref()
	}

	async getData(searchValue: string): Promise<void> {
		if (this.actionApiUrl && searchValue) {
			const request = new Request(
				`${this.actionApiUrl}?action=wbsearchentities&search=${searchValue}&language=en&format=json&origin=*`,
				{ method: 'GET' }
			)
			this.loading.value = true

			try {
				const response = await fetch(request)
				this.status.value = { code: response.status, text: response.statusText }
				if (this.status.value.code == 200) {
					this.data.value = (await response.json()) as SearchResult
				}
			} catch (error: unknown) {
				this.status.value = { code: 500, text: `${error}` }
			} finally {
				this.loading.value = false
			}
		}
	}
}

export default DataFetcher
