import type { Point } from 'chart.js'

function onlyUnique(value: Point, index: number, array: Array<Point>): boolean {
	let firstIdx: number | null = null
	array.forEach((v, idx) => {
		if (firstIdx == null) {
			if (v.x == value.x && v.y == value.y) {
				firstIdx = idx
			}
		}
	})

	return firstIdx === index
}

export default onlyUnique
