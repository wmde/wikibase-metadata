export function getUrlParamValue<T>(paramName: string): T {
	const queryString = window.location.search
	const urlParams = new URLSearchParams(queryString)
	return urlParams.get(paramName) as T
}

export function updateUrlParamValue(paramName: string, v: string) {
	const searchURL = new URL(window.location.toString())
	searchURL.searchParams.set(paramName, v)
	window.history.pushState({}, '', searchURL)
}
