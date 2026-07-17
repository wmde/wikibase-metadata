import type { Point } from 'chart.js'

const sortByX = (a: Point, b: Point) =>
	a.x == null && b.x == null
		? 0
		: a.x == null
			? -1
			: b.x == null
				? 1
				: a.x > b.x
					? 1
					: a.x < b.x
						? -1
						: 0

export default sortByX
