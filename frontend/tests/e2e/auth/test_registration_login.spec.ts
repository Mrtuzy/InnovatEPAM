import { test, expect } from '@playwright/test';

test('registers a new user and logs in', async ({ page }) => {
  const timestamp = Date.now();
  const user = {
    email: `e2e-${timestamp}@example.com`,
    password: 'TestPassword123!',
    fullName: 'E2E Test User',
  };

  await page.goto('/register');

  await page.getByLabel('Email').fill(user.email);
  await page.getByLabel('Full Name').fill(user.fullName);
  await page.getByLabel('Password').fill(user.password);
  await page.getByRole('button', { name: /register/i }).click();

  await page.waitForURL('**/dashboard', { timeout: 10000 });
  await expect(page.getByText(user.email)).toBeVisible();

  await page.getByRole('button', { name: /logout/i }).click();
  await page.waitForURL('**/login', { timeout: 10000 });

  await page.getByLabel('Email').fill(user.email);
  await page.getByLabel('Password').fill(user.password);
  await page.getByRole('button', { name: /sign in/i }).click();

  await page.waitForURL('**/dashboard', { timeout: 10000 });
  await expect(page.getByText(user.fullName)).toBeVisible();
});
