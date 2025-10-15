export function compareByValue<T>(
	a: T,
	b: T,
	value: (v: T) => string | number | null | undefined
): -1 | 0 | 1 {
	const valA = value(a)
	const valB = value(b)
	if (valA == null || valA == undefined) {
		return valB == null || valB == undefined ? 0 : -1
	}
	if (valB == null || valB == undefined) {
		return 1
	}
	return valA > valB ? 1 : valA < valB ? -1 : 0
}

function sortByValue<T>(items: T[], value: (a: T) => string | number | undefined) {
	return items.sort((a, b) => compareByValue(a, b, value))
}

export default sortByValue
