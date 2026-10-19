export function getUrlParamValue<T>(paramName: string): T {
	const queryString = window.location.search
	const urlParams = new URLSearchParams(queryString)
	return urlParams.get(paramName) as T
}

export function updateUrlParamValue(paramName: string, v: string | null | undefined) {
	const searchURL = new URL(window.location.toString())
	if (v) {
		searchURL.searchParams.set(paramName, v)
	} else {
		searchURL.searchParams.delete(paramName)
	}
	window.history.pushState({}, '', searchURL)
}
