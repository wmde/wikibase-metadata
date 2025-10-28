function uniqueValues<T>(values: T[], uniqueId: (v: T) => string | number): T[] {
	return values.filter(
		(value, i, array) =>
			!array
				.slice(i + 1)
				.map((v) => uniqueId(v))
				.includes(uniqueId(value))
	)
}

export default uniqueValues
