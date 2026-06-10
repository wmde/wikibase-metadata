function getActionApiUrl(baseUrl: string, scriptPath: string | null | undefined): string | null {
	if (scriptPath === null || scriptPath === undefined) {
		return null
	}

	const base = baseUrl.replace(/\/+$/, '')
	// remove extra leading and trailing slashes
	const stripped = scriptPath.trim().replace(/^\/|\/$/g, '')
	const s = stripped ? `/${stripped}/` : '/'
	return `${base}${s}api.php`
}

export default getActionApiUrl
