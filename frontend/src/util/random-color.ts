const HEX = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

const randomHex = () => {
	const value = Math.floor(Math.random() * 256)
	const firstDigit = Math.floor(value / 16)
	const secondDigit = value % 16
	return `${HEX[firstDigit]}${HEX[secondDigit]}`
}

const randomColor = () => `#${randomHex()}${randomHex()}${randomHex()}`

export default randomColor
