export type TimeDelta = {
	days: number
	hours: number
	minutes: number
	seconds: number
	milliseconds: number
}

export const isNegative = (t: TimeDelta) =>
	t.days < 0 || t.hours < 0 || t.minutes < 0 || t.seconds < 0 || t.milliseconds < 0

const MILLISECONDS_PER_SECOND = 1000
const SECONDS_PER_MINUTE = 60
const MINUTES_PER_HOUR = 60
const HOURS_PER_DAY = 24

const computeTimedelta = (msdelta: number): TimeDelta => {
	const milliseconds = msdelta % MILLISECONDS_PER_SECOND
	const seconds = Math.floor(msdelta / MILLISECONDS_PER_SECOND) % SECONDS_PER_MINUTE
	const minutes =
		Math.floor(msdelta / (MILLISECONDS_PER_SECOND * SECONDS_PER_MINUTE)) % MINUTES_PER_HOUR
	const hours =
		Math.floor(msdelta / (MILLISECONDS_PER_SECOND * SECONDS_PER_MINUTE * MINUTES_PER_HOUR)) %
		HOURS_PER_DAY
	const days = Math.floor(
		msdelta / (MILLISECONDS_PER_SECOND * SECONDS_PER_MINUTE * MINUTES_PER_HOUR * HOURS_PER_DAY)
	)
	return { days, hours, minutes, seconds, milliseconds }
}

export default computeTimedelta
