const powerOfThousand = (value: number, power: number = 0) => {
	if (value >= 1000) {
		return powerOfThousand(value / 1000, power + 1)
	}
	return { value, power }
}

export default powerOfThousand
