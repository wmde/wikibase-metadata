import PaginationFooter from '@/component/wikibase-table/PaginationFooter.vue'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick } from 'vue'

const mockSetPageNumber = vi.fn().mockName('setPageNumber')
const mockSetPageSize = vi.fn().mockName('setPageSize')

describe('PaginationFooter', async () => {
	beforeEach(() => vi.resetAllMocks())

	it('renders properly', async () => {
		const wrapper = mount(PaginationFooter, {
			global: { plugins: [vuetify] },
			props: {
				pageNumber: 1,
				pageSize: 25,
				totalCount: 100,
				totalPages: 4,
				setPageNumber: mockSetPageNumber,
				setPageSize: mockSetPageSize
			}
		})

		const container = wrapper.find('.pagination-container')
		expect(container.exists()).toEqual(true)

		const pageContainer = container.find('.pagination-row-container')
		expect(pageContainer.exists()).toEqual(true)

		const countContainer = pageContainer.find('.item-number-container')
		expect(countContainer.exists()).toEqual(true)
		expect(countContainer.text()).toEqual('1–25 of 100')

		const buttonContainer = pageContainer.find('.button-container')
		expect(buttonContainer.exists()).toEqual(true)
		expect(buttonContainer.findAll('.v-btn')).toHaveLength(4)
		buttonContainer
			.findAll('.v-btn')
			.forEach((button) => expect(button.find('i.v-icon').exists()).toEqual(true))

		const pageSizeContainer = container.find('.page-size-container')
		expect(pageSizeContainer.exists()).toEqual(true)

		const label = pageSizeContainer.find('.page-size-label')
		expect(label.exists()).toEqual(true)
		expect(label.text()).toEqual('Items per page:')

		const select = pageSizeContainer.find('.v-select')
		expect(select.exists()).toEqual(true)
	})

	it('has back and first disabled on first page', async () => {
		const wrapper = mount(PaginationFooter, {
			global: { plugins: [vuetify] },
			props: {
				pageNumber: 1,
				pageSize: 25,
				totalCount: 100,
				totalPages: 4,
				setPageNumber: mockSetPageNumber,
				setPageSize: mockSetPageSize
			}
		})

		const container = wrapper.find('.pagination-container')
		expect(container.exists()).toEqual(true)

		const pageContainer = container.find('.pagination-row-container')
		expect(pageContainer.exists()).toEqual(true)

		const buttonContainer = pageContainer.find('.button-container')
		expect(buttonContainer.exists()).toEqual(true)
		expect(buttonContainer.findAll('.v-btn')).toHaveLength(4)
		buttonContainer
			.findAll('.v-btn')
			.forEach((button) => expect(button.find('i.v-icon').exists()).toEqual(true))

		expect(buttonContainer.findAll('.v-btn')[0]?.classes()).toContain('v-btn--disabled')
		expect(buttonContainer.findAll('.v-btn')[1]?.classes()).toContain('v-btn--disabled')
		expect(buttonContainer.findAll('.v-btn')[2]?.classes()).not.toContain('v-btn--disabled')
		expect(buttonContainer.findAll('.v-btn')[3]?.classes()).not.toContain('v-btn--disabled')
	})

	it('has next and last disabled on last page', async () => {
		const wrapper = mount(PaginationFooter, {
			global: { plugins: [vuetify] },
			props: {
				pageNumber: 4,
				pageSize: 25,
				totalCount: 100,
				totalPages: 4,
				setPageNumber: mockSetPageNumber,
				setPageSize: mockSetPageSize
			}
		})

		const container = wrapper.find('.pagination-container')
		expect(container.exists()).toEqual(true)

		const pageContainer = container.find('.pagination-row-container')
		expect(pageContainer.exists()).toEqual(true)

		const buttonContainer = pageContainer.find('.button-container')
		expect(buttonContainer.exists()).toEqual(true)
		expect(buttonContainer.findAll('.v-btn')).toHaveLength(4)
		buttonContainer
			.findAll('.v-btn')
			.forEach((button) => expect(button.find('i.v-icon').exists()).toEqual(true))

		expect(buttonContainer.findAll('.v-btn')[0]?.classes()).not.toContain('v-btn--disabled')
		expect(buttonContainer.findAll('.v-btn')[1]?.classes()).not.toContain('v-btn--disabled')
		expect(buttonContainer.findAll('.v-btn')[2]?.classes()).toContain('v-btn--disabled')
		expect(buttonContainer.findAll('.v-btn')[3]?.classes()).toContain('v-btn--disabled')
	})

	it('calls set page on first page', async () => {
		const wrapper = mount(PaginationFooter, {
			global: { plugins: [vuetify] },
			props: {
				pageNumber: 3,
				pageSize: 25,
				totalCount: 101,
				totalPages: 5,
				setPageNumber: mockSetPageNumber,
				setPageSize: mockSetPageSize
			}
		})

		const container = wrapper.find('.pagination-container')
		expect(container.exists()).toEqual(true)

		const pageContainer = container.find('.pagination-row-container')
		expect(pageContainer.exists()).toEqual(true)

		const buttonContainer = pageContainer.find('.button-container')
		expect(buttonContainer.exists()).toEqual(true)
		expect(buttonContainer.findAll('.v-btn')).toHaveLength(4)
		buttonContainer
			.findAll('.v-btn')
			.forEach((button) => expect(button.find('i.v-icon').exists()).toEqual(true))

		expect(mockSetPageNumber).toHaveBeenCalledTimes(0)

		await buttonContainer.findAll('.v-btn')[0]?.trigger('click')
		await nextTick()

		expect(mockSetPageNumber).toHaveBeenCalledWith(1)
	})

	it('calls set page on prev page', async () => {
		const wrapper = mount(PaginationFooter, {
			global: { plugins: [vuetify] },
			props: {
				pageNumber: 3,
				pageSize: 25,
				totalCount: 101,
				totalPages: 5,
				setPageNumber: mockSetPageNumber,
				setPageSize: mockSetPageSize
			}
		})

		const container = wrapper.find('.pagination-container')
		expect(container.exists()).toEqual(true)

		const pageContainer = container.find('.pagination-row-container')
		expect(pageContainer.exists()).toEqual(true)

		const buttonContainer = pageContainer.find('.button-container')
		expect(buttonContainer.exists()).toEqual(true)
		expect(buttonContainer.findAll('.v-btn')).toHaveLength(4)
		buttonContainer
			.findAll('.v-btn')
			.forEach((button) => expect(button.find('i.v-icon').exists()).toEqual(true))

		expect(mockSetPageNumber).toHaveBeenCalledTimes(0)

		await buttonContainer.findAll('.v-btn')[1]?.trigger('click')
		await nextTick()

		expect(mockSetPageNumber).toHaveBeenCalledWith(2)
	})

	it('calls set page on next page', async () => {
		const wrapper = mount(PaginationFooter, {
			global: { plugins: [vuetify] },
			props: {
				pageNumber: 3,
				pageSize: 25,
				totalCount: 101,
				totalPages: 5,
				setPageNumber: mockSetPageNumber,
				setPageSize: mockSetPageSize
			}
		})

		const container = wrapper.find('.pagination-container')
		expect(container.exists()).toEqual(true)

		const pageContainer = container.find('.pagination-row-container')
		expect(pageContainer.exists()).toEqual(true)

		const buttonContainer = pageContainer.find('.button-container')
		expect(buttonContainer.exists()).toEqual(true)
		expect(buttonContainer.findAll('.v-btn')).toHaveLength(4)
		buttonContainer
			.findAll('.v-btn')
			.forEach((button) => expect(button.find('i.v-icon').exists()).toEqual(true))

		expect(mockSetPageNumber).toHaveBeenCalledTimes(0)

		await buttonContainer.findAll('.v-btn')[2]?.trigger('click')
		await nextTick()

		expect(mockSetPageNumber).toHaveBeenCalledWith(4)
	})

	it('calls set page on last page', async () => {
		const wrapper = mount(PaginationFooter, {
			global: { plugins: [vuetify] },
			props: {
				pageNumber: 3,
				pageSize: 25,
				totalCount: 101,
				totalPages: 5,
				setPageNumber: mockSetPageNumber,
				setPageSize: mockSetPageSize
			}
		})

		const container = wrapper.find('.pagination-container')
		expect(container.exists()).toEqual(true)

		const pageContainer = container.find('.pagination-row-container')
		expect(pageContainer.exists()).toEqual(true)

		const buttonContainer = pageContainer.find('.button-container')
		expect(buttonContainer.exists()).toEqual(true)
		expect(buttonContainer.findAll('.v-btn')).toHaveLength(4)
		buttonContainer
			.findAll('.v-btn')
			.forEach((button) => expect(button.find('i.v-icon').exists()).toEqual(true))

		expect(mockSetPageNumber).toHaveBeenCalledTimes(0)

		await buttonContainer.findAll('.v-btn')[3]?.trigger('click')
		await nextTick()

		expect(mockSetPageNumber).toHaveBeenCalledWith(5)
	})
})
