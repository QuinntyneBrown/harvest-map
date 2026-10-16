import { expect, test, type Page } from "@playwright/test";
import { FakeApi } from "./support/fakeApi";
import { OrganizationFormPage } from "./pages/OrganizationFormPage";
import { ToastRegion } from "./pages/ToastRegion";
import { UnsavedChangesDialog } from "./pages/UnsavedChangesDialog";
import { faithtechDetail } from "./fixtures/organizations";

async function openEdit(page: Page) {
  const api = new FakeApi(page);
  await api.on("GET", "/api/organizations/o1", { body: faithtechDetail });
  const form = new OrganizationFormPage(page);
  await form.openEdit();
  await expect(form.name).toHaveValue("FaithTech");
  return { api, form };
}

test.describe("L2-008 Create and edit organization", () => {
  test("AC1: the form is prefilled and says when and by whom it was last saved", async ({ page }) => {
    const { form } = await openEdit(page);
    await expect(form.heading).toHaveText("Edit organization");
    await expect(form.subtitle).toHaveText("FaithTech · last saved Tue 14 Oct by Tobias Mwangi");
    await expect(form.type).toHaveValue("Community");
    await expect(form.founded).toHaveValue("2016");
    await expect(form.city).toHaveValue("Waterloo");
    await expect(form.country).toHaveValue("Canada");
    await expect(form.website).toHaveValue("faithtech.com");
    await expect(form.summary).toHaveValue(faithtechDetail.summary);
    await expect(form.tag("AI")).toBeChecked();
    await expect(form.tag("Moonshot")).not.toBeChecked();
  });

  test("AC1: a skeleton shows while loading and a failure offers Try again", async ({ page }) => {
    const api = new FakeApi(page);
    let recovered = false;
    await api.on("GET", "/api/organizations/o1", () => (recovered ? { body: faithtechDetail } : { status: 500 }));
    const form = new OrganizationFormPage(page);
    await form.openEdit();
    await expect(form.loadError).toBeVisible();
    recovered = true;
    await form.tryAgain.click();
    await expect(form.name).toHaveValue("FaithTech");
  });

  test("AC1: skeleton while the form loads", async ({ page }) => {
    const api = new FakeApi(page);
    await api.hang("GET", "/api/organizations/o1");
    const form = new OrganizationFormPage(page);
    await form.openEdit();
    await expect(form.skeleton).toBeVisible();
  });

  test("AC2: an empty name and a bad website stop at the error summary", async ({ page }) => {
    // Given an empty Name and a Website that is not a domain
    const { api, form } = await openEdit(page);
    await form.name.fill("");
    await form.website.fill("not a site");
    // When the user saves
    await form.save.click();
    // Then the summary lists both, each field shows its message and focus is on the summary
    await expect(form.errorSummary).toContainText("Fix 2 things to save");
    await expect(form.summaryItem("Enter a name")).toBeVisible();
    await expect(form.summaryItem("Enter a website like example.org")).toBeVisible();
    await expect(form.fieldError("org-name")).toHaveText("Enter a name");
    await expect(form.fieldError("org-site")).toHaveText("Enter a website like example.org");
    await expect(form.errorSummary).toBeFocused();
    expect(api.sent("POST", "/api/organizations/o1")).toHaveLength(0);
    // And selecting a summary item focuses its field
    await form.summaryItem("Enter a name").click();
    await expect(form.name).toBeFocused();
  });

  test("AC3: a valid save is busy, ignores a second submit, saves and returns to the organization", async ({ page }) => {
    // Given valid values and a slow server
    const { api, form } = await openEdit(page);
    await api.on("POST", "/api/organizations/o1", { delayMs: 600, body: { ok: true, id: "o1" } });
    await form.summary.fill("A global community of Christian technologists.");
    await form.tag("Moonshot").check();
    // When the user saves twice
    await form.save.click();
    await expect(form.save).toHaveAttribute("aria-busy", "true");
    await form.save.click({ force: true });
    // Then a toast confirms, the organization page opens and one request went out, with the values
    await expect(new ToastRegion(page).toast("FaithTech saved")).toBeVisible();
    await expect(page).toHaveURL(/\/organizations\/o1$/);
    expect(api.sent("POST", "/api/organizations/o1")).toHaveLength(1);
    expect(api.sent("POST", "/api/organizations/o1")[0].body).toMatchObject({
      name: "FaithTech",
      type: "Community",
      founded: "2016",
      city: "Waterloo",
      country: "Canada",
      website: "faithtech.com",
      summary: "A global community of Christian technologists.",
      tags: ["AI", "Youth", "Moonshot", "Community"],
    });
  });

  test("AC4: a failed save shows an alert, keeps the entries and can be retried", async ({ page }) => {
    // Given the save fails once
    const { api, form } = await openEdit(page);
    let recovered = false;
    await api.on("POST", "/api/organizations/o1", () => (recovered ? { body: { ok: true, id: "o1" } } : { status: 500 }));
    await form.summary.fill("Changed text");
    // When the user saves
    await form.save.click();
    // Then the alert shows and the entries are kept
    await expect(form.failedAlert).toContainText("Couldn't save");
    await expect(form.summary).toHaveValue("Changed text");
    await expect(form.save).toBeEnabled();
    // And Save retries
    recovered = true;
    await form.save.click();
    await expect(page).toHaveURL(/\/organizations\/o1$/);
  });

  test("AC5: Cancel with changes lists them in the discard dialog; Keep editing stays, Discard leaves", async ({ page }) => {
    // Given changed fields
    const { api, form } = await openEdit(page);
    await api.on("GET", "/api/organizations/o1", { body: faithtechDetail });
    await form.summary.fill("New summary");
    await form.tag("Moonshot").check();
    // When the user selects Cancel
    await form.cancel.click();
    // Then the dialog lists the changed fields
    const dialog = new UnsavedChangesDialog(page, "FaithTech");
    await expect(dialog.root).toBeVisible();
    await expect(dialog.description).toHaveText("2 fields changed: Summary, Tags.");
    await expect(dialog.keepEditing).toBeFocused();
    // And Keep editing returns to the form with the changes
    await dialog.keepEditing.click();
    await expect(dialog.root).toBeHidden();
    await expect(form.summary).toHaveValue("New summary");
    // And Discard leaves the form
    await form.cancel.click();
    await dialog.discard.click();
    await expect(page).toHaveURL(/\/organizations\/o1$/);
  });

  test("AC5: browser back with changes asks before leaving", async ({ page }) => {
    const { api, form } = await openEdit(page);
    await api.on("GET", "/api/organizations/o1", { body: faithtechDetail });
    await form.summary.fill("New summary");
    await page.goBack();
    await expect(new UnsavedChangesDialog(page, "FaithTech").root).toBeVisible();
  });

  test("AC5: Cancel without changes leaves at once", async ({ page }) => {
    const { api, form } = await openEdit(page);
    await api.on("GET", "/api/organizations/o1", { body: faithtechDetail });
    await form.cancel.click();
    await expect(page).toHaveURL(/\/organizations\/o1$/);
  });

  test("AC6: the Summary field grows with its text", async ({ page }) => {
    const { form } = await openEdit(page);
    const before = (await form.summary.boundingBox())!.height;
    await form.summary.fill(Array.from({ length: 12 }, (_, i) => `Line ${i + 1} of a long summary`).join("\n"));
    const after = (await form.summary.boundingBox())!.height;
    expect(after).toBeGreaterThan(before + 40);
  });

  test("new organization: a blank form saves and opens the new record", async ({ page }) => {
    // Given a blank form
    const api = new FakeApi(page);
    await api.on("POST", "/api/organizations", { body: { ok: true, id: "o9" } });
    await api.on("GET", "/api/organizations/o9", { body: { ...faithtechDetail, id: "o9", name: "Kingdom Code" } });
    const form = new OrganizationFormPage(page);
    await form.openNew();
    await expect(form.heading).toHaveText("New organization");
    await expect(form.name).toHaveValue("");
    // When the user fills the required fields and saves
    await form.name.fill("Kingdom Code");
    await form.country.fill("United Kingdom");
    await form.website.fill("kingdomcode.org");
    await form.save.click();
    // Then it is created and its page opens
    await expect(page).toHaveURL(/\/organizations\/o9$/);
    expect(api.sent("POST", "/api/organizations")[0].body).toMatchObject({ name: "Kingdom Code", country: "United Kingdom", website: "kingdomcode.org" });
  });
});
