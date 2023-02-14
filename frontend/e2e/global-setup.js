// global-setup.ts
import { chromium, FullConfig } from '@playwright/test'

async function globalSetup(config) {
  const browser = await chromium.launch()
  await new Promise((r) => setTimeout(r, 1000))
  const page = await browser.newPage()
  await new Promise((r) => setTimeout(r, 1000))
  await page.goto('http://localhost:3000/en/-/login/')
  await new Promise((r) => setTimeout(r, 500))
  await page.locator('[data-test="signin-username"]').fill('test1-user@test.com')
  await new Promise((r) => setTimeout(r, 500))
  await page.locator('[data-test="signin-password"]').fill('testpassword')
  await new Promise((r) => setTimeout(r, 500))
  await page.locator('[data-test="signin-submit"]').click()
  await new Promise((r) => setTimeout(r, 500))
  // Save signed-in state to 'storageState.json'.
  await page.context().storageState({ path: 'storageState.json' })
  await browser.close()
}

export default globalSetup
