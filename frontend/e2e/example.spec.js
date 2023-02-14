// @ts-check
import { test, expect } from '@playwright/test'

test('has title', async ({ page }) => {
  await page.goto('http://localhost:3000/en/-/')

  // Expect a title "to contain" a substring.
  await expect(page.getByText('Welcome test1')).toBeVisible()
})

test('get started link', async ({ page }) => {
  await page.goto('http://localhost:3000/en/-/')

  // Click the get started link.
  await page.getByRole('link', { name: 'Inventory' }).click()

  // Expects the URL to contain intro.
  await expect(page).toHaveURL(/.*inventory\/list/)
})
