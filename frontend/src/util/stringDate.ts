const stringDate = (i: string | Date): Date => (typeof i === 'string' ? new Date(i) : i)

export default stringDate
